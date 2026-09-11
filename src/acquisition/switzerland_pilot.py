"""Swiss methods-transfer pilot: SED/ETH FDSN helpers (no California coupling).

Pure functions for configuration, event IDs, acquisition windows, availability
parsing, station selection, MiniSEED validation, and manifest rows. Network I/O
lives in ``scripts/download/download_sed_switzerland_pilot.py``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from obspy import Stream, UTCDateTime

from src.acquisition.exceptions import AcquisitionConfigurationError

MANIFEST_FIELDS: tuple[str, ...] = (
    "event_id",
    "origin_time_utc",
    "latitude",
    "longitude",
    "depth_km",
    "magnitude",
    "magnitude_type",
    "region",
    "network",
    "station",
    "location",
    "channels",
    "sampling_rate_hz",
    "waveform_start_utc",
    "waveform_end_utc",
    "pre_event_seconds",
    "post_event_seconds",
    "stationxml_available",
    "waveform_file",
    "download_status",
    "validation_status",
)

HH_3C = ("HHZ", "HHN", "HHE")
BH_3C = ("BHZ", "BHN", "BHE")


def load_switzerland_config(path: str | Path) -> dict[str, Any]:
    """Load and validate the Swiss pilot YAML configuration."""
    config_path = Path(path)
    if not config_path.exists():
        raise AcquisitionConfigurationError(f"Swiss pilot config not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}
    if not isinstance(config, dict):
        raise AcquisitionConfigurationError("Swiss pilot config must be a YAML mapping.")
    validate_switzerland_config(config)
    return config


def validate_switzerland_config(config: dict[str, Any]) -> None:
    """Raise if required Swiss pilot keys are missing or malformed."""
    endpoints = config.get("endpoints")
    if not isinstance(endpoints, dict):
        raise AcquisitionConfigurationError("endpoints must be a mapping.")
    for key in ("event", "station", "dataselect", "availability"):
        value = endpoints.get(key)
        if not isinstance(value, str) or not value.strip():
            raise AcquisitionConfigurationError(f"endpoints.{key} must be a non-empty string.")

    event_ids = config.get("event_ids")
    if not isinstance(event_ids, list) or not event_ids:
        raise AcquisitionConfigurationError("event_ids must be a non-empty list.")
    for item in event_ids:
        if not isinstance(item, str) or not item.strip():
            raise AcquisitionConfigurationError("each event_id must be a non-empty string.")
        if event_short_id(item) != item.strip():
            raise AcquisitionConfigurationError(
                f"event_ids must be short IDs (got {item!r}); full resource IDs are resolved from SED."
            )

    window = config.get("window")
    if not isinstance(window, dict):
        raise AcquisitionConfigurationError("window must be a mapping.")
    for key in ("pre_event_seconds", "post_event_seconds"):
        value = window.get(key)
        if not isinstance(value, (int, float)) or value <= 0:
            raise AcquisitionConfigurationError(f"window.{key} must be a positive number.")

    selection = config.get("station_selection")
    if not isinstance(selection, dict):
        raise AcquisitionConfigurationError("station_selection must be a mapping.")
    if selection.get("network") != "CH":
        raise AcquisitionConfigurationError("station_selection.network must be CH for this pilot.")

    output = config.get("output")
    if not isinstance(output, dict):
        raise AcquisitionConfigurationError("output must be a mapping.")
    for key in ("raw_dir", "metadata_dir", "manifest_csv", "logs_dir"):
        value = output.get(key)
        if not isinstance(value, str) or not value.strip():
            raise AcquisitionConfigurationError(f"output.{key} must be a non-empty string.")
        if "iris" in Path(value).as_posix().lower() or "california" in Path(value).as_posix().lower():
            raise AcquisitionConfigurationError(
                f"output.{key} must not point at California/IRIS paths: {value}"
            )


def event_short_id(resource_id: str) -> str:
    """Return the trailing SED event token (e.g. 2020btnrcj)."""
    text = str(resource_id).strip().rstrip("/")
    if not text:
        return ""
    return text.rsplit("/", 1)[-1]


def acquisition_window(
    origin: UTCDateTime,
    pre_event_seconds: float,
    post_event_seconds: float,
) -> tuple[UTCDateTime, UTCDateTime]:
    """Return (start, end) as origin−pre and origin+post. Not origin-aligned."""
    if pre_event_seconds <= 0 or post_event_seconds <= 0:
        raise ValueError("pre_event_seconds and post_event_seconds must be positive.")
    return origin - float(pre_event_seconds), origin + float(post_event_seconds)


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometres."""
    radius_km = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius_km * math.asin(min(1.0, math.sqrt(a)))


