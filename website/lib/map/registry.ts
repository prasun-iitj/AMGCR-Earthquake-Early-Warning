import type { MapDatasetId } from "@/lib/map/types";

/** Dataset registry — add future regions without component changes. */
export const mapDatasetOrder: MapDatasetId[] = [
  "california-pilot",
  "europe-future",
  "japan-reference",
  "additional-pilots",
];

export const mapDatasetLabels: Record<MapDatasetId, string> = {
  "california-pilot": "California Pilot",
  "europe-future": "Europe (ORFEUS / EIDA)",
  "japan-reference": "Japan (EarthESND Reference)",
  "additional-pilots": "Additional Western Pilots",
};

export const mapDatasetStatus: Record<MapDatasetId, "active" | "planned"> = {
  "california-pilot": "active",
  "europe-future": "planned",
  "japan-reference": "planned",
  "additional-pilots": "planned",
};

export function magnitudeMarkerRadius(magnitude: number): number {
  return Math.max(6, Math.min(18, magnitude * 2.5));
}

export function magnitudeMarkerColor(magnitude: number): string {
  if (magnitude >= 4.7) {
    return "#c45c26";
  }
  if (magnitude >= 4.3) {
    return "#1e3a5f";
  }
  return "#2d6a4f";
}
