I’ll build this as an evidence map, not a paper-by-paper catalogue. I’ll first search the historical and modern method families, then extract study designs and evaluation practices, and finally search for counterexamples to each proposed gap. I’ll distinguish published findings, author claims, cross-paper inferences, and proposed experiments, and report any limits to coverage.The search has already ruled out several overly broad gap claims: morphology-preserving filtering, real-motion experiments, embedded implementations, and downstream-task evaluation all have precedents. I’m now checking the narrower questions—how well those results generalize across devices and patients, whether clinical morphology is preserved, and whether reported runtimes establish causal streaming operation.The counterexample search has narrowed the opportunity map further: retrieved work includes cross-dataset testing, unpaired real-noise training, multi-lead autoencoders, and uncertainty-aware diffusion. Those are not empty research areas. The stronger residual questions concern validation under realistic shifts and preservation of clinical information. One limitation is important: the final searches were still finding relevant studies when the session’s retrieval limit was reached, so I cannot honestly claim the requested search-saturation criterion was met.## 1. Executive synthesis

**The central research problem in ECG denoising is not simply removing noise. It is determining which information can be recovered, which clinically relevant information must remain unchanged, and when reconstruction should not be trusted.** Published studies show that these objectives are not interchangeable: filtering can alter ST segments; methods can differ in their preservation of individual landmarks despite similar aggregate performance; and denoising can worsen a downstream classifier even when reconstruction metrics improve. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5361052/?utm_source=openai))

**Scope and evidence status.** This is a structured, evidence-grounded **scoping survey and research-opportunity analysis**, with a literature cutoff of **September 24, 2026**. It is not a completed, database-exported systematic review or meta-analysis. The investigation progressed through broad discovery, terminology expansion, primary-study extraction, version normalization, taxonomy construction, counterexample searches, gap revision, and research-question formulation. Importantly, the final searches continued to identify relevant studies before the retrieval limit was reached; therefore, the requested search-saturation criterion was **not fully met**.

Four distinctions organize the review:

- **Demonstrated finding:** an outcome evaluated in a study’s actual experiment.
- **Author claim:** an interpretation, proposed application, or future direction that exceeds the directly measured endpoints.
- **Cross-paper inference:** a pattern inferred from the retrieved evidence.
- **Research proposal:** an experiment or question developed here, not an established result.

### Main conclusions

1. **The field is broader than a classical-versus-deep-learning comparison.** Its main methodological principles include frequency-selective filtering, reference-assisted cancellation, dynamical estimation, multiresolution shrinkage, adaptive decomposition, sparse representation, low-rank redundancy, learned regression, and generative restoration. Hybridization predates modern neural networks: wavelet–Wiener filtering and decomposition–thresholding combinations are established examples. ([researchportal.tuni.fi](https://researchportal.tuni.fi/fi/publications/ecg-signal-denoising-using-wavelet-domain-wiener-filtering?utm_source=openai))

2. **A major recurring experimental construction is real ECG plus separately recorded or simulated additive noise.** This is useful because it supplies a reference waveform, but it is not equivalent to observing naturally corrupted ECG during acquisition. NSTDB itself makes this distinction clear: its artifact recordings are real, while its standard noisy ECG records are constructed mixtures. ([archive.physionet.org](https://archive.physionet.org/physiobank/database/nstdb/?utm_source=openai))

3. **Neither morphology preservation nor downstream evaluation is an untouched topic.** Relevant precedents include ST-preservation studies, landmark-focused EMG suppression, embedded beat-detection evaluation, classification after self-supervised denoising, and recent frequency-guided models reporting diagnostic-task results. The residual problem is the breadth, independence, and clinical relevance of validation—not the absence of such work. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5361052/?utm_source=openai))

4. **Several apparent modern gaps have already been partially addressed.** Retrieved counterexamples include subject-disjoint cross-dataset testing, unpaired real-noise training, simultaneous multi-lead denoising, and uncertainty-aware diffusion. “Apply self-supervision,” “use multiple leads,” or “estimate uncertainty” is consequently insufficient as a novelty claim. ([doi.org](https://doi.org/10.1109/BIBM66473.2025.11356550?utm_source=openai))

5. **The most defensible opportunities are intersections:** clinical-feature preservation under domain shift; noisy-only learning under correlated artifacts; calibrated rejection of unreliable reconstructions; sensor-assisted denoising under realistic motion; and morphology-constrained streaming under measured resource limits. These are **synthesis-derived opportunities**, qualified below rather than asserted as empty fields.

---

## 2. Evolution of ECG denoising research

The development is better understood as accumulation of modeling assumptions than replacement of one generation by another.

| Period | Main development | What changed scientifically |
|---|---|---|
| Foundational filtering and adaptive processing | Frequency-selective filters, baseline tracking, reference cancellation, real-time ST-preserving designs | Established the trade-off between interference rejection, waveform distortion, and processing delay. A 1991 study already addressed baseline suppression with ST accuracy in real-time operation. ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/002207369190014D?utm_source=openai)) |
| 1990s–early 2000s | Wavelet and multiresolution processing; mathematical morphology; wavelet–Wiener combinations | Introduced scale-dependent and shape-dependent processing instead of relying solely on fixed frequency bands. High-resolution ECG and small-amplitude features were explicit motivations. ([pure.johnshopkins.edu](https://pure.johnshopkins.edu/en/publications/selective-noise-filtering-of-high-resolution-ecg-through-wavelet--3/?utm_source=openai)) |
| Mid-2000s–2010s | Nonlinear Bayesian filtering, EMD, sparse coding, nonlocal redundancy, matrix factorization | Shifted attention toward explicit cardiac models, adaptive signal decomposition, and structural redundancy. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/18075033/?utm_source=openai)) |
| Late 2010s–early 2020s | Recurrent denoisers, convolutional autoencoders, encoder–decoders, learned baseline filters, adversarial approaches | Learned noisy-to-reference mappings and latent representations became prominent, usually with constructed training pairs. ([arxiv.org](https://arxiv.org/abs/1807.11551?utm_source=openai)) |
| 2022–2024 | Conditional diffusion, broader hybrid models, joint generative/contrastive representations | Generative restoration and representation pretraining expanded the design space beyond deterministic regression. DeScoD-ECG appeared as a 2022 preprint and in its final journal volume in 2024; these are not independent methods. ([arxiv.org](https://arxiv.org/abs/2208.00542?utm_source=openai)) |
| 2025–retrieved 2026 literature | Noisy-only learning, unpaired adversarial training, model-unrolled sparse learning, multi-lead autoencoders, frequency-guided attention, uncertainty-aware sampling | Recent work increasingly targets training-data assumptions, spatial information, generalization, or efficiency—but often still evaluates only part of the intended clinical-use chain. ([ieeexplore.ieee.org](https://ieeexplore.ieee.org/document/10872955/?utm_source=openai)) |

**Interpretation:** classical methods remain relevant baselines because they encode useful assumptions with relatively transparent behavior. Architectural recency is not evidence of superiority under a different noise model, clinical task, or computational budget.

---

## 3. Comprehensive taxonomy

The taxonomy should be **multi-axis**. A method can simultaneously be adaptive, wavelet-domain, self-supervised, multi-lead, and streaming. Treating these labels as mutually exclusive categories obscures the actual scientific contribution.

### A. Noise and source characteristics

| Category | Normalized meaning | Important distinction |
|---|---|---|
| Baseline wander/drift | Slowly varying displacement associated with respiration, movement, and acquisition conditions | Overlaps with diagnostically relevant low-frequency content; suppression and ST preservation must be evaluated together. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5361052/?utm_source=openai)) |
| Power-line interference | Mains-frequency interference and potentially harmonics or time-varying amplitude | A stationary sinusoid is only one test condition; harmonic/baseline mixtures have also been studied. ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S0169260716305946?utm_source=openai)) |
| EMG/muscle artifact | Skeletal-muscle electrical contamination | Its spectrum overlaps ECG content, making simple frequency separation insufficient in general. ([archive.physionet.org](https://archive.physionet.org/physiotools/wag/wag.pdf?utm_source=openai)) |
| Electrode-motion artifact | Disturbance associated with mechanical changes at the electrode interface | Can resemble cardiac waveform components; must not be conflated with EMG. ([archive.physionet.org](https://archive.physionet.org/physiotools/wag/wag.pdf?utm_source=openai)) |
| Motion artifact | Umbrella acquisition condition rather than one uniquely defined process | May involve electrode movement, impedance changes, baseline shifts, and muscle activity. Auxiliary motion measurements need not be equally informative in every condition. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC8450177/?utm_source=openai)) |
| Instrumentation/environmental disturbance | Electronic interference and acquisition-system effects | Analog prevention, common-mode rejection, and digital correction are related but distinct interventions. ([ietresearch.onlinelibrary.wiley.com](https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/iet-cds.2019.0409?utm_source=openai)) |
| Mixed noise | Simultaneous or sequential combinations | Performance on separate noise classes does not establish robustness to their interactions. Existing studies explicitly investigate combined noise. ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S0169260716305946?utm_source=openai)) |
| Other physiological interference | An unwanted physiological source relative to a specified target | Maternal–fetal separation or removal of ECG from EMG changes the target-estimation problem and should not be pooled indiscriminately with adult surface-ECG denoising. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/18460766/?utm_source=openai)) |

**Terminology normalization:** in NSTDB, `bw` denotes baseline wander, `ma` muscle artifact, and `em` electrode-motion artifact. Across papers, “MA,” “EM,” and “EMG” are not consistently used; extraction should record the underlying source rather than trust the abbreviation. ([archive.physionet.org](https://archive.physionet.org/physiobank/database/html/about.htm?utm_source=openai))

### B–I. Methodological axes

| Axis | Hierarchical categories | Interpretation |
|---|---|---|
| **B. Denoising paradigm** | Deterministic filtering → FIR/IIR, notch, median/spline, mathematical morphology; statistical/model-based → Wiener, Kalman, Gaussian-process-type estimation; adaptive → LMS/NLMS/RLS; decomposition → wavelet, EMD-family, VMD/EWT; structural → sparse, dictionary, low-rank/matrix/tensor; learned → conventional ML, deep regression, generative restoration; hybrid/unrolled | Categorize by the assumption enabling separation, not by model acronym. Representative overlaps include wavelet–Wiener filtering and learned sparse optimization. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0010482502000343?utm_source=openai)) |
| **C. Representation** | Raw time series; Fourier/spectral; time–frequency; wavelet coefficients; learned latent; multiresolution; multi-lead spatial representation | The representation determines which structures are easy to preserve or suppress. Frequency-guided neural models and spectrogram factorization span several categories. ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S0169260716305946?utm_source=openai)) |
| **D. Learning regime** | Supervised; self-supervised; unpaired/unsupervised; weakly supervised; transfer; personalized; federated/distributed | “Autoencoder” does not imply unsupervised denoising. Clean-target reconstruction is supervised even if diagnostic labels are unused. Representation pretraining and waveform restoration must be distinguished. ([researchgate.net](https://www.researchgate.net/publication/333228342_Noise_Reduction_in_ECG_Signals_Using_Fully_Convolutional_Denoising_Autoencoders?utm_source=openai)) |
| **E. Target construction** | Clean/noisy pairs; synthetic corruption; measured-artifact mixtures; noisy-to-noisy; masking; consistency/cycle objectives; latent reconstruction; pseudo-clean targets; task-derived targets | Target provenance is often more consequential than architecture. Unpaired clean/noisy distributions are different from having no clean signals at all. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11422060/?utm_source=openai)) |
| **F. Temporal/context modeling** | Sample-local; beat-aligned; fixed window; long sequence; recurrent; convolutional; attention; multiscale; causal versus bidirectional | Context length and future dependence must be reported separately from processing speed. Beat aggregation can be useful without preserving every beat’s individual morphology. ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/002207369190014D?utm_source=openai)) |
| **G. Morphology strategy** | None stated; implicit waveform loss; explicit regional/derivative loss; landmark preservation; diagnostic-task loss; physiological constraints; morphology-aware post-processing | Mathematical morphology is a processing family, not proof of clinical morphology preservation. Explicit weighted losses and landmark-focused algorithms already exist. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0010482502000343?utm_source=openai)) |
| **H. Evaluation** | Signal similarity; regional morphology; landmark/interval error; beat detection; rhythm/diagnostic classification; reader interpretation; resource measurements | These are different validation levels, not interchangeable proxies. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5361052/?utm_source=openai)) |
| **I. Deployment** | Offline; blockwise online; causal streaming; wearable/mobile; embedded/edge; low-power; sensor-assisted acquisition | Report whether deployment was implemented, simulated, or merely proposed. Real embedded implementations exist; “no edge work” is not a defensible gap. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/23367417/?utm_source=openai)) |

