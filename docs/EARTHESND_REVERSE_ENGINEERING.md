# EarthESND reverse-engineering specification

## Scope and evidence boundary

This document is a reverse-engineering specification of the supplied main
article, *Scalable multiscale echo state reservoirs with dendritic readouts for
intelligent earthquake early warning systems*, Joshi, Singh, and Raman,
*Computers and Electrical Engineering* 135 (2026) 111161. It was prepared from
`references/papers/ScienceDirect_EarthESND_2026.pdf` only. No external source
was consulted.

The PDF is a 14-page main article. It repeatedly refers to supplementary
sections, figures, and tables, but those materials are not contained in the
supplied PDF. Where a requested detail is absent from the main article, this
document says **Not specified in the paper.** That statement includes details
deferred exclusively to the unavailable supplement.

## 1. System in one view

The proposed final predictor is an average of:

1. `y_ESN`: a deep, serial, multi-scale ESN whose final terminal state is
   concatenated with physics-based tabular P-wave features and passed through a
   two-layer dendritic neural-network (DENN) readout.
2. Six tree-model predictions: XGBoost, LightGBM, and CatBoost, each trained
   once on real tabular data and once on tabular data augmented with 10,000
   DENN-CTGAN synthetic records.

The paper’s Figure 1 pipeline is: STA/LTA trigger -> preprocessing -> nine
waveform channels to serial reservoirs; vertical-component feature extraction
to seven named tabular features -> ESN/DENN predictor; DENN-CTGAN -> tabular
ML ensemble; average ensemble result with `y_ESN` -> `y_pred`.

## 2. Dataset and acquisition

### 2.1 Japan development dataset

| Item | Paper detail |
|---|---|
| Region | Japan |
| Raw waveform source | K-NET / Kyoshin Network strong-motion seismograms |
| Catalogue attribution | Japan Meteorological Agency catalogue in §3; Data Availability instead attributes K-NET/KiK-net to NIED. The paper does not resolve this wording difference. |
| Time range | 1996 through July 2024 |
| Sampling frequency | 100 Hz |
| Components | North–south (NS), east–west (EW), up–down (UD) acceleration |
| Records | 36,196 total: 25,337 train, 5,429 test, 5,430 validation |
| Split | 70:15:15 train:test:validation; stratified magnitude bins `np.arange(3.0, 8.5, 0.5)` |
| Magnitude selection | §3 says 3.0–7.6 `M_JMA`; Table 1 reports a maximum of 7.7 in every split. The paper does not reconcile the discrepancy. |
| Distance/depth filters | No lower or upper limits imposed on epicentral distance, focal depth, or hypocentral distance. |
| Windows | 2, 3, 4, 5, 6 seconds from initial P wave, called 2SE–6SE; records/splits are identical across windows. |
| Held-out event | 232 records from the 1 January 2024 Noto event, magnitude 7.6 `M_JMA`, separated for testing. |

Table 1 ranges:

| Split | Magnitude min–max (`M_JMA`) | Epicentral km min–max | Focal-depth km min–max | Hypocentral km min–max |
|---|---:|---:|---:|---:|
| Train | 3.0–7.7 | 1.08–1607.85 | 0–619 | 5.57–1668.29 |
| Test | 3.0–7.7 | 2.87–1253.71 | 0–619 | 9.49–1341.38 |
| Validation | 3.0–7.7 | 2.02–1404.37 | 0–619 | 7.30–1483.17 |

### 2.2 Inter-region generalization dataset

The paper uses PESMOS (IIT Roorkee) records from India and nearby regions as a
cross-region test set: 157 records from 12 events. It does not state whether
the model was retrained or only evaluated; the text says it was trained in
Japan and tested in the other region, so this is interpreted as zero-shot
evaluation.

| Region/event | Date | Stations | `M_w` | Focal depth km |
|---|---|---:|---:|---:|
| Myanmar–India border | 11-08-2011 | 12 | 5.6 | 12 |
| Uttarkashi, India | 21-09-2009 | 10 | 4.7 | 12 |
| Bhutan | 31-12-2009 | 5 | 5.5 | 5 |
| Punjab–Himachal border, India | 14-03-2010 | 12 | 4.6 | 13 |
| Bageshwar, Uttarakhand | 01-05-2010 | 6 | 4.6 | 13 |
| India–Nepal border | 04-04-2011 | 23 | 5.7 | 24 |
| Nepal | 01-12-2016 | 20 | 5.2 | 20 |
| Chamoli, Uttarakhand | 20-06-2011 | 11 | 4.6 | 7 |
| Sonipat, India | 07-09-2011 | 6 | 4.2 | 7 |
| Sikkim–India/Nepal border | 18-09-2011 | 13 | 6.8 | 9 |
| Bahadurgarh, India | 05-03-2012 | 19 | 4.9 | 21 |
| Chamoli, India | 29-11-2015 | 10 | 4.0 | 14 |

Acquisition endpoint URLs, station-selection policy, event-query fields,
response-removal procedure, instrument metadata, file format, and waveform
units before processing are **Not specified in the paper.**

