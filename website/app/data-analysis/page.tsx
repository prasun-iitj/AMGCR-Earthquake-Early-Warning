import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";
import { Breadcrumbs } from "@/components/content/Breadcrumbs";
import { Section } from "@/components/ui/Section";
import { githubRepoUrl } from "@/lib/content/paths";
import { loadDataLineage } from "@/lib/data/loader";
import { buildPageMetadata } from "@/lib/seo/metadata";

export const metadata: Metadata = buildPageMetadata({
  title: "Data Collection & Analysis",
  description:
    "The complete data journey of the AMGCR project: original sources (USGS, EarthScope/IRIS, SED/ETH), acquisition, raw files, preprocessing, Swiss Set A and Set C construction, features and analysis, with scripts, schemas and reproduction steps.",
  path: "/data-analysis",
});

const gh = (p: string) => `${githubRepoUrl}/blob/main/${p}`;

function Fig({ src, title, caption, source }: { src: string; title: string; caption: string; source: string }) {
  return (
    <figure className="rounded-xl border border-border bg-surface-elevated p-3">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={src} alt={`${title}. ${caption}`} loading="lazy" className="w-full rounded" />
      <figcaption className="mt-2 text-sm leading-relaxed">
        <span className="font-semibold">{title}.</span> <span className="text-text-muted">{caption}</span>
        <span className="mt-1 block font-mono text-xs text-text-muted">Source: {source}</span>
      </figcaption>
    </figure>
  );
}