def parse_availability_text(text: str) -> list[dict[str, Any]]:
    """Parse FDSN availability text. Skip inverted or malformed time spans."""
    rows: list[dict[str, Any]] = []
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("|") if "|" in line else line.split()
        if len(parts) < 8:
            continue
        try:
            earliest = UTCDateTime(parts[6].strip())
            latest = UTCDateTime(parts[7].strip())
            rate = float(parts[5]) if parts[5] else None
        except (TypeError, ValueError):
            continue
        if latest < earliest:
            continue
        loc = parts[2].strip()
        if loc in {"", "--"}:
            loc = ""
        rows.append(
            {
                "network": parts[0].strip(),
                "station": parts[1].strip(),
                "location": loc,
                "channel": parts[3].strip(),
                "quality": parts[4].strip(),
                "sample_rate": rate,
                "earliest": earliest,
                "latest": latest,
            }
        )
    return rows


def has_three_component(channels: set[str], band: str) -> bool:
    """True when Z/N/E exist for the given band (HH or BH)."""
    needed = {f"{band}Z", f"{band}N", f"{band}E"}
    return needed.issubset(channels)


@dataclass
class StationCandidate:
    """One CH station/location with availability in the request window."""

    network: str
    station: str
    location: str
    channels: set[str]
    sample_rates_hz: set[float]
    earliest: UTCDateTime
    latest: UTCDateTime
    latitude: float | None = None
    longitude: float | None = None
    distance_km: float | None = None
    site: str = ""

    @property
    def has_hh_3c(self) -> bool:
        return has_three_component(self.channels, "HH")

    @property
    def has_bh_3c(self) -> bool:
        return has_three_component(self.channels, "BH")

    @property
    def preferred_band(self) -> str | None:
        if self.has_hh_3c:
            return "HH"
        if self.has_bh_3c:
            return "BH"
        return None

    @property
    def download_channels(self) -> tuple[str, ...]:
        band = self.preferred_band
        if band == "HH":
            return HH_3C
        if band == "BH":
            return BH_3C
        return tuple(sorted(self.channels))


def group_availability_by_station(
    rows: list[dict[str, Any]],
    origin: UTCDateTime,
    pre_event_seconds: float,
    post_event_seconds: float,
    network: str = "CH",
) -> list[StationCandidate]:
    """Collapse availability rows into per-station candidates covering the window."""
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    window_start = origin - pre_event_seconds
    window_end = origin + post_event_seconds
    for row in rows:
        if row["network"] != network:
            continue
        if row["latest"] < window_start or row["earliest"] > window_end:
            continue
        key = (row["network"], row["station"], row["location"])
        grouped.setdefault(key, []).append(row)

    candidates: list[StationCandidate] = []
    for (net, sta, loc), items in grouped.items():
        earliest = min(item["earliest"] for item in items)
        latest = max(item["latest"] for item in items)
        if earliest > origin - 30.0:
            continue
        if latest < origin + 30.0:
            continue
        rates = {item["sample_rate"] for item in items if item["sample_rate"] is not None}
        candidates.append(
            StationCandidate(
                network=net,
                station=sta,
                location=loc,
                channels={item["channel"] for item in items},
                sample_rates_hz={float(r) for r in rates},
                earliest=earliest,
                latest=latest,
            )
        )
    return candidates


def attach_coordinates(
    candidates: list[StationCandidate],
    station_coords: dict[str, dict[str, Any]],
    event_lat: float,
    event_lon: float,
) -> None:
    """Fill lat/lon/distance on candidates from a station metadata map."""
    for candidate in candidates:
        meta = station_coords.get(candidate.station)
        if not meta:
            continue
        candidate.latitude = float(meta["latitude"])
        candidate.longitude = float(meta["longitude"])
        candidate.site = str(meta.get("site") or "")
        candidate.distance_km = haversine_km(event_lat, event_lon, candidate.latitude, candidate.longitude)


def distance_bin_index(distance_km: float, edges: list[float]) -> int:
    """Return bin index for distance_km given increasing edges. Last bin is open-ended."""
    if distance_km < 0:
        return 0
    for index in range(len(edges) - 1):
        if edges[index] <= distance_km < edges[index + 1]:
            return index
    return max(0, len(edges) - 2)


def select_stations(
    candidates: list[StationCandidate],
    *,
    max_stations: int,
    bin_edges_km: list[float],
    max_per_bin: int,
    prefer_three_component: bool = True,
    allow_incomplete: bool = False,
) -> list[StationCandidate]:
    """Select stations with 3C preference and distance-bin diversity (not nearest-only)."""
    if max_stations <= 0:
        return []

    suitable = [c for c in candidates if c.preferred_band is not None]
    if not suitable and allow_incomplete:
        suitable = [c for c in candidates if any(ch.endswith("Z") for ch in c.channels)]
    if prefer_three_component and not suitable and not allow_incomplete:
        return []
    if not suitable:
        return []

    located = [c for c in suitable if c.distance_km is not None]
    unlocated = [c for c in suitable if c.distance_km is None]

    def sort_key(item: StationCandidate) -> tuple:
        return (
            0 if item.has_hh_3c else 1,
            0 if item.has_bh_3c else 1,
            item.distance_km if item.distance_km is not None else 1e9,
            item.station,
        )

    selected: list[StationCandidate] = []
    selected_ids: set[str] = set()
    if located and len(bin_edges_km) >= 2:
        n_bins = len(bin_edges_km) - 1
        buckets: list[list[StationCandidate]] = [[] for _ in range(n_bins)]
        for item in located:
            buckets[distance_bin_index(item.distance_km or 0.0, bin_edges_km)].append(item)
        for bucket in buckets:
            bucket.sort(key=sort_key)
            for item in bucket[:max_per_bin]:
                if item.station in selected_ids:
                    continue
                selected.append(item)
                selected_ids.add(item.station)
                if len(selected) >= max_stations:
                    return selected

    remaining = [c for c in sorted(located, key=sort_key) if c.station not in selected_ids]
    remaining.extend(sorted(unlocated, key=lambda c: c.station))
    for item in remaining:
        if len(selected) >= max_stations:
            break
        if item.station in selected_ids:
            continue
        selected.append(item)
        selected_ids.add(item.station)
    return selected


