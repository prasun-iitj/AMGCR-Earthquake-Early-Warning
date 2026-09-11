"""Independent Swiss validation-set audit helpers (no STA/LTA, no waveform download).

The 20-event development IDs are excluded by construction. Selection never uses
automatic trigger quality.
"""

from __future__ import annotations

import csv
import re
from io import BytesIO
from pathlib import Path
from typing import Any

import yaml

from src.acquisition.exceptions import AcquisitionConfigurationError
from src.acquisition.switzerland_pilot import event_short_id, haversine_km

NEIGHBOUR_REGION_SUFFIX = re.compile(r"\s+(F|I|D|A|A[Uu]|IT|FR|DE|AT|FL|LI)\.?$", re.IGNORECASE)

CANDIDATE_FIELDS: tuple[str, ...] = (
    "short_id",
    "event_id",
    "origin_time_utc",
    "latitude",
    "longitude",
    "depth_km",
    "magnitude",
    "magnitude_type",
    "region",
    "event_type",
    "location_class",
    "in_development_set",
    "pool_role",
    "proposed_validation",
    "n_ch_p_picks",
    "n_ch_manual_p_picks",
    "n_ch_hhz_p_picks",
    "n_unique_ch_stations_with_first_p",
    "sed_p_pick_available",
    "sed_p_pick_modes",
    "n_unique_ch_stations_with_hh_3c",
    "n_unique_ch_stations_with_hhz",
    "acquisition_window_obtainable",
    "n_same_station_first_p_and_hhz",
    "n_same_station_hhz_first_p_and_hhz",
    "stationxml_status",
    "exclusion_concern",
)


