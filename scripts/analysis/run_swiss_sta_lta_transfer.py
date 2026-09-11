#!/usr/bin/env python3
"""Swiss STA/LTA methods-transfer investigation.

Sensitivity analysis only. Does not modify California artefacts, Swiss raw
MiniSEED, or the official Swiss signal-analysis trigger pipeline.
Triggers are automatic STA/LTA onsets, not validated P arrivals.
"""

from __future__ import annotations

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

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.acquisition.switzerland_pilot import event_short_id
from src.analysis.switzerland_signal import (
    REQUIRED_HH_3C,
    common_overlap,
    edge_mute_seconds,
    has_complete_hh_3c,
    identify_hh_components,
    load_swiss_analysis_config,
    merge_stream_justified,
    peak_abs,
    pre_filt_for_sampling,
    rms,
    sampling_rates_consistent,
    slice_array_window,
    stationxml_path_for_row,
)
from src.analysis.switzerland_sta_lta_transfer import (
    apply_proposal_rule,
    cft_window_stats,
    finite_median,
    load_transfer_config,
    onset_times_from_samples,
    onsets_from_cft,
    sta_lta_characteristic_function,
    trigger_window_counts,
    unmasked_onset_is_in_mute_region,
    window_pair,
)

LOGGER = logging.getLogger("swiss_sta_lta_transfer")
DEFAULT_CONFIG = REPO_ROOT / "configs" / "swiss_sta_lta_transfer.yaml"


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


def _bandpass(stream: Stream, rate: float, bandpass_cfg: dict[str, Any], zerophase: bool) -> None:
    nyquist = 0.5 * rate
    fmax = min(float(bandpass_cfg["freqmax_hz"]), float(bandpass_cfg.get("nyquist_guard", 0.9)) * nyquist)
    stream.filter(
        "bandpass",
        freqmin=float(bandpass_cfg["freqmin_hz"]),
        freqmax=fmax,
        corners=int(bandpass_cfg["corners"]),
        zerophase=zerophase,
    )


def load_processed_record(row: pd.Series, analysis_cfg: dict[str, Any], repo_root: Path) -> dict[str, Any] | None:
    short_id = event_short_id(str(row["event_id"]))
    origin = UTCDateTime(str(row["origin_time_utc"]))
    waveform = repo_root / str(row["waveform_file"]).replace("\\", "/")
    xml_path = stationxml_path_for_row(
        repo_root,
        analysis_cfg["inputs"]["metadata_dir"],
        str(row["event_id"]),
        str(row["station"]),
        str(row.get("location", "--")),
    )
    if not waveform.exists():
        LOGGER.warning("missing_waveform %s %s", short_id, row["station"])
        return None
    stream = read(str(waveform))
    merged, _ = merge_stream_justified(stream)
    if not has_complete_hh_3c(merged) or not sampling_rates_consistent(merged):
        LOGGER.warning("skip_incomplete %s %s", short_id, row["station"])
        return None
    overlap = common_overlap(merged)
    if overlap is None:
        return None
    merged.trim(overlap[0], overlap[1], pad=False, nearest_sample=True)
    raw_3c = _align_npts(_component_traces(merged))
    rate = float(raw_3c["HHZ"].stats.sampling_rate)
    starttime = raw_3c["HHZ"].stats.starttime

    prep = Stream([raw_3c[ch].copy() for ch in REQUIRED_HH_3C])
    prep.detrend("demean")
    prep.detrend("linear")
    tapered = prep.copy()
    tapered.taper(max_percentage=0.05, type="hann")
    vel = tapered.copy()
    if xml_path.exists():
        inv = read_inventory(str(xml_path))
        pre_filt = pre_filt_for_sampling(rate, analysis_cfg["instrument_response"], analysis_cfg["bandpass"])
        vel.remove_response(
            inventory=inv,
            output=str(analysis_cfg["instrument_response"]["output"]),
            water_level=float(analysis_cfg["instrument_response"]["water_level"]),
            pre_filt=pre_filt,
            zero_mean=False,
            taper=False,
        )
    causal = vel.copy()
    zph = vel.copy()
    _bandpass(causal, rate, analysis_cfg["bandpass"], zerophase=False)
    _bandpass(zph, rate, analysis_cfg["bandpass"], zerophase=True)
    mute_s = edge_mute_seconds(len(raw_3c["HHZ"].data), rate, 0.05, 10.0, 0.0)
    variants = {
        "raw_counts": _align_npts(_component_traces(prep)),
        "response_vel": _align_npts(_component_traces(vel)),
        "causal_bandpass": _align_npts(_component_traces(causal)),
        "zerophase_bandpass": _align_npts(_component_traces(zph)),
    }
    return {
        "event_id": short_id,
        "station": str(row["station"]),
        "origin": origin,
        "starttime": starttime,
        "sampling_rate": rate,
        "mute_s": mute_s,
        "magnitude": float(row["magnitude"]),
        "magnitude_type": str(row["magnitude_type"]),
        "variants": variants,
    }


