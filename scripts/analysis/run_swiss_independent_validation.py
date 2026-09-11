#!/usr/bin/env python3
"""Frozen STA/LTA validation on Independent Swiss/Adjacent-Border Set C.

Evaluates the pre-declared configuration (causal 0.1–15 Hz HHZ, STA 0.5 s,
LTA 10 s, trigger_on 8.0). Does not retune, sweep thresholds, modify Set A,
or modify California v1.0.0. Automatic times are candidate onsets, not
validated P arrivals.
"""

from __future__ import annotations

import csv
import json
import logging
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from obspy import Stream, UTCDateTime, read, read_inventory

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.acquisition.switzerland_pilot import event_short_id
from src.acquisition.switzerland_validation_audit import window_offsets
from src.analysis.switzerland_signal import (
    bandpass_freqmax_used,
    edge_mute_seconds,
    merge_stream_justified,
    pre_filt_for_sampling,
)
from src.analysis.switzerland_sta_lta_transfer import (
    compute_cft_and_onsets,
    count_in_window,
    onset_times_from_samples,
    window_pair,
)
from src.analysis.switzerland_validation import (
    EVENT_SUMMARY_FIELDS,
    TRACE_METRIC_FIELDS,
    apply_timing_fields,
    count_noise_onsets,
    event_summary_rows,
    first_detection_onset,
    load_validation_run_config,
    locked_set_c_ids,
    same_station_pick_for_record,
    summarize_trace_rows,
    yes_no,
)

LOGGER = logging.getLogger("switzerland_independent_validation")
DEFAULT_CONFIG = REPO_ROOT / "configs" / "sed_switzerland_validation.yaml"


def _setup_logging(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    LOGGER.handlers.clear()
    LOGGER.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(formatter)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    LOGGER.addHandler(fh)
    LOGGER.addHandler(sh)


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


def _csv_cell(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        return ""
    return value


def _write_csv(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: _csv_cell(row.get(field, "")) for field in fields})


def _apply_plot_style() -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "font.family": "DejaVu Sans",
            "axes.grid": True,
            "grid.alpha": 0.35,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "savefig.bbox": "tight",
        }
    )


