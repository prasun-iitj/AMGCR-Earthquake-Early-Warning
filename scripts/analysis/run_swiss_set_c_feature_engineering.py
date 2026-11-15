"""Feature Extraction script for Swiss Set C Vertical (HHZ) Waveforms.

AMGCR Earthquake Research - Supervised ML Track (STEP ML-4)
Extracts the exact 18 vertical-component features for independent cross-dataset evaluation.
Total: 550 records * 2 windows = 1,100 samples across 15 events.
"""

from __future__ import annotations

import csv
import json
import logging
import math
import sys
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd
from obspy import UTCDateTime, read, read_inventory
from obspy.signal.trigger import classic_sta_lta
from scipy.stats import kurtosis, skew

from src.models.vertical_models import VERTICAL_FEATURE_COLUMNS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("swiss_set_c_features")

SET_C_MANIFEST = PROJECT_ROOT / "data/manifests/sed_switzerland_validation_waveforms.csv"
OUTPUT_DIR = PROJECT_ROOT / "reports/features"
SET_C_FEATURE_MATRIX_PATH = OUTPUT_DIR / "swiss_set_c_feature_matrix.csv"
SET_C_FEATURE_SUMMARY_PATH = OUTPUT_DIR / "swiss_set_c_feature_summary.json"

WINDOW_LENGTH_S = 4.0
STA_WINDOW_S = 1.0
LTA_WINDOW_S = 10.0
WATER_LEVEL = 60.0
BANDPASS_FMIN = 0.1
BANDPASS_FMAX = 15.0


def _shannon_entropy(p: np.ndarray) -> float:
    p = np.asarray(p, dtype=float)
    s = p.sum()
    if s <= 0:
        return 0.0
    p = p / s
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))


def _spectral_features(x: np.ndarray, fs: float) -> dict[str, float]:
    n = len(x)
    if n < 4 or fs <= 0:
        return {
            "dominant_frequency_hz": float("nan"),
            "spectral_centroid_hz": float("nan"),
            "spectral_bandwidth_hz": float("nan"),
            "spectral_rolloff_95_hz": float("nan"),
            "spectral_entropy": float("nan"),
        }
    spec = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    power = (np.abs(spec) ** 2).astype(float)
    if power.sum() <= 0:
        return {
            "dominant_frequency_hz": float("nan"),
            "spectral_centroid_hz": float("nan"),
            "spectral_bandwidth_hz": float("nan"),
            "spectral_rolloff_95_hz": float("nan"),
            "spectral_entropy": float("nan"),
        }
    mask = freqs > 0
    f_pos = freqs[mask]
    p_pos = power[mask]
    p_sum = p_pos.sum()
    centroid = float(np.sum(f_pos * p_pos) / p_sum)
    bandwidth = float(np.sqrt(np.sum(((f_pos - centroid) ** 2) * p_pos) / p_sum))
    dom_idx = int(np.argmax(p_pos))
    dominant = float(f_pos[dom_idx])
    cum = np.cumsum(p_pos) / p_sum
    rolloff_idx = int(np.searchsorted(cum, 0.95))
    rolloff = float(f_pos[min(rolloff_idx, len(f_pos) - 1)])
    spec_entropy = _shannon_entropy(p_pos)
    return {
        "dominant_frequency_hz": dominant,
        "spectral_centroid_hz": centroid,
        "spectral_bandwidth_hz": bandwidth,
        "spectral_rolloff_95_hz": rolloff,
        "spectral_entropy": spec_entropy,
    }


def _zero_crossing_rate_hz(x: np.ndarray, fs: float) -> float:
    if len(x) < 2 or fs <= 0:
        return 0.0
    signs = np.signbit(x.astype(float))
    crossings = np.sum(signs[1:] != signs[:-1])
    duration = len(x) / fs
    return float(crossings / duration) if duration > 0 else 0.0


