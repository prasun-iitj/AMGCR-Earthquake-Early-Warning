# Data Dictionary

Definitions are taken from the code that produces each column (`scripts/analysis/run_swiss_set_a_feature_engineering.py`, `run_swiss_set_c_feature_engineering.py`, `run_california_feature_engineering.py`, the download scripts) and from the committed file headers. Counts: `reports/data_lineage/data_lineage_summary.json`. Narrative: [DATA_COLLECTION_AND_ANALYSIS_REPORT.md](DATA_COLLECTION_AND_ANALYSIS_REPORT.md).

## 1. Datasets and files

| Dataset | Files | Format | Location | Published |
|---|---|---|---|---|
| California pilot | 8 MiniSEED listed in `data/manifests/iris_california_pilot_events.csv` | MiniSEED, counts, 40 Hz, `CI.<ADO|USC>.--.BHZ` | `data/raw/iris/` | manifest only |
| Swiss Set A | 120 MiniSEED (3 components per file), 120 StationXML, 20 QuakeML | MiniSEED, StationXML, QuakeML | `data/raw/switzerland/`, `data/metadata/switzerland/` | manifests and feature matrix only |
| Swiss Set C | 550 MiniSEED (HHZ), 550 StationXML | MiniSEED, StationXML | `data/raw/switzerland_validation/`, `data/metadata/switzerland_validation/` | manifests and feature matrix only |
| Feature matrices | `reports/features/feature_matrix.csv` (8 x 25), `swiss_set_a_feature_matrix.csv` (240 x 45), `swiss_set_c_feature_matrix.csv` (1,100 x 35) | CSV | `reports/features/` | yes |

Channel codes: `HH`/`BH` = broadband seismometer band (high/broad); last letter = component: `Z` vertical, `N` north, `E` east. Network `CH` = Swiss national network; `CI` = Southern California Seismic Network. Location code is empty (`--`).

## 2. Labels

| Value | Meaning |
|---|---|
| `is_earthquake = 1`, `window_type = early_p_wave` | 4.0 s window starting at the SED analyst first-P pick |
| `is_earthquake = 0`, `window_type = ambient_noise` | 4.0 s window from origin -35 s to origin -31 s of the same record |
| `p_evaluation_mode = manual` | pick evaluation mode taken from SED QuakeML (all 120 Set A, all 550 Set C) |
| `p_phase` | `Pg` (crustal direct), `P1`, `Pn` (refracted); Set A: Pg 114, P1 3, Pn 3; Set C: Pg 390, P1 87, Pn 73 |

## 3. Manifest columns (published, `data/manifests/`)

| File | Rows | Key columns |
|---|---|---|
| `iris_california_pilot_events.csv` | 8 | event_id (folder name), origin_time_utc, latitude, longitude, depth_km, magnitude, magnitude_type, waveform_file_count, waveform_files, fdsn_event_provider (USGS), fdsn_waveform_provider (EARTHSCOPE) |
| `sed_switzerland_pilot_events.csv` | 120 | event_id (SED resource ID), origin_time_utc, latitude, longitude, depth_km, magnitude, magnitude_type (MLh, MLhc), region, network, station, location, channels (`HHE;HHN;HHZ`), sampling_rate_hz, waveform_start_utc, waveform_end_utc, pre_event_seconds, post_event_seconds, stationxml_available, waveform_file, download_status, validation_status |
| `sed_switzerland_set_a_picks.csv` | 120 | short_id, sed_event_resource_id, origin_time, network, station, location, channel, pick_phase, pick_time_utc, pick_evaluation_mode, pick_evaluation_status, pick_source, same_station_pick_status |
| `sed_switzerland_validation_candidates.csv` | 227 | short_id, event_id, origin_time_utc, latitude, longitude, depth_km, magnitude, region, event_type, location_class, in_development_set, pool_role (212 pool, 15 proposed), proposed_validation, pick and station availability counts, stationxml_status, exclusion_concern |
| `sed_switzerland_validation_waveforms.csv` | 550 | event_id, short_id, sed_event_resource_id, origin_time, magnitude, magnitude_type, region, location_class (swiss_territory 312, immediate_border 238), network, station, location, channel (HHZ), requested/actual start and end, sampling_rate, sample_count, n_traces, file_size_bytes, gaps, overlaps, masked_or_empty, coverage_status, MiniSEED_path, StationXML_path, StationXML_status, pick_* columns, download_status, verification_status, source_provider, request_parameters |
| `sed_switzerland_validation_picks.csv` | 550 | same schema as the Set A picks file |

