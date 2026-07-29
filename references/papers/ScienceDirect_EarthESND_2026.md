# Scalable multiscale echo state reservoirs with dendritic readouts for intelligent earthquake early warning systems

Source conversion: `ScienceDirect_EarthESND_2026.pdf` (local PDF text extraction; 14 pages). Text and line breaks reflect PDF extraction; equations may be represented in plain text.


## Page 1

 
Contents lists available at ScienceDirect
Computers and Electrical Engineering
journal homepage: www.elsevier.com/locate/compeleceng  
Scalable multiscale echo state reservoirs with dendritic readouts for 
intelligent earthquake early warning systems
Anushka Joshi a
 ,∗, Pradeep Singh b
 , Balasubramanian Raman c
a School of Artificial Intelligence and Data Science, Indian Institute of Technology Jodhpur, Rajasthan, India
b Department of Mathematics and Computational Sciences, Indian Institute of Information Technology Surat, Gujarat, India
c Department of Computer Science and Engineering, Indian Institute of Technology Roorkee, Uttarakhand, India
A R T I C L E  I N F O
Dataset link: https://github.com/anushka-joshi
/EarthESND-Model, https://pesmos.org
Keywords:
Earthquake early warning system
Magnitude
Reservoir learning
Echo state network
Dendritic neural network
 A B S T R A C T
Accurate and prompt prediction of earthquake magnitude using the early few seconds of 
earthquake wave is a critical objective of onsite earthquake early warning systems. However, 
it remains challenging because of the highly nonlinear and complex nature of seismic signals. 
Recent advancements in deep sequence-to-sequence learning have demonstrated strong per-
formance in this domain. However, their multi-million trainable parameters require high-end 
computational systems. On the other hand, conventional early warning approaches primarily 
rely on regression-based methods that are computationally efficient but unable to model the 
nonlinear dynamics inherent in seismic signals. To address this, we propose an earthquake 
echo state network with dendrites, a lightweight sequence to scalar architecture based on (i) 
multiscale and multi-layer echo state networks and (ii) enhancement with dendritic neural 
network layers to achieve non-linearity at reservoir read-out. Echo state networks are a type 
of recurrent neural network characterized by a fixed, sparsely connected dynamic reservoir. 
Quantitative analysis reveals that the framework enables efficient modeling of seismic time 
series with training times of 7.80, 6.71, 10.55, 9.32, and 10.99 s for 2, 3, 4, 5, and 6 s of 
primary waveform, respectively. The model is evaluated using 36196 three-component seismic 
records with primary wave windows ranging from 2 to 6 s. A comparative analysis with state-
of-the-art methods demonstrates that the proposed method delivers superior performance in 
terms of both prediction error and computational efficiency, making it a practical solution for 
onsite early warning deployment on low-resource systems.
1. Introduction
The impact of an earthquake can be reduced using a timely and accurate earthquake early warning system (EEWS) that predicts 
earthquake parameters. In an onsite EEWS, the warning is sent to areas using the informative primary waveform (P wave) to predict 
the parameters of the destructive secondary waveform (S wave) of seismic waves [1]. The warning time is usually short to reduce 
damage and early initiation of the rescue operation. Magnitude estimation is a key component in predicting earthquake impact [2]. 
Therefore, it is treated as an important subject worth focusing on for the onsite EEW system. Currently, many EEWS worldwide 
use simple parameter regression relations to predict magnitude [3]. For example, a study shows that recent alarming systems for 
the Taiwan dataset in EEWS use cumulative absolute absement or peak displacement based regression relations by Lin and Wu 
(2025) [3]. However, regression relations that use empirically defined terms with partial information limit the performance of 
∗ Corresponding author.
E-mail address: anushkajoshi@iitj.ac.in (A. Joshi).
https://doi.org/10.1016/j.compeleceng.2026.111161
Received 11 August 2025; Received in revised form 1 April 2026; Accepted 3 April 2026
Computers and Electrical Engineering 135 (2026) 111161 
Available online 7 April 2026 
0045-7906/© 2026 Elsevier Ltd. All rights are reserved, including those for text and data mining, AI training, and similar technologies.

## Page 2

A. Joshi et al.
magnitude estimation [1] and can be replaced by a more advanced framework, such as deep learning. The magnitude estimation is 
shown to perform better when treated as a timeseries prediction problem rather than a tabular parameter prediction problem [1,4,5]. 
Thus, the recent trend involves the use of complex artificial intelligence models for timeseries prediction tasks [6]. However, the 
millions of learnable parameters in these networks require high computational hardware even for inference. The computational 
problem have been addressed in this study by using a scalable echo state network architecture.
EEWS magnitude prediction has a history of state-of-the-art networks. The deep neural network model proposed by Apriani 
et al. (2021) [7], which operates at a sampling rate of 80 Hz, is specifically designed for earthquake magnitude estimation using 
seismic data from the Indonesia region. The deep convolutional network, EEWNet [2] predicts earthquake magnitude (4 to 9) using 
the first 3 s of the P wave, but is limited to epicenter distances of 25 to 200 km. Unlike convolutional neural network (CNN) [8] 
based models, the sequence learning models capture temporal dependencies. Bilal et al. (2023) [9] employed a stacked, normalized 
recurrent neural network (RNN) architecture [10] to forecast earthquakes in the Turkish region. RNNs use high memory and employ 
error backpropagation (BP) [11]. One major drawback of BP is its sensitivity to bifurcations, which can lead to divergence during 
training, high computational cost, and suboptimal local minima [12]. Additionally, the training process is often affected by the 
exploding gradient problem. The long short term memory (LSTM) [10] inverse Correlation framework was proposed by Devi et al. 
(2024) [13] for earthquake forecasting in the Chile region. However, each LSTM unit contains multiple fully connected layers, 
making it training computationally intensive for deep networks with long time spans [14]. The large number of parameters also 
increases the risk of overfitting. Unlike prior EEW magnitude prediction studies [2,9] that rely on linear readouts or end-to-end deep 
architectures without explicitly addressing data imbalance, this work integrates a dendritic neural network (DENN) [15] readout 
and a DENN-based CTGAN framework to enhance nonlinear expressivity and improve generalizability across underrepresented 
magnitude ranges.
Ensembling technique for magnitude prediction by combining CNN and sequence to sequence learning models add generalization. 
This includes a CNN and an LSTM-based architecture for earthquake magnitude prediction for 0 to 5.7 𝑀𝑤 by Mousavi and Beroza 
(2019) [4]. Chakraborty et al. (2022) [16] utilized a convolutional network followed by an LSTM network for magnitude prediction. 
Yoon et al. (2023) [17] utilized a dense CNN and LSTM based model architecture with an embedding network for EEW magnitude 
prediction. After CNN and LSTM ensemble, the focus shifted to more advanced transformer based networks. Transformers have 
demonstrated strong capabilities in sequence modeling and scalable design, which has driven a increase of interest in adapting 
them for time series forecasting. Saad et al. (2022) [5] employed a Vision Transformer network for magnitude prediction using 30 s 
three component seismograms from Texas seismic data, focusing on events within a narrow magnitude range of 0 to 5.7 𝑀𝐿. Ge 
et al. (2024) [18] utilized a Fourier Transformer based architecture for magnitude prediction. However, these networks increase 
computational cost due to the ensembling of many different units. While prior models [5,18] improve accuracy through architectural 
depth and attention mechanisms, the proposed work demonstrates that comparable predictive performance can be achieved using 
a computationally efficient reservoir framework.
The advanced EEWS used in the USA, called ShakeAlert, employs EPIC for rapid point-source estimation and FinDer for finite 
fault rupture detection using early P wave signals. However, these physics based algorithms rely on predefined models and multi 
station data, limiting adaptability and accuracy compared to machine learning approaches, and offer scope for improvement [19]. 
Another model, installed in New Zealand, the Eastern Ruapehu Lahar Warning System [20], uses only threshold based logic to trigger 
alarms. More advanced existing EEW, such as the CRED framework [21], detect earthquake signals using a 30 s long window for 
real implementation to continuous data recorded in Guy-Greenbrier, Arkansas, using CNN and LSTM networks.
The most widely adopted approach focuses on component adaptation on timeseries, including Autoformer [22]. These archi-
tectures particularly refine the attention mechanism to capture temporal dependencies and to optimize long-sequence complexity. 
However, the rise of larger lookback windows degraded performance and introduced larger computation explosion as a challenge 
in these frameworks [6]. Another challenge is that, although the ordering of time steps is crucial in time series, these models often 
use permutation-invariant attention along the temporal axis, thereby ignoring the sequential order [23]. Together, these factors 
reduce the Transformer’s ability to learn rich representations and model dependencies across variables, ultimately limiting both its 
effectiveness and generalization on diverse datasets [6]. To overcome the above limitations, iTransformer [6] and Reformer [24] 
use reversible layers in the Transformer. However, these layers can introduce numerical errors that accumulate across layers, 
potentially reducing overall model performance. To cut off cost computation in transformer framework, the Flowformer [25] 
has been introduced. However, the predictive effectiveness is reduced. In this study, earthquake magnitude prediction is treated 
as a timeseries prediction problem, and representative transformer architectures including Autoformer [22], iTransformer [6], 
Reformer [24], and Flowformer [25] are used as benchmark models. Unlike these computation intensive frameworks, which may 
hinder rapid disaster warning in resource constrained regions, the proposed approach achieves both lower computational cost and 
reduced prediction error. This demonstrates that increasing architectural complexity for generalized timeseries modeling does not 
necessarily result in superior performance for complex seismic energy pattern prediction tasks.
The high computation requirement problem is addressed recently by Echo State Networks (ESNs) [26] that provide a middle 
ground. Over the past decade, reservoir computing has gained attention as an alternative to gradient-based approaches for training 
recurrent neural networks [27]. ESNs have long been leveraged for chaotic atmospheric and hydrological signals, including rainfall 
runoff forecasting, wind speed prediction, and geomagnetic indices [14]. Therefore, ESNs offer greater learning efficiency for physics-
based signals compared to complex architectures [14]. ESN addresses convergence challenges and reduces computational costs by 
using a least-squares approach for training rather than traditional methods [14]. 𝜙-ESN by Gallicchio and Micheli (2011) [28] 
extends a standard ESN by projecting its reservoir into a larger, randomly weighted space via an Extreme Learning Machine, 
Computers and Electrical Engineering 135 (2026) 111161 
2

## Page 3