def extract_vertical_channel_features(x: np.ndarray, fs: float, cft_slice: np.ndarray | None = None) -> dict[str, float]:
    """Compute the 18 vertical features for a 4-second trace slice."""
    x = np.asarray(x, dtype=float)
    if x.size == 0:
        return {k: float("nan") for k in VERTICAL_FEATURE_COLUMNS}

    peak = float(np.max(np.abs(x)))
    rms = float(np.sqrt(np.mean(x**2)))
    dt = 1.0 / fs if fs > 0 else 0.0
    spectral = _spectral_features(x, fs)
    cav = float(np.sum(np.abs(x)) * dt)

    sta_lta_max = float(np.max(cft_slice)) if (cft_slice is not None and len(cft_slice) > 0) else 1.0
    sta_lta_mean = float(np.mean(cft_slice)) if (cft_slice is not None and len(cft_slice) > 0) else 1.0

    return {
        "z_peak_velocity_m_s": peak,
        "z_p2p_amplitude_m_s": float(np.ptp(x)),
        "z_rms_velocity_m_s": rms,
        "z_variance": float(np.var(x)),
        "z_std": float(np.std(x)),
        "z_zero_crossing_rate_hz": _zero_crossing_rate_hz(x, fs),
        "z_signal_energy_m2_s": float(np.sum(x**2) * dt),
        "z_crest_factor": peak / max(rms, 1e-12),
        "z_kurtosis": float(kurtosis(x)),
        "z_skewness": float(skew(x)),
        "z_cav_m_s": cav,
        "z_dominant_frequency_hz": spectral["dominant_frequency_hz"],
        "z_spectral_centroid_hz": spectral["spectral_centroid_hz"],
        "z_spectral_bandwidth_hz": spectral["spectral_bandwidth_hz"],
        "z_spectral_rolloff_95_hz": spectral["spectral_rolloff_95_hz"],
        "z_spectral_entropy": spectral["spectral_entropy"],
        "sta_lta_max": sta_lta_max,
        "sta_lta_mean": sta_lta_mean,
    }


def slice_window(data: np.ndarray, trace_start: UTCDateTime, fs: float, win_start: UTCDateTime, win_len_s: float) -> np.ndarray:
    n_samples = int(round(win_len_s * fs))
    start_idx = int(round((win_start - trace_start) * fs))
    end_idx = start_idx + n_samples
    if start_idx < 0 or end_idx > len(data):
        raise ValueError(f"Window [{win_start}, {win_start + win_len_s}] out of bounds for trace starting at {trace_start}")
    return data[start_idx:end_idx]


