# SED Switzerland Dataset Report

**Swiss seismic-data acquisition — methods-transfer pilot**  
**Not** an operational EEW system, **not** a trained model, and **not** a Swiss scientific performance study.

| Field | Value |
|-------|--------|
| Document date (UTC) | 2026-09-06 |
| Pipeline | `scripts/download/download_sed_switzerland_pilot.py` |
| Configuration | `configs/sed_switzerland_pilot.yaml` |
| Manifest | `data/manifests/sed_switzerland_pilot_events.csv` |
| Raw MiniSEED | `data/raw/switzerland/` (gitignored) |
| StationXML | `data/metadata/switzerland/` (XML gitignored; regenerable) |
| Logs | `logs/switzerland/sed_switzerland_pilot.log` |
| Machine-readable summary | `reports/switzerland_pilot/acquisition_summary.json` |
| California v1.0.0 | **Unchanged** |

---

## 1. Purpose

This document records the first implemented Swiss/European data step: **acquire and validate** real CH-network waveforms for twenty SED catalogue events, using a window that includes **pre-event noise**, **three-component** broadband channels, and **StationXML** response metadata.

It is a **methods-transfer pilot**: the California v1.0.0 analysis chain remains frozen. No STA/LTA, preprocessing, feature matrix, or ML is run on these Swiss files in this step.

---

## 2. Official SED/FDSN services

Endpoints used (SED/ETH EIDA; ObsPy client base `https://eida.ethz.ch`):

| Service | URL | Role |
|---------|-----|------|
| Event | https://eida.ethz.ch/fdsnws/event/1/ | SED catalogue (QuakeML/text) |
| Station | https://eida.ethz.ch/fdsnws/station/1/ | CH inventory and StationXML |
| Dataselect | https://eida.ethz.ch/fdsnws/dataselect/1/ | MiniSEED waveforms |
| Availability | https://eida.ethz.ch/fdsnws/availability/1/ | Time-span holdings (no waveform bytes) |

No USGS, EarthScope, or other catalogue was substituted. HTTP 429/503 would abort the run.

---

## 3. Event-selection policy

Twenty short event IDs were taken from the prior feasibility audit and **re-resolved** against the live SED catalogue (2020-01-01 to 2026-09-07, M ≥ 2.5, ECOS-09 box 45.4–48.3°N, 5.6–11.1°E). Hypocentres, magnitudes, and region names were **not** hard-coded.

All twenty IDs were present in the 2026-09-06 catalogue query. Event types for this set are earthquakes (SED `EventType` field). Magnitude types are `MLh` / `MLhc` as reported by SED.

---

## 4. Waveform-selection policy

For each event:

1. Query FDSN **availability** for CH broadband channels `HHZ,HHN,HHE,BHZ,BHN,BHE` over the acquisition window (stations batched).
2. Keep stations whose available spans cover origin with ≥30 s on each side at the availability layer, then prefer **complete HH 3C**, else **complete BH 3C**.
3. Attach coordinates from `fdsnws-station` and select up to **six** stations using **distance bins** (0–50, 50–100, 100–150, 150–250, 250–400 km; max two per bin), not the N nearest stations.
4. If fewer than six suitable stations exist, keep all suitable stations (no padded quota).

This run selected **six stations per event** (120 event–station rows). Unique CH stations in the manifest: **54**.

---

## 5. Acquisition window

```text
start = origin_time − 90 s
end   = origin_time + 210 s
```

This is **not** the California origin-aligned 300 s window (California starts at origin with no pre-event). Validation requires ≥60 s of **actual** MiniSEED before and after origin.

Observed on downloaded traces: pre-event **≥ 89.997 s**, post-event **≥ 209.997 s** for all 120 records.

---

## 6. Station/channel policy (as executed)

- Network: **CH** only.
- Downloaded band: **HH** three-component (`HHE`, `HHN`, `HHZ`) for all 120 records.
- Sampling rates in MiniSEED: **200 Hz** (108 records) or **120 Hz** (12 records).
- Location code: `--` (empty FDSN location) on all records.

---

## 7. StationXML strategy

For every selected station, StationXML was requested at `level=response` for the HH channels and the same time window, and written under `data/metadata/switzerland/<short_id>/`.

Association is by event ID + `CH.<STA>.--.HH.xml` next to `CH.<STA>.--.HH.<origin>.mseed`.

