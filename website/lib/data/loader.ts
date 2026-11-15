import fs from "node:fs";
import { resolveRepoPath } from "@/lib/content/paths";

/** Build-time loader for reports/data_lineage/data_lineage_summary.json (committed; no raw data needed). */

type Counts = Record<string, number>;
type EventRow = { short_id: string; region: string; magnitude: number; records: number; stations: number; location_class?: string };

export type DataLineage = {
  generated_at_utc: string;
  california: {
    events: number;
    waveform_files_in_manifest: number;
    stations_in_manifest: string[];
    channels_in_manifest: string[];
    magnitude_range: [number, number];
    local_raw_mseed_files: number | null;
    local_raw_files_not_in_manifest: string[] | null;
  };
  set_a: {
    events: number; records: number; stations: number; channels: string[]; sampling_rates_hz: Counts;
    magnitude_range: [number, number]; download_status: Counts; validation_status: Counts; stationxml_available: Counts;
    pre_event_seconds_min: number; post_event_seconds_min: number;
    picks: { n: number; phases: Counts; evaluation_mode: Counts };
    windows: { total: number; positive: number; negative: number };
    p_latency_s_range: [number, number]; epicentral_distance_km_range: [number, number];
    local_raw_mseed_files: number | null; local_stationxml_files: number | null; events_table: EventRow[];
  };
  set_c: {
    events: number; records: number; stations: number; channels: string[]; sampling_rates_hz: Counts;
    magnitude_range: [number, number]; location_class_records: Counts; download_status: Counts; verification_status: Counts;
    coverage_status: Counts; stationxml_status: Counts; gaps_total: number; overlaps_total: number;
    picks: { n: number; phases: Counts; evaluation_mode: Counts };
    candidate_pool: { rows: number; pool_role: Counts };
    windows: { total: number; positive: number; negative: number };
    local_raw_mseed_files: number | null; local_stationxml_files: number | null; events_table: EventRow[];
  };
  overlap: {
    event_overlap: number; stations_set_a: number; stations_set_c: number; stations_shared: number;
    stations_set_c_only: number; set_c_records_at_shared_stations: number;
  };
  schemas: {
    feature_columns_24_in_set_a_matrix_order: string[]; vertical_schema_json: string[];
    vertical_schema_matches_vertical_models: boolean; nan_counts: Counts; n_24: number; n_18: number;
  };
};

export function loadDataLineage(): DataLineage | null {
  const p = resolveRepoPath("reports/data_lineage/data_lineage_summary.json");
  if (!fs.existsSync(p)) return null;
  try {
    return JSON.parse(fs.readFileSync(p, "utf8")) as DataLineage;
  } catch {
    return null;
  }
}