function Table({ head, rows }: { head: string[]; rows: ReactNode[][] }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-border">
      <table className="w-full min-w-[640px] text-sm">
        <thead className="bg-surface text-left text-xs uppercase tracking-wide text-text-muted">
          <tr>{head.map((h) => <th key={h} className="px-3 py-2">{h}</th>)}</tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i} className="border-t border-border align-top">
              {r.map((c, j) => <td key={j} className="px-3 py-2">{c}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Note({ children, tone = "info" }: { children: ReactNode; tone?: "info" | "warn" }) {
  return (
    <p className={`rounded-lg border p-4 text-sm leading-relaxed ${tone === "warn" ? "border-accent/50 bg-accent/5" : "border-border bg-surface"}`}>
      {children}
    </p>
  );
}

const dl = (file: string, label: string) => (
  <li key={file}>
    <a className="block rounded-lg border border-border bg-surface px-4 py-3 text-sm hover:border-accent" href={`/data-downloads/${file}`} download>
      {label} <span className="block font-mono text-xs text-text-muted">{file}</span>
    </a>
  </li>
);

const rate = (c: Record<string, number>) => Object.entries(c).map(([k, v]) => `${Number(k).toFixed(0)} Hz (${v})`).join(", ");

export default function DataAnalysisPage() {
  const d = loadDataLineage();
  if (!d) {
    return <Section title="Data Collection & Analysis"><p>reports/data_lineage/data_lineage_summary.json was not found at build time.</p></Section>;
  }
  const { california: ca, set_a: a, set_c: c, overlap: o, schemas: s } = d;
  const f24 = s.feature_columns_24_in_set_a_matrix_order;
  const f18 = s.vertical_schema_json;

  return (
    <>
      <section className="border-b border-border bg-primary py-12 text-white md:py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="[&_nav_a]:text-white/80 [&_nav_a:hover]:text-white [&_nav_ol]:text-white/70 [&_nav_span]:text-white">
            <Breadcrumbs items={[{ label: "Home", href: "/" }, { label: "Data Collection & Analysis" }]} />
          </div>
          <p className="text-sm font-semibold uppercase tracking-wider text-white/80">Data journey</p>
          <h1 className="mt-2 font-serif text-3xl font-semibold tracking-tight md:text-4xl">Data Collection &amp; Analysis</h1>
          <p className="mt-4 max-w-3xl text-lg leading-relaxed text-white/85">
            Original seismic source &rarr; acquisition &rarr; raw waveform and metadata &rarr; validation &rarr; preprocessing &rarr; manual P-wave annotation &rarr;
            Swiss Set A and Set C &rarr; candidate windows &rarr; features &rarr; machine-learning analysis &rarr; independent evaluation.
          </p>
          <nav aria-label="On this page" className="mt-6 flex flex-wrap gap-2 text-xs">
            {[["overview", "Overview"], ["sources", "Sources"], ["acquisition", "Acquisition"], ["raw", "Raw data"], ["preprocessing", "Preprocessing"], ["set-a", "Set A"], ["set-c", "Set C"], ["california", "California"], ["features", "Features"], ["analysis", "Analysis"], ["comparison", "Comparison"], ["integrity", "Integrity"], ["reproduce", "Reproduce"]].map(([id, l]) => (
              <a key={id} href={`#${id}`} className="rounded-full border border-white/30 px-3 py-1 hover:bg-white/10">{l}</a>
            ))}
          </nav>
        </div>
      </section>

      <Section id="overview" eyebrow="1" title="Research data overview" variant="muted"
        subtitle="Three separate research stages with different sources and purposes. Their results are never merged.">
        <Table head={["Stage", "Provider", "Events", "Records", "Stations", "Channels", "P labels", "Role"]} rows={[
          ["California pilot (v1.0.0, frozen)", "USGS events, EarthScope waveforms", ca.events, ca.waveform_files_in_manifest, ca.stations_in_manifest.length, "CI BHZ", "automatic STA/LTA (no analyst picks)", "workflow development"],
          ["Swiss Set A", "SED / ETH (EIDA)", a.events, a.records, a.stations, "CH HHZ+HHN+HHE", `${a.picks.n} manual first-P`, "development, training, CV"],
          ["Swiss Set C", "SED / ETH (EIDA)", c.events, c.records, c.stations, "CH HHZ only", `${c.picks.n} manual first-P`, "independent evaluation"],
        ]} />
        <div className="mt-8 grid gap-6 lg:grid-cols-2">
          <Fig src="/data-figures/dfig01_source_to_dataset_lineage.png" title="Source-to-dataset lineage" caption="Blue-grey: downloaded; orange: SED analyst annotation; green: derived by project code." source="manifests and scripts" />
          <Fig src="/final-figures/fig02_dataset_evolution.png" title="Dataset evolution" caption="California, Set A (development), Set C (evaluation)." source="reports/figures/final/fig02" />
        </div>
        <Note>
          Scope: an offline P-wave versus ambient-noise window-classification research benchmark. It is not an operational real-time
          early-warning system. California v1.0.0 is the frozen submission release; v1.8.0 is an internal documentation milestone.
        </Note>
      </Section>

      <Section id="sources" eyebrow="2" title="Original data sources">
        <Table head={["Source", "Data supplied", "Purpose", "Acquisition method", "Reference"]} rows={[
          ["USGS FDSN event service", "California event origin, location, magnitude", "pilot event list", "ObsPy Client(\"https://earthquake.usgs.gov\").get_events", <a key="u" className="text-accent underline" href="https://earthquake.usgs.gov/fdsnws/event/1/">usgs.gov</a>],
          ["EarthScope (formerly IRIS) dataselect", "California BHZ MiniSEED", "pilot waveforms", "Client(\"EARTHSCOPE\").get_waveforms (service.earthscope.org)", <a key="e" className="text-accent underline" href="https://www.earthscope.org/data/">earthscope.org</a>],
          ["Swiss Seismological Service (SED, ETH) via EIDA", "Swiss catalogue, MiniSEED, StationXML, QuakeML arrivals (analyst picks)", "Set A and Set C", "FDSN event, dataselect, station and availability services at eida.ethz.ch", <a key="s" className="text-accent underline" href="https://eida.ethz.ch/">eida.ethz.ch</a>],
        ]} />
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <Note><strong>IRIS/EarthScope supplied waveforms only.</strong> California events came from USGS; P-wave arrivals were produced by the project&apos;s STA/LTA trigger (0.5 s / 10 s, threshold 2.5). No analyst picks and no StationXML were obtained, so California amplitudes remain in digital counts.</Note>
          <Note><strong>SED supplied everything Swiss:</strong> events, waveforms, instrument response (StationXML) and the manual first-P picks. Waveforms and picks are distinct: the picks are analyst annotations delivered in QuakeML, not part of the MiniSEED.</Note>
        </div>
        <div className="mt-6"><Fig src="/data-figures/dfig02_iris_vs_sed_sources.png" title="IRIS/USGS vs SED sources" caption="What each provider supplied." source="scripts/download/*.py, configs/*.yaml" /></div>
        <p className="mt-4 text-sm text-text-muted">Provider licence and citation terms were not reviewed in the repository. Check them before redistributing any raw data.</p>
      </Section>

      <Section id="acquisition" eyebrow="3" title="Data acquisition journey" variant="muted">
        <div className="grid gap-6 lg:grid-cols-3">
          <article className="rounded-xl border border-border bg-surface-elevated p-5 text-sm leading-relaxed">
            <h3 className="font-semibold">California (2026-07-29 run)</h3>
            <ol className="mt-2 list-decimal space-y-1 pl-5">
              <li>USGS query 2024, California box, M 4.0 to 7.5: 41 matches.</li>
              <li>Scan in time order until 8 events return waveform data.</li>
              <li>Predefined broadband sites ranked by distance; 1 station per event (CI.ADO, CI.USC).</li>
              <li>EarthScope BHZ, 300 s from origin, 40 Hz.</li>
            </ol>
            <p className="mt-2"><a className="text-accent underline" href={gh("scripts/download/download_iris_california_pilot.py")}>download_iris_california_pilot.py</a></p>
          </article>
          <article className="rounded-xl border border-border bg-surface-elevated p-5 text-sm leading-relaxed">
            <h3 className="font-semibold">Swiss Set A (2026-09-06)</h3>
            <ol className="mt-2 list-decimal space-y-1 pl-5">
              <li>20 fixed event IDs, re-resolved in the live SED catalogue (M &ge; 2.5, 2020 to 2026).</li>
              <li>Availability query; prefer complete HH three-component stations.</li>
              <li>Up to 6 stations per event from distance bins (0 to 400 km): 120 records, 54 stations.</li>
              <li>MiniSEED origin &minus;90 s to +210 s; StationXML (level=response); checked for &ge; 60 s before and after origin.</li>
              <li>Manual P picks from SED QuakeML (<code>includearrivals=true</code>), matched per station: 120/120.</li>
            </ol>
            <p className="mt-2"><a className="text-accent underline" href={gh("scripts/download/download_sed_switzerland_pilot.py")}>pilot</a> &middot; <a className="text-accent underline" href={gh("scripts/download/download_sed_switzerland_set_a_picks.py")}>picks</a> &middot; <a className="text-accent underline" href={gh("configs/sed_switzerland_pilot.yaml")}>config</a></p>
          </article>
          <article className="rounded-xl border border-border bg-surface-elevated p-5 text-sm leading-relaxed">
            <h3 className="font-semibold">Swiss Set C (2026-09-11)</h3>
            <ol className="mt-2 list-decimal space-y-1 pl-5">
              <li>Catalogue pool: 251 rows, 24 excluded, {c.candidate_pool.rows} independent earthquakes (none in Set A).</li>
              <li>15 events locked by diversity rules (year quotas, 15 km separation, magnitude bins, &ge; 6 Swiss territory), not by detector performance.</li>
              <li>Every station with a same-station first-P pick and an HHZ record: {c.records} records.</li>
              <li>MiniSEED origin &minus;60 s to +90 s; StationXML verified {c.stationxml_status.verified}/{c.records}; picks via full SED resource ID.</li>
            </ol>
            <p className="mt-2"><a className="text-accent underline" href={gh("scripts/download/download_sed_switzerland_validation.py")}>download</a> &middot; <a className="text-accent underline" href={gh("scripts/audit/audit_swiss_validation_candidates.py")}>candidate audit</a> &middot; <a className="text-accent underline" href={gh("configs/sed_switzerland_validation_audit.yaml")}>config</a></p>
          </article>
        </div>
      </Section>

      <Section id="raw" eyebrow="4" title="Raw data inventory"
        subtitle={`Counts come from reports/data_lineage/data_lineage_summary.json, generated ${d.generated_at_utc.slice(0, 10)} by scripts/reporting/audit_data_lineage.py from the manifests, matrices and local folders.`}>
        <Table head={["Item", "California", "Set A", "Set C"]} rows={[
          ["Events", ca.events, a.events, c.events],
          ["Records (waveform files)", `${ca.waveform_files_in_manifest} (manifest)`, a.records, c.records],
          ["Stations", ca.stations_in_manifest.join(", "), a.stations, c.stations],
          ["Channels", "BHZ", "HHZ, HHN, HHE (one file)", "HHZ"],
          ["Sampling rate", "40 Hz", rate(a.sampling_rates_hz), rate(c.sampling_rates_hz)],
          ["Magnitude range", ca.magnitude_range.join(" to "), `${a.magnitude_range.join(" to ")} (MLh/MLhc)`, `${c.magnitude_range.join(" to ")}`],
          ["Manual picks", "none", `${a.picks.n} (Pg ${a.picks.phases.Pg}, P1 ${a.picks.phases.P1}, Pn ${a.picks.phases.Pn})`, `${c.picks.n} (Pg ${c.picks.phases.Pg}, P1 ${c.picks.phases.P1}, Pn ${c.picks.phases.Pn})`],
          ["StationXML", "none saved", `${a.stationxml_available.YES}/${a.records}`, `${c.stationxml_status.verified}/${c.records}`],
          ["MiniSEED files on local disk", ca.local_raw_mseed_files ?? "n/a", a.local_raw_mseed_files ?? "n/a", c.local_raw_mseed_files ?? "n/a"],
          ["Raw files on GitHub", "no", "no", "no"],
        ]} />
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <Table head={["Availability class", "Content"]} rows={[
            ["A. Local raw files", "All MiniSEED, StationXML and QuakeML listed above"],
            ["B. Local, excluded from GitHub", "Same files (.gitignore: data/raw, data/metadata XML): size and provider terms"],
            ["C. Published on GitHub", "Manifests, feature matrices, models, JSON/CSV results, scripts, figures, documents"],
            ["D. External only", "USGS, EarthScope, SED/ETH archives"],
            ["E. Reconstructable by script", "All raw data via the three download scripts"],
          ]} />
          <Fig src="/data-figures/dfig03_raw_data_structure.png" title="Actual raw-data structure" caption="Local folder names, file patterns and counts." source="filesystem audit, data_lineage_summary.json" />
        </div>
        <Note>
          GitHub does not contain waveforms. A reviewer must re-download them to re-run feature extraction. California: {ca.local_raw_files_not_in_manifest?.length ?? 0} extra local
          MiniSEED files are not listed in the manifest; the repository does not explain them, and the manifest&apos;s 8 files define the pilot.
        </Note>
        <div className="mt-6 grid gap-4 md:grid-cols-2 text-sm leading-relaxed">
          <Note><strong>MiniSEED</strong> stores waveform samples as digital counts, with a network.station.location.channel code (e.g. CH.EMBD..HHZ), a start time and a sampling rate. Channel code HH = broadband; last letter Z/N/E = vertical/north/east.</Note>
          <Note><strong>StationXML</strong> holds station coordinates, channel orientation and the instrument response. It is required to convert counts to ground velocity (m/s). <strong>QuakeML</strong> (SED event files) carries origins, magnitudes and analyst picks; a <strong>pick</strong> is the analyst&apos;s first-P arrival time at one station.</Note>
        </div>
      </Section>

      <Section id="preprocessing" eyebrow="5" title="Preprocessing: raw waveform to research record" variant="muted"
        subtitle="Swiss feature scripts: run_swiss_set_a_feature_engineering.py and run_swiss_set_c_feature_engineering.py.">
        <Table head={["#", "Stage", "Operation and parameters", "Output"]} rows={[
          [1, "Read and validate", "MiniSEED + StationXML + pick; skip and log a failure if missing; Set C merges fragmented traces", "ObsPy stream (counts)"],
          [2, "Clean", "demean, linear detrend, 5% Hann taper", "stream"],
          [3, "Response correction", "remove_response, output VEL, water level 60, cosine pre-filter", "velocity, m/s"],
          [4, "Filter", "bandpass 0.1 to 15 Hz, 4 corners, zero-phase, applied to the full trace", "filtered velocity"],
          [5, "Components", "Set A: Z, N, E. Set C: Z only", "arrays"],
          [6, "STA/LTA trace", "classic_sta_lta on filtered Z; LTA 10 s; STA 0.5 s (A) or 1.0 s (C)", "characteristic function"],
          [7, "P-pick alignment and windows", "positive: pick to pick+4 s. negative: origin-35 s to origin-31 s", "2 windows per record"],
          [8, "Labels", "is_earthquake 1 / 0", "label"],
          [9, "Features", "24 (A) or 18 (C) numbers per window", "feature matrix CSV"],
        ]} />
        <div className="mt-8 grid gap-6 lg:grid-cols-2">
          <Fig src="/data-figures/dfig04_preprocessing_pipeline.png" title="Preprocessing pipeline" caption="Step 4 (orange) runs on the full trace before windows are cut." source="the two feature scripts" />
          <Fig src="/data-figures/dfig05_filtering_before_after.png" title="Before and after (real record)" caption="Set A event 2020btnrcj, CH.EMBD HHZ: counts, velocity, filtered velocity. Grey: noise window; red: P window. The documented steps were applied to this one record for display." source="data/raw/switzerland/2020btnrcj, data/metadata/switzerland/2020btnrcj (local)" />
          <Fig src="/final-figures/fig03_waveform_windows.png" title="Positive and negative windows" caption="Real Set A trace (counts, display only) with the analyst pick." source="Set A feature matrix, raw MiniSEED" />
          <Fig src="/data-figures/dfig06_three_component_vs_vertical.png" title="Three components vs vertical only" caption="Set A has Z, N and E; Set C was acquired with HHZ only." source="real Set A and Set C records (local)" />
        </div>
        <div className="mt-6 grid gap-3 md:grid-cols-2 text-sm leading-relaxed">
          <Note tone="warn"><strong>Filtering disclosure.</strong> &quot;Causal windows&quot; refers to window placement only. The zero-phase bandpass is applied to the full trace before windowing, so window samples depend on neighbouring (including later) samples. The effect is not quantified, and this pipeline must not be described as suitable for real-time operation.</Note>
          <Note tone="warn"><strong>Not identical between sets.</strong> STA window 0.5 s (Set A) vs 1.0 s (Set C) changes <code>sta_lta_max/mean</code>; the response pre-filter corners also differ (Set A 0.75/0.85 Nyquist; Set C min(18 Hz, 0.75 Nyquist) / min(22.5 Hz, 0.85 Nyquist)). The numerical impact of both is unverified.</Note>
        </div>
      </Section>

      <Section id="set-a" eyebrow="6" title="Swiss Set A (development)">
        <div className="grid gap-4 md:grid-cols-4">
          {[["Events", a.events], ["Records", a.records], ["Stations", a.stations], ["Windows", `${a.windows.total} (${a.windows.positive}+${a.windows.negative})`]].map(([l, v]) => (
            <article key={String(l)} className="rounded-xl border border-border bg-surface-elevated px-5 py-4"><p className="text-sm text-text-muted">{l}</p><p className="mt-1 font-serif text-2xl font-semibold text-primary">{v}</p></article>
          ))}
        </div>
        <ul className="mt-6 list-disc space-y-2 pl-5 text-sm leading-relaxed">
          <li><strong>Why:</strong> transfer the California workflow to European data, obtain independent analyst labels and train supervised models.</li>
          <li><strong>Records:</strong> 20 events x 6 stations = 120 three-component HH files; epicentral distance {a.epicentral_distance_km_range.join(" to ")} km; magnitude {a.magnitude_range.join(" to ")}; sampling {rate(a.sampling_rates_hz)}.</li>
          <li><strong>Labels:</strong> {a.picks.n} manual SED first-P picks; pick time after origin {a.p_latency_s_range.join(" to ")} s.</li>
          <li><strong>Windows:</strong> {a.windows.positive} positive and {a.windows.negative} negative, 4 s each; one pair per record.</li>
          <li><strong>Use:</strong> Random Forest and XGBoost with 20-fold Leave-One-Group-Out CV grouped by earthquake event.</li>
          <li><strong>The 240 windows are not 240 independent earthquakes:</strong> they come from 20 events.</li>
        </ul>
        <div className="mt-6"><Table head={["Event", "Region", "Magnitude", "Records", "Stations"]} rows={a.events_table.map((e) => [<code key={e.short_id}>{e.short_id}</code>, e.region, e.magnitude, e.records, e.stations])} /></div>
      </Section>

      <Section id="set-c" eyebrow="7" title="Swiss Set C (independent evaluation)" variant="muted">
        <div className="grid gap-4 md:grid-cols-4">
          {[["Events", c.events], ["Records (HHZ)", c.records], ["Stations", c.stations], ["Windows", `${c.windows.total} (${c.windows.positive}+${c.windows.negative})`]].map(([l, v]) => (
            <article key={String(l)} className="rounded-xl border border-border bg-surface-elevated px-5 py-4"><p className="text-sm text-text-muted">{l}</p><p className="mt-1 font-serif text-2xl font-semibold text-primary">{v}</p></article>
          ))}
        </div>
        <ul className="mt-6 list-disc space-y-2 pl-5 text-sm leading-relaxed">
          <li><strong>Why:</strong> events not used for development, to test the frozen Set A-trained models.</li>
          <li><strong>HHZ only:</strong> the acquisition rule downloaded the vertical channel; horizontals were not requested, so the six three-component-dependent features cannot be computed. Models use the 18 vertical features.</li>
          <li><strong>Records:</strong> {c.location_class_records.swiss_territory} from Swiss-territory events and {c.location_class_records.immediate_border} from immediate-border events (9 of 15 events are border events). {c.records} records, 3 to 62 per event.</li>
          <li><strong>Validation:</strong> download {c.download_status.ok}/{c.records}, verification {c.verification_status.PASS}/{c.records}, coverage full {c.coverage_status.full}/{c.records}, gaps {c.gaps_total}, overlaps {c.overlaps_total}; {c.picks.n} manual picks (Pg {c.picks.phases.Pg}, P1 {c.picks.phases.P1}, Pn {c.picks.phases.Pn}).</li>
          <li><strong>Evaluation:</strong> frozen vertical Random Forest and XGBoost applied once, decision threshold 0.5, no Set C tuning.</li>
        </ul>
        <Note tone="warn">
          <strong>Independence is event-level.</strong> Set A and Set C share {o.event_overlap} events: 15 unseen events. But all {o.stations_set_a} Set A stations also occur in Set C ({o.stations_shared} of {o.stations_set_c} Set C stations are shared; {o.stations_set_c_only} are Set C only; {o.set_c_records_at_shared_stations} of {c.records} Set C records come from shared stations). Unseen stations are not claimed.
        </Note>
        <div className="mt-6 grid gap-6 lg:grid-cols-2">
          <Fig src="/final-figures/fig11_dataset_independence.png" title="Event and station overlap" caption="No shared events; every Set A station is also in Set C." source="swiss_set_{a,c}_feature_matrix.csv" />
          <Fig src="/data-figures/dfig07_set_a_vs_set_c_comparison.png" title="Set A vs Set C" caption="Counts on a log scale; windows are not independent events." source="data_lineage_summary.json" />
        </div>
        <div className="mt-6"><Table head={["Event", "Region", "Class", "Magnitude", "Records"]} rows={c.events_table.map((e) => [<code key={e.short_id}>{e.short_id}</code>, e.region, e.location_class, e.magnitude, e.records])} /></div>
      </Section>

      <Section id="california" eyebrow="8" title="California pilot (original stage, frozen v1.0.0)">
        <ul className="list-disc space-y-2 pl-5 text-sm leading-relaxed">
          <li>8 events, 2024-05-01 to 2024-10-25, magnitude {ca.magnitude_range.join(" to ")}, one BHZ station per event ({ca.stations_in_manifest.join(", ")}), 300 s from origin, 40 Hz. Events from USGS, waveforms from EarthScope.</li>
          <li>P onset from the project&apos;s STA/LTA trigger (0.5 s / 10 s, threshold 2.5), not from analyst picks. Response removal was not applied (StationXML fetch failed in the run), so amplitudes are in counts.</li>
          <li>8 x 18 feature matrix, EDA, signal analysis and preprocessing figures, the final report and the FINAL_SUBMISSION package. It developed the workflow later applied to Switzerland. It is preserved unchanged and its metrics are not combined with the Swiss results.</li>
        </ul>
      </Section>

      <Section id="features" eyebrow="9" title="Feature engineering" variant="muted"
        subtitle="A feature is a number computed from a waveform window. Classifiers need fixed-length numeric vectors, so each 4 s window is summarised by amplitude, energy, shape and frequency statistics.">
        <div className="grid gap-6 lg:grid-cols-2">
          <Fig src="/final-figures/fig04_feature_engineering.png" title="Feature pipeline" caption="Window to feature groups to classifier." source="feature scripts" />
          <Fig src="/data-figures/dfig08_feature_matrix_structure.png" title="Feature-matrix structure" caption="Metadata/label columns and feature columns of the two committed matrices." source="reports/features/swiss_set_{a,c}_feature_matrix.csv" />
        </div>
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <div>
            <h3 className="mb-2 font-semibold">24-feature schema (Set A, STEP ML-3), saved-model order</h3>
            <ol className="columns-1 space-y-0.5 pl-5 font-mono text-xs sm:columns-2" start={1}>{f24.map((f) => <li key={f} className="list-decimal">{f}</li>)}</ol>
          </div>
          <div>
            <h3 className="mb-2 font-semibold">18-feature vertical schema (Set A training, Set C evaluation)</h3>
            <ol className="columns-1 space-y-0.5 pl-5 font-mono text-xs sm:columns-2">{f18.map((f) => <li key={f} className="list-decimal">{f}</li>)}</ol>
            <p className="mt-3 text-sm text-text-muted">
              Verified: schema JSON, source constant, both saved vertical models and Set C inference share these {s.n_18} names in this order ({String(s.vertical_schema_matches_vertical_models)}). NaN values in feature columns: Set A {s.nan_counts.set_a_features}, Set C {s.nan_counts.set_c_features}.
            </p>
          </div>
        </div>
        <Table head={["Group", "Features", "Unit"]} rows={[
          ["Amplitude", "z_peak_velocity, z_p2p_amplitude, z_rms_velocity, z_cav", "m/s (z_cav is sum|v|*dt, dimensionally a length; name kept as in the schema)"],
          ["Energy", "z_variance, z_std, z_signal_energy", "m^2/s^2, m/s, m^2/s"],
          ["Shape", "z_crest_factor, z_kurtosis, z_skewness, z_zero_crossing_rate", "unitless, Hz"],
          ["Frequency", "z_dominant_frequency, z_spectral_centroid, z_spectral_bandwidth, z_spectral_rolloff_95, z_spectral_entropy", "Hz, bits"],
          ["STA/LTA", "sta_lta_max, sta_lta_mean (STA 0.5 s Set A, 1.0 s Set C)", "ratio"],
          ["Three-component only (Set A)", "h_peak, h_rms, vec3c_peak, vec3c_rms, vh_ratio, snr_db", "m/s, unitless, dB"],
        ]} />
        <p className="mt-3 text-sm"><a className="text-accent underline" href="/data-downloads/DATA_DICTIONARY.md">Full data dictionary</a> with definitions from the code, units and availability.</p>
      </Section>

      <Section id="analysis" eyebrow="10" title="How the data were analysed">
        <ol className="list-decimal space-y-3 pl-5 text-sm leading-relaxed">
          <li><strong>Validation.</strong> Manifest status, time coverage, StationXML, picks, finite feature values.</li>
          <li><strong>Candidate windows.</strong> One P-wave and one noise window per record.</li>
          <li><strong>Features.</strong> Section 9.</li>
          <li><strong>Training and cross-validation.</strong> Random Forest (200 trees, depth 6) and XGBoost (100 trees, depth 4). 20-fold Leave-One-Group-Out, one earthquake held out per fold. Grouping matters because windows from one event are correlated and an ungrouped split would overstate accuracy.</li>
          <li><strong>Independent evaluation.</strong> Models fitted on Set A, frozen, applied to Set C.</li>
          <li><strong>Baseline.</strong> The ML-4 baseline is a <em>window-level</em> rule (<code>sta_lta_max &ge; 8.0</code>, STA 1.0 s). The STEP 2K detector is <em>record-level</em> (STA 0.5 s / LTA 10 s, first trigger in origin to +90 s; 401/550 records detected, 72.9%). They are different procedures and are not interchangeable. Threshold 8.0 was derived from the Swiss Set A grid, not from California (2.5); documents state it was pre-declared, but Git history cannot independently prove the order.</li>
          <li><strong>Interpretation.</strong> Positive = P-wave window. Precision: flagged windows that are P-wave. Recall: P-wave windows found. F1: harmonic mean. ROC-AUC: ranking quality over all thresholds. A false positive is a noise window flagged; a false negative is a missed P-wave window.</li>
        </ol>
        <div className="mt-6 grid gap-6 lg:grid-cols-2">
          <Fig src="/final-figures/fig06_logo_cross_validation.png" title="Leave-One-Group-Out" caption="All windows of an event stay together." source="reports/figures/final/fig06" />
          <Fig src="/data-figures/dfig09_quality_control_summary.png" title="Quality-control summary" caption="Checks on manifests, picks and feature matrices." source="manifests, matrices" />
        </div>
        <p className="mt-4 text-sm">Results, confusion matrices and importances: <Link className="text-accent underline" href="/ml-evaluation">ML Evaluation</Link>. These show discrimination of pre-cut windows, not detection latency or operational alerting.</p>
      </Section>

      <Section id="comparison" eyebrow="11" title="Dataset comparison" variant="muted">
        <Table head={["Property", "California", "Set A", "Set C"]} rows={[
          ["Provider", "USGS + EarthScope", "SED/ETH", "SED/ETH"],
          ["Events / records / stations", `${ca.events} / ${ca.waveform_files_in_manifest} / ${ca.stations_in_manifest.length}`, `${a.events} / ${a.records} / ${a.stations}`, `${c.events} / ${c.records} / ${c.stations}`],
          ["Channels", "BHZ", "HHZ+HHN+HHE", "HHZ"],
          ["Acquisition window", "origin to +300 s", "origin -90 to +210 s", "origin -60 to +90 s"],
          ["Station rule", "distance-ranked predefined list, 1 per event", "distance bins, up to 6 per event", "all same-station pick and HHZ pairs"],
          ["Response corrected", "no (counts)", "yes (m/s)", "yes (m/s)"],
          ["P labels", "STA/LTA trigger (2.5)", `${a.picks.n} manual`, `${c.picks.n} manual`],
          ["Windows", "none", a.windows.total, c.windows.total],
          ["Features", "18 (counts)", 24, 18],
          ["Role", "frozen v1.0.0", "development", "independent evaluation"],
        ]} />
      </Section>

      <Section id="integrity" eyebrow="12" title="Data integrity and limitations">
        <ul className="grid gap-3 text-sm leading-relaxed md:grid-cols-2">
          {[
            "Event-level independence only: all 54 Set A stations also occur in Set C.",
            "Set A is three-component; Set C is HHZ only.",
            "STA window differs (0.5 s vs 1.0 s) in sta_lta_max/mean; numerical impact unverified.",
            "Response pre-filter corners differ between the two feature scripts; impact unverified.",
            "Zero-phase bandpass is applied to full traces before windowing; effect on real-time applicability unquantified.",
            "Windows are not independent events (240 from 20 events; 1,100 from 15).",
            "No explicit check that the origin -35 s noise windows are free of other seismic energy.",
            "Set A stations are not a complete network snapshot (availability timeouts); Set C is border-heavy (9 of 15 events).",
            "Mixed sampling rates (200, 120, 100 Hz); SED magnitudes are MLh/MLhc, not comparable with California ml/mw.",
            "Reasons for choosing the original 20 Set A events, and the exact ranking steps for the final 15 Set C IDs, are not documented beyond the configs.",
            "Provider licence terms not reviewed; raw data are not redistributed.",
            "Offline benchmark, not an operational early-warning system.",
          ].map((t) => <li key={t} className="rounded-lg border border-border bg-surface p-4">{t}</li>)}
        </ul>
        <p className="mt-4 text-sm"><a className="text-accent underline" href="/data-downloads/FINAL_INTEGRITY_CHECK.md">Integrity check</a></p>
      </Section>

      <Section id="reproduce" eyebrow="13" title="Reproducibility and downloads" variant="muted"
        subtitle="Only published, redistributable files are linked. Raw waveforms must be re-acquired with the scripts.">
        <ol className="mb-6 list-decimal space-y-1 pl-5 text-sm">
          <li><code>python scripts/download/download_sed_switzerland_pilot.py --config configs/sed_switzerland_pilot.yaml</code></li>
          <li><code>python scripts/download/download_sed_switzerland_set_a_picks.py</code></li>
          <li><code>python scripts/download/download_sed_switzerland_validation.py --config configs/sed_switzerland_validation_acquisition.yaml</code></li>
          <li><code>python scripts/analysis/run_swiss_set_a_feature_engineering.py</code> and <code>run_swiss_set_c_feature_engineering.py</code></li>
        </ol>
        <p className="mb-4 text-sm text-text-muted">These commands overwrite committed manifests and matrices; use a separate clone. Details and expected outputs are in the reproduction guide.</p>
        <ul className="grid gap-2 sm:grid-cols-2">
          {[
            ["DATA_COLLECTION_AND_ANALYSIS_REPORT.md", "Main data report"],
            ["DATA_DICTIONARY.md", "Data dictionary"],
            ["DATA_ACQUISITION_AND_REPRODUCTION.md", "Acquisition and reproduction guide"],
            ["DATA_AND_MODEL_INVENTORY.md", "Data and model inventory"],
            ["RESEARCH_PACKAGE.md", "Research package"],
            ["ML_REPRODUCTION_GUIDE.md", "ML reproduction guide"],
            ["data_lineage_summary.json", "Verified lineage counts (JSON)"],
            ["vertical_feature_schema.json", "18-feature schema (JSON)"],
            ["iris_california_pilot_events.csv", "California manifest"],
            ["sed_switzerland_pilot_events.csv", "Set A record manifest"],
            ["sed_switzerland_set_a_picks.csv", "Set A manual picks"],
            ["sed_switzerland_validation_candidates.csv", "Set C candidate pool"],
            ["sed_switzerland_validation_waveforms.csv", "Set C record manifest"],
            ["sed_switzerland_validation_picks.csv", "Set C manual picks"],
            ["swiss_set_a_feature_matrix.csv", "Set A feature matrix (240 x 45)"],
            ["swiss_set_c_feature_matrix.csv", "Set C feature matrix (1,100 x 35)"],
          ].map(([f, l]) => dl(f, l))}
        </ul>
        <p className="mt-4 text-sm">Scripts and configs: <a className="text-accent underline" href={`${githubRepoUrl}/tree/main/scripts`}>scripts/</a>, <a className="text-accent underline" href={`${githubRepoUrl}/tree/main/configs`}>configs/</a>. Also read the <Link className="text-accent underline" href="/docs/data-collection-and-analysis-report">main report</Link> in the documentation portal.</p>
      </Section>
    </>
  );
}