## 4. Feature-matrix metadata columns

**Set A (21 columns):** event_id, short_id, station, channel_group (`HH_3C`), sampling_rate_hz, magnitude, magnitude_type, region, epicentral_distance_km, hypocentral_distance_km, origin_time_utc, p_pick_time_utc, p_latency_s (pick minus origin, s), p_phase, p_evaluation_mode, sample_id, window_type, is_earthquake, window_start_utc, window_end_utc, window_duration_s (4.0).

**Set C (17 columns):** event_id, short_id, station, magnitude, magnitude_type, region, sampling_rate_hz, origin_time_utc, p_pick_time_utc, p_phase, p_evaluation_mode, sample_id, window_type, is_earthquake, window_start_utc, window_end_utc, window_duration_s. (No distance columns and no `p_latency_s`.)

`short_id` is the grouping key for Leave-One-Group-Out cross-validation. `sample_id` = `<short_id>_<station>_<noise|p_arrival>`.

## 5. Feature dictionary (Swiss)

Computed on a 4.0 s window of **ground velocity in m/s** (response removed, 0.1 to 15 Hz zero-phase bandpass), vertical channel unless stated. `x` = window samples, `fs` = sampling rate, `dt` = 1/fs. Position = order in the saved models (24-feature order = Set A matrix order; 18-feature order = `reports/ml/vertical_feature_schema.json`).

| # (24) | # (18) | Feature | Description | Unit | Set A | Set C |
|---|---|---|---|---|---|---|
| 1 | 1 | `z_peak_velocity_m_s` | max abs(x) | m/s | yes | yes |
| 2 | 2 | `z_p2p_amplitude_m_s` | max(x) - min(x) | m/s | yes | yes |
| 3 | 3 | `z_rms_velocity_m_s` | root mean square of x | m/s | yes | yes |
| 4 | 4 | `z_variance` | variance of x | m^2/s^2 | yes | yes |
| 5 | 5 | `z_std` | standard deviation of x | m/s | yes | yes |
| 6 | 6 | `z_zero_crossing_rate_hz` | sign changes divided by window duration | Hz | yes | yes |
| 7 | 7 | `z_signal_energy_m2_s` | sum(x^2) * dt | m^2/s | yes | yes |
| 8 | 8 | `z_crest_factor` | peak / max(RMS, 1e-12) | unitless | yes | yes |
| 9 | 9 | `z_kurtosis` | scipy.stats.kurtosis (Fisher, excess) | unitless | yes | yes |
| 10 | 10 | `z_skewness` | scipy.stats.skew | unitless | yes | yes |
| 11 | 11 | `z_cav_m_s` | sum(abs(x)) * dt (dimensionally a length; name kept as in schema) | m (named m_s) | yes | yes |
| 12 | 12 | `z_dominant_frequency_hz` | frequency of maximum FFT power (f > 0) | Hz | yes | yes |
| 13 | 13 | `z_spectral_centroid_hz` | power-weighted mean frequency | Hz | yes | yes |
| 14 | 14 | `z_spectral_bandwidth_hz` | power-weighted standard deviation about the centroid | Hz | yes | yes |
| 15 | 15 | `z_spectral_rolloff_95_hz` | frequency below which 95% of power lies | Hz | yes | yes |
| 16 | 16 | `z_spectral_entropy` | Shannon entropy (log2) of the normalised power spectrum | bits | yes | yes |
| 17 | n/a | `h_peak_velocity_m_s` | max of sqrt(N^2 + E^2) | m/s | yes | no |
| 18 | n/a | `h_rms_velocity_m_s` | RMS of sqrt(N^2 + E^2) | m/s | yes | no |
| 19 | n/a | `vec3c_peak_velocity_m_s` | max of sqrt(Z^2 + N^2 + E^2) | m/s | yes | no |
| 20 | n/a | `vec3c_rms_velocity_m_s` | RMS of the 3C vector | m/s | yes | no |
| 21 | n/a | `vh_ratio` | z RMS / max(horizontal RMS, 1e-12) | unitless | yes | no |
| 22 | 17 | `sta_lta_max` | max of the `classic_sta_lta` characteristic function inside the window (STA 0.5 s in Set A, **1.0 s in Set C**, LTA 10 s; computed on the full filtered trace, then sliced) | ratio | yes | yes |
| 23 | 18 | `sta_lta_mean` | mean of the same function inside the window (same STA caveat) | ratio | yes | yes |
| 24 | n/a | `snr_db` | 20 log10(3C RMS / RMS of the vertical trace from origin -45 s to -15 s in the same record); linear value floored at 1e-6 | dB | yes | no |