A. Joshi et al.
thereby capturing richer temporal dynamics for improved predictions. However, it relies on a single-scale reservoir. To overcome 
this, multi-reservoir ESN models have been developed that use multiple reservoirs to improve prediction performance [14].
Research on DeepESN architectures [29] has shown that stacking reservoirs can significantly increase short-term memory capacity 
and enrich feature representations [30]. Inoue et al. (2024) [31] and Sun et al. (2024) [14] utilized multi-scale ESN to achieve better 
performance than regular ESN. Consequently, DeepESN [29] and its variants [32] often achieve better prediction performance than 
standard single layer ESN models [14]. Deep-ESNs are well-suited for handling nonlinear dynamic signals with multi-scale temporal 
patterns [14]. However, most ESN studies rely on a single-scale leak factor that fails to capture the broadband nature of earthquake 
sources. Leaking rate controls the decay of neuron dynamics, effectively adjusting how much past information influences the current 
state. By tuning the leaking rate for each layer, Deep-ESNs can achieve layer-specific temporal responses without the rapid signal 
loss that occurs when scaling input weights [33]. The long short term ESN (LS-ESN) by Zheng et al. (2020) [34] consists of three 
independent reservoirs, each designed with distinct recurrent dynamics to capture temporal dependencies at different time scales 
within the time series. Further, advancement involves the Long short-term cross ESN (LSCross-ESN) by Jiang et al. (2025) [35]. It 
enables the network to capture and fuse multi-scale temporal dependencies by allowing information exchange between reservoirs 
with delayed and sliding-window connections, preserving both long- and short-term features for better time series prediction. Inter-
ESN [36] introduces bidirectional links between two reservoirs, enhancing the exchange of internal states and strengthening the 
model’s overall representational capacity. However, in the case of earthquake signals, where high magnitude depends on long-time 
phase and low magnitude depends on shorter-time phase, it is complicated to consider both using current ESN frameworks. Multi-leak 
ESNs can smoothly regulate temporal scales via leak rates, whereas LSCross-ESN [35] relies on discrete reservoirs and delay settings, 
which are harder to balance [31]. As a result, clear design guidelines for reservoir behavior are still lacking. To avoid the trial-and-
error method and the Bayesian optimization approach, we utilized multiscale leaky rate methods that exhibit multiple time-scale 
dynamics to enhance nonlinear dynamic timeseries prediction. Another important aspect of this study is replacing the linear or 
traditional readouts with neurophysically inspired readouts. Neurophysiology reveals that biological neurons integrate inputs over 
multiple membrane time constants and employ nonlinear dendritic sub-compartments to enrich their computational repertoire [37]. 
Transplanting this principle to artificial networks has triggered a wave of DENN [15] in which each hidden unit is partitioned into 
sub-compartments that perform quadratic or threshold operations on restricted input subsets. At equal parameter count, dendritic 
ANNs exhibit higher robustness and sample efficiency than classical multi-layer perceptrons [38]. Poirazi and Mel (2001) [39] 
demonstrated that dendritic structures can achieve high capacity through structural learning and random synapse formation. The 
DENN network differs by modeling both the nonlinear response and the localized nonlinearity. Localized nonlinearity refers to a 
synapse affecting nearby synapses in a nonlinear manner, rather than influencing only the entire neuron [15]. Recently, DENN has 
been utilized for earthquake magnitude and peak ground acceleration prediction by Joshi et al. (2025) [1], which represents its 
success in EEW prediction tasks. These advances motivate our adoption of a multiscale leakage vector combined with dendritic 
readouts for EarthESND.
The work has been extended to address data imbalance by generating a synthetic dataset using conditional tabular adversarial 
networks (CTGAN) [40], with a dendritic neural network in the generator and discriminator blocks of the GAN. Data augmentation 
using GANs has been shown to be an effective technique for handling data imbalance in earthquake magnitude prediction [41]. 
Therefore, in this study, we employ CTGAN to generate synthetic tabular data, providing new insights into data augmentation for this 
task. The shallow ML techniques are still utilized to handle earthquake magnitude prediction [42]. Thus, the generated synthetic data 
are integrated into the machine learning (ML) module, where they are used to enhance and average the final magnitude predictions. 
Artificial intelligence techniques require a well balanced dataset, especially in earthquake magnitude prediction, where the dataset 
is more heavily weighted toward small events. Recent work by Joshi et al. (2025) [41] proves that onsite magnitude prediction could 
be improved using data imbalancing techniques. Based on the study by Joshi et al. (2025) [41], we applied CTGAN [40], enhanced 
with dendritic neural networks in both the generator and discriminator, are used to generate synthetic tabular data samples.
Translating these principles to ESNs suggests (i) using a vector of leak rates to maintain parallel memories spanning 10−1–101 s, 
and (ii) replacing the plain affine read-out with dendrite-like quadratic mixing to boost expressiveness at negligible training cost. 
Biological neurons are more complex and superlinear in nature [15] than typical neural networks [43]. The presence of active 
channels, along with the leaky properties of dendritic membranes, indicates that a single synaptic input may exert a nonlinear 
effect on nearby synapses [15]. This study introduces EarthESND, a multi-scale Echo State Network with dendritic read-outs tailored 
for real-time magnitude prediction of events recorded in Japan using 2, 3, 4, 5, and 6 s of P-wave dataset. The key contributions of 
the proposed work are: (1) Cost Effective modeling: Unlike prior EEW magnitude prediction approaches that rely on computationally 
intensive deep learning models, this study emphasizes the use of reservoir computing on low-cost devices, achieving comparable 
prediction performance with reduced computational demands. (2) Multiscale reservoir: This work employs a multiscale, deep ESN 
architecture for efficient time series prediction. A log-uniform leak vector enables simultaneous tracking of fast P-wave onsets 
and slower cumulative-energy build-up. (3) Dendritic read-out: The final layer is replaced with a more expressive dendritic neural 
network, which also incorporates physics-based earthquake parameters as additional tabular inputs, making the framework novel 
compared to existing EEW prediction models. (4) Synthetic Data Generation: The study is further extended to address data imbalance 
by generating synthetic samples using a dendritic neural network based generator and discriminator units in a CTGAN framework, 
namely, dendritic conditional tabular generative adversarial network (DENN-CTGAN). (5) Extensive Result Study: Experiments were 
conducted on recent efficient time-series transformers, novel ESN frameworks, and state-of-the-art regression and deep learning 
models for magnitude prediction, followed by a detailed analysis of the 2024 Noto earthquake and inter-region Indian earthquake 
analysis using the proposed framework.
Computers and Electrical Engineering 135 (2026) 111161 
3

## Page 4

A. Joshi et al.
Fig. 1. End-to-end EarthESND workflow for onsite EEW magnitude estimation. (a) The triggered strong-motion seismogram is recorded using the 
short-term average and long-term average algorithm [44]. (b) The processed waveforms are passed to the (c) reservoir network. (d) Extraction of 
physics-based tabular features from input waveforms. (e) The concatenated input features from the reservoir and tabular features are passed to 
DENN for magnitude prediction, 𝑦𝐸𝑆𝑁 . (f) The synthetic dataset is generated using DENN-CTGAN. (g) The synthetic and real datasets are passed 
to the ML ensemble block. (h) The final result, 𝑦𝑝𝑟𝑒𝑑 , is the average of the predicted magnitude from the ML Ensemble block and 𝑦𝐸𝑆𝑁 .
Motivation. The utilization of low-end computational machines for earthquake parameter prediction enables the wide resolution 
to develop cost-effective yet efficient EEW systems. This approach achieves comparable performance with minimal computational 
cost, enabling wider participation in research and the practical deployment of EEW.
2. Methodology
2.1. Problem formulation and notation
The raw accelerograms of three components, named as north-south (NS), east–west (EW), and up-down (UD), of early 𝑁
seconds of P wave are passed as input to the model as shown in Fig.  1(a). These raw acceleration waveforms are transformed 
into processed waveform 𝑐 ∈ R𝑇 ×1, 𝑐 ∈ { 𝑁𝑆, 𝐸𝑊 , 𝑈 𝐷 } using baseline correction, station specific scaling, and transformed into 
velocity, 𝑐 ∈ R𝑇 ×1, 𝑐 ∈ { 𝑁𝑆, 𝐸𝑊 , 𝑈 𝐷 }, and displacement, 𝑐 ∈ R𝑇 ×1, 𝑐 ∈ { 𝑁𝑆, 𝐸𝑊 , 𝑈 𝐷 }. 𝑇 = 𝑆 × 𝑁 denotes the sampling 
frequency times seconds (100 Hz for the target dataset).
𝐗𝑖 = {𝑁𝑆 , 𝐸𝑊 , 𝑈 𝐷, 𝑁𝑆 , 𝐸𝑊 , 𝑈 𝐷, 𝑁𝑆 , 𝐸𝑊 , 𝑈 𝐷} ∈ R𝑇 ×𝐶 is a multichannel seismograms of length 𝑇 sampled. Channel 
size 𝐶 = 9 , corresponding to the concatenation of three-component acceleration 𝐚(𝑡) and the co-integrated velocity 𝐯(𝑡) = ∫ 𝐚(𝑡) 𝑑𝑡
and displacement 𝐝(𝑡) = ∫ 𝐯(𝑡) 𝑑𝑡 as shown in Fig.  1(a). Our goal is to learn a mapping 𝑓𝜽 ∶ R𝑇 ×𝐶 → R such that ̂𝑀𝑖 = 𝑓𝜽(𝐗𝑖). Some 
prominent tabular features (𝑇 𝑎𝑏𝑚𝑎𝑔 ∈ R6×1) that correlate well with earthquake magnitude are predicted from the waveform. The 
waveform 𝑖 ∈ R𝑇 ×9 for 𝑖th record and 𝑇 𝑎𝑏𝑚𝑎𝑔 ∈ R6×1 are passed as input to the proposed architecture. The current multi-scale 
ESN with dendritic readouts produces deterministic point estimates of magnitude (continuous real values). The magnitude (𝑦𝑝𝑟𝑒𝑑 ) 
in 𝑀𝐽 𝑀𝐴 scale is predicted as output.
P phase selection. Prior to modeling, we reject traces that do not contain an event onset through a two-stage gate. First, the 
earthquake P wave recording from the station is picked using the short-term average and long-term average algorithm (STA/LTA) 
pick [44] with a threshold of 2.5. This threshold was empirically selected to reliably capture the onset of 𝑀𝐽 𝑀𝐴 ≥ 3 strong-
motion seismogram, ensuring early and stable detection of the initial P-wave arrival. Then apply the scaling factor corresponding to 
each station. To further suppress small-amplitude fluctuations and spurious triggers, we compute the mean of the first 20 samples 
of each candidate window; only windows with a mean acceleration exceeding 0.01 gal are passed to the ESN. After STA–LTA 
detection, we perform baseline correction to remove baseline drift by subtracting the mean of the first 20 samples [45]. Then apply 
Butterworth bandpass filtering with a 4-pole bandpass filter of 0.0075 to 45 Hz to clean the waveform and remove the original shift. 
Consequently, the present framework is intended for event-containing earthquake records, and performance on arbitrary continuous 
streams or extremely low-SNR traces outside this gate is not applicable. Traces with missing waveform segments or weak signals 
are automatically rejected during preprocessing using a mean amplitude criterion of 0.01 gal computed over the first 20 samples. 
This ensures that only clear, strong motion signals containing P-wave records are passed to the model. Previous studies have shown 
that longer P wave durations lead to more reliable magnitude estimation, but the lead time cost decrease [46]. Thus, in practice, 
researchers only need to pass a strong-motion seismogram into the model, and if the event magnitude is greater than 𝑀𝐽 𝑀𝐴 3, the 
model will automatically detect and estimate it without any manual intervention.
Reservoir dynamics. An Echo State Network projects the sequence 𝐗𝑖 into a high-dimensional state trajectory as given by 𝐡𝑡+1 =
(1 − 𝜶) ⊙ 𝐡𝑡 + 𝜶 ⊙ tanh(𝐖𝑖𝑛𝐱𝑡 + 𝐖𝑟𝑒𝑠𝐡𝑡
), where 𝐡𝑡 ∈ R𝑁𝑟𝑒𝑠 , 𝐱𝑡 ∈ R𝐶 is the input at time 𝑡, 𝐖𝑖𝑛 ∈ R𝑁𝑟𝑒𝑠×𝐶 and 𝐖𝑟𝑒𝑠 ∈ R𝑁𝑟𝑒𝑠×𝑁𝑟𝑒𝑠 are fixed 
random matrices, and 𝜶 ∈ (0 , 1]𝑁𝑟𝑒𝑠 is the vector of leak rates. We retain only the terminal state 𝐡𝑇 as a sequence fingerprint; thus 
the design matrix is 𝐇 = [𝐡⊤
1 , … , 𝐡⊤
𝑁 ]⊤ ∈ R𝑁×𝑁𝑟𝑒𝑠 . The ESN formulation preserves causality and offers (𝑁𝑟𝑒𝑠𝐶) compute per sample, 
orders of magnitude lighter than back-propagated RNNs [26]. A dendritic neural network read-out then yields the prediction.
Computers and Electrical Engineering 135 (2026) 111161 
4

