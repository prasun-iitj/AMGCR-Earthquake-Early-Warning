import fs from "node:fs";
import { resolveRepoPath } from "@/lib/content/paths";
import { resolveStageLink } from "@/lib/workflow/stages.config";
import {
  mapDatasetLabels,
  mapDatasetOrder,
  mapDatasetStatus,
} from "@/lib/map/registry";
import type {
  LoadedMapExplorer,
  MapDatasetOption,
  MapEvent,
  MapFilterBounds,
  MapFilterState,
} from "@/lib/map/types";

type EventSummaryRow = {
  eventId: string;
  originTimeUtc: string;
  latitude: string;
  longitude: string;
  depthKm: string;
  magnitude: string;
  magnitudeType: string;
  stationId: string;
  channel: string;
};

function parseCsvLine(line: string): string[] {
  const values: string[] = [];
  let current = "";
  let inQuotes = false;

  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];

    if (char === '"') {
      inQuotes = !inQuotes;
      continue;
    }

    if (char === "," && !inQuotes) {
      values.push(current.trim());
      current = "";
      continue;
    }

    current += char;
  }

  values.push(current.trim());
  return values;
}

function extractShortId(eventId: string): string {
  const marker = "_query_eventid_";
  const formatMarker = "_format_quakeml";
  const start = eventId.indexOf(marker);
  if (start === -1) {
    return eventId;
  }
  const from = start + marker.length;
  const end = eventId.indexOf(formatMarker, from);
  return end === -1 ? eventId.slice(from) : eventId.slice(from, end);
}

function toLink(label: string, repoPath: string) {
  const { href, external } = resolveStageLink(repoPath);
  return { label, path: repoPath, href, external };
}

function loadEventSummaryRows(): EventSummaryRow[] {
  const csvPath = resolveRepoPath("reports/tables/event_summary.csv");
  if (!fs.existsSync(csvPath)) {
    return [];
  }

  const lines = fs
    .readFileSync(csvPath, "utf8")
    .split(/\r?\n/)
    .filter((line) => line.trim().length > 0);

  if (lines.length < 2) {
    return [];
  }

  return lines.slice(1).map((line) => {
    const [
      eventId,
      originTimeUtc,
      latitude,
      longitude,
      depthKm,
      magnitude,
      magnitudeType,
      stationId,
      channel,
    ] = parseCsvLine(line);

    return {
      eventId,
      originTimeUtc,
      latitude,
      longitude,
      depthKm,
      magnitude,
      magnitudeType,
      stationId,
      channel,
    };
  });
}

function buildMapEvent(row: EventSummaryRow): MapEvent {
  const shortId = extractShortId(row.eventId);

  return {
    id: shortId,
    eventId: row.eventId,
    datasetId: "california-pilot",
    datasetName: mapDatasetLabels["california-pilot"],
    latitude: Number.parseFloat(row.latitude),
    longitude: Number.parseFloat(row.longitude),
    depthKm: Number.parseFloat(row.depthKm),
    magnitude: Number.parseFloat(row.magnitude),
    magnitudeType: row.magnitudeType,
    originTimeUtc: row.originTimeUtc,
    stationId: row.stationId,
    channel: row.channel,
    waveformHref: `/waveforms#${shortId}`,
    datasetHref: "/dataset#california-pilot",
    workflowHref: "/workflow#signal-analysis",
    resultsHref: "/results",
    relatedReport: toLink("Signal analysis report", "docs/SIGNAL_ANALYSIS_REPORT.md"),
    workflowStage: {
      label: "Signal analysis workflow stage",
      path: "docs/SIGNAL_ANALYSIS_REPORT.md",
      href: "/workflow#signal-analysis",
      external: false,
    },
    metadata: {
      event_id: shortId,
      full_event_id: row.eventId,
      dataset_id: "california-pilot",
      latitude: Number.parseFloat(row.latitude),
      longitude: Number.parseFloat(row.longitude),
      depth_km: Number.parseFloat(row.depthKm),
      magnitude: Number.parseFloat(row.magnitude),
      origin_time_utc: row.originTimeUtc,
      station_id: row.stationId,
      channel: row.channel,
    },
  };
}

function computeFilterBounds(events: MapEvent[]): MapFilterBounds {
  if (events.length === 0) {
    return {
      magnitudeMin: 0,
      magnitudeMax: 10,
      timeStart: "2024-01-01",
      timeEnd: "2026-12-31",
    };
  }

  const magnitudes = events.map((event) => event.magnitude);
  const times = events
    .map((event) => new Date(event.originTimeUtc).getTime())
    .filter((value) => !Number.isNaN(value));

  const minTime = Math.min(...times);
  const maxTime = Math.max(...times);

  return {
    magnitudeMin: Math.floor(Math.min(...magnitudes) * 10) / 10,
    magnitudeMax: Math.ceil(Math.max(...magnitudes) * 10) / 10,
    timeStart: new Date(minTime).toISOString().slice(0, 10),
    timeEnd: new Date(maxTime).toISOString().slice(0, 10),
  };
}

function buildDatasetOptions(events: MapEvent[]): MapDatasetOption[] {
  const counts = Object.fromEntries(
    mapDatasetOrder.map((id) => [id, 0]),
  ) as Record<string, number>;

  for (const event of events) {
    counts[event.datasetId] = (counts[event.datasetId] ?? 0) + 1;
  }

  const perDataset = mapDatasetOrder.map((id) => ({
    id,
    label: mapDatasetLabels[id],
    status: mapDatasetStatus[id],
    eventCount: counts[id] ?? 0,
  }));

  return [
    {
      id: "all",
      label: "All datasets",
      status: "active",
      eventCount: events.length,
    },
    ...perDataset,
  ];
}

function computeMapCenter(events: MapEvent[]): [number, number] {
  if (events.length === 0) {
    return [36.7, -118.0];
  }

  const latitude =
    events.reduce((sum, event) => sum + event.latitude, 0) / events.length;
  const longitude =
    events.reduce((sum, event) => sum + event.longitude, 0) / events.length;

  return [latitude, longitude];
}

export function loadMapExplorer(): LoadedMapExplorer {
  const events = loadEventSummaryRows().map(buildMapEvent);
  const filterBounds = computeFilterBounds(events);

  const defaultFilter: MapFilterState = {
    dataset: "all",
    magnitudeMin: filterBounds.magnitudeMin,
    magnitudeMax: filterBounds.magnitudeMax,
    timeStart: filterBounds.timeStart,
    timeEnd: filterBounds.timeEnd,
  };

  return {
    events,
    datasetOptions: buildDatasetOptions(events),
    filterBounds,
    defaultFilter,
    defaultSelectedId: events[0]?.id ?? null,
    mapCenter: computeMapCenter(events),
    mapZoom: 6,
  };
}

/** Phase 9 hook: resolve map event by id. */
export function getMapEventById(id: string): MapEvent | null {
  return loadMapExplorer().events.find((event) => event.id === id) ?? null;
}

/** Phase 9 / v3 hook: export serializable map metadata index. */
export function getMapMetadataIndex(): Record<string, MapEvent["metadata"]> {
  return Object.fromEntries(
    loadMapExplorer().events.map((event) => [event.id, event.metadata]),
  );
}

/** Phase 9 hook: apply static filters server-side for dashboard reuse. */
export { filterMapEvents } from "@/lib/map/filters";
