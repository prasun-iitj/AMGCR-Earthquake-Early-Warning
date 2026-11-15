"""Data-journey figures (reports/figures/data/).

Diagrams contain only documented structure. Count figures read
reports/data_lineage/data_lineage_summary.json (run audit_data_lineage.py first).
Waveform figures apply the documented preprocessing steps to ONE record each,
for display only; nothing is written back to any dataset.

Existing figures reused (not regenerated): reports/figures/final/fig02, fig03, fig04, fig06, fig11.

Usage (repo root):  python scripts/reporting/make_data_figures.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_final_figures import arrow, box, canvas  # noqa: E402  (diagram helpers)

OUT = ROOT / "reports/figures/data"
OUT.mkdir(parents=True, exist_ok=True)
L = json.load(open(ROOT / "reports/data_lineage/data_lineage_summary.json"))
C_CA, C_A, C_C = "#8c8c8c", "#4c72b0", "#c44e52"


def save(fig, name):
    p = OUT / name
    fig.savefig(p, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", p.relative_to(ROOT))


# D1 lineage ---------------------------------------------------------------
def d1():
    fig, ax = canvas(13, 6.2, "Data Fig. 1  Source-to-dataset lineage (what was downloaded, annotated and derived)")
    rows = [
        (4.7, "California pilot", C_CA, [("USGS FDSN events\n(M4.0-7.5, 2024)", "#eef2f8"), ("EarthScope waveforms\n8 x CI BHZ MiniSEED", "#eef2f8"),
                                          ("Counts, no response\n(0/8 applied)", "#eef2f8"), ("STA/LTA picks (2.5)\n8x18 features", "#eef2f8")]),
        (2.9, "Swiss Set A", C_A, [("SED event catalogue\n20 fixed event IDs", "#eef2f8"), ("SED/ETH waveforms\n120 HH 3C MiniSEED\n+ StationXML", "#eef2f8"),
                                    ("SED QuakeML picks\n120 manual first-P", "#fdebd0"), ("240 windows\n24 features", "#d5f5e3")]),
        (1.1, "Swiss Set C", C_C, [("SED catalogue pool\n227 -> 15 locked", "#eef2f8"), ("SED/ETH waveforms\n550 HHZ MiniSEED\n+ StationXML", "#eef2f8"),
                                    ("SED QuakeML picks\n550 manual first-P", "#fdebd0"), ("1,100 windows\n18 features", "#d5f5e3")]),
    ]
    for y, name, col, cells in rows:
        ax.text(0.15, y + 0.55, name, fontweight="bold", color=col, fontsize=11, va="center", rotation=0)
        for i, (t, fc) in enumerate(cells):
            x = 2.2 + i * 2.7
            box(ax, x, y, 2.3, 1.1, t, fc=fc, fs=8.5)
            if i:
                arrow(ax, x - 0.38, y + 0.55, x - 0.02, y + 0.55)
    ax.text(2.2, 0.35, "Blue-grey: downloaded from provider.  Orange: analyst annotation (SED).  Green: derived by project code.",
            fontsize=9)
    save(fig, "dfig01_source_to_dataset_lineage.png")


# D2 sources ---------------------------------------------------------------
def d2():
    fig, ax = canvas(13, 4.8, "Data Fig. 2  Original data sources: IRIS/EarthScope + USGS (California) vs SED/ETH (Switzerland)")
    cols = [
        ("California pilot", C_CA, ["Events: USGS FDSN event service", "  earthquake.usgs.gov", "Waveforms: EarthScope (IRIS) dataselect", "  service.earthscope.org",
                                   "Channel BHZ, 300 s from origin", "No analyst picks; no StationXML saved"]),
        ("Swiss (Set A and Set C)", C_A, ["Events, picks, waveforms, metadata:", "  SED/ETH FDSN via eida.ethz.ch", "  event (QuakeML), dataselect (MiniSEED),",
                                         "  station (StationXML level=response)", "Network CH; HH channels", "Analyst P picks from QuakeML arrivals"]),
    ]
    for i, (t, c, lines) in enumerate(cols):
        x = 0.4 + i * 6.4
        ax.add_patch(FancyBboxPatch((x, 0.8), 6.0, 3.4, boxstyle="round,pad=0.02,rounding_size=0.15", fc="white", ec=c, lw=2.5))
        ax.text(x + 0.25, 3.8, t, fontweight="bold", color=c, fontsize=12)
        for j, l in enumerate(lines):
            ax.text(x + 0.25, 3.3 - j * 0.42, l, fontsize=9.8)
    ax.text(0.4, 0.3, "Sources verified in scripts/download/*.py and configs/*.yaml. Provider licence terms were not reviewed here.", fontsize=9)
    save(fig, "dfig02_iris_vs_sed_sources.png")


# D3 raw structure ---------------------------------------------------------
def d3():
    a, c = L["set_a"], L["set_c"]
    fig, ax = canvas(13, 6.0, "Data Fig. 3  Actual raw-data folder structure (local; git-ignored)")
    txt = (
        "data/\n"
        "  raw/\n"
        f"    iris/quakeml_..._eventid_<usgs-id>_format_quakeml/CI.ADO.--.BHZ.<origin>.mseed   {L['california']['local_raw_mseed_files']} files (8 in manifest)\n"
        "    catalogs/catalog.xml                                       1 QuakeML test catalogue (acquisition_config.yaml)\n"
        f"    switzerland/<short_id>/CH.<STA>.--.HH.<origin>.mseed       {a['local_raw_mseed_files']} files, 20 event folders (3 components per file)\n"
        f"    switzerland_validation/<short_id>/CH.<STA>.--.HHZ.<origin>.mseed   {c['local_raw_mseed_files']} files, 15 event folders\n"
        "  metadata/\n"
        f"    switzerland/<short_id>/CH.<STA>.--.HH.xml (StationXML) + quakeml.xml     {a['local_stationxml_files']} XML\n"
        f"    switzerland_validation/<short_id>/CH.<STA>.--.HHZ.xml (+ quakeml.xml)    {c['local_stationxml_files']} XML\n"
        "  manifests/   (published)\n"
        "    iris_california_pilot_events.csv                     8 rows\n"
        f"    sed_switzerland_pilot_events.csv                     {a['records']} rows (Set A records)\n"
        f"    sed_switzerland_set_a_picks.csv                      {a['picks']['n']} rows\n"
        "    sed_switzerland_validation_candidates.csv            227 rows\n"
        f"    sed_switzerland_validation_waveforms.csv             {c['records']} rows\n"
        f"    sed_switzerland_validation_picks.csv                 {c['picks']['n']} rows\n"
        "reports/features/swiss_set_a_feature_matrix.csv   240 x 45   |   swiss_set_c_feature_matrix.csv   1,100 x 35  (published)"
    )
    ax.text(0.25, 5.3, txt, family="monospace", fontsize=8.1, va="top", linespacing=1.55)
    save(fig, "dfig03_raw_data_structure.png")


# D4 pipeline --------------------------------------------------------------
def d4():
    fig, ax = canvas(13, 6.0, "Data Fig. 4  Preprocessing and feature pipeline (Set A / Set C scripts)")
    steps = [
        "1 Read MiniSEED\n+ StationXML", "2 Demean,\nlinear detrend", "3 5% Hann\ntaper", "4 remove_response\nVEL, water level 60\n(pre-filter)",
        "5 Bandpass 0.1-15 Hz\n4 corners,\nzero-phase", "6 Select HHZ (A: 3C)\nSTA/LTA on full trace", "7 Cut 4 s windows\npick -> pick+4 s\norigin-35 s -> -31 s", "8 Window features\n24 (A) / 18 (C)",
    ]
    for i, t in enumerate(steps):
        r, cidx = divmod(i, 4)
        x, y = 0.4 + cidx * 3.2, 3.5 - r * 2.2
        box(ax, x, y, 2.7, 1.5, t, fs=9, fc="#fdebd0" if i == 4 else "#eef2f8")
        if cidx:
            arrow(ax, x - 0.48, y + 0.75, x - 0.02, y + 0.75)
    arrow(ax, 12.2, 3.5, 1.7, 3.0, "#7f8c8d")
    ax.text(0.4, 0.5, "Step 5 (orange) is applied to the full trace before windowing: window samples depend on neighbouring samples.\n"
            "Pre-filter corners differ: Set A uses src/analysis/switzerland_signal.pre_filt_for_sampling; Set C uses explicit corners "
            "(f3 = min(18 Hz, 0.75 Nyquist), f4 = min(22.5 Hz, 0.85 Nyquist)).", fontsize=8.6)
    save(fig, "dfig04_preprocessing_pipeline.png")


# helpers for real waveforms -----------------------------------------------
def pre_filt_set_a(fs):
    from src.analysis.switzerland_signal import pre_filt_for_sampling
    return pre_filt_for_sampling(fs, {"pre_filt_f1_hz": 0.05, "pre_filt_f2_hz": 0.08, "pre_filt_f3_nyquist_fraction": 0.75,
                                      "pre_filt_f4_nyquist_fraction": 0.85}, {"freqmax_hz": 15.0})


def pre_filt_set_c(fs):
    ny = 0.5 * fs
    f3 = min(15.0 * 1.2, ny * 0.75)
    f4 = min(15.0 * 1.5, ny * 0.85)
    if f4 <= f3:
        f4 = min(ny * 0.95, f3 + 5.0)
    return (0.05, 0.08, f3, f4)


def process(st, inv, pre_filt, stage):
    s = st.copy()
    s.detrend("demean"); s.detrend("linear"); s.taper(max_percentage=0.05, type="hann")
    s.remove_response(inventory=inv, output="VEL", water_level=60.0, pre_filt=pre_filt, zero_mean=True, taper=False)
    if stage == "bp":
        s.filter("bandpass", freqmin=0.1, freqmax=15.0, corners=4, zerophase=True)
    return s


# D5 filtering before/after (real) ------------------------------------------
def d5():
    from obspy import UTCDateTime, read, read_inventory
    man = pd.read_csv(ROOT / "data/manifests/sed_switzerland_pilot_events.csv")
    pk = pd.read_csv(ROOT / "data/manifests/sed_switzerland_set_a_picks.csv")
    row = man[(man.event_id.str.endswith("2020btnrcj")) & (man.station == "EMBD")].iloc[0]
    pick = pk[(pk.short_id == "2020btnrcj") & (pk.station == "EMBD")].iloc[0]
    f = ROOT / row.waveform_file
    if not f.exists():
        print("d5 skipped: raw waveform not available locally"); return
    st = read(str(f)).select(channel="HHZ"); st.merge(method=1, fill_value=0)
    inv = read_inventory(str(ROOT / "data/metadata/switzerland/2020btnrcj/CH.EMBD.--.HH.xml"))
    origin, tp = UTCDateTime(row.origin_time_utc), UTCDateTime(pick.pick_time_utc)
    fs = st[0].stats.sampling_rate
    stages = [("(a) Raw counts", st), ("(b) Response removed to velocity, no bandpass", process(st, inv, pre_filt_set_a(fs), "resp")),
              ("(c) Velocity + 0.1-15 Hz zero-phase bandpass (used for features)", process(st, inv, pre_filt_set_a(fs), "bp"))]
    units = ["counts", "m/s", "m/s"]
    fig, axs = plt.subplots(3, 1, figsize=(11, 7.4), sharex=True)
    for ax, (lab, s), u in zip(axs, stages, units):
        tr = s[0]; t = np.array([x - origin for x in tr.times("utcdatetime")])
        m = (t > -45) & (t < 40)
        ax.plot(t[m], tr.data[m], color="#222", lw=0.6)
        ax.axvline(tp - origin, color=C_C, ls="--", lw=1.1, label=f"SED analyst pick {pick.pick_phase}")
        ax.axvspan(-35, -31, color="#7f8c8d", alpha=0.25); ax.axvspan(tp - origin, tp - origin + 4, color=C_C, alpha=0.2)
        ax.set_ylabel(u); ax.set_title(lab, loc="left", fontsize=10)
    axs[0].legend(loc="upper left", fontsize=8)
    axs[-1].set_xlabel("Time relative to catalogue origin (s)   (grey: noise window, red: P window)")
    fig.suptitle(f"Data Fig. 5  Before/after preprocessing, real Set A record (event 2020btnrcj, CH.EMBD, HHZ, {fs:.0f} Hz)",
                 x=0.01, ha="left", fontweight="bold")
    fig.tight_layout()
    save(fig, "dfig05_filtering_before_after.png")


# D6 3C vs vertical-only (real) ---------------------------------------------
def d6():
    from obspy import UTCDateTime, read, read_inventory
    man = pd.read_csv(ROOT / "data/manifests/sed_switzerland_pilot_events.csv")
    pk = pd.read_csv(ROOT / "data/manifests/sed_switzerland_set_a_picks.csv")
    ra = man[(man.event_id.str.endswith("2020btnrcj")) & (man.station == "EMBD")].iloc[0]
    pa = pk[(pk.short_id == "2020btnrcj") & (pk.station == "EMBD")].iloc[0]
    cm = pd.read_csv(ROOT / "data/manifests/sed_switzerland_validation_waveforms.csv").sort_values("magnitude", ascending=False)
    rc = cm.iloc[0]
    fa_, fc_ = ROOT / ra.waveform_file, ROOT / rc.MiniSEED_path
    if not (fa_.exists() and fc_.exists()):
        print("d6 skipped: raw waveforms not available locally"); return
    sta_ = read(str(fa_)); invA = read_inventory(str(ROOT / "data/metadata/switzerland/2020btnrcj/CH.EMBD.--.HH.xml"))
    stc = read(str(fc_)); stc.merge(method=1, fill_value="interpolate"); invC = read_inventory(str(ROOT / rc.StationXML_path))
    pa_s = process(sta_, invA, pre_filt_set_a(sta_[0].stats.sampling_rate), "bp")
    pc_s = process(stc, invC, pre_filt_set_c(stc[0].stats.sampling_rate), "bp")
    oa, oc = UTCDateTime(ra.origin_time_utc), UTCDateTime(rc.origin_time)
    ta, tc = UTCDateTime(pa.pick_time_utc), UTCDateTime(rc.pick_time_utc)
    fig, axs = plt.subplots(4, 1, figsize=(11, 8), sharex=False)
    for ax, ch in zip(axs[:3], ["HHZ", "HHN", "HHE"]):
        tr = pa_s.select(channel=ch)[0]; t = np.array([x - oa for x in tr.times("utcdatetime")]); m = (t > -10) & (t < 40)
        ax.plot(t[m], tr.data[m], color="#222", lw=0.6); ax.axvline(ta - oa, color=C_C, ls="--", lw=1)
        ax.set_ylabel(f"{ch}\nm/s"); 
    axs[0].set_title(f"Set A: three components, CH.EMBD, event 2020btnrcj (M{ra.magnitude:.1f})", loc="left", fontsize=10)
    tr = pc_s[0]; t = np.array([x - oc for x in tr.times("utcdatetime")]); m = (t > -10) & (t < 40)
    axs[3].plot(t[m], tr.data[m], color="#222", lw=0.6); axs[3].axvline(tc - oc, color=C_C, ls="--", lw=1)
    axs[3].set_ylabel("HHZ\nm/s"); axs[3].set_xlabel("Time relative to origin (s); dashed = SED analyst pick")
    axs[3].set_title(f"Set C: vertical only, CH.{rc.station}, event {rc.short_id} (M{rc.magnitude:.1f})", loc="left", fontsize=10)
    fig.suptitle("Data Fig. 6  Three-component (Set A) vs vertical-only (Set C) records, response-corrected and 0.1-15 Hz filtered",
                 x=0.01, ha="left", fontweight="bold")
    fig.tight_layout()
    save(fig, "dfig06_three_component_vs_vertical.png")


# D7 comparison ------------------------------------------------------------
def d7():
    a, c, ca = L["set_a"], L["set_c"], L["california"]
    keys = ["Events", "Stations", "Records", "Windows"]
    vals = {"California": [ca["events"], 2, ca["waveform_files_in_manifest"], 0],
            "Set A": [a["events"], a["stations"], a["records"], a["windows"]["total"]],
            "Set C": [c["events"], c["stations"], c["records"], c["windows"]["total"]]}
    fig, ax = plt.subplots(figsize=(11, 4.6)); w = 0.26
    for k, (n, col) in enumerate(zip(vals, [C_CA, C_A, C_C])):
        xs = np.arange(4) + (k - 1) * w; ax.bar(xs, vals[n], w, color=col, label=n)
        for x, v in zip(xs, vals[n]): ax.text(x, v * 1.08 + 0.5, f"{v:,}" if v else "n/a", ha="center", fontsize=8.5)
    ax.set_yscale("log"); ax.set_xticks(range(4)); ax.set_xticklabels(keys); ax.set_ylabel("Count (log scale)"); ax.legend()
    ax.set_title("Data Fig. 7  Dataset comparison. California has no ML windows; windows are not independent events", loc="left", fontweight="bold")
    save(fig, "dfig07_set_a_vs_set_c_comparison.png")


# D8 feature matrix structure ----------------------------------------------
def d8():
    fig, ax = canvas(13, 5.4, "Data Fig. 8  Feature-matrix structure (columns read from the committed CSV files)")
    sa = L["schemas"]["set_a_matrix_columns"]; sc = L["schemas"]["set_c_matrix_columns"]
    f24 = L["schemas"]["feature_columns_24_in_set_a_matrix_order"]; f18 = L["schemas"]["vertical_schema_json"]
    def row(y, title, ncol, nrow, meta, feat, col):
        ax.text(0.3, y + 1.15, f"{title}: {nrow:,} rows x {ncol} columns", fontweight="bold", color=col)
        box(ax, 0.3, y, 4.6, 0.95, f"{meta} metadata / label columns\n(ids, station, magnitude, times, window_type,\nis_earthquake = label)", fc="#eef2f8", fs=8.5)
        box(ax, 5.1, y, 7.6, 0.95, f"{feat} feature columns (model inputs)\n" + ("z_* (16), h_*/vec3c_* (4), vh_ratio, sta_lta_max/mean, snr_db" if feat == 24 else "z_* (16), sta_lta_max, sta_lta_mean"),
            fc="#d5f5e3", fs=8.5)
    row(3.1, "swiss_set_a_feature_matrix.csv", len(sa), L["set_a"]["windows"]["total"], len(sa) - len(f24), len(f24), C_A)
    row(1.0, "swiss_set_c_feature_matrix.csv", len(sc), L["set_c"]["windows"]["total"], len(sc) - len(f18), len(f18), C_C)
    ax.text(0.3, 0.25, "Set A has extra metadata (distances, p_latency_s, channel_group). The 18 vertical features are present in both files, same names; "
            "order is fixed by reports/ml/vertical_feature_schema.json.", fontsize=8.6)
    save(fig, "dfig08_feature_matrix_structure.png")


# D9 QC summary ------------------------------------------------------------
def d9():
    a, c = L["set_a"], L["set_c"]
    items = [
        ("Downloads OK", f"A {a['download_status'].get('OK', 0)}/{a['records']}", f"C {c['download_status'].get('ok', 0)}/{c['records']}"),
        ("MiniSEED validation PASS", f"A {a['validation_status'].get('PASS', 0)}/{a['records']}", f"C {c['verification_status'].get('PASS', 0)}/{c['records']}"),
        ("StationXML available", f"A {a['stationxml_available'].get('YES', 0)}/{a['records']}", f"C {c['stationxml_status'].get('verified', 0)}/{c['records']}"),
        ("Full time coverage", f"A min pre {a['pre_event_seconds_min']:.0f} s, post {a['post_event_seconds_min']:.0f} s", f"C coverage full {c['coverage_status'].get('full', 0)}/{c['records']}"),
        ("Gaps / overlaps in MiniSEED", "A not recorded in manifest", f"C {c['gaps_total']} / {c['overlaps_total']}"),
        ("Manual first-P picks", f"A {a['picks']['n']}  (Pg {a['picks']['phases']['Pg']}, P1 {a['picks']['phases']['P1']}, Pn {a['picks']['phases']['Pn']})",
         f"C {c['picks']['n']}  (Pg {c['picks']['phases']['Pg']}, P1 {c['picks']['phases']['P1']}, Pn {c['picks']['phases']['Pn']})"),
        ("Feature NaN values", f"A {L['schemas']['nan_counts']['set_a_features']}", f"C {L['schemas']['nan_counts']['set_c_features']}"),
        ("Windows (positive / negative)", f"A {a['windows']['positive']} / {a['windows']['negative']}", f"C {c['windows']['positive']} / {c['windows']['negative']}"),
    ]
    fig, ax = plt.subplots(figsize=(11, 4.6)); ax.axis("off")
    tbl = ax.table(cellText=[list(i) for i in items], colLabels=["Check", "Swiss Set A", "Swiss Set C"], loc="center", cellLoc="left", colWidths=[0.28, 0.36, 0.36])
    tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1, 1.7)
    for (r, cidx), cell in tbl.get_celld().items():
        if r == 0: cell.set_facecolor("#1e3a5f"); cell.set_text_props(color="white", fontweight="bold")
    ax.set_title("Data Fig. 9  Quality-control summary from manifests, picks and feature matrices", loc="left", fontweight="bold")
    save(fig, "dfig09_quality_control_summary.png")


if __name__ == "__main__":
    for f in (d1, d2, d3, d4, d5, d6, d7, d8, d9):
        f()