## Page 5

A. Joshi et al.
Dendritic neural network. The first step in DENN is a composition of dendritic layers that defines a function 𝐷𝐸𝑁𝑁 (𝑥) =
{𝑓out◦𝑓 𝐷
𝐿 ◦ ⋯ ◦𝑓 𝐷
1 (𝑥)}, where 𝑓 𝐷
𝑙 ∶ R𝑛𝑙−1 → R𝑛𝑙 represents the dendritic layer 𝑙 [15]. Each layer contains 𝑛𝑙 neurons, and each 
neuron consists of 𝑑 dendritic branches. Each branch receives a subset of inputs (𝑛𝑙−1∕𝑑) from the previous layer and performs 
a local weighted summation followed by a nonlinear transformation: ℎ𝑙,𝑖,𝑗 (𝑥𝑙−1) = 𝜙𝑗
(∑𝑛𝑙−1
𝑚=1(𝑆𝑙,𝑖,𝑗,𝑚 𝑊𝑙,𝑖,𝑗,𝑚 ) 𝑥𝑙−1,𝑚 + 𝑏𝑙,𝑖,𝑗
) , 𝑗 ∈ [ 𝑑],
where 𝑆𝑙,𝑖,𝑗,𝑚 ∈ {0, 1} denotes whether the 𝑚th input connects to the 𝑗th branch of the 𝑖th neuron, 𝑊𝑙,𝑖,𝑗,𝑚 are the synaptic weights, 
and 𝜙𝑗 (⋅) is the local dendritic nonlinearity (e.g., sigmoid or Gaussian). The neuron output aggregates all dendritic branch responses: 
𝑔𝑙,𝑖(𝑥𝑙−1) = 𝑓𝑖
(∑𝑑
𝑗=1 ℎ𝑙,𝑖,𝑗 (𝑥𝑙−1)
)
+𝑏𝑙,𝑖, where 𝑓𝑖(⋅) is the neuron-level activation function and 𝑏𝑙,𝑖 is the neuron bias. Thus, the dendritic 
layer output is 𝑓 𝐷
𝑙 (𝑥𝑙−1) = [ 𝑔𝑙,1(𝑥𝑙−1), … , 𝑔𝑙,𝑛𝑙 (𝑥𝑙−1)]⊤.. In particular, when 𝑑 = 1 and 𝜙(⋅) is linear, the dendritic layer reduces to a 
standard fully connected layer. The DENN architecture ensures nonlinearity and localized learning by controlling a subset of input 
passed [15].
2.2. Proposed framework
Deep Echo state Network (DESN) [47] involves incorporating multiple reservoirs and allowing for dense connections for complex 
representations. Following the neurophysiological observation that cortical pyramidal Cells integrate inputs over multiple membrane 
time scales [37], we draw a vector 𝜶 = [𝛼(1), … , 𝛼(𝑁𝑟𝑒𝑠)] from a log–uniform prior 𝛼(𝑘) ∼  (10−1, 1). The resulting update rule 
𝐡𝑡+1 = (1 − 𝜶) ⊙ 𝐡𝑡 + 𝜶 ⊙ tanh(𝐖𝑖𝑛𝐱𝑡 + 𝐖𝑟𝑒𝑠𝐡𝑡) creates parallel fading memories ranging from 0.1 to 1 s. This design shows that Deep-ESN 
performance improves by 15–25% on chaotic signals, with empirical support [31].
We stack 𝐿 multi–scale reservoirs in series and propagate the seismic tensor only forward as shown in Fig.  1(c). The output of 
layer 𝓁 is fed as the sole input to layer 𝓁 + 1. Intermediate states are not concatenated or skip–connected. Formally, the update rule 
with 𝐡(𝓁)
𝑡 ∈ R𝑁 (𝓁)
res be the hidden state of layer 𝓁 at time 𝑡 is as follows: 
𝐡(𝓁)
𝑡+1 = (1 − 𝜶(𝓁)) ⊙ 𝐡(𝓁)
𝑡 + 𝜶(𝓁) ⊙ tanh(𝐖(𝓁)
in 𝐱(𝓁)
𝑡 + 𝐖(𝓁)
res 𝐡(𝓁)
𝑡
) (1)
where 𝐖(𝓁)
in ∈ R𝑁 (𝓁)
res ×𝐶(𝓁)
, 𝐖(𝓁)
res ∈ R𝑁 (𝓁)
res ×𝑁 (𝓁)
res , and the leak vector 𝜶(𝓁) ∈ (0, 1]𝑁 (𝓁)
res are fixed. After the final reservoir (𝓁 = 𝐿) we retain 
only its terminal state 𝐡(𝐿)
𝑇 . Only the last reservoir contributes to the read-out, and gradients are never propagated through any other 
ESN layer. 𝜶(𝓁) is the per-neuron leak rate vector. It controls how much of the new input (from tanh(⋅)) influences the next hidden 
state versus how much of the previous state is retained [14].
To initialize the reservoir in a multi layer and multi ESN, a random recurrent matrix 𝑊 (𝑖,𝓁)
raw ∈ R𝐷(𝓁)×𝐷(𝓁)
 is first generated for 
𝑖th stack of 𝓁𝑡ℎ layer reservoir. Each reservoir in each layer follows Eq. (1). 𝜈 ∈ (0 , 1] is the sparsity denoting fraction of non-zero 
weights. Binary masking with 𝜈 ∈ (0, 1] check is done for 𝑊 (𝑖,𝓁)
raw  and filled with standard normal distribution ( (0, 1)). This improves 
memory separation and computational efficiency. The spectral radius of this matrix is then computed as 𝜌(𝓁)
raw = max 𝑖 |𝜆𝑖(𝑊 (𝑖,𝓁)
raw )|, 
where 𝜆𝑖 are the eigenvalues of 𝑊 (𝑖,𝓁)
raw . To ensure the desired dynamic behavior of the reservoir, the matrix is rescaled so that its 
spectral radius matches a predefined target value 𝜌(𝓁)
target. This is done using the transformation, for 𝑖𝑡ℎ ∈ {0, 𝑘} layer of reservoir and 
𝓁𝑡ℎ reservoir with 𝑘 total layers: 
𝑊 (𝑖,𝓁)
𝑟𝑒𝑠 = 𝜌(𝓁)(𝑊 (𝑖,𝓁)
𝑟𝑒𝑠 ) = 𝑊 (𝑖,𝓁)
raw
𝜌(𝓁)
raw
⋅ 𝜌(𝓁)
target (2)
This procedure ensures that the internal dynamics of the reservoir are stable and satisfy the echo state property. 𝑊𝑖𝑛 is the 
input scaling parameter and is initialized with a normal distribution. The output from one reservoir is passed as input to the other 
reservoir. After processing all 𝑇 timesteps, the output of the 𝐿th layer is its terminal hidden state: 𝐇𝐿 = 𝐡(𝐿)
𝑇 ∈ R𝑁 (𝓁)
res .
Data fusion enables more complete and precise insights to support decision-making in disaster management [48]. The earthquake 
parameters are correlated with physics-based earthquake features derived from the P-waveform. Thus, to decrease prediction error, 
the output received from the last ESN layer has been concatenated with the tabular feature set. The tabular feature set is denoted 
by 𝑇 𝑎𝑏𝑚𝑎𝑔 as shown in Fig.  1(d). These parameters have been widely used as tabular input in several studies for magnitude 
prediction [41,49,50] and are described in Supplementary Section 1.1, Feature Description. The tabular set consists of characteristic 
period (𝜏𝑐), integrated squared displacement (𝐼𝐷 2), integrated squared velocity (𝐼𝑉 2), P wave index (𝑃 𝐼), root sum of squared 
velocity (𝑅𝑆𝑆𝐶𝑉 ), peak velocity acceleration ratio (𝑇𝑣𝑎), and cumulative absolute velocity (𝐶𝐴𝑉 ). These parameters are obtained 
from the vertical component of the P waveform since the signal-to-noise ratio is better in the vertical component than in the 
horizontal components. This makes them more reliable for high-quality earthquake magnitude analysis [51].
Linear read-outs are the norm in reservoir computing because they admit a closed-form solution, yet they implicitly assume 
that the reservoir state is linearly separable with respect to the target. We augment the read-out with a DENN to raise the 
expressive ceiling without iterative back-propagation. The final reservoir’s output is concatenated with tabular features, 𝐶 =
[𝐻 (𝐿)|𝑇 𝑎𝑏𝑚𝑎𝑔]. It is then passed through 𝐷𝐸𝑁𝑁 (𝐶(𝑡); 𝜃). We obtain the magnitude prediction by a 𝐾 layer dendritic neural: 
𝑦𝑝𝑟𝑒𝑑 = 𝐷𝐸𝑁𝑁 𝑖+1...(𝐷𝐸𝑁𝑁 1(𝐶(𝑡); 𝜃1), 𝜃𝑖+1), 𝑖 ∈ {0 , … , 𝐾}. There are two DENN layers utilized in this network that give optimal 
performance. Stochastic regularizers like dropout and activation functions like rectified linear unit remain distinct [52], even though 
both influence a neuron’s output. The Gaussian error linear units (GELU) activation is utilized to provide a smooth nonlinearity that 
can be interpreted as the expected value of an input-dependent stochastic dropout-like mask. The GELUs [52] activation have been 
utilized in 𝐷𝐸𝑁𝑁 1 and is represented as: GELU(𝑥) = 1
2 𝑥
(
1 + tanh(√
2
𝜋 (𝑥 + 0.044715 𝑥3)))
. The linear activation has been utilized in 
the 𝐷𝐸𝑁𝑁 2 layer. The two DENN layers, 𝐷𝐸𝑁𝑁 1 and 𝐷𝐸𝑁𝑁 2 are used after reservoir network units (𝑛𝑙) of 64 and 1 for all five 
datasets. The branches (𝑑) of 𝐷𝐸𝑁𝑁 1 are 2, 2, 3, 3, and 2 are 2SE, 3SE, 4SE, 5SE, and 6SE datasets. The sparsity (𝜈 ∈ (0 , 1]) of 
Computers and Electrical Engineering 135 (2026) 111161 
5

