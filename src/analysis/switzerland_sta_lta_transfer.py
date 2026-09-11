"""STA/LTA methods-transfer helpers for the Swiss pilot.

Does not alter California logic or the existing Swiss official-trigger pipeline.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import yaml
from obspy import UTCDateTime
from obspy.signal.trigger import classic_sta_lta, trigger_onset
from pathlib import Path

from src.acquisition.exceptions import AcquisitionConfigurationError


def load_transfer_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise AcquisitionConfigurationError(f"STA/LTA transfer config not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}
    if not isinstance(config, dict):
        raise AcquisitionConfigurationError("STA/LTA transfer config must be a YAML mapping.")
    validate_transfer_config(config)
    return config


def validate_transfer_config(config: dict[str, Any]) -> None:
    for section in ("inputs", "output", "baseline", "windows", "thresholds", "sta_lta_windows", "proposal_rule"):
        if section not in config:
            raise AcquisitionConfigurationError(f"missing {section}")
    out = config["output"]["reports_dir"]
    posix = Path(str(out)).as_posix().lower()
    if "iris" in posix or "california" in posix:
        raise AcquisitionConfigurationError("output must not point at California/IRIS paths")
    if not config["thresholds"]:
        raise AcquisitionConfigurationError("thresholds must be a non-empty list")
    rule = config["proposal_rule"]
    if float(rule["max_noise_record_fraction"]) <= 0 or float(rule["min_post_origin_coverage"]) <= 0:
        raise AcquisitionConfigurationError("proposal_rule fractions must be positive")


def sample_times(starttime: UTCDateTime, sampling_rate: float, n_samples: int) -> np.ndarray:
    return np.asarray(starttime) + (np.arange(n_samples, dtype=float) / sampling_rate)


def onset_times_from_samples(
    starttime: UTCDateTime,
    sampling_rate: float,
    samples: list[int] | np.ndarray,
) -> list[UTCDateTime]:
    return [starttime + (int(s) / sampling_rate) for s in samples]


def count_in_window(times: list[UTCDateTime], start: UTCDateTime, end: UTCDateTime) -> int:
    return sum(1 for t in times if start <= t < end)


def first_in_window(times: list[UTCDateTime], start: UTCDateTime, end: UTCDateTime) -> UTCDateTime | None:
    inside = [t for t in times if start <= t < end]
    return inside[0] if inside else None


def window_pair(origin: UTCDateTime, start_offset_s: float, end_offset_s: float) -> tuple[UTCDateTime, UTCDateTime]:
    return origin + float(start_offset_s), origin + float(end_offset_s)


def cft_window_stats(
    cft: np.ndarray,
    starttime: UTCDateTime,
    sampling_rate: float,
    window: tuple[UTCDateTime, UTCDateTime],
    threshold: float,
) -> dict[str, float]:
    """Max CFT and fraction of samples at/above threshold inside a UTC window."""
    if cft is None or len(cft) == 0 or sampling_rate <= 0:
        return {"n_samples": 0, "max_cft": float("nan"), "n_above": 0, "fraction_above": float("nan")}
    rel0 = float(window[0] - starttime)
    rel1 = float(window[1] - starttime)
    i0 = max(0, int(math.floor(rel0 * sampling_rate)))
    i1 = min(len(cft), int(math.ceil(rel1 * sampling_rate)))
    if i1 <= i0:
        return {"n_samples": 0, "max_cft": float("nan"), "n_above": 0, "fraction_above": float("nan")}
    seg = np.asarray(cft[i0:i1], dtype=float)
    n_above = int(np.sum(seg >= threshold))
    return {
        "n_samples": int(seg.size),
        "max_cft": float(np.max(seg)),
        "n_above": n_above,
        "fraction_above": float(n_above / seg.size),
    }


def trigger_window_counts(
    onset_times: list[UTCDateTime],
    origin: UTCDateTime,
    windows_cfg: dict[str, Any],
) -> dict[str, Any]:
    noise = window_pair(origin, windows_cfg["noise_start_offset_s"], windows_cfg["noise_end_offset_s"])
    pre = window_pair(origin, windows_cfg["pre_origin_start_offset_s"], windows_cfg["pre_origin_end_offset_s"])
    post = window_pair(origin, windows_cfg["post_origin_start_offset_s"], windows_cfg["post_origin_end_offset_s"])
    first_pre = first_in_window(onset_times, *pre)
    first_post = first_in_window(onset_times, *post)
    first_search = first_in_window(onset_times, pre[0], post[1])
    latency_search = float(first_search - origin) if first_search is not None else float("nan")
    latency_post = float(first_post - origin) if first_post is not None else float("nan")
    return {
        "n_onsets_noise": count_in_window(onset_times, *noise),
        "n_onsets_pre_origin": count_in_window(onset_times, *pre),
        "n_onsets_post_origin": count_in_window(onset_times, *post),
        "has_noise_onset": count_in_window(onset_times, *noise) > 0,
        "has_pre_origin_onset": count_in_window(onset_times, *pre) > 0,
        "has_post_origin_onset": count_in_window(onset_times, *post) > 0,
        "first_search_latency_s": latency_search,
        "first_post_origin_latency_s": latency_post,
        "search_is_pre_origin": bool(first_search is not None and float(first_search - origin) < 0),
        "search_is_post_origin": bool(first_search is not None and float(first_search - origin) >= 0),
        "no_trigger_in_search": first_search is None,
    }


def sta_lta_characteristic_function(
    data: np.ndarray,
    sampling_rate: float,
    sta_window_s: float,
    lta_window_s: float,
) -> tuple[np.ndarray, int, int]:
    x = np.asarray(data, dtype=float)
    nsta = max(int(sta_window_s * sampling_rate), 1)
    nlta = max(int(lta_window_s * sampling_rate), nsta + 1)
    if x.size <= nlta + 1:
        return np.array([]), nsta, nlta
    return classic_sta_lta(x, nsta, nlta), nsta, nlta


def onsets_from_cft(
    cft: np.ndarray,
    sampling_rate: float,
    nlta: int,
    threshold: float,
    off_threshold: float,
    mute_start_s: float,
    mute_end_s: float,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "cft": cft,
        "nlta": nlta,
        "sample": None,
        "sample_unmasked": None,
        "onset_samples": [],
        "method": "no_crossing",
        "method_unmasked": "no_crossing",
    }
    if cft is None or len(cft) == 0:
        result["method"] = "trace_shorter_than_lta"
        result["method_unmasked"] = "trace_shorter_than_lta"
        return result
    unmasked, unmasked_method = _first_onset(cft, nlta, threshold, off_threshold, 0, len(cft))
    result["sample_unmasked"] = unmasked
    result["method_unmasked"] = unmasked_method
    n0 = max(int(mute_start_s * sampling_rate), 0)
    n1 = max(int(mute_end_s * sampling_rate), 0)
    n_end = max(len(cft) - n1, n0)
    sample, method = _first_onset(cft, nlta, threshold, off_threshold, n0, n_end)
    result["sample"] = sample
    result["method"] = method
    onsets = trigger_onset(cft, threshold, off_threshold)
    if len(onsets) > 0:
        result["onset_samples"] = [int(o[0]) for o in onsets if n0 <= int(o[0]) < n_end]
    return result


def _first_onset(cft: np.ndarray, nlta: int, threshold: float, off_threshold: float, n0: int, n_end: int) -> tuple[int | None, str]:
    onsets = trigger_onset(cft, threshold, off_threshold)
    if len(onsets) > 0:
        for onset in onsets:
            idx = int(onset[0])
            if n0 <= idx < n_end:
                return idx, "trigger_onset_first"
    lo = max(nlta, n0)
    hi = n_end
    if hi <= lo:
        return None, "no_crossing"
    crossings = np.where(cft[lo:hi] >= threshold)[0]
    if len(crossings) == 0:
        return None, "no_crossing"
    return int(crossings[0] + lo), "first_threshold_crossing"


def compute_cft_and_onsets(
    data: np.ndarray,
    sampling_rate: float,
    sta_window_s: float,
    lta_window_s: float,
    threshold: float,
    off_threshold: float,
    mute_start_s: float,
    mute_end_s: float,
) -> dict[str, Any]:
    cft, _nsta, nlta = sta_lta_characteristic_function(data, sampling_rate, sta_window_s, lta_window_s)
    return onsets_from_cft(cft, sampling_rate, nlta, threshold, off_threshold, mute_start_s, mute_end_s)


def unmasked_onset_is_in_mute_region(
    sample_unmasked: int | None,
    sampling_rate: float,
    mute_start_s: float,
) -> bool:
    if sample_unmasked is None or sampling_rate <= 0:
        return False
    return (sample_unmasked / sampling_rate) < float(mute_start_s)


def apply_proposal_rule(rows: list[dict[str, Any]], rule: dict[str, Any]) -> dict[str, Any]:
    """Select a proposed threshold from a pre-declared rule. Not an optimum."""
    eligible = [
        r
        for r in rows
        if math.isclose(float(r["sta_window_s"]), float(rule["sta_window_s"]))
        and math.isclose(float(r["lta_window_s"]), float(rule["lta_window_s"]))
        and r.get("processing") == rule["processing"]
        and r.get("channel") == rule["channel"]
    ]
    eligible = sorted(eligible, key=lambda r: float(r["threshold"]))
    primary = [
        r
        for r in eligible
        if float(r["noise_record_fraction"]) < float(rule["max_noise_record_fraction"])
        and float(r["post_origin_coverage"]) >= float(rule["min_post_origin_coverage"])
    ]
    if primary:
        chosen = primary[0]
        reason = (
            f"lowest threshold with noise_record_fraction < {rule['max_noise_record_fraction']} "
            f"and post_origin_coverage >= {rule['min_post_origin_coverage']}"
        )
        mode = "primary"
    else:
        fallback = [
            r for r in eligible if float(r["post_origin_coverage"]) >= float(rule["fallback_min_post_origin_coverage"])
        ]
        if fallback:
            chosen = min(fallback, key=lambda r: (float(r["noise_record_fraction"]), float(r["threshold"])))
            reason = (
                f"no row met both primary cuts; lowest noise_record_fraction among "
                f"post_origin_coverage >= {rule['fallback_min_post_origin_coverage']}"
            )
            mode = "fallback"
        elif eligible:
            chosen = min(eligible, key=lambda r: (float(r["noise_record_fraction"]), -float(r["post_origin_coverage"])))
            reason = "no coverage cut met; row with lowest noise_record_fraction (still not validated)"
            mode = "unconstrained_fallback"
        else:
            return {
                "proposed": False,
                "reason": "no matching sensitivity rows",
                "mode": "none",
            }
    return {
        "proposed": True,
        "mode": mode,
        "reason": reason,
        "threshold": float(chosen["threshold"]),
        "sta_window_s": float(chosen["sta_window_s"]),
        "lta_window_s": float(chosen["lta_window_s"]),
        "processing": chosen["processing"],
        "channel": chosen["channel"],
        "noise_record_fraction": float(chosen["noise_record_fraction"]),
        "post_origin_coverage": float(chosen["post_origin_coverage"]),
        "median_post_origin_latency_s": float(chosen.get("median_post_origin_latency_s", float("nan"))),
        "label": "proposed configuration — not validated, not optimal",
    }


def finite_median(values: list[float] | np.ndarray) -> float:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float("nan")
    return float(np.median(arr))
