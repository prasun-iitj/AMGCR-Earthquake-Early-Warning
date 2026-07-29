#!/usr/bin/env python3
"""Phase A.1 EDA for the California IRIS/EarthScope pilot (MiniSEED only).

Reads ``data/raw/iris/**/*.mseed`` and ``data/manifests/iris_california_pilot_events.csv``.
Writes reports under ``reports/eda``, ``reports/figures``, and ``reports/tables``.
"""

from __future__ import annotations


import json
import math
import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from obspy import read

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_IRIS = REPO_ROOT / "data" / "raw" / "iris"
MANIFEST_PATH = REPO_ROOT / "data" / "manifests" / "iris_california_pilot_events.csv"
REPORTS_EDA = REPO_ROOT / "reports" / "eda"
REPORTS_FIGURES = REPO_ROOT / "reports" / "figures"
REPORTS_TABLES = REPO_ROOT / "reports" / "tables"

STATION_ID_RE = re.compile(
    r"(?P<net>[A-Z0-9]+)\.(?P<sta>[A-Z0-9]+)\.(?P<loc>[^.]*)\.(?P<cha>[A-Z0-9]+)\."
)


def _apply_plot_style() -> None:
    plt.rcParams.update(
        {
            "font.size": 11,
            "font.family": "DejaVu Sans",
            "axes.labelsize": 12,
            "axes.titlesize": 13,
            "legend.fontsize": 10,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "axes.grid": True,
            "grid.alpha": 0.35,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


@dataclass
class TraceInspection:
    file_path: str
    event_folder: str
    network: str
    station: str
    location: str
    channel: str
    station_id: str
    sampling_rate_hz: float
    n_samples: int
    duration_s: float
    starttime_utc: str
    endtime_utc: str
    data_min: float
    data_max: float
    data_mean: float
    data_std: float
    in_manifest: bool


def parse_station_from_filename(path: Path) -> tuple[str, str, str, str, str]:
    name = path.name
    match = STATION_ID_RE.match(name)
    if not match:
        return ("", "", "", "", path.stem)
    net = match.group("net")
    sta = match.group("sta")
    loc = match.group("loc") if match.group("loc") else "--"
    cha = match.group("cha")
    station_id = f"{net}.{sta}.{loc}.{cha}"
    return net, sta, loc, cha, station_id


def load_manifest() -> pd.DataFrame:
    if not MANIFEST_PATH.is_file():
        raise FileNotFoundError(f"Missing manifest: {MANIFEST_PATH}")
    df = pd.read_csv(MANIFEST_PATH)
    df["origin_time_utc"] = pd.to_datetime(df["origin_time_utc"], utc=True)
    return df


def manifest_file_set(manifest: pd.DataFrame) -> set[str]:
    paths: set[str] = set()
    for _, row in manifest.iterrows():
        rel = str(row["waveform_files"])
        paths.add(rel.replace("\\", "/"))
    return paths


def inspect_mseed_files(manifest: pd.DataFrame) -> list[TraceInspection]:
    manifest_paths = manifest_file_set(manifest)
    records: list[TraceInspection] = []
    for path in sorted(RAW_IRIS.rglob("*.mseed")):
        rel = path.relative_to(RAW_IRIS).as_posix()
        in_manifest = rel in manifest_paths
        st = read(str(path), headonly=False)
        if len(st) == 0:
            continue
        tr = st[0]
        net, sta, loc, cha, station_id = parse_station_from_filename(path)
        if not net:
            net, sta, loc, cha = tr.stats.network, tr.stats.station, tr.stats.location or "--", tr.stats.channel
            station_id = f"{net}.{sta}.{loc or '--'}.{cha}"
        data = tr.data.astype(float)
        records.append(
            TraceInspection(
                file_path=rel,
                event_folder=path.parent.name,
                network=net,
                station=sta,
                location=loc,
                channel=cha,
                station_id=station_id,
                sampling_rate_hz=float(tr.stats.sampling_rate),
                n_samples=int(tr.stats.npts),
                duration_s=float(tr.stats.npts / tr.stats.sampling_rate),
                starttime_utc=str(tr.stats.starttime.datetime.replace(tzinfo=timezone.utc)),
                endtime_utc=str(tr.stats.endtime.datetime.replace(tzinfo=timezone.utc)),
                data_min=float(np.min(data)),
                data_max=float(np.max(data)),
                data_mean=float(np.mean(data)),
                data_std=float(np.std(data)),
                in_manifest=in_manifest,
            )
        )
    return records


def build_event_summary(manifest: pd.DataFrame, inspections: list[TraceInspection]) -> pd.DataFrame:
    insp_by_event = {i.event_folder: i for i in inspections if i.in_manifest}
    rows: list[dict[str, Any]] = []
    for _, ev in manifest.iterrows():
        eid = str(ev["event_id"])
        insp = insp_by_event.get(eid)
        rows.append(
            {
                "event_id": eid,
                "origin_time_utc": ev["origin_time_utc"].isoformat(),
                "latitude": ev["latitude"],
                "longitude": ev["longitude"],
                "depth_km": ev["depth_km"],
                "magnitude": ev["magnitude"],
                "magnitude_type": ev["magnitude_type"],
                "station_id": insp.station_id if insp else "",
                "channel": insp.channel if insp else "",
                "sampling_rate_hz": insp.sampling_rate_hz if insp else math.nan,
                "duration_s": insp.duration_s if insp else math.nan,
                "waveform_file": insp.file_path if insp else "",
            }
        )
    return pd.DataFrame(rows)


def build_station_summary(inspections: list[TraceInspection]) -> pd.DataFrame:
    manifest_traces = [i for i in inspections if i.in_manifest]
    if not manifest_traces:
        manifest_traces = inspections
    counts = Counter(t.station_id for t in manifest_traces)
    rows: list[dict[str, Any]] = []
    for station_id, n_events in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
        subset = [t for t in manifest_traces if t.station_id == station_id]
        rates = [t.sampling_rate_hz for t in subset]
        durs = [t.duration_s for t in subset]
        rows.append(
            {
                "station_id": station_id,
                "network": subset[0].network,
                "station": subset[0].station,
                "channel": subset[0].channel,
                "event_count": n_events,
                "mean_sampling_rate_hz": float(np.mean(rates)),
                "mean_duration_s": float(np.mean(durs)),
                "min_duration_s": float(np.min(durs)),
                "max_duration_s": float(np.max(durs)),
            }
        )
    return pd.DataFrame(rows)


def dataset_summary_dict(
    manifest: pd.DataFrame,
    inspections: list[TraceInspection],
) -> dict[str, Any]:
    manifest_traces = [i for i in inspections if i.in_manifest]
    all_traces = inspections
    mags = manifest["magnitude"].astype(float)
    origins = manifest["origin_time_utc"]
    channels = sorted({t.channel for t in all_traces})
    stations = sorted({t.station_id for t in manifest_traces})
    rates = [t.sampling_rate_hz for t in manifest_traces]
    durs = [t.duration_s for t in manifest_traces]
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "data_root": str(RAW_IRIS),
        "manifest_path": str(MANIFEST_PATH),
        "n_mseed_files_total": len(all_traces),
        "n_mseed_files_in_manifest": len(manifest_traces),
        "n_events_manifest": int(len(manifest)),
        "n_unique_stations_manifest": len(stations),
        "channels": channels,
        "sampling_rates_hz_unique": sorted({t.sampling_rate_hz for t in manifest_traces}),
        "duration_s": {
            "min": float(np.min(durs)) if durs else None,
            "max": float(np.max(durs)) if durs else None,
            "mean": float(np.mean(durs)) if durs else None,
        },
        "magnitude": {
            "min": float(mags.min()),
            "max": float(mags.max()),
            "mean": float(mags.mean()),
            "median": float(mags.median()),
            "std": float(mags.std(ddof=0)),
        },
        "time_coverage": {
            "first_origin_utc": origins.min().isoformat(),
            "last_origin_utc": origins.max().isoformat(),
        },
        "station_ids_manifest": stations,
    }


def plot_example_waveform(manifest: pd.DataFrame, inspections: list[TraceInspection], out: Path) -> dict[str, str]:
    manifest_traces = [i for i in inspections if i.in_manifest]
    if not manifest_traces:
        raise RuntimeError("No manifest-linked MiniSEED files found.")
    idx = manifest["magnitude"].astype(float).idxmax()
    event_id = str(manifest.loc[idx, "event_id"])
    chosen = next(t for t in manifest_traces if t.event_folder == event_id)
    path = RAW_IRIS / chosen.file_path
    tr = read(str(path))[0]
    times = tr.times()
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.plot(times, tr.data, color="#1f4e79", linewidth=0.6)
    mag = manifest.loc[idx, "magnitude"]
    ax.set_title(
        f"Raw vertical component — {chosen.station_id}\n"
        f"M {mag:.2f} ({manifest.loc[idx, 'magnitude_type']}) · origin {manifest.loc[idx, 'origin_time_utc']}"
    )
    ax.set_xlabel("Time since trace start (s)")
    ax.set_ylabel("Counts")
    fig.savefig(out)
    plt.close(fig)
    return {"figure": out.name, "event_id": event_id, "file": chosen.file_path}


def plot_magnitude_histogram(manifest: pd.DataFrame, out: Path) -> None:
    mags = manifest["magnitude"].astype(float)
    fig, ax = plt.subplots(figsize=(5.5, 4))
    bins = np.linspace(mags.min() - 0.05, mags.max() + 0.05, 8)
    ax.hist(mags, bins=bins, color="#2e7d32", edgecolor="white", linewidth=0.8)
    ax.set_xlabel("Magnitude")
    ax.set_ylabel("Event count")
    ax.set_title("California pilot — magnitude distribution")
    fig.savefig(out)
    plt.close(fig)


def plot_events_over_time(manifest: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4))
    times = manifest["origin_time_utc"]
    mags = manifest["magnitude"].astype(float)
    ax.scatter(times, mags, s=70, c="#c62828", edgecolors="white", linewidths=0.8, zorder=3)
    for _, row in manifest.iterrows():
        ax.annotate(
            f"{row['magnitude']:.2f}",
            (row["origin_time_utc"], row["magnitude"]),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=8,
        )
    ax.set_xlabel("Origin time (UTC)")
    ax.set_ylabel("Magnitude")
    ax.set_title("Pilot events over time")
    fig.autofmt_xdate()
    fig.savefig(out)
    plt.close(fig)


