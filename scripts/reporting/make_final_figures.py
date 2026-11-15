"""Generate the final research figures (reports/figures/final/).

Read-only with respect to science: every number plotted is read from existing
saved artifacts (JSON summaries, feature matrices, per-event CSVs). Diagram
figures contain only documented structure (no data values).

Usage (from repo root):  python scripts/reporting/make_final_figures.py
"""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports/figures/final"
ML = ROOT / "reports/ml"
FEAT = ROOT / "reports/features"
OUT.mkdir(parents=True, exist_ok=True)

C_RF, C_XGB, C_STA = "#1f77b4", "#2ca02c", "#ff7f0e"
C_A, C_C, C_CA = "#4c72b0", "#c44e52", "#8c8c8c"
C_BOX = "#eef2f8"
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "font.family": "DejaVu Sans"})


def save(fig, name):
    p = OUT / name
    fig.savefig(p, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", p.relative_to(ROOT))


def box(ax, x, y, w, h, text, fc=C_BOX, ec="#34495e", fs=10, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc=fc, ec=ec, lw=1.3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", wrap=True)


def arrow(ax, x1, y1, x2, y2, color="#34495e"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16,
                                 lw=1.5, color=color))


def canvas(w, h, title):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    ax.set_title(title, fontsize=14, fontweight="bold", loc="left")
    return fig, ax


# ---------------------------------------------------------------- results
sc = json.load(open(ML / "vertical_set_c_evaluation_summary.json"))
sa = json.load(open(ML / "vertical_set_a_evaluation_summary.json"))
ml3 = json.load(open(ML / "swiss_ml_evaluation_summary.json"))
fa = pd.read_csv(FEAT / "swiss_set_a_feature_matrix.csv")
fc = pd.read_csv(FEAT / "swiss_set_c_feature_matrix.csv")


# 01 workflow -------------------------------------------------------------
def fig01():
    fig, ax = canvas(13, 4.6, "Fig. 1  End-to-end research workflow (offline window-classification benchmark)")
    steps = [
        ("California\npilot (IRIS)\n8 events\nv1.0.0 frozen", C_CA),
        ("Swiss Set A\n20 events\n120 3C records\nSED P picks", C_A),
        ("Response\ncorrection\n-> velocity\n0.1-15 Hz", C_BOX),
        ("4 s windows\n(pick-aligned P,\npre-origin noise)\n240 windows", C_BOX),
        ("Features\n24 (3C)\n18 (vertical)", C_BOX),
        ("RF + XGBoost\n20-fold LOGO\nCV on Set A", C_BOX),
        ("Freeze, then\nSet C test\n15 unseen events\n1,100 windows", C_C),
    ]
    n = len(steps)
    w, gap = 1.5, 0.3
    x0 = 0.3
    for i, (t, c) in enumerate(steps):
        x = x0 + i * (w + gap)
        box(ax, x, 1.9, w, 1.5, t, fc=c if c != C_BOX else C_BOX, fs=9,
            bold=False)
        if i:
            arrow(ax, x - gap + 0.02, 2.65, x - 0.02, 2.65)
    ax.text(0.3, 1.2, "Baselines: STA/LTA threshold 8.0 (Set A grid-derived). STEP 2K record-level detector is a separate, "
            "frozen validation (401/550 = 72.9% detected).", fontsize=9.5)
    ax.text(0.3, 0.7, "Not an operational real-time EEW system. Classifier judges pre-cut 4 s windows.",
            fontsize=9.5, color="#a93226")
    save(fig, "fig01_research_workflow.png")


# 02 datasets -------------------------------------------------------------
def fig02():
    fig, ax = canvas(13, 4.8, "Fig. 2  Dataset evolution: California -> Swiss Set A -> Swiss Set C")
    cols = [
        ("California pilot (v1.0.0)", C_CA, ["8 events", "IRIS / EarthScope", "BHZ, 8x18 feature matrix",
                                              "Role: methods laboratory (frozen)"]),
        ("Swiss Set A (development)", C_A, ["20 events, 54 stations", "120 CH HH 3C records",
                                             "240 windows (120 P + 120 noise)", "Role: train + LOGO CV"]),
        ("Swiss Set C (evaluation)", C_C, ["15 events, 79 stations", "550 CH HHZ records",
                                            "1,100 windows (550 P + 550 noise)", "Role: independent test"]),
    ]
    for i, (t, c, lines) in enumerate(cols):
        x = 0.4 + i * 4.3
        ax.add_patch(FancyBboxPatch((x, 0.9), 3.6, 3.0, boxstyle="round,pad=0.02,rounding_size=0.15",
                                    fc="white", ec=c, lw=2.5))
        ax.text(x + 1.8, 3.55, t, ha="center", fontweight="bold", color=c, fontsize=11.5)
        for j, l in enumerate(lines):
            ax.text(x + 0.2, 3.0 - j * 0.5, "- " + l, fontsize=10)
        if i:
            arrow(ax, x - 0.65, 2.4, x - 0.05, 2.4)
    ax.text(0.4, 0.35, "Set C events are not in Set A (0 event overlap). All 54 Set A stations also occur in Set C.",
            fontsize=10, color="#a93226")
    save(fig, "fig02_dataset_evolution.png")


# 03 waveform -------------------------------------------------------------
def fig03():
    from obspy import UTCDateTime, read
    row_p = fa[(fa.is_earthquake == 1)].iloc[0]
    ev, sta = row_p.event_id, row_p.station
    row_n = fa[(fa.is_earthquake == 0) & (fa.event_id == ev) & (fa.station == sta)].iloc[0]
    files = sorted((ROOT / "data/raw/switzerland" / row_p.short_id).glob(f"CH.{sta}.*.mseed"))
    if not files:
        print("fig03 skipped: raw waveform not available locally")
        return
    st = read(str(files[0])).select(channel="HHZ")
    st.merge(method=1, fill_value=0)
    tr = st[0]
    tr.detrend("demean")
    tr.filter("bandpass", freqmin=0.1, freqmax=15.0, corners=4, zerophase=False)
    origin = UTCDateTime(row_p.origin_time_utc)
    t = tr.times("utcdatetime")
    rel = np.array([x - origin for x in t])
    mask = (rel > -60) & (rel < 60)
    fig, ax = plt.subplots(figsize=(12, 4.2))
    ax.plot(rel[mask], tr.data[mask], color="#222", lw=0.6)
    for r, lab, col in [(row_n, "noise window (class 0)", "#7f8c8d"), (row_p, "P-wave window (class 1)", C_C)]:
        s = UTCDateTime(r.window_start_utc) - origin
        e = UTCDateTime(r.window_end_utc) - origin
        ax.axvspan(s, e, color=col, alpha=0.3, label=f"{lab}: {s:+.1f} to {e:+.1f} s")
    pk = UTCDateTime(row_p.p_pick_time_utc) - origin
    ax.axvline(pk, color=C_C, ls="--", lw=1.2, label=f"SED analyst P pick ({row_p.p_phase}, {pk:+.1f} s)")
    ax.axvline(0, color="#2c3e50", ls=":", lw=1, label="catalogue origin time")
    ax.set_xlabel("Time relative to origin (s)")
    ax.set_ylabel("Amplitude (counts, bandpass 0.1-15 Hz)\n[display only]")
    ax.set_title(f"Fig. 3  Set A example: event {row_p.short_id}, station {sta}, HHZ", loc="left",
                 fontweight="bold")
    ax.legend(fontsize=8.5, loc="upper left")
    save(fig, "fig03_waveform_windows.png")


# 04 features -------------------------------------------------------------
def fig04():
    fig, ax = canvas(13, 5, "Fig. 4  Feature engineering: waveform window -> numerical features -> classifier")
    box(ax, 0.3, 2.0, 2.2, 1.6, "4 s window\nvelocity (m/s)\n0.1-15 Hz\n(zero-phase filter)", fs=10)
    groups = [
        ("Time domain (vertical)", "peak, p2p, RMS, variance, std,\nzero-crossing, energy, crest,\nkurtosis, skewness, CAV"),
        ("Frequency domain (vertical)", "dominant freq, centroid, bandwidth,\n95% rolloff, spectral entropy"),
        ("STA/LTA (window)", "sta_lta_max, sta_lta_mean\nLTA 10 s; STA 0.5 s (Set A)\nvs 1.0 s (Set C)"),
        ("3C-only (24-feature models)", "h_peak, h_rms, vec3c_peak, vec3c_rms,\nV/H ratio, SNR (dB)"),
    ]
    for i, (t, d) in enumerate(groups):
        y = 3.55 - i * 1.0
        fc = "#fdebd0" if i == 2 else ("#e8e8e8" if i == 3 else C_BOX)
        flat = textwrap.fill(d.replace("\n", " "), 62)
        box(ax, 3.4, y - 0.1, 5.2, 0.85, f"{t}\n{flat}", fc=fc, fs=7.8)
        arrow(ax, 2.55, 2.8, 3.38, y + 0.3)
    box(ax, 9.3, 2.0, 1.5, 1.6, "Feature\nvector\n18 (vertical)\n24 (3C)", fs=10)
    box(ax, 11.3, 2.0, 1.5, 1.6, "RF / XGBoost\nP-wave vs\nnoise", fc="#d5f5e3", fs=10)
    arrow(ax, 8.65, 2.8, 9.28, 2.8)
    arrow(ax, 10.85, 2.8, 11.28, 2.8)
    ax.text(0.3, 0.02, "Orange: feature computed with different STA window in Set A vs Set C (numerical impact unverified).\n"
            "Grey: excluded from the 18-feature vertical schema because Set C has HHZ only.", fontsize=9, va="bottom")
    save(fig, "fig04_feature_engineering.png")


# 05 methodology ----------------------------------------------------------
def fig05():
    fig, ax = canvas(13, 4.8, "Fig. 5  Classifier methodology (hyper-parameters from saved model artifacts)")
    box(ax, 0.3, 1.3, 3.0, 2.6, "Random Forest\n(vertical)\n\n200 trees, max depth 6\nmin_samples_split 4, leaf 2\nmax_features sqrt\nclass_weight balanced\nseed 42",
        fc="#d6eaf8", fs=10)
    box(ax, 4.4, 1.3, 3.0, 2.6, "XGBoost\n(vertical)\n\n100 trees, max depth 4\nlearning rate 0.05\nsubsample 0.8, colsample 0.8\nL1 0.1, L2 1.0\nseed 42",
        fc="#d5f5e3", fs=10)
    box(ax, 8.5, 2.55, 4.1, 1.35, "Output: P(window contains P-wave)\ndecision threshold 0.5 (fixed, not tuned)", fs=10)
    box(ax, 8.5, 1.3, 4.1, 1.0, "Baseline: sta_lta_max >= 8.0\n(window-level, STA 1.0 s / LTA 10 s)", fc="#fdebd0", fs=10)
    ax.text(3.85, 2.6, "+", fontsize=18, ha="center", va="center", fontweight="bold")
    ax.text(3.85, 1.0, "two independent models", fontsize=8.5, ha="center")
    arrow(ax, 7.45, 3.2, 8.45, 3.2)
    ax.text(0.3, 0.5, "Both trained on Set A only. Set C is never used for training, tuning or threshold choice.", fontsize=10)
    save(fig, "fig05_classifier_methodology.png")


# 06 LOGO -----------------------------------------------------------------
def fig06():
    fig, ax = canvas(13, 5, "Fig. 6  20-fold Leave-One-Group-Out cross-validation (group = earthquake event, Set A)")
    nshow = 8
    for i in range(nshow):
        y = 4.0 - i * 0.42
        for j in range(nshow):
            col = C_C if i == j else C_A
            ax.add_patch(plt.Rectangle((1.6 + j * 0.9, y), 0.82, 0.32, fc=col, ec="white"))
        ax.text(1.3, y + 0.05, f"fold {i+1}", ha="right", fontsize=8.5)
    ax.text(1.6, 4.55, "Event 1", fontsize=8.5)
    ax.text(1.6 + 7 * 0.9, 4.55, "Event 8 ...", fontsize=8.5)
    ax.text(9.2, 3.2, "... 20 folds in total\n(one per event)", fontsize=10)
    ax.add_patch(plt.Rectangle((9.2, 2.3), 0.3, 0.3, fc=C_A))
    ax.text(9.6, 2.33, "train: 19 events (all stations)", fontsize=9.5)
    ax.add_patch(plt.Rectangle((9.2, 1.8), 0.3, 0.3, fc=C_C))
    ax.text(9.6, 1.83, "held out: 1 event (all its stations)", fontsize=9.5)
    ax.text(0.3, 0.7, "All windows of one event stay together, so no event leaks between train and test folds.\n"
            "Set A CV predictions are pooled over 20 folds; Set C is a separate, later evaluation.", fontsize=10)
    save(fig, "fig06_logo_cross_validation.png")


# 07 Set A comparison -----------------------------------------------------
def fig07():
    items = [
        ("RF 24-feat\n(ML-3)", ml3["models"]["random_forest"], C_RF),
        ("XGB 24-feat\n(ML-3)", ml3["models"]["xgboost"], C_XGB),
        ("STA/LTA 8.0\n(ML-3 baseline)", ml3["models"]["sta_lta_threshold_8_0"], C_STA),
        ("RF 18-feat\n(ML-4)", sa["models"]["random_forest_vertical"], C_RF),
        ("XGB 18-feat\n(ML-4)", sa["models"]["xgboost_vertical"], C_XGB),
    ]
    mets = [("accuracy", "Accuracy"), ("recall", "Recall"), ("f1_score", "F1"), ("roc_auc", "ROC-AUC")]
    fig, ax = plt.subplots(figsize=(12, 4.8))
    wd = 0.2
    for k, (m, lab) in enumerate(mets):
        vals = [it[1][m] for it in items]
        xs = np.arange(len(items)) + (k - 1.5) * wd
        b = ax.bar(xs, vals, wd, label=lab, alpha=0.9 - 0.12 * k)
        for x, v in zip(xs, vals):
            ax.text(x, v + 0.003, f"{v:.3f}", ha="center", fontsize=7, rotation=90)
    ax.set_xticks(range(len(items)))
    ax.set_xticklabels([i[0] for i in items])
    ax.set_ylim(0.8, 1.04)
    ax.set_ylabel("Score")
    ax.legend(ncol=4, loc="lower center", fontsize=9)
    ax.set_title("Fig. 7  Set A, 20-fold LOGO cross-validation (N=240 windows)", loc="left", fontweight="bold")
    save(fig, "fig07_set_a_model_comparison.png")


# 08 Set C comparison -----------------------------------------------------
def fig08():
    m = sc["models"]
    items = [("Random Forest", m["random_forest_vertical"], C_RF), ("XGBoost", m["xgboost_vertical"], C_XGB),
             ("STA/LTA >= 8.0\n(window-level baseline)", m["sta_lta_threshold_8_0"], C_STA)]
    mets = [("accuracy", "Accuracy"), ("precision", "Precision"), ("recall", "Recall"),
            ("f1_score", "F1"), ("roc_auc", "ROC-AUC")]
    fig, ax = plt.subplots(figsize=(12, 4.8))
    wd = 0.25
    for k, (name, d, col) in enumerate(items):
        vals = [d[x] for x, _ in mets]
        xs = np.arange(len(mets)) + (k - 1) * wd
        ax.bar(xs, vals, wd, label=name.replace("\n", " "), color=col)
        for x, v in zip(xs, vals):
            ax.text(x, v + 0.01, f"{v:.3f}", ha="center", fontsize=8)
    ax.set_xticks(range(len(mets)))
    ax.set_xticklabels([l for _, l in mets])
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("Score")
    ax.legend(loc="lower left", fontsize=9)
    ax.set_title("Fig. 8  Independent Set C evaluation (N=1,100 windows, 15 unseen events)", loc="left",
                 fontweight="bold")
    save(fig, "fig08_set_c_model_comparison.png")


# 09 confusion ------------------------------------------------------------
def fig09():
    m = sc["models"]
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.4))
    for ax, (name, key) in zip(axs, [("Random Forest (18-feat)", "random_forest_vertical"),
                                    ("XGBoost (18-feat)", "xgboost_vertical")]):
        d = m[key]
        cm = np.array([[d["tn"], d["fp"]], [d["fn"], d["tp"]]])
        ax.imshow(cm, cmap="Blues", vmin=0, vmax=cm.max())
        for i in range(2):
            for j in range(2):
                ax.text(j, i, str(cm[i, j]), ha="center", va="center", fontsize=16,
                        color="white" if cm[i, j] > cm.max() / 2 else "black")
        ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
        ax.set_xticklabels(["Pred noise", "Pred P-wave"]); ax.set_yticklabels(["True noise", "True P-wave"])
        ax.set_title(f"{name}\nacc {d['accuracy']:.4f}  recall {d['recall']:.4f}", fontsize=10.5)
        for s in ax.spines.values():
            s.set_visible(True)
    fig.suptitle("Fig. 9  Set C confusion matrices (N=1,100)", x=0.02, ha="left", fontweight="bold")
    fig.tight_layout()
    save(fig, "fig09_set_c_confusion_matrices.png")


