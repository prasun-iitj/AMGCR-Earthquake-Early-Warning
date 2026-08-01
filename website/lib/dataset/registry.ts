import type { DatasetRegistryEntry } from "@/lib/dataset/types";

/** Central dataset registry — add future datasets here without component changes. */
export const datasetRegistry: DatasetRegistryEntry[] = [
  {
    id: "california-pilot",
    name: "California Pilot",
    region: "United States (California)",
    status: "active",
    teaser:
      "Completed IRIS/EarthScope pilot with eight events, ObsPy acquisition, and full analysis pipeline.",
  },
  {
    id: "europe-future",
    name: "Europe (ORFEUS / EIDA)",
    region: "Europe",
    status: "planned",
    teaser:
      "Planned expansion to European FDSN archives following the same manifest-and-report pattern.",
  },
  {
    id: "japan-reference",
    name: "Japan (EarthESND Reference)",
    region: "Japan",
    status: "planned",
    teaser:
      "Optional K-NET-scale reference track aligned with EarthESND literature benchmarks.",
  },
  {
    id: "additional-pilots",
    name: "Additional Western Pilots",
    region: "Western USA / scalable catalogues",
    status: "planned",
    teaser:
      "Future scaled catalogues for stratified magnitude, distance, and azimuth sampling.",
  },
];

export function getRegistryEntry(id: string): DatasetRegistryEntry | undefined {
  return datasetRegistry.find((entry) => entry.id === id);
}

export const defaultDatasetId = "california-pilot";
