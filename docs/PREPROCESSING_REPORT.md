# PREPROCESSING_REPORT.md

**Phase B.1 — Waveform preprocessing**  
California IRIS / EarthScope pilot (8 manifest traces)

| Field | Value |
|-------|--------|
| Report date (UTC) | 2026-07-29 |
| Script | `scripts/analysis/run_california_preprocessing.py` |
| Manifest | `data/manifests/iris_california_pilot_events.csv` |
| Prior phases | [EDA_REPORT.md](EDA_REPORT.md), [SIGNAL_ANALYSIS_REPORT.md](SIGNAL_ANALYSIS_REPORT.md) |

Re-run:

```powershell
python scripts/analysis/run_california_preprocessing.py
```

Parameters are frozen in `reports/preprocessing/preprocessing_config.json`.

---

## 1. Why each step matters for EEW

| Step | EEW role |
|------|----------|
| **Remove mean (demean)** | Removes DC offset from digitizers so triggers and ML inputs reflect ground motion, not baseline drift. |
| **Linear detrend** | Removes long-period instrument/temperature trends that can masquerade as low-frequency seismic energy. |
| **Taper** | Reduces spectral leakage before filtering and avoids edge artifacts in finite windows—critical for stable band-limited onsite features. |
| **Band-pass filter** | Isolates frequency bands where P/S energy and magnitude-sensitive amplitude measures live; suppresses microseism and high-frequency noise outside the EEW decision band. |
| **Instrument response** | Converts counts to physical units (e.g. velocity) so amplitudes are comparable across stations and suitable for physics-informed ML; **required for rigorous magnitude estimation**. |
| **Peak normalization** | Puts traces on a common scale for neural models and cross-event comparison without erasing relative waveform shape (after physical units are restored). |

This pipeline is a **certificate-track research workflow** in `scripts/analysis/` and does **not** modify the EarthESND reference implementation.

---

## 2. Processing parameters

| Parameter | Value |
|-----------|--------|
| Taper | Hann, **5%** of trace length |
| Band-pass | **0.1–15 Hz** (4 corners, zero-phase); fmax capped at **0.9 × Nyquist** (15 Hz at 40 Hz sampling) |
| Response removal | EarthScope FDSN `level=response`, output **velocity**, water level **60**, pre-filter **0.08–0.1–20–25 Hz** |
| Normalization | Divide by **peak \|amplitude\|** on the filtered trace |
| SNR noise window | First **5 s** of each trace (same as Phase A.2; origin-aligned data—see limitations) |

---

## 3. Pipeline order

1. Raw (reference)  
2. Demean + linear detrend → **detrended**  
3. Taper → optional **remove_response** → **band-pass** → **filtered**  
4. Peak normalization → **normalized**

---

## 4. Instrument response — limitation

| Result | Count |
|--------|--------|
| Response applied | **0 / 8** |
| Response skipped | **8 / 8** (FDSN fetch/attach raised **`TypeError`** in this environment) |

**Effect:** All filtered waveforms remain in **digital counts** after band-pass. Figures and tables label units accordingly. For production EEW or cross-station magnitude work, store **StationXML/response** alongside MiniSEED (or use ObsPy `read_inventory` from a cached file) and re-run response removal offline.

---

## 5. Aggregate quality statistics

| Metric | Raw (before) | After filter (before norm) |
|--------|----------------|----------------------------|
| **SNR (peak)** min | 6.3 | 15.6 |
| **SNR (peak)** max | 778 | 7486 |
| **SNR (peak)** mean | 137 | 1684 |
| **SNR change ratio** (filtered/raw) | 2.5 – 27.6 (mean **17.1**) |

Per-event means, standard deviations, peaks, and RMS appear in `reports/tables/preprocessing_quality_metrics.csv`.

**Interpretation:** Band-pass filtering **reduces low-frequency drift and out-of-band noise** in the noise window, so peak-SNR computed with the fixed 0–5 s proxy often **increases sharply**. This is **not** a substitute for true pre-event noise; it shows processing sensitivity, not operational EEW detection performance.

---

## 6. Figures

Eight comparison plots in `reports/figures/`:

| File pattern | Panels |
|--------------|--------|
| `preprocessing_<short_id>.png` | Raw → Detrended → Filtered → Normalized |

Examples: `preprocessing_ci40675215.png` (largest raw amplitudes), `preprocessing_ci40699207.png` (lowest raw SNR).

---

## 7. Tables and sidecar files

| Path | Content |
|------|---------|
| `reports/tables/preprocessing_quality_metrics.csv` | Full before/after metrics per event |
| `reports/preprocessing/preprocessing_config.json` | Parameter record |
| `reports/preprocessing/preprocessing_summary.json` | Cohort aggregates |
| `reports/preprocessing/<short_id>_metrics.json` | Per-event details + response status |
| `reports/preprocessing/<short_id>_stages.npz` | Numeric arrays for each stage |

---

## 8. Effect on signal quality

**Improvements observed**

- Detrending removes slow baseline wander visible on long 300 s windows.  
- Band-pass **0.1–15 Hz** emphasizes regional P/S band energy and stabilizes amplitude statistics (lower mean offset on filtered traces).  
- Normalization yields **peak = 1** traces ready for fixed-length ML tensors.

**Limitations**

- **No response correction** in this run → amplitudes are not in velocity/acceleration for ML magnitude training.  
- **Origin-aligned windows** → noise window still contaminated on some records (Phase A.2 finding).  
- **Single BHZ component** → no vector magnitude or rotation.  
- SNR metric uses the **same 5 s noise proxy** on raw and filtered data; filtered noise RMS drops, inflating apparent SNR gain.

---

## 9. Preparation for AI-based EEW

1. **Normalized, band-limited traces** (`*_stages.npz` → `normalized`) provide a **fixed-scale input** for deep learning or reservoir computing experiments (Phase D).  
2. **Filtered (unnormalized) traces** should be used when training **amplitude-aware** models once response correction is added.  
3. Documented parameters support **reproducibility** and alignment with proposal **Methodology** text.  
4. Next steps: cache inventory, add **pre-origin download**, export **windowed arrays** around STA/LTA picks (Phase B.2 / feature extraction), then optional comparison with EarthESND reference code **without modifying** that codebase.

---

## 10. Key observations

1. Preprocessing **visually clarifies** phase arrivals on detrended/filtered panels versus raw counts.  
2. **USC** events show the largest raw peaks; **ADO** dominates the sample count.  
3. **Instrument response** must be resolved before claiming physical-amplitude EEW metrics.  
4. Peak normalization **must be applied after** SNR assessment on filtered physical/count traces (as in the CSV columns `filtered_snr_peak` vs normalized peak = 1).  
5. The workflow is **standalone and reproducible**—suitable for European pilot data reuse with the same script pattern.

---

Version: **1.0.0** (Phase B.1)
