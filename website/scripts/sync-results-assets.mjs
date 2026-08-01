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

const figuresCopied = copyMatchingFiles(
  path.join(repoRoot, "reports/figures"),
  path.join(websiteRoot, "public/figures"),
  (file) => file.endsWith(".png"),
);

const tablesCopied = copyMatchingFiles(
  path.join(repoRoot, "reports/tables"),
  path.join(websiteRoot, "public/tables"),
  (file) => file.endsWith(".csv"),
);

const datasetsCopied = copyMatchingFiles(
  path.join(repoRoot, "data/manifests"),
  path.join(websiteRoot, "public/datasets"),
  (file) => file.endsWith(".csv"),
);

const waveformsExported = exportWaveforms();

console.log(
  `[sync-results-assets] Copied ${figuresCopied} figures, ${tablesCopied} tables, ${datasetsCopied} manifests; exported ${waveformsExported} waveform JSON files`,
);
