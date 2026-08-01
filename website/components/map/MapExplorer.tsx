"use client";

import dynamic from "next/dynamic";
import { useEffect, useMemo, useState } from "react";
import { EventDetailsPanel } from "@/components/map/EventDetailsPanel";
import { MapFilters } from "@/components/map/MapFilters";
import { filterMapEvents } from "@/lib/map/filters";
import type { LoadedMapExplorer, MapEvent, MapFilterState } from "@/lib/map/types";

const EarthquakeMap = dynamic(
  () =>
    import("@/components/map/EarthquakeMap").then((module) => module.EarthquakeMap),
  {
    ssr: false,
    loading: () => (
      <div className="flex h-[420px] items-center justify-center rounded-xl border border-dashed border-border bg-surface text-sm text-text-muted md:h-[520px] lg:h-[620px]">
        Loading map…
      </div>
    ),
  },
);

type MapExplorerProps = {
  data: LoadedMapExplorer;
};

function findEvent(events: MapEvent[], id: string | null): MapEvent | null {
  if (!id) {
    return events[0] ?? null;
  }
  return events.find((event) => event.id === id) ?? events[0] ?? null;
}

export function MapExplorer({ data }: MapExplorerProps) {
  const [filters, setFilters] = useState<MapFilterState>(data.defaultFilter);
  const [selectedId, setSelectedId] = useState<string | null>(() => {
    if (typeof window === "undefined") {
      return data.defaultSelectedId;
    }
    const hash = window.location.hash.replace("#", "");
    if (hash && data.events.some((event) => event.id === hash)) {
      return hash;
    }
    return data.defaultSelectedId;
  });
  const [mobileDetailsOpen, setMobileDetailsOpen] = useState(true);

  useEffect(() => {
    const applyHash = () => {
      const hash = window.location.hash.replace("#", "");
      if (hash && data.events.some((event) => event.id === hash)) {
        setSelectedId(hash);
        setMobileDetailsOpen(true);
      }
    };

    window.addEventListener("hashchange", applyHash);
    return () => window.removeEventListener("hashchange", applyHash);
  }, [data.events]);

  const filteredEvents = useMemo(
    () => filterMapEvents(data.events, filters),
    [data.events, filters],
  );

  const effectiveSelectedId = useMemo(() => {
    if (selectedId && filteredEvents.some((event) => event.id === selectedId)) {
      return selectedId;
    }
    return filteredEvents[0]?.id ?? null;
  }, [filteredEvents, selectedId]);

  const selectedEvent = useMemo(
    () => findEvent(filteredEvents, effectiveSelectedId),
    [filteredEvents, effectiveSelectedId],
  );

  const handleFilterChange = (nextFilters: MapFilterState) => {
    setFilters(nextFilters);
    const nextFiltered = filterMapEvents(data.events, nextFilters);
    if (
      selectedId &&
      !nextFiltered.some((event) => event.id === selectedId) &&
      nextFiltered[0]
    ) {
      setSelectedId(nextFiltered[0].id);
      window.history.replaceState(null, "", `#${nextFiltered[0].id}`);
    }
  };

  const selectEvent = (id: string) => {
    setSelectedId(id);
    setMobileDetailsOpen(true);
    window.history.replaceState(null, "", `#${id}`);
  };

  const resetFilters = () => {
    setFilters(data.defaultFilter);
  };

  if (data.events.length === 0) {
    return (
      <div className="border-t border-border bg-surface py-16 text-center text-sm text-text-muted">
        No geolocated events discovered. Regenerate pilot outputs per the
        reproducibility statement.
      </div>
    );
  }

  return (
    <section className="border-t border-border bg-surface py-12 md:py-16">
      <div className="mx-auto max-w-7xl space-y-6 px-4 sm:px-6 lg:px-8">
        <MapFilters
          filters={filters}
          bounds={data.filterBounds}
          datasetOptions={data.datasetOptions}
          visibleCount={filteredEvents.length}
          totalCount={data.events.length}
          onChange={handleFilterChange}
          onReset={resetFilters}
        />

        <div className="grid gap-6 xl:grid-cols-[minmax(0,1.5fr)_minmax(0,1fr)]">
          <div className="min-w-0">
            {filteredEvents.length > 0 ? (
              <EarthquakeMap
                events={filteredEvents}
                selectedId={effectiveSelectedId}
                center={data.mapCenter}
                zoom={data.mapZoom}
                onSelect={selectEvent}
              />
            ) : (
              <div className="flex h-[420px] items-center justify-center rounded-xl border border-dashed border-border bg-surface-elevated text-sm text-text-muted md:h-[520px]">
                No events match the current filters.
              </div>
            )}
            <p className="mt-3 text-xs text-text-muted">
              Map tiles © OpenStreetMap contributors · Marker size scales with magnitude
            </p>
          </div>

          <div className="hidden xl:block">
            <div className="sticky top-24">
              <EventDetailsPanel event={selectedEvent} />
            </div>
          </div>
        </div>

        <div className="xl:hidden">
          <button
            type="button"
            onClick={() => setMobileDetailsOpen((open) => !open)}
            className="flex w-full items-center justify-between rounded-xl border border-border bg-surface-elevated px-4 py-3 text-left"
            aria-expanded={mobileDetailsOpen}
          >
            <span className="font-medium text-text">
              {selectedEvent
                ? `Event details · ${selectedEvent.id}`
                : "Event details"}
            </span>
            <span className="text-sm text-text-muted">
              {mobileDetailsOpen ? "Hide" : "Show"}
            </span>
          </button>
          {mobileDetailsOpen ? (
            <div className="mt-4">
              <EventDetailsPanel event={selectedEvent} compact />
            </div>
          ) : null}
        </div>
      </div>
    </section>
  );
}
