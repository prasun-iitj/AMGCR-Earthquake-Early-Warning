#!/usr/bin/env python3
"""
Export downsampled waveform stage arrays from v1.0 NPZ archives for static web preview.

Read-only against reports/preprocessing/*_stages.npz and signal_analysis/*_metrics.json.
Output: website/public/waveforms/{short_id}.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

MAX_POINTS = 1200


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def website_root() -> Path:
    return Path(__file__).resolve().parents[1]


def downsample(values: np.ndarray, target: int) -> list[float]:
    if values.size <= target:
        return values.astype(float).tolist()
    indices = np.linspace(0, values.size - 1, target, dtype=int)
    return values[indices].astype(float).tolist()


def load_signal_metrics(metrics_path: Path) -> dict:
    if not metrics_path.exists():
        return {}
    return json.loads(metrics_path.read_text(encoding="utf-8"))


def export_waveform(short_id: str, repo: Path, output_dir: Path) -> bool:
    npz_path = repo / "reports/preprocessing" / f"{short_id}_stages.npz"
    signal_metrics_path = repo / "reports/signal_analysis" / f"{short_id}_metrics.json"
    preprocessing_metrics_path = (
        repo / "reports/preprocessing" / f"{short_id}_metrics.json"
    )

    if not npz_path.exists():
        return False

    data = np.load(npz_path)
    signal_metrics = load_signal_metrics(signal_metrics_path)
    preprocessing_metrics = load_signal_metrics(preprocessing_metrics_path)

    stages = ["times", "raw", "detrended", "filtered", "normalized"]
    payload = {
        "short_id": short_id,
        "event_id": signal_metrics.get("event_id"),
        "dataset_id": "california-pilot",
        "sampling_rate_hz": float(signal_metrics.get("sampling_rate_hz", 40.0)),
        "original_sample_count": int(data["times"].shape[0]),
        "downsampled_point_count": min(MAX_POINTS, int(data["times"].shape[0])),
        "p_pick_time_s": signal_metrics.get("p_pick_time_s"),
        "snr_peak": signal_metrics.get("snr_peak"),
        "series": {
            stage: downsample(data[stage], MAX_POINTS) for stage in stages
        },
        "signal_metrics": signal_metrics,
        "preprocessing_metrics": preprocessing_metrics,
    }

    output_path = output_dir / f"{short_id}.json"
    output_path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    return True


def main() -> int:
    repo = repo_root()
    output_dir = website_root() / "public" / "waveforms"
    output_dir.mkdir(parents=True, exist_ok=True)

    npz_dir = repo / "reports/preprocessing"
    if not npz_dir.exists():
        print("[export-waveforms] No preprocessing NPZ directory found; skipping.")
        return 0

    exported = 0
    for npz_path in sorted(npz_dir.glob("*_stages.npz")):
        short_id = npz_path.name.replace("_stages.npz", "")
        if export_waveform(short_id, repo, output_dir):
            exported += 1

    print(f"[export-waveforms] Exported {exported} waveform JSON files to public/waveforms/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