## 3. Preprocessing and input construction

### 3.1 Event gate and P-wave selection

1. Pick the P-wave onset using STA/LTA with threshold **2.5**. The paper says
   this was selected empirically to reliably capture onset of `M_JMA >= 3`
   strong-motion seismograms.
2. Apply a station-specific scaling factor.
3. Compute the mean of the first 20 samples in each candidate window; reject
   the window unless mean acceleration exceeds **0.01 gal**.
4. Baseline-correct by subtracting the mean of the first 20 samples.
5. Apply a 4-pole Butterworth bandpass, **0.0075–45 Hz**.
6. Retain 2, 3, 4, 5, or 6 s after the P-wave arrival. At 100 Hz these have
   `T = 200, 300, 400, 500, 600` samples respectively.

The STA/LTA short and long window lengths, trigger/onset timing convention,
station scaling formula/values, filter implementation details (zero-phase or
causal, order interpretation, transient handling), and whether integration is
performed before or after filtering are **Not specified in the paper.**

### 3.2 Nine-channel tensor

Let processed accelerations be `A_c in R^(T x 1)` for `c in {NS, EW, UD}`.
Velocity and displacement are co-integrated:

`v(t) = integral a(t) dt`, and `d(t) = integral v(t) dt`.

The waveform tensor is

`X_i = {A_NS, A_EW, A_UD, V_NS, V_EW, V_UD, D_NS, D_EW, D_UD} in R^(T x C)`,
with `C = 9`.

The model learns `f_theta: R^(T x C) -> R`, producing a continuous magnitude
in the `M_JMA` scale. Numerical integration method, initial conditions,
normalization/standardization, clipping, padding, and missing-data handling
beyond rejecting missing segments are **Not specified in the paper.**

### 3.3 Explicit operational applicability

The authors state that this is a system for event-containing records. It is
not applicable to arbitrary continuous streams or extremely low-SNR traces
outside the stated gate. Traces with missing waveform segments or weak signals
are automatically rejected through the first-20-sample, 0.01-gal mean criterion.

## 4. Feature engineering and fusion

Physics-based features are computed from the **vertical** P-wave component,
because the paper states it has higher signal-to-noise ratio than horizontal
components. The named features are:

1. characteristic period, `tau_c`
2. integrated squared displacement, `ID2`
3. integrated squared velocity, `IV2`
4. P-wave index, `PI`
5. root sum of squared velocity, `RSSCV`
6. peak velocity-acceleration ratio, `Tva`
7. cumulative absolute velocity, `CAV`

There is an internal paper inconsistency: §2.1 calls `Tab_mag` a six-element
vector (`R^(6 x 1)`), but §2.2 lists the seven features above. This document
preserves the seven explicitly named features; the dimension and any omitted
feature are **Not specified in the paper.** Their formulas, units, integration
limits, feature scaling, missing-value treatment, and exact implementation are
deferred to “Supplementary Section 1.1” and therefore are **Not specified in
the paper.**

The fusion vector is `C = [H^(L) | Tab_mag]`, i.e., the terminal state from the
last reservoir concatenated with the tabular feature vector.

## 5. ESN architecture

### 5.1 Base reservoir update

The single-reservoir form supplied in §2.1 is:

`h_(t+1) = (1 - alpha) odot h_t + alpha odot tanh(W_in x_t + W_res h_t)`.

Here `h_t in R^(N_res)`, `x_t in R^C`, `W_in in R^(N_res x C)`, and
`W_res in R^(N_res x N_res)`. `W_in` and `W_res` are fixed random matrices;
`alpha in (0, 1]^(N_res)` is a per-neuron leak vector. `odot` is elementwise
multiplication. This convex blend retains some prior state and admits a
tanh-transformed new activation.

The text first says `H = [h_1^T, ..., h_N^T]^T`, but then says only terminal
state `h_T` is retained as the sequence fingerprint. The latter is repeated
for the deep architecture and is the operative specification.

### 5.2 Deep serial multi-scale ESN

There are `L` serial reservoirs. The input to layer `l+1` is only the output
of layer `l`; there are no skip connections and intermediate states are not
concatenated. For each layer:

`h^(l)_(t+1) = (1 - alpha^(l)) odot h^(l)_t + alpha^(l) odot tanh(W_in^(l) x_t^(l) + W_res^(l) h^(l)_t)`.  (Eq. 1)

The layer state is `h^(l)_t in R^(N_res^(l))`, input weights are
`W_in^(l) in R^(N_res^(l) x C^(l))`, recurrent weights are
`W_res^(l) in R^(N_res^(l) x N_res^(l))`, and `alpha^(l)` is fixed. After all
timesteps, only `H_L = h^(L)_T` is read out. Gradients are never propagated
through ESN layers, although the paper later states Adam is used for the
reservoir network; the exact optimization boundary is therefore unclear.

Leak values reported for datasets 2SE through 6SE are respectively
**0.8, 1.0, 0.5, 0.1, 0.08**. The prose also says each reservoir’s per-neuron
leak values are drawn log-uniformly from `U(10^-1, 1)`, creating memories from
0.1 to 1 s. It does not explain whether the listed values parameterize that
distribution, are layer values, or replace it; this is **Not specified in the
paper.**

