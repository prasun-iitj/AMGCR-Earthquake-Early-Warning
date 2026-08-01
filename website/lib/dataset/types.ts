/**
 * Core dataset types — designed for future waveform explorer, map, dashboard, and AI (v3).
 */

export type DatasetStatus = "active" | "planned";

export type DatasetCapabilities = {
  /** Phase 7: waveform explorer */
  waveforms: boolean;
  /** Phase 8: earthquake map */
  map: boolean;
  /** Phase 9: dashboard statistics */
  dashboard: boolean;
  /** Version 3: semantic / RAG metadata */
  aiMetadata: boolean;
};

export type DatasetLink = {
  label: string;
  path: string;
  href: string;
  external: boolean;
};

export type DatasetStatistics = {
  eventCount: number | null;
  stationCount: number | null;
  waveformCount: number | null;
  magnitudeMin: number | null;
  magnitudeMax: number | null;
  timeRangeStart: string | null;
  timeRangeEnd: string | null;
  samplingRateHz: number | null;
  channels: string[];
  featureCount: number | null;
  figureCount: number | null;
  tableCount: number | null;
  reportCount: number | null;
};

export type DatasetRecord = {
  id: string;
  name: string;
  region: string;
  status: DatasetStatus;
  summary: string;
  source: string;
  acquisitionMethod: string;
  providers: string[];
  capabilities: DatasetCapabilities;
  statistics: DatasetStatistics;
  manifestPath: string | null;
  rawDataPath: string | null;
  reports: DatasetLink[];
  figures: DatasetLink[];
  tables: DatasetLink[];
  documentation: DatasetLink[];
  downloads: DatasetLink[];
  /** Structured metadata for future AI / search indexing (v3). */
  metadata: Record<string, string | number | boolean | string[] | null>;
};

export type DatasetJourneyStep = {
  id: string;
  label: string;
  description: string;
  href: string;
  external: boolean;
  /** Future: associate step with dataset phase for workflow/map hooks */
  phase?: string;
};

export type DatasetRegistryEntry = {
  id: string;
  name: string;
  region: string;
  status: DatasetStatus;
  teaser: string;
};

export type LoadedDatasetExplorer = {
  overview: {
    activeDatasetCount: number;
    plannedDatasetCount: number;
    totalEvents: number;
    totalStations: number;
  };
  datasets: DatasetRecord[];
  registry: DatasetRegistryEntry[];
  journey: DatasetJourneyStep[];
  defaultDatasetId: string;
};
