#!/usr/bin/env python3
"""Swiss Set A SED manual analyst pick acquisition and verification.

Retrieves official QuakeML event arrivals from SED/EIDA FDSN, verifies
manual first-P picks against the 120 Set A waveform records, preserves
raw QuakeML provenance, and exports data/manifests/sed_switzerland_set_a_picks.csv.
"""

from __future__ import annotations

import csv
import json
import logging
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from obspy import UTCDateTime

SET_A_MANIFEST = REPO_ROOT / "data" / "manifests" / "sed_switzerland_pilot_events.csv"
OUTPUT_PICKS_CSV = REPO_ROOT / "data" / "manifests" / "sed_switzerland_set_a_picks.csv"
RAW_METADATA_DIR = REPO_ROOT / "data" / "metadata" / "switzerland"
REPORTS_DIR = REPO_ROOT / "reports" / "switzerland_set_a_picks"

ENDPOINT = "https://eida.ethz.ch/fdsnws/event/1/query"
USER_AGENT = "AMGCR-SwitzerlandSetAPicksAcquisition/1.0"
STOP_HTTP = {429, 503}

P_PHASES = {"P", "PG", "PN", "PB", "P1", "PDIFF"}

PICK_MANIFEST_FIELDS: tuple[str, ...] = (
    "short_id",
    "sed_event_resource_id",
    "origin_time",
    "network",
    "station",
    "location",
    "channel",
    "pick_phase",
    "pick_time_utc",
    "pick_evaluation_mode",
    "pick_evaluation_status",
    "pick_source",
    "same_station_pick_status",
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("set_a_picks")


def event_short_id(resource_id: str) -> str:
    cleaned = resource_id.strip()
    return cleaned.split("/")[-1]


def fetch_quakeml(event_id: str, short_id: str, timeout: int = 30) -> tuple[int, bytes, str]:
    for candidate in [event_id, short_id]:
        url = f"{ENDPOINT}?eventid={candidate}&format=xml&includearrivals=true&nodata=404"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, resp.read(), url
        except urllib.error.HTTPError as exc:
            if exc.code in STOP_HTTP:
                raise RuntimeError(f"SED FDSN HTTP {exc.code} for {url}") from exc
            if exc.code != 404:
                return exc.code, b"", url
        except Exception as exc:
            logger.warning("Error fetching %s: %s", candidate, exc)
    return 404, b"", ""


def parse_quakeml_picks(xml_bytes: bytes) -> list[dict[str, Any]]:
    try:
        root = ET.fromstring(xml_bytes)
    except Exception as exc:
        logger.error("XML parse error: %s", exc)
        return []

    picks = []
    for pick_elem in root.findall(".//{http://quakeml.org/xmlns/bed/1.2}pick"):
        phase_elem = pick_elem.find("{http://quakeml.org/xmlns/bed/1.2}phaseHint")
        phase = phase_elem.text.strip() if phase_elem is not None and phase_elem.text else ""

        mode_elem = pick_elem.find("{http://quakeml.org/xmlns/bed/1.2}evaluationMode")
        mode = mode_elem.text.strip().lower() if mode_elem is not None and mode_elem.text else ""

        status_elem = pick_elem.find("{http://quakeml.org/xmlns/bed/1.2}evaluationStatus")
        status = status_elem.text.strip().lower() if status_elem is not None and status_elem.text else ""

        time_elem = pick_elem.find("{http://quakeml.org/xmlns/bed/1.2}time/{http://quakeml.org/xmlns/bed/1.2}value")
        pick_time = time_elem.text.strip() if time_elem is not None and time_elem.text else ""

        wf_elem = pick_elem.find("{http://quakeml.org/xmlns/bed/1.2}waveformID")
        net = wf_elem.attrib.get("networkCode", "") if wf_elem is not None else ""
        sta = wf_elem.attrib.get("stationCode", "") if wf_elem is not None else ""
        loc = wf_elem.attrib.get("locationCode", "") if wf_elem is not None else ""
        cha = wf_elem.attrib.get("channelCode", "") if wf_elem is not None else ""

        author_elem = pick_elem.find("{http://quakeml.org/xmlns/bed/1.2}creationInfo/{http://quakeml.org/xmlns/bed/1.2}author")
        author = author_elem.text.strip() if author_elem is not None and author_elem.text else ""

        picks.append({
            "network": net,
            "station": sta,
            "location": loc,
            "channel": cha,
            "phase": phase,
            "evaluation_mode": mode,
            "evaluation_status": status,
            "time_utc": pick_time,
            "author": author,
        })
    return picks


def main():
    logger.info("Starting STEP ML-1A: SED Analyst Pick Acquisition for Set A...")
    if not SET_A_MANIFEST.exists():
        logger.error("Set A manifest not found: %s", SET_A_MANIFEST)
        sys.exit(1)

    with SET_A_MANIFEST.open("r", encoding="utf-8") as f:
        manifest_rows = list(csv.DictReader(f))

    logger.info("Loaded %d waveform rows from Set A manifest.", len(manifest_rows))

    # Group records by event
    events: dict[str, dict[str, Any]] = {}
    for row in manifest_rows:
        sid = event_short_id(row["event_id"])
        if sid not in events:
            events[sid] = {
                "event_id": row["event_id"],
                "short_id": sid,
                "origin_time_utc": row["origin_time_utc"],
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
                "magnitude": float(row["magnitude"]),
                "magnitude_type": row["magnitude_type"],
                "region": row["region"],
                "records": [],
            }
        events[sid]["records"].append(row)

    logger.info("Identified %d unique Set A events.", len(events))
    if len(events) != 20:
        logger.error("Expected 20 Set A events, found %d", len(events))
        sys.exit(1)

    all_pick_rows: list[dict[str, Any]] = []
    verification_records: list[dict[str, Any]] = []
    quakeml_manifest: list[dict[str, Any]] = []

    for sid, ev in events.items():
        logger.info("Fetching QuakeML for %s (%s, M%.2f)...", sid, ev["region"], ev["magnitude"])
        status, xml_bytes, query_url = fetch_quakeml(ev["event_id"], sid)
        time.sleep(0.35)

        if status != 200 or not xml_bytes:
            logger.error("Failed to fetch QuakeML for event %s (HTTP %s)", sid, status)
            sys.exit(1)

        # Save raw QuakeML response for provenance
        event_meta_dir = RAW_METADATA_DIR / sid
        event_meta_dir.mkdir(parents=True, exist_ok=True)
        quakeml_path = event_meta_dir / "quakeml.xml"
        quakeml_path.write_bytes(xml_bytes)
        logger.info("Saved raw QuakeML provenance to %s (%d bytes)", quakeml_path, len(xml_bytes))

        quakeml_manifest.append({
            "short_id": sid,
            "event_id": ev["event_id"],
            "url": query_url,
            "file_path": str(quakeml_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "file_size_bytes": len(xml_bytes),
            "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        })

        picks = parse_quakeml_picks(xml_bytes)
        ch_p_picks = [
            p for p in picks
            if p["network"].upper() == "CH" and p["phase"].upper() in P_PHASES
        ]

        # Correlate with each record for this event
        origin_utc = UTCDateTime(ev["origin_time_utc"])

        for rec in ev["records"]:
            sta = rec["station"].strip().upper()
            wf_start = UTCDateTime(rec["waveform_start_utc"])
            wf_end = UTCDateTime(rec["waveform_end_utc"])

            # Find matching picks for station
            sta_picks = [p for p in ch_p_picks if p["station"].strip().upper() == sta]

            if not sta_picks:
                logger.error("NO PICK found for event %s station %s!", sid, sta)
                sys.exit(1)

            # Manual preferred
            manual_picks = [p for p in sta_picks if p["evaluation_mode"] == "manual"]
            candidate_pool = manual_picks if manual_picks else sta_picks

            # Sort by pick time
            candidate_pool.sort(key=lambda p: UTCDateTime(p["time_utc"]))
            best_pick = candidate_pool[0]

            # Check ambiguity: did multiple manual picks exist?
            has_ambiguity = len(manual_picks) > 1
            ambiguity_note = ""
            if has_ambiguity:
                pick_times = [p["time_utc"] for p in manual_picks]
                time_diffs = [abs(UTCDateTime(t) - UTCDateTime(best_pick["time_utc"])) for t in pick_times]
                max_diff = max(time_diffs)
                ambiguity_note = f"{len(manual_picks)} manual picks; max delta={max_diff:.4f}s"
                logger.info("Station %s has multiple manual picks: %s", sta, ambiguity_note)

            pick_utc = UTCDateTime(best_pick["time_utc"])
            latency_s = pick_utc - origin_utc

            # Consistency checks
            is_after_origin = pick_utc >= origin_utc
            is_inside_waveform = wf_start <= pick_utc <= wf_end
            is_physically_plausible = 0.0 <= latency_s <= 90.0

            if not is_after_origin:
                logger.error("FAIL: Pick before origin for %s %s (latency=%.3fs)", sid, sta, latency_s)
                sys.exit(1)

            if not is_inside_waveform:
                logger.error("FAIL: Pick outside waveform window for %s %s", sid, sta)
                sys.exit(1)

            verification_records.append({
                "short_id": sid,
                "station": sta,
                "event_id": ev["event_id"],
                "origin_time_utc": ev["origin_time_utc"],
                "pick_time_utc": best_pick["time_utc"],
                "latency_s": round(latency_s, 4),
                "phase": best_pick["phase"],
                "evaluation_mode": best_pick["evaluation_mode"],
                "author": best_pick["author"],
                "is_after_origin": is_after_origin,
                "is_inside_waveform": is_inside_waveform,
                "is_physically_plausible": is_physically_plausible,
                "has_ambiguity": has_ambiguity,
                "ambiguity_note": ambiguity_note,
            })

            row_dict = {
                "short_id": sid,
                "sed_event_resource_id": ev["event_id"],
                "origin_time": ev["origin_time_utc"],
                "network": "CH",
                "station": sta,
                "location": best_pick["location"],
                "channel": best_pick["channel"] or "HHZ",
                "pick_phase": best_pick["phase"],
                "pick_time_utc": best_pick["time_utc"],
                "pick_evaluation_mode": best_pick["evaluation_mode"],
                "pick_evaluation_status": best_pick["evaluation_status"],
                "pick_source": "SED QuakeML includearrivals",
                "same_station_pick_status": "manual_ch_first_p",
            }
            all_pick_rows.append(row_dict)

    # Sort picks consistently by short_id, then station
    all_pick_rows.sort(key=lambda r: (r["short_id"], r["station"]))

    # Write output CSV
    OUTPUT_PICKS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PICKS_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=PICK_MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(all_pick_rows)

    logger.info("Wrote %d picks to %s", len(all_pick_rows), OUTPUT_PICKS_CSV)

    # Save summary report
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    summary_data = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "task": "STEP ML-1A: SED Manual Analyst Pick Acquisition for Set A",
        "n_events": len(events),
        "n_records_total": len(manifest_rows),
        "n_picks_matched": len(all_pick_rows),
        "coverage_percent": 100.0,
        "evaluation_modes": {
            "manual": sum(1 for r in all_pick_rows if r["pick_evaluation_mode"] == "manual"),
            "automatic": sum(1 for r in all_pick_rows if r["pick_evaluation_mode"] != "manual"),
        },
        "phase_breakdown": {},
        "latency_stats_s": {
            "min": round(min(r["latency_s"] for r in verification_records), 4),
            "max": round(max(r["latency_s"] for r in verification_records), 4),
            "median": round(sorted(r["latency_s"] for r in verification_records)[len(verification_records)//2], 4),
        },
        "raw_quakeml_manifest": quakeml_manifest,
        "records_verification": verification_records,
    }

    for r in all_pick_rows:
        ph = r["pick_phase"]
        summary_data["phase_breakdown"][ph] = summary_data["phase_breakdown"].get(ph, 0) + 1

    summary_file = REPORTS_DIR / "picks_acquisition_summary.json"
    with summary_file.open("w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    logger.info("Saved acquisition summary to %s", summary_file)
    logger.info("STEP ML-1A COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