# 10 importance -----------------------------------------------------------
def fig10():
    rf, xg = sc["feature_importances_rf"], sc["feature_importances_xgb"]
    feats = sorted(rf, key=lambda k: -(rf[k] + xg[k]))[:12]
    fig, ax = plt.subplots(figsize=(11, 5.4))
    y = np.arange(len(feats))
    ax.barh(y - 0.2, [rf[f] for f in feats], 0.4, color=C_RF, label="Random Forest (Gini)")
    ax.barh(y + 0.2, [xg[f] for f in feats], 0.4, color=C_XGB, label="XGBoost (normalised gain)")
    ax.set_yticks(y); ax.set_yticklabels(feats, fontsize=9); ax.invert_yaxis()
    ax.set_xlabel("Importance (each model sums to 1; scales are not comparable across models)")
    ax.legend(loc="lower right")
    ax.set_title("Fig. 10  Feature importance (saved vertical models, trained on Set A only)", loc="left",
                 fontweight="bold")
    ax.text(0.99, 0.55, "sta_lta_* use STA 0.5 s (Set A) vs 1.0 s (Set C)\nimpact unverified", transform=ax.transAxes,
            ha="right", fontsize=8.5, color="#a93226")
    save(fig, "fig10_feature_importance.png")


# 11 independence ---------------------------------------------------------
def fig11():
    sa_s, sc_s = set(fa.station), set(fc.station)
    ev_a, ev_c = set(fa.event_id), set(fc.event_id)
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
    ax = axs[0]
    ax.bar(["Set A", "Set C"], [len(ev_a), len(ev_c)], color=[C_A, C_C])
    ax.bar(["Overlap"], [len(ev_a & ev_c)], color="#555")
    for x, v in zip(["Set A", "Set C", "Overlap"], [len(ev_a), len(ev_c), len(ev_a & ev_c)]):
        ax.text(x, v + 0.4, str(v), ha="center", fontweight="bold")
    ax.set_title("Events: no overlap (event-level independence)", fontsize=10.5)
    ax.set_ylabel("Unique events")
    ax = axs[1]
    shared, a_only, c_only = len(sa_s & sc_s), len(sa_s - sc_s), len(sc_s - sa_s)
    ax.bar(["Shared\n(A and C)", "Set A only", "Set C only"], [shared, a_only, c_only], color=["#8e44ad", C_A, C_C])
    for x, v in zip(range(3), [shared, a_only, c_only]):
        ax.text(x, v + 0.8, str(v), ha="center", fontweight="bold")
    ax.set_title(f"Stations: A={len(sa_s)}, C={len(sc_s)}; all Set A stations also in Set C", fontsize=10.5)
    ax.set_ylabel("Unique stations")
    fig.suptitle("Fig. 11  Dataset independence: 15 unseen events, but NOT unseen stations", x=0.02, ha="left",
                 fontweight="bold")
    fig.tight_layout()
    save(fig, "fig11_dataset_independence.png")


