import type { WaveformDatasetGroup } from "@/lib/waveforms/types";

/** Dataset group registry — add future datasets without component changes. */
export const waveformDatasetOrder = [
  "california-pilot",
  "europe-future",
  "japan-reference",
  "additional-pilots",
] as const;

export type WaveformDatasetId = (typeof waveformDatasetOrder)[number];

export const waveformDatasetLabels: Record<WaveformDatasetId, string> = {
  "california-pilot": "California Pilot",
  "europe-future": "Europe (ORFEUS / EIDA)",
  "japan-reference": "Japan (EarthESND Reference)",
  "additional-pilots": "Additional Western Pilots",
};

export function groupWaveformsByDataset(
  groups: WaveformDatasetGroup[],
): WaveformDatasetGroup[] {
  return waveformDatasetOrder.map((datasetId) => {
    const existing = groups.find((group) => group.datasetId === datasetId);
    if (existing) {
      return existing;
    }

    return {
      datasetId,
      datasetName: waveformDatasetLabels[datasetId],
      status: datasetId === "california-pilot" ? "active" : "planned",
      waveforms: [],
      waveformCount: 0,
    };
  });
}