## Page 6

A. Joshi et al.
the 2SE, 3SE, 4SE, 5SE, and 6SE datasets is 0.1, 0.1, 0.2, 0.1, and 0.1. The prediction from the final DENN layer is the predicted 
magnitude using seismograms passed to the reservoir network and is denoted by 𝑦𝐸𝑆𝑁  as shown in Fig.  1(e). The adaptive moment 
estimation (Adam) optimizer is utilized in this work, which combines the advantages of handling sparse gradients (increases the 
learning rate for rarely-updated parameters) and handling non-stationary settings (mini-batches that vary a lot) [53]. Moreover, 
unlike stochastic gradient descent, each parameter get its own adaptive weights [53]. The learning rate of the reservoir network for 
all five datasets is set to 0.001, 0.0014, 0.001, 0.001, and 0.001. The mean squared error (MSE) is used as the loss function. The 
multiple scales are obtained from multiple leaky rates, which are selected as 0.8, 1.0, 0.5, 0.1, and 0.08 for all dataset (2SE to 6SE). 
The epoch size is 50 for all five datasets, and batch_size is 512 for all datasets.
2.3. Generating synthetic dataset
The imbalance causes the model performance to be skewed towards the majority magnitude cases. The dendritic neural network-
based CTGAN delivered in the proposed work acts as an answer to this problem. CTGAN employs mode-specific normalization 
to effectively represent multimodal and non-Gaussian data distributions of continuous columns. The mode-specific normalization 
utilizes a Variational Gaussian Mixture model [54] to approximate its distribution of continuous column (𝐶𝑖). The learned Gaussian 
mixture for column 𝐶𝑖 is expressed as: 𝑃𝐶𝑖 (𝑐𝑖,𝑗 ) = ∑𝑚𝑘
𝑝=1 𝜇𝑝  (𝑐𝑖,𝑗 ; 𝜂𝑝, 𝜃𝑝), where 𝜇𝑝 and 𝜃𝑝 represent the weight and standard 
deviation of the 𝑝th mode, respectively. The conditional generator in CTGAN aims to reproduce the true data distribution, which 
can be formulated as: P(row) = ∑
𝑘∈𝐷𝑖∗ P𝐺(row ∣ 𝐷𝑖∗ = 𝑘∗) P(𝐷𝑖∗ = 𝑘) [40]. The DENN network serves as both the generator 
and discriminator in the CTGAN architecture, referred to as DENN-CTGAN, which is employed in this study for synthetic data 
generation, as shown in Fig.  1(g). The t-Distributed Stochastic Neighbor Embedding (t-SNE) [55] elevates the crowding and the 
optimization problems of SNE and are used in our study to visualize actual and synthetic high dimensional data as shown by Fig. 
1(g) for 3SE dataset. t-SNE Plots comparing synthetic and real input output parameters generated by DENN-CTGAN are presented 
in Supplementary, Figure 1. A total of 10000 synthetic records are generated using the features 𝑇 𝑎𝑏𝑚𝑎𝑔 and target values 𝑦𝑎𝑐𝑡 from the 
training set, which serves as inputs to the DENN-CTGAN model. The resulting synthetic dataset is denoted as {𝑇 𝑎𝑏𝑠𝑦𝑛 ∣ 𝑦𝑠𝑦𝑛}. The 
augmented dataset is the combination of {𝑇 𝑎𝑏𝑎𝑢𝑔|𝑦𝑎𝑢𝑔} = { 𝑇 𝑎𝑏𝑠𝑦𝑛|𝑦𝑠𝑦𝑛} ∥ { 𝑇 𝑎𝑏𝑎𝑐𝑡 |𝑦𝑎𝑐𝑡 }. These records are sent to the ML Ensemble 
block for training. The ML ensemble block consists of the XGBoost (XGB) [56], Light GBM (LGBM) [57], and CatB [58] learners 
trained using an augmented dataset and a real dataset. Each learner is trained twice: once using the augmented dataset {𝑇 𝑎𝑏𝑎𝑢𝑔 ∣ 𝑦𝑎𝑢𝑔}
and once using the real dataset {𝑇 𝑎𝑏𝑎𝑐𝑡 ∣ 𝑦𝑎𝑐𝑡}. Thus, six ensemble models are obtained in total. The final magnitude prediction is 
computed by averaging the outputs of these six ML models with the 𝑦𝐸𝑆𝑁  result from the reservoir framework, as illustrated in Fig. 
1(h).
3. Dataset
Selected area. The seismicity rate in Japan is the highest, and large earthquakes are frequently experienced in Japan. These 
earthquakes are due to the complex geodynamic context of oceanic plate interaction. These plates include the Philippine and Pacific 
sea plates that subduct beneath the Eurasian plate [49]. These plate interactions cause deep, intermediate, and crustal earthquakes 
in Japan. The raw strong-motion seismograms of the earthquake dataset have been organized in the Kyoshin Network (K-NET) 
repository, maintained by the Japan Meteorological Agency (JMA) catalog [59]. The database’s accuracy and the variety of events 
it contains make it a crucial dataset for understanding seismic signatures.
Selected events. Fig.  2 represents the (a) station and (b) epicenter location of the selected earthquakes. Events are split into 70:15:15 
of train, test, and validation datasets with 25337, 5429, and 5430 records from 1996 to July 2024 as shown in Table  1. The Fig. 
2(c) represents the magnitude distribution of the test, train, and validation sets with respect to epicenter distance. The qualitative 
overall counts of the train, test, and validation splits are shown in Fig.  2(d) and (e) for earthquake epicenter distance and magnitude. 
Fig.  2(f) and (g) represent the scatter plot of focal depth and epicenter distance, and the count of focal depth with respect to the 
dataset. We used the train:test:validation split with well-established practical heuristics commonly used in applied machine learning, 
and validated these choices empirically via quantitative analysis of random splits [60]. Care was taken to address the imbalance 
in magnitude distribution in real events. Since the magnitudes are continuous, they were divided into discrete bins ranging from 
3.0 to 8.0 with an interval of 0.5 using np.arange(3.0, 8.5, 0.5) to ensure stratified sampling across the magnitude range. We have 
separated the Noto event 232 records for testing. Supplementary Table 2 shows that the 70:15:15 ratio was selected as the optimal 
ratio set for the proposed prediction problem. In this work, the dataset is segmented into windows of 2, 3, 4, 5, and 6 s from 
the initial portion of the P-wave for magnitude prediction. The training, testing, and validation records remain the same across all 
segments, with only the time window varying. These datasets are referred to as 2SE, 3SE, 4SE, 5SE, and 6SE, corresponding to the 
2, 3, 4, 5, and 6-second P-wave windows, respectively. The developed model imposes no lower or upper limits on the selection 
of epicenter distance, focal depth, or hypocenter distance. Only earthquakes with magnitudes ranging from 3.0 to 7.6 𝑀𝐽 𝑀𝐴 were 
considered, thereby reducing the influence of outliers to prevent the high data imbalance problem. Another reason for selecting 
magnitudes below 8 𝑀𝐽 𝑀𝐴 is that the analysis by Noda and Ellsworth (2016) [61] shows that for earthquakes of magnitudes 5, 6, 
and 7 𝑀𝑤, the departure period emerges approximately 0.38 to 1.5 s, 1.05 to 4 s, and 2.87 to 10 s after the P-wave arrival. Thus, 
the 2- to 6-second P-wave window can rarely contain the departure time information for greater than 7 𝑀𝐽 𝑀𝐴.
We have used earthquake events recorded in the Indian strong-motion seismograms to assess the generalizability of the 
framework in areas of sparse coverage, as shown in Fig.  2(h). These events were taken from the ‘‘Program for Excellence in 
Strong Motion Studies (PESMOS)’’ database, curated by the Indian Institute of Technology, Roorkee, India (www.pesmos.in). These 
events form the inter-regional earthquake dataset consists of 157 records of 12 earthquakes. Details of this dataset are provided in
Table  2.
Computers and Electrical Engineering 135 (2026) 111161 
6

## Page 7

A. Joshi et al.
Table 1
The maximum and minimum values of parameters used in the training, testing, and validation datasets.
 Set Records Parameter
 Magnitude (𝑀𝐽 𝑀𝐴) Epicenter Distance (km) Focal Depth (km) Hypocenter Distance (km)
 Min Max Min Max Min Max Min Max  
 Training 25 337 3.0 7.7 1.08 1607.85 0 619 5.57 1668.29  
 Testing 5 429 3.0 7.7 2.87 1253.71 0 619 9.49 1341.38  
 Validation 5 430 3.0 7.7 2.02 1404.37 0 619 7.30 1483.17  
