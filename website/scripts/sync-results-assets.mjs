import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const websiteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const repoRoot = path.resolve(websiteRoot, "..");

function copyMatchingFiles(sourceDir, destDir, predicate) {
  fs.mkdirSync(destDir, { recursive: true });

  if (!fs.existsSync(sourceDir)) {
    return 0;
  }

  let copied = 0;
  for (const file of fs.readdirSync(sourceDir)) {
    if (!predicate(file)) {
      continue;
    }

    fs.copyFileSync(path.join(sourceDir, file), path.join(destDir, file));
    copied += 1;
  }

  return copied;
}

function exportWaveforms() {
  const scriptPath = path.join(websiteRoot, "scripts/export-waveforms.py");
  if (!fs.existsSync(scriptPath)) {
    console.warn("[sync-results-assets] export-waveforms.py not found; skipping.");
    return 0;
  }

  const result = spawnSync("python", [scriptPath], {
    cwd: websiteRoot,
    stdio: "inherit",
    shell: process.platform === "win32",
  });

  if (result.status !== 0) {
    console.warn(
      "[sync-results-assets] Waveform export failed or Python unavailable; PNG fallback only.",
    );
    return 0;
  }

  const outputDir = path.join(websiteRoot, "public/waveforms");
  if (!fs.existsSync(outputDir)) {
    return 0;
  }

  return fs.readdirSync(outputDir).filter((file) => file.endsWith(".json")).length;
}

const figuresCopied =
  copyMatchingFiles(
    path.join(repoRoot, "reports/figures"),
    path.join(websiteRoot, "public/figures"),
    (file) => file.endsWith(".png"),
  ) +
  copyMatchingFiles(
    path.join(repoRoot, "reports/switzerland_validation/figures"),
    path.join(websiteRoot, "public/figures"),
    (file) => file.endsWith(".png"),
  ) +
  copyMatchingFiles(
    path.join(repoRoot, "reports/swiss_signal_analysis/figures"),
    path.join(websiteRoot, "public/figures"),
    (file) => file.endsWith(".png"),
  );

const tablesCopied =
  copyMatchingFiles(
    path.join(repoRoot, "reports/tables"),
    path.join(websiteRoot, "public/tables"),
    (file) => file.endsWith(".csv"),
  ) +
  copyMatchingFiles(
    path.join(repoRoot, "reports/switzerland_validation"),
    path.join(websiteRoot, "public/tables"),
    (file) => file.endsWith(".csv"),
  ) +
  copyMatchingFiles(
    path.join(repoRoot, "reports/swiss_signal_analysis"),
    path.join(websiteRoot, "public/tables"),
    (file) => file.endsWith(".csv"),
  );

const datasetsCopied = copyMatchingFiles(
  path.join(repoRoot, "data/manifests"),
  path.join(websiteRoot, "public/datasets"),
  (file) => file.endsWith(".csv"),
);

// STEP ML-1A..ML-4 assets: final research figures + downloadable saved results.
const finalFiguresCopied = copyMatchingFiles(
  path.join(repoRoot, "reports/figures/final"),
  path.join(websiteRoot, "public/final-figures"),
  (file) => file.endsWith(".png"),
);

const mlDownloads = [
  "reports/ml/vertical_set_c_evaluation_summary.json",
  "reports/ml/vertical_set_a_evaluation_summary.json",
  "reports/ml/swiss_ml_evaluation_summary.json",
  "reports/ml/vertical_feature_schema.json",
  "reports/ml/vertical_set_c_per_event_results.csv",
  "reports/ml/vertical_set_a_per_event_cv.csv",
  "reports/ml/STEP_ML4_COMPREHENSIVE_REPORT.md",
  "docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md",
  "docs/RESEARCH_PACKAGE.md",
  "docs/ML_REPRODUCTION_GUIDE.md",
  "docs/DATA_AND_MODEL_INVENTORY.md",
  "FINAL_INTEGRITY_CHECK.md",
];
let mlDownloadsCopied = 0;
fs.mkdirSync(path.join(websiteRoot, "public/ml-downloads"), { recursive: true });
for (const rel of mlDownloads) {
  const src = path.join(repoRoot, rel);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, path.join(websiteRoot, "public/ml-downloads", path.basename(rel)));
    mlDownloadsCopied += 1;
  }
}

const waveformsExported = exportWaveforms();

console.log(
  `[sync-results-assets] Copied ${figuresCopied} figures, ${tablesCopied} tables, ${datasetsCopied} manifests, ${finalFiguresCopied} final figures, ${mlDownloadsCopied} ML downloads; exported ${waveformsExported} waveform JSON files`,
);
