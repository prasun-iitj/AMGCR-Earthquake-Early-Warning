#!/usr/bin/env python3
"""Phase A.2 waveform signal analysis for the California IRIS pilot.

Analyses every manifest-linked MiniSEED trace: amplitudes, noise proxy, SNR,
STA/LTA P-wave pick, and per-event figures. Standalone from EarthESND ``src/``.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from obspy import read
from obspy.signal.trigger import classic_sta_lta, trigger_onset

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_IRIS = REPO_ROOT / "data" / "raw" / "iris"
MANIFEST_PATH = REPO_ROOT / "data" / "manifests" / "iris_california_pilot_events.csv"
OUT_SIGNAL = REPO_ROOT / "reports" / "signal_analysis"
OUT_FIGURES = REPO_ROOT / "reports" / "figures"
OUT_TABLES = REPO_ROOT / "reports" / "tables"

STA_LTA_THRESHOLD = 2.5
STA_WINDOW_S = 0.5
LTA_WINDOW_S = 10.0
NOISE_MAX_S = 5.0
NOISE_MARGIN_BEFORE_P_S = 0.5
SIGNAL_DURATION_THRESHOLD_SIGMA = 3.0


def _apply_plot_style() -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "font.family": "DejaVu Sans",
            "axes.labelsize": 11,
            "axes.titlesize": 11,
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "axes.grid": True,
            "grid.alpha": 0.35,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def _short_event_id(event_id: str) -> str:
    match = re.search(r"eventid_([^_]+)_format", event_id)
    return match.group(1) if match else event_id[-24:]


@dataclass
class WaveformMetrics:
    event_id: str
    origin_time_utc: str
    magnitude: float
    magnitude_type: str
    station_id: str
    channel: str
    waveform_file: str
    sampling_rate_hz: float
    trace_duration_s: float
    peak_amplitude_counts: float
    rms_amplitude_counts: float
    rms_signal_window_counts: float
    noise_rms_counts: float
    noise_window_start_s: float
    noise_window_end_s: float
    noise_window_note: str
    snr_peak: float
    snr_rms: float
    signal_duration_s: float
    sta_lta_threshold: float
    sta_window_s: float
    lta_window_s: float
    p_pick_time_s: float
    p_pick_sample: int
    p_pick_sta_lta_value: float
    p_pick_method: str


def _noise_window(p_pick_sample: int, df: float, n_samples: int) -> tuple[int, int, str]:
    """Return noise sample range [i0, i1) and description."""
    p_time_s = p_pick_sample / df
    if p_pick_sample > int(NOISE_MARGIN_BEFORE_P_S * df) + 10:
        end_s = min(p_time_s - NOISE_MARGIN_BEFORE_P_S, NOISE_MAX_S)
        end_sample = max(int(end_s * df), int(0.5 * df))
        if end_sample >= 10:
            return 0, end_sample, "samples_before_sta_lta_pick"
    fallback = min(int(NOISE_MAX_S * df), n_samples // 4, p_pick_sample)
    fallback = max(fallback, int(1.0 * df))
    return 0, min(fallback, n_samples), "initial_segment_proxy_no_pre_event_data"


def _signal_duration_s(
    data: np.ndarray,
    p_sample: int,
    df: float,
    noise_rms: float,
) -> float:
    if p_sample >= len(data) - 1:
        return 0.0
    threshold = SIGNAL_DURATION_THRESHOLD_SIGMA * max(noise_rms, 1e-12)
    post = np.abs(data[p_sample:].astype(float))
    above = post >= threshold
    if not np.any(above):
        return 0.0
    last_idx = int(np.max(np.where(above)[0]))
    return (last_idx + 1) / df


def _pick_p_sta_lta(data: np.ndarray, df: float) -> tuple[int, float, np.ndarray, str]:
    nsta = max(int(STA_WINDOW_S * df), 1)
    nlta = max(int(LTA_WINDOW_S * df), nsta + 1)
    cft = classic_sta_lta(data.astype(float), nsta, nlta)
    onsets = trigger_onset(cft, STA_LTA_THRESHOLD, 0.5)
    if len(onsets) > 0:
        sample = int(onsets[0, 0])
        val = float(cft[sample]) if sample < len(cft) else float("nan")
        return sample, val, cft, "trigger_onset_first"
    crossings = np.where(cft[nlta:] >= STA_LTA_THRESHOLD)[0]
    if len(crossings) == 0:
        sample = nlta
        return sample, float(cft[sample]), cft, "no_crossing_used_lta_end"
    sample = int(crossings[0] + nlta)
    return sample, float(cft[sample]), cft, "first_threshold_crossing"


def analyze_trace(row: pd.Series) -> WaveformMetrics:
    rel = str(row["waveform_files"]).replace("\\", "/")
    path = RAW_IRIS / rel
    tr = read(str(path))[0]
    data = tr.data.astype(float)
    df = float(tr.stats.sampling_rate)
    n = len(data)
    net = tr.stats.network
    sta = tr.stats.station
    loc = tr.stats.location or "--"
    cha = tr.stats.channel
    station_id = f"{net}.{sta}.{loc}.{cha}"

    p_sample, p_cft_val, _cft, pick_method = _pick_p_sta_lta(data, df)
    p_time_s = p_sample / df

    i0, i1, noise_note = _noise_window(p_sample, df, n)
    noise_seg = data[i0:i1]
    noise_rms = float(np.sqrt(np.mean(noise_seg**2))) if len(noise_seg) else float("nan")

    peak = float(np.max(np.abs(data)))
    rms_full = float(np.sqrt(np.mean(data**2)))
    sig_end = n
    sig_seg = data[p_sample:sig_end]
    rms_signal = float(np.sqrt(np.mean(sig_seg**2))) if len(sig_seg) else float("nan")

    snr_peak = peak / max(noise_rms, 1e-12)
    snr_rms = rms_signal / max(noise_rms, 1e-12)
    sig_dur = _signal_duration_s(data, p_sample, df, noise_rms)

    return WaveformMetrics(
        event_id=str(row["event_id"]),
        origin_time_utc=pd.Timestamp(row["origin_time_utc"]).isoformat(),
        magnitude=float(row["magnitude"]),
        magnitude_type=str(row["magnitude_type"]),
        station_id=station_id,
        channel=cha,
        waveform_file=rel,
        sampling_rate_hz=df,
        trace_duration_s=n / df,
        peak_amplitude_counts=peak,
        rms_amplitude_counts=rms_full,
        rms_signal_window_counts=rms_signal,
        noise_rms_counts=noise_rms,
        noise_window_start_s=i0 / df,
        noise_window_end_s=i1 / df,
        noise_window_note=noise_note,
        snr_peak=snr_peak,
        snr_rms=snr_rms,
        signal_duration_s=sig_dur,
        sta_lta_threshold=STA_LTA_THRESHOLD,
        sta_window_s=STA_WINDOW_S,
        lta_window_s=LTA_WINDOW_S,
        p_pick_time_s=p_time_s,
        p_pick_sample=p_sample,
        p_pick_sta_lta_value=p_cft_val,
        p_pick_method=pick_method,
    )


def plot_event(row: pd.Series, metrics: WaveformMetrics, out_path: Path) -> None:
    path = RAW_IRIS / metrics.waveform_file
    tr = read(str(path))[0]
    data = tr.data.astype(float)
    df = float(tr.stats.sampling_rate)
    times = np.arange(len(data)) / df
    nsta = max(int(STA_WINDOW_S * df), 1)
    nlta = max(int(LTA_WINDOW_S * df), nsta + 1)
    cft = classic_sta_lta(data, nsta, nlta)
    peak = metrics.peak_amplitude_counts
    normalized = data / peak if peak > 0 else data
    p_t = metrics.p_pick_time_s
    short_id = _short_event_id(metrics.event_id)

    fig, axes = plt.subplots(4, 1, figsize=(9, 9), sharex=True)
    fig.suptitle(
        f"{metrics.station_id} · M {metrics.magnitude:.2f} ({metrics.magnitude_type}) · {short_id}",
        fontsize=12,
        y=0.995,
    )

    ax0 = axes[0]
    ax0.plot(times, data, color="#1f4e79", linewidth=0.55)
    ax0.axvline(p_t, color="#c62828", linestyle="--", linewidth=1.2, label=f"P pick ≈ {p_t:.2f} s")
    ax0.set_ylabel("Counts")
    ax0.set_title("Raw waveform")
    ax0.legend(loc="upper right", fontsize=8)

    ax1 = axes[1]
    ax1.plot(times, normalized, color="#2e7d32", linewidth=0.55)
    ax1.axvline(p_t, color="#c62828", linestyle="--", linewidth=1.2)
    ax1.set_ylabel("Normalized")
    ax1.set_title("Amplitude normalized by peak")

    ax2 = axes[2]
    ax2.plot(times, cft, color="#5c6bc0", linewidth=0.7)
    ax2.axhline(STA_LTA_THRESHOLD, color="#888888", linestyle=":", linewidth=1, label=f"Threshold {STA_LTA_THRESHOLD}")
    ax2.axvline(p_t, color="#c62828", linestyle="--", linewidth=1.2)
    ax2.set_ylabel("STA/LTA")
    ax2.set_title("STA/LTA characteristic function (ObsPy classic_sta_lta)")
    ax2.legend(loc="upper right", fontsize=8)

    ax3 = axes[3]
    ax3.plot(times, data, color="#1f4e79", linewidth=0.55, alpha=0.85)
    ax3.axvline(p_t, color="#c62828", linewidth=2, label="Estimated P onset")
    ax3.scatter([p_t], [data[metrics.p_pick_sample]], color="#c62828", s=40, zorder=5)
    ax3.set_xlabel("Time since trace start (s)")
    ax3.set_ylabel("Counts")
    ax3.set_title("Raw waveform with P-wave arrival marker")
    ax3.legend(loc="upper right", fontsize=8)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def aggregate_summary(metrics_list: list[WaveformMetrics]) -> dict[str, Any]:
    df = pd.DataFrame([asdict(m) for m in metrics_list])
    by_station = df.groupby("station_id").agg(
        n_events=("event_id", "count"),
        mean_snr_peak=("snr_peak", "mean"),
        mean_p_pick_s=("p_pick_time_s", "mean"),
        mean_peak=("peak_amplitude_counts", "mean"),
    )
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "n_waveforms": len(metrics_list),
        "sta_lta": {
            "threshold": STA_LTA_THRESHOLD,
            "sta_window_s": STA_WINDOW_S,
            "lta_window_s": LTA_WINDOW_S,
        },
        "magnitude": {
            "min": float(df["magnitude"].min()),
            "max": float(df["magnitude"].max()),
        },
        "peak_amplitude_counts": {
            "min": float(df["peak_amplitude_counts"].min()),
            "max": float(df["peak_amplitude_counts"].max()),
            "mean": float(df["peak_amplitude_counts"].mean()),
        },
        "snr_peak": {
            "min": float(df["snr_peak"].min()),
            "max": float(df["snr_peak"].max()),
            "mean": float(df["snr_peak"].mean()),
            "median": float(df["snr_peak"].median()),
        },
        "p_pick_time_s": {
            "min": float(df["p_pick_time_s"].min()),
            "max": float(df["p_pick_time_s"].max()),
            "mean": float(df["p_pick_time_s"].mean()),
        },
        "signal_duration_s": {
            "min": float(df["signal_duration_s"].min()),
            "max": float(df["signal_duration_s"].max()),
            "mean": float(df["signal_duration_s"].mean()),
        },
        "by_station": by_station.reset_index().to_dict(orient="records"),
    }


def main() -> None:
    _apply_plot_style()
    for d in (OUT_SIGNAL, OUT_FIGURES, OUT_TABLES):
        d.mkdir(parents=True, exist_ok=True)

    manifest = pd.read_csv(MANIFEST_PATH)
    manifest["origin_time_utc"] = pd.to_datetime(manifest["origin_time_utc"], utc=True)

    metrics_list: list[WaveformMetrics] = []
    figure_paths: list[str] = []

    for _, row in manifest.iterrows():
        m = analyze_trace(row)
        metrics_list.append(m)
        short_id = _short_event_id(m.event_id)
        per_event_json = OUT_SIGNAL / f"{short_id}_metrics.json"
        with per_event_json.open("w", encoding="utf-8") as fh:
            json.dump(asdict(m), fh, indent=2)
        fig_name = f"signal_analysis_{short_id}.png"
        plot_event(row, m, OUT_FIGURES / fig_name)
        figure_paths.append(fig_name)

    summary_df = pd.DataFrame([asdict(m) for m in metrics_list])
    summary_df.to_csv(OUT_TABLES / "signal_analysis_per_event.csv", index=False)

    agg = aggregate_summary(metrics_list)
    with (OUT_SIGNAL / "signal_analysis_summary.json").open("w", encoding="utf-8") as fh:
        json.dump(agg, fh, indent=2)

    run_meta = {
        "summary": agg,
        "figures": figure_paths,
        "tables": ["signal_analysis_per_event.csv"],
        "per_event_metrics_dir": str(OUT_SIGNAL),
    }
    with (OUT_SIGNAL / "run_metadata.json").open("w", encoding="utf-8") as fh:
        json.dump(run_meta, fh, indent=2)

    print(json.dumps(agg, indent=2))


if __name__ == "__main__":
    main()