Fig. 2. Geographical visualization of the: (a) station and (b) earthquake epicenters. The color bar indicates the focal depth (km). (c) Scatter plot 
of magnitude against epicentral distance (km). (d) Distribution of epicentral distances and (e) magnitude distributions for the training, validation, 
and test sets. (f) Focal depth and epicentral distance. (g) Focal depth distribution across data splits. (h) The spatial distribution of the Indian 
region stations and earthquake epicenters with 157 records. The color bar represents focal depth (km) and land elevation (m).
Table 2
Dataset of inter-region earthquakes occurring in India, Myanmar, Bhutan, and Nepal with 157 records and 12 
earthquakes.
 Region Date No. of Stations Magnitude (𝑀𝑤) Focal Depth 
 Myanmar-India Border 11-08-2011 12 5.6 12  
 Uttarkashi, India 21-09-2009 10 4.7 12  
 Bhutan 31-12-2009 5 5.5 5  
 Punjab - Himachal Border, India 14-03-2010 12 4.6 13  
 Bageshwar, Uttarakhand, India 01-05-2010 6 4.6 13  
 India- Nepal Border 04-04-2011 23 5.7 24  
 Nepal 01-12-2016 20 5.2 20  
 Chamoli, Uttarakhand, India 20-06-2011 11 4.6 7  
 Sonipat, India 07-09-2011 6 4.2 7  
 Sikkim, India -Nepal Border 18-09-2011 13 6.8 9  
 Bahadurgarh, India 05-03-2012 19 4.9 21  
 Chamoli, India 29-11-2015 10 4.0 14  
4. Result
Metrics includes percentage mean absolute error (MAE), root mean squared error (RMSE), and improvement, and a down arrow 
↓ is used . The percentage improvement of our model over another model in terms of MAE is given by: Percent Improvement = 
MAEother−MAEours
MAEother
× 100%. Down (↓) arrows are included next to each performance metric to indicate that lower values are better.
4.1. Ablation study and parameter analysis
In this paper, ablation study and parameter analysis refer to systematically removing or modifying model units and changing 
hyperparameters. Selecting the right parameters is essential for building an optimal ESN. The layer configuration and corresponding 
units yielding the lowest error are discussed in detail in Supplementary Section 2.1 as the optimal setup for the proposed model. 
Table  3 presents the ablation study performed by replacing and adding different units to identify the best-performing configuration. 
The improvement in model performance based on MAE is 8.0%↓, 9.4%↓, 8.1%↓, 6.8%↓, and 8.8%↓ compared to the model when 
a fully connected neural network (FCNN) is replaced with DENN for the 2 to 6SE dataset. The ablation study shows that the ESN 
network with DENN performs better than the FCNN-based reservoir readout. Thus, justifying the selection of DENN in the EarthESND 
framework. The DENN’s efficacy is further demonstrated by replacing it with ridge or linear regression. For the 2SE dataset, the error 
for ridge regression reservoir readout is approximately 22.5%↓, 23.9%↓, 22.7%↓, 23.6%↓, and 23.6%↓ higher than the EarthESND 
model for 2 to 6SE dataset. While using linear regression as the output layer results in an error about 21.6%↓, 24.7%↓, 22.7%↓, 
Computers and Electrical Engineering 135 (2026) 111161 
7

## Page 8

A. Joshi et al.
Table 3
Ablation study to evaluate the individual contribution of each architectural component to the overall system performance on test data of Japan.
 Method 2SE 3SE 4SE 5SE 6SE
 MAE(↓) RMSE(↓) MAE(↓) RMSE(↓) MAE(↓) RMSE(↓) MAE(↓) RMSE(↓) MAE(↓) RMSE(↓) 
 Single ESN Layer DENN 0.81 0.96 0.80 0.95 0.80 0.97 0.79 0.95 0.77 0.91  
 Single ESN Layer FCNN 0.84 0.99 0.84 0.91 0.82 0.90 0.81 0.91 0.78 0.89  
 Multiscale Single Layer reservoir + DENN 0.87 1.16 0.86 1.15 0.86 1.14 0.84 1.09 0.82 1.08  
 Multiscale Single Layer reservoir + FCNN 0.88 1.13 0.88 1.10 0.86 1.04 0.83 0.98 0.81 0.94  
 Deep ESN (2 stack) + FCNN 1.21 1.53 1.19 1.50 1.18 1.45 1.15 1.40 1.12 1.38  
 Deep ESN (3 stack) + FCNN 0.91 1.24 0.90 1.21 0.91 1.23 0.90 1.19 0.90 1.21  
 Deep ESN (4 stack) + FCNN 0.97 1.28 0.95 1.22 0.94 1.20 0.92 1.12 0.90 1.11  
 Deep ESN (8 stack) + FCNN 0.92 1.02 0.90 1.01 0.89 0.99 0.90 0.98 0.97 1.01  
 Deep ESN (2 stack) + DENN 1.02 1.42 1.02 1.40 1.00 1.38 0.99 1.35 0.99 1.32  
 Deep ESN (3 stack) + DENN 0.87 0.99 0.87 0.98 0.87 0.99 0.88 1.00 0.89 1.03  
 Deep ESN (4 stack) + DENN 0.96 1.25 0.94 1.20 0.94 1.12 0.92 1.08 0.91 1.05  
 Deep ESN (8 stack) + DENN 0.92 1.12 0.93 1.10 0.92 1.08 0.91 1.05 0.92 0.99  
 EarthESND with FCNN 0.75 0.98 0.74 0.97 0.74 0.98 0.73 0.96 0.74 0.92  
 Ridge Regression at output layer 0.89 1.12 0.88 1.11 0.88 1.10 0.89 1.14 0.89 1.14  
 Linear regression at output layer 0.88 1.11 0.89 1.13 0.88 1.12 0.87 1.08 0.87 1.06  
 Removed Tabular Input 0.90 1.25 0.91 1.26 0.89 1.21 0.89 1.22 0.88 1.19  
 RNN network with DENN 0.92 1.22 0.92 1.23 0.91 1.21 0.89 1.19 0.89 1.20  
 RNN network with FCNN 0.91 1.27 0.91 1.26 0.92 1.27 0.90 1.18 0.90 1.21  
 LSTM network with DENN 0.88 1.16 0.90 1.21 0.90 1.19 0.88 1.18 0.87 1.14  
 LSTM network with FCNN 0.92 1.21 0.91 1..22 0.90 1.19 0.90 1.21 0.89 1.18  
 Only 𝐗𝑖 = {𝑁𝑆 , 𝐸𝑊 , 𝑈 𝐷} 0.85 1.14 0.85 1.12 0.85 1.14 0.84 1.12 0.83 1.12  
 Only 𝐗𝑖 = {𝑁𝑆 , 𝐸𝑊 , 𝑈 𝐷} 0.83 1.19 0.84 1.21 0.84 1.20 0.85 1.23 0.82 1.16  
 Only 𝐗𝑖 = {𝑁𝑆 , 𝐸𝑊 , 𝑈 𝐷} 0.80 1.09 0.82 1.13 0.80 1.10 0.80 1.11 0.82 1.16  
 CTGAN-NN 0.78 0.97 0.79 0.99 0.79 0.98 0.77 0.96 0.77 0.97  
 CTGAN-Conv 0.83 1.25 0.83 1.21 0.82 1.19 0.82 1.18 0.81 1.17  
 ML Block: RF and XGB 0.78 0.96 0.78 0.97 0.77 0.96 0.77 0.95 0.76 0.94  
 ML Block: XGB and LGBM 0.76 0.94 0.76 0.93 0.75 0.94 0.74 0.93 0.74 0.92  
 ML Block: CatB, RF, and XGB 0.72 0.92 0.72 0.93 0.71 0.92 0.71 0.92 0.72 0.93  
 Only ML Block ({𝑇 𝑎𝑏𝑎𝑢𝑔 |𝑦𝑎𝑢𝑔 }) 0.98 1.28 0.97 1.26 0.97 1.27 0.96 1.26 0.96 1.27  
 Only ML Block ({𝑇 𝑎𝑏𝑠𝑦𝑛|𝑦𝑠𝑦𝑛}) 1.05 1.34 1.05 1.35 1.01 1.30 1.02 1.31 0.98 1.28  
 Only ML Block ({𝑇 𝑎𝑏𝑎𝑐𝑡 |𝑦𝑎𝑐𝑡 }) 1.03 1.37 1.03 1.35 0.99 1.30 0.98 1.30 0.96 1.25  
 Vanilla ESN 0.89 1.15 0.88 1.10 0.86 1.09 0.86 1.02 0.86 1.01  
 Deep ESN + Linear 0.84 1.03 0.83 0.98 0.83 0.98 0.81 0.97 0.81 0.97  
 Deep ESN + DENN 0.78 0.96 0.76 0.97 0.76 0.96 0.75 0.97 0.75 0.97  
 Deep Multiscale ESN+ DENN 0.74 0.96 0.73 0.96 0.73 0.95 0.74 0.96 0.72 0.95  
 Deep ESN + DENN+ Multiscale reservoir+ ML 
Block + DENN-CTGAN (Proposed)
0.69 0.86 0.67 0.84 0.68 0.86 0.68 0.85 0.68 0.85  
21.8%↓, and 21.8%↓ higher than proposed network for 2 to 6SE dataset. Thus, demonstrating the efficacy of the DENN model over 
regression-based reservoir readout, as shown in Table  3. Similarly, the EarthESND model is compared with sequence-to-sequence 
learning models using simple RNNs and LSTMs. As shown in Table  3, the ESN-based model with layering and scaling outperforms 
the simpler RNN and LSTM approaches.
Fig.  3 represents the actual and predicted magnitude using early (a) 2, (b) 3, (c) 4, (d) 5, and (e) 6 s of P waveform. Fig. 
3 represents the error (predicted-actual) obtained with respect to epicenter distance for (f) 2, (g) 3, (h) 4, (i) 5, and (j) 6 s of 
P waveform. It can be visualized from Fig.  3 (f-j) that the nearby epicenter distance gives more error due to the collapsing of 
the P waveform on the S waveform. Therefore, more energy information is released in the P waveform [1]. The error increases 
with increasing epicentral distance because seismic waves lose more energy at greater epicentral distances. This energy reduction 
reduces the clarity of the waveform features related to the earthquake source [41]. Thus, the epicenter distance affects the model’s 
magnitude-prediction error. One major limitation of EEW parameter prediction is the data skewness toward moderate to low 
magnitude events (less than 5 𝑀𝐽 𝑀𝐴).
4.2. State-of-the-art comparison
In this study, all the previous state-of-the-art deep learning frameworks for timeseries were retrained using the same training, 
testing, and validation datasets as the proposed model to ensure a fair and consistent comparison. Thus, the predicted magnitude is 
in the 𝑀𝐽 𝑀𝐴 scale. Table  4 represents the quantitative analysis of the MAE and RMSE for comparison of EarthESND performance 
with other state-of-the-art methods. All models were tuned using the same protocol, with mean squared error (MSE) as the validation 
metric and a fixed training budget of 50 epochs. The final hyperparameters are listed in Supplementary Table 12 and 13. It can be 
seen from Table  4 that the EarthESND model outperforms other state-of-the-art methods in terms of MAE and RMSE for 3SE to 6SE 
dataset. However, for 2SE and 3SE, the DFTQuake [1] performs better then the proposed method. However, the training time of 
Computers and Electrical Engineering 135 (2026) 111161 
8

