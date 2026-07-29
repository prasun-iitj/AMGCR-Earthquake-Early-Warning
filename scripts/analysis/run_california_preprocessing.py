#!/usr/bin/env python3
"""Phase B.1 waveform preprocessing for the California IRIS pilot.

Standalone research workflow (not EarthESND ``src/``). Reads manifest-linked
MiniSEED, applies demean/detrend/taper/band-pass, optional response removal,
peak normalization, and writes reports plus comparison figures.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from obspy import read, Trace
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import FDSNException

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_IRIS = REPO_ROOT / "data" / "raw" / "iris"
MANIFEST_PATH = REPO_ROOT / "data" / "manifests" / "iris_california_pilot_events.csv"
OUT_PREP = REPO_ROOT / "reports" / "preprocessing"
OUT_FIGURES = REPO_ROOT / "reports" / "figures"
OUT_TABLES = REPO_ROOT / "reports" / "tables"

# Documented in PREPROCESSING_REPORT.md and preprocessing_config.json
TAPER_MAX_PERCENTAGE = 0.05
TAPER_TYPE = "hann"
BANDPASS_FREQMIN_HZ = 0.1
BANDPASS_FREQMAX_HZ = 15.0
BANDPASS_CORNERS = 4
BANDPASS_ZEROPHASE = True
RESPONSE_OUTPUT = "VEL"
RESPONSE_WATER_LEVEL = 60.0
NOISE_WINDOW_S = 5.0
NORMALIZATION = "peak_abs"

FDSN_WAVEFORM_CLIENT = "EARTHSCOPE"


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


def _times(tr: Trace) -> np.ndarray:
    return np.arange(tr.stats.npts) / float(tr.stats.sampling_rate)


def _noise_rms(data: np.ndarray, df: float) -> float:
    n = min(int(NOISE_WINDOW_S * df), len(data))
    n = max(n, 1)
    seg = data[:n].astype(float)
    return float(np.sqrt(np.mean(seg**2)))


def _trace_stats(data: np.ndarray) -> dict[str, float]:
    x = data.astype(float)
    return {
        "mean": float(np.mean(x)),
        "std": float(np.std(x)),
        "peak_amplitude": float(np.max(np.abs(x))),
        "rms": float(np.sqrt(np.mean(x**2))),
    }


def _snr_peak(data: np.ndarray, df: float) -> float:
    noise = _noise_rms(data, df)
    peak = float(np.max(np.abs(data.astype(float))))
    return peak / max(noise, 1e-12)


def _try_attach_response(tr: Trace) -> tuple[Trace, str, str]:
    """Return trace with response removed to velocity, or original with reason."""
    work = deepcopy(tr)
    net = work.stats.network
    sta = work.stats.station
    loc = work.stats.location or ""
    cha = work.stats.channel
    try:
        client = Client(FDSN_WAVEFORM_CLIENT)
        inv = client.get_stations(
            network=net,
            station=sta,
            location=loc,
            channel=cha,
            starttime=work.stats.starttime,
            endtime=work.stats.endtime,
            level="response",
        )
        work.attach_response(inventory=inv)
        work.remove_response(
            output=RESPONSE_OUTPUT,
            water_level=RESPONSE_WATER_LEVEL,
            zero_mean=False,
            taper=False,
            pre_filt=(0.08, 0.1, 20.0, 25.0),
        )
        units = f"{RESPONSE_OUTPUT} (FDSN response removed)"
        return work, "applied", units
    except (FDSNException, Exception) as exc:  # noqa: BLE001 — report failure reason
        return deepcopy(tr), "skipped", f"skipped: {type(exc).__name__}"


@dataclass
class PreprocessResult:
    event_id: str
    short_id: str
    origin_time_utc: str
    magnitude: float
    magnitude_type: str
    station_id: str
    waveform_file: str
    sampling_rate_hz: float
    response_status: str
    response_detail: str
    amplitude_units_final: str
    raw_mean: float
    raw_std: float
    raw_peak: float
    raw_rms: float
    raw_snr_peak: float
    filtered_mean: float
    filtered_std: float
    filtered_peak: float
    filtered_rms: float
    filtered_snr_peak: float
    snr_peak_change_ratio: float
    final_mean: float
    final_std: float
    final_peak: float
    final_rms: float


def preprocess_trace(tr: Trace) -> tuple[dict[str, Trace], PreprocessResult | None, dict[str, Any]]:
    """Build pipeline stages and metrics; ``PreprocessResult`` filled by caller with metadata."""
    raw = deepcopy(tr)
    stages: dict[str, Trace] = {"raw": raw}

    det = deepcopy(raw)
    det.detrend(type="demean")
    det.detrend(type="linear")
    stages["detrended"] = det

    filt_path = deepcopy(det)
    filt_path.taper(max_percentage=TAPER_MAX_PERCENTAGE, type=TAPER_TYPE)

    response_tr, response_status, response_detail = _try_attach_response(deepcopy(filt_path))
    if response_status == "applied":
        filt_path = response_tr
        amp_units = response_detail
    else:
        amp_units = "counts (response not applied)"

    nyquist = 0.5 * float(filt_path.stats.sampling_rate)
    fmax = min(BANDPASS_FREQMAX_HZ, nyquist * 0.9)
    filt_path.filter(
        "bandpass",
        freqmin=BANDPASS_FREQMIN_HZ,
        freqmax=fmax,
        corners=BANDPASS_CORNERS,
        zerophase=BANDPASS_ZEROPHASE,
    )
    stages["filtered"] = deepcopy(filt_path)

    norm = deepcopy(filt_path)
    peak = float(np.max(np.abs(norm.data.astype(float))))
    if peak > 0 and NORMALIZATION == "peak_abs":
        norm.data = (norm.data / peak).astype(norm.data.dtype)
    stages["normalized"] = norm

    df = float(raw.stats.sampling_rate)
    raw_m = _trace_stats(raw.data)
    raw_snr = _snr_peak(raw.data, df)
    filtered_snr = _snr_peak(filt_path.data, df)
    filtered_m = _trace_stats(filt_path.data)
    fin_m = _trace_stats(norm.data)

    meta = {
        "response_status": response_status,
        "response_detail": response_detail,
        "amplitude_units_final": amp_units,
        "bandpass_freqmax_used_hz": fmax,
        "raw_metrics": raw_m,
        "filtered_metrics": filtered_m,
        "final_metrics": fin_m,
        "raw_snr_peak": raw_snr,
        "filtered_snr_peak": filtered_snr,
    }
    return stages, None, meta


def plot_comparison(stages: dict[str, Trace], title: str, ylabels: dict[str, str], out: Path) -> None:
    fig, axes = plt.subplots(4, 1, figsize=(9, 9), sharex=True)
    fig.suptitle(title, fontsize=12)
    order = ["raw", "detrended", "filtered", "normalized"]
    titles = ["Raw waveform", "Detrended (demean + linear)", "Filtered", "Normalized (peak = 1)"]
    colors = ["#1f4e79", "#2e7d32", "#5c6bc0", "#c62828"]
    for ax, key, stitle, color in zip(axes, order, titles, colors):
        tr = stages[key]
        ax.plot(_times(tr), tr.data, color=color, linewidth=0.55)
        ax.set_ylabel(ylabels.get(key, "Amplitude"))
        ax.set_title(stitle)
    axes[-1].set_xlabel("Time since trace start (s)")
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def build_config() -> dict[str, Any]:
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "pipeline_order": [
            "demean",
            "linear_detrend",
            "taper",
            "instrument_response_optional",
            "bandpass",
            "peak_normalization",
        ],
        "taper": {"max_percentage": TAPER_MAX_PERCENTAGE, "type": TAPER_TYPE},
        "bandpass": {
            "freqmin_hz": BANDPASS_FREQMIN_HZ,
            "freqmax_hz_nominal": BANDPASS_FREQMAX_HZ,
            "corners": BANDPASS_CORNERS,
            "zerophase": BANDPASS_ZEROPHASE,
            "note": "freqmax capped below Nyquist per trace",
        },
        "instrument_response": {
            "fdsn_client": FDSN_WAVEFORM_CLIENT,
            "level": "response",
            "output": RESPONSE_OUTPUT,
            "water_level": RESPONSE_WATER_LEVEL,
            "pre_filt_hz": [0.08, 0.1, 20.0, 25.0],
        },
        "normalization": NORMALIZATION,
        "snr_noise_window_s": NOISE_WINDOW_S,
    }


def main() -> None:
    _apply_plot_style()
    for d in (OUT_PREP, OUT_FIGURES, OUT_TABLES):
        d.mkdir(parents=True, exist_ok=True)

    config = build_config()
    with (OUT_PREP / "preprocessing_config.json").open("w", encoding="utf-8") as fh:
        json.dump(config, fh, indent=2)

    manifest = pd.read_csv(MANIFEST_PATH)
    manifest["origin_time_utc"] = pd.to_datetime(manifest["origin_time_utc"], utc=True)

    results: list[PreprocessResult] = []
    response_counts: dict[str, int] = {"applied": 0, "skipped": 0}

    for _, row in manifest.iterrows():
        rel = str(row["waveform_files"]).replace("\\", "/")
        path = RAW_IRIS / rel
        tr = read(str(path))[0]
        short_id = _short_event_id(str(row["event_id"]))
        net = tr.stats.network
        sta = tr.stats.station
        loc = tr.stats.location or "--"
        station_id = f"{net}.{sta}.{loc}.{tr.stats.channel}"

        stages, _, meta = preprocess_trace(tr)
        response_counts[meta["response_status"]] = response_counts.get(meta["response_status"], 0) + 1

        ylabels = {
            "raw": "Counts",
            "detrended": "Counts",
            "filtered": meta["amplitude_units_final"][:20],
            "normalized": "Norm.",
        }
        fig_name = f"preprocessing_{short_id}.png"
        plot_comparison(
            stages,
            f"{station_id} · M {row['magnitude']:.2f} · preprocessing",
            ylabels,
            OUT_FIGURES / fig_name,
        )

        npz_path = OUT_PREP / f"{short_id}_stages.npz"
        np.savez(
            npz_path,
            times=_times(tr),
            raw=stages["raw"].data,
            detrended=stages["detrended"].data,
            filtered=stages["filtered"].data,
            normalized=stages["normalized"].data,
        )

        pr = PreprocessResult(
            event_id=str(row["event_id"]),
            short_id=short_id,
            origin_time_utc=pd.Timestamp(row["origin_time_utc"]).isoformat(),
            magnitude=float(row["magnitude"]),
            magnitude_type=str(row["magnitude_type"]),
            station_id=station_id,
            waveform_file=rel,
            sampling_rate_hz=float(tr.stats.sampling_rate),
            response_status=meta["response_status"],
            response_detail=meta["response_detail"],
            amplitude_units_final=meta["amplitude_units_final"],
            raw_mean=meta["raw_metrics"]["mean"],
            raw_std=meta["raw_metrics"]["std"],
            raw_peak=meta["raw_metrics"]["peak_amplitude"],
            raw_rms=meta["raw_metrics"]["rms"],
            raw_snr_peak=meta["raw_snr_peak"],
            filtered_mean=meta["filtered_metrics"]["mean"],
            filtered_std=meta["filtered_metrics"]["std"],
            filtered_peak=meta["filtered_metrics"]["peak_amplitude"],
            filtered_rms=meta["filtered_metrics"]["rms"],
            filtered_snr_peak=meta["filtered_snr_peak"],
            snr_peak_change_ratio=meta["filtered_snr_peak"] / max(meta["raw_snr_peak"], 1e-12),
            final_mean=meta["final_metrics"]["mean"],
            final_std=meta["final_metrics"]["std"],
            final_peak=meta["final_metrics"]["peak_amplitude"],
            final_rms=meta["final_metrics"]["rms"],
        )
        results.append(pr)
        with (OUT_PREP / f"{short_id}_metrics.json").open("w", encoding="utf-8") as fh:
            json.dump({**asdict(pr), "bandpass_freqmax_hz": meta["bandpass_freqmax_used_hz"]}, fh, indent=2)

    df = pd.DataFrame([asdict(r) for r in results])
    df.to_csv(OUT_TABLES / "preprocessing_quality_metrics.csv", index=False)

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "n_waveforms": len(results),
        "config_path": str(OUT_PREP / "preprocessing_config.json"),
        "instrument_response": response_counts,
        "raw_snr_peak": {
            "min": float(df["raw_snr_peak"].min()),
            "max": float(df["raw_snr_peak"].max()),
            "mean": float(df["raw_snr_peak"].mean()),
        },
        "filtered_snr_peak": {
            "min": float(df["filtered_snr_peak"].min()),
            "max": float(df["filtered_snr_peak"].max()),
            "mean": float(df["filtered_snr_peak"].mean()),
        },
        "snr_peak_change_ratio": {
            "min": float(df["snr_peak_change_ratio"].min()),
            "max": float(df["snr_peak_change_ratio"].max()),
            "mean": float(df["snr_peak_change_ratio"].mean()),
        },
    }
    with (OUT_PREP / "preprocessing_summary.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