### 5.3 Reservoir initialization and stability

For an `i`th stack of the `l`th reservoir, create
`W_raw^(i,l) in R^(D^(l) x D^(l))`. Apply a binary mask at sparsity `nu in
(0, 1]` and populate retained entries from `N(0, 1)`. The maximum absolute
eigenvalue is:

`rho_raw^(l) = max_i |lambda_i(W_raw^(i,l))|`.

Rescale to the target spectral radius:

`W_res^(i,l) = rho^(l)(W_res^(i,l)) = (W_raw^(i,l) / rho_raw^(l)) * rho_target^(l)`.  (Eq. 2)

The stated purpose is stable internal dynamics and the echo-state property.
`W_in` is initialized from a normal distribution. The following are **Not
specified in the paper:** number of serial layers `L` of the final model;
reservoir widths; input scale/distribution variance; recurrent sparsity values;
target spectral radii; initial state; random seeds; washout; whether input and
recurrent biases exist; exact definition of `D^(l)`; and the implementation of
the “i-th stack” terminology.

## 6. Dendritic readout

### 6.1 Generic dendritic layer

The DENN composition is:

`DENN(x) = f_out o f_D_L o ... o f_D_1(x)`, where `f_D_l: R^(n_(l-1)) -> R^(n_l)`.

Each layer has `n_l` neurons and each neuron has `d` dendritic branches. A
branch response is:

`h_(l,i,j)(x_(l-1)) = phi_j(sum_(m=1)^(n_(l-1)) (S_(l,i,j,m) W_(l,i,j,m)) x_(l-1,m) + b_(l,i,j))`, for `j in [d]`.

`S_(l,i,j,m) in {0,1}` is the branch connectivity mask, `W` is the synaptic
weight, `b_(l,i,j)` is branch bias, and `phi_j` is a local dendritic
nonlinearity (the generic examples are sigmoid or Gaussian).

The neuron aggregates branches as:

`g_(l,i)(x_(l-1)) = f_i(sum_(j=1)^d h_(l,i,j)(x_(l-1))) + b_(l,i)`.

The whole layer output is:

`f_D_l(x_(l-1)) = [g_(l,1)(x_(l-1)), ..., g_(l,n_l)(x_(l-1))]^T`.

With `d = 1` and a linear `phi`, it reduces to a conventional fully connected
layer. Exact branch subset construction, local nonlinearity selected for this
model, mask initialization, all branch weights/biases, and whether masks are
learned are **Not specified in the paper.**

### 6.2 Applied readout

The fused vector `C(t)` is passed through `K = 2` DENN layers:

`y_pred = DENN_(i+1)...(DENN_1(C(t); theta_1), theta_(i+1))`, `i in {0, ..., K}`.

The paper calls its intermediate output `y_ESN`; the final system output is an
average with the ML block. Applied DENN layer widths are **64 then 1** across
all five windows. DENN-1 uses GELU, DENN-2 is linear. The given GELU formula is:

`GELU(x) = 1/2 x (1 + tanh(sqrt(2/pi) (x + 0.044715 x^3)))`.

DENN-1 branches by 2SE–6SE are **2, 2, 3, 3, 2**. Reported sparsity values
`nu` by 2SE–6SE are **0.1, 0.1, 0.2, 0.1, 0.1**. The paper does not say whether
this refers to reservoir or DENN connectivity in this paragraph, although the
nearby text uses `nu` for reservoir matrices; exact placement is **Not
specified in the paper.**

## 7. Synthetic data and ML ensemble

### 7.1 DENN-CTGAN

The generator and discriminator are DENNs. CTGAN uses mode-specific
normalization with a variational Gaussian mixture to model a continuous column
`C_i`:

`P_C_i(c_(i,j)) = sum_(p=1)^(m_k) mu_p N(c_(i,j); eta_p, theta_p)`.

The paper calls `mu_p` and `theta_p` the weight and standard deviation of mode
`p`; `eta_p` appears as the Gaussian location but is not described in prose.

The conditional generator target is:

`P(row) = sum_(k in D_i*) P_G(row | D_i* = k*) P(D_i* = k)`.

Using real training features `Tab_act` and target `y_act`, it generates 10,000
records `{Tab_syn | y_syn}`. The augmented set is:

`{Tab_aug | y_aug} = {Tab_syn | y_syn} || {Tab_act | y_act}`.

The authors use t-SNE to visualize real vs. synthetic high-dimensional data.
GAN dimensions, number/type of DENN layers, latent dimension, conditioning
scheme, optimizer, learning rate, epochs, batch size, discriminator steps,
mixture components, random seed, data-quality test, t-SNE parameters, and
synthetic class/magnitude distribution are **Not specified in the paper.**

### 7.2 Ensemble and final average