## Page 9

A. Joshi et al.
Fig. 3. Actual and predicted magnitudes from the EarthESND model using (a) 2, (b) 3, (c) 4, (d) 5, and (e) 6 s of P-wave data. The red line 
indicates the ideal 1:1 relation. Prediction errors (predicted - actual) versus epicentral distance (km) for (f) 2, (g) 3, (h) 4, (i) 5, and (j) 6 s inputs 
are also shown; the green line represents zero error.
Table 4
Comparison of state-of-the-art ESN frameworks, deep learning methods for early earthquake magnitude prediction, and recent time series 
forecasting transformer frameworks on test data of Japan. The boldface represents the least error. Metrics are in 𝑀𝐽 𝑀𝐴.
 Method 2SE 3SE 4SE 5SE 6SE
 MAE(↓) RMSE(↓) MAE(↓) RMSE(↓) MAE(↓) RMSE(↓) MAE(↓) RMSE(↓) MAE(↓) RMSE(↓) 
 LSCross-ESN [35] 0.99 1.15 0.99 1.15 0.99 1.15 0.98 1.12 0.96 1.10  
 LS-ESN [34] 1.01 1.21 0.99 1.18 0.98 1.02 0.97 1.11 0.97 1.08  
 Inter-ESN [36] 0.96 1.21 0.95 1.20 0.94 1.18 0.94 1.15 0.92 1.12  
 𝜙-ESN [28] 0.96 1.14 0.95 1.11 0.94 1.12 0.93 1.11 0.92 1.08  
 Vanilla ESN [26] 1.21 1.15 1.08 1.10 1.08 1.08 1.02 1.12 1.02 1.02  
 Deep ESN [29] 0.84 1.03 0.83 0.98 0.83 0.98 0.81 0.97 0.81 0.97  
 Ensemble ESN [32] 1.08 1.39 1.04 1.32 1.01 1.28 0.99 1.25 0.99 1.20  
 edRVFl [65] 0.94 1.08 0.95 1.06 0.91 1.05 0.90 1.03 0.91 1.02  
 edESN [66] 1.11 1.42 1.02 1.31 0.99 1.21 0.97 1.17 0.98 1.13  
 SNRNN [9] 1.12 1.27 1.19 1.34 1.13 1.28 1.02 1.18 1.01 1.04  
 ViT magnitude [5] 0.70 0.86 0.71 0.87 0.75 0.95 0.73 0.91 0.91 1.15  
 CRNN [17] 0.90 1.11 0.99 1.24 0.80 0.99 0.79 0.98 1.02 1.18  
 EEWNet [2] 0.90 1.07 1.01 1.18 1.02 1.18 0.81 0.98 0.99 1.15  
 CREIME [16] 0.65 0.82 0.74 0.91 0.71 0.89 0.78 0.95 0.97 1.14  
 MFTnet [18] 0.84 1.04 0.88 1.16 0.94 1.13 1.11 1.37 1.06 1.37  
 DNN regression [7] 1.43 3.54 1.71 3.01 1.59 3.41 1.56 3.21 2.01 4.35  
 MagNet [4] 0.77 0.95 0.83 1.01 0.88 1.07 0.96 1.15 0.99 1.15  
 DFTQuake [1] 0.65 0.78 0.64 0.82 0.72 0.88 0.71 0.89 0.70 0.87  
 MagPred [41] 0.88 0.98 0.87 0.95 0.92 1.03 0.94 1.05 0.92 1.08  
 Flowformer [25] 0.80 1.03 0.80 1.01 0.79 1.02 0.79 0.98 0.78 0.98  
 Reformer [24] 0.91 1.11 0.93 1.09 0.92 1.07 0.91 1.02 0.90 1.01  
 iTransformer [6] 1.23 1.56 1.19 1.46 1.10 1.32 1.08 1.21 1.09 1.12  
 Proposed method 0.69 0.86 0.67 0.84 0.68 0.86 0.68 0.85 0.68 0.85  
DFTQuake [1] is almost 8.5 times higher than the proposed method as shown in Table  5. The second-best-performing model across 
five cases is the vision transformer model by Saad et al. (2024) [62]. However, the training time per epoch of the model by Saad 
et al. (2024) [62] is 23.47, 22.67, 23.56, 40.75, and 52.86 s, as shown in Table  5 due to the advanced network structure used by 
the model. Recently, deep random vector functional link (RVFL) neural networks have been widely applied to various tasks due to 
their simplicity and strong performance across different domains [63,64]. Therefore, in this study, we include the ensemble deep 
RVFL (edRVFL) [65] framework for comparison alongside ESN, as reported in Table  4.
The best time, shown by boldface, is obtained from the [7] method as shown in Table  5. The network by [7] utilizes a few layers 
of dense network only for prediction, which is also present as a DENN layer in the EarthESND model at the last layer. The reason for 
this increase in time is that the overhead of reservoir learning is present in the EarthESND network, which results in an increase in 
training time per epoch compared to the [7] method. The second-best time is obtained from the proposed model. It can be observed 
that for the [7] model, the training time per unit error is approximately 2.00, 2.49, 3.19, 2.61, and 2.64 s across the 2SE, 3SE, 
4SE, 5SE, and 5SE datasets. In comparison, the EarthESND model achieves a much lower MAE of 0.78, 0.76, 0.77, 0.75, and 0.76 
Computers and Electrical Engineering 135 (2026) 111161 
9

## Page 10

A. Joshi et al.
Table 5
The time (↓) in seconds taken per epoch for model training. The best timing is presented by a boldface.
 Method 2SE 3SE 4SE 5SE 6SE
 LSCross-ESN [35] 156.18 163.28 179.98 189.23 200.32 
 LS-ESN [34] 12.88 13.54 14.76 15.64 16.48  
 Inter-ESN [36] 40.13 49.94 55.90 50.68 65.15  
 𝜙-ESN [28] 5.46 7.53 7.89 8.43 10.64  
 Vanilla ESN [26] 11.23 16.45 15.28 18.78 21.84  
 Deep ESN [29] 22.41 25.45 29.64 31.16 34.87  
 Ensemble ESN [32] 20.61 26.21 32.75 36.86 33.12  
 edRVFl [65] 10.64 22.73 28.12 32.83 37.26  
 edESN [66] 24.32 29.56 32.64 36.32 39.16  
 SNRNN [9] 225.98 342.71 453.61 544.41 643.15 
 ViT magnitude [5] 23.47 22.67 23.56 40.75 52.86  
 CRNN [17] 24.79 30.86 25.90 39.07 45.23  
 EEWNet [2] 80.35 90.77 98.14 107.73 121.34 
 CREIME [16] 13.78 14.05 15.25 21.58 34.24  
 MFTnet [18] 25.49 21.39 21.01 42.79 45.98  
 DNN regression [7] 4.74 5.92 5.34 5.16 6.86  
 MagNet [4] 10.68 11.62 14.62 16.84 18.43  
 DFTQuake [1] 67.44 74.65 82.69 89.90 94.12  
 MagPred [41] 6.53 7.13 7.27 8.85 9.02  
 Flowformer [25] 31.09 30.42 32.77 32.48 33.34  
 Autoformer [22] 256.23 267.84 487.74 534.56 611.74 
 iTransformer [6] 25.98 29.76 30.43 33.88 34.87  
 Reformer [24] 32.41 36.88 42.65 46.89 50.21  
 Proposed method 7.80 6.71 10.55 9.32 10.99  
𝑀𝐽 𝑀𝐴 with comparable training times of 3.27, 6.72, 5.59, 8.19, and 7.04 s for respective datasets as shown in Table  5. This error 
demonstrates the ability of EarthESND to deliver significantly higher performance without a substantial increase in training time.
The higher errors in the other models are due to the removal of the epicenter distance limit in the current study, which 
introduces outliers that the previous methods are unable to handle effectively. Supplementary Figure 2 shows a flowchart illustrating 
the differences between regression-based, deep learning (CNN [4,16], RNN [9,17], Transformer [5,18]), and reservoir computing 
network proposed in this work in EEWS. For transparency and reproducibility, a comprehensive summary of all model-specific 
hyperparameters is provided in the Supplementary Table 11, 12, and 13. Supplementary Table 7 summarizes the model’s single 
sample inference latency in milliseconds. We have added the number of learnable parameters for the state-of-the-art early magnitude 
prediction models in Supplementary Table 8, as learnable parameters directly contribute to the computational cost required during 
inference.
In addition to these models, we also evaluated the proposed method against widely used regression relationships in EEWS, 
discussed in detail in Supplementary Section 2.7, Table 9. The regression relations are designed considering the output in moment 
magnitude 𝑀𝑤 scale as discussed in Supplementary Section 2.7, Eq. (8). These regression-based approaches are compared with the 
EarthESND model as described by the mathematical formula in Supplementary Table 9. The cumulative absolute absement (𝐶𝐴𝐴) 
parameter was used by Lin and Wu (2025) [3] and Wu et al. (2023) [67]. For the 6-second duration, the same equations used for 
the 5-second P-wave were adopted from Kumar et al. (2020) [68], Wu et al. (2023) [67], and Lin and Wu (2025) [3] due to the 
unavailability of specific 6-second P-wave equations. Similarly, for the 2SE dataset in Kumar et al. (2020) [68], the equations for 
the 3-second P-wave were used because no dedicated 2-second P-wave equations were available. Table  6 represents the quantitative 
analysis of the state-of-the-art regression relations for EEW magnitude prediction on the 2SE, 3SE, 4SE, 5SE, and 6SE datasets. It 
can be seen that the proposed method outperforms the other regression relations. The recent regression relation given by Lin and 
Wu (2025) [3] and Wu et al. (2023) [67] gives more error compared to the proposed method. This is because they are designed 
using different magnitude range of 4.5 to 7.5 𝑀𝑤 and 5.0 to 8.5 𝑀𝑤 as shown in Supplementary Section 2.7, Table 9.
4.3. Multi-station and inter-region study
2024 noto earthquake. The great Noto earthquake occurred on January 1, 2024, with a magnitude of 7.6 𝑀𝐽 𝑀𝐴 in the Noto 
Peninsula. The area was severely affected, and the rescue operation was delayed [73]. The prior prediction of earthquake magnitude 
during an event will give lead time for rescuers to operate strategically. In this study, the approach was extended to multi-station 
magnitude prediction for the 2024 Noto earthquake, used as the test set with 232 records, as shown in Fig.  4. Fig.  4 represents 
the 2024 Noto event magnitude error with respect to epicenter distance using (a) 2, (b) 3, (c) 4, (d) 5, and (e) 6 s of P wave. 
Fig.  4 (f-j) represents the prediction error distribution with respect to epicenter distance as shown in the 2SE, 3SE, 4SE, 5SE, and 
6SE datasets. Fig.  4 (k-o) S wave arrival time distribution with respect to the prediction error of 2SE, 3SE, 4SE, 5SE, and 6SE 
datasets. The quantitative analysis, based on the MAE and RMSE of the Noto event using several state-of-the-art methods, is shown 
in Supplementary Section 2.8.
Computers and Electrical Engineering 135 (2026) 111161 
10

