# FEATURE_ENGINEERING_REPORT.md

**Phase B.2 — Feature engineering**  
California IRIS pilot (filtered traces from Phase B.1)

| Field | Value |
|-------|--------|
| Report date (UTC) | 2026-07-29 |
| Script | `scripts/analysis/run_california_feature_engineering.py` |
| Input data | `reports/preprocessing/<short_id>_stages.npz` → **`filtered`** array |
| P-wave times | `reports/signal_analysis/<short_id>_metrics.json` (Phase A.2) |
| Preprocessing context | [PREPROCESSING_REPORT.md](PREPROCESSING_REPORT.md) |

Re-run:

```powershell
python scripts/analysis/run_california_feature_engineering.py
```

---

## 1. Feature matrix

| Property | Value |
|----------|--------|
| **Events (rows)** | **8** |
| **Extracted features (columns)** | **18** |
| **Matrix shape** | **8 × 18** (+ metadata columns in CSV) |
| **Primary file** | `reports/features/feature_matrix.csv` |
| **Summary** | `reports/features/feature_summary.json` |

Metadata columns in CSV: `event_id`, `short_id`, `station_id`, `magnitude`, `magnitude_type`, `sampling_rate_hz`, `p_pick_source`.

---

## 2. Feature catalogue and EEW relevance

### 2.1 Time-domain (9)

| Feature | EEW relevance | Robustness (this pilot) |
|---------|---------------|-------------------------|
| **peak_amplitude** | Onsite shaking strength; correlates with damage/alert tiers when calibrated in physical units. | **Exploratory** — counts, station gain dominates. |
| **peak_to_peak_amplitude** | Full swing of motion; sensitive to low-frequency drift if detrend incomplete. | Exploratory |
| **rms** | Average energy in window; stable summary for ML inputs. | Moderate |
| **variance / std** | Spread of amplitude; complements RMS for anomaly detection. | Moderate (redundant with RMS) |
| **zero_crossing_rate_hz** | Rough frequency content proxy; fast estimate for embedded systems. | **Robust** shape statistic (less gain-sensitive when normalized) |
| **signal_energy** | ∫x² dt proxy; related to intensity measures. | Exploratory (counts²) |
| **signal_entropy** | Complexity of amplitude distribution; may separate impulsive P vs noisy coda. | **Robust** as relative metric |
| **crest_factor** | Peak/RMS; impulsiveness indicator for P arrivals. | **Robust** for ranking events |

### 2.2 Frequency-domain (5 + FFT figures)

Computed from **one-sided FFT power** of the filtered trace. **FFT spectra** are plotted (not stored as matrix columns).

| Feature | EEW relevance | Robustness |
|---------|---------------|------------|
| **dominant_frequency_hz** | Highlights prevailing oscillation; shifts with magnitude/distance in theory. | Exploratory (N=8, single component) |
| **spectral_centroid_hz** | “Center of mass” of spectrum — timbre of shaking. | Moderate |
| **spectral_bandwidth_hz** | Spectral spread; wider often means richer coda. | Moderate |
| **spectral_rolloff_95_hz** | Frequency below 95% energy — high-frequency content indicator. | Moderate |
| **spectral_entropy** | Disorder in spectrum; useful for ML diversity. | **Robust** relative measure |

### 2.3 Earthquake-related (4)

| Feature | EEW relevance | Robustness |
|---------|---------------|------------|
| **p_arrival_time_s** | Warning time budget; from Phase A.2 STA/LTA (approximate). | Exploratory pick quality |
| **signal_duration_s** | Coda length above noise threshold post-P; shaking duration proxy. | Moderate |
| **pgm_proxy_counts** | max \|filtered\| in **counts** — **not** true PGA/PGV without response removal. | Exploratory |
| **arias_intensity_counts2_s_proxy** | ∑x²/fs in **counts²·s** — **not** standard Arias (needs acceleration in g). | Exploratory |