# 12 limitations/roadmap --------------------------------------------------
def fig12():
    fig, ax = canvas(13, 5.4, "Fig. 12  Limitations and future research (from project documentation)")
    ax.text(0.3, 4.6, "Limitations / disclosures", fontweight="bold", fontsize=12, color="#a93226")
    lim = [
        "Offline classifier of pre-cut 4 s windows; not a continuous real-time picker or operational EEW.",
        "Small training set: 240 windows from 20 events (Set A).",
        "Event-level independence only: all 54 Set A stations also occur in Set C.",
        "sta_lta_max/mean: STA 0.5 s (Set A) vs 1.0 s (Set C); numerical impact unverified.",
        "Threshold 8.0 derived on Set A grid; pre-declaration is documented, not provable from git history.",
        "ML-4 baseline is window-level; STEP 2K is a separate record-level detector (72.9% detected).",
        "Vertical-only: no particle-motion or V/H features. Misses concentrate on small, distant events.",
        "Zero-phase bandpass applied to full traces before windowing; P windows start at the analyst pick (not a latency test).",
    ]
    for i, t in enumerate(lim):
        ax.text(0.4, 4.15 - i * 0.34, "- " + t, fontsize=9.5)
    ax.text(0.3, 1.2, "Future work (docs/ROADMAP.md)", fontweight="bold", fontsize=12, color="#1b4f72")
    fut = [("v2.1", "Platform maintenance,\ncontent sync, deployment"),
           ("v3.0", "Europe expansion (ORFEUS/EIDA),\nstreaming (SeedLink) tests"),
           ("v3.0", "Optional EarthESND training,\ncross-region comparison")]
    for i, (v, t) in enumerate(fut):
        box(ax, 0.4 + i * 4.2, 0.1, 3.9, 0.95, f"{v}: {t}", fc="#d6eaf8", fs=9)
    save(fig, "fig12_limitations_roadmap.png")


if __name__ == "__main__":
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12):
        f()

