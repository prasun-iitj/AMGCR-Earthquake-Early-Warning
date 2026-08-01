"use client";

import { useEffect, useMemo, useState } from "react";
import { DatasetCardGrid } from "@/components/dataset/DatasetCardGrid";
import { DatasetDetailsPanel } from "@/components/dataset/DatasetDetailsPanel";
import { DatasetDownloads } from "@/components/dataset/DatasetDownloads";
import { DatasetOverview } from "@/components/dataset/DatasetOverview";
import type { LoadedDatasetExplorer } from "@/lib/dataset/types";

type DatasetExplorerProps = {
  data: LoadedDatasetExplorer;
};

export function DatasetExplorer({ data }: DatasetExplorerProps) {
  const [selectedId, setSelectedId] = useState(() => {
    if (typeof window === "undefined") {
      return data.defaultDatasetId;
    }
    const hash = window.location.hash.replace("#", "");
    if (hash && data.datasets.some((dataset) => dataset.id === hash)) {
      return hash;
    }
    return data.defaultDatasetId;
  });

  useEffect(() => {
    const applyHash = () => {
      const hash = window.location.hash.replace("#", "");
      if (hash && data.datasets.some((dataset) => dataset.id === hash)) {
        setSelectedId(hash);
      }
    };

    window.addEventListener("hashchange", applyHash);
    return () => window.removeEventListener("hashchange", applyHash);
  }, [data.datasets]);

  const selectedDataset = useMemo(
    () =>
      data.datasets.find((dataset) => dataset.id === selectedId) ??
      data.datasets[0],
    [data.datasets, selectedId],
  );

  const selectDataset = (id: string) => {
    setSelectedId(id);
    window.history.replaceState(null, "", `#${id}`);
  };

  return (
    <>
      {selectedDataset.status === "active" && (
        <DatasetOverview dataset={selectedDataset} />
      )}

      <DatasetCardGrid
        registry={data.registry}
        selectedId={selectedId}
        onSelect={selectDataset}
      />

      <DatasetDetailsPanel dataset={selectedDataset} />

      {selectedDataset.status === "active" && (
        <DatasetDownloads dataset={selectedDataset} />
      )}
    </>
  );
}
