import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumbs } from "@/components/content/Breadcrumbs";
import { Section } from "@/components/ui/Section";
import { buildPageMetadata } from "@/lib/seo/metadata";

export const metadata: Metadata = buildPageMetadata({
  title: "Reviewer Guide",
  description: "A guided route through the AMGCR earthquake research website, datasets, methods, results, figures and reproducibility records.",
  path: "/review-guide",
});

const repo = "https://github.com/prasun-iitj/AMGCR-Earthquake-Early-Warning";

const groups = [
  {
    title: "1. Understand the project first",
    intro: "Start with the research question, scope and the distinction between the earlier California pilot and the Swiss machine-learning benchmark.",
    links: [
      ["Project overview", "/research", "Research objective, background and scope"],
      ["Research workflow", "/workflow", "How data moves from source records to candidate windows and model evaluation"],
      ["Project repository", repo, "Source code, documentation and version history"],
    ],
  },
  {
    title: "2. Inspect the datasets and processing",
    intro: "These pages explain where the data came from, how records were selected, what files were used and how features were prepared.",
    links: [
      ["Data Collection & Analysis", "/data-analysis", "USGS, EarthScope/IRIS and SED/EIDA sources; acquisition, preprocessing, Set A and Set C"],
      ["Dataset overview", "/dataset", "Dataset-level information and record summaries"],
      ["Waveform examples", "/waveforms", "Waveform visualisation and candidate-window context"],
      ["Data and model inventory", repo + "/blob/main/docs/DATA_AND_MODEL_INVENTORY.md", "Repository paths for manifests, feature matrices, saved models and results"],
      ["Data dictionary", repo + "/blob/main/docs/DATA_DICTIONARY.md", "Meaning of feature columns and metadata fields"],
    ],
  },
  {
    title: "3. Review the machine-learning results",
    intro: "The results pages show model performance, comparison charts and the independent Set C evaluation. Read the limitations alongside the metrics.",
    links: [
      ["ML Evaluation", "/ml-evaluation", "Random Forest, XGBoost, confusion matrices, feature importance and per-event results"],
      ["Results summary", "/results", "Project result highlights and comparison"],
      ["Set C evaluation report", repo + "/blob/main/docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md", "Detailed metrics and experimental protocol"],
      ["Integrity and limitations", repo + "/blob/main/FINAL_INTEGRITY_CHECK.md", "Known caveats, data checks and unresolved issues"],
    ],
  },
  {
    title: "4. Verify and reproduce the work",
    intro: "Use the source documents and committed artefacts to trace the reported results. Raw waveform files are not published in the repository.",
    links: [
      ["Resources and downloads", "/resources", "Project documents and downloadable research artefacts"],
      ["ML reproduction guide", repo + "/blob/main/docs/ML_REPRODUCTION_GUIDE.md", "Commands and steps for checking the model experiments"],
      ["Data acquisition and reproduction", repo + "/blob/main/docs/DATA_ACQUISITION_AND_REPRODUCTION.md", "How the public waveform data and metadata can be re-downloaded"],
      ["Professor handover guide", repo + "/blob/main/docs/professor_handover/PROFESSOR_HANDOVER_GUIDE.md", "Full reviewer handover, repository map and disclosures"],
      ["Review checklist", repo + "/blob/main/docs/professor_handover/PROFESSOR_REVIEW_CHECKLIST.md", "Suggested checks while reviewing the project"],
    ],
  },
];

export default function ReviewerGuidePage() {
  return (
    <>
      <section className="border-b border-border bg-primary py-12 text-white md:py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="[&_nav_a]:text-white/80 [&_nav_a:hover]:text-white [&_nav_ol]:text-white/70 [&_nav_span]:text-white">
            <Breadcrumbs items={[{ label: "Home", href: "/" }, { label: "Reviewer Guide" }]} />
          </div>
          <p className="text-sm font-semibold uppercase tracking-wider text-white/80">For faculty and project reviewers</p>
          <h1 className="mt-2 font-serif text-3xl font-semibold tracking-tight md:text-4xl">Explore the Research</h1>
          <p className="mt-4 max-w-3xl text-lg leading-relaxed text-white/85">
            A guided route through the project: what was studied, where the data came from, how it was processed,
            what the models achieved, and where the supporting evidence can be inspected.
          </p>
          <p className="mt-4 max-w-3xl text-sm leading-relaxed text-white/75">
            Research scope: offline, pre-cut P-wave candidate-window classification. The results do not establish
            continuous real-time detection or an operational earthquake early-warning system.
          </p>
        </div>
      </section>
      <Section title="Suggested review order" eyebrow="Start here" subtitle="The sequence below follows the research from its motivation to its evidence and reproducibility.">
        <div className="grid gap-5 lg:grid-cols-2">
          {groups.map((group) => (
            <article key={group.title} className="rounded-xl border border-border bg-surface-elevated p-5 shadow-sm">
              <h2 className="font-serif text-xl font-semibold text-primary">{group.title}</h2>
              <p className="mt-2 text-sm leading-relaxed text-text-muted">{group.intro}</p>
              <ul className="mt-4 space-y-3">
                {group.links.map(([label, href, detail]) => {
                  const external = href.startsWith("https://");
                  return (
                    <li key={label} className="border-t border-border pt-3">
                      <Link href={href} target={external ? "_blank" : undefined} rel={external ? "noreferrer" : undefined}
                        className="font-semibold text-primary underline-offset-4 hover:underline">
                        {label}{external ? " ↗" : " →"}
                      </Link>
                      <p className="mt-1 text-sm text-text-muted">{detail}</p>
                    </li>
                  );
                })}
              </ul>
            </article>
          ))}
        </div>
      </Section>
      <Section title="Important interpretation notes" eyebrow="Read with the results">
        <ul className="list-disc space-y-2 pl-5 text-sm leading-relaxed">
          <li>Set A contains 20 events and is used for model development; Set C contains 15 different events and is used for event-level independent evaluation.</li>
          <li>Set A and Set C share stations, so the evaluation is not station-independent.</li>
          <li>The ML-4 STA/LTA comparison is a window-level baseline and is different from the separate record-level STEP 2K detector.</li>
          <li>Raw MiniSEED, StationXML and QuakeML files are not committed to GitHub. Manifests, feature matrices, models, result files, scripts, figures and documentation are published.</li>
        </ul>
        <p className="mt-5 text-sm text-text-muted">
          Suggested route: read the project overview, then Data Collection &amp; Analysis, then ML Evaluation,
          and finally the integrity and reproduction documents.
        </p>
      </Section>
    </>
  );
}
