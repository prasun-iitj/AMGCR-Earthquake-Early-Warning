#!/usr/bin/env python3
"""Build the certificate wrap PowerPoint (no science re-run)."""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "reports" / "Certificate_Wrap_Presentation.pptx"

NAVY = RGBColor(0x1B, 0x36, 0x5D)
GOLD = RGBColor(0xC4, 0xA3, 0x5A)
SLATE = RGBColor(0x33, 0x3A, 0x44)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MUTED = RGBColor(0x5C, 0x67, 0x73)


def _set_run_font(run, *, size=18, bold=False, color=SLATE, name="Calibri"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = name


def _bar(slide, prs):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.18))
    shape.fill.solid()
    shape.fill.fore_color.rgb = NAVY
    shape.line.fill.background()
    foot = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, prs.slide_height - Inches(0.38), prs.slide_width, Inches(0.38)
    )
    foot.fill.solid()
    foot.fill.fore_color.rgb = NAVY
    foot.line.fill.background()
    tf = foot.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = "  AMGCR  ·  Certificate wrap  ·  Not operational EEW  ·  No model trained"
    _set_run_font(run, size=11, color=WHITE)


def _title_block(slide, title: str, subtitle: str | None = None):
    box = slide.shapes.add_textbox(Inches(0.55), Inches(0.32), Inches(12.2), Inches(0.9))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title
    _set_run_font(run, size=28, bold=True, color=NAVY)
    if subtitle:
        p2 = tf.add_paragraph()
        run2 = p2.add_run()
        run2.text = subtitle
        _set_run_font(run2, size=16, color=MUTED)


def _bullets(slide, items: list[str], top=1.35, font=20):
    box = slide.shapes.add_textbox(Inches(0.7), Inches(top), Inches(12.0), Inches(5.5))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = 0
        p.space_after = Pt(10)
        run = p.add_run()
        run.text = "•  " + item
        _set_run_font(run, size=font, color=SLATE)


def _notes(slide, text: str):
    notes = slide.notes_slide.notes_text_frame
    notes.text = text


def add_title(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY
    bg.line.fill.background()
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(5.55), prs.slide_width, Inches(0.12))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = GOLD
    stripe.line.fill.background()
    t = slide.shapes.add_textbox(Inches(0.7), Inches(2.0), Inches(12.0), Inches(1.4))
    p = t.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "Reproducible AI-Assisted EEW Methods Research"
    _set_run_font(r, size=34, bold=True, color=WHITE)
    s = slide.shapes.add_textbox(Inches(0.7), Inches(3.5), Inches(12.0), Inches(1.6))
    tf = s.text_frame
    tf.word_wrap = True
    for line in (
        "California methods laboratory  ·  Swiss independent validation  ·  Honest ML close-out",
        "AMGCR certificate programme  ·  November 2026",
        "Not operational earthquake early warning  ·  No supervised model trained",
    ):
        p = tf.paragraphs[0] if line.startswith("California") else tf.add_paragraph()
        run = p.add_run()
        run.text = line
        _set_run_font(run, size=18, color=WHITE)
    _notes(
        slide,
        "Open by stating this is methods research. Do not imply a deployed EEW system or a trained neural detector.",
    )