def plot_station_usage(station_summary: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(5, 4))
    labels = station_summary["station_id"].tolist()
    counts = station_summary["event_count"].tolist()
    y_pos = np.arange(len(labels))
    ax.barh(y_pos, counts, color="#5c6bc0", edgecolor="white")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Number of events")
    ax.set_title("Station usage frequency (manifest waveforms)")
    fig.savefig(out)
    plt.close(fig)


def main() -> None:
    _apply_plot_style()
    for d in (REPORTS_EDA, REPORTS_FIGURES, REPORTS_TABLES):
        d.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest()
    inspections = inspect_mseed_files(manifest)
    if not inspections:
        raise FileNotFoundError(f"No MiniSEED files under {RAW_IRIS}")

    summary = dataset_summary_dict(manifest, inspections)
    event_df = build_event_summary(manifest, inspections)
    station_df = build_station_summary(inspections)

    inspection_df = pd.DataFrame([asdict(i) for i in inspections])
    inspection_df.to_csv(REPORTS_EDA / "mseed_file_inspection.csv", index=False)
    with (REPORTS_EDA / "dataset_summary.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    event_df.to_csv(REPORTS_TABLES / "event_summary.csv", index=False)
    station_df.to_csv(REPORTS_TABLES / "station_summary.csv", index=False)

    waveform_meta = plot_example_waveform(
        manifest, inspections, REPORTS_FIGURES / "example_waveform_raw.png"
    )
    plot_magnitude_histogram(manifest, REPORTS_FIGURES / "magnitude_histogram.png")
    plot_events_over_time(manifest, REPORTS_FIGURES / "events_over_time.png")
    plot_station_usage(station_df, REPORTS_FIGURES / "station_usage_frequency.png")

    run_meta = {
        "summary": summary,
        "example_waveform": waveform_meta,
        "outputs": {
            "eda": [p.name for p in sorted(REPORTS_EDA.iterdir())],
            "figures": [p.name for p in sorted(REPORTS_FIGURES.iterdir())],
            "tables": [p.name for p in sorted(REPORTS_TABLES.iterdir())],
        },
    }
    with (REPORTS_EDA / "eda_run_metadata.json").open("w", encoding="utf-8") as fh:
        json.dump(run_meta, fh, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