In the 24-feature order, `sta_lta_max`, `sta_lta_mean`, `snr_db` come last (positions 22 to 24), and in the 18-feature order they are positions 17 and 18. The 18 features are columns of both matrices with identical names.

**Schema consistency (verified 2026-11-15).** `src/models/vertical_models.py::VERTICAL_FEATURE_COLUMNS`, `reports/ml/vertical_feature_schema.json`, and `feature_columns` inside `vertical_rf_model_set_a.joblib` and `vertical_xgb_model_set_a.joblib` are identical; the saved 24-feature models match each other and the Set A matrix order. No NaN in either matrix's feature columns.

## 6. California feature matrix (frozen, units are digital counts)

`reports/features/feature_matrix.csv`, 8 rows. Metadata: event_id, short_id, station_id, magnitude, magnitude_type, sampling_rate_hz (40), p_pick_source (`phase_a2_metrics` = STA/LTA picks of the signal-analysis step). Features (18): peak_amplitude, peak_to_peak_amplitude, rms, variance, std, zero_crossing_rate_hz, signal_energy, signal_entropy, crest_factor; dominant_frequency_hz, spectral_centroid_hz, spectral_bandwidth_hz, spectral_rolloff_95_hz, spectral_entropy; p_arrival_time_s, signal_duration_s, pgm_proxy_counts, arias_intensity_counts2_s_proxy. Not comparable in scale or definition with the Swiss features.

## 7. Dataset-specific differences that affect interpretation

| Item | California | Set A | Set C |
|---|---|---|---|
| Units | counts | m/s | m/s |
| Components | Z | Z, N, E | Z |
| STA window of STA/LTA | 0.5 s (picker) | 0.5 s (feature) | 1.0 s (feature) |
| Response pre-filter f3/f4 | not applied | 0.75/0.85 Nyquist (via `pre_filt_for_sampling`) | min(18 Hz, 0.75 Nyq) / min(22.5 Hz, 0.85 Nyq) |
| Distance columns | no | yes | no |
| Features | 18 | 24 | 18 |

## 8. Result files

| File | Content |
|---|---|
| `reports/ml/vertical_set_c_evaluation_summary.json` | Set C metrics, confusion counts, importances |
| `reports/ml/vertical_set_a_evaluation_summary.json` | Set A CV (18 features) |
| `reports/ml/swiss_ml_evaluation_summary.json` | Set A CV (24 features) |
| `reports/ml/vertical_set_c_per_event_results.csv` | per-event Set C scores |
| `reports/data_lineage/data_lineage_summary.json` | counts and checks behind this documentation |
