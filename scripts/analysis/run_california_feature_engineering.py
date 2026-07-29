#!/usr/bin/env python3
"""Phase B.2 feature engineering for the California IRIS pilot.

Reads Phase B.1 outputs (``reports/preprocessing/*_stages.npz``) and optional
Phase A.2 P picks (``reports/signal_analysis/*_metrics.json``). Standalone workflow.
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
from obspy.signal.trigger import classic_sta_lta, trigger_onset

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "data" / "manifests" / "iris_california_pilot_events.csv"
PREP_DIR = REPO_ROOT / "reports" / "preprocessing"
SIGNAL_DIR = REPO_ROOT / "reports" / "signal_analysis"
OUT_FEATURES = REPO_ROOT / "reports" / "features"
OUT_FIGURES = REPO_ROOT / "reports" / "figures"
OUT_TABLES = REPO_ROOT / "reports" / "tables"

NOISE_WINDOW_S = 5.0
SIGNAL_DURATION_SIGMA = 3.0
STA_LTA_THRESHOLD = 2.5
STA_WINDOW_S = 0.5
LTA_WINDOW_S = 10.0

TIME_DOMAIN_FEATURES = [
    "peak_amplitude",
    "peak_to_peak_amplitude",
    "rms",
    "variance",
    "std",
    "zero_crossing_rate_hz",
    "signal_energy",
    "signal_entropy",
    "crest_factor",
]
FREQ_DOMAIN_FEATURES = [
    "dominant_frequency_hz",
    "spectral_centroid_hz",
    "spectral_bandwidth_hz",
    "spectral_rolloff_95_hz",
    "spectral_entropy",
]
EQ_FEATURES = [
    "p_arrival_time_s",
    "signal_duration_s",
    "pgm_proxy_counts",
    "arias_intensity_counts2_s_proxy",
]

FEATURE_COLUMNS = TIME_DOMAIN_FEATURES + FREQ_DOMAIN_FEATURES + EQ_FEATURES


def _apply_plot_style() -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "font.family": "DejaVu Sans",
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
        }
    )


def _short_event_id(event_id: str) -> str:
    match = re.search(r"eventid_([^_]+)_format", event_id)
    return match.group(1) if match else event_id[-24:]


def _shannon_entropy(p: np.ndarray) -> float:
    p = p.astype(float)
    p = p[p > 0]
    if p.size == 0:
        return float("nan")
    p = p / p.sum()
    return float(-np.sum(p * np.log2(p)))


def _signal_entropy(x: np.ndarray, bins: int = 64) -> float:
    hist, _ = np.histogram(x.astype(float), bins=bins, density=True)
    return _shannon_entropy(hist)


def _zero_crossing_rate_hz(x: np.ndarray, fs: float) -> float:
    signs = np.signbit(x.astype(float))
    crossings = np.sum(signs[1:] != signs[:-1])
    duration = len(x) / fs
    return float(crossings / duration) if duration > 0 else 0.0


def _spectral_features(x: np.ndarray, fs: float) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    n = len(x)
    spec = np.fft.rfft(x.astype(float))
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    power = (np.abs(spec) ** 2).astype(float)
    if power.sum() <= 0:
        nan = {k: float("nan") for k in FREQ_DOMAIN_FEATURES}
        return freqs, power, nan
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
    return freqs, power, {
        "dominant_frequency_hz": dominant,
        "spectral_centroid_hz": centroid,
        "spectral_bandwidth_hz": bandwidth,
        "spectral_rolloff_95_hz": rolloff,
        "spectral_entropy": spec_entropy,
    }


def _load_p_pick(short_id: str) -> tuple[float, str]:
    path = SIGNAL_DIR / f"{short_id}_metrics.json"
    if path.is_file():
        data = json.loads(path.read_text(encoding="utf-8"))
        return float(data["p_pick_time_s"]), "phase_a2_metrics"
    return float("nan"), "missing"


def _fallback_p_pick(x: np.ndarray, fs: float) -> tuple[float, str]:
    nsta = max(int(STA_WINDOW_S * fs), 1)
    nlta = max(int(LTA_WINDOW_S * fs), nsta + 1)
    cft = classic_sta_lta(x.astype(float), nsta, nlta)
    onsets = trigger_onset(cft, STA_LTA_THRESHOLD, 0.5)
    if len(onsets) > 0:
        return float(onsets[0, 0] / fs), "sta_lta_fallback"
    idx = np.where(cft[nlta:] >= STA_LTA_THRESHOLD)[0]
    if len(idx) == 0:
        return float(nlta / fs), "sta_lta_default"
    return float((idx[0] + nlta) / fs), "sta_lta_fallback"


def _noise_rms(x: np.ndarray, fs: float) -> float:
    n = min(int(NOISE_WINDOW_S * fs), len(x))
    seg = x[: max(n, 1)].astype(float)
    return float(np.sqrt(np.mean(seg**2)))


def _signal_duration(x: np.ndarray, fs: float, p_sample: int, noise_rms: float) -> float:
    if p_sample >= len(x) - 1:
        return 0.0
    thr = SIGNAL_DURATION_SIGMA * max(noise_rms, 1e-12)
    post = np.abs(x[p_sample:].astype(float))
    above = post >= thr
    if not np.any(above):
        return 0.0
    return float((int(np.max(np.where(above)[0])) + 1) / fs)


@dataclass
class EventFeatures:
    event_id: str
    short_id: str
    station_id: str
    magnitude: float
    magnitude_type: str
    sampling_rate_hz: float
    p_pick_source: str
    feature_vector: dict[str, float]


def extract_event(row: pd.Series) -> tuple[EventFeatures, np.ndarray, np.ndarray]:
    short_id = _short_event_id(str(row["event_id"]))
    npz_path = PREP_DIR / f"{short_id}_stages.npz"
    if not npz_path.is_file():
        raise FileNotFoundError(f"Missing preprocessing archive: {npz_path}")

    data = np.load(npz_path)
    times = data["times"].astype(float)
    filtered = data["filtered"].astype(float)
    fs = float(1.0 / (times[1] - times[0])) if len(times) > 1 else 40.0

    prep_meta_path = PREP_DIR / f"{short_id}_metrics.json"
    station_id = ""
    if prep_meta_path.is_file():
        meta = json.loads(prep_meta_path.read_text(encoding="utf-8"))
        station_id = meta.get("station_id", "")

    x = filtered
    peak = float(np.max(np.abs(x)))
    rms = float(np.sqrt(np.mean(x**2)))
    p_time, p_source = _load_p_pick(short_id)
    if math.isnan(p_time):
        p_time, p_source = _fallback_p_pick(x, fs)
    p_sample = int(p_time * fs)
    noise = _noise_rms(x, fs)

    _, _, freq_feats = _spectral_features(x, fs)

    feats: dict[str, float] = {
        "peak_amplitude": peak,
        "peak_to_peak_amplitude": float(np.ptp(x)),
        "rms": rms,
        "variance": float(np.var(x)),
        "std": float(np.std(x)),
        "zero_crossing_rate_hz": _zero_crossing_rate_hz(x, fs),
        "signal_energy": float(np.sum(x**2) / fs),
        "signal_entropy": _signal_entropy(x),
        "crest_factor": peak / max(rms, 1e-12),
        **freq_feats,
        "p_arrival_time_s": p_time,
        "signal_duration_s": _signal_duration(x, fs, p_sample, noise),
        "pgm_proxy_counts": peak,
        "arias_intensity_counts2_s_proxy": float(np.sum(x.astype(float) ** 2) / fs),
    }

    ef = EventFeatures(
        event_id=str(row["event_id"]),
        short_id=short_id,
        station_id=station_id,
        magnitude=float(row["magnitude"]),
        magnitude_type=str(row["magnitude_type"]),
        sampling_rate_hz=fs,
        p_pick_source=p_source,
        feature_vector=feats,
    )
    freqs, power, _ = _spectral_features(x, fs)
    return ef, freqs, power


def plot_fft_grid(spectra: list[tuple[str, np.ndarray, np.ndarray]], out: Path) -> None:
    n = len(spectra)
    cols = 2
    rows = int(math.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(10, 2.5 * rows), squeeze=False)
    for idx, (title, freqs, power) in enumerate(spectra):
        r, c = divmod(idx, cols)
        ax = axes[r][c]
        ax.semilogy(freqs[1:], power[1:] + 1e-12, color="#1f4e79", linewidth=0.7)
        ax.set_title(title, fontsize=9)
        ax.set_xlim(0, 20)
        ax.set_xlabel("Hz")
        ax.set_ylabel("Power")
    for idx in range(n, rows * cols):
        r, c = divmod(idx, cols)
        axes[r][c].axis("off")
    fig.suptitle("FFT magnitude power (filtered traces)", fontsize=12)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def plot_correlation_heatmap(df: pd.DataFrame, out: Path) -> None:
    corr = df[FEATURE_COLUMNS].astype(float).corr()
    fig, ax = plt.subplots(figsize=(11, 9))
    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    labels = [c.replace("_", "\n") for c in FEATURE_COLUMNS]
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=90, fontsize=7)
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_title("Feature correlation (8-event pilot)")
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    corr.to_csv(OUT_TABLES / "feature_correlation_matrix.csv")


def plot_distributions(df: pd.DataFrame, out: Path) -> None:
    cols = 6
    rows = int(math.ceil(len(FEATURE_COLUMNS) / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(14, 2.2 * rows))
    axes_flat = np.array(axes).flatten()
    for i, col in enumerate(FEATURE_COLUMNS):
        ax = axes_flat[i]
        vals = df[col].astype(float).values
        ax.hist(vals, bins=min(8, max(3, len(vals))), color="#5c6bc0", edgecolor="white")
        ax.set_title(col, fontsize=8)
    for j in range(len(FEATURE_COLUMNS), len(axes_flat)):
        axes_flat[j].axis("off")
    fig.suptitle("Feature value distributions (N=8 events)", fontsize=12)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def plot_boxplots_by_station(df: pd.DataFrame, out: Path) -> None:
    key_feats = ["rms", "crest_factor", "dominant_frequency_hz", "spectral_centroid_hz", "pgm_proxy_counts"]
    fig, axes = plt.subplots(1, len(key_feats), figsize=(12, 3.5))
    stations = sorted(df["station_id"].unique())
    for ax, col in zip(axes, key_feats):
        groups = [df.loc[df["station_id"] == st, col].astype(float).values for st in stations]
        ax.boxplot(groups, tick_labels=[s.split(".")[1] if "." in s else s for s in stations])
        ax.set_title(col, fontsize=9)
        ax.set_xlabel("Station")
    fig.suptitle("Feature boxplots by station (small-N pilot)", fontsize=11)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def main() -> None:
    _apply_plot_style()
    for d in (OUT_FEATURES, OUT_FIGURES, OUT_TABLES):
        d.mkdir(parents=True, exist_ok=True)

    manifest = pd.read_csv(MANIFEST_PATH)
    events: list[EventFeatures] = []
    spectra: list[tuple[str, np.ndarray, np.ndarray]] = []

    rows: list[dict[str, Any]] = []
    for _, row in manifest.iterrows():
        ef, freqs, power = extract_event(row)
        events.append(ef)
        spectra.append((f"{ef.short_id} M{ef.magnitude:.1f}", freqs, power))
        record = {
            "event_id": ef.event_id,
            "short_id": ef.short_id,
            "station_id": ef.station_id,
            "magnitude": ef.magnitude,
            "magnitude_type": ef.magnitude_type,
            "sampling_rate_hz": ef.sampling_rate_hz,
            "p_pick_source": ef.p_pick_source,
            **ef.feature_vector,
        }
        rows.append(record)

    df = pd.DataFrame(rows)
    df.to_csv(OUT_FEATURES / "feature_matrix.csv", index=False)
    df.to_csv(OUT_TABLES / "feature_matrix.csv", index=False)

    numeric = df[FEATURE_COLUMNS].astype(float)
    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "n_events": len(df),
        "n_features": len(FEATURE_COLUMNS),
        "feature_names": FEATURE_COLUMNS,
        "matrix_shape": {"rows": int(len(df)), "feature_columns": len(FEATURE_COLUMNS)},
        "data_source": "reports/preprocessing/*_stages.npz (filtered trace)",
        "units_note": "Counts-based; no instrument response correction in B.1",
        "p_pick_sources": df["p_pick_source"].value_counts().to_dict(),
        "feature_means": numeric.mean().to_dict(),
        "feature_stds": numeric.std(ddof=0).to_dict(),
    }
    with (OUT_FEATURES / "feature_summary.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    per_event = {e.short_id: e.feature_vector for e in events}
    with (OUT_FEATURES / "per_event_features.json").open("w", encoding="utf-8") as fh:
        json.dump(per_event, fh, indent=2)

    plot_fft_grid(spectra, OUT_FIGURES / "feature_engineering_fft_spectra.png")
    plot_correlation_heatmap(df, OUT_FIGURES / "feature_correlation_heatmap.png")
    plot_distributions(df, OUT_FIGURES / "feature_distributions.png")
    plot_boxplots_by_station(df, OUT_FIGURES / "feature_boxplots_by_station.png")

    with (OUT_FEATURES / "run_metadata.json").open("w", encoding="utf-8") as fh:
        json.dump(
            {
                "summary": summary,
                "figures": [
                    "feature_engineering_fft_spectra.png",
                    "feature_correlation_heatmap.png",
                    "feature_distributions.png",
                    "feature_boxplots_by_station.png",
                ],
                "tables": ["feature_matrix.csv", "feature_correlation_matrix.csv"],
            },
            fh,
            indent=2,
        )

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
