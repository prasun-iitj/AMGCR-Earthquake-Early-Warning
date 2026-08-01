"use client";

import Link from "next/link";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import type { WaveformRecord } from "@/lib/waveforms/types";

type WaveformDetailsPanelProps = {
  waveform: WaveformRecord;
};

function formatOriginTime(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toISOString().replace("T", " ").slice(0, 19);
}

export function WaveformDetailsPanel({ waveform }: WaveformDetailsPanelProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <AnimatePresence mode="wait">
      <motion.aside
        key={waveform.id}
        initial={shouldReduceMotion ? false : { opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={shouldReduceMotion ? undefined : { opacity: 0, y: -8 }}
        transition={{ duration: 0.22 }}
        className="space-y-8"
        aria-label="Waveform details"
      >
        <div className="rounded-xl border border-border bg-surface p-6">
          <h3 className="font-serif text-xl font-semibold text-text">
            Event metadata
          </h3>
          <dl className="mt-4 space-y-3 text-sm">
            <DetailItem label="Event ID" value={waveform.id} mono />
            <DetailItem label="Full event ID" value={waveform.eventId} mono />
            <DetailItem label="Station" value={waveform.stationId} />
            <DetailItem
              label="Magnitude"
              value={`${waveform.magnitude} (${waveform.magnitudeType})`}
            />
            <DetailItem
              label="Origin time (UTC)"
              value={formatOriginTime(waveform.originTimeUtc)}
            />
            <DetailItem
              label="Location"
              value={
                waveform.latitude != null && waveform.longitude != null
                  ? `${waveform.latitude}, ${waveform.longitude} · depth ${waveform.depthKm} km`
                  : "—"
              }
            />
            <DetailItem
              label="Sampling / duration"
              value={`${waveform.samplingRateHz} Hz · ${waveform.durationS}s · ${waveform.channel}`}
            />
            <DetailItem label="Dataset" value={waveform.datasetName} />
            {waveform.snrPeak != null ? (
              <DetailItem label="SNR peak" value={waveform.snrPeak.toFixed(2)} />
            ) : null}
            {waveform.pPickTimeS != null ? (
              <DetailItem
                label="P-pick (STA/LTA)"
                value={`${waveform.pPickTimeS}s`}
              />
            ) : null}
          </dl>
        </div>

        <div className="rounded-xl border border-border bg-surface p-6">
          <h3 className="font-serif text-xl font-semibold text-text">
            Acquisition & processing
          </h3>
          <ul className="mt-4 space-y-2 text-sm text-text-muted">
            <li>USGS FDSN events · EarthScope MiniSEED waveforms · ObsPy acquisition</li>
            <li>Pipeline stages: raw → detrended → filtered → normalized</li>
            <li>
              Source NPZ:{" "}
              <ExternalOrInternalLink
                href={waveform.npzLink.href}
                external={waveform.npzLink.external}
                label={waveform.npzSourcePath}
              />
            </li>
          </ul>
        </div>

        <LinkSection title="Related reports" links={waveform.relatedReports} />
        <LinkSection title="Related figures" links={figureLinks(waveform)} />
        <LinkSection title="Workflow stages" links={waveform.workflowStages} />
        <LinkSection title="Feature extraction" links={waveform.featureLinks} />
        <LinkSection title="Documentation" links={waveform.relatedDocs} />

        <div className="rounded-xl border border-dashed border-border bg-surface p-4 text-xs text-text-muted">
          <p className="font-semibold uppercase tracking-wider">Cross-navigation</p>
          <ul className="mt-2 space-y-2">
            <li>
              <Link href="/dataset#california-pilot" className="text-primary hover:text-primary-light">
                Dataset Explorer →
              </Link>
            </li>
            <li>
              <Link href="/workflow#signal-analysis" className="text-primary hover:text-primary-light">
                Workflow Explorer →
              </Link>
            </li>
            <li>
              <Link href="/results" className="text-primary hover:text-primary-light">
                Results Explorer →
              </Link>
            </li>
            <li>
              <Link href="/research/report" className="text-primary hover:text-primary-light">
                Research report →
              </Link>
            </li>
          </ul>
        </div>
      </motion.aside>
    </AnimatePresence>
  );
}

function figureLinks(waveform: WaveformRecord) {
  return [
    {
      label: waveform.previewFigures.signalAnalysis.label,
      path: `reports/figures/${waveform.previewFigures.signalAnalysis.filename}`,
      href: waveform.previewFigures.signalAnalysis.available
        ? waveform.previewFigures.signalAnalysis.publicUrl
        : waveform.previewFigures.signalAnalysis.reportHref,
      external: !waveform.previewFigures.signalAnalysis.available,
    },
    {
      label: waveform.previewFigures.preprocessing.label,
      path: `reports/figures/${waveform.previewFigures.preprocessing.filename}`,
      href: waveform.previewFigures.preprocessing.available
        ? waveform.previewFigures.preprocessing.publicUrl
        : waveform.previewFigures.preprocessing.reportHref,
      external: !waveform.previewFigures.preprocessing.available,
    },
  ];
}

function DetailItem({
  label,
  value,
  mono = false,
}: {
  label: string;
  value: string;
  mono?: boolean;
}) {
  return (
    <div>
      <dt className="text-xs font-semibold uppercase tracking-wider text-text-muted">
        {label}
      </dt>
      <dd className={`mt-1 text-text ${mono ? "font-mono text-xs break-all" : ""}`}>
        {value}
      </dd>
    </div>
  );
}

function LinkSection({
  title,
  links,
}: {
  title: string;
  links: WaveformRecord["relatedReports"];
}) {
  return (
    <div className="rounded-xl border border-border bg-surface p-6">
      <h3 className="font-serif text-lg font-semibold text-text">{title}</h3>
      <ul className="mt-3 space-y-2">
        {links.map((link) => (
          <li key={link.path}>
            <ExternalOrInternalLink
              href={link.href}
              external={link.external}
              label={link.label}
            />
          </li>
        ))}
      </ul>
    </div>
  );
}

function ExternalOrInternalLink({
  href,
  external,
  label,
}: {
  href: string;
  external: boolean;
  label: string;
}) {
  const className = "text-sm text-text-muted transition-colors hover:text-primary";

  if (external) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" className={className}>
        {label} ↗
      </a>
    );
  }

  return (
    <Link href={href} className={className}>
      {label} →
    </Link>
  );
}
