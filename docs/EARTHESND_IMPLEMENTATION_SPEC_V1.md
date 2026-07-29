# EarthESND Implementation Specification v1.0

## Authority and rules

This specification is derived solely from
[EARTHESND_REVERSE_ENGINEERING.md](EARTHESND_REVERSE_ENGINEERING.md), denoted
**RE**. Every artifact below includes a trace to RE. The paper does not dictate
software file names, Python APIs, configuration formats, schemas, test runners,
or error behavior. Those are marked **Project assumption**.

If RE records a detail as “Not specified in the paper,” no implementation may
invent a default or call it a paper reproduction. The relevant configuration
field must be `null` until it is explicitly approved and recorded as a project
assumption.

## Requirements register

| ID | Requirement | Trace |
|---|---|---|
| R-DATA | Japan K-NET 100-Hz NS/EW/UD P-wave records, 2–6 s windows, 70:15:15 stratified split; 157-record India/PESMOS cross-region evaluation and 232-record Noto holdout. | `RE §2, §12` |
| R-PRE | STA/LTA 2.5; first-20-sample >0.01 gal gate; first-20-sample baseline subtraction; 4-pole 0.0075–45 Hz Butterworth; acceleration, velocity, displacement. | `RE §3` |
| R-FEAT | Vertical-component `tau_c`, `ID2`, `IV2`, `PI`, `RSSCV`, `Tva`, and `CAV`; preserve the paper’s six-versus-seven conflict. | `RE §4, §16` |
| R-ESN | Fixed-random, spectrally scaled, serial multiscale ESN; final-layer terminal state only. | `RE §5` |
| R-DENN | Masked branch composition; two-layer 64/GELU then 1/linear readout. | `RE §6` |
| R-SYN | DENN-CTGAN, fitted only on training tabular features/targets, requests 10,000 synthetic records. | `RE §7.1` |
| R-ENS | XGBoost, LightGBM, CatBoost each trained on real and augmented data; preserve six ML outputs and combine with ESN output under declared weights. | `RE §7.2, §16` |
| R-TRAIN | MSE, Adam, 50 epochs, batch 512; reported per-window values. | `RE §8` |
| R-EVAL | MAE, RMSE, percentage MAE improvement, training seconds/epoch; retain `M_JMA` vs `M_w` labels. | `RE §9–§12` |
| R-REP | Store configuration, provenance, unresolved fields, and deviations; do not claim exact reproduction while any required field is unresolved. | `RE §15–§16` |

## Project configuration

The directory and YAML layout below are **Project assumptions**. The current
repository is configuration-driven, and RE calls for all settings to be
recorded, but does not prescribe filenames or YAML. Trace: `RE §14–§16`.

| Proposed file | Contract | Trace |
|---|---|---|
| `configs/earthesnd/data.yaml` | Source provenance, target scales, windows, split, Noto, manifest. | `RE §2, §12, §15.A` |
| `configs/earthesnd/preprocessing.yaml` | Paper-specified preprocessing and null fields for omitted details. | `RE §3, §15.B` |
| `configs/earthesnd/model.yaml` | ESN/DENN and schedule, with nulls for unspecified architecture. | `RE §5–§8, §15.C` |
| `configs/earthesnd/synthetic_ensemble.yaml` | CTGAN, tree-model and aggregation declarations. | `RE §7, §15.D` |
| `configs/earthesnd/evaluation.yaml` | Metrics, target scale and timing/repetition declarations. | `RE §9–§12, §15.E` |

### `data.yaml`

```yaml
# Key layout is a Project assumption.
japan:
  provider: k_net
  time_range: {start: "1996", end: "2024-07"}
  sampling_rate_hz: 100
  components: [NS, EW, UD]
  magnitude_scale: M_JMA
  magnitude_min: 3.0
  magnitude_max: null # Paper conflict: 7.6 text vs 7.7 Table 1.
india:
  provider: pesmos
  records: 157
  events: 12
  magnitude_scale: M_w
windows_seconds: [2, 3, 4, 5, 6]
split:
  train: 0.70
  test: 0.15
  validation: 0.15
  stratification_bins: "np.arange(3.0, 8.5, 0.5)"
  random_seed: null # Not specified in the paper.
noto: {date: "2024-01-01", records: 232, magnitude: 7.6, magnitude_scale: M_JMA}
manifest_path: null # Project-assumption local path.
```

### `preprocessing.yaml`