### Normalization rules used in this review

- **Preprint and journal versions are grouped.** DeepFilter’s authors explicitly maintain separate repositories for preprint and revised journal experimental schemes; results from those versions should not be silently merged. ([github.com](https://github.com/fperdigon/DeepFilter?utm_source=openai))
- **Architectural variants are grouped by principle.** Adding attention, gates, or a different nonlinear block to an encoder–decoder does not automatically establish a new denoising paradigm.
- **“Real noise” is separated from “real noisy acquisition.”** A measured artifact added digitally to a reference ECG is classified here as **semi-synthetic contamination**.
- **Reconstruction, denoising, and source separation are distinguished.** Missing-lead reconstruction and ECG-image cleanup are adjacent tasks, not interchangeable evidence for waveform denoising. ([frontiersin.org](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2026.1827352/full?utm_source=openai))

---

## 4. Research-landscape matrix

Maturity labels below are **qualitative judgments from the retrieved evidence**, not bibliometric counts or rankings.

| Direction | Representative methodological families | Approximate literature maturity | Common datasets/noise | Common evaluation | Strengths | Recurrent limitations | Under-explored aspects |
|---|---|---|---|---|---|---|---|
| Baseline and mains suppression | FIR/IIR, notch, spline, median, morphology | Extensively studied | Simulated drift, recorded baseline, clinical ECG | Residual noise, distortion, sometimes ST error | Transparent; practical implementations | Frequency overlap; delay and phase behavior | Task-specific settings under changing acquisition conditions. ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/002207369190014D?utm_source=openai)) |
| Reference-assisted motion cancellation | LMS/NLMS/RLS; impedance/IMU references | Established but fragmented | Custom textile, ambulatory, capacitive recordings | Correlation, signal quality, beat detection | Uses information unavailable in ECG alone | Reference usefulness varies; additional sensing | Conditional benefit, reference failure, sensor synchronization. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC8450177/?utm_source=openai)) |
| Dynamical/model-based estimation | EKF/EKS/UKF and physiological models | Established but fragmented | Reference ECG with synthetic/recorded noise | SNR and morphology | Explicit prior and state interpretation | Dependence on model fit and cardiac-pattern assumptions | Safe adaptation to unusual morphology. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/18075033/?utm_source=openai)) |
| Wavelet/multiresolution | Thresholding, Wiener shrinkage, NLM hybrids | Extensively studied | Gaussian noise, EMG, baseline | SNR/RMSE/PRD; selected landmarks | Localized multiscale processing | Basis, scale, threshold and boundary choices | Common morphology-aware evaluation across configurations. ([researchportal.tuni.fi](https://researchportal.tuni.fi/fi/publications/ecg-signal-denoising-using-wavelet-domain-wiener-filtering?utm_source=openai)) |
| Adaptive decomposition | EMD/EEMD-family, VMD, EWT, decomposition hybrids | Established but fragmented | Simulated and measured-artifact mixtures | Mostly waveform metrics | Data-adaptive decomposition | Component selection and parameter dependence | Streaming behavior and independent real-noise comparisons. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0010482507001114?utm_source=openai)) |
| Sparse/low-rank optimization | Learned dictionaries, NMF, nuclear-norm methods | Moderately studied | Hospital/public ECG plus constructed corruption | Reconstruction metrics | Explicit structural assumptions; small-data possibilities | Rare morphology may not match learned structure | Matched-budget comparison with modern denoisers. ([spars2011.eng.ed.ac.uk](https://www.spars2011.eng.ed.ac.uk/sites/spars2011.eng.ed.ac.uk/files/attachments/basicpage/spars11.pdf?utm_source=openai)) |
| Discriminative neural denoising | CNN, RNN, DAE, U-Net, gated encoder–decoder | Extensively studied within constructed benchmarks | MIT-BIH/QT and added artifacts | SNR/RMSE/PRD/correlation | Flexible nonlinear mapping | Target construction and distribution dependence | External clinical and device validation. ([scholars.lib.ntu.edu.tw](https://scholars.lib.ntu.edu.tw/entities/publication/5ae56f43-3ade-47ba-9e8a-98dd993cc4a3?utm_source=openai)) |
| Attention/frequency-guided models | Convolution–transformer, multiscale attention | Emerging | Public ECG plus generated mixtures | Similarity and some diagnostic evaluation | Combines temporal and spectral modeling | Additional modules do not resolve target validity | Demonstrating benefits beyond capacity and tuning. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0952197626008511?utm_source=openai)) |
| Generative restoration | GAN/CycleGAN, conditional diffusion | Emerging | QT/NSTDB; increasingly unpaired wearable data | Distance metrics; some uncertainty analyses | Distribution modeling; alternative training objectives | Reconstruction plausibility is not patient-specific truth | Calibrated feature uncertainty and identity preservation. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11422060/?utm_source=openai)) |
| Noisy-only/representation learning | TP-informed self-supervision; generative/contrastive learning | Emerging | Tianchi, multi-lead unlabeled ECG | Reconstruction or downstream classification | Reduces some annotation requirements | Noise/physiology assumptions remain | Correlated-artifact identifiability and target leakage. ([researchgate.net](https://www.researchgate.net/publication/388711199_Self-Supervised_Electrocardiograph_De-noising?utm_source=openai)) |
| Multi-lead denoising | Spatial autoencoders, matrix/tensor redundancy | Established structural ideas; emerging neural variants | Multi-lead real/simulated ECG | MSE/SNR improvement | Exploits inter-lead redundancy | Aggregate metrics may miss lead-specific damage | Shared-electrode corruption and localized pathology. ([mdpi.com](https://www.mdpi.com/2624-6120/7/1/18?utm_source=openai)) |
| Embedded/streaming systems | DSP adaptive/ICA; FPGA filters and hybrids | Established but fragmented | Public-record replay and custom acquisition | Timing, resources, power, signal metrics | Demonstrated hardware feasibility | Different platforms and accounting conventions | Joint clinical-fidelity/latency/energy benchmarks. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/23367417/?utm_source=openai)) |

---

## 5. Major methodological directions

### 5.1 Deterministic filtering and mathematical morphology

**Principle:** remove components based on frequency, local shape, or estimated baseline.

Representative methods include FIR/IIR high-pass and low-pass filtering, notch filtering, median/spline baseline estimation, and morphological opening/closing. The 2002 study *ECG signal conditioning by morphological filtering* explicitly sought baseline correction and noise suppression with reduced distortion and computational burden. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0010482502000343?utm_source=openai))

Their value is not limited to serving as weak baselines. A large ischemic-ECG simulation found wavelet baseline cancellation most accurate among the tested methods, while judging Butterworth filtering attractive because of its computational cost and near-comparable accuracy. All evaluated methods altered ST content to some extent. **That finding is conditional on the simulated electrophysiology and baseline model.** ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5361052/?utm_source=openai))

**Current status:** mature methods, but parameter selection remains task-dependent. A detector-oriented filter and a diagnostic-display filter should not be assumed to have the same acceptable distortion.

### 5.2 Adaptive and sensor-assisted filtering

**Principle:** estimate contamination using a reference correlated with the artifact.

References include accelerometry, gyroscope signals, electrode impedance, and impedance pneumography. Relevant studies include a real-time DSP implementation of adaptive filtering/ICA, per-electrode IMU-assisted cancellation, and simultaneous ECG–impedance-pneumography acquisition. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/23367417/?utm_source=openai))

**Strength:** auxiliary measurements can help separate processes that overlap in the ECG spectrum.

**Limitation:** the presence of a motion sensor does not establish a useful artifact reference. The per-electrode IMU study reported variable performance and called for identifying conditions in which cancellation is beneficial. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC8450177/?utm_source=openai))

**Current status:** established, with renewed interest in non-contact and wearable acquisition. A retrieved 2026 non-contact study combines multi-reference NLMS, motion gating, and QRS-preserving mechanisms, further weakening claims that conditional adaptive cancellation is unexplored. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC13306560/?utm_source=openai))

### 5.3 Statistical, Bayesian, and physiology-informed estimation

**Principle:** use an explicit stochastic or dynamical model to estimate latent cardiac activity.

Sameni et al.’s 2007 framework integrated an ECG dynamical model with EKF, EKS, and UKF variants. Its experiments included artificially contaminated normal ECGs and real nonstationary muscle artifact, with SNR and morphology evaluation. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/18075033/?utm_source=openai))

**Strength:** assumptions can be inspected and manipulated, unlike an entirely implicit learned prior.

**Limitation—inference:** a prior that improves estimation for familiar morphology can also become a source of bias when the physiology changes. This is a hypothesis to test, not evidence that all model-based methods erase abnormalities.

**Current status:** physiology-informed denoising is not new. Recent neural formulations should be compared with older model-based estimators rather than presented as the first use of cardiac knowledge.

### 5.4 Wavelet, Wiener, and nonlocal methods

**Principle:** exploit separation across scales or similarity between local waveform neighborhoods.

Wavelet–Wiener filtering was studied around 2000; subsequent work combines wavelets with NLM and adaptive smoothing. These approaches connect deterministic transforms, statistical estimation, and data redundancy. ([researchportal.tuni.fi](https://researchportal.tuni.fi/fi/publications/ecg-signal-denoising-using-wavelet-domain-wiener-filtering?utm_source=openai))

The 2024 morphology-preserving EMG study is particularly informative because it compares performance at clinically relevant landmarks, including the region near the J point, rather than relying only on a whole-signal score. Its preferred method depends on noise severity and the feature of interest. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11100958/?utm_source=openai))

**Current status:** extensively studied, but not exhausted. Defensible contributions concern parameter robustness, specific morphology, real-time constraints, or reproducible comparisons—not simply another wavelet/threshold combination.

### 5.5 EMD-family and related decompositions

**Principle:** decompose a nonstationary signal into components, select or denoise components, and reconstruct.

The 2008 EMD study addressed both high-frequency contamination and baseline correction. Later methods combine decomposition with wavelet shrinkage or NLM; ESMD–NLM is one example evaluated using signal metrics and a mean-opinion-score measure. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0010482507001114?utm_source=openai))

**Strength:** decomposition adapts to the observed signal.

**Limitation—inference:** component adaptivity does not itself establish that a component is artifact rather than physiology. Component-selection sensitivity should therefore be treated as an experimental variable.