## Page 11

A. Joshi et al.
Table 6
Comparison of state-of-the-art regression relations for early earthquake magnitude prediction of the test dataset. The boldface values represent 
the least error. The results are in 𝑀𝑤.
 Parameter Reference Region 2SE 3SE 4SE 5SE 6SE
 MAE(↓) RMSE(↓) MAE(↓) RMSE(↓) MAE(↓) RMSE(↓) MAE(↓) RMSE(↓) MAE(↓) RMSE(↓) 
 𝜏𝑐 [69] Japan 1.06 1.26 1.18 1.44 1.01 1.26 1.01 1.26 0.99 1.15  
 𝜏𝑝 [70] USA 3.20 4.45 3.32 4.71 3.21 4.45 3.21 4.45 3.20 4.43  
 𝑃𝑑 [70] USA 3.76 3.89 3.46 3.60 3.76 3.89 3.76 3.89 3.78 3.89  
 𝜏𝑐 [71] Taiwan 0.81 1.02 0.89 1.11 0.80 1.02 0.80 1.02 1.01 1.26  
 𝜏𝑐 [68] India 4.87 5.12 5.34 5.60 4.87 5.12 4.74 5.11 4.87 5.12  
 𝑃𝑑 [68] India 0.91 1.14 0.81 1.01 0.91 1.14 0.90 1.12 0.91 1.14  
 𝜏𝑐 [72] Japan, Taiwan, Italy 1.34 1.60 1.59 1.87 1.34 1.61 1.24 1.51 1.34 1.61  
 𝜏𝑐 [50] Japan 1.43 1.69 1.71 1.99 1.43 1.69 1.23 1.48 1.18 1.32  
 CAA [67] Japan 4.41 4.52 4.63 4.77 4.85 4.91 4.99 5.07 4.56 4.98  
 𝑃𝑑 [67] Japan 1.10 1.36 1.15 1.42 1.10 1.36 1.10 1.36 0.99 1.21  
 CAA [3] Japan 4.51 5.69 4.54 5.32 4.51 5.68 4.21 5.67 4.12 5.23  
 𝑃𝑑 [3] Japan 3.21 4.65 3.93 4.57 3.43 4.21 3.54 4.12 3.12 3.87  
 Proposed method Japan 0.55 0.68 0.53 0.67 0.54 0.67 0.54 0.67 0.54 0.67  
Fig. 4. The station-based contour maps of predicted magnitudes from the proposed model for the 7.6 𝑀𝐽 𝑀𝐴 2024 Noto event are shown for (a) 
2 s, (b) 3 s, (c) 4 s, (d) 5 s, and (e) 6 s of P-wave data. Red star and cyan triangle denote the epicenter and station locations. The corresponding 
prediction errors (predicted - actual) with respect to epicentral distance are shown for (f) 2 s, (g) 3 s, (h) 4 s, (i) 5 s, and (j) 6 s of P-wave data. 
Similarly, the prediction errors (predicted - actual) with respect to time advantage before S-wave arrival are presented for (k) 2 s, (l) 3 s, (m) 
4 s, (n) 5 s, and (o) 6 s of P-wave data. Plot (k–o) also includes the time magnitude density plot of EarthESND predictions for the 2024 Noto 
event. The red line shows the smoothed predicted magnitude, the red dashed line shows ±0.4 Mw uncertainty bounds, and the blue dashed line 
marks the true 𝑀𝐽 𝑀𝐴 magnitude. 232 records of 2024 Noto events are selected for this study.
Inter region study: India. Cross-region testing was conducted on the Indian dataset to assess the model’s performance on inter-regional 
data. The MAE of 1.00, 0.97, 1.21, 1.24, and 1.11 𝑀𝑤 have been obtained from the 2, 3, 4, 5, and 6 s of P wave of the Indian 
dataset. The RMSE values of 1.13, 1.13, 1.32, 1.35, and 1.27 𝑀𝑤 were obtained from the 2, 3, 4, 5, and 6 s of the P wave in the 
Indian dataset, which comprised 157 records. Fig.  5 (a-e) represents the actual and predicted magnitude of the five datasets. The 
Fig.  5 (f-j) represents the error distribution with respect to epicenter distance (km) for five datasets. The high prediction error in 
the Indian region results from training the model in a region of Japan with different geography and testing it in another area.
5. Conclusion
The proposed work develops a framework that utilizes ESN to predict the onsite EEW magnitude. The proposed framework 
is scalable due to its significantly lower training time compared to advance deep learning models, and multiscale as it captures 
dynamics across multiple temporal scales within the ESN reservoir. The ablation study and parameter analysis comprehensively 
validate the performance of the EarthESND model compared to its variants. The proposed method shows better performance with 
respect to recent deep learning networks that additionally require longer training time, as shown in Table  4. Moreover, It can 
Computers and Electrical Engineering 135 (2026) 111161 
11

## Page 12