def main() -> None:
    logger.info("Starting STEP ML-4: Swiss Set C Feature Extraction (18 Vertical Features)...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with SET_C_MANIFEST.open("r", encoding="utf-8") as f:
        manifest_rows = list(csv.DictReader(f))

    logger.info("Loaded %d Set C waveform records across %d unique events.",
                len(manifest_rows), len(set(r["short_id"] for r in manifest_rows)))

    dataset_rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    for idx, row in enumerate(manifest_rows):
        sid = row["short_id"]
        sta = row["station"].strip().upper()
        mseed_path = PROJECT_ROOT / row["MiniSEED_path"]
        xml_path = PROJECT_ROOT / row["StationXML_path"]

        if not mseed_path.exists():
            failures.append({"row": idx, "short_id": sid, "station": sta, "reason": "Missing MiniSEED"})
            continue
        if not xml_path.exists():
            failures.append({"row": idx, "short_id": sid, "station": sta, "reason": "Missing StationXML"})
            continue

        try:
            st = read(str(mseed_path))
            if len(st) > 1:
                st.merge(method=1, fill_value="interpolate")
            inv = read_inventory(str(xml_path))

            tr_z = st[0]
            fs = float(tr_z.stats.sampling_rate)
            nyquist = 0.5 * fs

            # Nyquist-aware pre-filter frequencies
            f1, f2 = 0.05, 0.08
            f3 = min(BANDPASS_FMAX * 1.2, nyquist * 0.75)
            f4 = min(BANDPASS_FMAX * 1.5, nyquist * 0.85)
            if f4 <= f3:
                f4 = min(nyquist * 0.95, f3 + 5.0)

            st_proc = st.copy()
            st_proc.detrend("demean")
            st_proc.detrend("linear")
            st_proc.taper(max_percentage=0.05, type="hann")
            st_proc.remove_response(
                inventory=inv,
                output="VEL",
                water_level=WATER_LEVEL,
                pre_filt=(f1, f2, f3, f4),
                zero_mean=True,
                taper=False,
            )
            st_proc.filter("bandpass", freqmin=BANDPASS_FMIN, freqmax=BANDPASS_FMAX, corners=4, zerophase=True)

            tr_z_v = st_proc[0].data
            trace_start = tr_z.stats.starttime
            origin_utc = UTCDateTime(row["origin_time"])
            pick_utc = UTCDateTime(row["pick_time_utc"])

            # Compute continuous STA/LTA on full vertical velocity trace
            nsta_full = max(int(STA_WINDOW_S * fs), 1)
            nlta_full = max(int(LTA_WINDOW_S * fs), nsta_full + 1)
            cft_full = classic_sta_lta(tr_z_v, nsta_full, nlta_full)

            # Window 1: Negative Class (Pre-Origin Ambient Noise Window) -> is_earthquake = 0
            noise_start = origin_utc - 35.0
            noise_z = slice_window(tr_z_v, trace_start, fs, noise_start, WINDOW_LENGTH_S)
            cft_noise = slice_window(cft_full, trace_start, fs, noise_start, WINDOW_LENGTH_S)
            noise_feats = extract_vertical_channel_features(noise_z, fs, cft_noise)

            dataset_rows.append({
                "event_id": row["event_id"],
                "short_id": sid,
                "station": sta,
                "magnitude": float(row["magnitude"]),
                "magnitude_type": row["magnitude_type"],
                "region": row["region"],
                "sampling_rate_hz": fs,
                "origin_time_utc": origin_utc.isoformat(),
                "p_pick_time_utc": pick_utc.isoformat(),
                "p_phase": row["pick_phase"],
                "p_evaluation_mode": row["pick_evaluation_mode"],
                "sample_id": f"{sid}_{sta}_noise",
                "window_type": "ambient_noise",
                "is_earthquake": 0,
                "window_start_utc": noise_start.isoformat(),
                "window_end_utc": (noise_start + WINDOW_LENGTH_S).isoformat(),
                "window_duration_s": WINDOW_LENGTH_S,
                **noise_feats,
            })

            # Window 2: Positive Class (Early P-wave Arrival Window) -> is_earthquake = 1
            p_start = pick_utc
            p_z = slice_window(tr_z_v, trace_start, fs, p_start, WINDOW_LENGTH_S)
            cft_p = slice_window(cft_full, trace_start, fs, p_start, WINDOW_LENGTH_S)
            p_feats = extract_vertical_channel_features(p_z, fs, cft_p)

            dataset_rows.append({
                "event_id": row["event_id"],
                "short_id": sid,
                "station": sta,
                "magnitude": float(row["magnitude"]),
                "magnitude_type": row["magnitude_type"],
                "region": row["region"],
                "sampling_rate_hz": fs,
                "origin_time_utc": origin_utc.isoformat(),
                "p_pick_time_utc": pick_utc.isoformat(),
                "p_phase": row["pick_phase"],
                "p_evaluation_mode": row["pick_evaluation_mode"],
                "sample_id": f"{sid}_{sta}_p_wave",
                "window_type": "early_p_wave",
                "is_earthquake": 1,
                "window_start_utc": p_start.isoformat(),
                "window_end_utc": (p_start + WINDOW_LENGTH_S).isoformat(),
                "window_duration_s": WINDOW_LENGTH_S,
                **p_feats,
            })

        except Exception as e:
            failures.append({"row": idx, "short_id": sid, "station": sta, "reason": str(e)})

    logger.info("Extraction complete: %d samples extracted, %d failures.", len(dataset_rows), len(failures))
    if failures:
        logger.warning("Failures encountered: %s", failures[:5])

    df_c = pd.DataFrame(dataset_rows)
    df_c.to_csv(SET_C_FEATURE_MATRIX_PATH, index=False)
    logger.info("Saved Set C feature matrix to: %s (shape: %s)", SET_C_FEATURE_MATRIX_PATH, df_c.shape)

    # Compute summary stats
    summary_payload = {
        "dataset": "Swiss Set C Vertical Feature Matrix",
        "n_records_processed": len(manifest_rows),
        "n_samples_window_dataset": len(df_c),
        "class_balance": df_c["is_earthquake"].value_counts().to_dict(),
        "n_events": df_c["short_id"].nunique(),
        "n_stations": df_c["station"].nunique(),
        "features": VERTICAL_FEATURE_COLUMNS,
        "n_features": len(VERTICAL_FEATURE_COLUMNS),
        "failures_count": len(failures),
        "failures": failures,
    }
    with open(SET_C_FEATURE_SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2)
    logger.info("Saved Set C summary to: %s", SET_C_FEATURE_SUMMARY_PATH)


if __name__ == "__main__":
    main()