**120 / 120** records have `stationxml_available=YES`. Full `remove_response()` on the whole archive is **out of scope** for this step (see §10).

---

## 8. Actual acquisition results (2026-09-06 run)

| Quantity | Count |
|----------|------:|
| Candidate events | 20 |
| Events found in SED catalogue | 20 |
| Events with ≥1 validated MiniSEED | 20 |
| Event–station waveform records | 120 |
| `download_status=OK` | 120 |
| MiniSEED validation `PASS` | 120 |
| Complete HH 3C | 120 |
| Pre-event ≥ 60 s (actual traces) | 120 |
| StationXML YES | 120 |
| Failed / discarded records | 0 |

Raw files were not edited after download. Duplicate scientific rows were not created (one MiniSEED per event–station).

---

## 9. Failed / unavailable records

**No event–station download or MiniSEED validation failures** in this run.

Availability **batch timeouts** occurred on some CH station groups (logged; HTTP 0 / `TimeoutError`). Those batches were skipped; selection continued on stations with a successful availability response. This can omit stations from a timed-out batch but does **not** invent holdings. Example log: stations `SULZ,TORNY,TRULL,VANNI,VDL,VDR,VINZL,VMV` timed out for several 2025–2026 events.

---

## 10. Response-test results

Technical `Stream.remove_response()` only, on **3 events × 3 stations** (9 tests). Raw MiniSEED was not overwritten. Output target: velocity (`VEL`), water level 60, `pre_filt` 0.08–0.1–20–25 Hz.

| Event | Station | Channels | Units before | Units after | Status |
|-------|---------|----------|--------------|-------------|--------|
| 2020btnrcj | EMBD | HHE;HHN;HHZ | counts | m/s | PASS |
| 2020btnrcj | VANNI | HHE;HHN;HHZ | counts | m/s | PASS |
| 2020btnrcj | JAUN | HHE;HHN;HHZ | counts | m/s | PASS |
| 2022rvutkg | HAUIG | HHE;HHN;HHZ | counts | m/s | PASS |
| 2022rvutkg | MUTEZ | HHE;HHN;HHZ | counts | m/s | PASS |
| 2022rvutkg | SULZ | HHE;HHN;HHZ | counts | m/s | PASS |
| 2025ovpxfj | ZUR | HHE;HHN;HHZ | counts | m/s | PASS |
| 2025ovpxfj | DAGMA | HHE;HHN;HHZ | counts | m/s | PASS |
| 2025ovpxfj | SLE | HHE;HHN;HHZ | counts | m/s | PASS |

JSON: `reports/switzerland_pilot/response_test.json`.

This demonstrates that **instrument correction can be executed** on the Swiss files with locally saved StationXML. It is **not** Swiss scientific preprocessing and **not** a comparison to California SNR or features.

---

## 11. Reproducibility

From the repository root (Python 3.11+, ObsPy as in `pyproject.toml`):

```powershell
python scripts/download/download_sed_switzerland_pilot.py --config configs/sed_switzerland_pilot.yaml
python -m pytest tests/test_switzerland_pilot.py
```

Re-running Step 0 may change which CH stations fall in each distance bin if availability or inventory changes; the **published manifest** records the 2026-09-06 download.

California commands, manifests, and analysis scripts are separate and must not be used for this dataset.

---

## 12. Limitations

1. **Acquisition only** — no Swiss EDA, STA/LTA, preprocessing, or feature matrix.
2. **HH preferred** — BH 3C was allowed by policy but unused because HH 3C was available for selected stations.
3. **Availability timeouts** — some station batches were skipped; the 54 stations in the manifest are those successfully queried and selected, not a complete CH snapshot.
4. **Magnitude types** `MLh`/`MLhc` are not moment magnitude; they are not interchangeable with California `mw`/`ml` labels.
5. **Sampling rate** is mixed (120 Hz vs 200 Hz) among HH channels.
6. **No operational EEW claim** — no warning times, false-alarm rates, or magnitude estimates.
7. **No ML** — no training or evaluation on Swiss waveforms.
8. Raw MiniSEED and StationXML are local/gitignored; a fresh clone must re-run the download script.

---

Version: **0.1.0** (Swiss methods-transfer acquisition; California v1.0.0 frozen)
