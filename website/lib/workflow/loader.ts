import fs from "node:fs";
import path from "node:path";
import { resolveRepoPath } from "@/lib/content/paths";
import {
  resolveStageLink,
  workflowStageConfigs,
  type WorkflowStageConfig,
  type WorkflowStageId,
} from "@/lib/workflow/stages.config";

export type WorkflowLink = {
  label: string;
  path: string;
  href: string;
  external: boolean;
  exists: boolean;
};

export type LoadedWorkflowStage = {
  id: WorkflowStageId;
  title: string;
  order: number;
  purpose: string;
  inputs: WorkflowLink[];
  outputs: WorkflowLink[];
  reports: WorkflowLink[];
  figures: WorkflowLink[];
  documentation: WorkflowLink[];
  scripts: WorkflowLink[];
};

function pathExists(repoPath: string): boolean {
  if (repoPath.startsWith("http://") || repoPath.startsWith("https://")) {
    return true;
  }

  const absolute = resolveRepoPath(repoPath);
  return fs.existsSync(absolute);
}

function toWorkflowLink(entry: { label: string; path: string }): WorkflowLink {
  const { href, external } = resolveStageLink(entry.path);
  return {
    label: entry.label,
    path: entry.path,
    href,
    external,
    exists: pathExists(entry.path),
  };
}

function cleanMarkdownText(text: string): string {
  return text
    .split("\n")
    .filter((line) => !line.startsWith("|") && !line.startsWith("```"))
    .join("\n")
    .split("\n\n")
    .map((paragraph) =>
      paragraph
        .replace(/^>\s+/gm, "")
        .replace(/\*\*/g, "")
        .replace(/`([^`]+)`/g, "$1")
        .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
        .trim(),
    )
    .filter(Boolean)[0] ?? "";
}

function extractPurpose(config: WorkflowStageConfig): string {
  const reportPath = resolveRepoPath(config.primaryReport);
  if (!fs.existsSync(reportPath)) {
    return "Purpose described in the linked phase report.";
  }

  const content = fs.readFileSync(reportPath, "utf8");
  const sectionHeading = config.purposeSection ?? "## 1.";

  const sectionIndex = content.indexOf(sectionHeading);
  if (sectionIndex === -1) {
    return cleanMarkdownText(content) || "Purpose described in the linked phase report.";
  }

  const afterHeading = content.slice(sectionIndex + sectionHeading.length);
  const nextSection = afterHeading.search(/\n## |\n---/);
  const sectionBody =
    nextSection === -1 ? afterHeading : afterHeading.slice(0, nextSection);

  const purpose = cleanMarkdownText(sectionBody);
  if (purpose.length >= 40 && !purpose.startsWith("|")) {
    return purpose;
  }

  const intro = content.split("\n---\n")[0] ?? content;
  const introPurpose = cleanMarkdownText(
    intro.replace(/^#\s[^\n]+\n+/m, "").replace(/^\|[^\n]+\n/m, ""),
  );
  return introPurpose || "Purpose described in the linked phase report.";
}

function listFigures(config: WorkflowStageConfig): WorkflowLink[] {
  const figures = new Set<string>(config.figurePaths);

  if (config.figureDirectoryPrefixes?.length) {
    const figuresDir = resolveRepoPath("reports/figures");
    if (fs.existsSync(figuresDir)) {
      for (const file of fs.readdirSync(figuresDir)) {
        if (
          config.figureDirectoryPrefixes.some((prefix) => file.startsWith(prefix)) &&
          file.endsWith(".png")
        ) {
          figures.add(`reports/figures/${file}`);
        }
      }
    }
  }

  return Array.from(figures)
    .sort()
    .map((figurePath) =>
      toWorkflowLink({
        label: path.basename(figurePath),
        path: figurePath,
      }),
    );
}

function loadStage(config: WorkflowStageConfig): LoadedWorkflowStage {
  const scripts: WorkflowLink[] = config.script
    ? [
        toWorkflowLink({
          label: path.basename(config.script),
          path: config.script,
        }),
      ]
    : [];

  return {
    id: config.id,
    title: config.title,
    order: config.order,
    purpose: extractPurpose(config),
    inputs: config.inputs.map(toWorkflowLink),
    outputs: config.outputs.map(toWorkflowLink),
    reports: config.reports.map(toWorkflowLink),
    figures: listFigures(config),
    documentation: config.documentation.map(toWorkflowLink),
    scripts,
  };
}

export function loadWorkflowStages(): LoadedWorkflowStage[] {
  return workflowStageConfigs.map(loadStage);
}

export function loadWorkflowStage(id: WorkflowStageId): LoadedWorkflowStage {
  const config = workflowStageConfigs.find((stage) => stage.id === id);
  if (!config) {
    throw new Error(`Unknown workflow stage: ${id}`);
  }
  return loadStage(config);
}
