import fs from "node:fs";
import path from "node:path";
import { resolveRepoPath } from "@/lib/content/paths";
import { resolveStageLink } from "@/lib/workflow/stages.config";
import {
  classifyFigure,
  figurePhaseOrder,
  figurePhaseLabels,
  figureTitle,
  phaseReportPaths,
  tableDefinitions,
  type FigurePhase,
} from "@/lib/results/config";
import {
  defaultFigureDescription,
  parseEdaFigureDescriptions,
  parseFeatureFigureDescriptions,
} from "@/lib/results/descriptions";

export type ResultFigure = {
  id: string;
  filename: string;
  title: string;
  phase: FigurePhase;
  phaseLabel: string;
  description: string;
  publicUrl: string;
  available: boolean;
  reportPath: string;
  reportHref: string;
  reportExternal: boolean;
};

export type ResultTable = {
  filename: string;
  title: string;
  phase: FigurePhase;
  phaseLabel: string;
  description: string;
  reportPath: string;
  reportHref: string;
  reportExternal: boolean;
  downloadUrl: string;
  available: boolean;
  headers: string[];
  previewRows: string[][];
  rowCount: number;
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

function loadTablePreview(
  filename: string,
  maxRows = 5,
): Pick<ResultTable, "headers" | "previewRows" | "rowCount" | "available"> {
  const absolutePath = resolveRepoPath(path.join("reports/tables", filename));

  if (!fs.existsSync(absolutePath)) {
    return {
      headers: [],
      previewRows: [],
      rowCount: 0,
      available: false,
    };
  }

  const lines = fs
    .readFileSync(absolutePath, "utf8")
    .split(/\r?\n/)
    .filter((line) => line.trim().length > 0);

  if (lines.length === 0) {
    return {
      headers: [],
      previewRows: [],
      rowCount: 0,
      available: false,
    };
  }

  const headers = parseCsvLine(lines[0]);
  const dataLines = lines.slice(1);

  return {
    headers,
    previewRows: dataLines.slice(0, maxRows).map(parseCsvLine),
    rowCount: dataLines.length,
    available: true,
  };
}

function discoverFigures(): ResultFigure[] {
  const figuresDir = resolveRepoPath("reports/figures");
  const publicFiguresDir = path.resolve(process.cwd(), "public/figures");
  const edaDescriptions = parseEdaFigureDescriptions();
  const featureDescriptions = parseFeatureFigureDescriptions();

  const filenames = new Set<string>();

  if (fs.existsSync(figuresDir)) {
    for (const file of fs.readdirSync(figuresDir)) {
      if (file.endsWith(".png")) {
        filenames.add(file);
      }
    }
  }

  const figures = Array.from(filenames)
    .sort()
    .map((filename) => {
      const phase = classifyFigure(filename);
      const reportPath = phaseReportPaths[phase];
      const reportLink = resolveStageLink(reportPath);
      const available =
        fs.existsSync(path.join(figuresDir, filename)) ||
        fs.existsSync(path.join(publicFiguresDir, filename));

      const description =
        edaDescriptions[filename] ??
        featureDescriptions[filename] ??
        defaultFigureDescription(filename, figurePhaseLabels[phase]);

      return {
        id: filename,
        filename,
        title: figureTitle(filename),
        phase,
        phaseLabel: figurePhaseLabels[phase],
        description,
        publicUrl: `/figures/${filename}`,
        available,
        reportPath,
        reportHref: reportLink.href,
        reportExternal: reportLink.external,
      };
    });

  return figures.sort((a, b) => {
    const phaseDiff =
      figurePhaseOrder.indexOf(a.phase) - figurePhaseOrder.indexOf(b.phase);
    if (phaseDiff !== 0) {
      return phaseDiff;
    }
    return a.filename.localeCompare(b.filename);
  });
}

function loadTables(): ResultTable[] {
  return tableDefinitions.map((definition) => {
    const preview = loadTablePreview(definition.filename);
    const reportLink = resolveStageLink(definition.reportPath);
    const publicPath = path.resolve(
      process.cwd(),
      "public/tables",
      definition.filename,
    );

    return {
      filename: definition.filename,
      title: definition.title,
      phase: definition.phase,
      phaseLabel: figurePhaseLabels[definition.phase],
      description: definition.description,
      reportPath: definition.reportPath,
      reportHref: reportLink.href,
      reportExternal: reportLink.external,
      downloadUrl: `/tables/${definition.filename}`,
      available: preview.available && fs.existsSync(publicPath),
      headers: preview.headers,
      previewRows: preview.previewRows,
      rowCount: preview.rowCount,
    };
  });
}

export function loadResultsExplorerData() {
  return {
    figures: discoverFigures(),
    tables: loadTables(),
  };
}

export function groupFiguresByPhase(figures: ResultFigure[]) {
  return figurePhaseOrder.map((phase) => ({
    phase,
    label: figurePhaseLabels[phase],
    figures: figures.filter((figure) => figure.phase === phase),
  }));
}