```yaml
sample_rate_hz: 100
sta_lta: {threshold: 2.5, short_window: null, long_window: null}
station_scaling: {method: null}
quality_gate: {samples: 20, mean_acceleration_threshold_gal: 0.01, comparison: greater_than}
baseline_correction: {method: subtract_mean_first_n_samples, samples: 20}
bandpass:
  family: butterworth
  poles: 4
  low_hz: 0.0075
  high_hz: 45.0
  phase_mode: null
  transient_handling: null
integration: {method: null, initial_condition: null}
```

### `model.yaml`

```yaml
inputs:
  channels: [A_NS, A_EW, A_UD, V_NS, V_EW, V_UD, D_NS, D_EW, D_UD]
  channel_count: 9
target_scale: M_JMA
esn:
  architecture: serial_multiscale_deep
  terminal_state_only: true
  fixed_random_reservoir: true
  recurrent_weight_distribution: standard_normal
  input_weight_distribution: normal
  spectral_radius_scaling: true
  layer_count: null
  reservoir_widths: null
  input_scaling: null
  recurrent_sparsity: null
  target_spectral_radii: null
  initial_state: null
  random_seed: null
  washout: null
  leak_prior: "log_uniform(1e-1, 1)"
  windows: {"2": {reported_leak: 0.8}, "3": {reported_leak: 1.0}, "4": {reported_leak: 0.5}, "5": {reported_leak: 0.1}, "6": {reported_leak: 0.08}}
denn:
  layer_widths: [64, 1]
  activations: [gelu, linear]
  branch_connectivity_method: null
  local_branch_nonlinearity: null
  mask_learning: null
  windows: {"2": {branches: 2, reported_sparsity: 0.1}, "3": {branches: 2, reported_sparsity: 0.1}, "4": {branches: 3, reported_sparsity: 0.2}, "5": {branches: 3, reported_sparsity: 0.1}, "6": {branches: 2, reported_sparsity: 0.1}}
training:
  loss: mse
  optimizer: adam
  epochs: 50
  batch_size: 512
  windows: {"2": {learning_rate: 0.001}, "3": {learning_rate: 0.0014}, "4": {learning_rate: 0.001}, "5": {learning_rate: 0.001}, "6": {learning_rate: 0.001}}
  adam_betas: null
  adam_epsilon: null
  weight_decay: null
```

### `synthetic_ensemble.yaml` and `evaluation.yaml`

```yaml
# synthetic_ensemble.yaml
synthetic:
  model: denn_ctgan
  synthetic_record_count: 10000
  input: vertical_component_tabular_features_and_training_target
  generator_architecture: null
  discriminator_architecture: null
  training_hyperparameters: null
  t_sne_parameters: null
ensemble:
  learners: [xgboost, lightgbm, catboost]
  training_sets: [real, augmented]
  expected_model_count: 6
  aggregation_weights: null

# evaluation.yaml
metrics: [mae, rmse, percent_mae_improvement, training_seconds_per_epoch]
target_scales: [M_JMA, M_w]
inference_latency: null
repetitions: null
timing_environment: null
```

All `null` fields are **Not specified in the paper**. The `leak_prior` and
reported window leaks both remain because RE reports both but says their
relationship is unresolved. Trace: `RE §3–§9, §16`.

## Data contracts

The field names and serialization are **Project assumptions**; their inclusion
comes from the reproducibility roadmap in RE.

| Contract | Required fields / shape | Trace |
|---|---|---|
| `ManifestRecord` | `event_id`, `station_id`, `component_paths`, `p_pick`, `sampling_rate_hz`, `station_scaling_provenance`, `magnitude`, `magnitude_scale`, distance/depth fields, `split`, `is_noto_holdout`, `source_region`. | `RE §2, §3, §12, §15.A` |
| `waveform_tensor` | `(T, 9)` ordered `A_NS,A_EW,A_UD,V_NS,V_EW,V_UD,D_NS,D_EW,D_UD`; `T=100*N`, thus 200/300/400/500/600. | `RE §3.2` |
| `tabular_features` | Seven named vertical-component values; preserve the six-versus-seven discrepancy in run metadata. | `RE §4, §16` |
| `terminal_state` | `h_T^(L)` only; its width remains unresolved. | `RE §5.2–§5.3` |
| `fusion_vector` | `[terminal_state | tabular_features]`. | `RE §4–§6` |
| Predictions | `y_esn` plus six ML scalars; `y_pred` only after explicit aggregation policy. | `RE §1, §7` |

