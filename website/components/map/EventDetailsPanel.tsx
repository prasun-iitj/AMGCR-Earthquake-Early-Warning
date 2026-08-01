"use client";

import Link from "next/link";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import type { MapEvent } from "@/lib/map/types";

type EventDetailsPanelProps = {
  event: MapEvent | null;
  compact?: boolean;
};

function formatOriginTime(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toISOString().replace("T", " ").slice(0, 19);
}

export function EventDetailsPanel({ event, compact = false }: EventDetailsPanelProps) {
  const shouldReduceMotion = useReducedMotion();

  if (!event) {
    return (
      <div className="rounded-xl border border-dashed border-border bg-surface p-6 text-sm text-text-muted">
        Select an earthquake marker on the map to view event details and cross-links
        to waveforms, datasets, workflow, and results.
      </div>
    );
  }

  return (
    <AnimatePresence mode="wait">
      <motion.aside
        key={event.id}
        initial={shouldReduceMotion ? false : { opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={shouldReduceMotion ? undefined : { opacity: 0, y: -8 }}
        transition={{ duration: 0.22 }}
        className={[
          "rounded-xl border border-border bg-surface-elevated",
          compact ? "p-4" : "p-6",
        ].join(" ")}
        aria-label="Selected earthquake event details"
      >
        <p className="text-sm font-semibold uppercase tracking-wider text-accent">
          Event details
        </p>
        <h2 className="mt-2 font-serif text-2xl font-semibold text-text">
          {event.id}
        </h2>
        <p className="mt-2 text-sm text-text-muted">
          M{event.magnitude.toFixed(2)} ({event.magnitudeType}) · {event.datasetName}
        </p>

        <dl className="mt-6 space-y-3 text-sm">
          <DetailItem label="Event ID" value={event.id} mono />
          <DetailItem
            label="Date & time (UTC)"
            value={formatOriginTime(event.originTimeUtc)}
          />
          <DetailItem
            label="Latitude / longitude"
            value={`${event.latitude}, ${event.longitude}`}
          />
          <DetailItem label="Depth" value={`${event.depthKm} km`} />
          <DetailItem label="Station" value={event.stationId} />
          <DetailItem label="Channel" value={event.channel} />
          <DetailItem label="Dataset" value={event.datasetName} />
        </dl>

        <div className="mt-8 space-y-3">
          <h3 className="font-serif text-lg font-semibold text-text">Explore further</h3>
          <NavLink href={event.waveformHref} label="Related waveform" />
          <NavLink href={event.datasetHref} label="Dataset explorer" />
          <NavLink href={event.workflowHref} label="Workflow stage" />
          <NavLink href={event.resultsHref} label="Results explorer" />
          <ExternalOrInternalLink link={event.relatedReport} />
          <ExternalOrInternalLink link={event.workflowStage} />
          <NavLink href="/research/report" label="Research report" />
        </div>

        {!compact ? (
          <p className="mt-6 text-xs text-text-muted">
            Global synchronization with Dataset and Waveform explorers will connect
            selected events in a future UI enhancement.
          </p>
        ) : null}
      </motion.aside>
    </AnimatePresence>
  );
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
      <dd className={`mt-1 text-text ${mono ? "font-mono text-xs" : ""}`}>{value}</dd>
    </div>
  );
}

function NavLink({ href, label }: { href: string; label: string }) {
  return (
    <Link
      href={href}
      className="block text-sm font-medium text-primary hover:text-primary-light"
    >
      {label} →
    </Link>
  );
}

function ExternalOrInternalLink({
  link,
}: {
  link: MapEvent["relatedReport"];
}) {
  const className = "block text-sm font-medium text-primary hover:text-primary-light";

  if (link.external) {
    return (
      <a href={link.href} target="_blank" rel="noopener noreferrer" className={className}>
        {link.label} ↗
      </a>
    );
  }

  return (
    <Link href={link.href} className={className}>
      {link.label} →
    </Link>
  );
}