def _evaluate_onsets(
    pack: dict[str, Any],
    starttime: UTCDateTime,
    rate: float,
    origin: UTCDateTime,
    windows_cfg: dict[str, Any],
    mute_s: float,
) -> dict[str, Any]:
    samples = pack.get("onset_samples") or []
    times = onset_times_from_samples(starttime, rate, samples)
    counts = trigger_window_counts(times, origin, windows_cfg)
    counts["n_onsets_after_mute"] = len(samples)
    counts["unmasked_in_mute"] = unmasked_onset_is_in_mute_region(pack.get("sample_unmasked"), rate, mute_s)
    if pack.get("sample_unmasked") is not None:
        counts["unmasked_latency_s"] = float((starttime + pack["sample_unmasked"] / rate) - origin)
        counts["unmasked_from_trace_start_s"] = float(pack["sample_unmasked"] / rate)
    else:
        counts["unmasked_latency_s"] = float("nan")
        counts["unmasked_from_trace_start_s"] = float("nan")
    return counts


def aggregate_threshold_rows(record_rows: list[dict[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(record_rows)
    out = []
    keys = ["processing", "channel", "sta_window_s", "lta_window_s", "threshold"]
    for key, grp in df.groupby(keys, sort=False):
        rec = dict(zip(keys, key))
        n = len(grp)
        rec.update(
            {
                "n_records": n,
                "n_records_noise_onset": int(grp["has_noise_onset"].sum()),
                "n_records_pre_origin_onset": int(grp["has_pre_origin_onset"].sum()),
                "n_records_post_origin_onset": int(grp["has_post_origin_onset"].sum()),
                "n_records_no_search_trigger": int(grp["no_trigger_in_search"].sum()),
                "n_records_search_pre_origin": int(grp["search_is_pre_origin"].sum()),
                "n_records_search_post_origin": int(grp["search_is_post_origin"].sum()),
                "noise_record_fraction": float(grp["has_noise_onset"].mean()),
                "pre_origin_record_fraction": float(grp["has_pre_origin_onset"].mean()),
                "post_origin_coverage": float(grp["has_post_origin_onset"].mean()),
                "n_onsets_noise_total": int(grp["n_onsets_noise"].sum()),
                "n_onsets_pre_origin_total": int(grp["n_onsets_pre_origin"].sum()),
                "n_onsets_post_origin_total": int(grp["n_onsets_post_origin"].sum()),
                "median_search_latency_s": finite_median(grp["first_search_latency_s"]),
                "median_post_origin_latency_s": finite_median(grp["first_post_origin_latency_s"]),
            }
        )
        out.append(rec)
    return pd.DataFrame(out)


def make_figures(
    rec_df: pd.DataFrame,
    thresh_df: pd.DataFrame,
    window_df: pd.DataFrame,
    station_df: pd.DataFrame,
    component_df: pd.DataFrame,
    noise_df: pd.DataFrame,
    example_packs: dict[str, Any],
    transfer_cfg: dict[str, Any],
    fig_dir: Path,
) -> list[str]:
    fig_dir.mkdir(parents=True, exist_ok=True)
    dpi = int(transfer_cfg["figures"]["dpi"])
    written: list[str] = []
    base = thresh_df[
        (thresh_df["processing"] == "causal_bandpass")
        & (thresh_df["channel"] == "HHZ")
        & (thresh_df["sta_window_s"] == 0.5)
        & (thresh_df["lta_window_s"] == 10.0)
    ].sort_values("threshold")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(base["threshold"], 100 * base["noise_record_fraction"], "o-", color="#c62828", label="≥1 noise-window onset")
    ax.plot(base["threshold"], 100 * base["pre_origin_record_fraction"], "s--", color="#ef6c00", label="≥1 onset in [origin−5, origin)")
    ax.set_xlabel("STA/LTA threshold")
    ax.set_ylabel("Percent of records")
    ax.set_title("Threshold vs pre-event trigger-candidate rate (causal 0.1–15 Hz HHZ, 0.5/10 s)")
    ax.legend()
    path = fig_dir / "fig01_threshold_vs_preevent_rate.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(base["threshold"], 100 * base["post_origin_coverage"], "o-", color="#1565c0")
    ax.set_xlabel("STA/LTA threshold")
    ax.set_ylabel("Percent of records with ≥1 post-origin onset [0, 90] s")
    ax.set_title("Threshold vs post-origin trigger coverage (not a performance score)")
    path = fig_dir / "fig02_threshold_vs_post_origin_coverage.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(base["threshold"], base["median_post_origin_latency_s"], "o-", color="#6a1b9a", label="median first post-origin latency")
    ax.plot(base["threshold"], base["median_search_latency_s"], "s--", color="#00838f", label="median first search-window latency")
    ax.axhline(0.0, color="#333333", linestyle=":")
    ax.set_xlabel("STA/LTA threshold")
    ax.set_ylabel("Latency relative to origin (s)")
    ax.set_title("Threshold vs trigger latency (automatic onsets)")
    ax.legend()
    path = fig_dir / "fig03_threshold_vs_latency.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    order = station_df.sort_values("noise_onset_rate", ascending=False)
    ax.bar(np.arange(len(order)), 100 * order["noise_onset_rate"], color="#455a64")
    ax.set_xticks([])
    ax.set_ylabel("Percent of station records with ≥1 noise-window onset")
    ax.set_xlabel("CH stations (sorted)")
    ax.set_title("Station noise-window trigger-candidate rate at threshold 2.5 (causal HHZ)")
    path = fig_dir / "fig04_station_false_trigger_distribution.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(component_df["channel"], 100 * component_df["noise_record_fraction"], color=["#1f4e79", "#2e7d32", "#c62828"])
    ax.set_ylabel("Percent of records with ≥1 noise-window onset")
    ax.set_title("Component comparison at threshold 2.5 (causal 0.1–15 Hz, 0.5/10 s)")
    path = fig_dir / "fig05_component_comparison.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)

    mag = rec_df[(rec_df.processing == "causal_bandpass") & (rec_df.channel == "HHZ") & (rec_df.threshold == 2.5) & (rec_df.sta_window_s == 0.5) & (rec_df.lta_window_s == 10.0)]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = np.where(mag["has_post_origin_onset"], "#1565c0", "#c62828")
    ax.scatter(mag["magnitude"], mag["first_post_origin_latency_s"], c=colors, s=28, alpha=0.8)
    ax.axhline(0.0, color="#333333", linestyle=":")
    ax.set_xlabel("Catalogue magnitude (MLh/MLhc)")
    ax.set_ylabel("First post-origin onset latency (s)")
    ax.set_title("Magnitude vs first post-origin STA/LTA onset (blue=has post-origin onset)")
    path = fig_dir / "fig06_magnitude_vs_trigger.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(
        mag["epicentral_distance_km"],
        mag["n_onsets_noise"],
        c=np.log10(np.clip(mag["snr_peak_hhz"].to_numpy(dtype=float), 1e-6, None)),
        s=28,
        cmap="viridis",
        alpha=0.85,
    )
    cb = fig.colorbar(ax.collections[0], ax=ax)
    cb.set_label("log10 SNR peak HHZ")
    ax.set_xlabel("Epicentral distance (km)")
    ax.set_ylabel("Noise-window onset count (threshold 2.5)")
    ax.set_title("Distance vs noise-window STA/LTA onsets (not a detection model)")
    path = fig_dir / "fig07_distance_vs_trigger.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)

    def _plot_example(key: str, title: str, fname: str) -> None:
        pack = example_packs.get(key)
        if not pack:
            return
        t = (np.arange(len(pack["data"])) / pack["rate"]) + float(pack["starttime"] - pack["origin"])
        fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        fig.suptitle(title)
        axes[0].plot(t, pack["data"], color="#1f4e79", linewidth=0.5)
        axes[0].axvline(0.0, color="#333333", linestyle="--")
        axes[0].axvspan(-60, -10, color="#90caf9", alpha=0.3, label="noise")
        axes[0].axvspan(-5, 0, color="#ffe082", alpha=0.4, label="origin−5–0")
        axes[0].axvspan(0, 90, color="#ffcc80", alpha=0.25, label="origin–90")
        axes[0].set_ylabel(pack["ylabel"])
        axes[0].legend(loc="upper right", fontsize=8)
        tcft = t[: len(pack["cft"])]
        axes[1].plot(tcft, pack["cft"], color="#5c6bc0", linewidth=0.7)
        axes[1].axhline(2.5, color="#888888", linestyle=":", label="threshold 2.5")
        if math.isfinite(pack.get("mark_s", float("nan"))):
            axes[0].axvline(pack["mark_s"], color="#c62828", linestyle="--")
            axes[1].axvline(pack["mark_s"], color="#c62828", linestyle="--", label="onset")
        axes[1].set_xlim(-90, 120)
        axes[1].set_xlabel("Time relative to origin (s)")
        axes[1].set_ylabel("STA/LTA")
        axes[1].legend(loc="upper right", fontsize=8)
        fig.tight_layout()
        out = fig_dir / fname
        fig.savefig(out, dpi=dpi)
        plt.close(fig)
        written.append(out.name)

    _plot_example(
        "pre_event",
        "Representative pre-event STA/LTA (causal HHZ, 0.5/10, thr 2.5) — automatic onset, not a P pick",
        "fig08_representative_preevent_sta_lta.png",
    )
    _plot_example(
        "post_origin",
        "Representative post-origin STA/LTA (causal HHZ, 0.5/10, thr 2.5) — automatic onset, not a validated P",
        "fig09_representative_post_origin_sta_lta.png",
    )
    _plot_example(
        "edge",
        "Edge-effect diagnostic: CFT near trace start vs noise window (causal HHZ, thr 2.5)",
        "fig10_edge_effect_diagnostic.png",
    )

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(np.log10(np.clip(noise_df["noise_rms"].to_numpy(dtype=float), 1e-12, None)), bins=20, color="#1565c0", edgecolor="white")
    ax.set_xlabel("log10 noise RMS (causal 0.1–15 Hz HHZ, origin−60 to −10 s)")
    ax.set_ylabel("Records")
    ax.set_title("Pre-event noise RMS distribution")
    path = fig_dir / "fig11_noise_rms_distribution.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)

    proc = thresh_df[(thresh_df.channel == "HHZ") & (thresh_df.sta_window_s == 0.5) & (thresh_df.lta_window_s == 10.0) & (thresh_df.threshold == 2.5)]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(proc["processing"], 100 * proc["noise_record_fraction"], color="#6a1b9a")
    ax.set_ylabel("Percent of records with ≥1 noise-window onset")
    ax.set_title("Processing variant vs noise-window trigger rate (thr 2.5, 0.5/10 s, HHZ)")
    ax.tick_params(axis="x", rotation=20)
    path = fig_dir / "fig12_processing_variant_noise_rate.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    written.append(path.name)
    return written


def main() -> None:
    transfer_cfg = load_transfer_config(DEFAULT_CONFIG)
    analysis_cfg = load_swiss_analysis_config(REPO_ROOT / transfer_cfg["inputs"]["analysis_config"])
    out_dir = REPO_ROOT / transfer_cfg["output"]["reports_dir"]
    fig_dir = REPO_ROOT / transfer_cfg["output"]["figures_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    _setup_logging(REPO_ROOT / transfer_cfg["output"]["log_file"])
    _apply_plot_style()
    LOGGER.info("sta_lta_transfer_start")

    manifest = pd.read_csv(REPO_ROOT / transfer_cfg["inputs"]["manifest_csv"])
    metrics = pd.read_csv(REPO_ROOT / transfer_cfg["inputs"]["trace_metrics_csv"])
    metrics_key = metrics[["event_id", "station", "epicentral_distance_km", "snr_peak_hhz", "rms_vel_hhz_noise"]].copy()

    windows_cfg = transfer_cfg["windows"]
    thresholds = [float(t) for t in transfer_cfg["thresholds"]]
    sta_lta_windows = transfer_cfg["sta_lta_windows"]
    off_thr = float(transfer_cfg["baseline"]["off_threshold"])

    record_rows: list[dict[str, Any]] = []
    noise_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    example_packs: dict[str, Any] = {}

    for _, row in manifest.iterrows():
        loaded = load_processed_record(row, analysis_cfg, REPO_ROOT)
        if loaded is None:
            continue
        origin = loaded["origin"]
        starttime = loaded["starttime"]
        rate = loaded["sampling_rate"]
        mute_s = loaded["mute_s"]
        causal_z = loaded["variants"]["causal_bandpass"]["HHZ"]
        noise_win = window_pair(origin, windows_cfg["noise_start_offset_s"], windows_cfg["noise_end_offset_s"])
        noise_seg = slice_array_window(causal_z.data, starttime, rate, noise_win)
        noise_rows.append(
            {
                "event_id": loaded["event_id"],
                "station": loaded["station"],
                "noise_rms": rms(noise_seg),
                "noise_peak": peak_abs(noise_seg),
                "noise_std": float(np.std(noise_seg)) if len(noise_seg) else float("nan"),
                "sampling_rate_hz": rate,
            }
        )

        meta = metrics_key[(metrics_key.event_id == loaded["event_id"]) & (metrics_key.station == loaded["station"])]
        dist = float(meta["epicentral_distance_km"].iloc[0]) if not meta.empty else float("nan")
        snr = float(meta["snr_peak_hhz"].iloc[0]) if not meta.empty else float("nan")

        for variant_name, comps in loaded["variants"].items():
            channels = REQUIRED_HH_3C if variant_name == "causal_bandpass" else ("HHZ",)
            for channel in channels:
                tr = comps[channel]
                for win in sta_lta_windows:
                    sta_s = float(win["sta_window_s"])
                    lta_s = float(win["lta_window_s"])
                    if variant_name != "causal_bandpass" and not (
                        math.isclose(sta_s, 0.5) and math.isclose(lta_s, 10.0)
                    ):
                        continue
                    if channel != "HHZ" and not (math.isclose(sta_s, 0.5) and math.isclose(lta_s, 10.0)):
                        continue
                    mute = edge_mute_seconds(len(tr.data), rate, 0.05, lta_s, 0.0)
                    cft, _nsta, nlta = sta_lta_characteristic_function(
                        np.asarray(tr.data, dtype=float), rate, sta_s, lta_s
                    )
                    for threshold in thresholds:
                        pack = onsets_from_cft(cft, rate, nlta, threshold, off_thr, mute, mute)
                        counts = _evaluate_onsets(pack, starttime, rate, origin, windows_cfg, mute)
                        rec = {
                            "event_id": loaded["event_id"],
                            "station": loaded["station"],
                            "magnitude": loaded["magnitude"],
                            "epicentral_distance_km": dist,
                            "snr_peak_hhz": snr,
                            "processing": variant_name,
                            "channel": channel,
                            "sta_window_s": sta_s,
                            "lta_window_s": lta_s,
                            "threshold": threshold,
                            **counts,
                        }
                        record_rows.append(rec)
                        if (
                            variant_name == "causal_bandpass"
                            and channel == "HHZ"
                            and math.isclose(sta_s, 0.5)
                            and math.isclose(lta_s, 10.0)
                            and math.isclose(threshold, 2.5)
                        ):
                            cft = pack["cft"]
                            early_win = (starttime, starttime + mute)
                            post_mute = (starttime + mute, origin - 60.0)
                            gap = (origin - 10.0, origin)
                            post = (origin, origin + 90.0)
                            edge_rows.append(
                                {
                                    "event_id": loaded["event_id"],
                                    "station": loaded["station"],
                                    "mute_s": mute,
                                    "unmasked_in_mute": counts["unmasked_in_mute"],
                                    "unmasked_from_trace_start_s": counts["unmasked_from_trace_start_s"],
                                    "max_cft_mute_region": cft_window_stats(cft, starttime, rate, early_win, 2.5)["max_cft"],
                                    "max_cft_post_mute_pre_noise": cft_window_stats(cft, starttime, rate, post_mute, 2.5)["max_cft"],
                                    "max_cft_noise": cft_window_stats(cft, starttime, rate, noise_win, 2.5)["max_cft"],
                                    "frac_cft_noise_ge_2p5": cft_window_stats(cft, starttime, rate, noise_win, 2.5)["fraction_above"],
                                    "max_cft_origin_minus10_to_0": cft_window_stats(cft, starttime, rate, gap, 2.5)["max_cft"],
                                    "max_cft_post_origin_90": cft_window_stats(cft, starttime, rate, post, 2.5)["max_cft"],
                                    "n_onsets_noise": counts["n_onsets_noise"],
                                }
                            )
                            ex_pre = transfer_cfg["figures"]["example_pre_event"]
                            ex_post = transfer_cfg["figures"]["example_post_origin"]
                            payload = {
                                "data": np.asarray(tr.data, dtype=float),
                                "cft": cft,
                                "rate": rate,
                                "starttime": starttime,
                                "origin": origin,
                                "ylabel": "m/s (causal 0.1–15 Hz)",
                            }
                            if loaded["event_id"] == ex_pre["event_id"] and loaded["station"] == ex_pre["station"]:
                                payload["mark_s"] = counts["first_search_latency_s"]
                                example_packs["pre_event"] = dict(payload)
                                example_packs["edge"] = dict(payload)
                            if loaded["event_id"] == ex_post["event_id"] and loaded["station"] == ex_post["station"]:
                                payload["mark_s"] = counts["first_post_origin_latency_s"]
                                example_packs["post_origin"] = dict(payload)
        LOGGER.info("processed %s %s", loaded["event_id"], loaded["station"])

    rec_df = pd.DataFrame(record_rows)
    rec_df.to_csv(out_dir / "record_trigger_grid.csv", index=False)
    thresh_df = aggregate_threshold_rows(record_rows)
    causal_hh_z = thresh_df[
        (thresh_df.processing == "causal_bandpass") & (thresh_df.channel == "HHZ") & (thresh_df.sta_window_s == 0.5) & (thresh_df.lta_window_s == 10.0)
    ].sort_values("threshold")
    causal_hh_z.to_csv(out_dir / "threshold_sensitivity.csv", index=False)

    window_df = thresh_df[(thresh_df.processing == "causal_bandpass") & (thresh_df.channel == "HHZ") & (thresh_df.threshold == 2.5)].copy()
    window_df.to_csv(out_dir / "window_sensitivity.csv", index=False)

    proc_df = thresh_df[(thresh_df.channel == "HHZ") & (thresh_df.sta_window_s == 0.5) & (thresh_df.lta_window_s == 10.0) & (thresh_df.threshold == 2.5)]
    proc_df.to_csv(out_dir / "processing_variant_comparison.csv", index=False)

    base_rec = rec_df[
        (rec_df.processing == "causal_bandpass")
        & (rec_df.channel == "HHZ")
        & (rec_df.sta_window_s == 0.5)
        & (rec_df.lta_window_s == 10.0)
        & (rec_df.threshold == 2.5)
    ]
    noise_df = pd.DataFrame(noise_rows)
    station_df = (
        base_rec.merge(noise_df, on=["event_id", "station"], how="left")
        .groupby("station", sort=True)
        .agg(
            n_records=("event_id", "count"),
            n_noise_onset=("has_noise_onset", "sum"),
            noise_onset_rate=("has_noise_onset", "mean"),
            n_pre_origin=("has_pre_origin_onset", "sum"),
            n_post_origin=("has_post_origin_onset", "sum"),
            median_noise_rms=("noise_rms", finite_median),
            median_snr=("snr_peak_hhz", finite_median),
            median_search_latency_s=("first_search_latency_s", finite_median),
            median_post_origin_latency_s=("first_post_origin_latency_s", finite_median),
        )
        .reset_index()
    )
    station_df.to_csv(out_dir / "station_trigger_summary.csv", index=False)

    component_rows = []
    for channel, grp in rec_df[
        (rec_df.processing == "causal_bandpass") & (rec_df.sta_window_s == 0.5) & (rec_df.lta_window_s == 10.0) & (rec_df.threshold == 2.5)
    ].groupby("channel"):
        component_rows.append(
            {
                "channel": channel,
                "n_records": len(grp),
                "noise_record_fraction": float(grp["has_noise_onset"].mean()),
                "pre_origin_record_fraction": float(grp["has_pre_origin_onset"].mean()),
                "post_origin_coverage": float(grp["has_post_origin_onset"].mean()),
                "median_search_latency_s": finite_median(grp["first_search_latency_s"]),
                "median_post_origin_latency_s": finite_median(grp["first_post_origin_latency_s"]),
                "median_n_onsets_noise": finite_median(grp["n_onsets_noise"]),
            }
        )
    component_df = pd.DataFrame(component_rows)
    component_df.to_csv(out_dir / "component_trigger_summary.csv", index=False)

    edge_df = pd.DataFrame(edge_rows)
    edge_df.to_csv(out_dir / "edge_effect_diagnostics.csv", index=False)
    noise_df.to_csv(out_dir / "noise_window_statistics.csv", index=False)

    proposal = apply_proposal_rule(thresh_df.to_dict(orient="records"), transfer_cfg["proposal_rule"])

    figures = make_figures(rec_df, thresh_df, window_df, station_df, component_df, noise_df, example_packs, transfer_cfg, fig_dir)

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "n_records_processed": int(base_rec["event_id"].nunique() and len(base_rec)),
        "n_event_station": int(len(base_rec)),
        "implementation": {
            "algorithm": "ObsPy classic_sta_lta + trigger_onset",
            "official_swiss_run": "causal 0.1–15 Hz after VEL response; STA 0.5 s; LTA 10 s; on=2.5; off=0.5; edge mute max(LTA, 5% duration); official search origin-5 to +90 s",
            "california": "raw BHZ counts; same STA/LTA numbers; first onset on origin-aligned 300 s trace; no true pre-event",
        },
        "noise_window": {
            "rms_median": finite_median(noise_df["noise_rms"]),
            "rms_min": float(np.nanmin(noise_df["noise_rms"])),
            "rms_max": float(np.nanmax(noise_df["noise_rms"])),
            "peak_median": finite_median(noise_df["noise_peak"]),
        },
        "edge_effects_at_2p5_causal_hhz": {
            "n": int(len(edge_df)),
            "n_unmasked_in_mute": int(edge_df["unmasked_in_mute"].sum()) if len(edge_df) else 0,
            "median_max_cft_noise": finite_median(edge_df["max_cft_noise"]) if len(edge_df) else float("nan"),
            "median_frac_cft_noise_ge_2p5": finite_median(edge_df["frac_cft_noise_ge_2p5"]) if len(edge_df) else float("nan"),
            "median_max_cft_mute": finite_median(edge_df["max_cft_mute_region"]) if len(edge_df) else float("nan"),
            "median_max_cft_post_origin": finite_median(edge_df["max_cft_post_origin_90"]) if len(edge_df) else float("nan"),
        },
        "threshold_sensitivity_causal_hhz_0p5_10": causal_hh_z.to_dict(orient="records"),
        "processing_at_2p5": proc_df.to_dict(orient="records"),
        "window_sensitivity_at_2p5": window_df.to_dict(orient="records"),
        "components_at_2p5": component_df.to_dict(orient="records"),
        "proposal": proposal,
        "proposal_disclaimer": "Proposed configuration for a future validation study. Not validated. Not optimal. Not operational EEW.",
        "figures": figures,
    }
    (out_dir / "trigger_analysis.json").write_text(json.dumps(_json_ready(summary), indent=2), encoding="utf-8")
    LOGGER.info("sta_lta_transfer_complete records=%s proposal=%s", len(base_rec), proposal)
    print(json.dumps(_json_ready({"n": len(base_rec), "proposal": proposal, "edge": summary["edge_effects_at_2p5_causal_hhz"]}), indent=2))


if __name__ == "__main__":
    main()