def location_label(location: str) -> str:
    """FDSN empty location as ``--`` for filenames."""
    return location if location else "--"


def sampling_rate_label(rates: set[float], band: str | None) -> str:
    """Manifest sampling-rate string for the downloaded band."""
    if not rates:
        return ""
    if band == "HH":
        hh = [r for r in rates if r >= 80]
        if hh:
            return ";".join(str(r) for r in sorted(hh))
    if band == "BH":
        bh = [r for r in rates if 20 <= r <= 80]
        if bh:
            return ";".join(str(r) for r in sorted(bh))
    return ";".join(str(r) for r in sorted(rates))


@dataclass
class WaveformValidation:
    """Result of reading a downloaded MiniSEED stream against the origin window."""

    readable: bool
    origin_inside: bool
    pre_event_seconds: float | None
    post_event_seconds: float | None
    sampling_rate_hz: str
    channels: list[str]
    complete_3c: bool
    n_traces: int
    starttime: str
    endtime: str
    status: str
    notes: list[str] = field(default_factory=list)


def validate_stream(
    stream: Stream,
    origin: UTCDateTime,
    min_pre_event_seconds: float,
    min_post_event_seconds: float,
) -> WaveformValidation:
    """Validate actual traces. Failures are returned, not raised away."""
    notes: list[str] = []
    if stream is None or len(stream) == 0:
        return WaveformValidation(
            readable=False,
            origin_inside=False,
            pre_event_seconds=None,
            post_event_seconds=None,
            sampling_rate_hz="",
            channels=[],
            complete_3c=False,
            n_traces=0,
            starttime="",
            endtime="",
            status="FAIL",
            notes=["empty or unreadable stream"],
        )

    merged = stream.copy()
    merged.merge(method=1, fill_value="interpolate")
    start = min(tr.stats.starttime for tr in merged)
    end = max(tr.stats.endtime for tr in merged)
    channels = sorted({str(tr.stats.channel) for tr in merged})
    rates = sorted({float(tr.stats.sampling_rate) for tr in merged})
    pre_s = float(origin - start)
    post_s = float(end - origin)
    origin_inside = start <= origin <= end
    bands = {ch[:2] for ch in channels if len(ch) >= 3}
    complete_3c = any(has_three_component(set(channels), band) for band in bands)

    if not origin_inside:
        notes.append("origin not inside waveform interval")
    if pre_s < min_pre_event_seconds:
        notes.append(f"pre-event {pre_s:.1f}s < {min_pre_event_seconds:.1f}s")
    if post_s < min_post_event_seconds:
        notes.append(f"post-event {post_s:.1f}s < {min_post_event_seconds:.1f}s")
    if not complete_3c:
        notes.append("incomplete three-component set")

    if not origin_inside:
        status = "FAIL"
    elif pre_s < min_pre_event_seconds or post_s < min_post_event_seconds:
        status = "PARTIAL"
    else:
        status = "PASS"

    return WaveformValidation(
        readable=True,
        origin_inside=origin_inside,
        pre_event_seconds=round(pre_s, 3),
        post_event_seconds=round(post_s, 3),
        sampling_rate_hz=";".join(str(r) for r in rates),
        channels=channels,
        complete_3c=complete_3c,
        n_traces=len(merged),
        starttime=str(start),
        endtime=str(end),
        status=status,
        notes=notes,
    )


def empty_manifest_row(event: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    """Build a manifest row with required keys; missing fields stay empty."""
    row = {key: "" for key in MANIFEST_FIELDS}
    row["event_id"] = event.get("event_id", "")
    row["origin_time_utc"] = event.get("origin_time_utc", "")
    row["latitude"] = event.get("latitude", "")
    row["longitude"] = event.get("longitude", "")
    row["depth_km"] = event.get("depth_km", "")
    row["magnitude"] = event.get("magnitude", "")
    row["magnitude_type"] = event.get("magnitude_type", "")
    row["region"] = event.get("region", "")
    row["download_status"] = "FAILED"
    row["validation_status"] = "NOT_RUN"
    row.update(overrides)
    return row


def utc_now_iso() -> str:
    """UTC timestamp for logs."""
    return datetime.now(timezone.utc).isoformat()
