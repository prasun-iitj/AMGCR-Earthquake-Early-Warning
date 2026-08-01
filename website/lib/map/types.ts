/**
 * Earthquake map types — designed for dashboard (Phase 9) and AI (v3).
 */

export type MapDatasetId =
  | "california-pilot"
  | "europe-future"
  | "japan-reference"
  | "additional-pilots";

export type MapEventLink = {
  label: string;
  path: string;
  href: string;
  external: boolean;
};

export type MapEvent = {
  id: string;
  eventId: string;
  datasetId: MapDatasetId;
  datasetName: string;
  latitude: number;
  longitude: number;
  depthKm: number;
  magnitude: number;
  magnitudeType: string;
  originTimeUtc: string;
  stationId: string;
  channel: string;
  waveformHref: string;
  datasetHref: string;
  workflowHref: string;
  resultsHref: string;
  relatedReport: MapEventLink;
  workflowStage: MapEventLink;
  /** Serializable metadata for dashboard / AI indexing (v3). */
  metadata: Record<string, string | number | boolean | null>;
};

export type MapDatasetOption = {
  id: MapDatasetId | "all";
  label: string;
  status: "active" | "planned";
  eventCount: number;
};

/** Filter state reusable by Phase 9 dashboard. */
export type MapFilterState = {
  dataset: MapDatasetId | "all";
  magnitudeMin: number;
  magnitudeMax: number;
  timeStart: string;
  timeEnd: string;
};

export type MapFilterBounds = {
  magnitudeMin: number;
  magnitudeMax: number;
  timeStart: string;
  timeEnd: string;
};

export type LoadedMapExplorer = {
  events: MapEvent[];
  datasetOptions: MapDatasetOption[];
  filterBounds: MapFilterBounds;
  defaultFilter: MapFilterState;
  defaultSelectedId: string | null;
  mapCenter: [number, number];
  mapZoom: number;
};