def load_validation_audit_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise AcquisitionConfigurationError(f"validation audit config not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}
    if not isinstance(config, dict):
        raise AcquisitionConfigurationError("validation audit config must be a YAML mapping.")
    validate_validation_audit_config(config)
    return config


def validate_validation_audit_config(config: dict[str, Any]) -> None:
    frozen = config.get("frozen_configuration")
    if not isinstance(frozen, dict) or float(frozen.get("trigger_on", 0)) != 8.0:
        raise AcquisitionConfigurationError("frozen_configuration.trigger_on must be 8.0 (pre-declared, not retuned).")
    if float(frozen.get("search_start_offset_s", -1)) != 0.0:
        raise AcquisitionConfigurationError("official search must start at origin (offset 0).")
    if float(frozen.get("search_end_offset_s", 0)) != 90.0:
        raise AcquisitionConfigurationError("official search must end at origin + 90 s.")
    windows = config.get("windows")
    if not isinstance(windows, dict):
        raise AcquisitionConfigurationError("windows must distinguish acquisition, detection, and pre_event_noise.")
    offsets = window_offsets(config)
    acq_start, acq_end = offsets["acquisition"]
    det_start, det_end = offsets["detection"]
    noise_start, noise_end = offsets["pre_event_noise"]
    if (acq_start, acq_end) != (-60.0, 90.0):
        raise AcquisitionConfigurationError("acquisition window must be origin-60 s to origin+90 s.")
    if (det_start, det_end) != (0.0, 90.0):
        raise AcquisitionConfigurationError("detection window must be origin to origin+90 s.")
    if det_start < 0.0:
        raise AcquisitionConfigurationError("detection must not begin before origin.")
    if (noise_start, noise_end) != (-60.0, -10.0):
        raise AcquisitionConfigurationError("pre-event noise window must be origin-60 s to origin-10 s.")
    locked = config.get("locked_proposed_event_ids")
    if not isinstance(locked, list) or len(locked) != 15:
        raise AcquisitionConfigurationError("locked_proposed_event_ids must list exactly 15 short IDs.")
    if len(set(locked)) != 15:
        raise AcquisitionConfigurationError("locked proposed event IDs must be unique.")
    development = config.get("development_dataset", {})
    ids = development.get("event_ids")
    if not isinstance(ids, list) or len(ids) != 20:
        raise AcquisitionConfigurationError("development_dataset.event_ids must list exactly 20 short IDs.")
    if len(set(ids)) != 20:
        raise AcquisitionConfigurationError("development event IDs must be unique.")
    locked_ids = {event_short_id(item) for item in config["locked_proposed_event_ids"]}
    overlap = locked_ids & {event_short_id(item) for item in ids}
    if overlap:
        raise AcquisitionConfigurationError(f"locked proposed IDs overlap development set: {sorted(overlap)}")


def window_offsets(config: dict[str, Any]) -> dict[str, tuple[float, float]]:
    """Return (start_offset_s, end_offset_s) for the three distinct validation windows."""
    windows = config["windows"]
    return {
        "acquisition": (
            float(windows["acquisition"]["start_offset_s"]),
            float(windows["acquisition"]["end_offset_s"]),
        ),
        "detection": (
            float(windows["detection"]["start_offset_s"]),
            float(windows["detection"]["end_offset_s"]),
        ),
        "pre_event_noise": (
            float(windows["pre_event_noise"]["start_offset_s"]),
            float(windows["pre_event_noise"]["end_offset_s"]),
        ),
    }


def apply_window_offsets(origin: Any, start_offset_s: float, end_offset_s: float) -> tuple[Any, Any]:
    """Apply offsets to an origin (ObsPy UTCDateTime or equivalent)."""
    return origin + float(start_offset_s), origin + float(end_offset_s)


def locked_proposed_short_ids(config: dict[str, Any]) -> list[str]:
    return [event_short_id(item) for item in config["locked_proposed_event_ids"]]


def development_short_ids(config: dict[str, Any]) -> set[str]:
    return {event_short_id(item) for item in config["development_dataset"]["event_ids"]}


def is_allowed_event_type(event_type: str, allowed: list[str]) -> bool:
    text = (event_type or "").strip().lower()
    return text in {item.strip().lower() for item in allowed}


def classify_location(latitude: float, longitude: float, region: str, swiss_box: dict[str, Any]) -> str:
    """Label Swiss interior vs immediate-border from SED region text and a coarse box."""
    region_text = (region or "").strip()
    if NEIGHBOUR_REGION_SUFFIX.search(region_text):
        return "immediate_border"
    inside = (
        float(swiss_box["minlatitude"]) <= float(latitude) <= float(swiss_box["maxlatitude"])
        and float(swiss_box["minlongitude"]) <= float(longitude) <= float(swiss_box["maxlongitude"])
    )
    return "swiss_territory" if inside else "immediate_border"


def overlaps_development(short_id: str, development_ids: set[str]) -> bool:
    return event_short_id(short_id) in development_ids


def year_bin(origin_time_utc: str, bins: list[list[int]]) -> str:
    year = int(str(origin_time_utc)[:4])
    for start, end in bins:
        if start <= year <= end:
            return f"{start}-{end}"
    return "other"


def magnitude_bin(magnitude: float, bins: list[list[float]]) -> str:
    for lo, hi in bins:
        if lo <= float(magnitude) < hi:
            return f"{lo}-{hi}"
    return "other"


def geo_quadrant(latitude: float, longitude: float, lat_split: float, lon_split: float) -> str:
    ns = "N" if float(latitude) >= float(lat_split) else "S"
    ew = "E" if float(longitude) >= float(lon_split) else "W"
    return f"{ns}{ew}"


def diversity_key(event: dict[str, Any], diversity: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        year_bin(str(event["origin_time_utc"]), diversity["year_bins"]),
        magnitude_bin(float(event["magnitude"]), diversity["magnitude_bins"]),
        geo_quadrant(float(event["latitude"]), float(event["longitude"]), diversity["lat_split"], diversity["lon_split"]),
        str(event.get("location_class", "")),
    )


def _pick_score(event: dict[str, Any]) -> tuple[int, int]:
    """Reference-availability score only. Never uses STA/LTA quality or magnitude rank."""
    n_p = int(event.get("n_ch_p_picks") or 0)
    n_stations = int(event.get("n_ch_p_stations") or 0)
    return (n_p, n_stations)


def year_quotas(n_proposed: int, n_bins: int, explicit: list[int] | None = None) -> list[int]:
    if explicit:
        if len(explicit) != n_bins:
            raise AcquisitionConfigurationError("diversity.year_quotas must match year_bins length.")
        if sum(explicit) != n_proposed:
            raise AcquisitionConfigurationError("diversity.year_quotas must sum to n_proposed.")
        return [int(v) for v in explicit]
    base, rem = divmod(int(n_proposed), int(n_bins))
    return [base + (1 if i < rem else 0) for i in range(n_bins)]


def too_close(event: dict[str, Any], selected: list[dict[str, Any]], min_km: float) -> bool:
    for other in selected:
        dist = haversine_km(
            float(event["latitude"]),
            float(event["longitude"]),
            float(other["latitude"]),
            float(other["longitude"]),
        )
        if dist < float(min_km):
            return True
    return False


def _secondary_key(event: dict[str, Any], diversity: dict[str, Any]) -> tuple[str, str, str]:
    return (
        magnitude_bin(float(event["magnitude"]), diversity["magnitude_bins"]),
        geo_quadrant(float(event["latitude"]), float(event["longitude"]), diversity["lat_split"], diversity["lon_split"]),
        str(event.get("location_class", "")),
    )


def _fill_from_year_bucket(
    events: list[dict[str, Any]],
    quota: int,
    selected: list[dict[str, Any]],
    selected_ids: set[str],
    diversity: dict[str, Any],
    min_separation_km: float,
    enforce_separation: bool,
) -> None:
    mag_labels = [f"{lo}-{hi}" for lo, hi in diversity["magnitude_bins"]]
    taken = 0
    progressed = True
    while taken < quota and progressed:
        progressed = False
        for mag_label in mag_labels:
            if taken >= quota:
                break
            subset = [
                event
                for event in events
                if event["short_id"] not in selected_ids
                and magnitude_bin(float(event["magnitude"]), diversity["magnitude_bins"]) == mag_label
            ]
            strata: dict[tuple[str, str], list[dict[str, Any]]] = {}
            for event in subset:
                key = (
                    geo_quadrant(
                        float(event["latitude"]),
                        float(event["longitude"]),
                        diversity["lat_split"],
                        diversity["lon_split"],
                    ),
                    str(event.get("location_class", "")),
                )
                strata.setdefault(key, []).append(event)
            choice = None
            for key in sorted(strata.keys()):
                bucket = sorted(strata[key], key=_pick_score, reverse=True)
                for event in bucket:
                    if enforce_separation and too_close(event, selected, min_separation_km):
                        continue
                    choice = event
                    break
                if choice is not None:
                    break
            if choice is None:
                continue
            selected.append(choice)
            selected_ids.add(choice["short_id"])
            taken += 1
            progressed = True


def propose_validation_subset(
    pool: list[dict[str, Any]],
    n_proposed: int,
    diversity: dict[str, Any],
    min_separation_km: float,
) -> list[str]:
    """Fill pre-declared year quotas, then mag/geo/border strata. Ignores STA/LTA."""
    remaining = [e for e in pool if not e.get("in_development_set")]
    bins = diversity["year_bins"]
    quotas = year_quotas(n_proposed, len(bins), diversity.get("year_quotas"))
    by_year: dict[str, list[dict[str, Any]]] = {f"{a}-{b}": [] for a, b in bins}
    for event in remaining:
        by_year.setdefault(year_bin(str(event["origin_time_utc"]), bins), []).append(event)

    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    year_keys = [f"{a}-{b}" for a, b in bins]
    for key, quota in zip(year_keys, quotas):
        _fill_from_year_bucket(
            by_year.get(key, []),
            quota,
            selected,
            selected_ids,
            diversity,
            min_separation_km,
            enforce_separation=True,
        )

    if len(selected) < n_proposed:
        leftover_needed = n_proposed - len(selected)
        _fill_from_year_bucket(
            remaining,
            leftover_needed,
            selected,
            selected_ids,
            diversity,
            min_separation_km,
            enforce_separation=True,
        )

    if len(selected) < n_proposed:
        remaining_sorted = sorted(remaining, key=_pick_score, reverse=True)
        for event in remaining_sorted:
            if event["short_id"] in selected_ids:
                continue
            if too_close(event, selected, min_separation_km):
                continue
            selected.append(event)
            selected_ids.add(event["short_id"])
            if len(selected) >= n_proposed:
                break
    if len(selected) < n_proposed:
        remaining_sorted = sorted(remaining, key=_pick_score, reverse=True)
        for event in remaining_sorted:
            if event["short_id"] in selected_ids:
                continue
            selected.append(event)
            selected_ids.add(event["short_id"])
            if len(selected) >= n_proposed:
                break
    min_swiss = int(diversity.get("min_swiss_territory") or 0)
    if min_swiss > 0:
        _enforce_swiss_count(remaining, selected, selected_ids, diversity, min_separation_km, min_swiss)
    return [e["short_id"] for e in selected[:n_proposed]]


def _enforce_swiss_count(
    remaining: list[dict[str, Any]],
    selected: list[dict[str, Any]],
    selected_ids: set[str],
    diversity: dict[str, Any],
    min_separation_km: float,
    min_swiss: int,
) -> None:
    """Swap border events for unused Swiss-territory events without using STA/LTA."""
    bins = diversity["year_bins"]

    def is_swiss(event: dict[str, Any]) -> bool:
        return str(event.get("location_class") or "") == "swiss_territory"

    while sum(1 for event in selected if is_swiss(event)) < min_swiss:
        border_index = next((i for i, event in enumerate(selected) if not is_swiss(event)), None)
        if border_index is None:
            break
        donor = selected[border_index]
        donor_year = year_bin(str(donor["origin_time_utc"]), bins)
        donor_mag = magnitude_bin(float(donor["magnitude"]), diversity["magnitude_bins"])
        others = [event for i, event in enumerate(selected) if i != border_index]
        candidates = [
            event
            for event in remaining
            if is_swiss(event) and event["short_id"] not in selected_ids
        ]
        same_year_mag = [
            event
            for event in candidates
            if year_bin(str(event["origin_time_utc"]), bins) == donor_year
            and magnitude_bin(float(event["magnitude"]), diversity["magnitude_bins"]) == donor_mag
        ]
        same_year = [
            event
            for event in candidates
            if year_bin(str(event["origin_time_utc"]), bins) == donor_year
        ]
        ordered = same_year_mag or same_year or candidates
        spaced = [event for event in ordered if not too_close(event, others, min_separation_km)]
        pool = spaced or ordered
        if not pool:
            break
        pool.sort(key=_pick_score, reverse=True)
        choice = pool[0]
        selected_ids.discard(donor["short_id"])
        selected[border_index] = choice
        selected_ids.add(choice["short_id"])


def next_replacement(
    pool: list[dict[str, Any]],
    selected: list[dict[str, Any]],
    failed: dict[str, Any],
    diversity: dict[str, Any],
    min_separation_km: float,
    *,
    same_year_only: bool = True,
) -> dict[str, Any] | None:
    """Pick the next unused pool event. Never uses STA/LTA quality."""
    selected_ids = {event["short_id"] for event in selected}
    year_pref = year_bin(str(failed["origin_time_utc"]), diversity["year_bins"])
    mag_pref = magnitude_bin(float(failed["magnitude"]), diversity["magnitude_bins"])
    ranked: list[tuple[int, int, int, dict[str, Any]]] = []
    for event in pool:
        if event["short_id"] in selected_ids or event.get("in_development_set"):
            continue
        if int(event.get("n_ch_p_picks") or 0) <= 0:
            continue
        if str(event.get("hh_3c_availability_verified") or "") in {"no", "timeout_or_empty"}:
            continue
        year_key = year_bin(str(event["origin_time_utc"]), diversity["year_bins"])
        if same_year_only and year_key != year_pref:
            continue
        if too_close(event, selected, min_separation_km):
            continue
        same_year = 0 if year_key == year_pref else 1
        same_mag = 0 if magnitude_bin(float(event["magnitude"]), diversity["magnitude_bins"]) == mag_pref else 1
        n_p = -int(event.get("n_ch_p_picks") or 0)
        ranked.append((same_year, same_mag, n_p, event))
    ranked.sort(key=lambda item: (item[0], item[1], item[2]))
    return ranked[0][3] if ranked else None


def empty_candidate_row() -> dict[str, Any]:
    return {key: "" for key in CANDIDATE_FIELDS}


def short_ids_from_manifest_csv(path: str | Path, event_id_field: str = "event_id") -> set[str]:
    """Unique short event IDs from an existing Swiss event-station manifest."""
    ids: set[str] = set()
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            value = row.get(event_id_field) or row.get("short_id") or ""
            if value:
                ids.add(event_short_id(value))
    return ids


def parse_quakeml_picks(xml_text: str) -> dict[str, list[dict[str, Any]]]:
    """Index QuakeML picks by short event ID. Does not interpret STA/LTA times."""
    from obspy import read_events

    catalog = read_events(BytesIO(xml_text.encode("utf-8")))
    by_event: dict[str, list[dict[str, Any]]] = {}
    for event in catalog:
        short_id = event_short_id(str(event.resource_id))
        picks: list[dict[str, Any]] = []
        for pick in event.picks:
            waveform = pick.waveform_id
            picks.append(
                {
                    "network": (waveform.network_code if waveform else "") or "",
                    "station": (waveform.station_code if waveform else "") or "",
                    "location": (waveform.location_code if waveform else "") or "",
                    "channel": (waveform.channel_code if waveform else "") or "",
                    "phase": pick.phase_hint or "",
                    "time_utc": str(pick.time) if pick.time is not None else "",
                    "evaluation_mode": str(pick.evaluation_mode or ""),
                    "evaluation_status": str(pick.evaluation_status or ""),
                }
            )
        by_event.setdefault(short_id, []).extend(picks)
    return by_event


def count_ch_p_picks(picks: list[dict[str, Any]]) -> dict[str, Any]:
    """Count CH-network P-phase picks. Phase names like Pg, Pn, P count as P."""
    n_ch = 0
    n_hhz = 0
    n_manual = 0
    modes: set[str] = set()
    stations: set[str] = set()
    for pick in picks:
        network = str(pick.get("network") or "").upper()
        channel = str(pick.get("channel") or "").upper()
        phase = str(pick.get("phase") or "").strip()
        if network != "CH":
            continue
        if not _is_p_phase(phase):
            continue
        n_ch += 1
        stations.add(str(pick.get("station") or "").upper())
        mode = str(pick.get("evaluation_mode") or "").strip().lower()
        if mode:
            modes.add(mode)
        if mode == "manual":
            n_manual += 1
        if channel.endswith("Z") and channel.startswith(("HH", "BH", "EH", "HG")):
            n_hhz += 1
        elif channel == "HHZ":
            n_hhz += 1
    return {
        "n_ch_p_picks": n_ch,
        "n_ch_hhz_p_picks": n_hhz,
        "n_ch_manual_p_picks": n_manual,
        "n_ch_p_stations": len({s for s in stations if s}),
        "n_unique_ch_stations_with_first_p": len({s for s in stations if s}),
        "sed_p_pick_modes": ";".join(sorted(modes)) if modes else "",
        "sed_p_pick_available": "yes" if n_ch > 0 else "no",
    }


def _is_p_phase(phase: str) -> bool:
    """First-arrival P labels only. Reflections (PmP, PP, PcP) are not the reference."""
    token = phase.strip().upper()
    return token in {"P", "PG", "PN", "PB", "P1", "PDIFF"}


def first_p_station_codes(picks: list[dict[str, Any]], *, channel: str | None = None) -> set[str]:
    """Unique CH station codes with a first-P pick. Event-level picks without a station are ignored."""
    stations: set[str] = set()
    wanted = None if channel is None else str(channel).upper()
    for pick in picks:
        if str(pick.get("network") or "").upper() != "CH":
            continue
        if not _is_p_phase(str(pick.get("phase") or "")):
            continue
        station = str(pick.get("station") or "").strip().upper()
        if not station:
            continue
        if wanted is not None and str(pick.get("channel") or "").upper() != wanted:
            continue
        stations.add(station)
    return stations


def same_station_reference_counts(picks: list[dict[str, Any]], hhz_stations: set[str]) -> dict[str, Any]:
    """Match station-level CH first-P picks to stations that have HHZ availability."""
    p_stations = first_p_station_codes(picks)
    p_hhz = first_p_station_codes(picks, channel="HHZ")
    hhz = {str(item).upper() for item in hhz_stations if item}
    return {
        "n_unique_ch_stations_with_first_p": len(p_stations),
        "n_same_station_first_p_and_hhz": len(p_stations & hhz),
        "n_same_station_hhz_first_p_and_hhz": len(p_hhz & hhz),
        "has_event_level_picks": bool(picks),
        "has_station_level_ch_first_p": bool(p_stations),
    }


def span_covers_interval(earliest: Any, latest: Any, start: Any, end: Any, slack_s: float = 1.5) -> bool:
    """True when [earliest, latest] fully covers [start, end] within slack.

    Slack accounts for FDSN timestamp truncation and sample-interval rounding.
    """
    return earliest <= start + slack_s and latest >= end - slack_s


def unique_ch_stations_covering(
    rows: list[dict[str, Any]],
    start: Any,
    end: Any,
    channels: tuple[str, ...],
    slack_s: float = 1.5,
) -> set[str]:
    """Unique CH station codes whose listed channels each fully cover [start, end]."""
    needed = {str(channel).upper() for channel in channels}
    covering: dict[str, set[str]] = {}
    for row in rows:
        if str(row.get("network") or "").upper() != "CH":
            continue
        channel = str(row.get("channel") or "").upper()
        if channel not in needed:
            continue
        if not span_covers_interval(row["earliest"], row["latest"], start, end, slack_s):
            continue
        station = str(row.get("station") or "").strip().upper()
        if not station:
            continue
        covering.setdefault(station, set()).add(channel)
    return {station for station, have in covering.items() if needed.issubset(have)}


def exclusion_reason(
    event: dict[str, Any],
    *,
    development_ids: set[str],
    allowed_types: list[str],
    min_magnitude: float,
) -> str:
    short_id = event_short_id(str(event.get("short_id") or event.get("event_id") or ""))
    if not short_id:
        return "missing_event_id"
    if short_id in development_ids:
        return "in_development_20_event_set"
    if not is_allowed_event_type(str(event.get("event_type") or ""), allowed_types):
        return f"event_type:{event.get('event_type') or 'blank'}"
    mag = event.get("magnitude")
    try:
        if float(mag) < float(min_magnitude):
            return "magnitude_below_threshold"
    except (TypeError, ValueError):
        return "missing_magnitude"
    if not event.get("origin_time_utc"):
        return "missing_origin_time"
    if event.get("latitude") in ("", None) or event.get("longitude") in ("", None):
        return "missing_hypocentre"
    return ""
