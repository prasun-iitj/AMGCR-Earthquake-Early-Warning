import type { MapEvent, MapFilterState } from "@/lib/map/types";

/** Client-safe static filter — reused by Phase 9 dashboard. */
export function filterMapEvents(
  events: MapEvent[],
  filters: MapFilterState,
): MapEvent[] {
  const timeStart = new Date(`${filters.timeStart}T00:00:00`).getTime();
  const timeEnd = new Date(`${filters.timeEnd}T23:59:59`).getTime();

  return events.filter((event) => {
    if (filters.dataset !== "all" && event.datasetId !== filters.dataset) {
      return false;
    }

    if (
      event.magnitude < filters.magnitudeMin ||
      event.magnitude > filters.magnitudeMax
    ) {
      return false;
    }

    const eventTime = new Date(event.originTimeUtc).getTime();
    if (Number.isNaN(eventTime) || eventTime < timeStart || eventTime > timeEnd) {
      return false;
    }

    return true;
  });
}