XGBoost (XGB), LightGBM (LGBM), and CatBoost (CatB) are each trained twice:
on real `Tab_act` and on augmented `Tab_aug`, for six predictors. The final
system averages these six outputs with `y_ESN` (seven equal operands is the
natural reading, but the actual averaging weights/formula are **Not specified
in the paper**). Tree-model hyperparameters, feature preprocessing, early
stopping, and random seeds are **Not specified in the paper.**

## 8. Training pipeline and reported hyperparameters

1. Prepare Japan windows and magnitude-stratified 70:15:15 splits.
2. Train the ESN/DENN path with MSE loss and Adam. The reported learning rates
   for 2SE–6SE are **0.001, 0.0014, 0.001, 0.001, 0.001**.
3. Train for **50 epochs**, batch size **512**, for all windows.
4. Train DENN-CTGAN on the real training tabular features/targets and generate
   10,000 synthetic rows.
5. Train the six tree regressors on real and augmented tabular data.
6. Average ML outputs and `y_ESN`.
7. Evaluate on the held-out Japan test set; evaluate Noto and Indian records
   as stated in the results.

Although the paper says ESN matrices and leak vectors are fixed random
parameters and no gradients traverse ESN layers, it calls the reported rate a
“learning rate of the reservoir network.” Whether Adam trains only DENN or also
some ESN-associated parameters is **Not specified in the paper.** Adam beta
values, epsilon, weight decay, initialization, checkpoint selection, validation
criterion for the final model, hardware, software versions, and repetition/
confidence intervals are **Not specified in the paper.**

### Complete reported primary-model settings

| Setting | 2SE | 3SE | 4SE | 5SE | 6SE |
|---|---:|---:|---:|---:|---:|
| P-wave length s | 2 | 3 | 4 | 5 | 6 |
| Samples at 100 Hz | 200 | 300 | 400 | 500 | 600 |
| Reported multiscale leak | 0.8 | 1.0 | 0.5 | 0.1 | 0.08 |
| DENN-1 branches | 2 | 2 | 3 | 3 | 2 |
| Reported sparsity `nu` | 0.1 | 0.1 | 0.2 | 0.1 | 0.1 |
| Learning rate | 0.001 | 0.0014 | 0.001 | 0.001 | 0.001 |
| Epochs | 50 | 50 | 50 | 50 | 50 |
| Batch size | 512 | 512 | 512 | 512 | 512 |

Shared: 9 waveform channels; 2 DENN layers with widths 64/1; GELU then linear;
MSE loss; Adam; STA/LTA threshold 2.5; first-20-sample threshold/baseline
0.01 gal; 4-pole 0.0075–45 Hz filter; 10,000 synthetic records.

## 9. Evaluation metrics

The named metrics are MAE, RMSE, percentage MAE improvement, training seconds
per epoch, and (in a cited supplementary table) single-sample inference
latency. Only the main-PDF formulas are:

`Percent improvement = ((MAE_other - MAE_ours) / MAE_other) * 100%`.

Lower MAE, RMSE, and time are better. The standard MAE/RMSE formulas, their
denominators, aggregation level (record versus event), rounding, error bars,
and inference latency values are **Not specified in the paper.**

## 10. Ablation study (Table 3)

All values are test MAE / RMSE in `M_JMA`, ordered 2SE, 3SE, 4SE, 5SE, 6SE.