## Module, class, and function inventory

All names/signatures are **Project assumptions**. The required behavior is
paper-derived and mapped below.

| Proposed artifact | Classes / functions | Required behavior | Trace |
|---|---|---|---|
| `src/acquisition/knet_client.py` | `KNetClient.fetch_record(record)` | Loads/acquires three Japan components only when source access is explicitly configured. | `RE §2.1, §14–§15` |
| `src/acquisition/pesmos_client.py` | `PesmosClient.fetch_record(record)` | Loads/acquires India evaluation components only when access is configured. | `RE §2.2, §12, §14–§15` |
| `src/data/manifest.py` | `ManifestRecord`, `DatasetManifest`, `load_manifest`, `validate_manifest` | Stores required provenance and validates scale/split fields. | `RE §15.A, §16` |
| `src/data/splits.py` | `assign_stratified_splits(records, bins, proportions, seed)` | Applies stated bins/proportions; `seed` required, never defaulted. | `RE §2.1, §15.A` |
| `src/preprocessing/picking.py` | `pick_p_wave_sta_lta(trace, threshold, short_window, long_window)` | Uses threshold 2.5; refuses null STA/LTA windows. | `RE §3.1, §16` |
| `src/preprocessing/quality.py` | `mean_first_n_samples`, `passes_mean_amplitude_gate` | Applies first-20 mean >0.01 gal criterion. | `RE §3.1` |
| `src/preprocessing/baseline.py` | `subtract_first_n_mean` | Subtracts first-20-sample mean. | `RE §3.1` |
| `src/preprocessing/filtering.py` | `bandpass_butterworth` | Four-pole 0.0075–45 Hz Butterworth; requires a declared phase mode. | `RE §3.1, §16` |
| `src/preprocessing/integration.py` | `integrate_acceleration`, `integrate_velocity` | Forms velocity then displacement; requires a declared method/initial state. | `RE §3.2, §16` |
| `src/preprocessing/windows.py` | `extract_p_window` | Produces 2–6-s 100-Hz windows. | `RE §2.1, §3.2` |
| `src/preprocessing/pipeline.py` | `PreprocessingPipeline.process(record)` | Sequences gate, correction, filter, integration and `(T,9)` construction; returns rejection reason or tensor. | `RE §3` |
| `src/processing/features.py` | `VerticalPWaveFeatures`, `extract_vertical_features` | Names seven features; blocks numeric extraction until formulas are approved as deviations. | `RE §4, §15.B, §16` |
| `src/processing/fusion.py` | `concatenate_terminal_state_and_features` | Concatenates final state with tabular vector. | `RE §4–§6` |
| `src/models/esn.py` | `spectral_radius`, `scale_recurrent_matrix`, `SparseReservoir`, `SerialMultiscaleESN` | Implements Eq. 1 and Eq. 2, serial forward-only propagation, fixed random weights, terminal state only. | `RE §5` |
| `src/models/dendritic.py` | `DendriticBranch`, `DendriticLayer`, `DendriticReadout` | Implements masked branch -> local transform -> sum -> neuron activation; 64/GELU then 1/linear readout. | `RE §6` |
| `src/models/earthesnd.py` | `EarthESNDModel.fit`, `EarthESNDModel.predict` | Coordinates ESN state, fusion and DENN prediction `y_esn`. | `RE §1, §5–§6, §8` |
| `src/models/denn_ctgan.py` | `DennCtgan.fit`, `DennCtgan.sample`, `visualize_tsne` | Fits train-only tabular data and requests 10,000 samples; requires resolved GAN details. | `RE §7.1, §16` |
| `src/models/tabular_ensemble.py` | `TabularEnsemble.fit`, `predict_six` | Fits XGB/LGBM/CatB on real and augmented sets; exposes all six predictions. | `RE §7.2` |
| `src/models/aggregation.py` | `aggregate_predictions` | Requires declared weights; never assumes 1/7. | `RE §7.2, §16` |
| `src/models/full_pipeline.py` | `EarthESNDPipeline.fit`, `EarthESNDPipeline.predict` | Orchestrates both paths and preserves component predictions. | `RE §1, §7–§8` |
| `src/training/earthesnd_trainer.py` | `EarthESNDTrainer.train_window` | Uses MSE/Adam/50/512 and per-window values; records unresolved choices. | `RE §8` |
| `src/evaluation/metrics.py` | `mean_absolute_error`, `root_mean_squared_error`, `percent_mae_improvement` | Computes named metrics. | `RE §9` |
| `src/evaluation/benchmarks.py` | `evaluate_japan_test`, `evaluate_noto_holdout`, `evaluate_india_cross_region` | Separates reported scopes and scales. | `RE §10–§12` |
| `src/evaluation/timing.py` | `measure_training_seconds_per_epoch` | Records time with caller-provided environment metadata. | `RE §9, §11` |
| `src/experiments/run_metadata.py` | `ExperimentMetadata`, `write_deviation_log`, `assert_no_unresolved_settings` | Persists configs/provenance/deviations and blocks “exact” runs with nulls. | `RE §15–§16` |

