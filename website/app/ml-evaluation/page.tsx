import type { Metadata } from "next";
import { Breadcrumbs } from "@/components/content/Breadcrumbs";
import { ConfusionMatrix, FeatureImportance, MetricBars, PerEventTable } from "@/components/ml/MlCharts";
import { Section } from "@/components/ui/Section";
import { githubRepoUrl } from "@/lib/content/paths";
import { loadMlResults } from "@/lib/ml/loader";
import { buildPageMetadata } from "@/lib/seo/metadata";

export const metadata: Metadata = buildPageMetadata({
  title: "ML Evaluation (STEP ML-1A to ML-4)",
  description:
    "Offline window-classification benchmark: Random Forest and XGBoost trained on Swiss Set A and evaluated on independent Swiss Set C events. Results, figures, integrity disclosures and reproduction guide.",
  path: "/ml-evaluation",
});

const finalFigures: { file: string; title: string; caption: string }[] = [
  { file: "fig01_research_workflow.png", title: "Research workflow", caption: "From California pilot to the Set C test." },
  { file: "fig02_dataset_evolution.png", title: "Dataset evolution", caption: "California, Swiss Set A (development), Swiss Set C (evaluation)." },
  { file: "fig03_waveform_windows.png", title: "Waveform with windows", caption: "Real Set A trace (counts, display only) with the noise and P-wave windows." },
  { file: "fig04_feature_engineering.png", title: "Feature engineering", caption: "Waveform window to 24 / 18 features." },
  { file: "fig05_classifier_methodology.png", title: "Classifier methodology", caption: "Hyper-parameters read from the saved models." },
  { file: "fig06_logo_cross_validation.png", title: "Leave-One-Group-Out CV", caption: "Whole events held out together." },
  { file: "fig07_set_a_model_comparison.png", title: "Set A model comparison", caption: "20-fold LOGO CV, N=240." },
  { file: "fig08_set_c_model_comparison.png", title: "Set C model comparison", caption: "Independent evaluation, N=1,100." },
  { file: "fig09_set_c_confusion_matrices.png", title: "Set C confusion matrices", caption: "Random Forest and XGBoost." },
  { file: "fig10_feature_importance.png", title: "Feature importance", caption: "From saved vertical models." },
  { file: "fig11_dataset_independence.png", title: "Dataset independence", caption: "No shared events; all Set A stations also in Set C." },
  { file: "fig12_limitations_roadmap.png", title: "Limitations and roadmap", caption: "Disclosures and documented future work." },
];

const downloads: { file: string; label: string }[] = [
  { file: "RESEARCH_PACKAGE.md", label: "Research package (overview, methods, results)" },
  { file: "ML_REPRODUCTION_GUIDE.md", label: "ML reproduction guide" },
  { file: "DATA_AND_MODEL_INVENTORY.md", label: "Data and model inventory" },
  { file: "SET_C_VERTICAL_ML_EVALUATION_REPORT.md", label: "STEP ML-4 evaluation report" },
  { file: "STEP_ML4_COMPREHENSIVE_REPORT.md", label: "STEP ML-4 comprehensive report" },
  { file: "FINAL_INTEGRITY_CHECK.md", label: "Integrity check (read-only audit)" },
  { file: "vertical_set_c_evaluation_summary.json", label: "Set C results (JSON)" },
  { file: "vertical_set_a_evaluation_summary.json", label: "Set A vertical CV results (JSON)" },
  { file: "swiss_ml_evaluation_summary.json", label: "Set A 24-feature CV results (JSON)" },
  { file: "vertical_feature_schema.json", label: "18-feature schema (JSON)" },
  { file: "vertical_set_c_per_event_results.csv", label: "Set C per-event results (CSV)" },
  { file: "vertical_set_a_per_event_cv.csv", label: "Set A per-event CV (CSV)" },
];