| Method | 2SE | 3SE | 4SE | 5SE | 6SE |
|---|---|---|---|---|---|
| Single ESN layer + DENN | .81/.96 | .80/.95 | .80/.97 | .79/.95 | .77/.91 |
| Single ESN layer + FCNN | .84/.99 | .84/.91 | .82/.90 | .81/.91 | .78/.89 |
| Multiscale single reservoir + DENN | .87/1.16 | .86/1.15 | .86/1.14 | .84/1.09 | .82/1.08 |
| Multiscale single reservoir + FCNN | .88/1.13 | .88/1.10 | .86/1.04 | .83/.98 | .81/.94 |
| Deep ESN 2 stack + FCNN | 1.21/1.53 | 1.19/1.50 | 1.18/1.45 | 1.15/1.40 | 1.12/1.38 |
| Deep ESN 3 stack + FCNN | .91/1.24 | .90/1.21 | .91/1.23 | .90/1.19 | .90/1.21 |
| Deep ESN 4 stack + FCNN | .97/1.28 | .95/1.22 | .94/1.20 | .92/1.12 | .90/1.11 |
| Deep ESN 8 stack + FCNN | .92/1.02 | .90/1.01 | .89/.99 | .90/.98 | .97/1.01 |
| Deep ESN 2 stack + DENN | 1.02/1.42 | 1.02/1.40 | 1.00/1.38 | .99/1.35 | .99/1.32 |
| Deep ESN 3 stack + DENN | .87/.99 | .87/.98 | .87/.99 | .88/1.00 | .89/1.03 |
| Deep ESN 4 stack + DENN | .96/1.25 | .94/1.20 | .94/1.12 | .92/1.08 | .91/1.05 |
| Deep ESN 8 stack + DENN | .92/1.12 | .93/1.10 | .92/1.08 | .91/1.05 | .92/.99 |
| EarthESND with FCNN | .75/.98 | .74/.97 | .74/.98 | .73/.96 | .74/.92 |
| Ridge output | .89/1.12 | .88/1.11 | .88/1.10 | .89/1.14 | .89/1.14 |
| Linear output | .88/1.11 | .89/1.13 | .88/1.12 | .87/1.08 | .87/1.06 |
| Removed tabular input | .90/1.25 | .91/1.26 | .89/1.21 | .89/1.22 | .88/1.19 |
| RNN + DENN | .92/1.22 | .92/1.23 | .91/1.21 | .89/1.19 | .89/1.20 |
| RNN + FCNN | .91/1.27 | .91/1.26 | .92/1.27 | .90/1.18 | .90/1.21 |
| LSTM + DENN | .88/1.16 | .90/1.21 | .90/1.19 | .88/1.18 | .87/1.14 |
| LSTM + FCNN | .92/1.21 | .91/1.22* | .90/1.19 | .90/1.21 | .89/1.18 |
| Acceleration-only 3C | .85/1.14 | .85/1.12 | .85/1.14 | .84/1.12 | .83/1.12 |
| Velocity-only 3C | .83/1.19 | .84/1.21 | .84/1.20 | .85/1.23 | .82/1.16 |
| Displacement-only 3C | .80/1.09 | .82/1.13 | .80/1.10 | .80/1.11 | .82/1.16 |
| CTGAN-NN | .78/.97 | .79/.99 | .79/.98 | .77/.96 | .77/.97 |
| CTGAN-Conv | .83/1.25 | .83/1.21 | .82/1.19 | .82/1.18 | .81/1.17 |
| ML: RF + XGB | .78/.96 | .78/.97 | .77/.96 | .77/.95 | .76/.94 |
| ML: XGB + LGBM | .76/.94 | .76/.93 | .75/.94 | .74/.93 | .74/.92 |
| ML: CatB + RF + XGB | .72/.92 | .72/.93 | .71/.92 | .71/.92 | .72/.93 |
| ML only augmented | .98/1.28 | .97/1.26 | .97/1.27 | .96/1.26 | .96/1.27 |
| ML only synthetic | 1.05/1.34 | 1.05/1.35 | 1.01/1.30 | 1.02/1.31 | .98/1.28 |
| ML only real | 1.03/1.37 | 1.03/1.35 | .99/1.30 | .98/1.30 | .96/1.25 |
| Vanilla ESN | .89/1.15 | .88/1.10 | .86/1.09 | .86/1.02 | .86/1.01 |
| Deep ESN + linear | .84/1.03 | .83/.98 | .83/.98 | .81/.97 | .81/.97 |
| Deep ESN + DENN | .78/.96 | .76/.97 | .76/.96 | .75/.97 | .75/.97 |
| Deep multiscale ESN + DENN | .74/.96 | .73/.96 | .73/.95 | .74/.96 | .72/.95 |
| **Proposed full system** | **.69/.86** | **.67/.84** | **.68/.86** | **.68/.85** | **.68/.85** |

`*` The source table prints `1..22`; it is transcribed as printed rather than
silently corrected. The paper states DENN replacing FCNN improves MAE by
8.0%, 9.4%, 8.1%, 6.8%, 8.8% across 2SE–6SE; and ridge/linear readouts have
roughly 22–25% higher error than the proposed model. Exact ablation protocols
and the claimed optimal layer configuration are in unavailable Supplementary
§2.1, therefore **Not specified in the paper.**

## 11. Baseline comparison (Table 4)

Test MAE / RMSE in `M_JMA`, ordered 2SE–6SE:

| Method | 2SE | 3SE | 4SE | 5SE | 6SE |
|---|---|---|---|---|---|
| LSCross-ESN | .99/1.15 | .99/1.15 | .99/1.15 | .98/1.12 | .96/1.10 |
| LS-ESN | 1.01/1.21 | .99/1.18 | .98/1.02 | .97/1.11 | .97/1.08 |
| Inter-ESN | .96/1.21 | .95/1.20 | .94/1.18 | .94/1.15 | .92/1.12 |
| phi-ESN | .96/1.14 | .95/1.11 | .94/1.12 | .93/1.11 | .92/1.08 |
| Vanilla ESN | 1.21/1.15 | 1.08/1.10 | 1.08/1.08 | 1.02/1.12 | 1.02/1.02 |
| Deep ESN | .84/1.03 | .83/.98 | .83/.98 | .81/.97 | .81/.97 |
| Ensemble ESN | 1.08/1.39 | 1.04/1.32 | 1.01/1.28 | .99/1.25 | .99/1.20 |
| edRVFL | .94/1.08 | .95/1.06 | .91/1.05 | .90/1.03 | .91/1.02 |
| edESN | 1.11/1.42 | 1.02/1.31 | .99/1.21 | .97/1.17 | .98/1.13 |
| SNRNN | 1.12/1.27 | 1.19/1.34 | 1.13/1.28 | 1.02/1.18 | 1.01/1.04 |
| ViT magnitude | .70/.86 | .71/.87 | .75/.95 | .73/.91 | .91/1.15 |
| CRNN | .90/1.11 | .99/1.24 | .80/.99 | .79/.98 | 1.02/1.18 |
| EEWNet | .90/1.07 | 1.01/1.18 | 1.02/1.18 | .81/.98 | .99/1.15 |
| CREIME | .65/.82 | .74/.91 | .71/.89 | .78/.95 | .97/1.14 |
| MFTnet | .84/1.04 | .88/1.16 | .94/1.13 | 1.11/1.37 | 1.06/1.37 |
| DNN regression | 1.43/3.54 | 1.71/3.01 | 1.59/3.41 | 1.56/3.21 | 2.01/4.35 |
| MagNet | .77/.95 | .83/1.01 | .88/1.07 | .96/1.15 | .99/1.15 |
| DFTQuake | .65/.78 | .64/.82 | .72/.88 | .71/.89 | .70/.87 |
| MagPred | .88/.98 | .87/.95 | .92/1.03 | .94/1.05 | .92/1.08 |
| Flowformer | .80/1.03 | .80/1.01 | .79/1.02 | .79/.98 | .78/.98 |
| Reformer | .91/1.11 | .93/1.09 | .92/1.07 | .91/1.02 | .90/1.01 |
| iTransformer | 1.23/1.56 | 1.19/1.46 | 1.10/1.32 | 1.08/1.21 | 1.09/1.12 |
| **Proposed** | **.69/.86** | **.67/.84** | **.68/.86** | **.68/.85** | **.68/.85** |