The source adapters must fail rather than guess endpoints. ESN initialization
must require all unresolved topology/radius/seed values. DENN must require
mask/local-activation choices. These fail-closed rules are **Project
assumptions** supporting RE’s no-inference/reproducibility requirements.

## Test specification

Test file names and runner are **Project assumptions**. Each test is a
traceable verification of a paper-derived constraint or an explicit omission.

| Proposed test | Required assertion | Trace |
|---|---|---|
| `test_manifest_requires_scale_and_split` | Rejects absent target scale/split metadata. | `RE §2, §12, §16` |
| `test_stratification_uses_reported_bins_and_proportions` | Uses 3.0–8.0 step-.5 bins and 70/15/15; seed is required. | `RE §2.1` |
| `test_amplitude_gate_uses_first_twenty_samples` | Accepts only first-20 mean strictly >0.01 gal. | `RE §3.1` |
| `test_baseline_subtracts_first_twenty_mean` | Corrected first 20 samples mean to zero within numerical tolerance. | `RE §3.1` |
| `test_preprocessing_requires_unresolved_settings` | Blocks null STA/LTA windows, phase mode, and integration policy. | `RE §3, §16` |
| `test_window_shapes` | Shapes are `(200,9)` through `(600,9)`. | `RE §2.1, §3.2` |
| `test_feature_schema` | Exactly seven named vertical features and documented conflict metadata. | `RE §4, §16` |
| `test_feature_extraction_blocks_missing_formulae` | No numeric feature output without an approved deviation. | `RE §4, §16` |
| `test_spectral_scaling` | Matrix radius matches caller target. | `RE §5.3` |
| `test_reservoir_step_equation_one` | Fixed tensor case matches Eq. 1. | `RE §5.1–§5.2` |
| `test_serial_terminal_state_only` | No intermediate state concatenation/skip. | `RE §5.2` |
| `test_dendritic_equation` | Applies mask, branch transform, aggregate, activation, bias in stated order. | `RE §6.1` |
| `test_readout_shape_and_activation` | 64/GELU then 1/linear returns scalar. | `RE §6.2` |
| `test_synthetic_count` | Requests exactly 10,000 synthetic rows. | `RE §7.1` |
| `test_six_ensemble_predictions` | 3 learners × 2 datasets equals six. | `RE §7.2` |
| `test_aggregation_requires_weights` | No implicit equal-weight aggregation. | `RE §7.2, §16` |
| `test_reported_training_settings` | Verifies five window leak/branch/sparsity/rate values, MSE/Adam/50/512. | `RE §8` |
| `test_metric_equations_and_scale_guard` | Metrics work; direct `M_JMA`/`M_w` comparison is rejected. | `RE §9, §12, §16` |
| `test_exact_run_blocks_unresolved_fields` | Exact-reproduction mode fails while required configuration values remain null. | `RE §15–§16` |

Numerical tolerances, test fixtures, mocking approach, and coverage target are
**Not specified in the paper** and must be logged as Project assumptions.

## Build order and acceptance gates

1. **Data contracts and adapters:** validate manifest and preserve Japan/Noto/India separation. Gate: provenance, scales and splits are present. Trace: `RE §2, §12, §15.A`.
2. **Preprocessing:** implement all stated operations and fail on missing operational details. Gate: `(T,9)` shape tests pass. Trace: `RE §3, §15.B`.
3. **Feature schema:** represent named features, but block numerical extraction without approved formulas. Gate: no unsupported feature claim. Trace: `RE §4, §16`.
4. **ESN/DENN:** implement equations, terminal-state fusion, and reported readout/schedule. Gate: Eq. 1/Eq. 2 and dendritic-equation tests pass. Trace: `RE §5–§6, §8`.
5. **CTGAN/ensemble:** preserve train-only synthetic generation, six tree predictions, explicit aggregation. Gate: no test leakage; weights declared. Trace: `RE §7, §15.D`.
6. **Evaluation:** emit MAE/RMSE/improvement/timing, separate test scopes, and persist deviations. Gate: no cross-scale comparison and no exact claim with unresolved details. Trace: `RE §9–§16`.