A **July 13, 2026 preprint**, marked accepted for WISEE 2026, compares EMD variants, DWT, an autoencoder, and a physics-informed network on real upper-arm acquisitions. It reports different winners for noise suppression and morphological reconstruction. Its preprint status and acquisition-specific design limit generalization. ([arxiv.org](https://arxiv.org/abs/2607.11450))

### 5.6 Sparse, dictionary, low-rank, and optimization-based methods

**Principle:** represent cardiac activity or noise using a restricted set of atoms, low-dimensional structure, or regularized solutions.

Dictionary learning was already applied to ECG denoising in 2011, including natural-noise examples. Low-rank NMF methods have addressed joint harmonic and baseline suppression, while more recent work combines weighted nuclear-norm denoising with compressed-signal reconstruction. ([spars2011.eng.ed.ac.uk](https://www.spars2011.eng.ed.ac.uk/sites/spars2011.eng.ed.ac.uk/files/attachments/basicpage/spars11.pdf?utm_source=openai))

The 2025 FISTA-Net study is a useful methodological extension: it learns noise dictionaries with K-SVD and unfolds sparse estimation into a model-driven network, rather than merely adding another generic neural block. It reports experiments on BUT QDB and provides code. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/41335795/?fc=None&ff=20251204130013&v=2.18.0.post22+67771e2&utm_source=openai))

**Current status:** moderately studied and still evolving. Compression/reconstruction papers should be separated from pure denoising comparisons because the measurement operator changes the task.

### 5.7 Supervised neural regression

**Principle:** learn a mapping from a corrupted waveform to a reference waveform or residual.

Representative families are recurrent networks, fully convolutional DAEs, U-Net-like models, gated autoencoders, and frequency-guided convolution–transformer hybrids. Chiang et al.’s FCN-DAE uses waveform reconstruction supervision; FGDAE adds gating and a multi-component loss; FGCT incorporates wavelet-derived frequency guidance. ([arxiv.org](https://arxiv.org/abs/1807.11551?utm_source=openai))

**Strength:** flexible mappings can accommodate complex mixtures.

**Limitations—inference:** model expressiveness does not resolve uncertainty about the training target, leakage, acquisition mismatch, or clinical sufficiency of the loss.

**Current status:** densely populated. An additional architecture on the same constructed dataset is a weak scientific contribution unless it tests a substantive assumption or delivers a validated deployment benefit.

### 5.8 Generative, self-supervised, and unpaired learning

These should not be collapsed into one category:

- **Conditional diffusion:** DeScoD-ECG learns from clean/noisy pairs and uses iterative stochastic reconstruction and multi-shot averaging. Its reported advantage concerns distance-based similarity metrics—not demonstrated diagnostic superiority. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11422060/?utm_source=openai))
- **Unpaired adversarial learning:** SC-CycleGAN uses separate clean and naturally noisy distributions, with spectrum consistency and attention. It is therefore a counterexample to the claim that all learned denoisers require paired synthetic corruption. ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S095219762600179X?utm_source=openai))
- **Noisy-only self-supervision:** Liu et al. estimate noise from TP intervals and train an autoencoder using simulated noise. Their pipeline also uses manually annotated examples to train TP segmentation; “self-supervised” does not mean that every component is annotation-free. ([researchgate.net](https://www.researchgate.net/publication/388711199_Self-Supervised_Electrocardiograph_De-noising?utm_source=openai))
- **Representation learning:** generative–contrastive pretraining has been used for both denoising and disease-detection tasks. Representation transfer is distinct from proving faithful restoration of every waveform feature. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S1746809424003112?utm_source=openai))

**Current status:** emerging, with meaningful precedents. The residual questions concern assumptions, identity preservation, and external validity.

### 5.9 Multi-lead and deployment-oriented methods

ML-CDAE directly exploits inter-lead information and reports better MSE/SNR improvement than its single-lead comparators. However, statements about improved diagnosis should be distinguished from those measured reconstruction endpoints. ([mdpi.com](https://www.mdpi.com/2624-6120/7/1/18?utm_source=openai))

Hardware work also has substantial precedents, from the 2012 DSP study to FPGA implementations of IIR and DWT–adaptive-threshold methods. A recent FPGA study reports latency, power, and logic utilization, which is stronger deployment evidence than parameter count alone. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/23367417/?utm_source=openai))

### 5.10 Condensed evidence-extraction ledger

**NR-E = not reliably extracted from the accessible material.** It does **not** mean the paper omitted the information. Dataset totals must not be mistaken for the actual study sample.