The paper says all deep-learning/time-series baselines were retrained using
the same splits, MSE validation metric, and 50-epoch budget. Their final
hyperparameters are deferred to Supplementary Tables 12–13 and are **Not
specified in the paper.** The prose says DFTQuake is better at 2SE and 3SE,
then mistakenly says EarthESND outperforms at “3SE to 6SE”; the table supports
EarthESND at 4SE–6SE.

### Training time (Table 5, seconds/epoch)

| Method | 2SE | 3SE | 4SE | 5SE | 6SE |
|---|---:|---:|---:|---:|---:|
| LSCross-ESN | 156.18 | 163.28 | 179.98 | 189.23 | 200.32 |
| LS-ESN | 12.88 | 13.54 | 14.76 | 15.64 | 16.48 |
| Inter-ESN | 40.13 | 49.94 | 55.90 | 50.68 | 65.15 |
| phi-ESN | 5.46 | 7.53 | 7.89 | 8.43 | 10.64 |
| Vanilla ESN | 11.23 | 16.45 | 15.28 | 18.78 | 21.84 |
| Deep ESN | 22.41 | 25.45 | 29.64 | 31.16 | 34.87 |
| Ensemble ESN | 20.61 | 26.21 | 32.75 | 36.86 | 33.12 |
| edRVFL | 10.64 | 22.73 | 28.12 | 32.83 | 37.26 |
| edESN | 24.32 | 29.56 | 32.64 | 36.32 | 39.16 |
| SNRNN | 225.98 | 342.71 | 453.61 | 544.41 | 643.15 |
| ViT magnitude | 23.47 | 22.67 | 23.56 | 40.75 | 52.86 |
| CRNN | 24.79 | 30.86 | 25.90 | 39.07 | 45.23 |
| EEWNet | 80.35 | 90.77 | 98.14 | 107.73 | 121.34 |
| CREIME | 13.78 | 14.05 | 15.25 | 21.58 | 34.24 |
| MFTnet | 25.49 | 21.39 | 21.01 | 42.79 | 45.98 |
| DNN regression | 4.74 | 5.92 | 5.34 | 5.16 | 6.86 |
| MagNet | 10.68 | 11.62 | 14.62 | 16.84 | 18.43 |
| DFTQuake | 67.44 | 74.65 | 82.69 | 89.90 | 94.12 |
| MagPred | 6.53 | 7.13 | 7.27 | 8.85 | 9.02 |
| Flowformer | 31.09 | 30.42 | 32.77 | 32.48 | 33.34 |
| Autoformer | 256.23 | 267.84 | 487.74 | 534.56 | 611.74 |
| iTransformer | 25.98 | 29.76 | 30.43 | 33.88 | 34.87 |
| Reformer | 32.41 | 36.88 | 42.65 | 46.89 | 50.21 |
| **Proposed** | **7.80** | **6.71** | **10.55** | **9.32** | **10.99** |

Hardware and timing methodology are **Not specified in the paper.**

### Regression comparisons (Table 6)

