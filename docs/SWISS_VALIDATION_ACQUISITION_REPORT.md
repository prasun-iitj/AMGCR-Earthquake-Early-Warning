# Independent Swiss / adjacent-border validation acquisition (STEP 2J)

**Acquisition and structural verification only.**  
No STA/LTA was run **in this acquisition step**. Threshold **8.0** was not changed. Set C was not reselected. Frozen STA/LTA evaluation is documented separately in [SWISS_INDEPENDENT_VALIDATION_RESULTS.md](SWISS_INDEPENDENT_VALIDATION_RESULTS.md).

| Field | Value |
|-------|--------|
| Document date | 2026-09-11 |
| Dataset | **Independent Swiss/Adjacent-Border Validation Set** (locked 15 events) |
| Script | `scripts/download/download_sed_switzerland_validation.py` |
| Configuration | `configs/sed_switzerland_validation_acquisition.yaml` |
| Waveform manifest | `data/manifests/sed_switzerland_validation_waveforms.csv` |
| Pick provenance | `data/manifests/sed_switzerland_validation_picks.csv` |
| Raw MiniSEED | `data/raw/switzerland_validation/` (gitignored) |
| StationXML | `data/metadata/switzerland_validation/` (XML gitignored) |
| QC summary | `reports/switzerland_validation_acquisition/acquisition_summary.json` |
| California v1.0.0 | **Unchanged** |
| Set A (20-event development) | **Unchanged** |
| Frozen trigger_on | **8.0** (recorded, not used) |

**8.0 is the pre-declared/proposed threshold from the 20-event development dataset.** It is not an optimum and was not retuned in this step.

---

## Windows (kept distinct)

| Name | Interval | Used in STEP 2J? |
|------|----------|------------------|
| **Waveform acquisition** | origin − 60 s → origin + 90 s | **Yes** — every MiniSEED/StationXML request |
| **Detection / search** | origin → origin + 90 s | **No** — reserved for a later frozen STA/LTA step |
| **Pre-event noise / QC** | origin − 60 s → origin − 10 s | **No** — contained in the downloaded files, not treated as a detection interval |

---

## Station selection (not invented as a preference ranking)

The validation audit defined same-station CH first-P ∩ HHZ availability, but not a nearest-N or distance-bin subset.

STEP 2J therefore downloaded **HHZ for every audit-supported pair**:

- network **CH**
- channel **HHZ**
- FDSN availability covering the **acquisition** window
- station-level SED/manual first-P pick at the **same station**

Set A’s distance-bin / max-6 / HH 3C rule was **not** copied. Event-level picks were not used as a station reference.

---

## Results

| Item | Count |
|------|------:|
| Set C events attempted | **15** |
| Events with ≥1 downloaded HHZ MiniSEED | **15** |
| Events with structurally verified MiniSEED | **15** |
| Event–station HHZ records | **550** |
| MiniSEED `download_status=ok` | **550 / 550** |
| MiniSEED `verification_status=PASS` | **550 / 550** |
| Full requested-window coverage | **550 / 550** |
| Gaps | **0** |
| Overlaps | **0** |
| StationXML verified (per downloaded station/channel/interval) | **550 / 550** |
| Events without StationXML | **0** |
| Same-station SED/manual first-P references | **550 / 550** (15/15 events) |
| Failed downloads | **0** |

Unique CH stations in the waveform manifest: **79**.

Sparse-pick events were kept and fully acquired:

| Event | Same-station HHZ pairs downloaded |
|-------|----------------------------------:|
| `2024bvrces` (Imst A) | 3 (DAVOX, FUORN, LIENZ) |
| `2024ftcvhn` (Albstadt D) | 7 (BERGE, EMING, SLE, STEIN, TRULL, WALHA, WEIN2) |

QuakeML was requested with the full SED resource ID (`smi:ch.ethz.sed/...`). Short `eventid=` tokens were not relied on.

StationXML was retrieved **per downloaded** `CH.station.location.HHZ` and the acquired time interval. The earlier BALST spot-check was not used as coverage.

Raw files were stored without filtering, detrending, tapering, resampling, merging/interpolation, or response correction.

---

## Locked Set C (unchanged)

`2020flmsvb`, `2020vcnoon`, `2021ffattd`, `2021toxjpc`, `2022gzvhhy`, `2022isnvgj`, `2022ugepue`, `2023ksedgz`, `2024bvrces`, `2024cxfhdh`, `2024ftcvhn`, `2024ujblmf`, `2025phgpma`, `2025rtcqvh`, `2026bklhob`

---

## Explicitly not done

- STA/LTA
- Trigger times, detection coverage, trigger−P error, SNR, or any validation metric
- Retuning or sweeping threshold 8.0
- Reselection of Set C
- Modification of California or Set A data

The next scientific step after acquisition was STEP 2K: frozen STA/LTA evaluation on these files. See [SWISS_INDEPENDENT_VALIDATION_RESULTS.md](SWISS_INDEPENDENT_VALIDATION_RESULTS.md). Threshold 8.0 was not changed here.