def _read_csv_dicts(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _select_hhz(stream: Stream) -> Any:
    traces = [tr for tr in stream if str(tr.stats.channel).upper() == "HHZ"]
    if not traces:
        return None
    traces.sort(key=lambda tr: (str(tr.stats.starttime), str(tr.id)))
    return traces[0]


def _blank_row(manifest_row: dict[str, Any], origin: UTCDateTime | None) -> dict[str, Any]:
    return {
        "short_id": event_short_id(str(manifest_row.get("short_id") or manifest_row.get("event_id") or "")),
        "station": str(manifest_row.get("station") or ""),
        "location": str(manifest_row.get("location") or ""),
        "channel": "HHZ",
        "magnitude": manifest_row.get("magnitude", ""),
        "region": str(manifest_row.get("region") or ""),
        "location_class": str(manifest_row.get("location_class") or ""),
        "origin_time_utc": str(origin) if origin is not None else str(manifest_row.get("origin_time") or ""),
        "processing_status": "ok",
        "failure_reason": "",
        "has_usable_same_station_p": "no",
        "reference_p_time_utc": "",
        "reference_p_latency_s": float("nan"),
        "reference_p_phase": "",
        "reference_p_mode": "",
        "detection_status": "NO_DETECTION",
        "trigger_time_utc": "",
        "trigger_latency_s": float("nan"),
        "trigger_minus_p_s": float("nan"),
        "abs_trigger_minus_p_s": float("nan"),
        "trigger_at_or_after_p": "",
        "n_onsets_noise_window": 0,
        "has_noise_onset": "no",
        "n_onsets_detection_window": 0,
        "sampling_rate_hz": "",
        "mute_s": "",
        "units": "m/s",
    }


def load_processed_hhz(
    manifest_row: dict[str, Any],
    signal_cfg: dict[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    """HHZ-only causal velocity stream. Does not require HH 3C."""
    waveform = repo_root / str(manifest_row["MiniSEED_path"]).replace("\\", "/")
    xml_path = repo_root / str(manifest_row["StationXML_path"]).replace("\\", "/")
    if not waveform.exists():
        raise FileNotFoundError(f"missing MiniSEED: {waveform}")
    if not xml_path.exists():
        raise FileNotFoundError(f"missing StationXML: {xml_path}")
    stream = read(str(waveform))
    merged, merge_info = merge_stream_justified(stream)
    if merge_info.get("n_gaps", 0) > 0:
        raise ValueError(f"gaps_present:{merge_info['n_gaps']}")
    trace = _select_hhz(merged)
    if trace is None:
        raise ValueError("no_hhz_trace")
    if np.ma.isMaskedArray(trace.data) and np.ma.getmaskarray(trace.data).any():
        raise ValueError("masked_or_gappy_hhz")
    data = np.asarray(trace.data, dtype=float)
    if data.size == 0 or not np.isfinite(data).all():
        raise ValueError("empty_or_nonfinite_hhz")

    work = Stream([trace.copy()])
    work.detrend("demean")
    work.detrend("linear")
    work.taper(max_percentage=0.05, type="hann")
    rate = float(work[0].stats.sampling_rate)
    pre_filt = pre_filt_for_sampling(rate, signal_cfg["instrument_response"], signal_cfg["bandpass"])
    inv = read_inventory(str(xml_path))
    work.remove_response(
        inventory=inv,
        output=str(signal_cfg["instrument_response"]["output"]),
        water_level=float(signal_cfg["instrument_response"]["water_level"]),
        pre_filt=pre_filt,
        zero_mean=False,
        taper=False,
    )
    fmax = bandpass_freqmax_used(rate, signal_cfg["bandpass"])
    work.filter(
        "bandpass",
        freqmin=float(signal_cfg["bandpass"]["freqmin_hz"]),
        freqmax=fmax,
        corners=int(signal_cfg["bandpass"]["corners"]),
        zerophase=False,
    )
    processed = work[0]
    mute_s = edge_mute_seconds(len(processed.data), rate, 0.05, 10.0, 0.0)
    return {
        "data": np.asarray(processed.data, dtype=float),
        "starttime": processed.stats.starttime,
        "sampling_rate": rate,
        "mute_s": mute_s,
        "units": "m/s",
        "bandpass_freqmax_used": fmax,
    }


def evaluate_record(
    manifest_row: dict[str, Any],
    picks: list[dict[str, Any]],
    config: dict[str, Any],
    repo_root: Path,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    frozen = config["frozen_configuration"]
    signal_cfg = config["_signal"]
    offsets = window_offsets(config)
    short_id = event_short_id(str(manifest_row.get("short_id") or manifest_row.get("event_id") or ""))
    station = str(manifest_row.get("station") or "")
    try:
        origin = UTCDateTime(str(manifest_row["origin_time"]))
    except Exception as exc:  # noqa: BLE001 — keep the locked record
        row = _blank_row(manifest_row, None)
        row["processing_status"] = "failed"
        row["failure_reason"] = f"invalid_origin:{exc}"
        return row, {"short_id": short_id, "station": station, "reason": row["failure_reason"]}

    row = _blank_row(manifest_row, origin)
    pick = same_station_pick_for_record(picks, short_id, station)
    reference_p = None
    if pick is not None:
        try:
            reference_p = UTCDateTime(str(pick["pick_time_utc"]))
            row["has_usable_same_station_p"] = "yes"
            row["reference_p_phase"] = str(pick.get("pick_phase") or "")
            row["reference_p_mode"] = str(pick.get("pick_evaluation_mode") or pick.get("pick_source") or "")
        except Exception:  # noqa: BLE001
            reference_p = None
            row["has_usable_same_station_p"] = "no"

    try:
        processed = load_processed_hhz(manifest_row, signal_cfg, repo_root)
    except Exception as exc:  # noqa: BLE001 — retain the record, do not drop Set C
        row["processing_status"] = "failed"
        row["failure_reason"] = str(exc)
        apply_timing_fields(row, origin, None, reference_p)
        return row, {"short_id": short_id, "station": station, "reason": row["failure_reason"]}

    pack = compute_cft_and_onsets(
        processed["data"],
        processed["sampling_rate"],
        float(frozen["sta_window_s"]),
        float(frozen["lta_window_s"]),
        float(frozen["trigger_on"]),
        float(frozen["trigger_off"]),
        processed["mute_s"],
        processed["mute_s"],
    )
    onset_times = onset_times_from_samples(
        processed["starttime"],
        processed["sampling_rate"],
        pack.get("onset_samples") or [],
    )
    trigger = first_detection_onset(
        onset_times,
        origin,
        float(frozen["search_start_offset_s"]),
        float(frozen["search_end_offset_s"]),
    )
    det_start, det_end = window_pair(origin, offsets["detection"][0], offsets["detection"][1])
    n_noise = count_noise_onsets(onset_times, origin, offsets["pre_event_noise"][0], offsets["pre_event_noise"][1])
    row["processing_status"] = "ok"
    row["sampling_rate_hz"] = processed["sampling_rate"]
    row["mute_s"] = processed["mute_s"]
    row["units"] = processed["units"]
    row["n_onsets_noise_window"] = n_noise
    row["has_noise_onset"] = yes_no(n_noise > 0)
    row["n_onsets_detection_window"] = count_in_window(onset_times, det_start, det_end)
    apply_timing_fields(row, origin, trigger, reference_p)
    return row, None


def make_figures(rows: list[dict[str, Any]], event_rows: list[dict[str, Any]], fig_dir: Path) -> list[str]:
    fig_dir.mkdir(parents=True, exist_ok=True)
    _apply_plot_style()
    written: list[str] = []
    paired = [
        row
        for row in rows
        if row.get("processing_status") == "ok"
        and row.get("detection_status") == "DETECTED"
        and str(row.get("has_usable_same_station_p")) == "yes"
        and math.isfinite(float(row.get("trigger_latency_s", float("nan"))))
        and math.isfinite(float(row.get("reference_p_latency_s", float("nan"))))
    ]
    if paired:
        trig = np.array([float(row["trigger_latency_s"]) for row in paired], dtype=float)
        pref = np.array([float(row["reference_p_latency_s"]) for row in paired], dtype=float)
        err = np.array([float(row["trigger_minus_p_s"]) for row in paired], dtype=float)
        fig, ax = plt.subplots(figsize=(6.5, 6.0))
        ax.scatter(pref, trig, s=18, alpha=0.55, color="#1565c0", edgecolors="none")
        lo = min(float(np.min(pref)), float(np.min(trig)))
        hi = max(float(np.max(pref)), float(np.max(trig)))
        pad = 0.05 * (hi - lo if hi > lo else 1.0)
        ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad], color="#333333", linestyle="--", linewidth=1.0, label="1:1")
        ax.set_xlabel("Independent reference first-P latency (s after origin)")
        ax.set_ylabel("Automatic STA/LTA onset latency (s after origin)")
        ax.set_title("Frozen 8.0 trigger vs same-station reference P (Set C)")
        ax.legend(loc="upper left")
        path = fig_dir / "fig01_trigger_vs_reference_timing.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        written.append(path.name)

        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        ax.hist(err, bins=40, color="#6a1b9a", edgecolor="white")
        ax.axvline(0.0, color="#333333", linestyle="--", linewidth=1.0)
        ax.set_xlabel("Trigger − independent reference P (s)")
        ax.set_ylabel("Paired records")
        ax.set_title("Timing-error distribution (detected records with same-station P)")
        path = fig_dir / "fig02_timing_error_distribution.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        written.append(path.name)

    if event_rows:
        labels = [str(row["short_id"]) for row in event_rows]
        pct = [float(row["detection_percent"]) if math.isfinite(float(row.get("detection_percent", float("nan")))) else 0.0 for row in event_rows]
        fig, ax = plt.subplots(figsize=(10.5, 4.8))
        ax.bar(np.arange(len(labels)), pct, color="#455a64")
        ax.set_xticks(np.arange(len(labels)))
        ax.set_xticklabels(labels, rotation=55, ha="right")
        ax.set_ylabel("Detection percentage (usable records)")
        ax.set_ylim(0, 100)
        ax.set_title("Event-level automatic-onset coverage at frozen threshold 8.0")
        path = fig_dir / "fig03_event_detection_coverage.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        written.append(path.name)
    return written


def processing_config_payload(config: dict[str, Any]) -> dict[str, Any]:
    signal = config["_signal"]
    frozen = config["frozen_configuration"]
    return {
        "role": config.get("role"),
        "validation_dataset": config["validation_dataset"],
        "frozen_configuration": frozen,
        "windows": config["windows"],
        "scientific_boundary": config["scientific_boundary"],
        "signal_processing": {
            "source_config": config["signal_processing_config"],
            "preprocessing": signal["preprocessing"],
            "instrument_response": signal["instrument_response"],
            "bandpass": {
                "freqmin_hz": float(signal["bandpass"]["freqmin_hz"]),
                "freqmax_hz": float(signal["bandpass"]["freqmax_hz"]),
                "corners": int(signal["bandpass"]["corners"]),
                "zerophase": False,
                "note": "Detection uses the established causal band-pass; amplitude Set A used a separate zero-phase copy.",
            },
            "sta_lta": {
                "sta_window_s": float(frozen["sta_window_s"]),
                "lta_window_s": float(frozen["lta_window_s"]),
                "trigger_on": 8.0,
                "trigger_off": 0.5,
                "component": "HHZ",
                "edge_mute": "max(LTA, 5% of duration) at each end",
            },
        },
        "set_c_locked": True,
        "set_a_untouched": True,
        "california_v1_untouched": True,
        "threshold_retuned": False,
        "threshold_is_optimal": False,
    }


def main() -> None:
    config = load_validation_run_config(DEFAULT_CONFIG, repo_root=REPO_ROOT)
    locked = locked_set_c_ids(config)
    out_dir = REPO_ROOT / config["output"]["reports_dir"]
    fig_dir = REPO_ROOT / config["output"]["figures_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    _setup_logging(REPO_ROOT / config["output"]["logs_dir"] / config["output"]["log_name"])
    LOGGER.info("independent_validation_start config=%s locked=%s", DEFAULT_CONFIG, locked)

    waveform_path = REPO_ROOT / config["validation_dataset"]["waveform_manifest"]
    picks_path = REPO_ROOT / config["validation_dataset"]["picks_csv"]
    waveforms = _read_csv_dicts(waveform_path)
    picks = _read_csv_dicts(picks_path)
    expected = int(config["validation_dataset"]["n_records_expected"])
    LOGGER.info("loaded_manifests waveforms=%s picks=%s expected=%s", len(waveforms), len(picks), expected)

    rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for index, manifest_row in enumerate(waveforms, start=1):
        row, failure = evaluate_record(manifest_row, picks, config, REPO_ROOT)
        rows.append(row)
        if failure is not None:
            failures.append(failure)
            LOGGER.warning("processing_failure %s %s %s", failure["short_id"], failure["station"], failure["reason"])
        elif index % 25 == 0 or index == len(waveforms):
            LOGGER.info("processed %s/%s %s %s %s", index, len(waveforms), row["short_id"], row["station"], row["detection_status"])

    event_rows = event_summary_rows(rows, locked)
    summary = summarize_trace_rows(rows, locked)
    figures = make_figures(rows, event_rows, fig_dir)
    summary.update(
        {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "n_events": len(locked),
            "n_records_expected": expected,
            "dataset_name": config["validation_dataset"]["display_name"],
            "detection_window": "origin to origin+90 s",
            "noise_window": "origin-60 s to origin-10 s",
            "acquisition_window": "origin-60 s to origin+90 s",
            "reference": "same-station SED/manual first-P (independent reference, not ground truth)",
            "threshold_label": "pre-declared frozen threshold 8.0; not claimed optimal",
            "sta_lta_retuned": False,
            "operational_eew_claimed": False,
            "p_wave_picking_claimed": False,
            "edge_mute_note": (
                "Established mute is max(LTA, 5% duration) at each end. "
                "On 150 s Set C traces this is 10 s, so origin+80 to +90 s is muted; "
                "the mute was not changed to recover that interval."
            ),
            "figures": figures,
            "event_summaries": event_rows,
        }
    )

    _write_csv(out_dir / "validation_trace_metrics.csv", rows, TRACE_METRIC_FIELDS)
    _write_csv(out_dir / "validation_event_summary.csv", event_rows, EVENT_SUMMARY_FIELDS)
    (out_dir / "validation_summary.json").write_text(json.dumps(_json_ready(summary), indent=2), encoding="utf-8")
    (out_dir / "processing_config.json").write_text(
        json.dumps(_json_ready(processing_config_payload(config)), indent=2),
        encoding="utf-8",
    )
    (out_dir / "failures.json").write_text(
        json.dumps(
            {
                "n_processing_failures": len(failures),
                "processing_failures": failures,
                "n_no_detection": int(summary["n_no_detection"]),
                "note": "NO_DETECTION is a valid scientific outcome and is retained in validation_trace_metrics.csv. processing_failures are records where STA/LTA could not be evaluated.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    LOGGER.info(
        "independent_validation_complete processed=%s usable=%s detected=%s no_detection=%s failures=%s median_abs_err=%s",
        summary["n_records_processed"],
        summary["n_usable_station_event_records"],
        summary["n_detected"],
        summary["n_no_detection"],
        summary["n_processing_failures"],
        summary["median_abs_timing_error_s"],
    )
    print(
        json.dumps(
            _json_ready(
                {
                    "n_records_processed": summary["n_records_processed"],
                    "n_detected": summary["n_detected"],
                    "n_no_detection": summary["n_no_detection"],
                    "median_abs_timing_error_s": summary["median_abs_timing_error_s"],
                    "percent_detected_at_or_after_p": summary["percent_detected_at_or_after_p"],
                    "pre_event_noise_trigger_rate": summary["pre_event_noise_trigger_rate"],
                    "n_usable_same_station_independent_p": summary["n_usable_same_station_independent_p"],
                    "n_processing_failures": summary["n_processing_failures"],
                }
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
