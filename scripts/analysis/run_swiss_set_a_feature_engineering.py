#!/usr/bin/env python3
"""Swiss Set A Feature Engineering: ML-Ready 3C Waveform Feature Dataset.

Extracts causal, instrument-response-corrected velocity features (m/s) from the
120 Swiss Set A 3-component broadband records, paired with verified SED manual
analyst P-wave picks. Constructs balanced positive (P-arrival) and negative (noise)
windows for machine learning without future-window data leakage.
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
import pandas as pd
from obspy import Stream, UTCDateTime, read, read_inventory
from obspy.signal.trigger import classic_sta_lta
from scipy.stats import kurtosis, skew

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.analysis.switzerland_signal import (
    epicentral_distance_km,
    has_complete_hh_3c,
    hypocentral_distance_km,
    identify_hh_components,
    pre_filt_for_sampling,
)

SET_A_MANIFEST = REPO_ROOT / "data" / "manifests" / "sed_switzerland_pilot_events.csv"
SET_A_PICKS = REPO_ROOT / "data" / "manifests" / "sed_switzerland_set_a_picks.csv"
RAW_DATA_DIR = REPO_ROOT / "data" / "raw" / "switzerland"
METADATA_DIR = REPO_ROOT / "data" / "metadata" / "switzerland"

OUT_FEATURES_DIR = REPO_ROOT / "reports" / "features"
OUT_FIGURES_DIR = OUT_FEATURES_DIR / "swiss_figures"
OUT_CSV = OUT_FEATURES_DIR / "swiss_set_a_feature_matrix.csv"
OUT_PER_RECORD_CSV = OUT_FEATURES_DIR / "swiss_set_a_per_record_features.csv"
OUT_SUMMARY_JSON = OUT_FEATURES_DIR / "swiss_set_a_feature_summary.json"

# Causal window parameters (seconds)
WINDOW_LENGTH_S = 4.0
STA_WINDOW_S = 0.5
LTA_WINDOW_S = 10.0

# Instrument response deconvolution config
WATER_LEVEL = 60.0
BANDPASS_FMIN = 0.1
BANDPASS_FMAX = 15.0

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("swiss_features")


def _shannon_entropy(p: np.ndarray) -> float:
    p = p.astype(float)
    p = p[p > 0]
    if p.size == 0:
        return float("nan")
    p = p / p.sum()
    return float(-np.sum(p * np.log2(p)))


def _spectral_features(x: np.ndarray, fs: float) -> dict[str, float]:
    n = len(x)
    if n == 0 or fs <= 0:
        return {
            "dominant_frequency_hz": float("nan"),
            "spectral_centroid_hz": float("nan"),
            "spectral_bandwidth_hz": float("nan"),
            "spectral_rolloff_95_hz": float("nan"),
            "spectral_entropy": float("nan"),
        }
    spec = np.fft.rfft(x.astype(float))
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


def extract_single_channel_features(x: np.ndarray, fs: float, prefix: str = "") -> dict[str, float]:
    x = np.asarray(x, dtype=float)
    if x.size == 0:
        return {f"{prefix}{k}": float("nan") for k in [
            "peak_velocity_m_s", "p2p_amplitude_m_s", "rms_velocity_m_s",
            "variance", "std", "zero_crossing_rate_hz", "signal_energy_m2_s",
            "crest_factor", "kurtosis", "skewness", "dominant_frequency_hz",
            "spectral_centroid_hz", "spectral_bandwidth_hz", "spectral_rolloff_95_hz",
            "spectral_entropy", "cav_m_s",
        ]}
    peak = float(np.max(np.abs(x)))
    rms = float(np.sqrt(np.mean(x**2)))
    dt = 1.0 / fs if fs > 0 else 0.0
    spectral = _spectral_features(x, fs)
    cav = float(np.sum(np.abs(x)) * dt)

    out = {
        f"{prefix}peak_velocity_m_s": peak,
        f"{prefix}p2p_amplitude_m_s": float(np.ptp(x)),
        f"{prefix}rms_velocity_m_s": rms,
        f"{prefix}variance": float(np.var(x)),
        f"{prefix}std": float(np.std(x)),
        f"{prefix}zero_crossing_rate_hz": _zero_crossing_rate_hz(x, fs),
        f"{prefix}signal_energy_m2_s": float(np.sum(x**2) * dt),
        f"{prefix}crest_factor": peak / max(rms, 1e-12),
        f"{prefix}kurtosis": float(kurtosis(x)),
        f"{prefix}skewness": float(skew(x)),
        f"{prefix}cav_m_s": cav,
    }
    for k, v in spectral.items():
        out[f"{prefix}{k}"] = v
    return out


def extract_3c_window_features(
    z: np.ndarray,
    n: np.ndarray,
    e: np.ndarray,
    fs: float,
    baseline_noise_rms: float = 1e-12,
    cft_slice: np.ndarray | None = None,
) -> dict[str, float]:
    """Compute features across 3 components and vector magnitudes."""
    z = np.asarray(z, dtype=float)
    n = np.asarray(n, dtype=float)
    e = np.asarray(e, dtype=float)

    # 1. Individual vertical features
    z_feats = extract_single_channel_features(z, fs, prefix="z_")

    # 2. Vector horizontal and 3C magnitudes
    h_vec = np.sqrt(n**2 + e**2)
    vec_3c = np.sqrt(z**2 + n**2 + e**2)

    h_peak = float(np.max(h_vec)) if h_vec.size > 0 else float("nan")
    h_rms = float(np.sqrt(np.mean(h_vec**2))) if h_vec.size > 0 else float("nan")
    vec3c_peak = float(np.max(vec_3c)) if vec_3c.size > 0 else float("nan")
    vec3c_rms = float(np.sqrt(np.mean(vec_3c**2))) if vec_3c.size > 0 else float("nan")

    z_rms = z_feats["z_rms_velocity_m_s"]
    vh_ratio = z_rms / max(h_rms, 1e-12)

    # 3. STA/LTA characteristic function from continuous vertical trace
    if cft_slice is not None and len(cft_slice) > 0:
        sta_lta_max = float(np.max(cft_slice))
        sta_lta_mean = float(np.mean(cft_slice))
    else:
        sta_lta_max = 1.0
        sta_lta_mean = 1.0

    # 4. SNR relative to station baseline noise RMS
    snr_linear = vec3c_rms / max(baseline_noise_rms, 1e-12)
    snr_db = float(20.0 * np.log10(max(snr_linear, 1e-6)))

    out = {
        **z_feats,
        "h_peak_velocity_m_s": h_peak,
        "h_rms_velocity_m_s": h_rms,
        "vec3c_peak_velocity_m_s": vec3c_peak,
        "vec3c_rms_velocity_m_s": vec3c_rms,
        "vh_ratio": vh_ratio,
        "sta_lta_max": sta_lta_max,
        "sta_lta_mean": sta_lta_mean,
        "snr_db": snr_db,
    }
    return out


def slice_window_samples(trace_data: np.ndarray, trace_start: UTCDateTime, fs: float, win_start: UTCDateTime, win_len_s: float) -> np.ndarray:
    n_samples = int(round(win_len_s * fs))
    start_idx = int(round((win_start - trace_start) * fs))
    end_idx = start_idx + n_samples
    if start_idx < 0 or end_idx > len(trace_data):
        raise ValueError(f"Window [{win_start}, +{win_len_s}s] outside trace bounds [{trace_start}, {trace_start + len(trace_data)/fs}s]")
    return trace_data[start_idx:end_idx]


def main():
    logger.info("Starting STEP ML-2: Swiss Set A Feature Extraction...")

    OUT_FEATURES_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    with SET_A_MANIFEST.open("r", encoding="utf-8") as f:
        manifest_rows = list(csv.DictReader(f))
    with SET_A_PICKS.open("r", encoding="utf-8") as f:
        pick_rows = list(csv.DictReader(f))

    picks_map = {(r["short_id"], r["station"].upper()): r for r in pick_rows}
    logger.info("Loaded %d manifest records and %d picks.", len(manifest_rows), len(picks_map))

    window_dataset_rows: list[dict[str, Any]] = []
    record_dataset_rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    for idx, row in enumerate(manifest_rows):
        eid = row["event_id"]
        sid = eid.split("/")[-1]
        sta = row["station"].strip().upper()
        key = (sid, sta)

        pick = picks_map.get(key)
        if not pick:
            failures.append({"short_id": sid, "station": sta, "reason": "Missing verified pick"})
            continue

        mseed_path = REPO_ROOT / row["waveform_file"]
        xml_path = REPO_ROOT / f"data/metadata/switzerland/{sid}/CH.{sta}.--.HH.xml"

        if not mseed_path.exists():
            failures.append({"short_id": sid, "station": sta, "reason": f"MiniSEED not found: {mseed_path}"})
            continue
        if not xml_path.exists():
            failures.append({"short_id": sid, "station": sta, "reason": f"StationXML not found: {xml_path}"})
            continue

        try:
            st = read(str(mseed_path))
            inv = read_inventory(str(xml_path))

            if not has_complete_hh_3c(st):
                failures.append({"short_id": sid, "station": sta, "reason": "Missing 3C channels"})
                continue

            comp = identify_hh_components(st)
            tr_z = st[comp["HHZ"]]
            tr_n = st[comp["HHN"]]
            tr_e = st[comp["HHE"]]

            fs = float(tr_z.stats.sampling_rate)
            nyquist = 0.5 * fs

            # Deconvolve instrument response to velocity (m/s)
            resp_cfg = {
                "pre_filt_f1_hz": 0.05,
                "pre_filt_f2_hz": 0.08,
                "pre_filt_f3_nyquist_fraction": 0.75,
                "pre_filt_f4_nyquist_fraction": 0.85,
            }
            bp_cfg = {"freqmax_hz": BANDPASS_FMAX}
            pre_filt = pre_filt_for_sampling(fs, resp_cfg, bp_cfg)

            st_proc = st.copy()
            st_proc.detrend("demean")
            st_proc.detrend("linear")
            st_proc.taper(max_percentage=0.05, type="hann")
            st_proc.remove_response(
                inventory=inv,
                output="VEL",
                water_level=WATER_LEVEL,
                pre_filt=pre_filt,
                zero_mean=True,
                taper=False,
            )
            st_proc.filter("bandpass", freqmin=BANDPASS_FMIN, freqmax=BANDPASS_FMAX, corners=4, zerophase=True)

            tr_z_v = st_proc[comp["HHZ"]].data
            tr_n_v = st_proc[comp["HHN"]].data
            tr_e_v = st_proc[comp["HHE"]].data

            trace_start = tr_z.stats.starttime
            origin_utc = UTCDateTime(row["origin_time_utc"])
            p_pick_utc = UTCDateTime(pick["pick_time_utc"])

            # Metadata & distances
            ev_lat = float(row["latitude"])
            ev_lon = float(row["longitude"])
            ev_depth = float(row["depth_km"])
            mag = float(row["magnitude"])

            sta_coords = inv.get_coordinates(f"CH.{sta}..HHZ")
            sta_lat = sta_coords["latitude"]
            sta_lon = sta_coords["longitude"]

            epi_dist = epicentral_distance_km(ev_lat, ev_lon, sta_lat, sta_lon)
            hypo_dist = hypocentral_distance_km(epi_dist, ev_depth)
            p_latency = float(p_pick_utc - origin_utc)

            # Compute continuous STA/LTA on full vertical velocity trace
            nsta_full = max(int(STA_WINDOW_S * fs), 1)
            nlta_full = max(int(LTA_WINDOW_S * fs), nsta_full + 1)
            cft_full = classic_sta_lta(tr_z_v, nsta_full, nlta_full)

            # Baseline noise RMS for SNR calculation (from quiet window [origin - 45s, origin - 15s])
            noise_base_start = origin_utc - 45.0
            noise_base_z = slice_window_samples(tr_z_v, trace_start, fs, noise_base_start, 30.0)
            baseline_noise_rms = float(np.sqrt(np.mean(noise_base_z**2)))

            # Window 1: Negative Class (Ambient Noise Window) -> is_earthquake = 0
            # Strictly causal: origin - 35s to origin - 31s (before any earthquake origin or P-arrival)
            noise_win_start = origin_utc - 35.0
            noise_z = slice_window_samples(tr_z_v, trace_start, fs, noise_win_start, WINDOW_LENGTH_S)
            noise_n = slice_window_samples(tr_n_v, trace_start, fs, noise_win_start, WINDOW_LENGTH_S)
            noise_e = slice_window_samples(tr_e_v, trace_start, fs, noise_win_start, WINDOW_LENGTH_S)
            cft_noise = slice_window_samples(cft_full, trace_start, fs, noise_win_start, WINDOW_LENGTH_S)

            noise_features = extract_3c_window_features(noise_z, noise_n, noise_e, fs, baseline_noise_rms, cft_noise)

            # Window 2: Positive Class (Early P-Arrival Window) -> is_earthquake = 1
            # Strictly causal: P_pick to P_pick + 4.0s (first 4s of P-wave energy)
            p_win_start = p_pick_utc
            p_z = slice_window_samples(tr_z_v, trace_start, fs, p_win_start, WINDOW_LENGTH_S)
            p_n = slice_window_samples(tr_n_v, trace_start, fs, p_win_start, WINDOW_LENGTH_S)
            p_e = slice_window_samples(tr_e_v, trace_start, fs, p_win_start, WINDOW_LENGTH_S)
            cft_p = slice_window_samples(cft_full, trace_start, fs, p_win_start, WINDOW_LENGTH_S)

            p_features = extract_3c_window_features(p_z, p_n, p_e, fs, baseline_noise_rms, cft_p)

            common_meta = {
                "event_id": eid,
                "short_id": sid,
                "station": sta,
                "channel_group": "HH_3C",
                "sampling_rate_hz": fs,
                "magnitude": mag,
                "magnitude_type": row["magnitude_type"],
                "region": row["region"],
                "epicentral_distance_km": round(epi_dist, 3),
                "hypocentral_distance_km": round(hypo_dist, 3),
                "origin_time_utc": str(origin_utc),
                "p_pick_time_utc": str(p_pick_utc),
                "p_latency_s": round(p_latency, 4),
                "p_phase": pick["pick_phase"],
                "p_evaluation_mode": pick["pick_evaluation_mode"],
            }

            # Append Class 0 (Noise)
            window_dataset_rows.append({
                **common_meta,
                "sample_id": f"{sid}_{sta}_noise",
                "window_type": "ambient_noise",
                "is_earthquake": 0,
                "window_start_utc": str(noise_win_start),
                "window_end_utc": str(noise_win_start + WINDOW_LENGTH_S),
                "window_duration_s": WINDOW_LENGTH_S,
                **noise_features,
            })

            # Append Class 1 (Earthquake P-Wave)
            window_dataset_rows.append({
                **common_meta,
                "sample_id": f"{sid}_{sta}_p_arrival",
                "window_type": "early_p_wave",
                "is_earthquake": 1,
                "window_start_utc": str(p_win_start),
                "window_end_utc": str(p_win_start + WINDOW_LENGTH_S),
                "window_duration_s": WINDOW_LENGTH_S,
                **p_features,
            })

            # Append per-record summary (120 rows)
            record_dataset_rows.append({
                **common_meta,
                "baseline_noise_rms_m_s": baseline_noise_rms,
                "p_window_vec3c_peak_m_s": p_features["vec3c_peak_velocity_m_s"],
                "p_window_snr_db": p_features["snr_db"],
                "p_window_vh_ratio": p_features["vh_ratio"],
                "p_window_sta_lta_max": p_features["sta_lta_max"],
                "noise_window_vec3c_peak_m_s": noise_features["vec3c_peak_velocity_m_s"],
                "noise_window_sta_lta_max": noise_features["sta_lta_max"],
            })

            if (idx + 1) % 20 == 0:
                logger.info("Processed %d / %d records...", idx + 1, len(manifest_rows))

        except Exception as exc:
            logger.error("Error processing %s %s: %s", sid, sta, exc)
            failures.append({"short_id": sid, "station": sta, "reason": str(exc)})

    logger.info("Completed processing. Success: %d records, Failures: %d", len(record_dataset_rows), len(failures))

    # Save Window-Level Feature Matrix (240 samples: 120 Noise + 120 P-arrival)
    df_window = pd.DataFrame(window_dataset_rows)
    df_window.to_csv(OUT_CSV, index=False)
    logger.info("Saved ML-ready feature matrix (%d rows, %d cols) to %s", len(df_window), len(df_window.columns), OUT_CSV)

    # Save Record-Level Feature Matrix (120 records)
    df_record = pd.DataFrame(record_dataset_rows)
    df_record.to_csv(OUT_PER_RECORD_CSV, index=False)
    logger.info("Saved per-record feature table (%d rows) to %s", len(df_record), OUT_PER_RECORD_CSV)

    # Summary JSON
    numeric_cols = [c for c in df_window.columns if df_window[c].dtype in (np.float64, np.int64) and c not in ("is_earthquake", "magnitude", "epicentral_distance_km", "hypocentral_distance_km", "sampling_rate_hz", "window_duration_s", "p_latency_s")]

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "task": "STEP ML-2: Swiss Set A Feature Extraction",
        "units": "Velocity in m/s, time in s, frequency in Hz, SNR in dB",
        "n_records_processed": len(record_dataset_rows),
        "n_samples_window_dataset": len(df_window),
        "class_balance": {
            "is_earthquake_0_noise": int((df_window["is_earthquake"] == 0).sum()),
            "is_earthquake_1_p_arrival": int((df_window["is_earthquake"] == 1).sum()),
        },
        "feature_count_total": len(numeric_cols),
        "feature_names": numeric_cols,
        "causal_window_length_s": WINDOW_LENGTH_S,
        "instrument_response_output": "VEL (m/s)",
        "bandpass_hz": [BANDPASS_FMIN, BANDPASS_FMAX],
        "n_unique_events": int(df_window["short_id"].nunique()),
        "n_unique_stations": int(df_window["station"].nunique()),
        "failures_count": len(failures),
        "failures": failures,
        "feature_means_by_class": {
            "noise": {col: float(df_window[df_window["is_earthquake"] == 0][col].mean()) for col in numeric_cols[:10]},
            "p_wave": {col: float(df_window[df_window["is_earthquake"] == 1][col].mean()) for col in numeric_cols[:10]},
        },
    }

    with OUT_SUMMARY_JSON.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    logger.info("Saved summary JSON to %s", OUT_SUMMARY_JSON)

    # Generate QC Figures
    _generate_qc_plots(df_window, df_record)
    logger.info("STEP ML-2 COMPLETED SUCCESSFULLY!")


def _generate_qc_plots(df_window: pd.DataFrame, df_record: pd.DataFrame) -> None:
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # Fig 01: P-wave vs Noise Peak Velocity Distributions
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    noise = df_window[df_window["is_earthquake"] == 0]["vec3c_peak_velocity_m_s"] * 1e6  # to um/s
    p_wave = df_window[df_window["is_earthquake"] == 1]["vec3c_peak_velocity_m_s"] * 1e6

    try:
        axes[0].boxplot([noise, p_wave], tick_labels=["Noise (Pre-Origin)", "P-Wave (4s Onset)"], patch_artist=True)
    except TypeError:
        axes[0].boxplot([noise, p_wave], labels=["Noise (Pre-Origin)", "P-Wave (4s Onset)"], patch_artist=True)
    axes[0].set_yscale("log")
    axes[0].set_ylabel("Peak 3C Velocity (μm/s) [Log scale]")
    axes[0].set_title("Peak Velocity: Ambient Noise vs. Early P-Wave")

    snr = df_window[df_window["is_earthquake"] == 1]["snr_db"]
    axes[1].hist(snr, bins=15, color="steelblue", edgecolor="black", alpha=0.8)
    axes[1].set_xlabel("Signal-to-Noise Ratio (dB)")
    axes[1].set_ylabel("Record Count")
    axes[1].set_title("Set A P-Wave Window SNR Distribution (dB)")
    fig.tight_layout()
    fig.savefig(OUT_FIGURES_DIR / "fig01_noise_vs_pwave_velocity.png", dpi=300)
    plt.close(fig)

    # Fig 02: P-wave travel-time curve (verified picks vs distance)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df_record["hypocentral_distance_km"], df_record["p_latency_s"], c=df_record["magnitude"], cmap="viridis", s=50, edgecolors="k", alpha=0.9)
    dist_grid = np.linspace(0, max(df_record["hypocentral_distance_km"]) + 10, 100)
    ax.plot(dist_grid, dist_grid / 6.0, "r--", label="Reference Crustal P-Velocity (6.0 km/s)")
    ax.plot(dist_grid, dist_grid / 8.0, "b:", label="Upper Mantle Pn (8.0 km/s)")
    ax.set_xlabel("Hypocentral Distance (km)")
    ax.set_ylabel("P-Wave Arrival Latency after Origin (s)")
    ax.set_title("Swiss Set A: Verified Manual P-Arrival Latency vs. Distance")
    ax.legend()
    fig.colorbar(ax.collections[0], label="Magnitude (MLh/MLhc)")
    fig.tight_layout()
    fig.savefig(OUT_FIGURES_DIR / "fig02_p_latency_vs_distance.png", dpi=300)
    plt.close(fig)

    # Fig 03: V/H ratio vs STA/LTA
    fig, ax = plt.subplots(figsize=(8, 6))
    x_sta = np.clip(df_window["sta_lta_max"].fillna(1.0).astype(float), 0.1, None)
    y_vh = np.clip(df_window["vh_ratio"].fillna(1.0).astype(float), 0.01, None)
    scatter = ax.scatter(
        x_sta,
        y_vh,
        c=df_window["is_earthquake"],
        cmap="coolwarm",
        alpha=0.85,
        edgecolors="k",
        s=45,
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Max STA/LTA Ratio (Log scale)")
    ax.set_ylabel("Vertical-to-Horizontal Ratio (V/H) [Log scale]")
    ax.set_title("Feature Space Discrimination: STA/LTA vs. V/H Ratio")
    cbar = fig.colorbar(scatter, ticks=[0, 1])
    cbar.ax.set_yticklabels(["Noise (0)", "P-Wave (1)"])
    fig.tight_layout()
    fig.savefig(OUT_FIGURES_DIR / "fig03_sta_lta_vs_vh_ratio.png", dpi=300)
    plt.close(fig)

    # Fig 04: Dominant Frequency vs Signal Energy
    fig, ax = plt.subplots(figsize=(8, 6))
    x_energy = np.clip(df_window["z_signal_energy_m2_s"].fillna(1e-12).astype(float), 1e-15, None)
    y_freq = np.clip(df_window["z_dominant_frequency_hz"].fillna(1.0).astype(float), 0.1, None)
    scatter = ax.scatter(
        x_energy,
        y_freq,
        c=df_window["is_earthquake"],
        cmap="coolwarm",
        alpha=0.85,
        edgecolors="k",
        s=45,
    )
    ax.set_xscale("log")
    ax.set_xlabel("Vertical Signal Energy (m²/s) [Log scale]")
    ax.set_ylabel("Dominant Frequency (Hz)")
    ax.set_title("Feature Space Discrimination: Energy vs. Dominant Frequency")
    cbar = fig.colorbar(scatter, ticks=[0, 1])
    cbar.ax.set_yticklabels(["Noise (0)", "P-Wave (1)"])
    fig.tight_layout()
    fig.savefig(OUT_FIGURES_DIR / "fig04_energy_vs_frequency.png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