| Study | Verified data, target, and method details | Evaluation and implementation | Interpretive boundary |
|---|---|---|---|
| Sameni et al., *A nonlinear Bayesian filtering framework…* (2007) | Single-channel; normal reference ECG; added white/colored Gaussian noise and real muscle artifact; EKF/EKS/UKF; no supervised neural target | SNR and morphology; conventional filtering/adaptive/wavelet comparisons | Cohort size, sampling rate, window, and deployment resource totals NR-E. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/18075033/?utm_source=openai)) |
| *Comparison of Baseline Wander Removal Techniques…* (2017) | 765 electrophysiological setups; approximately 5.5 million simulated signals; modeled ischemia and baseline | Five methods; explicit ST-change assessment | Simulation provides controlled truth, not prospective clinical validation. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5361052/?utm_source=openai)) |
| Chiang et al., FCN-DAE (2019) | Supervised clean/denoised waveform MSE; convolutional architecture; Adam; batch normalization | SNR improvement and reconstruction comparisons | Clinical endpoints and complete split provenance NR-E. ([scholars.lib.ntu.edu.tw](https://scholars.lib.ntu.edu.tw/entities/publication/5ae56f43-3ade-47ba-9e8a-98dd993cc4a3?utm_source=openai)) |
| DeepFilter, 2021 preprint/later journal version | QT reference ECG; NSTDB baseline noise; learned baseline removal | Distance/similarity metrics; public code and comparator implementations | Experimental schemes differ between preprint and revised journal repositories. ([arxiv.org](https://arxiv.org/abs/2101.03423?utm_source=openai)) |
| Per-electrode IMU study (2021) | Custom acquisition; local motion sensing; two-stage NLMS | Actual motion scenarios; offline MATLAB processing | Instrumentation feasibility is not evidence of a completed real-time denoising pipeline. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC8450177/?utm_source=openai)) |
| DeScoD-ECG, final journal volume (2024) | QT + NSTDB; paired conditional diffusion; iterative inference; multi-shot averaging | Four distance-based metrics; digital and learned baselines | Sampling variability is not automatically calibrated clinical uncertainty; parameter count and end-to-end latency NR-E. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11422060/?utm_source=openai)) |
| *A Morphology-Preserving Algorithm…* (2024) | EMG contamination; MIT-BIH and synthetic signals; comparison with adaptive wavelet–Wiener filtering | Landmark/segment assessment; roughly 0.5 s per 30 s signal on an average PC | Throughput does not establish causal latency or bedside validity. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11100958/?utm_source=openai)) |
| Liu et al., *Self-Supervised Electrocardiograph De-Noising* (2025) | 18,604 selected Tianchi recordings; 500 Hz; 10 s; random 80:20 split; approximately 100 manually annotated examples for segmentation; TP-derived Gaussian noise assumptions | Autoencoder and segmentation U-Net; disease-classification evaluation | Patient-disjointness and true cross-device testing are not established by the extracted description. ([researchgate.net](https://www.researchgate.net/publication/388711199_Self-Supervised_Electrocardiograph_De-noising?utm_source=openai)) |
| Galiger et al., sparse dictionary/FISTA-Net (2025) | BUT QDB; K-SVD noise dictionary; learned sparse reconstruction and subtraction | Denoising and computational comparisons; public code | Exact cohort, context window, and clinical morphology endpoints NR-E. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/41335795/?fc=None&ff=20251204130013&v=2.18.0.post22+67771e2&utm_source=openai)) |
| *Enhancing ECG Movement Artifact Filtering for Unseen Data…*, BIBM (2025; indexed 2026) | PTB-XL/QT training; MIT-BIH external testing; subject-disjoint design; added NSTDB electrode-motion noise | SNR improvement/output SNR; low and medium input SNR | Cross-dataset evidence, but contamination remains constructed. ([doi.org](https://doi.org/10.1109/BIBM66473.2025.11356550?utm_source=openai)) |
| SC-CycleGAN (2026) | Real wearable noisy data for training; unpaired clean/noisy sets; spectrum-consistency loss; separate constructed evaluation data | Denoising and quality assessment | Unpaired learning partially addresses target availability, not automatically disease-identity preservation. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S095219762600179X?utm_source=openai)) |
| ML-CDAE (2026) | Simultaneous 12-lead input/output; real and simulated ECG; mixed physical noise | MSE/SNR improvement; reported model footprint ≈12,498 KB and inference latency 3.4 ms | Model storage is not peak RAM; inference time is not full acquisition-to-output latency. ([mdpi.com](https://www.mdpi.com/2624-6120/7/1/18?utm_source=openai)) |
| DWT–ADTF FPGA study (2026) | Intel Cyclone V SoC prototype; public ECG with controlled contamination | Reported 1.09 ms system latency, 426 mW, under 5% logic utilization | Hardware-specific evidence; general clinical preservation not established by these measures. ([mdpi.com](https://www.mdpi.com/2073-8994/18/7/1189?utm_source=openai)) |
| Granese et al., *The Negative Impact…* (2023 workshop) | Several denoisers evaluated before a TdP-risk classifier | Denoising metrics versus classifier accuracy/reliability | Demonstrates task-specific harm, not that all denoising is harmful. ([openreview.net](https://openreview.net/pdf/1b3fd4fcb06750e1ffe2a45485e409faede75a6b.pdf?utm_source=openai)) |

Across this ledger, population composition, independently sourced artifact diversity, training cost, peak memory, and comprehensive clinical-feature evaluation could not be consistently extracted. That is a limitation of both comparability and this survey—not proof that every paper omitted them.

---

## 6. Under-explored directions

“Few papers found” is separated below from evidence of an unresolved problem.

| Candidate direction | What the search establishes | Counterexamples/partial coverage | Confidence and limitation |
|---|---|---|---|
| **Feature-specific reliability and abstention** | Few retrieved studies directly connect reconstruction confidence to ST/QT/landmark error under external shift | Uncertainty-aware antithetic diffusion and joint quality/denoising frameworks exist | **Moderate confidence in the residual validation gap**, not in absence of uncertainty methods. ([pure.amsterdamumc.nl](https://pure.amsterdamumc.nl/en/publications/antithetic-sampling-enhanced-probabilistic-diffusion-for-denoisin/?utm_source=openai)) |
| **Naturally noisy, cross-device clinical validation** | Retrieved controlled benchmarks often retain constructed targets; real acquisition studies are setting-specific | Subject-disjoint cross-dataset work, unpaired wearable training, and upper-arm acquisition studies | **Moderate-to-high confidence** that these are distinct validation levels; broad field-wide prevalence remains unquantified. ([doi.org](https://doi.org/10.1109/BIBM66473.2025.11356550?utm_source=openai)) |
| **Preservation of low-amplitude and localized pathology in multi-lead restoration** | Multi-lead reconstruction gains are demonstrated more directly than diagnostic preservation | ML-CDAE; generative–contrastive multi-lead work; tensor-related precedents | **Moderate confidence**; late discovery of additional multi-lead literature prevents an absence claim. ([mdpi.com](https://www.mdpi.com/2624-6120/7/1/18?utm_source=openai)) |
| **Noisy-only learning under correlated, nonstationary artifacts** | Existing noisy-only approaches make specific assumptions about noise or physiological intervals | TP-informed self-supervision and unpaired SC-CycleGAN | **Strong methodological motivation; partial empirical coverage.** The question is assumption validity, not whether self-supervision exists. ([researchgate.net](https://www.researchgate.net/publication/388711199_Self-Supervised_Electrocardiograph_De-noising?utm_source=openai)) |
| **Joint morphology–latency–energy validation** | Resource measurements and morphology studies exist, but their intersection is not well established in the extracted evidence | DSP/FPGA implementations and neural timing reports | **Moderate confidence**; absence of a retrieved unified benchmark is not proof none exists. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/23367417/?utm_source=openai)) |
| **Federated/personalized waveform restoration** | Search results frequently concerned federated classification rather than independently validated denoising | Federated ECG systems with noise-aware components were retrieved | **Insufficient evidence for a verified gap.** Retain as a search lead, not a core research opportunity. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC12219762/?utm_source=openai)) |

**Not accepted as gaps:** “no real-noise studies,” “no morphology-aware methods,” “no downstream evaluation,” “no multi-lead denoising,” “no embedded implementations,” and “no self-supervised ECG denoising.”

---

## 7. Unresolved research gaps

The following are **residual gaps after counterexample review**. “Partially addressed” means a defensible unresolved question remains; it does not mean the direction is empty.

| ID / dimension | Already done and representative evidence | What remains unresolved and why it matters | Verification status and addressing experiment |
|---|---|---|---|
| **G1. Methodological foundations: target identifiability** | Paired restoration, TP-informed noisy-only learning, and unpaired translation use different assumptions. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11422060/?utm_source=openai)) | Which cardiac/artifact combinations are distinguishable from the available observations? A plausible output may not be the patient’s waveform. | **Partially addressed.** Vary signal–noise dependence and available references; test feature recovery and explicit failure detection. |
| **G2. Noise realism and synthetic-to-real transfer** | NSTDB enables controlled measured-artifact mixtures; custom studies evaluate actual motion. ([archive.physionet.org](https://archive.physionet.org/physiobank/database/nstdb/?utm_source=openai)) | A method’s ranking under additive corruption may not transfer to changing contact, saturation, or coupled motion/EMG conditions. | **Partially addressed.** Train under several corruption models; evaluate unchanged models on independently acquired natural artifacts. |
| **G3. Dataset, device, patient, and domain generalization** | Subject-split cross-dataset evaluation exists; real wearable datasets also exist. ([doi.org](https://doi.org/10.1109/BIBM66473.2025.11356550?utm_source=openai)) | Cross-dataset, cross-device, and cross-population claims are not equivalent. Their separate contributions remain insufficiently resolved in the extracted studies. | **Partially addressed.** Factorial patient × device × site × artifact-source holdouts; report subgroup uncertainty rather than only pooled scores. |
| **G4. Evaluation and benchmark comparability** | Studies use different signal metrics, noise scaling, datasets, and experimental versions; reproducible repositories are available. ([github.com](https://github.com/fperdigon/DeepFilter?utm_source=openai)) | Reported improvements cannot be pooled meaningfully without harmonizing target, normalization, splits, and corruption provenance. | **Defensible comparability gap.** Re-evaluate representative principles under a frozen, versioned protocol with paired patient-level statistics. |
| **G5. Morphology preservation** | ST simulation, landmark-focused EMG suppression, and morphology-weighted learning exist. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5361052/?utm_source=openai)) | Aggregate gains do not establish simultaneous preservation of P/QRS/T, ST, QT, timing, and rare morphology. | **Partially addressed.** Predefine feature-specific non-inferiority endpoints across pathologies and noise severities. |
| **G6. Clinical and downstream-task validity** | Both beneficial and harmful downstream effects have been reported. ([researchgate.net](https://www.researchgate.net/publication/388711199_Self-Supervised_Electrocardiograph_De-noising?utm_source=openai)) | When does denoising help rather than merely shift the input distribution or optimize one downstream model? | **Confirmed task dependence; unresolved conditions.** Compare frozen, retrained, and jointly trained downstream models, plus independent readers where appropriate. |
| **G7. Robustness, uncertainty, and recoverability** | Generative sampling, uncertainty-aware diffusion, and quality-assessment integration are available. ([pure.amsterdamumc.nl](https://pure.amsterdamumc.nl/en/publications/antithetic-sampling-enhanced-probabilistic-diffusion-for-denoisin/?utm_source=openai)) | Are uncertainty estimates calibrated to clinically meaningful reconstruction errors, especially outside training conditions? | **Partially addressed.** Evaluate feature-level interval coverage, selective risk, and rejection under held-out artifact mechanisms. |
| **G8. Temporal and beat-to-beat fidelity** | Recurrent processing, beat-based structural methods, and landmark preservation have precedents. ([arxiv.org](https://arxiv.org/abs/1807.11551?utm_source=openai)) | The extracted evidence does not establish a common evaluation of rhythm transitions, ectopy, and downstream HRV together with denoising. | **Bounded evidence gap; moderate confidence.** Test long continuous recordings without beat averaging, with annotated transitions and timing endpoints. |
| **G9. Computational, memory, and streaming constraints** | Embedded DSP, FPGA implementations, and neural timing/storage measurements exist. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/23367417/?utm_source=openai)) | Causality, look-ahead, initialization, memory, energy, and worst-case latency are not comparable across these demonstrations. | **Partially addressed.** Matched-hardware streaming benchmark with identical acquisition rate and full buffering costs. |
| **G10. Multi-lead and sensor-assisted reliability** | Multi-lead learning and reference-assisted cancellation demonstrate benefits. ([mdpi.com](https://www.mdpi.com/2624-6120/7/1/18?utm_source=openai)) | Which benefits survive shared-electrode corruption, reference failure, lead dropout, and lead-specific abnormalities? | **Partially addressed.** Controlled electrode/reference failure study with spatial morphology endpoints and uncertainty gating. |
| **G11. Reproducibility and standardized evidence** | Open implementations exist, and DeepFilter documents version-specific experimental differences. ([github.com](https://github.com/fperdigon/DeepFilter?utm_source=openai)) | Independent replication requires more than architecture code: data manifests, noise provenance, preprocessing, checkpoints, and runtime conditions matter. | **Defensible reproducibility requirement; prevalence unquantified.** Independent reruns using frozen manifests and published deviations. |

### Gaps removed or narrowed after verification

- **Simple suppression of known baseline or mains components:** extensively addressed; not a generic open problem.
- **Existence of morphology-preserving methods:** addressed; broadened validation remains open.
- **Existence of real-time implementation:** addressed; comparable clinical/resource trade-offs remain open.
- **Existence of cross-dataset, unpaired, multi-lead, or uncertainty-aware methods:** addressed at proof-of-concept level; broader robustness remains open.

A specific claim that pediatric, neonatal, paced, or other subpopulation denoising is “unexplored” is **not supported sufficiently by this search**. Such populations belong in validation planning, but not in unsupported novelty claims.

---

## 8. Future directions explicitly proposed by researchers

Only directions visible in the retrieved author text are attributed here. Broader ideas developed in this review remain labeled as synthesis.

### A. Repeatedly proposed across multiple studies

**Wearable and clinical deployment.** DeScoD-ECG discusses possible clinical monitoring applications; sparse-learning studies motivate wearable resource constraints; multi-lead and FPGA papers discuss practical implementation. These are recurring aspirations, but their supporting evidence ranges from algorithm experiments to actual hardware prototypes. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11422060/?utm_source=openai))

**More realistic generalization.** The unseen-data DAE study explicitly aims to improve validation toward free-living use. Real-noise unpaired learning and real-acquisition comparisons subsequently investigate related concerns. This is a longitudinal connection made here, not a verified citation chain between all authors. ([doi.org](https://doi.org/10.1109/BIBM66473.2025.11356550?utm_source=openai))

### B. Proposed by a small number of retrieved studies

- **Determine when auxiliary-motion cancellation is beneficial:** explicitly motivated by variable performance in the per-electrode IMU study. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC8450177/?utm_source=openai))
- **Pruning, quantization, and reduced precision for multi-lead neural deployment:** discussed as implementation optimizations by the ML-CDAE authors. They should not be treated as validated outcomes of that paper unless separately measured. ([mdpi.com](https://www.mdpi.com/2624-6120/7/1/18?utm_source=openai))
- **Small-data, interpretable sparse learning for wearables:** motivated in the 2024 dictionary study and subsequently developed through a learned FISTA-based formulation in 2025. ([degruyterbrill.com](https://www.degruyterbrill.com/document/doi/10.1515/cdbme-2024-2150/pdf?licenseType=open-access&utm_source=openai))

### C. Directions that have subsequently been investigated

| Earlier motivation | Retrieved subsequent investigation | What is not yet established |
|---|---|---|
| Reduce dependence on paired clean targets | TP-informed self-supervision; real unpaired SC-CycleGAN | Assumption validity across correlated artifacts and unusual rhythms. ([researchgate.net](https://www.researchgate.net/publication/388711199_Self-Supervised_Electrocardiograph_De-noising?utm_source=openai)) |
| Improve generalization beyond a single database | Subject-disjoint cross-dataset DAE evaluation | Full cross-device natural-artifact performance. ([doi.org](https://doi.org/10.1109/BIBM66473.2025.11356550?utm_source=openai)) |
| Exploit multiple leads | ML-CDAE and multi-lead representation learning | Clinical preservation under shared-source corruption. ([mdpi.com](https://www.mdpi.com/2624-6120/7/1/18?utm_source=openai)) |
| Make denoising computationally practical | DSP/FPGA demonstrations and efficient learned optimization | A common fidelity–latency–energy comparison. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/23367417/?utm_source=openai)) |

### D. Directions still unresolved at the claimed application level

Reliable clinical use under external shift, trustworthy reconstruction uncertainty, and preservation of diagnostically important details remain broader than the endpoints demonstrated in the retrieved studies. This is a **synthesis judgment**, not proof that every author explicitly listed these as future work.

---

## 9. Cross-paper gaps inferred from synthesis

The following are **inferences across studies**, not direct findings of one paper.

### 9.1 The target waveform can conceal the most important assumption

A nominally clean recording, a filtered recording, a synthetic ECG, and an unpaired sample from a “clean domain” represent different targets. Comparing models without distinguishing these targets can reward agreement with preprocessing or a population prior rather than recovery of the underlying patient signal. This inference follows from the contrasting constructions used in simulation, paired diffusion, and unpaired translation. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5361052/?utm_source=openai))

### 9.2 Noise-source independence is a separate generalization problem

Holding out patients does not hold out artifact generators. A benchmark can test new ECGs while reusing the same small noise collection. Consequently, subject generalization and noise-source generalization should be measured separately. NSTDB’s finite source recordings and the recent emphasis on subject-disjoint external evaluation motivate this distinction. ([archive.physionet.org](https://archive.physionet.org/physiobank/database/nstdb/?utm_source=openai))

### 9.3 “Morphology preservation” spans substantially different evidence

The term can mean a plausible plot, high correlation, landmark agreement, preserved ST amplitude, or unchanged diagnostic interpretation. These should be recorded as different evidence levels. The landmark-focused EMG study and ST simulation provide stronger feature-specific evidence than a global similarity score alone. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11100958/?utm_source=openai))

### 9.4 Task-aware optimization creates a second validation problem

A denoiser can preserve what one classifier uses while altering information required by another task or a clinician. Therefore, task-aware losses need independent-task and waveform evaluation. Opposing downstream results make universal preprocessing prescriptions unjustified. ([openreview.net](https://openreview.net/pdf/1b3fd4fcb06750e1ffe2a45485e409faede75a6b.pdf?utm_source=openai))

### 9.5 Speed, causality, and low power are different properties

Fast block processing does not reveal required future context; a small model does not reveal peak activation memory; FPGA power is not directly comparable with GPU timing. This follows from the heterogeneous reporting represented by PC throughput, neural inference timing, and hardware resource studies. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11100958/?utm_source=openai))

### 9.6 Scientific novelty increasingly lies outside the architecture

The coexistence of morphology losses, diffusion, unpaired learning, model-unrolled sparsity, and multi-lead networks suggests that the limiting question is often **what experiment would falsify the method’s assumptions**, rather than which new block can improve an existing benchmark. This is the review’s synthesis, not a quantitative claim about publication proportions.

---

## 10. Research questions

The questions below arise from the qualified gaps above. Proposed hypotheses are deliberately falsifiable.

### RQ1. Can denoising improve artifact suppression while preserving clinically important morphology across pathologies?

- **Underlying gap and support:** G5; explicit morphology studies exist, but their endpoints and conditions differ. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5361052/?utm_source=openai))
- **Why existing methods are insufficient:** success on ST correction, selected landmarks, or weighted waveform loss does not establish preservation of all relevant features.
- **Hypothesis:** a morphology-constrained objective reduces feature errors without materially sacrificing artifact suppression, including on unseen pathology.
- **Required data/noise:** annotated multi-lead ECG with ST abnormalities, conduction changes, ectopy, and varied P/T morphology; controlled baseline, EMG, electrode-motion mixtures plus naturally noisy recordings.
- **Baselines/design:** task-appropriate classical filters, wavelet–Wiener, model-based filtering, FCN/U-Net, and generative restoration. Match training data and tuning budgets; ablate each constraint.
- **Primary evaluation:** prespecified ST-amplitude, QT, QRS-duration, and landmark-error endpoints—not a composite score hiding trade-offs. Use independent readers or delineators and patient-level confidence intervals.
- **Generalization/computation:** leave-pathology, dataset, and device out; report latency and memory.
- **Confounders/failure modes:** annotation uncertainty, normalization erasing amplitude, circular evaluation using the training delineator, suppression of uncommon features.
- **Meaningful progress:** improved noise rejection with prespecified feature non-inferiority across external strata, not merely better mean RMSE.

### RQ2. Under which conditions does denoising improve downstream analysis relative to robust analysis of raw ECG?

- **Gap/support:** G6; both downstream benefit and harm have been reported. ([openreview.net](https://openreview.net/pdf/1b3fd4fcb06750e1ffe2a45485e409faede75a6b.pdf?utm_source=openai))
- **Hypothesis:** benefit depends on noise severity, task, and whether the downstream model is adapted to denoised inputs.
- **Data/noise:** identical ECG cohorts supporting QRS detection, rhythm classification, and at least one morphology-sensitive task; clean, controlled-noise, and natural-noise strata.
- **Baselines:** raw-input model; conventional preprocessing; learned denoising; noise-augmented raw-input model; joint denoiser–task model.
- **Design:** factorial comparison of **frozen**, **retrained**, and **jointly trained** downstream models. Keep test subjects and annotation rules fixed.
- **Primary metrics:** task-specific sensitivity/precision or AUROC/AUPRC and calibration; report false positives per monitoring time when relevant.
- **Morphology/generalization:** independent interval/landmark assessment and an external dataset; evaluate tasks not used in training.
- **Computational evaluation:** added acquisition-to-decision latency and energy.
- **Confounders/failures:** train–test representation mismatch, classifier-specific shortcuts, label imbalance, loss of diagnostically useful information.
- **Progress:** identify reproducible conditions of benefit, neutrality, and harm—not a universal claim that preprocessing is necessary.

### RQ3. Which corruption models produce genuine synthetic-to-real and cross-device transfer?

- **Gap/support:** G2–G3; cross-dataset constructed-noise evaluation and real wearable acquisition studies partially address different parts of this question. ([doi.org](https://doi.org/10.1109/BIBM66473.2025.11356550?utm_source=openai))
- **Hypothesis:** device- and state-conditioned corruption models transfer better than fixed additive mixtures.
- **Data/noise:** synchronized recordings across devices/electrode types, activity labels, and auxiliary motion/contact measurements; independent artifact sessions.
- **Baselines:** AWGN-only training; NSTDB additive training; mixed-artifact training; real unpaired training; classical/adaptive methods.
- **Design:** hold out artifact sessions, patients, devices, and sites separately and jointly. Include controlled contact disturbance, EMG, baseline, mains interference, and acquisition failures.
- **Primary metrics:** external feature errors and downstream performance; waveform error only where a defensible reference exists.
- **Morphology/generalization:** blinded interpretation and lead-specific endpoints; distinguish hardware from anatomical lead-position changes.
- **Computation:** include adaptation/training cost as well as inference.
- **Confounders/failures:** reference mismatch, synchronization errors, altered physiology during activity, device-specific gain normalization.
- **Progress:** transfer gains on untouched natural recordings, with uncertainty around performance and no hidden target-device tuning.

### RQ4. What assumptions make noisy-only ECG denoising valid under correlated artifacts?

- **Gap/support:** G1; TP-informed learning and unpaired adversarial methods provide distinct precedents. ([researchgate.net](https://www.researchgate.net/publication/388711199_Self-Supervised_Electrocardiograph_De-noising?utm_source=openai))
- **Hypothesis:** explicitly accounting for temporal artifact correlation and uncertain reference intervals reduces bias compared with independence-based objectives.
- **Data/noise:** controlled benchmark with known clean truth plus real wearable data; colored noise, burst EMG, drift, electrode-motion transients, and signal-dependent contamination.
- **Baselines:** paired-supervised upper-reference condition, TP-informed self-supervision, masking/consistency methods, unpaired translation, and classical denoisers.
- **Design:** independently vary noise correlation, mean, signal dependence, and TP-interval availability. Test annotation-assisted and annotation-free components separately.
- **Primary metrics:** conditional reconstruction bias, feature error, and downstream performance.
- **Morphology/generalization:** include rhythms without a simple regular isoelectric interval; external artifact sources.
- **Computation:** adaptation time and per-record optimization cost.
- **Confounders/failures:** identity mapping, learning residual noise, treating genuine low-amplitude activity as artifact, transferring clean-domain morphology.
- **Progress:** an explicit validity envelope and detectable failure conditions, not only average superiority.

### RQ5. Can a denoiser recognize when clinically relevant reconstruction is unreliable?

- **Gap/support:** G7; uncertainty-aware diffusion and joint denoising/quality assessment already exist. ([pure.amsterdamumc.nl](https://pure.amsterdamumc.nl/en/publications/antithetic-sampling-enhanced-probabilistic-diffusion-for-denoisin/?utm_source=openai))
- **Hypothesis:** feature-specific uncertainty is more useful for safe rejection than generic output variance or a global quality label.
- **Data/noise:** paired controlled data spanning mild to severe corruption; naturally noisy records with adjudicated interpretability and external devices.
- **Baselines:** deterministic denoiser with quality score, ensemble, stochastic generative model, and no-reconstruction/reacquisition policy.
- **Design:** calibrate on validation subjects only; evaluate under unseen noise, clipping, dropout, and domain shift.
- **Primary metrics:** coverage and width of feature intervals, risk–coverage curves, missed-failure rate, and retained usable recording time.
- **Clinical evaluation:** uncertainty in ST amplitude, QT, and R timing; blinded assessment of false confidence.
- **Computation:** cost of repeated sampling and alternative lightweight uncertainty estimators.
- **Confounders/failures:** shared bias across ensemble members, confidently generated plausible beats, rejection concentrated in certain populations.
- **Progress:** fewer clinically important errors at a declared retained-coverage level, with external calibration.

### RQ6. Does multi-lead denoising preserve spatially localized diagnostic information under correlated corruption?

- **Gap/support:** G10; multi-lead reconstruction benefits are established at signal-metric level. ([mdpi.com](https://www.mdpi.com/2624-6120/7/1/18?utm_source=openai))
- **Hypothesis:** spatially constrained denoising improves robustness without copying morphology from cleaner but physiologically different leads.
- **Data/noise:** diagnostic 12-lead ECG, localized abnormalities, synchronized shared-electrode artifacts, lead dropout, and independent lead noise.
- **Baselines:** independent single-lead denoisers, low-rank methods, multi-lead autoencoder, and physiology-constrained spatial models.
- **Design:** distinguish independent lead corruption from shared-electrode corruption; ablate lead-consistency constraints.
- **Primary metrics:** per-lead feature error and preservation of diagnostic lead patterns, not only averaged SNR.
- **Clinical/generalization:** independent diagnostic interpretation; hold out devices and abnormality groups.
- **Computation:** scaling with lead count, missing-lead handling, peak memory, latency.
- **Confounders/failures:** lead mislabeling, electrode-position differences, algebraic redundancy overstating sample size, transfer of abnormalities between leads.
- **Progress:** spatial diagnostic non-inferiority with improved robustness under correlated artifacts.

### RQ7. When do auxiliary sensors add useful information beyond ECG-only denoising?

- **Gap/support:** G10; IMU and impedance references have benefits but condition-dependent performance. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC8450177/?utm_source=openai))
- **Hypothesis:** reference-quality gating outperforms unconditional sensor fusion and ECG-only processing across heterogeneous motion.
- **Data/noise:** simultaneous ECG, per-electrode motion where feasible, impedance/contact signals, and activity annotations.
- **Baselines:** NLMS/RLS, ungated fusion, ECG-only neural denoiser, and quality-based rejection.
- **Design:** controlled motion plus free living; introduce reference dropout, delay, and misleading correlation.
- **Primary metrics:** independently adjudicated usable-signal duration and downstream detection, supported by feature error where valid references exist.
- **Morphology/generalization:** P/QRS/T preservation and rhythm transitions across participants/electrode types.
- **Computation:** total sensor, synchronization, processing, and communication energy.
- **Confounders/failures:** reference contains physiology, motion sensor misses local contact changes, cancellation removes genuine activity.
- **Progress:** a validated decision rule specifying when sensing helps, when it does not, and when to abstain.

### RQ8. What fidelity is achievable under genuinely causal, low-power streaming constraints?

- **Gap/support:** G9; embedded implementations already establish feasibility. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/23367417/?utm_source=openai))
- **Hypothesis:** constrained hybrid or model-unrolled methods offer competitive clinical fidelity at lower end-to-end resource cost than unrestricted offline models.
- **Data/noise:** continuous recordings with intermittent artifacts, transitions, clean periods, and device disconnect/reconnect events.
- **Baselines:** causal classical/adaptive methods, causal convolutional models, learned sparse methods, and offline methods as non-deployable reference bounds.
- **Design:** fixed hardware, sampling rate, memory budget, and permitted look-ahead; include quantized implementations and startup behavior.
- **Primary metrics:** morphology non-inferiority, tail latency, peak RAM, and energy per recorded hour.
- **Generalization:** external devices, sampling rates, and artifact severity.
- **Confounders/failures:** excluding buffering cost, reporting batch throughput as latency, thermal/power measurement mismatch, state drift.
- **Progress:** reproducible continuous operation within declared budgets without clinically important degradation.

### RQ9. How stable are published method comparisons after harmonizing evaluation and provenance?

- **Gap/support:** G4–G11; version-specific experimental changes and heterogeneous endpoints complicate comparison. ([github.com](https://github.com/fperdigon/DeepFilter?utm_source=openai))
- **Hypothesis:** some apparent architectural advantages shrink or reverse after equalizing splits, targets, noise sources, tuning, and causal context.
- **Data/noise:** frozen patient and artifact manifests across multiple public datasets, plus a held-out real-noise cohort.
- **Baselines:** representative principles rather than dozens of nearly identical architectures.
- **Design:** independent reproduction, identical corruption draws, equal tuning budgets, repeated seeds, and preregistered endpoints.
- **Primary metrics:** paired patient-level differences and uncertainty; reproducibility of morphology and task outcomes.
- **Generalization/computation:** external datasets and matched-platform measurements.
- **Confounders/failures:** unequal implementation quality, selective hyperparameter tuning, undocumented preprocessing, benchmark overfitting.
- **Progress:** reproducible conditional conclusions about method assumptions and trade-offs, even if no universal winner emerges.

---

## 11. Recommended experimental designs and evaluation protocols

The following is a **proposed evaluation framework**, motivated by the heterogeneous evidence above.

### 11.1 Split the causes of generalization failure

Create independent partitions for:

1. **Patients**
2. **Recording sessions**
3. **Devices and electrode configurations**
4. **Artifact-source recordings**
5. **Sites**
6. **Pathology groups**, where the scientific question requires it

All segments from the same patient should remain together for the primary patient-generalization analysis. Overlapping windows must remain in the same partition. Normalization, dictionaries, denoising thresholds, and learned preprocessing must be fit without test information.

A patient-disjoint split is necessary for that claim, but does not establish artifact-source or device independence. The retrieved cross-dataset study illustrates progress on the former while retaining an additive artifact construction. ([doi.org](https://doi.org/10.1109/BIBM66473.2025.11356550?utm_source=openai))

### 11.2 Use three complementary data tracks

| Track | Construction | What it can establish | What it cannot establish alone |
|---|---|---|---|
| **Controlled synthetic** | Simulated cardiac activity and noise | Exact target, mechanistic stress tests, feature-specific bias | Real-acquisition validity |
| **Semi-synthetic** | Recorded reference ECG plus independently recorded artifacts | Controlled severity with realistic artifact waveforms | Coupled acquisition effects or perfect reference cleanliness |
| **Natural acquisition** | ECG recorded during genuine interference | Practical utility and robustness | Exact waveform error without an adequate reference |

This separation follows the fundamentally different constructions represented by ischemic simulation, NSTDB, and wearable acquisition studies. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5361052/?utm_source=openai))

### 11.3 Treat noise severity as multidimensional

In addition to a declared SNR definition, vary:

- artifact duration and intermittency;
- temporal correlation and spectrum;
- mixture composition;
- cross-lead dependence;
- relationship to cardiac phase or activity;
- abruptness of contact changes;
- clipping, missing samples, and reconnection.

For real recordings without a clean reference, do not report a nominal SNR as though it were ground truth. Use adjudicated quality, task success, and defensible auxiliary-reference analyses.

### 11.4 Require a clean-input preservation test

Every denoiser should also process clean or high-quality ECG. Measure:

- changes in amplitude and intervals;
- spurious peaks or waves;
- loss of small deflections;
- altered beat timing;
- downstream prediction changes.

This is a proposed safeguard against unnecessary modification, motivated by the demonstrated possibility of downstream degradation. ([openreview.net](https://openreview.net/pdf/1b3fd4fcb06750e1ffe2a45485e409faede75a6b.pdf?utm_source=openai))

### 11.5 Use an evaluation hierarchy

1. **Signal level:** explicitly defined SNR improvement, RMSE, PRD, correlation.
2. **Regional level:** P, QRS, ST, T, and baseline-reference regions.
3. **Feature level:** amplitudes, onset/offset timing, QRS duration, QT, R timing.
4. **Sequence level:** RR intervals, ectopy, rhythm transitions, HRV where appropriate.
5. **Task level:** detection, rhythm classification, diagnostic classification.
6. **Interpretation level:** blinded reader agreement or task-specific adjudication.
7. **Reliability level:** calibration, selective rejection, failure detection.
8. **Deployment level:** latency, memory, energy, causality, startup and boundary behavior.

Existing ST, landmark, detector, and classifier studies justify keeping these levels separate. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5361052/?utm_source=openai))

### 11.6 Statistical and reproducibility requirements

- Use the **patient or recording session**, not individual samples, as the principal independent unit.
- Report distributions and worst-performing strata, not only pooled means.
- Pair comparisons using identical test signals and noise realizations.
- Prespecify clinically meaningful non-inferiority margins with domain experts.
- Separate primary endpoints from exploratory metrics.
- Publish record IDs, patient mappings, artifact offsets, scaling rules, seeds, preprocessing order, versions, checkpoints, and hardware settings.
- Report failed runs and excluded recordings.
- Distinguish reproduction of author code from independent reimplementation.

### 11.7 What a strong benchmark would contain

A strong benchmark would combine:

- multiple ECG datasets and acquisition systems;
- clinically annotated morphology;
- controlled and natural noise;
- independent noise-source holdouts;
- rare morphology and rhythm-transition challenge sets;
- raw/no-denoise and strong classical baselines;
- supervised, unpaired, and model-based methods;
- a causal embedded track;
- hidden external tests;
- a failure/abstention track;
- versioned, executable evaluation.

The benchmark should produce **conditional comparisons**, not one aggregate ranking that conceals clinical and computational trade-offs.

---

## 12. Key datasets and evaluation practices

### 12.1 Recurring and complementary datasets

| Dataset/resource | Verified characteristics | Appropriate role | Important limitation |
|---|---|---|---|
| **MIT-BIH Arrhythmia Database** | 48 approximately half-hour, two-channel recordings from 47 subjects; 360 Hz | Beat/rhythm reference, historical denoising comparisons | Not an acquisition-paired clean/noisy database; actual selected records and leads must be disclosed. ([physionet.org](https://physionet.org/content/mitdb/1.0.0/)) |
| **MIT-BIH Noise Stress Test Database** | Recorded baseline, muscle, and electrode-motion artifacts; standard constructed ECGs based on records 118/119 at −6 to 24 dB | Reproducible artifact stress testing | Few source recordings; measured noise plus digital addition is semi-synthetic; standard stress records emphasize electrode motion. ([archive.physionet.org](https://archive.physionet.org/physiobank/database/nstdb/?utm_source=openai)) |
| **QT Database** | 105 fifteen-minute, two-channel excerpts; 250 Hz; selected to avoid substantial artifacts; representative beats have manual wave annotations | Morphology/delineation and paired corruption benchmarks | Manual annotations cover selected beats rather than every sample; “selected clean” is not physically noise-free. ([physionet.org](https://physionet.org/physiobank/database/qtdb/doc/node3.html?utm_source=openai)) |
| **PTB-XL v1.0.3** | 21,799 ten-second, 12-lead ECGs from 18,869 patients; 100/500 Hz distributions | Diagnostic diversity and external evaluation | Version matters; not a paired denoising target dataset. ([physionet.org](https://www.physionet.org/content/ptb-xl/1.0.3/records100/18000/?utm_source=openai)) |
| **LUDB** | 200 ten-second, 12-lead recordings; 500 Hz; cardiologist P/QRS/T boundaries and peaks; varied diagnoses | Explicit morphology validation | Small, short-record dataset; not long-duration natural-artifact ground truth. ([physionet.org](https://physionet.org/content/ludb/1.0.1/data/?utm_source=openai)) |
| **BUT QDB** | 18 long-term single-lead recordings from 15 subjects, ages 21–83; ECG 1,000 Hz and accelerometer 100 Hz; free-living acquisition | Natural quality changes, sensor-assisted studies | Quality labels are not clean waveform targets; annotation coverage varies by record. ([physionet.org](https://physionet.org/content/butqdb/1.0.0/?utm_source=openai)) |
| **Motion Artifact Contaminated ECG Database** | Short recordings from one healthy 25-year-old male performing activities | Mechanistic motion examples | Cannot substantiate population generalization. ([physionet.org](https://www.physionet.org/content/macecgdb/1.0.0/?utm_source=openai)) |
| **MIMIC-IV-ECG** | Diagnostic ECG repository linked to clinical data | External clinical and diagnostic validation | Linkage and diagnostic labels do not provide a simultaneous clean counterpart. ([physionet.org](https://physionet.org/content/mimic-iv-ecg/1.0/)) |
| **BUT PDB** | ECG resource with P-wave annotations | Targeted low-amplitude atrial-wave evaluation | Should complement, not replace, broader morphology and rhythm testing. ([physionet.org](https://physionet.org/content/but-pdb/1.0.0/?utm_source=openai)) |
| **Custom wearable/upper-arm/impedance datasets** | Actual acquisition under specific movement or muscle conditions | Test acquisition realism and auxiliary sensing | Device-specific references and limited populations complicate comparison. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9332869/?utm_source=openai)) |

**Adjacent resource:** ECG-image datasets and grayscale-image denoising studies address scanning, photography, and paper artifacts. They can support digitization research but should not be pooled with electrical waveform artifact removal. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S174680942500919X?utm_source=openai))

### 12.2 Metrics: what they establish

- **SNR/SNR improvement:** require explicit signal/noise definitions and scaling. They support controlled reconstruction comparisons.
- **RMSE/MSE:** quantify amplitude error under the chosen scaling.
- **PRD:** requires an explicit denominator and centering convention.
- **Correlation/cosine similarity:** summarize shape agreement but do not independently establish correct amplitudes, intervals, or diagnosis.
- **Landmark/interval error:** directly evaluates selected morphology, but depends on annotation and delineator reliability.
- **Downstream performance:** establishes usefulness for that task/model/cohort, not universal clinical safety.
- **Reader assessment:** adds interpretation evidence but needs blinding, adjudication, and inter-reader analysis.

The different conclusions reached by signal-only, landmark-focused, ST-focused, and classifier-focused studies illustrate why these metrics should not be substituted for one another. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11422060/?utm_source=openai))

**Recommended practice:** publish metric formulas, physical units, normalization order, alignment policy, and treatment of boundary samples. Do not compare numerical scores across studies unless these conditions match.

---

## 13. Contradictions and unresolved debates

### Does denoising necessarily improve diagnosis?

No universal conclusion is supported. Granese et al. report deterioration in a TdP-risk classification setting; Liu et al. report classification benefit; FGCT reports improved diagnostic accuracy. These studies differ in task, training, data, and preprocessing. The disagreement calls for factorial testing, not selecting one result as generally authoritative. ([openreview.net](https://openreview.net/pdf/1b3fd4fcb06750e1ffe2a45485e409faede75a6b.pdf?utm_source=openai))

### Are deep methods superior to classical methods?

Only conditionally. The real upper-arm comparison reports stronger morphological reconstruction for learned methods but stronger noise suppression for DWT. The ST simulation also identifies a computationally attractive classical alternative close to the best reconstruction method. Neither supports a universal family-level winner. ([arxiv.org](https://arxiv.org/abs/2607.11450))

### Is stronger suppression always preferable?

No. The morphology-preserving EMG comparison yields feature- and severity-dependent preferences. This supports evaluating a **noise-removal versus information-preservation trade-off**, rather than maximizing one signal metric. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11100958/?utm_source=openai))

### Does self-supervision remove the need for assumptions?

No. It changes the assumptions. TP-informed learning assumes particular noise information can be obtained from selected intervals; unpaired translation assumes a learnable relationship between noisy and clean distributions. Their validity must be tested under the intended physiology and acquisition process. ([researchgate.net](https://www.researchgate.net/publication/388711199_Self-Supervised_Electrocardiograph_De-noising?utm_source=openai))

### Is denoising necessary before another reconstruction model?

A 2026 lead-reconstruction study investigates whether models trained directly on noisy ECG can make separate denoising redundant. Its experiment uses added Gaussian noise and a particular reconstruction task; it is an important counterexample, not evidence that denoising is unnecessary for diagnostic display or all physiological analysis. ([frontiersin.org](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2026.1827352/full?utm_source=openai))

### Do stochastic reconstructions provide trustworthy uncertainty?

Not automatically. Uncertainty-aware diffusion is now explicitly investigated, but the next question is whether uncertainty predicts clinically relevant feature errors under external shift. Reconstruction variability and calibrated patient-specific uncertainty should remain separate claims. ([pure.amsterdamumc.nl](https://pure.amsterdamumc.nl/en/publications/antithetic-sampling-enhanced-probabilistic-diffusion-for-denoisin/?utm_source=openai))

---

## 14. Limitations of this survey

1. **Search saturation was not reached in full.** Major families, noise types, and recurring datasets were represented, and apparent gaps were challenged. However, late searches still identified relevant multi-lead, unpaired, and uncertainty-aware work when the retrieval limit was reached. It would be inaccurate to state otherwise.

2. **This was not a formal database-exported systematic review.** Discovery used web-indexed scholarly records, PubMed/PMC, publisher pages, PhysioNet, institutional repositories, and preprints. It did not include complete Scopus, Web of Science, Embase, or IEEE Xplore exports, duplicate-independent screening, or a registered protocol.

3. **Full-text access was uneven.** Some publisher and repository pages were inaccessible. Consequently, detailed extraction is incomplete for patient characteristics, exact sample selection, windows, parameter counts, training resources, code versions, and reported author limitations. NR-E explicitly records this uncertainty.

4. **Maturity judgments are descriptive.** No publication-frequency estimates, arbitrary scores, or pooled performance rankings were generated.

5. **Terminology creates substantial retrieval ambiguity.** “ECG artifact removal” can mean removing ECG from another biosignal; “restoration” can mean missing-lead reconstruction; “denoising autoencoder” can describe representation learning rather than waveform cleanup.

6. **Coverage is weaker for specialized settings.** Fetal/neonatal ECG, MRI-related interference, electrosurgery, pacemaker-spike preservation, and subgroup-specific validation were not investigated sufficiently to support absence claims.

7. **Recent evidence has varying status.** Workshop papers and preprints are labeled. Search-index dates were not treated as publication dates.

8. **No claim of universal clinical validity is supported.** Evidence of better reconstruction, task performance, or hardware execution is kept separate from prospective clinical benefit.

**Critical self-review outcome:** the broad gap claims were revised after counterexamples. The retained opportunities concern qualified residual problems; federated/personalized restoration and population-specific “empty fields” were not promoted to verified gaps.

---

## 15. Research opportunity map

This map is descriptive and **does not rank opportunities**.

| Landscape region | Directions | Scientific emphasis |
|---|---|---|
| **Dense** | Frequency filtering; wavelet variants; supervised CNN/DAE restoration on constructed corruption | Contribution requires stronger assumptions testing, clinical endpoints, or deployment evidence—not architecture alone. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0010482502000343?utm_source=openai)) |
| **Established but fragmented** | Adaptive motion cancellation; Bayesian estimation; decomposition; sparse/low-rank processing; embedded implementations | Common protocols and failure characterization can connect otherwise isolated evidence. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/23367417/?utm_source=openai)) |
| **Emerging** | Unpaired/noisy-only learning; diffusion reliability; model-unrolled sparsity; frequency-guided attention | Test the new training or modeling assumption, not merely the model label. ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S095219762600179X?utm_source=openai)) |
| **Sparse within retrieved evidence** | Feature-calibrated abstention; unified clinical/resource evaluation; controlled cross-device natural-artifact transfer | Absence is not established; these remain qualified opportunity areas. |
| **Unresolved intersections** | Morphology × domain shift; self-supervision × correlated artifacts; multi-lead redundancy × localized pathology; sensor fusion × reference failure; streaming × calibrated reliability | These intersections motivate the concrete experiments below. |

---

## 16. Research opportunity table

| Research opportunity | Specific verified gap | Supporting evidence | Research question | Required experiment | Key evaluation |
|---|---|---|---|---|---|
| **Morphology-constrained restoration** | Explicit preservation methods exist, but comprehensive external feature preservation remains only partially addressed | ST, landmark, and morphology-weighted studies. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5361052/?utm_source=openai)) | Can artifact suppression improve without clinically important morphology changes? | Pathology-stratified comparison with constraint ablations and external testing | ST/QT/QRS/landmark non-inferiority; noise reduction; reader agreement |
| **Task-conditional denoising** | Downstream benefit is task-dependent, with documented benefit and harm | Classification studies with opposing outcomes. ([openreview.net](https://openreview.net/pdf/1b3fd4fcb06750e1ffe2a45485e409faede75a6b.pdf?utm_source=openai)) | When is denoising preferable to robust analysis of raw ECG? | Frozen/retrained/joint-model factorial experiment | Detection/classification performance, calibration, morphology, added latency |
| **Real-acquisition transfer benchmark** | Constructed-noise success does not establish natural-artifact validity | NSTDB construction and real acquisition studies. ([archive.physionet.org](https://archive.physionet.org/physiobank/database/nstdb/?utm_source=openai)) | Which methods retain usefulness on untouched natural artifacts? | Controlled, semi-synthetic, and natural tracks with independent artifact sources | External task performance, usable recording time, feature error |
| **Cross-device denoising** | Cross-dataset evaluation partially addresses, but does not isolate, device shift | Subject-disjoint external DAE testing and wearable acquisition evidence. ([doi.org](https://doi.org/10.1109/BIBM66473.2025.11356550?utm_source=openai)) | Which acquisition differences drive transfer failure? | Patient × device × electrode-condition holdouts | Device-stratified morphology and task performance; calibration |
| **Correlated-noise self-supervision** | Noisy-only approaches exist, but validity depends on noise and physiological assumptions | TP-informed learning and unpaired SC-CycleGAN. ([researchgate.net](https://www.researchgate.net/publication/388711199_Self-Supervised_Electrocardiograph_De-noising?utm_source=openai)) | When does noisy-only learning recover physiology rather than residual artifact? | Systematically vary temporal correlation, signal dependence, and reference-interval validity | Conditional bias, landmark errors, downstream performance |
| **Patient-identity preservation in unpaired restoration** | Unpaired real-noise learning reduces pairing requirements without automatically proving preservation of abnormal morphology | SC-CycleGAN’s unpaired construction. ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S095219762600179X?utm_source=openai)) | Can distribution translation avoid changing patient-specific abnormalities? | Controlled abnormality challenge set plus blinded natural-data evaluation | Abnormality retention, lead-specific features, false normalization |
| **Feature-calibrated uncertainty and abstention** | Uncertainty methods exist; clinical-feature calibration under external shift remains a residual question | Uncertainty-aware diffusion and joint quality/denoising work. ([pure.amsterdamumc.nl](https://pure.amsterdamumc.nl/en/publications/antithetic-sampling-enhanced-probabilistic-diffusion-for-denoisin/?utm_source=openai)) | Can the model identify unreliable ST/QT/timing reconstruction? | Held-out noise mechanisms and devices; calibrated rejection policy | Feature coverage, selective risk, missed failures, retained coverage |
| **Multi-lead restoration under shared corruption** | Multi-lead gains are demonstrated more directly than spatial diagnostic preservation | ML-CDAE. ([mdpi.com](https://www.mdpi.com/2624-6120/7/1/18?utm_source=openai)) | Can inter-lead redundancy help without transferring or erasing localized features? | Independent versus shared-electrode noise, dropout, localized pathology | Per-lead ST/QRS/T fidelity, diagnostic patterns, memory and latency |
| **Conditional auxiliary-sensor fusion** | Reference-assisted cancellation is effective in some conditions but variable | Per-electrode IMU and impedance studies. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC8450177/?utm_source=openai)) | When should an auxiliary reference be used, ignored, or trigger rejection? | Reference-quality gating with delay, dropout, and misleading-reference stress tests | Task utility, morphology, usable duration, total sensing energy |
| **Causal morphology-preserving edge denoising** | Embedded feasibility is established; unified clinical/latency/energy comparison remains fragmented | DSP and FPGA implementations. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/23367417/?utm_source=openai)) | What fidelity is achievable under fixed causal resource budgets? | Matched-hardware continuous-stream benchmark, including quantization and startup | Feature non-inferiority, tail latency, peak RAM, energy/hour |
| **Safe physiological and sparse priors** | Explicit priors and small-data learned optimization exist; behavior on unusual morphology requires targeted testing | Bayesian ECG model and FISTA-based dictionary learning. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/18075033/?utm_source=openai)) | Can interpretable priors improve efficiency without biasing unfamiliar beats? | Leave-morphology-out testing with prior-strength and adaptation ablations | Rare-feature retention, reconstruction bias, failure detection, compute |
| **Versioned, independently reproducible benchmarking** | Open code exists, but experimental-version and protocol differences complicate comparisons | DeepFilter’s separate experimental repositories and heterogeneous evaluation endpoints. ([github.com](https://github.com/fperdigon/DeepFilter?utm_source=openai)) | Which conclusions survive harmonized data, noise, tuning, and context? | Frozen manifests, independent reruns, equal tuning budgets, external hidden tests | Paired patient-level effects, reproducibility, morphology/task/resource trade-offs |


| RQ                                                           | Publication potential | Feasibility for you | Novelty potential | Main concern                                             |
| ------------------------------------------------------------ | --------------------- | ------------------- | ----------------- | -------------------------------------------------------- |
| **RQ2 — When does denoising help/hurt downstream analysis?** | **Very high**         | **Very high**       | **High**          | Need carefully chosen downstream tasks                   |
| **RQ5 — Can denoiser recognize unreliable reconstruction?**  | **Very high**         | High                | **Very high**     | Uncertainty methodology can become complicated           |
| **RQ3 — Synthetic-to-real / cross-device transfer**          | **Very high**         | Medium–High         | **Very high**     | Requires substantial real wearable data                  |
| **RQ8 — Causal, low-power streaming fidelity**               | **High–Very high**    | **High**            | High              | Hardware/deployment work must be genuinely rigorous      |
| **RQ1 — Morphology-constrained denoising across pathology**  | **High**              | Medium              | Medium–High       | Already a crowded research direction                     |
| **RQ7 — Auxiliary sensors**                                  | **High**              | Medium–High         | High              | Requires IMU/impedance synchronization and hardware work |
| **RQ6 — Multi-lead spatial preservation**                    | High                  | Low–Medium          | High              | Requires good 12-lead pathological data                  |
| **RQ4 — Validity of noisy-only denoising assumptions**       | High                  | Medium              | **Very high**     | More theoretical/methodological than your current setup  |
| **RQ9 — Harmonized benchmark/reproducibility**               | Medium–High           | High                | High              | Huge scope; contribution must go beyond benchmarking     |


# What would make this genuinely journal-level?

The key is that you should not make the main contribution another neural-network architecture.

Instead, your contribution becomes a decision framework.

For example:

Contribution 1 — Empirical finding

Establish that:

$$ \text{denoising benefit} \neq \text{monotonic function of noise removal} $$

and quantify regions where denoising is:

beneficial,
neutral,
harmful.

Your existing clean-signal result is extremely useful here.

Contribution 2 — Selective denoising

Develop:

$$ D(x)= \begin{cases} x, & Q(x)>\tau_1\\ f(x), & \tau_2<Q(x)\leq\tau_1\\ \text{abstain}, & Q(x)\leq\tau_2 \end{cases} $$

rather than applying \(f\) universally.

Contribution 3 — Feature-level safety

Instead of saying:

"The reconstructed waveform looks good."

measure:

QRS duration,
QT/QTc,
PR,
R timing,
P/T amplitudes,
ST deviation,
RR/HRV features.
Contribution 4 — Reliability

Estimate whether:

$$ |\Delta F| > \epsilon_F $$

for each feature \(F\).

Contribution 5 — Real wearable validation

Take the algorithm outside PhysioNet and put it through your actual acquisition chain.

Contribution 6 — Causal deployment

Measure:

RAM,
flash,
latency,
look-ahead,
energy,
sampling rate,
quantization effects.

That combination is substantially harder to dismiss as incremental.

What journal/conference level could this target?

If executed at the level above, I would consider the following tiers.

Ambitious

IEEE Transactions on Biomedical Engineering

The topic is squarely within its biomedical signal-processing and wearable-monitoring scope, but TBME explicitly expects major advances rather than incremental refinements.

Your work would therefore need:

rigorous experimental design,
real wearable validation,
strong statistical analysis,
clinically meaningful endpoints,
convincing generalization,
actual engineering contribution.
Very reasonable targets

IEEE Journal of Biomedical and Health Informatics

Particularly if the emphasis becomes:

trustworthy ECG preprocessing + downstream analysis + wearable data.

The fact that a recent JBHI paper on ECG denoising itself identifies cross-dataset robustness, realistic noise mixtures and computational efficiency as remaining practical gaps is encouraging for this direction.

Strong signal-processing target

Biomedical Signal Processing and Control

Especially suitable if the contribution emphasizes:

selective denoising,
morphology/feature fidelity,
signal-quality modeling,
artifact characterization.
Hardware-oriented

IEEE Transactions on Biomedical Circuits and Systems

This becomes more appropriate if your actual contribution substantially involves:

ECG AFE
+
acquisition
+
artifact sensing
+
embedded denoising
+
resource-aware implementation

rather than simply running a model on a microcontroller.

Conference route

IEEE EMBC / IEEE BioCAS

A very good route for an initial version of the system, particularly if you want to establish the hardware + algorithm concept before extending it into a journal paper.

My recommendation for your project

If I were structuring your research—not ECG denoising in general—I would choose:

Primary RQ

Under what signal-quality and artifact conditions does ECG denoising improve downstream analysis, and when can it instead introduce clinically relevant distortion?

That's your RQ2, sharpened.

Then add:

Secondary RQ

Can a denoising system identify when its reconstructed ECG is unreliable and selectively abstain from reconstruction?

That's RQ5.

And finally:

Deployment RQ

Can this selective denoising strategy preserve its reliability under causal, low-power wearable constraints?

That's RQ8.

Use RQ3 as the generalization experiment rather than necessarily making it a separate paper.

#3. RQ2 — When does denoising help/hurt downstream analysis?
Your RQ

Under which conditions does denoising improve downstream analysis relative to robust analysis of raw ECG?

Counterexample search: No direct counterexample found

This is where the strict test changes my confidence.

I found work demonstrating that denoising affects clinical interpretation. One study compared raw ECG with denoised ECG and found improved rhythm interpretation when clinicians were given the raw and denoised signals together.

I also found papers combining:

denoising,
signal-quality assessment,
noise localization,
downstream ECG analysis.

And recent work explicitly investigates whether denoising is even necessary for ECG reconstruction.

But I did not find a prior study that directly answers your broader conditional question:

$$ \text{When is} \quad \text{denoising} > \text{raw ECG} $$

versus

$$ \text{raw ECG} > \text{denoised ECG}? $$

Specifically, I did not find a study systematically varying:

noise severity,
artifact type,
downstream task,
raw vs denoised representation,
retrained vs frozen downstream models,

while explicitly identifying benefit / neutrality / harm regimes.

This is a crucial distinction.

A paper showing:

denoising improves arrhythmia classification

is not a counterexample.

A paper showing:

denoising improves clinician interpretation

is not a complete counterexample.

A paper showing:

denoising can distort morphology

is not a complete counterexample.

To kill RQ2, we would need something closer to:

"We systematically determine the conditions under which denoising versus raw ECG improves or harms downstream ECG analysis."

I did not find that.

Verdict

Novelty: 🟢 survives

Publication potential: 🟢 very high

This is now the strongest RQ under your counterexample criterion.

# RQ4 — Validity of noisy-only denoising assumptions
Your RQ

What assumptions make noisy-only ECG denoising valid under correlated artifacts?

Counterexample: partial

A 2025 self-supervised ECG denoising paper explicitly performs denoising without clean ECG supervision and uses the TP interval as a noise estimate.

That is a direct counterexample to the claim that noisy-only ECG denoising is unexplored.

However, it does not answer your deeper question:

Under what correlation/signal-dependence conditions is noisy-only learning valid?

The paper makes a structural assumption:

$$ x=y+s $$

and assumes noise can be estimated from TP intervals.

Your proposed experiment is different because it explicitly asks whether the assumptions fail when:

noise is temporally correlated,
noise is signal-dependent,
noise is bursty,
TP intervals aren't clean,
morphology varies,
artifact depends on activity.
So:

The methodological question survives.

But the broad statement:

"Noisy-only ECG denoising is an unexplored problem"

would be false.

Verdict

Novelty: 🟢 survives only in the assumption/validity-envelope formulation

Publication potential: high–very high

This is potentially one of the most fundamental RQs, but it is considerably harder than RQ2

# RQ5 — Unreliable reconstruction / uncertainty

This one requires the biggest correction.

Your RQ

Can a denoiser recognize when clinically relevant reconstruction is unreliable?

Counterexample: YES — multiple

A 2026 JBHI paper uses probabilistic diffusion specifically to stabilize uncertainty estimates during ECG/cardiac-signal denoising and produces time-resolved uncertainty maps aligned with physiological transitions.

Another 2026 study explicitly evaluates whether predictive uncertainty can be trusted for wearable ECG signal-quality assessment, including selective prediction and external distribution shift.

And a 2026 ECG reconstruction paper uses Monte Carlo dropout to estimate predictive uncertainty and reports correlations between uncertainty and reconstruction error.

Therefore the broad proposition:

"Can uncertainty tell us when ECG reconstruction is unreliable?"

has already been investigated.

This kills the novelty of RQ5 as currently phrased.

But there is still an interesting narrower question.

Your proposed RQ says:

feature-specific uncertainty is more useful for safe rejection than generic output variance/global quality.

That is much narrower.

For example:

$$ U_{QT}, U_{QRS}, U_{ST}, U_R $$

and evaluate:

$$ P(|\Delta QT|>\epsilon_{QT}\mid U_{QT}) $$

rather than merely:

$$ P(\text{bad ECG}\mid U). $$

I have not found a convincing counterexample for that exact formulation.

The recent uncertainty literature I found establishes:

uncertainty estimation,
uncertainty/error correlation,
selective prediction,
uncertainty under distribution shift.

It does not establish the exact feature-specific clinical reconstruction error → calibrated abstention framework you're proposing.

Verdict

Original RQ5 novelty: ❌ invalidated

Narrowed feature-specific selective-reconstruction RQ: 🟢 potentially novel

That is an important downgrade from my previous assessment.

# RQ8 — Causal, low-power streaming
Your RQ

What fidelity is achievable under genuinely causal, low-power streaming constraints?

Counterexample: YES to the broad deployment idea

This one also needs a correction.

Recent work already explicitly targets wearable ECG denoising under dynamic noise and low computational complexity. A 2026 DCPA-SNN paper is specifically framed as wearable ECG denoising under dynamic noise with low-complexity SNN processing.

Recent work also combines denoising, signal-quality assessment, pruning and quantization for real-time edge deployment.

And recent ECG-ARD work explicitly describes a causal decoder and a deployment-oriented evaluation protocol.

Therefore:

"Can ECG denoising be done causally and on low-power hardware?"

Novelty is killed.

But here's where your RQ can survive

Your actual question is about:

fidelity under an explicitly declared causal/resource budget.

That is a different question.

For example:

$$ \max \text{morphological fidelity} $$

subject to

$$ RAM \leq R $$ $$ Energy/hour \leq E $$ $$ Latency \leq L $$ $$ Lookahead = 0 $$

Then characterize the Pareto frontier between:

denoising benefit,
morphology distortion,
latency,
energy,
memory.

I have not found a direct counterexample that establishes such a frontier for ECG denoising.

Verdict

Broad RQ8 novelty: ❌

Resource-constrained fidelity-frontier formulation: 🟢 potentially novel

This is a major distinction.


## 
| RQ      | Direct counterexample to broad RQ?           | Broad RQ novelty survives? | Narrow version that may survive                                 |
| ------- | -------------------------------------------- | -------------------------- | --------------------------------------------------------------- |
| **RQ1** | **Yes**                                      | ❌                          | Pathology-specific non-inferiority / external morphology safety |
| **RQ2** | **No direct one found**                      | 🟢 **Yes**                 | Conditional benefit/harm regimes                                |
| **RQ3** | Partial                                      | 🟢 **Yes, narrowly**       | Which corruption assumptions transfer synthetic → real          |
| **RQ4** | Partial                                      | 🟢 **Yes, narrowly**       | Validity envelope under correlated/signal-dependent artifacts   |
| **RQ5** | **Yes**                                      | ❌                          | Feature-specific error-calibrated abstention                    |
| **RQ6** | **Yes for broad multi-lead preservation**    | ❌ broadly                  | Correlated artifact + spatial diagnostic non-inferiority        |
| **RQ7** | **Yes**                                      | ❌                          | Cost-aware sensor-selection / reference-quality gating          |
| **RQ8** | **Yes for broad low-power causal denoising** | ❌ broadly                  | Fidelity/resource Pareto frontier under strict causal budget    |
| **RQ9** | Partial                                      | 🟡                         | Which evaluation choices actually reverse denoising conclusions |


There is an even stronger version of RQ2

I would sharpen it to:

Under what combinations of artifact severity, artifact type, downstream task, and model adaptation does ECG denoising improve, leave unchanged, or degrade downstream analysis relative to direct analysis of the raw ECG?

This is important because it makes the novelty falsifiable.

Your hypotheses could be:

$$ H_1: \Delta_{\text{task}}>0 $$

for moderate/severe artifact,

$$ H_2: \Delta_{\text{task}}\approx0 $$

for some low-artifact conditions,

and

$$ H_3: \Delta_{\text{task}}<0 $$

for particular clean/mild-noise regimes.

That is much stronger than simply proposing a new denoiser.

And your existing result becomes extremely relevant

Your existing benchmark already has the preliminary observation that several learned denoisers can produce negative ΔSNR on already-clean wearable ECG, while the classical methods improved SNR.

That does not prove RQ2.

But it gives you a very good preliminary observation:

The effect of denoising is not necessarily monotonic with signal quality.

Then your research asks whether that phenomenon extends to:

QRS detection,
rhythm classification,
morphology measurements,
HRV,
pathological ECG,
different artifact types,
different denoisers,
different datasets.

That is a legitimate research program.

What I would now call genuinely "novel-capable"

Under your strict criterion, I would reduce the field to these:

🟢 Strongest surviving RQs

RQ2 — Conditional downstream benefit/harm

No direct counterexample found.

RQ3 — Synthetic corruption → real-device transfer

Broad transfer is not novel, but the specific corruption-model-to-transfer question survives.

RQ4 — Validity envelope of noisy-only learning

No direct counterexample found for the assumption/failure-boundary formulation.

🟡 Potentially novel only after narrowing

RQ5 — feature-specific uncertainty → error-calibrated abstention

Broad uncertainty-aware denoising is already done.

RQ8 — morphology fidelity under explicit causal resource constraints

Broad low-power causal denoising is already being done.

RQ9 — causal explanation of why denoising rankings change under harmonized evaluation

General reproducible benchmarking is already being done.

RQ6 — correlated-lead corruption and spatial diagnostic preservation

Broad multi-lead denoising is already done.

🔴 Broad RQ already has counterexamples

RQ1

RQ5 as originally phrased

RQ6 as originally phrased

RQ7 as originally phrased

RQ8 as originally phrased

One methodological warning

There is a subtle but important danger in this exercise.

"I found no counterexample" does not prove novelty.

It means:

After searching the relevant literature, I did not find a study that directly answers the same question.

That is evidence supporting a novelty claim, not proof of novelty.

To make the eventual paper defensible, you'd want a formal novelty matrix where every candidate RQ is decomposed into:

$$ \text{Question} = \{ \text{population}, \text{artifact}, \text{intervention}, \text{comparison}, \text{outcome}, \text{generalization condition} \} $$

and every apparently similar paper is checked against those dimensions.

That is much stronger than title/abstract similarity.

Based on that stricter standard, my current conclusion is:
$$ \boxed{\textbf{RQ2 is the safest genuinely novel research question in your list.}} $$

And the most interesting complementary direction is:

$$ \boxed{ \textbf{RQ2 + RQ3 + a narrowly defined RQ5/RQ8} } $$

—not because those three are individually all novel, but because RQ2 provides the surviving scientific question, while RQ3 and a carefully narrowed RQ5/RQ8 can supply the generalization, reliability, and deployment dimensions without making unsupported novelty claims.