A. Joshi et al.
Fig. 5. The station-based contour maps of predicted magnitudes from the proposed model for the India earthquake are shown for (a) 2 s, (b) 
3 s, (c) 4 s, (d) 5 s, and (e) 6 s of P-wave data. The corresponding prediction errors (predicted - actual) with respect to epicentral distance (km) 
are shown for (f) 2 s, (g) 3 s, (h) 4 s, (i) 5 s, and (j) 6 s of P-wave data. The dataset consists of 157 records of 12 earthquakes.
be observed from Table  6 that the proposed EarthESND network outperforms the recently and widely used regression relations 
for earthquake prediction. The research findings of this study establish an advanced EEW framework that relies on high-end 
computational systems for magnitude prediction. The geoscience and computer science communities can apply the proposed model 
to identify and monitor severely impacted regions during an earthquake, thereby helping reduce potential damage and losses at 
low computational cost. Future work can evaluate the model’s robustness under low-SNR conditions to assess stability in noisy 
environments and can further explore the EEW magnitude detection using broadband sensors. Another future direction is the 
development of a framework for identifying noise in earthquake signals, which may also support more reliable P-wave onset 
detection.
Declaration of competing interest
The authors declare that they have no known competing financial interests or personal relationships that could have appeared 
to influence the work reported in this paper.
Appendix A. Supplementary data
Supplementary material related to this article can be found online at https://doi.org/10.1016/j.compeleceng.2026.111161.
Data and Code Availability
The source codes are available for download at the link: https://github.com/anushka-joshi/EarthESND-Model. Event datasets 
were curated from Japan’s Kyoshin Net (K-NET) mained by National Research Institute for Earth Science and Disaster Resilience 
(NIED) [59] and India’s PESMOS that is a project run by department of earthquake engineering, Indian Institute of Technology 
Roorkee, Roorkee (https://pesmos.org). We thank the data providers for public access.
References
[1] Joshi A, Vedium NR, Raman B. DFTQuake: Tripartite Fourier attention and dendrite network for real-time early prediction of earthquake magnitude and 
peak ground acceleration. Eng Appl Artif Intell 2025;144:110077.
[2] Wang Y, Li X, Wang Z, Liu J. Deep learning for magnitude prediction in earthquake early warning. Gondwana Res 2023;123:164–73.
[3] Lin YH, Wu YM. Magnitude determination for earthquake early warning using P-alert low-cost sensors during 2024 Mw7.4 Hualien, Taiwan earthquake. 
Sci Rep 2025;15.
[4] Mousavi SM, Beroza GC. A machine-learning approach for earthquake magnitude estimation. Geophys Res Lett 2019;47.
[5] Saad OM, Chen Y, Savvaidis A, Fomel S, Zhang Y. Real-time earthquake detection and magnitude estimation using vision transformer. J Geophys Res 
Solid Earth 2022;127.
[6] Liu Y, Hu T, Zhang H, Wu H, Wang S, Ma L, Long M. iTransformer: Inverted transformers are effective for time series forecasting. In: The twelfth 
international conference on learning representations. 2024, p. 1–24.
[7] Apriani M, Wijaya SK, Daryono. Earthquake magnitude estimation based on machine learning: Application to earthquake early warning system. J Phys 
Conf Ser 2021;1951:012057.
[8] Krizhevsky A, Sutskever I, Hinton GE. ImageNet classification with deep convolutional neural networks. Commun ACM 2012;60:84–90.
[9] Bilal MA, Wang Y, Ji Y, Akhter MP, Liu H. Earthquake detection using stacked normalized recurrent neural network (SNRNN). Appl Sci 2023;13(14):8121.
[10] Sherstinsky A. Fundamentals of recurrent neural network (RNN) and long short-term memory (LSTM) network. 2018, arXiv, arXiv:1808.03314.
Computers and Electrical Engineering 135 (2026) 111161 
12

## Page 13

A. Joshi et al.
[11] Rumelhart DE, McClelland JL. Learning internal representations by error propagation. Parallel Distrib Process: Explor Microstruct Cogn: Found IEEE 
1987;318–62.
[12] Kenji D. Bifurcations in the learning of recurrent neural networks. [Proceedings] 1992 IEEE Int Symp Circuits Syst 1992;6:2777–80 vol.6.
[13] Devi RD, Govindarajan P, Venkatanathan N. Towards real-time earthquake forecasting in Chile: Integrating intelligent technologies and machine learning. 
Comput Electr Eng 2024;117:109285.
[14] Sun C, Song M, Cai D, Zhang BF, linda Qiao, Li H. A systematic review of echo state networks from design to application. IEEE Trans Artif Intell 
2022;5:23–37.
[15] Wu X, Liu X, Li W, Wu Q. Improved expressivity through dendritic neural networks. In: Bengio S, Wallach H, Larochelle H, Grauman K, Bianchi NC, 
Garnett R, editors. In: NeurIPS, vol. 31, Curran Associates, Inc.; 2018, p. 8068–79.
[16] Chakraborty M, Fenner D, Li W, Faber J, Zhou K, Ruempker G, Stoecker H, Srivastava N. CREIME a convolutional recurrent model for earthquake 
identification and magnitude estimation. J Geophys Res: Solid Earth 2022;127.
[17] Yoon D, Li Y, Ku B, Ko H. Estimation of magnitude and epicentral distance from seismic waves using deeper CRNN. IEEE Geosci Remote Sens Lett 
2023;20:1–5.
[18] Ge K, Wang C, Guo Y, Tang Y, Fan J-S. A multitask Fourier transformer network for seismic source characterization estimation from a single-station 
waveform. IEEE Geosci Remote Sens Lett 2024;21:1–5.
[19] Mcbride SK, Bostrom A, Sutton JN, de Groot RM, Baltay AS, Terbush B, Bodin P, Dixon M, Holland E, Arba R, Laustsen P, Liu S, Vinci M. Developing 
post-alert messaging for ShakeAlert, the earthquake early warning system for the West Coast of the United States of America. Int J Disaster Risk Reduct 
2020.
[20] Galley IJ, Leonard G, Johnston DM, Balm R, Paton D. The Ruapehu lahar emergency response plan development process: An analysis. Australas J Disaster 
Trauma Stud 2004;1.
[21] Mousavi SM, Zhu W, Sheng Y, Beroza GC. CRED: A deep residual network of convolutional and recurrent units for earthquake signal detection. Sci Rep 
2018;9.
[22] Wu H, Xu J, Wang J, Long M. Autoformer: Decomposition transformers with auto-correlation for long-term series forecasting. In: NeuralIPS, vol. 1717, 
2021, p. 22419–30.
[23] Zeng A, Chen M-H, Zhang L, Xu Q. Are transformers effective for time series forecasting? In: AAAI conference on artificial intelligence. 2022, p. 11121–8.
[24] Kitaev N, Kaiser L, Levskaya A. Reformer: The efficient transformer. Int Conf Learn Represent 2020.
[25] Huang Z, Shi X, Zhang C, Wang Q, Cheung KC, Qin H, Dai J, Li H. FlowFormer: A transformer architecture for optical flow. In: European conference on 
computer vision. 2022, p. 668–85.
[26] Jaeger H. The ‘‘echo state’’ approach to analysing and training recurrent neural networks. GMD Tech Rep 2001;148:1–47.
[27] Yildiz IB, Jaeger H, Kiebel SJ. Re-visiting the echo state property. Neural Networks : Off J Int Neural Netw Soc 2012;35:1–9.
[28] Gallicchio C, Micheli A. Architectural and Markovian factors of echo state networks. Neural Networks : Off J Int Neural Netw Soc 2011;24 5:440–56.
[29] Gallicchio C, Micheli A, Pedrelli L. Design of deep echo state networks. Neural Netw 2018;108:33–47.
[30] Gallicchio C, Micheli A. Richness of deep echo state network dynamics. In: International work-conference on artificial and natural neural networks, vol. 
11506, 2019, p. 480–91.
[31] Inoue S, Nobukawa S, Nishimura H, Watanabe E, Isokawa T. Multi-scale dynamics by adjusting the leaking rate to enhance the performance of deep echo 
state networks. Front Artif Intell 2024;7.
[32] Mallea M, Nebot À, Mugica F. Ensemble echo state networks trained collectively for reliable energy forecasting in facilities. Comput Electr Eng 
2026;129:110854.
[33] Schrauwen B, Defour J, Verstraeten D, Campenhout JMV. The introduction of time-scales in reservoir computing, applied to isolated digits recognition. 
In: International conference on artificial neural networks. 2007, p. 471–9.
[34] Zheng K, Qian B, Li S, Xiao Y, Zhuang W, Ma Q. Long-short term echo state network for time series prediction. IEEE Access 2020;8:91961–74.
[35] Jiang D, Cui L, Zeng Y, You M, Wang G. Long-short term cross echo state network for time series forecasting task. Appl Soft Comput 2025;174:112997.
[36] Liu J, Xu X, Li E. An echo state network with interacting reservoirs for modeling and analysis of nonlinear systems. Nonlinear Dynam 2024.
[37] London M, Häusser M. Dendritic computation. Annu Rev Neurosci 2005;28:503–32.
[38] Pagkalos M, Makarov R, Poirazi P. Leveraging dendritic properties to advance machine learning and neuro-inspired computing. Curr Opin Neurobiol 
2024;85:102853.
[39] Poirazi P, Mel BW. Impact of active dendrites and structural plasticity on the memory capacity of neural tissue. Neuron 2001;29:779–96.
[40] Xu L, Skoularidou M, Infante AC, Veeramachaneni K. Modeling tabular data using conditional GAN. In: NeuralIPS, vol. 659, 2019, p. 7335–45.
[41] Joshi A, Raman B, Mohan CK. Real-time earthquake magnitude prediction using designed machine learning ensemble trained on real and CTGAN generated 
synthetic data. Geod Geodyn 2025.
[42] Saad OM, Chen Y, Trugman DT, Soliman MS, Samy L, Savvaidis A, Khamis MA, Hafez AG, Fomel S, Chen Y. Machine learning for fast and reliable 
source-location estimation in earthquake early warning. IEEE Geosci Remote Sens Lett 2022;19:1–5.
[43] Rosenblatt F. The perceptron: a probabilistic model for information storage and organization in the brain. Psychol Rev 1958;65 6:386–408.
[44] Allen RV. Automatic earthquake recognition and timing from single traces. Bull Seismol Soc Am 1978;68(5):1521–32.
[45] Boore DM, Bommer JJ. Processing of strong-motion accelerograms: needs, options and consequences. Soil Dyn Earthq Eng 2005;25:93–115.
[46] Wu Y-M, Kanamori H, Allen RM, Hauksson E. Determination of earthquake early warning parameters, 𝜏 c and Pd, for southern California. Geophys J Int 
2007;170:711–7.
[47] Gallicchio C, Micheli A, Pedrelli L. Deep reservoir computing: A critical experimental analysis. Neurocomputing 2017;268:87–99.
[48] Joshi A, Singh P, Balasubramanian R. A deep attention model for onsite estimation of earthquake epicenter distance and magnitude. IEEE Trans Geosci 
Remote Sens 2024;62:1–11.
[49] Joshi A, Chalavadi V, Mohan K. Early detection of earthquake magnitude based on stacked ensemble model. J Asian Earth Sci: X 2022;8:100122–36.
[50] Zhu J, Li S, Song J, Wang Y. Magnitude estimation for earthquake early warning using a deep convolutional neural network. Front Earth Sci 2021;9:653226.
[51] Liu Y, Zhao Q, Wang Y. Peak ground acceleration prediction for on-site earthquake early warning with deep learning. Sci Rep 2024;14:5485.
[52] Hendrycks D, Gimpel K. Gaussian error linear units (GELUs). 2016, arXiv: Learning.
[53] Kingma DP, Ba J. Adam: A method for stochastic optimization. CoRR 2014. arXiv:1412.6980.
[54] Bishop CM. Information science and statistics. In: Grey wolf optimizer. Springer New York, NY; 2006, 
[55] Maaten L, Hinton G. Visualizing data using t-SNE. J Mach Learn Res 2008;9(86):2579–605.
[56] Chen T, Guestrin C. XGBoost: A scalable tree boosting system. Proc the 22nd ACM SIGKDD Int Conf Knowl Discov Data Min 2016;16:785–94.
[57] Ke G, Meng Q, Finley T, Wang T, Chen W, Ma W, Ye Q, Liu T-Y. LightGBM: A highly efficient gradient boosting decision tree. In: NeurIPS, vol. 17, 2017, 
p. 3149–57.
[58] Ostroumova L, Gusev G, Vorobev A, Dorogush AV, Gulin A. CatBoost: unbiased boosting with categorical features. In: NeurIPS, vol. 18, 2017, p. 6639–49.
[59] NIED. NIED K-NET, KiK-net, National Research Institute for Earth Science and Disaster Resilience. Natl Res Inst Earth Sci Disaster Resil 2019. 
http://dx.doi.org/10.17598/NIED.0004.
[60] Joshi A, Singh P, Balasubramanian R. IsoMapGen: Framework for early prediction of peak ground acceleration using tripartite feature extraction and gated 
attention model. Comput Geosci 2025;196:105849.
Computers and Electrical Engineering 135 (2026) 111161 
13

## Page 14

A. Joshi et al.
[61] Noda S, Ellsworth WL. Scaling relation between earthquake magnitude and the departure time from P wave similar growth. Geophys Res Lett 
2016;43:9053–60.
[62] Saad O, Helmy I, Mohammed M, Savvaidis A, Chatterjee A, Chen Y. Deep learning peak ground acceleration prediction using single-station waveforms. 
IEEE Trans Geosci Remote Sens 2024;62:1–13.
[63] Du L, Gao R, Suganthan PN, Wang DZW. Graph ensemble deep random vector functional link network for traffic forecasting. Appl Soft Comput 
2022;131:109809.
[64] Gao R, Hu M, Li R, Luo X, Suganthan PN, Tanveer M. Stacked ensemble deep random vector functional link network with residual learning for medium-scale 
time-series forecasting. IEEE Trans Neural Networks Learn Syst 2025;36:10833–43.
[65] Hu M, Chion JH, Suganthan PN, Katuwal R. Ensemble deep random vector functional link neural network for regression. IEEE Trans Syst Man, Cybern: 
Syst 2023;53:2604–15.
[66] Gao R, Li R, Hu M, Suganthan PN, Yuen KF. Dynamic ensemble deep echo state network for significant wave height forecasting. Appl Energy 2023.
[67] Wu YM, Mittal H, Lin YH, Chang YH. Magnitude determination using cumulative absolute absement for earthquake early warning. Geosci Lett 2023;10:1–7.
[68] Kumar S, Mittal H, Roy KS, Wu Y-M, Chaubey R, Singh AP. Development of earthquake early warning system for Kachchh, Gujarat, in India using 𝜏c and 
Pd. Arab J Geosci 2020;13.
[69] Wu Y-M, Kanamori H. Exploring the feasibility of on-site earthquake early warning using close-in records of the 2007 Noto Hanto earthquake. Earth, 
Planets Space 2008;60:155–60.
[70] Wurman G, Allen RM, Lombard PN. Toward earthquake early warning in northern California. J Geophys Res 2007;112.
[71] Wu Y-M, Yen H, Zhao L, Huang B-S, Liang W-T. Magnitude determination using initial P waves: A single-station approach. Geophys Res Lett 2006;33.
[72] Zollo A, Amoroso O, Lancieri M, Wu Y-M, Kanamori H. A threshold-based earthquake early warning using dense accelerometer networks. Geophys J Int 
2010;183:963–74.
[73] Suppasri A, Kitamura M, Alexander DE, Seto S, Imamura F. The 2024 Noto Peninsula earthquake: Preliminary observations and lessons to be learned. Int 
J Disaster Risk Reduct 2024.
Computers and Electrical Engineering 135 (2026) 111161 
14