def add_content(prs, title, bullets, notes, subtitle=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fill = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    fill.fill.solid()
    fill.fill.fore_color.rgb = WHITE
    fill.line.fill.background()
    _bar(slide, prs)
    _title_block(slide, title, subtitle)
    _bullets(slide, bullets)
    _notes(slide, notes)


def main() -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    add_title(prs)

    add_content(
        prs,
        "What this talk is",
        [
            "A completed methods chain — not a civil-protection alert product",
            "California v1.0.0: frozen methods laboratory (29 July 2026)",
            "Switzerland: methods transfer plus independent STA/LTA validation",
            "AI/ML: EarthESND as literature; supervised training audited and declined",
            "Threshold 8.0 was pre-declared and was not retuned after seeing Set C",
        ],
        "Slide 2. Repeat: independent validation, not operational EEW.",
    )
    add_content(
        prs,
        "Research design",
        [
            "Europe is the long-term programme target",
            "California IRIS/EarthScope: 8 events — method development, then freeze",
            "Swiss Set A: 20 events / 120 CH 3C records — development only",
            "Swiss Set C: 15 locked events / 550 HHZ records — independent test",
            "EarthESND (Joshi et al., 2026): architecture reference; K-NET tables not reproduced",
        ],
        "Do not mix Set A and Set C. Set C was not used to choose 8.0.",
    )
    add_content(
        prs,
        "What was built",
        [
            "ObsPy FDSN acquisition, manifests, StationXML (Swiss physical units)",
            "California chain: EDA → signal → preprocess → 8×18 feature matrix",
            "Swiss Set A: causal 0.1–15 Hz HHZ STA/LTA diagnosis",
            "Proposed configuration: STA 0.5 s, LTA 10 s, trigger ON 8.0",
            "Swiss Set C: frozen evaluation; failures and NO-DETECTION retained",
        ],
        "Interactive website (v2.0) exists but is not the scientific result.",
    )
    add_content(
        prs,
        "California pilot (frozen v1.0)",
        [
            "8 events, primarily CI.ADO BHZ — exploratory, not a regional model",
            "Feature matrix: 8 rows × 18 features (time, spectrum, onset proxies)",
            "Used to design a reproducible workflow, not to train a classifier",
            "N=8 is too small for supervised generalisation — that is a result",
            "v1.0 artefacts remain frozen; Swiss work did not rewrite them",
        ],
        "If asked about ML on California: 8 samples cannot support a detector.",
    )
    add_content(
        prs,
        "Swiss development set (Set A)",
        [
            "20 SED earthquakes, 120 complete HH 3C records, StationXML",
            "True pre-event noise (origin−60 to −10 s) — California lacked this",
            "California threshold 2.5 produces almost universal noise-window onsets",
            "A pre-declared rule selected trigger ON = 8.0 for later validation",
            "Set A was not reused as the test set",
        ],
        "8.0 is proposed from development, not proven on Set A as ‘best’.",
    )
    add_content(
        prs,
        "Frozen automatic-onset configuration",
        [
            "Causal 0.1–15 Hz HHZ after response correction to velocity (m/s)",
            "STA 0.5 s / LTA 10 s / ON 8.0 / OFF 0.5",
            "Detection search: origin → origin + 90 s (never before catalogue origin)",
            "First muted onset only; later ‘nicer’ triggers were not selected",
            "8.0 is pre-declared. It is not claimed to be optimal",
        ],
        "If challenged on 8.0: it is the reserved independent-test value, not an optimum search.",
    )
    add_content(
        prs,
        "Independent validation set (Set C)",
        [
            "Independent Swiss/Adjacent-Border Validation Set — 15 locked IDs",
            "550 CH HHZ records; same-station SED/manual first-P on every row",
            "Those picks are independent references — not ground truth",
            "Acquisition −60 to +90 s; detection starts at origin",
            "Set C was not reselected after seeing STA/LTA scores",
        ],
        "Nine of fifteen events are immediate-border; the name says so.",
    )
    add_content(
        prs,
        "STEP 2K headline results",
        [
            "550 / 550 usable records · 0 processing failures",
            "401 detections (72.9%) · 149 NO DETECTION (27.1%)",
            "Median |trigger − independent reference P| = 1.24 s",
            "381 / 401 (95.0%) at or after the independent reference P",
            "Pre-event noise-trigger rate 69 / 550 (12.5%)",
            "Misses kept — including sparse-station and weak-coverage events",
        ],
        "Quote numbers exactly. Do not upgrade them to ‘successful P picking’.",
    )
    add_content(
        prs,
        "How to read the timing comparison",
        [
            "Error = automatic onset minus same-station independent first-P",
            "Median signed error +0.88 s: the ratio detector tends to fire after P",
            "Event coverage is uneven (about 15% to 100%)",
            "Some events have large absolute errors even when a trigger exists",
            "This supports an independent onset-configuration test — not a P-picker claim",
        ],
        "STA/LTA is energy-ratio logic. Late triggers are expected, not proof of P identification.",
    )
    add_content(
        prs,
        "AI/ML in this project — three layers",
        [
            "Layer 1 — Literature: EarthESND (ESN + dendritic readout) as a benchmark idea",
            "Layer 2 — AI-assisted workflow: reproducible processing, features, validation",
            "Layer 3 — Supervised ML on Swiss tables: feasibility audit only",
            "Layer 3 decision: NO-GO. No model was trained",
            "That refusal is the ML contribution for this certificate close-out",
        ],
        "AI-assisted ≠ trained model. Say both words if asked.",
    )
    add_content(
        prs,
        "Why we did not train — the ML result",
        [
            "Set A has no independent first-P pick file",
            "STA/LTA outcome columns are the detector, not labels",
            "Set C has the independent picks — it must remain the frozen test",
            "California N=8 cannot carry a supervised detector",
            "Inventing labels to ‘add AI’ would invalidate the validation story",
        ],
        "STEP 3A. If pressed: we chose scientific integrity over a last-minute classifier.",
    )
    add_content(
        prs,
        "Leakage we refused",
        [
            "Event ID, origin time, trigger time, and CFT values as model inputs",
            "Training on Set C picks or STEP 2K detection status",
            "Random split of 120 station-rows (six stations share one earthquake)",
            "Using post-origin amplitude to predict a detection defined on that window",
            "Repeating the 9,720-row threshold grid as if it were 9,720 samples",
        ],
        "Leakage is the fastest way to get a good-looking F1 that means nothing.",
    )
    add_content(
        prs,
        "If ML is added later (not this wrap)",
        [
            "Acquire Set A same-station first-P without touching Set C",
            "Build window-level Swiss features; do not train on STA/LTA outputs",
            "Event-grouped cross-validation; L2 logistic or ridge only",
            "Freeze the model, then evaluate once on Set C",
            "Until then, do not add a network for the certificate narrative",
        ],
        "Future work is data and labels, not architecture shopping.",
    )
    add_content(
        prs,
        "Limitations (state them)",
        [
            "Not operational EEW; not a national network evaluation",
            "Small N; mixed MLh/MLhc; CH stations only",
            "Catalogue origin is not a P arrival",
            "Edge mute on 150 s traces covers origin+80 to +90 s — documented, not patched",
            "EarthESND published tables were not reproduced",
        ],
        "Limitations slide is a strength. Do not skip it.",
    )
    add_content(
        prs,
        "Close",
        [
            "Methods chain complete and frozen (California + Swiss validation)",
            "Independent test of a pre-declared STA/LTA configuration on 550 records",
            "72.9% detections, 27.1% misses, 1.24 s median absolute timing error",
            "AI/ML ending: know when not to train",
            "Thank you — questions",
        ],
        "End on integrity. Invite questions on validation numbers or the ML NO-GO.",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