export default function MlEvaluationPage() {
  const r = loadMlResults();
  const c = r.setC;
  const xgb = c?.models.XGBoost;
  const rf = c?.models["Random Forest"];
  const sta = c?.models["STA/LTA >= 8.0 (window-level)"];
  const redX = xgb && sta ? ((sta.fn - xgb.fn) / sta.fn) * 100 : null;
  const redR = rf && sta ? ((sta.fn - rf.fn) / sta.fn) * 100 : null;
  const o = r.overlap;

  return (
    <>
      <section className="border-b border-border bg-primary py-12 text-white md:py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="[&_nav_a]:text-white/80 [&_nav_a:hover]:text-white [&_nav_ol]:text-white/70 [&_nav_span]:text-white">
            <Breadcrumbs items={[{ label: "Home", href: "/" }, { label: "ML Evaluation" }]} />
          </div>
          <p className="text-sm font-semibold uppercase tracking-wider text-white/80">STEP ML-1A to ML-4</p>
          <h1 className="mt-2 font-serif text-3xl font-semibold tracking-tight md:text-4xl">
            Supervised P-wave window classification (Swiss Set A to Set C)
          </h1>
          <p className="mt-4 max-w-3xl text-lg leading-relaxed text-white/85">
            Random Forest and XGBoost trained on 20 Swiss events and evaluated on 15 unseen events. This is an offline
            window-classification benchmark. It is not an operational real-time early warning system.
          </p>
        </div>
      </section>

      <Section id="headline" eyebrow="Headline" title="Independent Set C result" variant="muted"
        subtitle="All numbers below are read at build time from the saved evaluation JSON in reports/ml/.">
        {c && xgb && rf && sta ? (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { l: "XGBoost F1", v: xgb.f1_score.toFixed(4), d: `AUC ${xgb.roc_auc.toFixed(4)} · FP ${xgb.fp} · FN ${xgb.fn}` },
              { l: "Random Forest F1", v: rf.f1_score.toFixed(4), d: `AUC ${rf.roc_auc.toFixed(4)} · FP ${rf.fp} · FN ${rf.fn}` },
              { l: "Window-level STA/LTA >= 8.0 F1", v: sta.f1_score.toFixed(4), d: `recall ${sta.recall.toFixed(4)} · FN ${sta.fn}` },
              { l: "Fewer missed windows", v: `${redX?.toFixed(1)}% / ${redR?.toFixed(1)}%`, d: "XGBoost / Random Forest vs the window-level baseline" },
            ].map((k) => (
              <article key={k.l} className="rounded-xl border border-border bg-surface-elevated px-6 py-5 shadow-sm">
                <p className="text-sm font-medium text-text-muted">{k.l}</p>
                <p className="mt-2 font-serif text-2xl font-semibold text-primary">{k.v}</p>
                <p className="mt-2 text-xs text-text-muted">{k.d}</p>
              </article>
            ))}
          </div>
        ) : (
          <p className="text-text-muted">Result files were not found at build time.</p>
        )}
        <p className="mt-4 text-sm text-text-muted">
          Set C: {c?.nSamples ?? "-"} windows, {c?.nEvents ?? "-"} events, {c?.nStations ?? "-"} stations. The window-level
          baseline is not the STEP 2K record-level detector (401/550 records detected, 72.9%).
        </p>
      </Section>

      <Section id="disclosures" eyebrow="Integrity" title="Disclosures a reviewer should read first">
        <ul className="grid gap-3 text-sm leading-relaxed text-text md:grid-cols-2">
          <li className="rounded-lg border border-border bg-surface p-4">
            <strong>Event-level independence only.</strong> Set A and Set C share {o?.eventOverlap ?? 0} events, but all{" "}
            {o?.setAStations ?? 54} Set A stations also occur in Set C ({o?.sharedStations ?? 54} of {o?.setCStations ?? 79} Set C
            stations are shared; {o?.setCOnlyStations ?? 25} are Set C only). Unseen stations are not claimed.
          </li>
          <li className="rounded-lg border border-border bg-surface p-4">
            <strong>STA window mismatch.</strong> <code>sta_lta_max</code> and <code>sta_lta_mean</code> use STA 0.5 s for Set A and
            STA 1.0 s for Set C (LTA 10 s in both). The numerical impact is unverified.
          </li>
          <li className="rounded-lg border border-border bg-surface p-4">
            <strong>Two different &quot;STA/LTA 8.0&quot; results.</strong> The ML-4 baseline is a window-level rule
            (<code>sta_lta_max &ge; 8.0</code>). STEP 2K is a record-level detector evaluated on all 550 records. They are not
            directly comparable.
          </li>
          <li className="rounded-lg border border-border bg-surface p-4">
            <strong>Threshold 8.0 provenance.</strong> It came from the Swiss Set A threshold grid (the California baseline was
            2.5). Documents state it was pre-declared before Set C; Git history cannot prove the order.
          </li>
          <li className="rounded-lg border border-border bg-surface p-4">
            <strong>Versions.</strong> v1.0.0 is the frozen submission release. v1.8.0 is an internal documentation milestone, not a
            software release.
          </li>
          <li className="rounded-lg border border-border bg-surface p-4">
            <strong>Filtering and window placement.</strong> The feature scripts apply a zero-phase bandpass to the full trace before
            cutting windows, so window samples are influenced by neighbouring samples (including later ones). Positive windows start
            at the analyst pick and noise windows at origin &minus; 35 s. Both sets are treated the same way; the effect is not quantified.
          </li>
          <li className="rounded-lg border border-border bg-surface p-4">
            <strong>Scope.</strong> Offline classification of pre-cut 4 s windows. No continuous picking, latency or alerting claim.
          </li>
        </ul>
      </Section>

      <Section id="figures" eyebrow="Figures" title="Research figures" variant="muted"
        subtitle="Generated by scripts/reporting/make_final_figures.py from saved results and a real Set A waveform.">
        <div className="grid gap-6 md:grid-cols-2">
          {finalFigures.map((f) => (
            <figure key={f.file} className="rounded-xl border border-border bg-surface-elevated p-3">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={`/final-figures/${f.file}`} alt={f.caption} loading="lazy" className="w-full rounded" />
              <figcaption className="mt-2 text-sm">
                <span className="font-semibold">{f.title}.</span> <span className="text-text-muted">{f.caption}</span>
              </figcaption>
            </figure>
          ))}
        </div>
      </Section>

      <Section id="set-a" eyebrow="Development" title="Set A cross-validation (N=240)">
        <div className="grid gap-10 lg:grid-cols-2">
          {r.setA24 ? (
            <div>
              <h3 className="mb-3 font-semibold">24-feature models (STEP ML-3)</h3>
              <MetricBars models={r.setA24} metrics={[{ key: "f1_score", label: "F1" }, { key: "recall", label: "Recall" }, { key: "roc_auc", label: "ROC-AUC" }]} />
            </div>
          ) : null}
          {r.setAVertical ? (
            <div>
              <h3 className="mb-3 font-semibold">18-feature vertical models (STEP ML-4)</h3>
              <MetricBars models={r.setAVertical} metrics={[{ key: "f1_score", label: "F1" }, { key: "recall", label: "Recall" }, { key: "roc_auc", label: "ROC-AUC" }]} />
            </div>
          ) : null}
        </div>
        <p className="mt-6 text-sm text-text-muted">
          Validation: 20-fold Leave-One-Group-Out, grouped by earthquake event, so every station of a held-out event is excluded
          from training.
        </p>
      </Section>

      <Section id="set-c" eyebrow="Independent evaluation" title="Set C comparison (N=1,100)" variant="muted">
        {c ? (
          <MetricBars
            models={c.models}
            metrics={[
              { key: "accuracy", label: "Accuracy" },
              { key: "precision", label: "Precision" },
              { key: "recall", label: "Recall" },
              { key: "f1_score", label: "F1" },
              { key: "roc_auc", label: "ROC-AUC" },
            ]}
          />
        ) : null}
      </Section>

      <Section id="confusion" eyebrow="Errors" title="Confusion matrices (Set C)">
        {c ? (
          <div className="grid gap-4 md:grid-cols-3">
            {Object.entries(c.models).map(([name, m]) => (
              <ConfusionMatrix key={name} title={name} m={m} />
            ))}
          </div>
        ) : null}
      </Section>

      <Section id="importance" eyebrow="Interpretation" title="Feature importance" variant="muted">
        {c ? <FeatureImportance rf={c.rf} xgb={c.xgb} /> : null}
      </Section>

      <Section id="per-event" eyebrow="Generalisation" title="Per-event Set C recall">
        <PerEventTable rows={r.perEventC} />
        <p className="mt-3 text-sm text-text-muted">
          Lowest recall occurs for the smallest events (magnitude about 2.6 to 2.7). Distance effects were not quantified in the
          saved per-event table.
        </p>
      </Section>

      <Section id="provenance" eyebrow="Provenance" title="Data, labels and reproducibility" variant="muted">
        <ul className="list-disc space-y-2 pl-5 text-sm leading-relaxed">
          <li>Swiss waveforms and StationXML from the SED/ETH FDSN service; Set A labels are 120/120 SED manual first-P picks (STEP ML-1A).</li>
          <li>Windows: 4 s; noise from origin &minus; 35 s to origin &minus; 31 s; P-wave from the analyst pick to pick + 4 s (same rule in both sets).</li>
          <li>Preprocessing: demean, linear detrend, 5% Hann taper, instrument response removed to velocity (m/s, water level 60), 0.1 to 15 Hz zero-phase bandpass (4 corners).</li>
          <li>Raw MiniSEED is not committed (data/raw is git-ignored). Re-download scripts and manifests are in the repository.</li>
          <li>
            Reproduction steps: <a className="text-accent underline" href="/ml-downloads/ML_REPRODUCTION_GUIDE.md">ML reproduction guide</a>. Inventory:{" "}
            <a className="text-accent underline" href="/ml-downloads/DATA_AND_MODEL_INVENTORY.md">data and model inventory</a>.
          </li>
          <li>
            Source code and saved models:{" "}
            <a className="text-accent underline" href={`${githubRepoUrl}/tree/main/reports/ml`}>reports/ml on GitHub</a>.
          </li>
        </ul>
      </Section>

      <Section id="downloads" eyebrow="Downloads" title="Reports and result files">
        <ul className="grid gap-2 sm:grid-cols-2">
          {downloads.map((d) => (
            <li key={d.file}>
              <a className="block rounded-lg border border-border bg-surface px-4 py-3 text-sm hover:border-accent" href={`/ml-downloads/${d.file}`} download>
                {d.label} <span className="block font-mono text-xs text-text-muted">{d.file}</span>
              </a>
            </li>
          ))}
        </ul>
      </Section>
    </>
  );
}