All Table 6 values are in `M_w`, not `M_JMA`; the paper does not describe a
conversion. The proposed row is .55/.68, .53/.67, .54/.67, .54/.67, .54/.67
(MAE/RMSE, 2SE–6SE). Baseline rows are `tau_c` Japan .(1.06/1.26,
1.18/1.44,1.01/1.26,1.01/1.26,.99/1.15); `tau_p` USA (3.20/4.45,
3.32/4.71,3.21/4.45,3.21/4.45,3.20/4.43); `P_d` USA (3.76/3.89,
3.46/3.60,3.76/3.89,3.76/3.89,3.78/3.89); `tau_c` Taiwan (.81/1.02,
.89/1.11,.80/1.02,.80/1.02,1.01/1.26); `tau_c` India (4.87/5.12,
5.34/5.60,4.87/5.12,4.74/5.11,4.87/5.12); `P_d` India (.91/1.14,
.81/1.01,.91/1.14,.90/1.12,.91/1.14); `tau_c` Japan/Taiwan/Italy
(1.34/1.60,1.59/1.87,1.34/1.61,1.24/1.51,1.34/1.61); `tau_c` Japan
(1.43/1.69,1.71/1.99,1.43/1.69,1.23/1.48,1.18/1.32); CAA Japan
(4.41/4.52,4.63/4.77,4.85/4.91,4.99/5.07,4.56/4.98); `P_d` Japan
(1.10/1.36,1.15/1.42,1.10/1.36,1.10/1.36,.99/1.21); CAA Japan
(4.51/5.69,4.54/5.32,4.51/5.68,4.21/5.67,4.12/5.23); and `P_d` Japan
(3.21/4.65,3.93/4.57,3.43/4.21,3.54/4.12,3.12/3.87).

The formulae for those regressions are only said to be in Supplementary Table
9 / §2.7 and are **Not specified in the paper.** For missing 6-s equations,
the authors reuse 5-s equations; for Kumar et al. at 2SE, they reuse 3-s
equations.

## 12. Noto and India results

For India (157 records), reported MAE (`M_w`) for 2–6 s is **1.00, 0.97, 1.21,
1.24, 1.11** and RMSE is **1.13, 1.13, 1.32, 1.35, 1.27**. The stated
explanation for high error is Japan-to-India geographic difference. Noto
quantitative comparisons are deferred to Supplementary §2.8 and are **Not
specified in the paper.** Figure 4 uses ±0.4 `M_w` uncertainty bounds, but the
method used to derive those bounds is **Not specified in the paper.**

## 13. Explicit paper assumptions and claims that constrain implementation

- Timely accurate onsite EEW reduces impact; only early P-wave data should be
  used to predict destructive S-wave consequences.
- Event records pass the STA/LTA and amplitude gate; the model is not claimed
  to handle arbitrary continuous or very-low-SNR streams.
- `M_JMA >= 3` strong-motion onset is detectable under the selected gate.
- Longer P-wave duration generally improves magnitude reliability but reduces
  lead time.
- Japan’s P-wave inputs have 100-Hz sampling and three components.
- Vertical P-wave signals have higher SNR and yield more reliable physics
  features than horizontal components.
- Magnitude is treated as continuous time-series prediction, not tabular-only
  regression; tabular features are complementary rather than sufficient.
- Per-neuron leak rates represent multiple time scales, proposed as 0.1–1 s;
  serial deep reservoirs increase representation/memory capacity.
- Fixed random reservoirs and terminal-state-only readout preserve causality
  and are computationally cheaper than backpropagated RNNs.
- Spectral-radius scaling produces stable dynamics/echo-state property.
- Dendritic branches provide localized nonlinear mixing and are intended to
  outperform a linear reservoir readout.
- Magnitude distribution is imbalanced toward small events; synthetic tabular
  data is intended to reduce the associated skew.
- The 2–6 s window can rarely include the P-wave departure-time information of
  events above 7 `M_JMA`; this motivates restricting the magnitude range.
- Far-distance attenuation and P/S overlap near the epicenter affect error.
- All deep baselines can be fairly compared when retrained on the same splits,
  MSE validation metric, and 50 epochs.

## 14. Paper-to-current-repository mapping

| Paper requirement | Existing repository status | Mapping / required addition |
|---|---|---|
| Dataset catalogue | Implemented generically | `src/acquisition/catalog_client.py` retrieves generic FDSN catalogues; it does not retrieve K-NET/Japan data or match the paper schema. Add a K-NET-specific acquisition adapter and provenance manifest. |
| Waveforms | Placeholder only | `src/acquisition/waveform_client.py` returns a placeholder. Implement retrieval/storage of 3-component strong-motion records. |
| Station metadata/scaling | Placeholder only | `src/acquisition/station_client.py` is a placeholder. Add station metadata plus the paper’s station-specific scale-factor representation (formula unavailable). |
| Raw/processed stores | Directories/config already exist | Use `data/raw/` for immutable waveform/catalogue downloads, `data/processed/` for filtered windows and feature matrices. |
| Configuration | Generic acquisition YAML exists | Extend `configs/acquisition_config.yaml` or add paper-specific configs for source, window sizes, sampling rate, filter, threshold, splits, and seed. |
| Preprocessing | Missing package implementation | `src/preprocessing/` contains only `__init__.py`. Add trigger, QC, baseline, filter, integration, and window modules. |
| Features | Missing | `src/processing/` contains only `__init__.py`. Add feature functions and tests. Feature formulas must be independently specified because the paper does not supply them. |
| ESN/DENN/CTGAN/ensemble | Missing | `src/models/` contains only `__init__.py`. Add isolated, testable model modules and experiment orchestration. |
| Evaluation | Missing | Add metrics, split management, baseline runners, timing, and result persistence. |
| Tests | Acquisition tests exist | Add deterministic unit tests for signal transforms, shapes, masks, feature values, split leakage, and model smoke tests. |
| Reproduction docs | High-level plan exists | Update `docs/PAPER_REPRODUCTION.md` to point to this specification and record implementation deviations. |

