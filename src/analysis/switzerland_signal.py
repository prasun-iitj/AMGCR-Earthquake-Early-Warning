"""Swiss methods-transfer signal analysis helpers (no California I/O).

Pure functions for windows, 3C handling, SNR, STA/LTA, amplitudes, and
distance. Network and file I/O live in ``scripts/analysis/run_swiss_signal_analysis.py``.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import yaml
from obspy import Stream, UTCDateTime
from obspy.signal.trigger import classic_sta_lta, trigger_onset
from pathlib import Path

from src.acquisition.exceptions import AcquisitionConfigurationError
from src.acquisition.switzerland_pilot import event_short_id

REQUIRED_HH_3C = ("HHZ", "HHN", "HHE")
EARTH_RADIUS_KM = 6371.0


def load_swiss_analysis_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise AcquisitionConfigurationError(f"Swiss analysis config not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}
    if not isinstance(config, dict):
        raise AcquisitionConfigurationError("Swiss analysis config must be a YAML mapping.")
    validate_swiss_analysis_config(config)
    return config


def validate_swiss_analysis_config(config: dict[str, Any]) -> None:
    inputs = config.get("inputs")
    output = config.get("output")
    if not isinstance(inputs, dict) or not isinstance(output, dict):
        raise AcquisitionConfigurationError("inputs and output must be mappings.")
    for key in ("manifest_csv", "raw_dir", "metadata_dir"):
        value = inputs.get(key)
        if not isinstance(value, str) or not value.strip():
            raise AcquisitionConfigurationError(f"inputs.{key} must be a non-empty string.")
        _reject_california_path(f"inputs.{key}", value)
    for key in ("reports_dir", "figures_dir", "logs_dir"):
        value = output.get(key)
        if not isinstance(value, str) or not value.strip():
            raise AcquisitionConfigurationError(f"output.{key} must be a non-empty string.")
        _reject_california_path(f"output.{key}", value)

    windows = config.get("windows")
    if not isinstance(windows, dict):
        raise AcquisitionConfigurationError("windows must be a mapping.")
    noise_start = float(windows["noise_start_offset_s"])
    noise_end = float(windows["noise_end_offset_s"])
    event_start = float(windows["event_start_offset_s"])
    event_end = float(windows["event_end_offset_s"])
    if not (noise_start < noise_end <= 0.0):
        raise AcquisitionConfigurationError("noise window must lie entirely before origin.")
    if not (event_start >= 0.0 and event_end > event_start):
        raise AcquisitionConfigurationError("event window must start at/after origin.")

    bandpass = config.get("bandpass")
    if not isinstance(bandpass, dict):
        raise AcquisitionConfigurationError("bandpass must be a mapping.")
    if float(bandpass["freqmin_hz"]) <= 0 or float(bandpass["freqmax_hz"]) <= float(bandpass["freqmin_hz"]):
        raise AcquisitionConfigurationError("bandpass frequencies are invalid.")

    sta = config.get("sta_lta")
    if not isinstance(sta, dict):
        raise AcquisitionConfigurationError("sta_lta must be a mapping.")
    if float(sta["sta_window_s"]) <= 0 or float(sta["lta_window_s"]) <= float(sta["sta_window_s"]):
        raise AcquisitionConfigurationError("STA must be positive and shorter than LTA.")


def _reject_california_path(label: str, value: str) -> None:
    posix = Path(value).as_posix().lower()
    if "iris" in posix or "california" in posix:
        raise AcquisitionConfigurationError(f"{label} must not point at California/IRIS paths: {value}")


def analysis_windows(origin: UTCDateTime, windows_cfg: dict[str, Any]) -> dict[str, tuple[UTCDateTime, UTCDateTime]]:
    """Absolute UTC windows from origin-relative offsets."""

    def _pair(start_key: str, end_key: str) -> tuple[UTCDateTime, UTCDateTime]:
        return (
            origin + float(windows_cfg[start_key]),
            origin + float(windows_cfg[end_key]),
        )

    return {
        "noise": _pair("noise_start_offset_s", "noise_end_offset_s"),
        "event": _pair("event_start_offset_s", "event_end_offset_s"),
        "expected_trigger": _pair("expected_trigger_start_offset_s", "expected_trigger_end_offset_s"),
    }


def window_covered(trace_start: UTCDateTime, trace_end: UTCDateTime, window: tuple[UTCDateTime, UTCDateTime]) -> bool:
    start, end = window
    return trace_start <= start and trace_end >= end


def identify_hh_components(stream: Stream) -> dict[str, int]:
    """Return channel → first matching trace index for HHZ/HHN/HHE."""
    found: dict[str, int] = {}
    for index, trace in enumerate(stream):
        channel = str(trace.stats.channel).upper()
        if channel in REQUIRED_HH_3C and channel not in found:
            found[channel] = index
    return found


def has_complete_hh_3c(stream: Stream) -> bool:
    return set(identify_hh_components(stream).keys()) == set(REQUIRED_HH_3C)


def sampling_rates_consistent(stream: Stream, channels: tuple[str, ...] = REQUIRED_HH_3C) -> bool:
    components = identify_hh_components(stream)
    rates = [float(stream[components[ch]].stats.sampling_rate) for ch in channels if ch in components]
    if len(rates) < 2:
        return True
    return max(rates) - min(rates) < 1e-6


def common_overlap(stream: Stream, channels: tuple[str, ...] = REQUIRED_HH_3C) -> tuple[UTCDateTime, UTCDateTime] | None:
    components = identify_hh_components(stream)
    if any(ch not in components for ch in channels):
        return None
    start = max(stream[components[ch]].stats.starttime for ch in channels)
    end = min(stream[components[ch]].stats.endtime for ch in channels)
    if end <= start:
        return None
    return start, end


def merge_stream_justified(stream: Stream) -> tuple[Stream, dict[str, Any]]:
    """Merge only same-id traces. Record gaps; do not invent samples across gaps."""
    work = stream.copy()
    gap_list = work.get_gaps()
    n_before = len(work)
    work.merge(method=0, fill_value=None)
    info = {
        "n_traces_before_merge": n_before,
        "n_traces_after_merge": len(work),
        "n_gaps": len(gap_list),
        "gaps": [
            {
                "network": g[0],
                "station": g[1],
                "location": g[2],
                "channel": g[3],
                "start": str(g[4]),
                "end": str(g[5]),
            }
            for g in gap_list
        ],
        "merged": n_before != len(work),
    }
    return work, info


def slice_array_window(
    data: np.ndarray,
    starttime: UTCDateTime,
    sampling_rate: float,
    window: tuple[UTCDateTime, UTCDateTime],
) -> np.ndarray:
    """Return samples whose timestamps fall in [window_start, window_end)."""
    n = len(data)
    if n == 0 or sampling_rate <= 0:
        return np.array([], dtype=float)
    rel0 = float(window[0] - starttime)
    rel1 = float(window[1] - starttime)
    i0 = int(math.floor(rel0 * sampling_rate))
    i1 = int(math.ceil(rel1 * sampling_rate))
    i0 = max(0, min(i0, n))
    i1 = max(0, min(i1, n))
    if i1 <= i0:
        return np.array([], dtype=float)
    return np.asarray(data[i0:i1], dtype=float)


def rms(values: np.ndarray) -> float:
    if values.size == 0:
        return float("nan")
    x = np.asarray(values, dtype=float)
    return float(np.sqrt(np.mean(x * x)))


def peak_abs(values: np.ndarray) -> float:
    if values.size == 0:
        return float("nan")
    return float(np.max(np.abs(np.asarray(values, dtype=float))))


def snr_ratio(signal_metric: float, noise_rms: float, epsilon: float = 1e-12) -> float:
    if not math.isfinite(signal_metric) or not math.isfinite(noise_rms):
        return float("nan")
    return float(signal_metric / max(abs(noise_rms), epsilon))


def horizontal_amplitude(north: np.ndarray, east: np.ndarray) -> np.ndarray:
    n = np.asarray(north, dtype=float)
    e = np.asarray(east, dtype=float)
    if n.shape != e.shape:
        raise ValueError("HHN and HHE arrays must share shape for horizontal amplitude.")
    return np.sqrt(n * n + e * e)


def vector_amplitude(vertical: np.ndarray, north: np.ndarray, east: np.ndarray) -> np.ndarray:
    z = np.asarray(vertical, dtype=float)
    n = np.asarray(north, dtype=float)
    e = np.asarray(east, dtype=float)
    if not (z.shape == n.shape == e.shape):
        raise ValueError("HHZ/HHN/HHE arrays must share shape for vector amplitude.")
    return np.sqrt(z * z + n * n + e * e)


def cumulative_squared(values: np.ndarray, dt: float) -> float:
    if values.size == 0 or not math.isfinite(dt) or dt <= 0:
        return float("nan")
    x = np.asarray(values, dtype=float)
    return float(np.sum(x * x) * dt)


def epicentral_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlmb / 2.0) ** 2
    return 2.0 * EARTH_RADIUS_KM * math.asin(min(1.0, math.sqrt(a)))


def hypocentral_distance_km(epicentral_km: float, depth_km: float) -> float:
    return math.hypot(float(epicentral_km), float(depth_km))


def pre_filt_for_sampling(
    sampling_rate_hz: float,
    response_cfg: dict[str, Any],
    bandpass_cfg: dict[str, Any],
) -> tuple[float, float, float, float]:
    """Nyquist-aware cosine taper for remove_response (not California 40 Hz corners)."""
    nyquist = 0.5 * float(sampling_rate_hz)
    f1 = float(response_cfg["pre_filt_f1_hz"])
    f2 = float(response_cfg["pre_filt_f2_hz"])
    f3 = float(response_cfg["pre_filt_f3_nyquist_fraction"]) * nyquist
    f4 = float(response_cfg["pre_filt_f4_nyquist_fraction"]) * nyquist
    fmax = float(bandpass_cfg["freqmax_hz"])
    if f3 <= fmax:
        f3 = min(nyquist * 0.5, max(fmax * 1.5, fmax + 5.0))
    if f4 <= f3:
        f4 = min(nyquist * 0.9, f3 + 10.0)
    if not (0 < f1 < f2 < f3 < f4 < nyquist * 1.0001):
        raise ValueError(
            f"pre_filt invalid for sampling_rate={sampling_rate_hz} Hz: {(f1, f2, f3, f4)} nyquist={nyquist}"
        )
    return (f1, f2, f3, f4)


def bandpass_freqmax_used(sampling_rate_hz: float, bandpass_cfg: dict[str, Any]) -> float:
    nyquist = 0.5 * float(sampling_rate_hz)
    requested = float(bandpass_cfg["freqmax_hz"])
    guard = float(bandpass_cfg.get("nyquist_guard", 0.9)) * nyquist
    return min(requested, guard)


def _first_cft_onset(cft: np.ndarray, nlta: int, threshold: float, off_threshold: float) -> tuple[int | None, str]:
    onsets = trigger_onset(cft, threshold, off_threshold)
    if len(onsets) > 0:
        return int(onsets[0, 0]), "trigger_onset_first"
    crossings = np.where(cft[nlta:] >= threshold)[0]
    if len(crossings) == 0:
        return None, "no_crossing"
    return int(crossings[0] + nlta), "first_threshold_crossing"


def edge_mute_seconds(n_samples: int, sampling_rate: float, taper_max_percentage: float, lta_window_s: float, extra_s: float = 0.0) -> float:
    """Seconds muted at each end so taper/filter transients are not treated as picks."""
    duration = n_samples / sampling_rate if sampling_rate else 0.0
    return max(float(lta_window_s), float(taper_max_percentage) * duration, float(extra_s))


def first_sta_lta_trigger(
    data: np.ndarray,
    sampling_rate: float,
    sta_window_s: float,
    lta_window_s: float,
    threshold: float,
    off_threshold: float,
    mute_start_s: float = 0.0,
    mute_end_s: float = 0.0,
) -> dict[str, Any]:
    """First classic STA/LTA onset, or no_crossing. Does not invent a pick."""
    x = np.asarray(data, dtype=float)
    nsta = max(int(sta_window_s * sampling_rate), 1)
    nlta = max(int(lta_window_s * sampling_rate), nsta + 1)
    result: dict[str, Any] = {
        "nsta": nsta,
        "nlta": nlta,
        "sample": None,
        "sample_unmasked": None,
        "value": float("nan"),
        "method": "no_crossing",
        "method_unmasked": "no_crossing",
        "cft": None,
        "mute_start_s": float(mute_start_s),
        "mute_end_s": float(mute_end_s),
    }
    if x.size <= nlta + 1:
        result["method"] = "trace_shorter_than_lta"
        result["method_unmasked"] = "trace_shorter_than_lta"
        return result
    cft = classic_sta_lta(x, nsta, nlta)
    result["cft"] = cft
    unmasked_sample, unmasked_method = _first_cft_onset(cft, nlta, threshold, off_threshold)
    result["sample_unmasked"] = unmasked_sample
    result["method_unmasked"] = unmasked_method

    n0 = max(int(mute_start_s * sampling_rate), 0)
    n1 = max(int(mute_end_s * sampling_rate), 0)
    n_end = max(len(cft) - n1, n0)
    onsets = trigger_onset(cft, threshold, off_threshold)
    sample = None
    method = "no_crossing"
    if len(onsets) > 0:
        for onset in onsets:
            idx = int(onset[0])
            if n0 <= idx < n_end:
                sample = idx
                method = "trigger_onset_first"
                break
    if sample is None:
        crossings = np.where(cft[max(nlta, n0) : n_end] >= threshold)[0]
        if len(crossings):
            sample = int(crossings[0] + max(nlta, n0))
            method = "first_threshold_crossing"
    result["sample"] = sample
    result["method"] = method
    if sample is not None and sample < len(cft):
        result["value"] = float(cft[sample])
    onset_samples: list[int] = []
    all_onsets = trigger_onset(cft, threshold, off_threshold)
    if len(all_onsets) > 0:
        for onset in all_onsets:
            idx = int(onset[0])
            if n0 <= idx < n_end:
                onset_samples.append(idx)
    result["onset_samples"] = onset_samples
    return result


def select_trigger_from_onsets(
    onset_times: list[UTCDateTime],
    origin: UTCDateTime,
    windows: dict[str, tuple[UTCDateTime, UTCDateTime]],
    search_start_offset_s: float,
    search_end_offset_s: float,
) -> dict[str, Any]:
    """Primary trigger is the first onset in the search window; noise-window hits are diagnostics."""
    search = (origin + float(search_start_offset_s), origin + float(search_end_offset_s))
    in_noise = [t for t in onset_times if windows["noise"][0] <= t < windows["noise"][1]]
    in_search = [t for t in onset_times if search[0] <= t < search[1]]
    primary = in_search[0] if in_search else None
    classified = classify_trigger(primary, origin, windows)
    classified["false_trigger_candidate"] = len(in_noise) > 0
    classified["n_onsets_after_edge_mute"] = len(onset_times)
    classified["n_onsets_in_noise_window"] = len(in_noise)
    classified["search_window_start_offset_s"] = float(search_start_offset_s)
    classified["search_window_end_offset_s"] = float(search_end_offset_s)
    if primary is None:
        classified["trigger_class"] = "no_trigger_in_search_window"
    elif float(primary - origin) < 0:
        classified["trigger_class"] = "search_window_pre_origin"
    return classified


def classify_trigger(
    trigger_time: UTCDateTime | None,
    origin: UTCDateTime,
    windows: dict[str, tuple[UTCDateTime, UTCDateTime]],
) -> dict[str, Any]:
    if trigger_time is None:
        return {
            "trigger_time_utc": "",
            "trigger_latency_s": float("nan"),
            "in_noise_window": False,
            "in_expected_event_window": False,
            "false_trigger_candidate": False,
            "trigger_class": "no_trigger",
        }
    latency = float(trigger_time - origin)
    in_noise = windows["noise"][0] <= trigger_time < windows["noise"][1]
    in_expected = windows["expected_trigger"][0] <= trigger_time < windows["expected_trigger"][1]
    if in_noise:
        trigger_class = "false_trigger_candidate_pre_event"
    elif in_expected:
        trigger_class = "expected_event_window"
    elif latency < 0:
        trigger_class = "pre_origin_outside_noise_window"
    else:
        trigger_class = "late_or_outside_expected_window"
    return {
        "trigger_time_utc": str(trigger_time),
        "trigger_latency_s": latency,
        "in_noise_window": in_noise,
        "in_expected_event_window": in_expected,
        "false_trigger_candidate": in_noise,
        "trigger_class": trigger_class,
    }


def units_label(response_output: str, status: str) -> str:
    if status != "applied":
        return "counts"
    output = response_output.upper()
    if output == "VEL":
        return "m/s"
    if output == "ACC":
        return "m/s^2"
    if output == "DISP":
        return "m"
    return f"unknown:{response_output}"


def amplitude_term(units: str, kind: str) -> str:
    """Neutral name unless units justify PGV/PGA."""
    if units == "m/s" and kind in {"peak", "pgv"}:
        return "band_limited_pgv_m_s"
    if units == "m/s^2" and kind in {"peak", "pga"}:
        return "band_limited_pga_m_s2"
    return "peak_response_corrected_amplitude"


def plausibility_flag(peak_velocity: float, peak_acceleration: float, cfg: dict[str, Any]) -> str:
    notes = []
    if math.isfinite(peak_velocity) and peak_velocity > float(cfg["max_peak_velocity_m_s"]):
        notes.append("peak_velocity_exceeds_threshold")
    if math.isfinite(peak_acceleration) and peak_acceleration > float(cfg["max_peak_acceleration_m_s2"]):
        notes.append("peak_acceleration_exceeds_threshold")
    return ";".join(notes) if notes else "ok"


def stationxml_path_for_row(repo_root: Path, metadata_dir: str, event_id: str, station: str, location: str) -> Path:
    short = event_short_id(event_id)
    loc = location if location and location not in {".", ""} else "--"
    return repo_root / metadata_dir / short / f"CH.{station}.{loc}.HH.xml"


def finite_median(values: list[float] | np.ndarray) -> float:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float("nan")
    return float(np.median(arr))


def finite_stats(values: list[float] | np.ndarray) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return {"n": 0, "min": float("nan"), "max": float("nan"), "mean": float("nan"), "median": float("nan")}
    return {
        "n": int(arr.size),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
    }
