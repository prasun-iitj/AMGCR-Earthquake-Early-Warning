#!/usr/bin/env python3
"""IRIS / EarthScope FDSN pilot: California events and miniSEED waveforms.

Standalone acquisition script (not part of the EarthESND pipeline). Event metadata
is retrieved via the USGS FDSN event service; waveforms via EarthScope dataselect
(ObsPy client short name ``EARTHSCOPE``, formerly IRIS).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import FDSNException, FDSNNoDataException

REPO_ROOT = Path(__file__).resolve().parents[2]
EVENT_FDSN_BASE_URL = "https://earthquake.usgs.gov"
WAVEFORM_FDSN_BASE_URL = "https://service.earthscope.org"
DEFAULT_NETWORKS = "CI,NC,BK"
DEFAULT_START = "2024-01-01T00:00:00"
DEFAULT_END = "2024-12-31T23:59:59"
DEFAULT_MIN_MAG = 4.0
DEFAULT_MAX_MAG = 7.5
DEFAULT_EVENT_COUNT = 8
DEFAULT_MIN_EVENTS = 5
# Approximate California bounding box (WGS84)
CA_MIN_LAT = 32.5
CA_MAX_LAT = 42.0
CA_MIN_LON = -124.5
CA_MAX_LON = -114.0
WAVEFORM_DURATION_S = 300
MAX_STATIONS_PER_EVENT = 1
STATION_SEARCH_RADIUS_DEG = 3.0
MAX_CATALOG_SCAN = 100
MAX_CHANNEL_ATTEMPTS = 5
FDSN_RETRIES = 2
FDSN_RETRY_DELAY_S = 1.0


def _fdsn_call(func, *args, **kwargs):
    last_exc: Exception | None = None
    for attempt in range(FDSN_RETRIES):
        try:
            return func(*args, **kwargs)
        except FDSNNoDataException:
            raise
        except (FDSNException, ConnectionError, TimeoutError, OSError) as exc:
            last_exc = exc
            if attempt + 1 < FDSN_RETRIES:
                time.sleep(FDSN_RETRY_DELAY_S * (attempt + 1))
    assert last_exc is not None
    raise last_exc


CHANNEL = "BHZ"

# Pilot waveform targets: network, station, location, channel, lat, lon (approximate).
CA_WAVEFORM_CANDIDATES: list[tuple[str, str, str, str, float, float]] = [
    ("CI", "PAS", "", "BHZ", 34.148, -118.171),
    ("CI", "USC", "", "BHZ", 34.019, -118.286),
    ("CI", "WNG", "", "BHZ", 34.042, -118.467),
    ("CI", "SYP", "", "BHZ", 34.344, -118.442),
    ("CI", "VLY", "", "BHZ", 34.186, -118.629),
    ("CI", "CPO", "", "BHZ", 33.919, -117.512),
    ("CI", "RVR", "", "BHZ", 33.993, -117.376),
    ("CI", "LUC2", "", "BHZ", 34.432, -118.607),
    ("CI", "SMP", "", "BHZ", 34.009, -118.497),
    ("CI", "ADO", "", "BHZ", 34.550, -117.439),
    ("NC", "CMB", "", "BHZ", 38.455, -120.642),
    ("NC", "BKS", "", "BHZ", 37.874, -122.235),
    ("NC", "SAO", "", "BHZ", 37.424, -122.174),
    ("BK", "CMB", "", "BHZ", 38.455, -120.642),
    ("BK", "KCC", "", "BHZ", 37.374, -118.419),
    ("BK", "JRC2", "", "BHZ", 37.691, -118.937),
]


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius_km * math.asin(min(1.0, math.sqrt(a)))


def _waveform_candidates(latitude: float, longitude: float) -> list[tuple[str, str, str, str]]:
    ranked = sorted(
        CA_WAVEFORM_CANDIDATES,
        key=lambda row: _haversine_km(latitude, longitude, row[4], row[5]),
    )
    return [(net, sta, loc, cha) for net, sta, loc, cha, _, _ in ranked[:MAX_CHANNEL_ATTEMPTS]]


@dataclass
class PilotSummary:
    event_fdsn_base_url: str
    waveform_fdsn_base_url: str
    start_time: str
    end_time: str
    min_latitude: float
    max_latitude: float
    min_longitude: float
    max_longitude: float
    min_magnitude: float
    max_magnitude: float
    target_event_count: int
    networks: str
    channel: str
    waveform_duration_s: int
    station_search_radius_deg: float = STATION_SEARCH_RADIUS_DEG
    max_stations_per_event: int = MAX_STATIONS_PER_EVENT
    events_requested: int = 0
    events_with_waveforms: int = 0
    magnitude_min_observed: float | None = None
    magnitude_max_observed: float | None = None
    origin_time_min: str | None = None
    origin_time_max: str | None = None
    stations: set[str] = field(default_factory=set)
    event_rows: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _repo_path(*parts: str) -> Path:
    return REPO_ROOT.joinpath(*parts)


def _event_id(event: Any, index: int) -> str:
    if event.resource_id:
        rid = str(event.resource_id.id)
        for ch in (":", "/", "?", "&", "=", "\\", "|", "*", "<", ">", '"'):
            rid = rid.replace(ch, "_")
        rid = rid.strip("_")
        return rid[:120] or f"event_{index:03d}"
    return f"event_{index:03d}"


def _preferred_magnitude(event: Any) -> tuple[float | None, str | None]:
    if not event.magnitudes:
        return None, None
    mag = event.magnitudes[0]
    return float(mag.mag), str(mag.magnitude_type or "")


def _search_events(client: Client, summary: PilotSummary) -> Any:
    return client.get_events(
        starttime=UTCDateTime(summary.start_time),
        endtime=UTCDateTime(summary.end_time),
        minlatitude=summary.min_latitude,
        maxlatitude=summary.max_latitude,
        minlongitude=summary.min_longitude,
        maxlongitude=summary.max_longitude,
        minmagnitude=summary.min_magnitude,
        maxmagnitude=summary.max_magnitude,
        orderby="time",
    )


def _download_event_waveforms(
    client: Client,
    summary: PilotSummary,
    event: Any,
    event_key: str,
    raw_dir: Path,
) -> list[str]:
    origin = event.preferred_origin() or event.origins[0]
    ot = origin.time
    saved: list[str] = []
    event_dir = raw_dir / event_key
    event_dir.mkdir(parents=True, exist_ok=True)

    station_triples = _waveform_candidates(float(origin.latitude), float(origin.longitude))
    if not station_triples:
        summary.errors.append(f"No stations found for event {event_key}")
        return saved

    for net, sta, loc, cha in station_triples:
        loc_label = loc if loc else "--"
        summary.stations.add(f"{net}.{sta}.{loc_label}.{cha}")
        try:
            stream = _fdsn_call(
                client.get_waveforms,
                network=net,
                station=sta,
                location=loc,
                channel=cha,
                starttime=ot,
                endtime=ot + summary.waveform_duration_s,
            )
        except FDSNNoDataException:
            continue
        except FDSNException:
            continue

        if len(stream) == 0:
            continue
        filename = f"{net}.{sta}.{loc_label}.{cha}.{ot.strftime('%Y%m%dT%H%M%S')}.mseed"
        path = event_dir / filename
        stream.merge(method=1, fill_value="interpolate")
        stream.write(str(path), format="MSEED")
        if path.stat().st_size > 0:
            saved.append(str(path.relative_to(raw_dir)).replace("\\", "/"))
            break

    if not saved and station_triples:
        summary.errors.append(f"No waveform bytes for event {event_key}")

    return saved


def _write_events_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _update_magnitude_range(summary: PilotSummary, mag: float | None) -> None:
    if mag is None:
        return
    if summary.magnitude_min_observed is None or mag < summary.magnitude_min_observed:
        summary.magnitude_min_observed = mag
    if summary.magnitude_max_observed is None or mag > summary.magnitude_max_observed:
        summary.magnitude_max_observed = mag


def run_pilot(
    *,
    raw_dir: Path | None = None,
    manifest_csv: Path | None = None,
    summary_json: Path | None = None,
    event_count: int = DEFAULT_EVENT_COUNT,
    min_events: int = DEFAULT_MIN_EVENTS,
) -> PilotSummary:
    raw_dir = raw_dir or _repo_path("data", "raw", "iris")
    manifest_csv = manifest_csv or _repo_path(
        "data", "manifests", "iris_california_pilot_events.csv"
    )
    summary_json = summary_json or _repo_path("logs", "iris_california_pilot_summary.json")
    raw_dir.mkdir(parents=True, exist_ok=True)

    summary = PilotSummary(
        event_fdsn_base_url=EVENT_FDSN_BASE_URL,
        waveform_fdsn_base_url=WAVEFORM_FDSN_BASE_URL,
        start_time=DEFAULT_START,
        end_time=DEFAULT_END,
        min_latitude=CA_MIN_LAT,
        max_latitude=CA_MAX_LAT,
        min_longitude=CA_MIN_LON,
        max_longitude=CA_MAX_LON,
        min_magnitude=DEFAULT_MIN_MAG,
        max_magnitude=DEFAULT_MAX_MAG,
        target_event_count=event_count,
        networks=DEFAULT_NETWORKS,
        channel=CHANNEL,
        waveform_duration_s=WAVEFORM_DURATION_S,
    )

    event_client = Client(EVENT_FDSN_BASE_URL, timeout=120)
    waveform_client = Client("EARTHSCOPE", timeout=120)
    catalog = _search_events(event_client, summary)
    summary.events_requested = min(len(catalog), event_count)

    selected: list[Any] = []
    scan_limit = len(catalog)
    for event in list(catalog)[:scan_limit]:
        if len(selected) >= event_count:
            break
        try:
            origin = event.preferred_origin() or event.origins[0]
            mag, mag_type = _preferred_magnitude(event)
            ot_iso = origin.time.isoformat()
            event_key = _event_id(event, len(selected) + 1)
            waveforms = _download_event_waveforms(
                waveform_client, summary, event, event_key, raw_dir
            )
        except (FDSNException, ConnectionError, TimeoutError, OSError) as exc:
            summary.errors.append(f"event skipped due to network error: {exc}")
            continue
        if not waveforms:
            continue

        _update_magnitude_range(summary, mag)
        if summary.origin_time_min is None or ot_iso < summary.origin_time_min:
            summary.origin_time_min = ot_iso
        if summary.origin_time_max is None or ot_iso > summary.origin_time_max:
            summary.origin_time_max = ot_iso

        summary.events_with_waveforms += 1
        selected.append(event)
        summary.event_rows.append(
            {
                "event_id": event_key,
                "origin_time_utc": ot_iso,
                "latitude": float(origin.latitude),
                "longitude": float(origin.longitude),
                "depth_km": float(origin.depth) / 1000.0 if origin.depth is not None else "",
                "magnitude": mag if mag is not None else "",
                "magnitude_type": mag_type or "",
                "waveform_file_count": len(waveforms),
                "waveform_files": ";".join(waveforms),
                "fdsn_event_provider": "USGS",
                "fdsn_waveform_provider": "EARTHSCOPE",
            }
        )

    summary.events_requested = len(selected)

    if len(selected) < min_events:
        raise RuntimeError(
            f"Waveforms retrieved for {len(selected)} events; need at least {min_events}."
        )

    _write_events_csv(manifest_csv, summary.event_rows)
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "manifest_csv": str(manifest_csv.resolve()),
        "raw_dir": str(raw_dir.resolve()),
        "query": {
            "event_fdsn_base_url": summary.event_fdsn_base_url,
            "waveform_fdsn_base_url": summary.waveform_fdsn_base_url,
            "start_time": summary.start_time,
            "end_time": summary.end_time,
            "minlatitude": summary.min_latitude,
            "maxlatitude": summary.max_latitude,
            "minlongitude": summary.min_longitude,
            "maxlongitude": summary.max_longitude,
            "minmagnitude": summary.min_magnitude,
            "maxmagnitude": summary.max_magnitude,
            "networks": summary.networks,
            "channel_preference": summary.channel,
            "waveform_duration_s": summary.waveform_duration_s,
            "max_stations_per_event": summary.max_stations_per_event,
            "station_search_radius_deg": summary.station_search_radius_deg,
            "target_event_count": summary.target_event_count,
        },
        "events_catalog_matches": len(catalog),
        "events_selected": len(selected),
        "events_with_waveforms": summary.events_with_waveforms,
        "magnitude_min_observed": summary.magnitude_min_observed,
        "magnitude_max_observed": summary.magnitude_max_observed,
        "origin_time_min": summary.origin_time_min,
        "origin_time_max": summary.origin_time_max,
        "stations": sorted(summary.stations),
        "errors": summary.errors,
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return summary


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download a small IRIS FDSN pilot dataset for California earthquakes."
    )
    parser.add_argument("--event-count", type=int, default=DEFAULT_EVENT_COUNT)
    parser.add_argument("--min-events", type=int, default=DEFAULT_MIN_EVENTS)
    parser.add_argument("--raw-dir", type=Path, default=None)
    parser.add_argument("--manifest-csv", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        summary = run_pilot(
            raw_dir=args.raw_dir,
            manifest_csv=args.manifest_csv,
            event_count=args.event_count,
            min_events=args.min_events,
        )
    except (RuntimeError, FDSNException) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "events_with_waveforms": summary.events_with_waveforms,
                "stations": sorted(summary.stations),
                "manifest": str(
                    (args.manifest_csv or _repo_path("data", "manifests", "iris_california_pilot_events.csv")).resolve()
                ),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