Current repository constraints that differ from the paper: `configs/acquisition_config.yaml` targets a generic FDSN/USGS-style sample (`IU.ANMO.BHZ`, one channel, January 2024, magnitudes 4–8); the paper requires 100-Hz, three-component Japan K-NET records from 1996–July 2024 and magnitude 3.0–7.6/7.7. The repository currently contains neither waveform acquisition nor preprocessing/model code.

## 15. Implementation roadmap

### Phase A — reproducible data contract

1. Define a versioned record manifest: event ID, station ID, component paths,
   P pick, sampling rate, scaling provenance, `M_JMA`, distance/depth fields,
   split, and Noto-exclusion flag.
2. Implement K-NET-compatible waveform and station acquisition only after the
   exact permitted data-access method is selected.
3. Persist immutable raw records and generate deterministic stratified splits
   using the paper bins. Document the apparent 7.6 vs 7.7 discrepancy as a
   configurable decision.

Acceptance: 36,196-record equivalent manifest (or a clearly documented
smaller reproduction subset), no event/station leakage policy violation, and
fixed seed retained with every split.

### Phase B — preprocessing and features

1. Implement STA/LTA threshold 2.5, first-20-sample amplitude gate, baseline
   correction, 4-pole bandpass 0.0075–45 Hz, and 2–6-s windowing.
2. Implement acceleration-to-velocity/displacement integration with a chosen,
   documented numerical method and tests.
3. Implement named vertical-component features only after their formulas are
   obtained or an explicit project convention is approved; label the resulting
   run as a reproduction deviation.
4. Materialize `(T, 9)` tensors and tabular feature matrices with provenance.

Acceptance: plotted before/after signals, quality-rejection log, shape tests
for all five windows, and hand-checked synthetic signal tests.

### Phase C — ESN/DENN core

1. Implement sparse, spectrally scaled reservoirs and terminal-state serial
   propagation.
2. Implement a masked dendritic layer, two-layer 64-to-1 readout, GELU/linear
   activations, MSE, and Adam.
3. Expose all reported settings in YAML; expose unresolved reservoir size,
   spectral radius, depth, and input scaling as explicit experiment variables,
   never as undocumented defaults.
4. Run shape, determinism, causality, and spectral-radius tests.

Acceptance: one-window training smoke run; persisted config, seed, metrics,
and artifact hashes; no gradient path through fixed reservoir parameters unless
an intentional documented deviation is selected.

### Phase D — synthetic/ensemble component

1. Implement or adopt a CTGAN only after defining all missing architecture and
   training settings; use training data only.
2. Generate 10,000 rows, validate distributions and target coverage, then fit
   XGB/LGBM/CatBoost on real and augmented data.
3. Implement an explicit final aggregation formula and record weights; use
   equal `1/7` weights only as a project assumption, not as a paper fact.

Acceptance: no test/validation contamination, synthetic-data diagnostics, and
independent prediction artifacts for all seven inputs to the aggregator.

### Phase E — evaluation and paper comparison

1. Implement MAE, RMSE, percentage improvement, training time, and optional
   inference latency.
2. Reproduce incremental ablations before the full model: waveform channels,
   tabular fusion, linear/ridge/FCNN/DENN readouts, depth, multi-scale leaks,
   synthetic and ML blocks.
3. Add the listed baseline models progressively, using one common split and
   50-epoch protocol where applicable.
4. Evaluate Japan test, Noto holdout, and India cross-region data separately;
   never mix `M_JMA` and `M_w` without a documented conversion/interpretation.

Acceptance: results tables with the same column order as Tables 3–6, a
deviation log, timing environment, seed/repetition policy, and a clear
comparison explaining gaps from published numbers.

## 16. Reproduction-risk register

| Risk | Why it matters | Required treatment |
|---|---|---|
| Missing supplement | It apparently contains feature formulas, optimal layers, baseline hyperparameters, timing and inference information. | Do not claim exact reproduction; mark each substituted setting as a deviation. |
| Paper inconsistencies | 6 vs 7 features; magnitude upper 7.6 vs 7.7; leak-vector description vs per-dataset scalar; text/table claims differ. | Make every choice config-driven and record it. |
| Dataset access/schema | Generic FDSN implementation does not match K-NET/PESMOS study records. | Build a source-specific manifest and preserve raw provenance. |
| Scale mismatch | Main results use `M_JMA`, regression table and India results use `M_w`. | Keep target scale explicit at every interface; do not silently compare scales. |
| Potential leakage | Synthetic generation and tabular models must use training data only. | Enforce split-aware pipelines and test them. |
| Undefined final averaging weights | Changes final score materially. | Treat equal averaging as a tested assumption, not a recovered paper setting. |
