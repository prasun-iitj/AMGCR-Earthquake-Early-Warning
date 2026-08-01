"use client";

import { useEffect } from "react";
import {
  CircleMarker,
  MapContainer,
  Popup,
  TileLayer,
  useMap,
} from "react-leaflet";
import type { LatLngBoundsExpression } from "leaflet";
import {
  magnitudeMarkerColor,
  magnitudeMarkerRadius,
} from "@/lib/map/registry";
import type { MapEvent } from "@/lib/map/types";
import "leaflet/dist/leaflet.css";

type EarthquakeMapProps = {
  events: MapEvent[];
  selectedId: string | null;
  center: [number, number];
  zoom: number;
  onSelect: (id: string) => void;
};

function FitBounds({ events }: { events: MapEvent[] }) {
  const map = useMap();

  useEffect(() => {
    if (events.length === 0) {
      return;
    }

    if (events.length === 1) {
      map.setView([events[0].latitude, events[0].longitude], 8);
      return;
    }

    const bounds: LatLngBoundsExpression = events.map((event) => [
      event.latitude,
      event.longitude,
    ]);
    map.fitBounds(bounds, { padding: [40, 40], maxZoom: 8 });
  }, [events, map]);

  return null;
}

function formatOriginTime(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toISOString().replace("T", " ").slice(0, 19);
}

export function EarthquakeMap({
  events,
  selectedId,
  center,
  zoom,
  onSelect,
}: EarthquakeMapProps) {
  return (
    <MapContainer
      center={center}
      zoom={zoom}
      scrollWheelZoom
      className="h-[420px] w-full rounded-xl border border-border md:h-[520px] lg:h-[620px]"
      aria-label="Earthquake event map"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <FitBounds events={events} />
      {events.map((event) => {
        const isSelected = event.id === selectedId;

        return (
          <CircleMarker
            key={event.id}
            center={[event.latitude, event.longitude]}
            radius={magnitudeMarkerRadius(event.magnitude)}
            pathOptions={{
              color: isSelected ? "#c45c26" : magnitudeMarkerColor(event.magnitude),
              fillColor: magnitudeMarkerColor(event.magnitude),
              fillOpacity: isSelected ? 0.95 : 0.75,
              weight: isSelected ? 3 : 2,
            }}
            eventHandlers={{
              click: () => onSelect(event.id),
            }}
          >
            <Popup>
              <div className="space-y-1 text-sm">
                <p className="font-semibold">{event.id}</p>
                <p>M{event.magnitude.toFixed(2)} · {event.stationId}</p>
                <p>{formatOriginTime(event.originTimeUtc)} UTC</p>
                <button
                  type="button"
                  onClick={() => onSelect(event.id)}
                  className="mt-2 text-primary underline"
                >
                  View details
                </button>
              </div>
            </Popup>
          </CircleMarker>
        );
      })}
    </MapContainer>
  );
}
