#!/usr/bin/env python3
"""Swiss methods-transfer waveform signal analysis.

Reads the Swiss SED pilot manifest and MiniSEED + StationXML. Does not modify
raw files, California analysis scripts, or California artefacts.

Not an operational EEW system. STA/LTA times are automatic triggers, not
validated P arrivals.
"""

from __future__ import annotations

import json
import logging
import math
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from obspy import Stream, UTCDateTime, read, read_inventory

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.acquisition.switzerland_pilot import event_short_id
from src.analysis.switzerland_signal import (
    REQUIRED_HH_3C,
    analysis_windows,
    amplitude_term,
    bandpass_freqmax_used,
    classify_trigger,
    common_overlap,
    cumulative_squared,
    epicentral_distance_km,
    finite_median,
    finite_stats,
    first_sta_lta_trigger,
    edge_mute_seconds,
    has_complete_hh_3c,
    horizontal_amplitude,
    hypocentral_distance_km,
    identify_hh_components,
    load_swiss_analysis_config,
    merge_stream_justified,
    peak_abs,
    plausibility_flag,
    pre_filt_for_sampling,
    rms,
    sampling_rates_consistent,
    select_trigger_from_onsets,
    slice_array_window,
    snr_ratio,
    stationxml_path_for_row,
    units_label,
    vector_amplitude,
    window_covered,
)

LOGGER = logging.getLogger("swiss_signal_analysis")
DEFAULT_CONFIG = REPO_ROOT / "configs" / "swiss_signal_analysis.yaml"


