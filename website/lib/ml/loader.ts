import fs from "node:fs";
import { resolveRepoPath } from "@/lib/content/paths";

/** Build-time loader for STEP ML-3/ML-4 saved results. Reads existing artifacts only. */

export type BinaryMetrics = {
  accuracy: number;
  precision: number;
  recall: number;
  specificity?: number;
  f1_score: number;
  roc_auc: number;
  tp: number;
  fp: number;
  tn: number;
  fn: number;
};

export type ModelSet = Record<string, BinaryMetrics>;

export type PerEventRow = {
  id: string;
  magnitude: number | null;
  samples: number | null;
  rfRecall: number;
  xgbRecall: number;
  staRecall: number | null;
  rfF1: number;
  xgbF1: number;
};

export type StationOverlap = {
  setAEvents: number;
  setCEvents: number;
  eventOverlap: number;
  setAStations: number;
  setCStations: number;
  sharedStations: number;
  setCOnlyStations: number;
};

export type MlResults = {
  setC: { models: ModelSet; nSamples: number; nEvents: number; nStations: number; rf: Record<string, number>; xgb: Record<string, number> } | null;
  setAVertical: ModelSet | null;
  setA24: ModelSet | null;
  features: string[];
  perEventC: PerEventRow[];
  overlap: StationOverlap | null;
};

function readJson<T>(rel: string): T | null {
  const p = resolveRepoPath(rel);
  if (!fs.existsSync(p)) return null;
  try {
    return JSON.parse(fs.readFileSync(p, "utf8")) as T;
  } catch {
    return null;
  }
}

function parseCsvLine(line: string): string[] {
  const out: string[] = [];
  let cur = "";
  let quoted = false;
  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (ch === '"') {
      if (quoted && line[i + 1] === '"') {
        cur += '"';
        i += 1;
      } else {
        quoted = !quoted;
      }
    } else if (ch === "," && !quoted) {
      out.push(cur);
      cur = "";
    } else {
      cur += ch;
    }
  }
  out.push(cur);
  return out;
}

function readCsv(rel: string): Record<string, string>[] {
  const p = resolveRepoPath(rel);
  if (!fs.existsSync(p)) return [];
  const lines = fs.readFileSync(p, "utf8").split(/\r?\n/).filter((l) => l.trim().length > 0);
  if (lines.length < 2) return [];
  const header = parseCsvLine(lines[0]);
  return lines.slice(1).map((line) => {
    const cells = parseCsvLine(line);
    return Object.fromEntries(header.map((h, i) => [h, cells[i] ?? ""]));
  });
}

function computeOverlap(): StationOverlap | null {
  const a = readCsv("reports/features/swiss_set_a_feature_matrix.csv");
  const c = readCsv("reports/features/swiss_set_c_feature_matrix.csv");
  if (!a.length || !c.length) return null;
  const evA = new Set(a.map((r) => r.event_id));
  const evC = new Set(c.map((r) => r.event_id));
  const stA = new Set(a.map((r) => r.station));
  const stC = new Set(c.map((r) => r.station));
  const shared = [...stA].filter((s) => stC.has(s)).length;
  return {
    setAEvents: evA.size,
    setCEvents: evC.size,
    eventOverlap: [...evA].filter((e) => evC.has(e)).length,
    setAStations: stA.size,
    setCStations: stC.size,
    sharedStations: shared,
    setCOnlyStations: [...stC].filter((s) => !stA.has(s)).length,
  };
}

export function loadMlResults(): MlResults {
  const c = readJson<{
    n_samples: number;
    n_events: number;
    n_stations: number;
    features: string[];
    models: { random_forest_vertical: BinaryMetrics; xgboost_vertical: BinaryMetrics; sta_lta_threshold_8_0: BinaryMetrics };
    feature_importances_rf: Record<string, number>;
    feature_importances_xgb: Record<string, number>;
  }>("reports/ml/vertical_set_c_evaluation_summary.json");
  const a = readJson<{ models: { random_forest_vertical: BinaryMetrics; xgboost_vertical: BinaryMetrics } }>(
    "reports/ml/vertical_set_a_evaluation_summary.json",
  );
  const ml3 = readJson<{
    models: { random_forest: BinaryMetrics; xgboost: BinaryMetrics; sta_lta_threshold_8_0: BinaryMetrics };
  }>("reports/ml/swiss_ml_evaluation_summary.json");

  const perEventC: PerEventRow[] = readCsv("reports/ml/vertical_set_c_per_event_results.csv").map((r) => ({
    id: r.short_id,
    magnitude: r.magnitude ? Number(r.magnitude) : null,
    samples: r.n_samples ? Number(r.n_samples) : null,
    rfRecall: Number(r.rf_recall),
    xgbRecall: Number(r.xgb_recall),
    staRecall: r.sta_recall ? Number(r.sta_recall) : null,
    rfF1: Number(r.rf_f1),
    xgbF1: Number(r.xgb_f1),
  }));

  return {
    setC: c
      ? {
          models: {
            "Random Forest": c.models.random_forest_vertical,
            XGBoost: c.models.xgboost_vertical,
            "STA/LTA >= 8.0 (window-level)": c.models.sta_lta_threshold_8_0,
          },
          nSamples: c.n_samples,
          nEvents: c.n_events,
          nStations: c.n_stations,
          rf: c.feature_importances_rf,
          xgb: c.feature_importances_xgb,
        }
      : null,
    setAVertical: a
      ? { "RF 18-feat": a.models.random_forest_vertical, "XGB 18-feat": a.models.xgboost_vertical }
      : null,
    setA24: ml3
      ? {
          "RF 24-feat": ml3.models.random_forest,
          "XGB 24-feat": ml3.models.xgboost,
          "STA/LTA 8.0": ml3.models.sta_lta_threshold_8_0,
        }
      : null,
    features: c?.features ?? [],
    perEventC,
    overlap: computeOverlap(),
  };
}