## Implementation progress

*Last synchronized with the repository: documentation pass v0.5.0. **65** automated tests passing. This section tracks delivery only; it does not change requirements above.*

### Completed (spec build-order gates)

| Gate | Project phase (README) | Status | Primary modules / tests |
|------|-------------------------|--------|-------------------------|
| 1 | Phase 1 — repository foundation | ✅ | `src/data/manifest.py`, `splits.py`; acquisition framework; `tests/test_earthesnd_manifest.py`, `test_earthesnd_splits.py`, acquisition tests |
| 2 | Phase 2 — preprocessing | ✅ | `src/preprocessing/*`, `pipeline.py`; `tests/test_earthesnd_preprocessing.py` |
| 3 | Phase 3 — feature engineering | ✅ | `src/processing/features.py`; schema tests; numeric extraction **blocked** |
| 4 (partial) | Phase 4 — ESN | ✅ | `src/models/esn.py`; `tests/models/test_esn.py` |
| 4 (partial) | Phase 5 — DENN, fusion, `EarthESNDModel` | ✅ | `src/models/dendritic.py`, `earthesnd.py`, `earthesnd_config.py`, `src/processing/fusion.py`; `tests/models/test_dendritic.py`, `test_earthesnd.py` |
| 5 | Phase 5 — CTGAN & ensemble **contracts** | ✅ | `denn_ctgan.py`, `tabular_ensemble.py`, `aggregation.py`, `tabular_data.py`; `tests/models/test_synthetic_ensemble.py` |

### Intentionally blocked (fail-closed; not paper-derived defaults)

| Area | Config / API behaviour | Trace |
|------|------------------------|-------|
| Vertical feature numerics | `extract_vertical_features` → `NotImplementedError` | `RE §4`, `R-FEAT` |
| Preprocessing omissions | Null STA/LTA windows, filter `phase_mode`, integration policy | `RE §3`, `R-PRE` |
| Serial multiscale deep ESN | `esn.layer_count`, widths, radii, washout null; single-reservoir `ESN` in code | `RE §5.2–§5.3`, `R-ESN` |
| DENN operational mask / local φ | `denn.branch_connectivity_method`, `local_branch_nonlinearity`, `mask_learning` null in YAML | `RE §6.1`, `R-DENN` |
| DENN Adam training | `EarthESNDModel.fit` blocked until `adam_betas`, `adam_epsilon`, `weight_decay` set; no training loop yet | `RE §8`, `R-TRAIN` |
| DENN-CTGAN synthesis | Generator/discriminator/training hyperparameters null | `RE §7.1`, `R-SYN` |
| Tree ensemble training | `learner_hyperparameters` absent in YAML | `RE §7.2`, `R-ENS` |
| Final averaging | `aggregation_weights` null; runtime weights required | `RE §7.2`, `R-ENS` |

### Remaining implementation work (spec inventory not yet delivered)

- `SerialMultiscaleESN`, spectral helpers as named in module inventory (beyond single-layer `ESN`).
- `src/training/earthesnd_trainer.py` — MSE / Adam / 50 / 512 per window.
- `src/models/full_pipeline.py` — full EarthESND + ML path orchestration.
- `src/evaluation/*`, `src/experiments/run_metadata.py`.
- K-NET / PESMOS acquisition adapters (`knet_client.py`, `pesmos_client.py` in inventory).
- Spec tests not yet present: e.g. `test_exact_run_blocks_unresolved_fields`, full `test_reported_training_settings` on trainer, metric/benchmark suites.

## Mandatory project-assumption log

Before any executable reproduction run, record all of the following as project
assumptions if they are set: source endpoints/formats; station scaling; STA/LTA
windows; filter phase/transients; numerical integration and initial values;
feature formulas; 6-vs-7 feature handling; 7.6-vs-7.7 upper magnitude; ESN
depth/width/input scale/sparsity/radii/seed/washout; leak interpretation; DENN
mask/local activation; CTGAN design/training; tree hyperparameters; aggregation
weights; Adam details; timing hardware; repetitions; and `M_JMA`/`M_w`
conversion.

Trace: `RE §2–§16`, especially `RE §16`. None may be described as
paper-derived.
