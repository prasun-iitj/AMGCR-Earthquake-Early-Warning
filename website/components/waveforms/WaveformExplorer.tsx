"use client";

import { useEffect, useMemo, useState } from "react";
import { WaveformDetailsPanel } from "@/components/waveforms/WaveformDetailsPanel";
import { WaveformList } from "@/components/waveforms/WaveformList";
import { WaveformViewer } from "@/components/waveforms/WaveformViewer";
import type { LoadedWaveformExplorer, WaveformRecord } from "@/lib/waveforms/types";

type WaveformExplorerProps = {
  data: LoadedWaveformExplorer;
};

function findWaveform(
  waveforms: WaveformRecord[],
  id: string | null,
): WaveformRecord | null {
  if (!id) {
    return waveforms[0] ?? null;
  }
  return waveforms.find((waveform) => waveform.id === id) ?? waveforms[0] ?? null;
}

export function WaveformExplorer({ data }: WaveformExplorerProps) {
  const [selectedId, setSelectedId] = useState(() => {
    if (typeof window === "undefined") {
      return data.defaultWaveformId;
    }
    const hash = window.location.hash.replace("#", "");
    if (hash && data.waveforms.some((waveform) => waveform.id === hash)) {
      return hash;
    }
    return data.defaultWaveformId;
  });

  useEffect(() => {
    const applyHash = () => {
      const hash = window.location.hash.replace("#", "");
      if (hash && data.waveforms.some((waveform) => waveform.id === hash)) {
        setSelectedId(hash);
      }
    };

    window.addEventListener("hashchange", applyHash);
    return () => window.removeEventListener("hashchange", applyHash);
  }, [data.waveforms]);

  const selectedWaveform = useMemo(
    () => findWaveform(data.waveforms, selectedId),
    [data.waveforms, selectedId],
  );

  const selectWaveform = (id: string) => {
    setSelectedId(id);
    window.history.replaceState(null, "", `#${id}`);
  };

  if (!selectedWaveform) {
    return (
      <div className="border-t border-border bg-surface py-16 text-center text-sm text-text-muted">
        No waveforms discovered for active datasets. Regenerate pilot outputs per
        the reproducibility statement.
      </div>
    );
  }

  return (
    <>
      <WaveformList
        groups={data.groups}
        selectedId={selectedWaveform.id}
        onSelect={selectWaveform}
        seriesAvailableCount={data.seriesAvailableCount}
        totalWaveforms={data.totalWaveforms}
      />

      <section className="border-t border-border bg-surface-elevated py-12 md:py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid gap-10 xl:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)]">
            <WaveformViewer waveform={selectedWaveform} />
            <WaveformDetailsPanel waveform={selectedWaveform} />
          </div>
        </div>
      </section>
    </>
  );
}