**Arias limitation:** Standard Arias intensity is \(I_a = \frac{\pi}{2g} \int a(t)^2 dt\). Here we report a **counts-based proxy** for relative ranking only, not physical hazard.

---

## 3. Why these features for AI-based EEW

1. **Multi-domain vectors** (time + frequency + onset timing) mirror onsite EEW pipelines that fuse amplitude, frequency, and pick latency before magnitude estimation.  
2. **Normalized-ready inputs:** combine with B.1 `normalized` arrays for neural nets; use this matrix for **tabular baselines** (random forest, linear regression on magnitude).  
3. **Crest factor, spectral centroid, entropy** tend to **generalize better** across stations than raw peaks when response is missing.  
4. **P arrival and duration** link features to **warning time** narratives in the proposal.  
5. Phase D can compare these Western features against **EarthESND reference** feature sets without modifying that codebase.

---

## 4. Visualisations

| Figure | Path | Description |
|--------|------|-------------|
| FFT spectra | `reports/figures/feature_engineering_fft_spectra.png` | Log-power vs frequency per event (filtered trace) |
| Correlation heatmap | `reports/figures/feature_correlation_heatmap.png` | 18×18 Pearson matrix (8 samples) |
| Distributions | `reports/figures/feature_distributions.png` | Histogram per feature |
| Boxplots | `reports/figures/feature_boxplots_by_station.png` | ADO vs USC for five key features |

Table: `reports/tables/feature_correlation_matrix.csv` (duplicate matrix path in `reports/tables/feature_matrix.csv`).

---

## 5. Aggregate statistics (pilot)

| Feature | Mean (approx.) | Notes |
|---------|----------------|--------|
| Dominant frequency | 2.6 Hz | Dominated by band-pass 0.1–15 Hz |
| Spectral centroid | 2.3 Hz | Similar scale |
| Crest factor | 11.4 | High impulsiveness on some traces |
| P arrival time | 31.3 s | Catalog-origin window; not travel-time validated |
| Signal duration | 234.6 s | Long coda above noise threshold |

See `feature_summary.json` for full means/stds.

---

## 6. Pilot limitations

1. **N = 8** — correlation heatmap and distributions are **illustrative**, not statistically stable.  
2. **Counts, no response** — peak, PGM proxy, Arias proxy **not physical**.  
3. **Single BHZ** — no vector intensity or MMI calibration.  
4. **Perfect correlation:** `peak_amplitude` ≡ `pgm_proxy_counts`; `signal_energy` ≡ `arias_intensity_counts2_s_proxy` (by definition here).  
5. **Filtered trace dependency** — features change if B.1 parameters change; matrix is versioned by preprocessing config.

---

## 7. Readiness for AI models

| Ready now | Needs more work |
|-----------|-----------------|
| Fixed-length **normalized** waveforms (B.1 NPZ) + this **18-D tabular** sidecar | Physical units + more events |
| **Crest factor, entropies, ZCR, spectral shape** for small-N exploration | Train/val split meaningless at N=8 |
| **Magnitude as label** for proof-of-concept regression demos | European data + held-out regions |
| Export to CSV for **scikit-learn** / **pandas** pipelines | Deep learning at scale |

Recommended Phase D path: accumulate **≥50–100** Western events, add response correction, then train with **normalized windows** around `p_arrival_time_s` and optional fusion with this feature matrix.

---

## 8. Output index

| Path | Type |
|------|------|
| `reports/features/feature_matrix.csv` | Main matrix |
| `reports/features/feature_summary.json` | Summary stats |
| `reports/features/per_event_features.json` | JSON dict by event |
| `reports/features/run_metadata.json` | Run index |
| `reports/tables/feature_matrix.csv` | Copy for tables folder |
| `reports/tables/feature_correlation_matrix.csv` | Correlation table |
| `docs/FEATURE_ENGINEERING_REPORT.md` | This document |

---

Version: **1.0.0** (Phase B.2)