def _setup_logging(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    LOGGER.handlers.clear()
    LOGGER.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(stream_handler)


def _apply_plot_style() -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "font.family": "DejaVu Sans",
            "axes.labelsize": 11,
            "axes.titlesize": 11,
            "figure.dpi": 120,
            "savefig.bbox": "tight",
            "axes.grid": True,
            "grid.alpha": 0.35,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def _json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        number = float(value)
        return number if math.isfinite(number) else None
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    return value


def _origin_relative_times(tr, origin: UTCDateTime) -> np.ndarray:
    t0 = float(tr.stats.starttime - origin)
    return t0 + np.arange(tr.stats.npts, dtype=float) / float(tr.stats.sampling_rate)


def _empty_metric_row(row: pd.Series, short_id: str) -> dict[str, Any]:
    return {
        "event_id": short_id,
        "event_resource_id": str(row["event_id"]),
        "origin_time_utc": str(row["origin_time_utc"]),
        "magnitude": float(row["magnitude"]),
        "magnitude_type": str(row["magnitude_type"]),
        "region": str(row.get("region", "")),
        "event_latitude": float(row["latitude"]),
        "event_longitude": float(row["longitude"]),
        "depth_km": float(row["depth_km"]),
        "network": str(row["network"]),
        "station": str(row["station"]),
        "location": str(row.get("location", "--")),
        "waveform_file": str(row["waveform_file"]),
        "stationxml_file": "",
        "analysis_status": "FAIL",
        "failure_reason": "",
        "n_gaps": 0,
        "channels_found": "",
        "three_component": False,
        "sampling_rate_hz": float("nan"),
        "overlap_start_utc": "",
        "overlap_end_utc": "",
        "noise_window_covered": False,
        "event_window_covered": False,
        "response_attempted": False,
        "response_status": "not_attempted",
        "response_exception": "",
        "units_before": "counts",
        "units_after": "counts",
        "pre_filt": "",
        "bandpass_freqmin_hz": float("nan"),
        "bandpass_freqmax_used_hz": float("nan"),
        "station_latitude": float("nan"),
        "station_longitude": float("nan"),
        "epicentral_distance_km": float("nan"),
        "hypocentral_distance_km": float("nan"),
        "peak_vel_hhz": float("nan"),
        "peak_vel_hhn": float("nan"),
        "peak_vel_hhe": float("nan"),
        "peak_vel_horizontal": float("nan"),
        "peak_vel_vector": float("nan"),
        "rms_vel_hhz_event": float("nan"),
        "rms_vel_hhz_noise": float("nan"),
        "cumulative_sq_vel_hhz": float("nan"),
        "peak_acc_hhz": float("nan"),
        "peak_acc_horizontal": float("nan"),
        "amplitude_name_velocity": "peak_response_corrected_amplitude",
        "amplitude_name_acceleration": "peak_response_corrected_amplitude",
        "plausibility": "",
        "snr_peak_hhz": float("nan"),
        "snr_rms_hhz": float("nan"),
        "snr_peak_horizontal": float("nan"),
        "snr_peak_vector": float("nan"),
        "snr_peak_hhz_counts": float("nan"),
        "sta_lta_method": "",
        "sta_lta_method_unmasked": "",
        "trigger_latency_unmasked_s": float("nan"),
        "trigger_latency_first_after_mute_s": float("nan"),
        "sta_lta_edge_mute_s": float("nan"),
        "trigger_time_utc": "",
        "trigger_latency_s": float("nan"),
        "trigger_sta_lta_value": float("nan"),
        "in_noise_window": False,
        "in_expected_event_window": False,
        "false_trigger_candidate": False,
        "n_onsets_after_edge_mute": 0,
        "n_onsets_in_noise_window": 0,
        "trigger_class": "",
        "sta_lta_hhn_latency_s": float("nan"),
        "sta_lta_hhe_latency_s": float("nan"),
        "horizontal_trigger_earlier_than_vertical": False,
    }


def _component_traces(stream: Stream) -> dict[str, Any]:
    idx = identify_hh_components(stream)
    return {ch: stream[idx[ch]] for ch in REQUIRED_HH_3C}


def _align_npts(components: dict[str, Any]) -> dict[str, Any]:
    npts = min(tr.stats.npts for tr in components.values())
    aligned = {}
    for channel, trace in components.items():
        work = trace.copy()
        if work.stats.npts != npts:
            work.data = work.data[:npts]
            work.stats.npts = npts
        aligned[channel] = work
    return aligned


def _apply_bandpass(
    stream: Stream,
    sampling_rate: float,
    bandpass_cfg: dict[str, Any],
    zerophase: bool | None = None,
) -> float:
    fmax = bandpass_freqmax_used(sampling_rate, bandpass_cfg)
    zp = bool(bandpass_cfg["zerophase"]) if zerophase is None else bool(zerophase)
    stream.filter(
        "bandpass",
        freqmin=float(bandpass_cfg["freqmin_hz"]),
        freqmax=fmax,
        corners=int(bandpass_cfg["corners"]),
        zerophase=zp,
    )
    return fmax


def process_record(row: pd.Series, config: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    short_id = event_short_id(str(row["event_id"]))
    result = _empty_metric_row(row, short_id)
    origin = UTCDateTime(str(row["origin_time_utc"]))
    windows = analysis_windows(origin, config["windows"])
    waveform = repo_root / str(row["waveform_file"]).replace("\\", "/")
    xml_path = stationxml_path_for_row(
        repo_root,
        config["inputs"]["metadata_dir"],
        str(row["event_id"]),
        str(row["station"]),
        str(row.get("location", "--")),
    )
    result["stationxml_file"] = str(xml_path.relative_to(repo_root)).replace("\\", "/")

    if not waveform.exists():
        result["failure_reason"] = f"waveform_missing:{waveform}"
        return result

    try:
        stream = read(str(waveform))
    except Exception as exc:  # noqa: BLE001 — record and continue
        result["failure_reason"] = f"mseed_read:{type(exc).__name__}:{exc}"
        return result

    merged, gap_info = merge_stream_justified(stream)
    result["n_gaps"] = int(gap_info["n_gaps"])
    result["channels_found"] = ";".join(sorted({tr.stats.channel for tr in merged}))

    if not has_complete_hh_3c(merged):
        result["failure_reason"] = f"incomplete_3c:{result['channels_found']}"
        return result
    result["three_component"] = True

    if not sampling_rates_consistent(merged):
        rates = {tr.stats.channel: tr.stats.sampling_rate for tr in merged}
        result["failure_reason"] = f"inconsistent_sampling_rates:{rates}"
        return result

    overlap = common_overlap(merged)
    if overlap is None:
        result["failure_reason"] = "no_common_time_overlap"
        return result
    merged.trim(overlap[0], overlap[1], pad=False, nearest_sample=True)
    result["overlap_start_utc"] = str(overlap[0])
    result["overlap_end_utc"] = str(overlap[1])
    result["noise_window_covered"] = window_covered(overlap[0], overlap[1], windows["noise"])
    result["event_window_covered"] = window_covered(overlap[0], overlap[1], windows["event"])

    raw_3c = _align_npts(_component_traces(merged))
    sampling_rate = float(raw_3c["HHZ"].stats.sampling_rate)
    result["sampling_rate_hz"] = sampling_rate

    prep_cfg = config["preprocessing"]
    processed = Stream([raw_3c[ch].copy() for ch in REQUIRED_HH_3C])
    if prep_cfg.get("detrend_demean", True):
        processed.detrend(type="demean")
    if prep_cfg.get("detrend_linear", True):
        processed.detrend(type="linear")
    processed.taper(
        max_percentage=float(prep_cfg["taper_max_percentage"]),
        type=str(prep_cfg["taper_type"]),
    )

    response_cfg = config["instrument_response"]
    result["response_attempted"] = True
    result["units_before"] = "counts"
    if not xml_path.exists():
        result["response_status"] = "failed"
        result["response_exception"] = f"stationxml_missing:{xml_path}"
        LOGGER.warning("response_failed event=%s station=%s reason=stationxml_missing", short_id, row["station"])
    else:
        try:
            inventory = read_inventory(str(xml_path))
            sta = inventory[0][0]
            result["station_latitude"] = float(sta.latitude)
            result["station_longitude"] = float(sta.longitude)
            pre_filt = pre_filt_for_sampling(sampling_rate, response_cfg, config["bandpass"])
            result["pre_filt"] = ",".join(f"{v:.4g}" for v in pre_filt)
            corrected = processed.copy()
            corrected.remove_response(
                inventory=inventory,
                output=str(response_cfg["output"]),
                water_level=float(response_cfg["water_level"]),
                pre_filt=pre_filt,
                zero_mean=False,
                taper=False,
            )
            processed = corrected
            result["response_status"] = "applied"
            result["units_after"] = units_label(str(response_cfg["output"]), "applied")
        except Exception as exc:  # noqa: BLE001 — keep raw-derived processed stream
            result["response_status"] = "failed"
            result["response_exception"] = f"{type(exc).__name__}: {exc}"
            result["units_after"] = "counts"
            LOGGER.warning(
                "response_failed event=%s station=%s reason=%s",
                short_id,
                row["station"],
                result["response_exception"],
            )

    post_response = processed.copy()
    fmax = _apply_bandpass(processed, sampling_rate, config["bandpass"], zerophase=True)
    result["bandpass_freqmin_hz"] = float(config["bandpass"]["freqmin_hz"])
    result["bandpass_freqmax_used_hz"] = fmax
    proc_3c = _align_npts(_component_traces(processed))
    pick_stream = post_response.copy()
    _apply_bandpass(
        pick_stream,
        sampling_rate,
        config["bandpass"],
        zerophase=bool(config["sta_lta"].get("filter_zerophase", False)),
    )
    pick_3c = _align_npts(_component_traces(pick_stream))

    acc_3c = None
    if result["response_status"] == "applied" and config["amplitude"].get("report_pga_from_velocity_derivative"):
        acc_stream = Stream([proc_3c[ch].copy() for ch in REQUIRED_HH_3C])
        acc_stream.differentiate()
        acc_3c = _align_npts(_component_traces(acc_stream))

    if math.isfinite(result["station_latitude"]):
        result["epicentral_distance_km"] = epicentral_distance_km(
            float(row["latitude"]),
            float(row["longitude"]),
            result["station_latitude"],
            result["station_longitude"],
        )
        result["hypocentral_distance_km"] = hypocentral_distance_km(
            result["epicentral_distance_km"],
            float(row["depth_km"]),
        )

    z = proc_3c["HHZ"]
    n = proc_3c["HHN"]
    e = proc_3c["HHE"]
    z_pick = pick_3c["HHZ"]
    z_event = slice_array_window(z.data, z.stats.starttime, sampling_rate, windows["event"])
    n_event = slice_array_window(n.data, n.stats.starttime, sampling_rate, windows["event"])
    e_event = slice_array_window(e.data, e.stats.starttime, sampling_rate, windows["event"])
    z_noise = slice_array_window(z.data, z.stats.starttime, sampling_rate, windows["noise"])
    n_noise = slice_array_window(n.data, n.stats.starttime, sampling_rate, windows["noise"])
    e_noise = slice_array_window(e.data, e.stats.starttime, sampling_rate, windows["noise"])

    min_event = min(len(z_event), len(n_event), len(e_event))
    min_noise = min(len(z_noise), len(n_noise), len(e_noise))
    z_event, n_event, e_event = z_event[:min_event], n_event[:min_event], e_event[:min_event]
    z_noise, n_noise, e_noise = z_noise[:min_noise], n_noise[:min_noise], e_noise[:min_noise]
    h_event = horizontal_amplitude(n_event, e_event) if min_event else np.array([])
    v_event = vector_amplitude(z_event, n_event, e_event) if min_event else np.array([])
    h_noise = horizontal_amplitude(n_noise, e_noise) if min_noise else np.array([])
    v_noise = vector_amplitude(z_noise, n_noise, e_noise) if min_noise else np.array([])

    result["peak_vel_hhz"] = peak_abs(z_event)
    result["peak_vel_hhn"] = peak_abs(n_event)
    result["peak_vel_hhe"] = peak_abs(e_event)
    result["peak_vel_horizontal"] = peak_abs(h_event)
    result["peak_vel_vector"] = peak_abs(v_event)
    result["rms_vel_hhz_event"] = rms(z_event)
    result["rms_vel_hhz_noise"] = rms(z_noise)
    result["cumulative_sq_vel_hhz"] = cumulative_squared(z_event, 1.0 / sampling_rate)
    result["snr_peak_hhz"] = snr_ratio(result["peak_vel_hhz"], result["rms_vel_hhz_noise"], float(config["snr"]["epsilon"]))
    result["snr_rms_hhz"] = snr_ratio(result["rms_vel_hhz_event"], result["rms_vel_hhz_noise"], float(config["snr"]["epsilon"]))
    result["snr_peak_horizontal"] = snr_ratio(result["peak_vel_horizontal"], rms(h_noise), float(config["snr"]["epsilon"]))
    result["snr_peak_vector"] = snr_ratio(result["peak_vel_vector"], rms(v_noise), float(config["snr"]["epsilon"]))

    raw_z = raw_3c["HHZ"]
    raw_event = slice_array_window(raw_z.data, raw_z.stats.starttime, sampling_rate, windows["event"])
    raw_noise = slice_array_window(raw_z.data, raw_z.stats.starttime, sampling_rate, windows["noise"])
    result["snr_peak_hhz_counts"] = snr_ratio(peak_abs(raw_event), rms(raw_noise), float(config["snr"]["epsilon"]))

    if acc_3c is not None:
        az = slice_array_window(acc_3c["HHZ"].data, acc_3c["HHZ"].stats.starttime, sampling_rate, windows["event"])
        an = slice_array_window(acc_3c["HHN"].data, acc_3c["HHN"].stats.starttime, sampling_rate, windows["event"])
        ae = slice_array_window(acc_3c["HHE"].data, acc_3c["HHE"].stats.starttime, sampling_rate, windows["event"])
        m = min(len(az), len(an), len(ae))
        result["peak_acc_hhz"] = peak_abs(az[:m])
        result["peak_acc_horizontal"] = peak_abs(horizontal_amplitude(an[:m], ae[:m])) if m else float("nan")

    result["amplitude_name_velocity"] = amplitude_term(result["units_after"], "pgv")
    acc_units = "m/s^2" if result["response_status"] == "applied" else "counts"
    result["amplitude_name_acceleration"] = amplitude_term(acc_units, "pga")
    result["plausibility"] = plausibility_flag(
        result["peak_vel_hhz"] if result["units_after"] == "m/s" else float("nan"),
        result["peak_acc_hhz"] if result["response_status"] == "applied" else float("nan"),
        config["plausibility"],
    )

    sta_cfg = config["sta_lta"]
    mute_s = 0.0
    if sta_cfg.get("mute_taper_edges", True):
        mute_s = edge_mute_seconds(
            len(z_pick.data),
            sampling_rate,
            float(config["preprocessing"]["taper_max_percentage"]),
            float(sta_cfg["lta_window_s"]),
            float(sta_cfg.get("extra_start_mute_s", 0.0)),
        )
    result["sta_lta_edge_mute_s"] = mute_s
    pick = first_sta_lta_trigger(
        np.asarray(z_pick.data, dtype=float),
        sampling_rate,
        float(sta_cfg["sta_window_s"]),
        float(sta_cfg["lta_window_s"]),
        float(sta_cfg["threshold"]),
        float(sta_cfg["off_threshold"]),
        mute_start_s=mute_s,
        mute_end_s=mute_s,
    )
    result["sta_lta_method"] = pick["method"]
    result["sta_lta_method_unmasked"] = pick.get("method_unmasked", "")
    result["trigger_sta_lta_value"] = pick["value"]
    if pick.get("sample_unmasked") is not None:
        result["trigger_latency_unmasked_s"] = float(
            (z_pick.stats.starttime + (pick["sample_unmasked"] / sampling_rate)) - origin
        )
    onset_times = [
        z_pick.stats.starttime + (sample / sampling_rate)
        for sample in pick.get("onset_samples") or []
    ]
    classified = select_trigger_from_onsets(
        onset_times,
        origin,
        windows,
        float(sta_cfg["search_start_offset_s"]),
        float(sta_cfg["search_end_offset_s"]),
    )
    result.update(classified)
    if pick["sample"] is not None:
        result["trigger_latency_first_after_mute_s"] = float(
            (z_pick.stats.starttime + (pick["sample"] / sampling_rate)) - origin
        )

    for channel, key in (("HHN", "sta_lta_hhn_latency_s"), ("HHE", "sta_lta_hhe_latency_s")):
        ch_pick = first_sta_lta_trigger(
            np.asarray(pick_3c[channel].data, dtype=float),
            sampling_rate,
            float(sta_cfg["sta_window_s"]),
            float(sta_cfg["lta_window_s"]),
            float(sta_cfg["threshold"]),
            float(sta_cfg["off_threshold"]),
            mute_start_s=mute_s,
            mute_end_s=mute_s,
        )
        if ch_pick["sample"] is not None:
            ch_time = pick_3c[channel].stats.starttime + (ch_pick["sample"] / sampling_rate)
            result[key] = float(ch_time - origin)
    horiz_latencies = [result["sta_lta_hhn_latency_s"], result["sta_lta_hhe_latency_s"]]
    if math.isfinite(result["trigger_latency_s"]) and any(math.isfinite(v) for v in horiz_latencies):
        earliest_h = min(v for v in horiz_latencies if math.isfinite(v))
        result["horizontal_trigger_earlier_than_vertical"] = earliest_h < result["trigger_latency_s"] - 0.5

    if result["response_status"] == "failed":
        result["analysis_status"] = "PARTIAL"
        if not result["failure_reason"]:
            result["failure_reason"] = result["response_exception"]
    else:
        result["analysis_status"] = "OK"
    return result


def event_summary(metrics: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for event_id, grp in metrics.groupby("event_id", sort=True):
        rows.append(
            {
                "event_id": event_id,
                "origin_time": grp["origin_time_utc"].iloc[0],
                "magnitude": grp["magnitude"].iloc[0],
                "magnitude_type": grp["magnitude_type"].iloc[0],
                "region": grp["region"].iloc[0],
                "number_of_stations": int(grp["station"].nunique()),
                "number_of_3C_records": int(grp["three_component"].sum()),
                "response_success_count": int((grp["response_status"] == "applied").sum()),
                "median_distance_km": finite_median(grp["epicentral_distance_km"]),
                "median_trigger_latency_s": finite_median(grp["trigger_latency_s"]),
                "median_snr_peak_hhz": finite_median(grp["snr_peak_hhz"]),
                "median_peak_vel_hhz": finite_median(grp["peak_vel_hhz"]),
                "max_peak_vel_hhz": float(np.nanmax(grp["peak_vel_hhz"].to_numpy(dtype=float))),
                "median_peak_acc_hhz": finite_median(grp["peak_acc_hhz"]),
                "n_false_trigger_candidates": int(grp["false_trigger_candidate"].sum()),
                "n_no_trigger": int((grp["trigger_class"] == "no_trigger").sum()),
            }
        )
    return pd.DataFrame(rows)


def station_summary(metrics: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for station, grp in metrics.groupby("station", sort=True):
        rates = sorted({f"{v:.4g}" for v in grp["sampling_rate_hz"].dropna().unique()})
        snr = grp["snr_peak_hhz"].to_numpy(dtype=float)
        lat = grp["trigger_latency_s"].to_numpy(dtype=float)
        rows.append(
            {
                "station": station,
                "number_of_events": int(grp["event_id"].nunique()),
                "sampling_rate": ";".join(rates),
                "component_availability": "HHZ,HHN,HHE" if bool(grp["three_component"].all()) else "incomplete",
                "response_applied": int((grp["response_status"] == "applied").sum()),
                "response_failed": int((grp["response_status"] == "failed").sum()),
                "median_distance_km": finite_median(grp["epicentral_distance_km"]),
                "min_distance_km": float(np.nanmin(grp["epicentral_distance_km"].to_numpy(dtype=float))),
                "max_distance_km": float(np.nanmax(grp["epicentral_distance_km"].to_numpy(dtype=float))),
                "median_snr_peak_hhz": finite_median(snr),
                "min_snr_peak_hhz": float(np.nanmin(snr)) if np.isfinite(snr).any() else float("nan"),
                "median_trigger_latency_s": finite_median(lat),
                "n_false_trigger_candidates": int(grp["false_trigger_candidate"].sum()),
                "n_no_trigger": int((grp["trigger_class"] == "no_trigger").sum()),
                "unusual_flag": "",
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    snr_med = finite_median(out["median_snr_peak_hhz"])
    flags = []
    for _, row in out.iterrows():
        notes = []
        # Noise-window STA/LTA onsets at threshold 2.5 are cohort-wide, not station-unusual.
        if row["n_no_trigger"] >= max(1, 0.5 * row["number_of_events"]):
            notes.append("high_no_trigger_rate")
        if math.isfinite(row["median_snr_peak_hhz"]) and math.isfinite(snr_med) and row["median_snr_peak_hhz"] < 0.3 * snr_med:
            notes.append("low_median_snr")
        if math.isfinite(row["median_trigger_latency_s"]) and row["median_trigger_latency_s"] > 20.0:
            notes.append("late_median_trigger")
        flags.append(";".join(notes))
    out["unusual_flag"] = flags
    return out


def _load_example_streams(
    metrics: pd.DataFrame,
    config: dict[str, Any],
    repo_root: Path,
    event_id: str,
    station: str,
) -> tuple[dict[str, Any], UTCDateTime, Stream, Stream, Stream] | None:
    match = metrics[(metrics["event_id"] == event_id) & (metrics["station"] == station)]
    if match.empty:
        return None
    row = match.iloc[0]
    waveform = repo_root / str(row["waveform_file"])
    xml_path = repo_root / str(row["stationxml_file"])
    origin = UTCDateTime(str(row["origin_time_utc"]))
    stream = read(str(waveform))
    merged, _ = merge_stream_justified(stream)
    overlap = common_overlap(merged)
    if overlap is None:
        return None
    merged.trim(overlap[0], overlap[1], pad=False, nearest_sample=True)
    raw = Stream([_component_traces(merged)[ch].copy() for ch in REQUIRED_HH_3C])
    processed = raw.copy()
    processed.detrend("demean")
    processed.detrend("linear")
    processed.taper(max_percentage=0.05, type="hann")
    if Path(xml_path).exists() and row["response_status"] == "applied":
        inv = read_inventory(str(xml_path))
        rate = float(processed[0].stats.sampling_rate)
        processed.remove_response(
            inventory=inv,
            output=str(config["instrument_response"]["output"]),
            water_level=float(config["instrument_response"]["water_level"]),
            pre_filt=pre_filt_for_sampling(rate, config["instrument_response"], config["bandpass"]),
            zero_mean=False,
            taper=False,
        )
    post_response = processed.copy()
    rate = float(processed[0].stats.sampling_rate)
    _apply_bandpass(processed, rate, config["bandpass"], zerophase=True)
    pick_stream = post_response.copy()
    _apply_bandpass(
        pick_stream,
        rate,
        config["bandpass"],
        zerophase=bool(config["sta_lta"].get("filter_zerophase", False)),
    )
    return row, origin, raw, processed, pick_stream


def _shade_windows(ax, windows: dict[str, tuple[UTCDateTime, UTCDateTime]], origin: UTCDateTime) -> None:
    noise = (float(windows["noise"][0] - origin), float(windows["noise"][1] - origin))
    event = (float(windows["event"][0] - origin), float(windows["event"][1] - origin))
    ax.axvspan(noise[0], noise[1], color="#90caf9", alpha=0.35, label="noise window")
    ax.axvspan(event[0], event[1], color="#ffcc80", alpha=0.35, label="event window")
    ax.axvline(0.0, color="#333333", linestyle="--", linewidth=1.0, label="origin")


def make_figures(
    metrics: pd.DataFrame,
    config: dict[str, Any],
    repo_root: Path,
    fig_dir: Path,
) -> list[str]:
    fig_dir.mkdir(parents=True, exist_ok=True)
    dpi = int(config["figures"]["dpi"])
    written: list[str] = []
    example_event = str(config["figures"]["example_event_id"])
    example_station = str(config["figures"]["example_station"])
    loaded = _load_example_streams(metrics, config, repo_root, example_event, example_station)
    origin_example = None
    windows_example = None
    if loaded is not None:
        example_row, origin_example, raw, processed, pick_stream = loaded
        windows_example = analysis_windows(origin_example, config["windows"])

        fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
        fig.suptitle(
            f"Swiss 3C waveform (response-corrected, {config['bandpass']['freqmin_hz']}-{config['bandpass']['freqmax_hz']} Hz)\n"
            f"{example_event}  CH.{example_station}  units={example_row['units_after']}"
        )
        colors = {"HHZ": "#1f4e79", "HHN": "#2e7d32", "HHE": "#c62828"}
        for ax, channel in zip(axes, REQUIRED_HH_3C):
            tr = _component_traces(processed)[channel]
            t = _origin_relative_times(tr, origin_example)
            ax.plot(t, tr.data, color=colors[channel], linewidth=0.5)
            ax.set_ylabel(f"{channel}\n({example_row['units_after']})")
        axes[-1].set_xlabel("Time relative to origin (s)")
        axes[-1].set_xlim(-90, 120)
        fig.tight_layout()
        path = fig_dir / "fig01_representative_3c_waveform.png"
        fig.savefig(path, dpi=dpi)
        plt.close(fig)
        written.append(path.name)

        fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        fig.suptitle(f"HHZ before/after response correction · {example_event} {example_station}")
        raw_z = _component_traces(raw)["HHZ"]
        proc_z = _component_traces(processed)["HHZ"]
        axes[0].plot(_origin_relative_times(raw_z, origin_example), raw_z.data, color="#1f4e79", linewidth=0.5)
        axes[0].set_ylabel("counts")
        axes[0].set_title("Raw MiniSEED (unchanged on disk)")
        axes[1].plot(_origin_relative_times(proc_z, origin_example), proc_z.data, color="#6a1b9a", linewidth=0.5)
        axes[1].set_ylabel(str(example_row["units_after"]))
        axes[1].set_title("Demean, detrend, taper, remove_response(VEL), band-pass")
        axes[1].set_xlabel("Time relative to origin (s)")
        axes[1].set_xlim(-90, 120)
        fig.tight_layout()
        path = fig_dir / "fig02_response_correction_hhz.png"
        fig.savefig(path, dpi=dpi)
        plt.close(fig)
        written.append(path.name)

        fig, ax = plt.subplots(figsize=(10, 4))
        t = _origin_relative_times(proc_z, origin_example)
        ax.plot(t, proc_z.data, color="#1f4e79", linewidth=0.5)
        _shade_windows(ax, windows_example, origin_example)
        ax.set_xlim(-90, 180)
        ax.set_xlabel("Time relative to origin (s)")
        ax.set_ylabel(str(example_row["units_after"]))
        ax.set_title(f"Pre-event noise vs event window · {example_event} {example_station} HHZ")
        ax.legend(loc="upper right", fontsize=8)
        fig.tight_layout()
        path = fig_dir / "fig03_noise_vs_event_window.png"
        fig.savefig(path, dpi=dpi)
        plt.close(fig)
        written.append(path.name)

        sta_cfg = config["sta_lta"]
        mute_s = float(example_row.get("sta_lta_edge_mute_s", 0.0) or 0.0)
        pick_z = _component_traces(pick_stream)["HHZ"]
        pick_t = _origin_relative_times(pick_z, origin_example)
        cft_pack = first_sta_lta_trigger(
            np.asarray(pick_z.data, dtype=float),
            float(pick_z.stats.sampling_rate),
            float(sta_cfg["sta_window_s"]),
            float(sta_cfg["lta_window_s"]),
            float(sta_cfg["threshold"]),
            float(sta_cfg["off_threshold"]),
            mute_start_s=mute_s,
            mute_end_s=mute_s,
        )
        fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        fig.suptitle(
            f"STA/LTA automatic trigger on causal 0.1–15 Hz HHZ (not a validated P pick)\n"
            f"{example_event} {example_station}  class={example_row['trigger_class']}  latency={example_row['trigger_latency_s']:.2f}s"
        )
        axes[0].plot(pick_t, pick_z.data, color="#1f4e79", linewidth=0.5)
        if math.isfinite(float(example_row["trigger_latency_s"])):
            axes[0].axvline(float(example_row["trigger_latency_s"]), color="#c62828", linestyle="--", label="STA/LTA trigger")
        axes[0].axvline(0.0, color="#333333", linestyle=":", linewidth=1.0)
        axes[0].set_ylabel(str(example_row["units_after"]))
        axes[0].legend(loc="upper right", fontsize=8)
        if cft_pack["cft"] is not None:
            tcft = pick_t[: len(cft_pack["cft"])]
            axes[1].plot(tcft, cft_pack["cft"], color="#5c6bc0", linewidth=0.7)
        axes[1].axhline(float(sta_cfg["threshold"]), color="#888888", linestyle=":", label=f"threshold {sta_cfg['threshold']}")
        if math.isfinite(float(example_row["trigger_latency_s"])):
            axes[1].axvline(float(example_row["trigger_latency_s"]), color="#c62828", linestyle="--")
        axes[1].set_ylabel("STA/LTA")
        axes[1].set_xlabel("Time relative to origin (s)")
        axes[1].set_xlim(-90, 120)
        axes[1].legend(loc="upper right", fontsize=8)
        fig.tight_layout()
        path = fig_dir / "fig04_sta_lta_example.png"
        fig.savefig(path, dpi=dpi)
        plt.close(fig)
        written.append(path.name)

        other = metrics[
            (metrics["trigger_class"] != example_row["trigger_class"]) & (metrics["analysis_status"] != "FAIL")
        ]
        if not other.empty:
            alt = other.iloc[0]
            alt_loaded = _load_example_streams(metrics, config, repo_root, str(alt["event_id"]), str(alt["station"]))
            if alt_loaded is not None:
                alt_row, alt_origin, _raw_alt, alt_proc, alt_pick = alt_loaded
                alt_z = _component_traces(alt_pick)["HHZ"]
                alt_t = _origin_relative_times(alt_z, alt_origin)
                alt_cft = first_sta_lta_trigger(
                    np.asarray(alt_z.data, dtype=float),
                    float(alt_z.stats.sampling_rate),
                    float(sta_cfg["sta_window_s"]),
                    float(sta_cfg["lta_window_s"]),
                    float(sta_cfg["threshold"]),
                    float(sta_cfg["off_threshold"]),
                    mute_start_s=float(alt_row.get("sta_lta_edge_mute_s", 0.0) or 0.0),
                    mute_end_s=float(alt_row.get("sta_lta_edge_mute_s", 0.0) or 0.0),
                )
                fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
                fig.suptitle(
                    f"Additional STA/LTA class (not cherry-picked for success) · {alt_row['event_id']} {alt_row['station']}\n"
                    f"class={alt_row['trigger_class']}"
                )
                axes[0].plot(alt_t, alt_z.data, color="#1f4e79", linewidth=0.5)
                if math.isfinite(float(alt_row["trigger_latency_s"])):
                    axes[0].axvline(float(alt_row["trigger_latency_s"]), color="#c62828", linestyle="--")
                axes[0].axvline(0.0, color="#333333", linestyle=":")
                if alt_cft["cft"] is not None:
                    axes[1].plot(alt_t[: len(alt_cft["cft"])], alt_cft["cft"], color="#5c6bc0", linewidth=0.7)
                axes[1].axhline(float(sta_cfg["threshold"]), color="#888888", linestyle=":")
                axes[1].set_xlabel("Time relative to origin (s)")
                axes[1].set_xlim(-90, 120)
                fig.tight_layout()
                path = fig_dir / "fig04b_sta_lta_additional_class.png"
                fig.savefig(path, dpi=dpi)
                plt.close(fig)
                written.append(path.name)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    snr_vals = metrics["snr_peak_hhz"].to_numpy(dtype=float)
    snr_vals = snr_vals[np.isfinite(snr_vals)]
    ax.hist(np.log10(np.clip(snr_vals, 1e-3, None)), bins=20, color="#1565c0", edgecolor="white")
    ax.set_xlabel("log10 SNR peak (HHZ, event max |x| / noise RMS)")
    ax.set_ylabel("Event–station records")
    ax.set_title("Swiss SNR peak distribution (all analysed records)")
    path = fig_dir / "fig05_snr_distribution.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    lat = metrics["trigger_latency_s"].to_numpy(dtype=float)
    lat = lat[np.isfinite(lat)]
    ax.hist(lat, bins=25, color="#6a1b9a", edgecolor="white")
    ax.axvline(0.0, color="#333333", linestyle="--", label="origin")
    ax.set_xlabel("STA/LTA trigger latency relative to origin (s)")
    ax.set_ylabel("Event–station records")
    ax.set_title("Swiss automatic-trigger latency (HHZ; not validated P picks)")
    ax.legend()
    path = fig_dir / "fig06_trigger_latency_distribution.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    vel = metrics["peak_vel_hhz"].to_numpy(dtype=float)
    vel = vel[np.isfinite(vel) & (vel > 0)]
    ax.hist(np.log10(vel), bins=20, color="#2e7d32", edgecolor="white")
    units = metrics["units_after"].mode().iloc[0] if not metrics.empty else ""
    xlabel = "log10 peak |HHZ| in event window"
    if units == "m/s":
        xlabel = "log10 band-limited PGV HHZ (m/s, 0.1–15 Hz)"
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Event–station records")
    ax.set_title("Swiss peak-amplitude distribution (all analysed records)")
    path = fig_dir / "fig07_peak_amplitude_distribution.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)

    fig, ax = plt.subplots(figsize=(8, 6.5))
    ev = metrics.drop_duplicates("event_id")
    ax.scatter(ev["event_longitude"], ev["event_latitude"], c="#c62828", s=40, zorder=3, label="events")
    sta = metrics.dropna(subset=["station_longitude", "station_latitude"]).drop_duplicates("station")
    ax.scatter(sta["station_longitude"], sta["station_latitude"], c="#1565c0", s=28, marker="^", zorder=2, label="CH stations")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Swiss pilot events and selected CH stations")
    ax.legend()
    ax.set_aspect("equal", adjustable="box")
    path = fig_dir / "fig08_station_event_map.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)

    fig, ax = plt.subplots(figsize=(8, 5))
    ok = metrics[np.isfinite(metrics["epicentral_distance_km"]) & np.isfinite(metrics["peak_vel_hhz"])]
    ax.scatter(ok["epicentral_distance_km"], ok["peak_vel_hhz"], c=ok["magnitude"], cmap="viridis", s=28, alpha=0.85)
    cb = fig.colorbar(ax.collections[0], ax=ax)
    cb.set_label("Catalogue magnitude")
    ax.set_xlabel("Epicentral distance (km)")
    ylabel = "Peak |HHZ| event window"
    if (metrics["units_after"] == "m/s").all():
        ylabel = "Band-limited PGV HHZ (m/s)"
        ax.set_yscale("log")
    ax.set_ylabel(ylabel)
    ax.set_title("Distance vs peak amplitude (no attenuation model fitted)")
    path = fig_dir / "fig09_distance_vs_amplitude.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)

    cal_path = repo_root / config["inputs"]["california_signal_summary"]
    cal = {}
    if cal_path.exists():
        cal = json.loads(cal_path.read_text(encoding="utf-8"))
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.axis("off")
    swiss_n = int(len(metrics))
    lines = [
        "Methods-transfer comparison (not a controlled performance experiment)",
        "",
        f"{'':22} {'California v1.0.0 (frozen)':32} {'Swiss pilot (this analysis)':32}",
        f"{'Events':22} {cal.get('n_waveforms', 8):<32} {metrics['event_id'].nunique():<32}",
        f"{'Records':22} {cal.get('n_waveforms', 8):<32} {swiss_n:<32}",
        f"{'Component':22} {'BHZ':<32} {'HH 3C':<32}",
        f"{'Window':22} {'origin-aligned 300 s':<32} {'origin−90 s to +210 s':<32}",
        f"{'Noise estimate':22} {'first 5 s proxy':<32} {'origin−60 to −10 s':<32}",
        f"{'Response removal':22} {'0/8':<32} {int((metrics['response_status']=='applied').sum())}/{swiss_n:<30}",
        f"{'Amplitude units':22} {'counts':<32} {str(metrics['units_after'].mode().iloc[0]) if not metrics.empty else '':<32}",
        f"{'STA/LTA':22} {'0.5 / 10 s, thr 2.5':<32} {'0.5 / 10 s, thr 2.5':<32}",
        "",
        "SNR and trigger latency are not interchangeable across datasets:",
        "different instrumentation, sampling, noise windows, magnitude range, and geography.",
    ]
    ax.text(0.02, 0.98, "\n".join(lines), va="top", ha="left", family="DejaVu Sans", fontsize=9, transform=ax.transAxes)
    ax.set_title("California vs Swiss structural comparison")
    path = fig_dir / "fig10_california_swiss_structural_comparison.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)
    return written


def build_summary(metrics: pd.DataFrame, config: dict[str, Any], figures: list[str], failures: list[dict[str, Any]]) -> dict[str, Any]:
    n = int(len(metrics))
    applied = int((metrics["response_status"] == "applied").sum())
    failed_resp = int((metrics["response_status"] == "failed").sum())
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "config": "configs/swiss_signal_analysis.yaml",
        "n_manifest_rows": n,
        "n_events": int(metrics["event_id"].nunique()) if n else 0,
        "n_ok": int((metrics["analysis_status"] == "OK").sum()),
        "n_partial": int((metrics["analysis_status"] == "PARTIAL").sum()),
        "n_fail": int((metrics["analysis_status"] == "FAIL").sum()),
        "response": {
            "attempted": int(metrics["response_attempted"].sum()) if n else 0,
            "successful": applied,
            "failed": failed_resp,
        },
        "units_after_counts": metrics["units_after"].value_counts(dropna=False).to_dict() if n else {},
        "three_component": int(metrics["three_component"].sum()) if n else 0,
        "pre_event_window_covered": int(metrics["noise_window_covered"].sum()) if n else 0,
        "event_window_covered": int(metrics["event_window_covered"].sum()) if n else 0,
        "sta_lta": {
            "parameters": {
                "sta_s": config["sta_lta"]["sta_window_s"],
                "lta_s": config["sta_lta"]["lta_window_s"],
                "threshold": config["sta_lta"]["threshold"],
            },
            "trigger_class_counts": metrics["trigger_class"].value_counts().to_dict() if n else {},
            "n_false_trigger_candidates": int(metrics["false_trigger_candidate"].sum()) if n else 0,
            "latency_s": finite_stats(metrics["trigger_latency_s"]) if n else {},
        },
        "snr_peak_hhz": finite_stats(metrics["snr_peak_hhz"]) if n else {},
        "snr_peak_horizontal": finite_stats(metrics["snr_peak_horizontal"]) if n else {},
        "snr_peak_vector": finite_stats(metrics["snr_peak_vector"]) if n else {},
        "peak_vel_hhz": finite_stats(metrics["peak_vel_hhz"]) if n else {},
        "peak_vel_horizontal": finite_stats(metrics["peak_vel_horizontal"]) if n else {},
        "peak_acc_hhz": finite_stats(metrics["peak_acc_hhz"]) if n else {},
        "epicentral_distance_km": finite_stats(metrics["epicentral_distance_km"]) if n else {},
        "hypocentral_distance_km": finite_stats(metrics["hypocentral_distance_km"]) if n else {},
        "sampling_rate_hz_counts": {str(k): int(v) for k, v in metrics["sampling_rate_hz"].value_counts().items()} if n else {},
        "plausibility_counts": metrics["plausibility"].value_counts().to_dict() if n else {},
        "failures": failures,
        "figures": figures,
        "windows": config["windows"],
        "bandpass": config["bandpass"],
        "language": {
            "dataset": "Swiss pilot dataset / Swiss seismic-data acquisition / methods-transfer pilot",
            "triggers": "automatic STA/LTA triggers, not validated P arrivals",
            "not": ["operational Swiss EEW", "validated Swiss EEW", "European EEW model"],
        },
    }


def main() -> None:
    config = load_swiss_analysis_config(DEFAULT_CONFIG)
    out_dir = REPO_ROOT / config["output"]["reports_dir"]
    fig_dir = REPO_ROOT / config["output"]["figures_dir"]
    log_path = REPO_ROOT / config["output"]["log_file"]
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    _setup_logging(log_path)
    _apply_plot_style()

    LOGGER.info("swiss_signal_analysis_start config=%s", DEFAULT_CONFIG)
    LOGGER.info(
        "windows noise=%s..%s event=%s..%s bandpass=%s-%s Hz STA/LTA=%s/%s thr=%s",
        config["windows"]["noise_start_offset_s"],
        config["windows"]["noise_end_offset_s"],
        config["windows"]["event_start_offset_s"],
        config["windows"]["event_end_offset_s"],
        config["bandpass"]["freqmin_hz"],
        config["bandpass"]["freqmax_hz"],
        config["sta_lta"]["sta_window_s"],
        config["sta_lta"]["lta_window_s"],
        config["sta_lta"]["threshold"],
    )

    manifest = pd.read_csv(REPO_ROOT / config["inputs"]["manifest_csv"])
    LOGGER.info("manifest_rows=%s unique_events=%s", len(manifest), manifest["event_id"].nunique())

    records: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for _, row in manifest.iterrows():
        result = process_record(row, config, REPO_ROOT)
        records.append(result)
        if result["analysis_status"] != "OK":
            failures.append(
                {
                    "event_id": result["event_id"],
                    "station": result["station"],
                    "status": result["analysis_status"],
                    "reason": result["failure_reason"] or result["response_exception"],
                }
            )
            LOGGER.warning(
                "record_not_ok event=%s station=%s status=%s reason=%s",
                result["event_id"],
                result["station"],
                result["analysis_status"],
                result["failure_reason"] or result["response_exception"],
            )
        else:
            LOGGER.info(
                "record_ok event=%s station=%s units=%s snr_peak_hhz=%.3g latency=%s class=%s",
                result["event_id"],
                result["station"],
                result["units_after"],
                result["snr_peak_hhz"] if math.isfinite(result["snr_peak_hhz"]) else float("nan"),
                f"{result['trigger_latency_s']:.2f}" if math.isfinite(result["trigger_latency_s"]) else "NA",
                result["trigger_class"],
            )

    metrics = pd.DataFrame(records)
    metrics.to_csv(out_dir / "swiss_trace_metrics.csv", index=False)
    ev = event_summary(metrics)
    ev.to_csv(out_dir / "swiss_event_summary.csv", index=False)
    st = station_summary(metrics)
    st.to_csv(out_dir / "swiss_station_summary.csv", index=False)

    snapshot = deepcopy(config)
    snapshot["generated_at_utc"] = datetime.now(timezone.utc).isoformat()
    (out_dir / "processing_config.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    (out_dir / "failures.json").write_text(json.dumps(failures, indent=2), encoding="utf-8")

    figures = make_figures(metrics, config, REPO_ROOT, fig_dir)
    summary = build_summary(metrics, config, figures, failures)
    (out_dir / "swiss_signal_summary.json").write_text(
        json.dumps(_json_ready(summary), indent=2),
        encoding="utf-8",
    )
    LOGGER.info(
        "swiss_signal_analysis_complete n=%s ok=%s partial=%s fail=%s response=%s/%s figures=%s",
        len(metrics),
        summary["n_ok"],
        summary["n_partial"],
        summary["n_fail"],
        summary["response"]["successful"],
        summary["response"]["attempted"],
        len(figures),
    )
    print(json.dumps({k: summary[k] for k in ("n_manifest_rows", "n_ok", "n_partial", "n_fail", "response", "units_after_counts")}, indent=2))


if __name__ == "__main__":
    main()
