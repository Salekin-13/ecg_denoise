# ECG Denoising: An Evidence-Audited Research Landscape, Adversarial Gap Verification, and Reconciliation with a Second-LLM Review (literature to September 2026)

The field's open problem is no longer how to suppress ECG noise. It is knowing when restoration keeps clinically meaningful information, for which task, under which real acquisition shift, and when an output should not be trusted. Most of the attached review's gap map survives verification, but its headline "safest genuinely novel" research question (RQ2: when denoising helps, is neutral or harms downstream analysis) is only partly novel. Published work already shows four things:
- severity-dependent help and harm (Seo et al., Sensors 2026, doi 10.3390/s26165183);
- downstream harm (Granese, Fall, Lence, Salem, Zucker and Prifti, "The Negative Impact of Denoising on Automated Classification of Electrocardiograms", DGM4H Workshop, NeurIPS 2023);
- only small losses for raw-ECG deep models on noisy input (Bender et al., Stud Health Technol Inform 302:977–981, doi 10.3233/SHTI230321);
- preprocessing that hurts CNN classifiers ("Architecture-Specific Impact of Preprocessing on Machine Learning Models for ECG Classification", Stud Health Technol Inform 2026, doi 10.3233/SHTI260227: "convolutional neural networks performed best when raw, unnormalized electrocardiograms are used").

What remains open is the full factorial map on naturally noisy data, including how the downstream model is adapted.

## TL;DR

- **Where the field stands.**
  - ECG denoising is dense and mature for baseline wander and mains interference. It is also mature for supervised deep models trained on QT/MIT-BIH ECG plus added NSTDB noise.
  - In that "semi-synthetic" setting (real clean ECG plus separately recorded real noise), SNR, RMSE and PRD dominate evaluation.
  - Several apparent "modern gaps" already have counterexamples: unpaired real-noise training (Operational Cycle-GANs, 2022); leakage-aware out-of-distribution testing (ECG-ARD, JBHI 2026; TFCDiff on SimEMG); uncertainty-aware diffusion (AV-cDDPM, 2026); SNN low-energy denoising (DCPA-SNN, 2026); and joint denoising/quality/localisation with compression (Sensors 2025).
- **Gaps that survive adversarial search are not architectural:**
  - target validity (the "clean" references are themselves filtered or package-denoised);
  - transfer to natural artifacts and other devices;
  - feature-level (QT/ST/P-wave) preservation under shift;
  - error-calibrated, feature-specific abstention;
  - measured, like-for-like fidelity-vs-latency/RAM/energy trade-offs for causal denoisers;
  - a factorial map of when denoising helps or harms downstream analysis.
- **What to do.** Build a PhD around three pieces, and treat architecture choice as secondary:
  - a leakage-free three-track benchmark (synthetic; semi-synthetic NSTDB with noise-channel separation; natural: SimEMG, BUT QDB, own wearable recordings);
  - a factorial help/harm study (severity × artifact × task × frozen/retrained/joint downstream model) that includes a clean-input "do-no-harm" test;
  - a quality-gated selective-denoising model with feature-specific abstention and measured on-device cost.

Evidence labels:

| Label | Meaning |
|---|---|
| [E] | Directly demonstrated in a primary study |
| [A] | Author claim |
| [P] | Pattern across multiple studies |
| [I] | My cross-paper inference |
| [L] | Claim from the attached LLM review |

---

## 1. Executive synthesis

**Methodological families.**
- Fixed and notch filtering.
- Adaptive and reference-based cancellation (LMS/NLMS/RLS; IMU- or reference-assisted).
- Model-based estimation (EKF/EKS on an ECG dynamical model, Sameni et al. 2007).
- Multiresolution shrinkage (DWT thresholding; wavelet–Wiener).
- Adaptive decomposition (EMD/EEMD/VMD, often with NLM).
- Sparse, low-rank and optimisation methods (dictionaries, group sparsity, total variation).
- Source separation (ICA, including online recursive ICA).
- Discriminative deep regression (RNN, FCN-DAE, U-Net, attention/transformer, Mamba).
- Generative restoration (GAN/CycleGAN, conditional score/diffusion).
- Noisy-only/self-supervised and multitask pipelines (denoising + signal quality assessment + noise localisation).
- Low-power families (SNNs, pruned/quantised networks, FPGA).

**Dominant assumptions [P].**
1. Noise is additive and independent of the ECG.
2. The "clean" reference is clean.
3. NSTDB's three records (bw, ma, em) represent real artifacts.
4. Better SNR/RMSE/PRD implies preserved diagnostic content.
5. Offline window-level evaluation implies deployability.

**Major evidence patterns.**
- **[P] Semi-synthetic benchmarks dominate.** DeepFilter, DeScoD-ECG, FGDAE (QTDB with randomly mixed NSTDB artifacts), DCPA-SNN (MIT-BIH + NSTDB at −6 to 4 dB), the Sensors 2026 image-encoding framework, ECA-Net-CycleGAN and a multi-scale transformer (arXiv 2407.11065) all use the QTDB/MIT-BIH + NSTDB template.\[1\]\[2\]\[3\]\[4\]\[5\]\[6\]
- **[E] Signal and task/feature metrics diverge.**
  - Denoising degraded torsade-de-pointes risk classifiers by up to 40 percentage points of accuracy (Granese et al., 2023).\[7\]
  - In a canine delineation preprint, classical filters sometimes scored higher on denoising metrics without better delineation (arXiv 2605.03183).\[8\]
  - A learned denoiser gave negative SNR improvement (about −3.93 to −4.09 dB) and lower P-wave correlation on lightly contaminated 12 dB input (Seo et al., Sensors 2026).\[5\]
- **[E] Natural-artifact evaluation exists but is thin.**
  - SimEMG (Atanasoski et al., IEEE OJEMB 2023) provides simultaneously recorded clean and EMG-contaminated ECG. TFCDiff and ECG-ARD use it for out-of-distribution (OOD) testing.
  - Real upper-arm EMG recordings were used in arXiv 2607.11450.
  - Armband ECG with muscle artifact was used by Hossain, Bashar, Lazaro et al. (Chon lab, UConn), "A Robust ECG Denoising Technique Using Variable Frequency Complex Demodulation", Comput Methods Programs Biomed 200:105856 (2021), doi 10.1016/j.cmpb.2020.105856.
- **[P] Deployment claims mix quantities that cannot be compared:**
  - Raspberry Pi latency of 1.41 s per 14-s segment (arXiv 2511.12478);
  - FPGA utilisation of 5% logic elements and 6% registers (Symmetry 2026);
  - spike-count energy estimates (DCPA-SNN);
  - "moderate latency per 10-s segment" (ECG-ARD).\[9\]

**Central unresolved issues [I; evidence chains in §11].**
1. **Target validity.** A self-supervised study evaluated against package-denoised signals re-noised with Gaussian noise. QTDB was curated to avoid artifacts but is not artifact-free. Filtered PTB-XL is used as a target.
2. Transfer from semi-synthetic to natural acquisition, and across devices.
3. ST/QT/P-wave and rhythm preservation under that transfer.
4. **Recoverability:** knowing, per feature, when not to trust a reconstruction.
5. Measured deployment trade-offs.

---

## 2. Evolution of ECG denoising

| Era | Principle | Representative evidence retrieved | Key shift |
|---|---|---|---|
| Classical (1970s–1990s) | Fixed high/low-pass, notch, spline baseline | A comparison of nine baseline methods found an FIR with 0.67 Hz cut-off best on real signals (arXiv 1807.11359).\[10\] The attached review's 1991 ST-preserving study was not verified from the retrieved evidence. | Baseline removal recognised to distort ST\[11\] |
| Adaptive / model-based (1990s–2010s) | LMS/NLMS/RLS; EKF on a dynamical ECG model | Sameni et al. 2007 EKF/EKS (reused in the ime-luebeck toolkit); online recursive ICA (2024)\[12\]\[13\] | Explicit priors on ECG dynamics |
| Decomposition / sparse (2000s–2020s) | Wavelet shrinkage, wavelet–Wiener, EMD/VMD, NLM, group sparsity, TV | EMD–NLM hybrid on MIT-BIH + NSTDB (PMC11064874);\[14\] wavelet-domain group sparsity (BSPC 2023);\[14\]\[15\] group-sparse baseline estimation (IEEE Access 2021) | Hybridisation predates deep learning |
| Deep discriminative (2018–2023) | Supervised noisy→clean regression | Antczak 2018 (preprint); Chiang et al. 2019 FCN-DAE (IEEE Access 7:60806);\[8\]\[16\] DeepFilter (BSPC 70:102992); CBAM-DAE (BSPC 2023); lightweight U-Net with noise localisation (BSPC 88:105504, 2024) | NSTDB-added noise becomes the standard |
| Generative (2020–2025) | GAN/CGAN/CycleGAN; score/diffusion | Singh & Pradhan GAN (TCBB 2020); CGAN (JBHI 26(7), 2022);\[17\] DeScoD-ECG (JBHI; citing lists say 2023, the attached review says 2024); diffusion with pruning (Comput Biol Med 193, 2025);\[15\] TFCDiff (arXiv 2511.16627, preprint) | Stochastic restoration |
| Noisy-only / unpaired / multitask (2022–2026) | No paired clean target; auxiliary tasks | Operational Cycle-GANs for real wearable ECG (arXiv 2202.00589); TP-interval self-supervision (bioRxiv 2024); multitask localisation + SQA + denoising (Sensors 2025, PMC12693763)\[18\]\[19\]\[20\] | Target construction becomes the key assumption |
| Deployment / emerging (2024–2026) | SNN, compression, FPGA, causal, uncertainty | DCPA-SNN (Sensors 2026); DWT–ADTF FPGA (Symmetry 2026); ECG-ARD causal decoder (JBHI 2026);\[21\] AV-cDDPM uncertainty maps (2026)\[1\]\[22\]\[23\] | Reliability and resource budgets enter the objective |

[I] Across these eras, the target-construction and evaluation assumptions change more than the architecture does. Mamba, attention and diffusion sit inside the same supervised regression-on-NSTDB paradigm. The real shifts are away from paired clean targets and toward task-, feature- and uncertainty-level evaluation.

---

## 3. Comprehensive taxonomy

**A. Noise/source.**
- Baseline wander (bw).
- Power-line interference.
- EMG/muscle (NSTDB "ma"; MA, EMG and "muscle" are used inconsistently).
- Electrode motion (em). Per the PhysioNet NSTDB v1.0.0 page, "Electrode motion artifact is generally considered the most troublesome, since it can mimic the appearance of ectopic beats and cannot be removed easily by simple filters".
- Broader motion artifact (dry/textile contact changes).
- Instrumentation.
- Mixed/composite (random NSTDB mixtures, as in FGDAE).
- Physiological/environmental: CPR artifacts before AED shock advisory; intermittent contact in cockpit "invisible ECG" (Biosensors 2026).

**B. Paradigm.** Deterministic → model-based (Wiener, EKF) → adaptive (LMS/RLS, reference/IMU) → decomposition (DWT, EMD/VMD) → sparse/low-rank/optimisation → machine learning → deep discriminative → generative → self-supervised/unpaired → hybrid (DWT+CNN+TV; wavelet-guided attention; physics-aware losses) → emerging (SNN, causal autoregressive, uncertainty-aware diffusion).

**C. Representation.**
- Time.
- Frequency (DCT in TFCDiff).
- Wavelet (wavelet layer in a CNN, arXiv 2501.06724).
- Latent (vector-quantised bottleneck in ECG-ARD).
- Multiresolution.
- Multi-lead/spatial (multichannel fetal-ECG adversarial denoising, PMC10774433).

**D. Learning regime.**
- Supervised (dominant).
- Self-supervised (TP-interval).
- Unpaired adversarial (Operational Cycle-GAN).
- Weakly supervised (multitask Transformer).
- Transfer/domain adaptation (sparse for ECG denoising; better developed in PPG, e.g. arXiv 2604.17480).
- Personalised/federated (search lead only).

**E. Target construction.**
- Paired simultaneous recording (SimEMG).
- Real ECG + recorded real noise (NSTDB, semi-synthetic).
- Real ECG + synthetic noise.
- Simulated ECG + modelled noise (Lenis et al.).
- Filtered or package-denoised ECG treated as clean.
- Unpaired distributions.
- Noisy-only (TP-interval).
- Masked/consistency objectives.
- (clean, clean) identity pairs teaching "do no harm" (arXiv 2605.03183).

**F. Temporal/context.**
- Beat-level (criticised in TFCDiff).
- Fixed window (1024 samples; 10 s).
- Long context (Mamba).
- Recurrent, convolutional, attention, multiscale.
- Causal vs bidirectional. ECG-ARD's causal decoder still conditions on the fully observed noisy segment, so it is not zero look-ahead [I].\[21\]

**G. Morphology strategy.**
- Implicit (MSE).
- Explicit losses: Seo et al. (MSE + derivative MSE + centre-window MSE); DCPA-SNN (physics-aware multi-domain loss); FGDAE (multi-component loss).
- Landmark preservation.
- Task preservation.
- Physiology-informed (PINN in arXiv 2607.11450).
- None reported.

**H. Evaluation level.**

| Level | What is evaluated | Examples |
|---|---|---|
| L0 | None | — |
| L1 | Visual | — |
| L2 | SNR/RMSE/PRD/correlation | Most deep papers |
| L3 | Features | ST in Lenis et al.; R-peak/P-wave in Seo et al. |
| L4 | Tasks | QRS detection in DCPA-SNN; classification in Granese et al.; delineation in the canine preprint |
| L5 | Clinician interpretation | PMC11417490 |

**I. Deployment.**
- Offline (most work).
- Real-time claims (often unmeasured).
- Streaming/causal (ECG-ARD decoder; online ICA).
- Wearable (armband, upper-arm, textile).
- Single-board (Raspberry Pi 4).
- MCU/µNPU (adjacent classification work: PhysioLite on MAX78000/Himax WE2, sub-~20 ms).
- FPGA.
- Low power (SNN energy estimates).

**Intersections.**
- Wavelet × deep.
- Diffusion × uncertainty (AV-cDDPM).
- Denoising × SQA × localisation (PMC12693763).
- Unpaired × real wearable (Operational Cycle-GAN).
- Causal × leakage-aware protocol (ECG-ARD).

---

## 4. Research-landscape matrix

| Direction | Representative methods | Maturity | Typical data/noise | Evaluation | Strengths | Recurrent limitations | Under-explored aspects |
|---|---|---|---|---|---|---|---|
| Baseline/mains suppression | Butterworth, FIR 0.67 Hz, notch, spline, wavelet | Extensively studied | Simulated/real ECG + bw | ST deviation (Lenis 2017; 289-ECG spline study) | Cheap, causal-capable | All methods alter ST somewhat\[24\] | ST/QT under natural motion |
| Reference/IMU cancellation | NLMS/RLS, multi-reference NLMS | Established but fragmented | Custom acquisitions | SNR, QRS | Physical reference | Small cohorts ([L]; not verified) | Reference-quality gating |
| Model-based Bayesian | EKF/EKS/UKF | Established but fragmented | Normal ECG + real muscle noise | SNR, morphology | Interpretable priors | Abnormal beats [I] | Pathology-robust priors |
| Wavelet/multiresolution | DWT shrinkage, wavelet–Wiener, DWT–ADTF | Extensively studied | MIT-BIH + NSTDB; real upper-arm | SNR, RMSE, PPSNR | Strong suppression; hardware-friendly | Often untuned as baseline (~1 dB SNR in arXiv 2407.11065)\[4\] | Fair tuning protocols |
| Adaptive decomposition | EMD/EEMD/VMD ± NLM | Established but fragmented | MIT-BIH + NSTDB, 0–10 dB\[14\] | SNR/RMSE/PRD/SSIM\[14\] | Data-adaptive | Mode mixing; cost | Streaming variants |
| Sparse/low-rank | Dictionary, group sparsity, TV | Moderately studied | Semi-synthetic | Signal metrics | Small-data, interpretable | Few natural-data tests | Sparse methods on wearable data |
| Discriminative deep | FCN-DAE, U-Net, CBAM-DAE, FGDAE, Mamba, transformers | Extensively studied within constructed benchmarks | QTDB/MIT-BIH + NSTDB | Signal metrics; some R-peak/classification | High in-distribution fidelity | Noise reuse; clean-input harm (Seo 2026) | Natural-noise/device transfer |
| Generative restoration | CGAN, CycleGAN, DeScoD, TFCDiff, AV-cDDPM, ECG-ARD | Emerging | QTDB + NSTDB; SimEMG OOD | Signal metrics; variance maps | Multi-modal outputs; OOD tests | Cost; hallucination; variance ≠ calibration | Calibrated feature uncertainty |
| Noisy-only / unpaired | TP-interval; Operational Cycle-GAN | Emerging | Tianchi; real wearable | PSNR vs package-denoised reference | No paired target | Target validity | Correlated artifacts |
| Multitask denoise+SQA | Multitask Transformer; lightweight U-Net | Emerging | Wearable, weak labels | F1, SNR | Aligns with usability | Limited external tests | Error-calibrated abstention |
| Multi-lead | Multichannel adversarial fetal ECG | Moderately studied (structural); emerging (neural 12-lead) | Synthetic/real fetal ECG | SNR, QRS detection | Spatial redundancy | Correlated-lead corruption rarely tested | Lead-specific ST preservation |
| Embedded/low-power | SNN, FPGA DWT, TFLite, pruning | Established but fragmented | Semi-synthetic | Latency, utilisation, estimated energy | Hardware evidence exists | Incommensurable metrics | Measured causal Pareto |

---

## 5. Major methodological directions

**5.1 Fixed filtering and baseline removal.** Maturity: extensively studied.
- Lenis et al. (2017) simulated 5.5 million signals from 765 electrophysiological setups [E].
  - Wavelet-based cancellation was most accurate. Yet "for medical applications, the Butterworth high-pass filter is the better choice because it is computationally cheap and almost as accurate".
  - All methods modified ST to some extent, but all were better than leaving baseline wander unfiltered.
- A companion study of 289 simulated ischemic 12-lead ECGs found cubic-spline interpolation best. It altered ST by 0.10 ± 0.06 mV at elevated K points [E].
- Limitation: the ground truth is simulated.

**5.2 Adaptive/reference and model-based.** Maturity: established but fragmented.
- EKF/EKS (Sameni et al., 2007) and online recursive ICA are real-time-capable.\[12\]\[13\]
- The IMU-assisted NLMS paper and the 2012 DSP study cited by the attached review were not independently verified.

**5.3 Wavelet/decomposition/sparse.** These methods are strong when tuned.
- Only one retrieved comparison uses natural acquisitions: upper-arm ECG under relaxed and voluntary contraction (arXiv 2607.11450, preprint). It found that "DL methods achieve superior morphological reconstruction, while DWT provides the strongest noise suppression" [E].
- The DWT–ADTF FPGA uses about 5% of logic elements and 6% of registers [E]. The attached review's 1.09 ms and 426 mW figures were not verified.

**5.4 Discriminative deep denoisers.**
- FGDAE reports best results on all seven error metrics, with a 61–73% model-size reduction versus the prior state of the art [A].
- Seo et al. (Sensors 2026, doi 10.3390/s26165183) mixed NSTDB bw/em/ma at −12, −6, 6 and 12 dB. They report that "the autoencoder achieved an SNR improvement of 5.63 dB and a correlation coefficient of 0.801" [E].
- TFCDiff raises three criticisms of earlier work [A]:
  - DeepFilter, DeScoD and IDPM train on baseline wander only;
  - other models train noise types separately or with fixed equal weights;
  - most models denoise single beats, which distorts RR intervals when beats are concatenated.

**5.5 Generative restoration.** Maturity: emerging.
- **TFCDiff** (preprint) applies DCT-domain diffusion to raw 10-s segments [A].
  - It is tested across datasets on SimEMG (15 healthy volunteers) and on AF/PVC segments.
  - On AF/PVC, "extreme noise intensities induce distortions in fine pathological features such as fibrillatory waves".
- **AV-cDDPM** uses antithetic sampling on more than 6,000 ventricular electrogram samples from over 50 patients, plus QTDB+NSTDB [A].
  - Reported results: MAP RMSE 3.32×10⁻³, PCC 0.978, ECG cosine similarity 0.926.
  - It also reports "time-resolved uncertainty maps aligned with physiological transitions".
- **ECG-ARD** (JBHI 2026) is autoregressive, with a causal decoder [A].
  - Its protocol is leakage-aware: record-wise splits, NSTDB channel separation, noisy-only normalisation.
  - It was tested OOD on SimEMG, with "moderate inference latency".
  - Parameter count, latency values and downstream tasks were not verified (abstract-level access only).

**5.6 Noisy-only/unpaired learning.** Maturity: emerging.
- **Liu et al., TP-interval self-supervision** (bioRxiv 2024, preprint). The method treats the TP interval as pure noise and trains a 1D U-Net segmenter on about 100 annotated samples.
  - For evaluation, "we first de-noised the ECG signals by using the package [49], and regard the de-noised signals as the clean data. Then we add the Gaussian noises" [E].
  - This is a direct target-validity problem.
- **Operational Cycle-GANs** (2022) argue that supervised synthetic-noise denoisers "will fail to restore any actual ECG signal from a wearable device corrupted with a blend of artifacts" [A].

**5.7 Multitask and quality-aware pipelines.** Maturity: emerging.
- The Sensors 2025 multitask Transformer (PMC12693763) links noise localisation, SQA and denoising under weak supervision [A].
  - It reports F1 of 95.72–98.49% and SNR improving from −1.95 ± 3.83 dB to 12.20 ± 2.51 dB, with pruning/quantisation.
- A long-term SNR-curve method (IEEE TBME 2020) defines three usability tiers: full-wave analysis, QRS-only, and unsuitable [A]. It is a direct antecedent of conditional processing.

**5.8 Low-power/embedded.** Maturity: established but fragmented.
- **DCPA-SNN** (Sensors 2026, 26(15):4695) [E/A]:
  - mixed-noise denoised SNR 5.80 dB and SNR improvement 6.80 dB;
  - R-peak detection rate from 90.71% to 95.72%;
  - energy is estimated from spike activity, not measured;
  - the authors plan "real-world validation … during diverse daily activities" [A].
- A lightweight autoencoder runs on Raspberry Pi 4 (float16 TFLite) at 1.41 s per 14-s segment (arXiv 2511.12478, preprint) [A].\[25\]

---

## 6. Evidence-quality and evaluation audit

### 6.0 Condensed evidence ledger

| Study | Data / noise | Target / split | Morph. level | Downstream | Key demonstrated result | Reviewer limitation | Strength |
|---|---|---|---|---|---|---|---|
| Lenis 2017 (journal) | Simulated ischemic ECG + modelled bw | Simulated truth | L3 (ST) | — | Wavelet best; Butterworth nearly as accurate; all alter ST\[24\] | Simulation only | High (bw/ST) |
| Granese 2023 (workshop) | Clinical TdP-risk ECG | Pretrained denoisers | — | L4 | Accuracy −40 pp; AUROC −27 pp with misclassification detection\[7\] | Workshop; denoisers trained elsewhere | Moderate |
| Seo, Sensors 2026 | MIT-BIH + NSTDB bw/em/ma, −12 to 12 dB | Paired; record-disjoint 33/7/8 | L2–L3 | Classifiers trained on denoised input only | Gains at −12 dB; harm at 12 dB (P-wave corr. 0.89–0.99 → 0.62–0.65)\[5\] | 8 test records; no raw-vs-denoised classifier arm | Moderate |
| DCPA-SNN, Sensors 2026 | MIT-BIH + NSTDB, −6 to 4 dB | Paired | L2 | L4 R-peak | 90.71% → 95.72% | No natural data; estimated energy | Moderate |
| ECG-ARD, JBHI 2026 | MITDB, QTDB; SimEMG OOD | Record-wise; noise-channel separation\[21\] | L2 | NR | OOD robustness claimed | Abstract only | Moderate |
| AV-cDDPM 2026 | MAP (>50 patients) + QTDB/NSTDB | Paired | L2–L3 | — | Uncertainty maps\[22\] | Variance not calibrated to feature error | Moderate |
| Liu (bioRxiv 2024) | Tianchi 12-lead, 500 Hz | Noisy-only; random 80:20 | L2 | L4 benefit | Classification improved\[18\] | Circular target; Gaussian test noise | Low |
| arXiv 2607.11450 | Real upper-arm EMG | Real acquisition | L2 | — | DWT best suppression; DL best morphology\[26\] | Preprint; small | Moderate |
| PMC11417490 | Real noisy ECG | — | L5 | Rhythm reading | Combined view: accuracy 75.7% → 80.6% (P = 0.0087); undiagnosable 14.2% → 4.5%\[27\] | Combined, not denoised-only | Moderate |
| Bender 2023 (Stud Health Technol Inform 302:977–981) | PTB-XL natural noise labels | Frozen pretrained Ribeiro et al. ResNet (trained on >2 million ECGs); no denoising | — | L4 AF | "False positive and false negative rates are slightly worse for data being labelled as noisy" | No denoising arm | Moderate |

NR = not reported or not verified.

### 6.1 Target construction [P, E]

1. **Filtered-as-clean.**
   - The TP-interval study's reference is package-denoised ECG plus Gaussian noise [E].\[28\]
   - PTB-XL contains substantial natural noise: a PTB-XL-derived dataset removed 4,566 records (20.9%) for baseline-drift or static-noise flags [E].\[29\]
   - QTDB was curated to avoid artifacts but not certified noise-free [L].
2. **Semi-synthetic additivity.**
   - NSTDB artifacts are real recordings, but mixing is digital and additive.
   - The few noise realisations are reused across train and test unless deliberately separated.
   - ECG-ARD introduced "NSTDB channel separation to reduce reuse of noise realizations" [A], which confirms that reuse is a recognised leakage path.
3. **Genuinely paired natural data** is rare. SimEMG (shoulder vs hand electrodes; EMG only; healthy volunteers) is the retrieved example.
4. **Identity pairs** ((clean, clean) training, canine preprint) are simple and rarely reported [I].
5. **Simulation truth** (Lenis) gives exact ST ground truth but not natural noise.

[I] Target validity is independent of architecture. A denoiser that exactly reproduces a filtered target inherits that filter's ST/QT distortion. Reported fidelity then measures agreement with the filter, not with physiology.

### 6.2 Synthetic vs natural noise

[P] Semi-synthetic NSTDB mixtures dominate. Natural-artifact tests found:
- SimEMG (OOD in TFCDiff and ECG-ARD);
- upper-arm recordings (2607.11450);
- armband muscle artifact (PMC7920915, evaluated by QRS detection);
- real wearable data (Operational Cycle-GAN).

[I] No natural electrode-motion artifact with a simultaneous clean reference was found.

### 6.3 Generalisation axes

| Axis | Demonstrated by | Status |
|---|---|---|
| Subject | Seo (record-disjoint); ECG-ARD (record-wise) | Partially standard; Seo documents correcting an earlier patient-overlap error [A]\[5\]\[30\] |
| Dataset | ECG-ARD, TFCDiff on SimEMG | Emerging |
| Noise source | ECG-ARD channel separation | Rare |
| Device | No controlled denoising experiment found | Gap (evidence absence) |
| Natural artifact | 2607.11450; SimEMG; armband | Sparse |

Adjacent work: generalisation of ECG noise *detection* across sources and noise types was studied (arXiv 2502.14522), but restoration was not.

### 6.4 Morphology

- **Level-3 evidence exists:**
  - ST (Lenis; spline);
  - R-peak amplitude and P-wave correlation (Seo);
  - repolarisation markers in MAPs (AV-cDDPM);
  - J-point/landmark assessment in the IRM EMG study (existence corroborated; details not verified).
- [P] Most deep papers stop at Level 2.
- [E] Levels 2 and 3 can diverge. In Seo et al., pooled P-wave correlation fell from 0.647 to 0.535 while R-peak error improved. The authors call the P/QRS measures "direction-inconsistent" across partitions.
- QT/QTc preservation under natural noise was not found.

### 6.5 Downstream and clinical tasks

- **Harm:** Granese 2023.
- **Help:**
  - DCPA-SNN (R-peak detection);
  - Liu (classification);
  - TFCDiff (wearable F1);
  - fetal multichannel GAN (QRS detection errors halved; input SNR −30 to 0 dB; average 20 dB gain);
  - clinician combined view.
- **Neutral/not needed:**
  - Bender 2023 (frozen AF ResNet on PTB-XL; static-noise accuracy 94.6% vs 96.8 ± 0.7% for clean controls).
  - "Architecture-Specific Impact of Preprocessing on Machine Learning Models for ECG Classification" (Stud Health Technol Inform 2026, doi 10.3233/SHTI260227) tested 24 preprocessing combinations × 6 architectures on PTB-XL. It found that "convolutional neural networks performed best when raw, unnormalized electrocardiograms are used, in direct contradiction to prevailing assumptions".
- **Evaluation practice:** Wang et al. 2023 (AI 2023, LNAI 14471) argued that "explicit evaluation may be insufficient and implicit metrics need to be considered".

### 6.6 Computational evaluation [P]

The reported quantities rarely match across papers:

| Reported quantity | Example |
|---|---|
| Single-board latency | 1.41 s per 14-s segment (Raspberry Pi) |
| FPGA utilisation | 5% logic elements, 6% registers |
| Parameter count | 15,554,085 for Seo's classifier, not the denoiser |
| Energy | Spike-based estimates (SNN) |

Adjacent MCU work (classification and detection, not denoising) does report measured costs:
- per-inference energy: an AF classifier at 143 ms and 3532 µJ (PMC12608751);
- peak RAM: noise detection within 30 KB on Cortex-M4 (arXiv 2112.07901).

Measured MCU energy and peak RAM for a *denoiser* were not found.

---

## 7. Under-explored directions

| Direction | Evidence | Counterexamples | Confidence under-explored |
|---|---|---|---|
| Natural-artifact × device transfer | No controlled cross-device study; SimEMG EMG-only | Operational Cycle-GAN; 2607.11450 | Moderate–high |
| QT/ST/P preservation under natural noise | Level-3 evidence simulated/semi-synthetic | Lenis; Seo | Moderate |
| Error-calibrated feature abstention | AV-cDDPM variance only | CPR cascade "indeterminate"; PPG uncertainty subset (2604.17480); TBME 2020 tiers\[31\]\[32\] | Moderate |
| Clean-input do-no-harm | Seo 12 dB harm | Canine (clean, clean) training | Moderate–high |
| Measured causal Pareto | Incommensurable reporting | DCPA-SNN, FPGA, Raspberry Pi | Moderate |
| Noisy-only under correlated artifacts | TP-interval assumes stationary additive noise\[33\] | EEG iPSD; Speckle2Self (adjacent)\[34\]\[35\] | Moderate |
| Correlated multi-lead × localised pathology | Not found | Fetal multichannel GAN | Low–moderate |
| Federated/personalised restoration | Not searched in depth | — | Search lead only |

---

## 8. Unresolved research gaps

| Area | Status | Detail |
|---|---|---|
| Methodology | Partially addressed | Joint denoise→task optimisation exists (CS-TRANS; multitask), but task-tuned restoration creates a second validation problem [I]. "New architecture for NSTDB" is not a gap. |
| Data | Confirmed gap | Paired natural data beyond EMG, and pathology-rich paired data. |
| Noise | Confirmed gap | Noise-source independence, and artifact diversity beyond three NSTDB records [P]. |
| Target validity | Confirmed gap | Filtered/package-denoised targets; no audit standard. |
| Generalisation | Partially addressed (datasets); confirmed gap (devices) | Datasets: SimEMG OOD tests. Devices: no controlled cross-device testing (moderate confidence; based on evidence absence). |
| Evaluation | Confirmed gap | Metric heterogeneity and untuned classical baselines [I]. |
| Morphology | Partially addressed | ST (simulation), P/R (semi-synthetic); QT/QTc under natural noise not found. |
| Clinical validity | Partially addressed | One clinician study (combined view); Granese harm; no prospective validation retrieved. |
| Computational constraints | Partially addressed | No measured MCU energy or peak RAM for denoisers. |
| Deployment | Partially addressed | Look-ahead rarely quantified [I]. |
| Reproducibility | Partially addressed | DeepFilter keeps separate preprint and journal repositories ([L]; not re-verified). An independent GitHub benchmark (pskeffington/ECG-denoising) adds freeze and morphology-review protocols but is not peer-reviewed. Seo publicly corrected leakage.\[2\]\[5\] How common leakage is remains unquantified. |

---

## 9. Future directions explicitly proposed by researchers

| Proposal (author) | Subsequent evidence | Status |
|---|---|---|
| Repeated: real-world wearable validation during daily activities (DCPA-SNN; others per [L])\[36\] | 2607.11450; Operational Cycle-GAN | Unresolved at scale |
| Repeated: faster diffusion and uncertainty quantification (EMBC 2025 cDDPM authors)\[37\] | AV-cDDPM (2026) | Investigated; calibration unresolved |
| Isolated: "perform the still-missing downstream denoising ablation under a fixed classifier" (Seo 2026)\[5\] | None found | Unresolved |
| Isolated: morphology constraints for spike-like residuals (DCPA-SNN)\[36\] | — | Unresolved |
| Isolated: implicit/downstream evaluation (Wang 2023; Granese 2023)\[7\]\[38\] | Canine preprint 2026; Seo 2026 | Partially investigated |
| Isolated: AED deployment "would require additional model optimization" (CPR cascade)\[39\] | — | Unresolved |
| Reduce paired-target dependence (multiple groups) | TP-interval; Cycle-GAN | Investigated; validity unresolved |

---

## 10. Cross-paper synthesis — model-derived inference

All items are [I] inferences, not author claims.

1. **The target hides the key assumption.** The reference (filtered PTB-XL, curated QTDB, package-denoised Tianchi) defines what "fidelity" means.
2. **Noise-source independence is a separate axis from subject independence.** Subject-disjoint splits that reuse NSTDB noise realisations still leak artifact identity, as ECG-ARD's protocol change implies.
3. **Whether denoising helps or harms depends on severity and on how the downstream model is adapted.**
   - Severity: Seo found gains at −12 dB and harm at 12 dB.
   - Adaptation: Granese fed denoised data to raw-trained classifiers; Bender's raw models were already robust.
   - Together this supports selective denoising.
4. **SNR/RMSE reward over-smoothing** (canine preprint; the upper-arm DWT vs DL trade-off).
5. **Stochastic variance is not calibrated uncertainty.** No retrieved ECG-denoising paper calibrates variance against feature error. PPG work (2604.17480; 2511.00301) shows such calibration is feasible and sensitive to hyperparameters.
6. **"Real-time" is under-specified:** window length, look-ahead, throughput and energy are conflated.
7. **Novelty now lies outside the architecture:** in the target, noise provenance, evaluation hierarchy and reliability.

---

## 11. Independent gap verification (adversarial)

| Candidate gap | Disproving evidence sought | Found | Verdict |
|---|---|---|---|
| "No natural-artifact evaluation" | SimEMG; upper-arm; armband | Yes | Unsupported; residual = scale, devices |
| "No morphology-aware denoising" | ST studies; morphology losses | Yes | Unsupported; residual = features under shift |
| "No downstream evaluation" | Granese; DCPA-SNN; Liu; canine | Yes | Unsupported |
| "No help/neutral/harm map" (attached RQ2) | Seo; Granese; Bender; SHTI 2026; Wang 2023 | Partial; subagent found no full factorial | Partially addressed (moderate confidence factorial open) |
| "No unpaired/noisy-only learning" | Cycle-GAN; TP-interval | Yes | Unsupported; residual = correlated artifacts |
| "No uncertainty-aware denoising" | AV-cDDPM; EMBC cDDPM | Yes | Unsupported; residual = feature calibration |
| "No low-power denoising" | DCPA-SNN; FPGA; Raspberry Pi | Yes | Unsupported; residual = measured Pareto |
| "No leakage-aware protocol" | ECG-ARD; Seo | Yes | Partially addressed; not standard |
| "No cross-device denoising test" | Wearable/cross-device searches | Not found | Confirmed (moderate) |
| "No clinician evaluation" | PMC11417490 | Yes | Unsupported; residual = denoised-only endpoints |
| "No joint SQA + denoising" | PMC12693763; TBME 2020 | Yes | Unsupported; residual = error-calibrated abstention |

---

## 12. Research questions

Each RQ covers the prompt's 19 fields, grouped into labelled blocks.

**RQ-A — factorial help/harm (refined from attached RQ2).**
- **Question.** Under which combinations of four factors does denoising improve, not change, or degrade performance versus raw input?
  - artifact type (bw/ma/em/natural);
  - severity (including clean input);
  - task (QRS detection, delineation/QT, rhythm, diagnosis);
  - downstream adaptation (frozen raw-trained, retrained, joint, raw-robust).
- **Gap status.** Partially addressed.
- **Evidence.** Seo 2026 (harm at 12 dB; the fixed-classifier ablation is called "still-missing"); Granese; Bender.
- **Counterevidence.** Canine delineation preprint; SHTI 2026.
- **Why unresolved.** No study crosses all factors or uses natural noise.
- **Hypotheses.**
  - H1: Δtask > 0 at moderate/severe artifact for frozen raw-trained models.
  - H2: Δtask ≈ 0 for retrained or raw-robust models.
  - H3: Δtask < 0 on clean/mild input without identity training.
- **Data.** PTB-XL (patient folds), MIT-BIH, QTDB/LUDB, SimEMG, BUT QDB.
- **Noise.** NSTDB with channel separation from −12 to 24 dB; clean input; natural segments.
- **Baselines.** Raw input; Butterworth/notch; tuned DWT; FCN-DAE; a diffusion model.
- **Design.** Full factorial, analysed with patient-level mixed effects.
- **Metrics and generalisation.** Δ in F1, sensitivity/PPV and delineation error (ms); QT/ST/P/R-timing error; dataset, noise-source and natural-artifact axes; denoiser cost reported beside Δtask.
- **Confounders.** Filtered "clean" folds; class imbalance.
- **Failure mode.** Interactions too small to detect.
- **Falsification.** Δtask ≈ 0 in every cell.
- **Progress.** A regime map with confidence intervals.

**RQ-B — feature-specific calibrated abstention.**
- **Question.** Can per-feature uncertainty (QT, ST, QRS duration, R timing) from stochastic or ensemble denoisers be calibrated to feature error, so that selective output meets a clinical tolerance at a stated coverage?
- **Gap status.** Partially addressed.
- **Evidence.** AV-cDDPM produces variance maps but does not calibrate them.
- **Counterevidence.** CPR cascade "indeterminate" routing; PPG uncertainty subsets.
- **Why unresolved.** No ECG feature-level calibration was found.
- **Hypothesis.** Feature uncertainty rank-correlates with feature error (Spearman > 0.5) and beats SQA-only gating on risk–coverage.
- **Data and noise.** QTDB/LUDB, SimEMG, BUT QDB; semi-synthetic plus natural noise.
- **Baselines.** Deep ensembles; MC dropout; diffusion sampling; SQA thresholds.
- **Metrics.** Feature-level ECE; AURC; coverage at QT error ≤10 ms; calibration under shift; cost of N samples.
- **Confounders.** Annotation error in reference fiducials.
- **Failure mode.** Uncertainty tracks noise level rather than error.
- **Falsification.** No gain over SQA-only gating.
- **Progress.** Calibrated abstention under shift.

**RQ-C — natural-artifact and device transfer.**
- **Question.** Which corruption models give feature fidelity that transfers to natural wearable ECG on unseen devices? Candidates: NSTDB additive; NSTDB channel-separated; parametric motion models; unpaired real-noise adversarial training.
- **Gap status.** Confirmed gap for devices; partially addressed for datasets.
- **Evidence.** Only SimEMG/EMG OOD tests exist.
- **Counterevidence.** ECG-ARD, TFCDiff.
- **Why unresolved.** No controlled device variable.
- **Hypothesis.** Noise-source separation shrinks the OOD gap more than architecture changes do.
- **Data.** Own multi-device paired recordings (a reference Holter beside a wearable), SimEMG, BUT QDB.
- **Conditions.** Rest, walking, arm movement, posture change.
- **Design.** Leave-one-device-out and leave-one-activity-out.
- **Metrics.** QRS/ST/QT error vs the reference device; QRS detection and delineation; per-model cost.
- **Confounders.** Lead-placement differences.
- **Failure mode.** The reference device is itself noisy.
- **Falsification.** Nothing beats raw input + Butterworth on external devices.
- **Progress.** A corruption recipe that transfers.

**RQ-D — noisy-only validity envelope.**
- **Question.** Under what artifact statistics (non-zero-mean, ECG-correlated, electrode motion) do TP-interval, blind-spot or partition-based self-supervised ECG denoisers become biased, and can the bias be bounded?
- **Gap status.** Partially addressed.
- **Evidence.** The TP-interval method assumes additive stationary noise.
- **Counterevidence.** Adjacent iPSD and Speckle2Self work shows both failures and fixes.
- **Hypothesis.** Bias grows with the correlation between artifact and QRS timing.
- **Design.** Simulated plus natural ECG; a controlled correlation sweep; supervised oracle vs self-supervised methods.
- **Metrics.** Bias in feature estimates, and its effect on the RQ-A tasks.
- **Confounders.** Heart-rate-dependent TP length.
- **Failure mode.** No TP segment in tachycardia.
- **Falsification.** No bias growth with correlation.
- **Progress.** A theory-backed validity envelope.

**RQ-E — causal resource Pareto.**
- **Question.** For zero-look-ahead denoisers on MCU hardware, what is the measured frontier of feature fidelity vs latency, peak RAM and energy per hour?
- **Gap status.** Partially addressed.
- **Evidence.** Reports cannot be compared with each other.
- **Counterevidence.** DCPA-SNN; FPGA DWT; multitask pruning.
- **Hypothesis.** Tuned causal IIR/wavelet methods beat small networks on QRS/R timing; networks win only on P/ST under EMG.
- **Noise.** Graded EMG and motion artifacts.
- **Methods compared.** Causal Butterworth, notch, streaming DWT, int8 CNN, SNN.
- **Design.** All methods on one Cortex-M4/M33 with a power monitor.
- **Metrics.** Measured latency, RAM, flash and energy; QRS detection.
- **Confounders.** Compiler settings.
- **Failure mode.** Board-specific results.
- **Falsification.** Networks dominate every point.
- **Progress.** A reproducible frontier.

**RQ-F — target-validity audit.**
- **Question.** How much of the reported fidelity is agreement with the reference's preprocessing rather than with physiology?
- **Gap status.** Confirmed gap.
- **Evidence.** Liu's reference construction; PTB-XL quality flags.
- **Counterevidence.** Simulation ground truth.
- **Hypothesis.** Method rankings change when the reference changes.
- **Design.** Retrain published denoisers against raw, filtered and simulated-truth references.
- **Metrics.** Kendall τ between rankings; ST/QT error vs simulated truth; stability of task rankings.
- **Confounders.** Differences in retraining.
- **Failure mode.** Unrealistic simulation.
- **Falsification.** τ > 0.9.
- **Progress.** Rankings that hold up across references.

---

## 13. Benchmark and experimental framework

**Already standard:**
- SNR improvement, RMSE, PRD, correlation;
- QTDB/MIT-BIH + NSTDB;
- bw/ma/em noise types;
- −6 to 24 dB SNR grids.

**Inconsistently practised:**
- patient/record-disjoint splits;
- mixed-noise training;
- R-peak detection after denoising;
- multi-beat 10-s windows;
- runtime reporting.

**Largely missing:**
- noise-channel/segment separation (ECG-ARD is the exception);
- clean-input do-no-harm tests;
- feature-level error with tolerances;
- natural-artifact tracks;
- cross-device splits;
- calibrated abstention;
- measured MCU RAM/energy;
- data and noise manifests.

**Proposed components.**
1. **Three tracks:**
   - simulated, with known truth;
   - semi-synthetic, with noise-disjoint NSTDB and noisy-only normalisation;
   - natural (SimEMG, BUT QDB, new multi-device recordings).
2. **Partitions** disjoint by patient, noise source, device and site.
3. **Severity** from −12 dB to clean, plus mixtures.
4. **Evaluation hierarchy:** signal → regional → feature (ms/mV tolerances) → sequence (RR/HRV/ectopy) → task (frozen/retrained/joint) → interpretation → reliability (risk–coverage) → deployment (latency, look-ahead, RAM, flash, energy per hour).
5. **Statistics:** patient-level mixed effects and non-inferiority margins.
6. **Release:** code, checkpoints and manifests.

---

## 14. Key datasets, noise sources, and evaluation practices

| Dataset | Role | Known limitations/biases |
|---|---|---|
| MIT-BIH Arrhythmia | Clean-ish source (2-channel, 360 Hz; 48 half-hour records, 47 subjects per [L])\[5\]\[14\] | Old; small; not artifact-free |
| NSTDB | Recorded bw/ma/em\[3\] | Few realisations → reuse leakage; additive assumption |
| QTDB | Annotated source (105 fifteen-minute excerpts, 250 Hz per [L])\[40\] | Selected to avoid artifacts; partial annotation |
| PTB-XL | 12-lead source; labels | Natural noise; a derivative excluded 20.9% on quality flags\[29\] |
| SimEMG | Paired clean/EMG (15 healthy volunteers)\[15\] | EMG only; healthy |
| BUT QDB | Free-living quality labels (per [L]) | No clean reference |
| Tianchi | Large 12-lead set (Liu)\[41\] | Patient-disjointness not established |
| Wearable SQA sets | 18 benchmark datasets reviewed (Physiol Meas 2026)\[42\] | Quality labels ≠ restoration truth |

[L] figures were not re-verified from primary dataset pages.

---

## 15. Contradictions and unresolved debates

1. **Does denoising help diagnosis?**
   - Harm: Granese.
   - Help: Liu (preprint), DCPA-SNN, the clinician combined view.
   - Neutral: Bender.
   - [I] The effect depends on severity and adaptation; it is unsettled.
2. **Deep vs classical.** Deep methods win in-distribution on NSTDB. On real upper-arm data, DWT suppresses noise best and DL preserves morphology best (preprint). Classical baselines are often untuned.
3. **Stronger suppression is not always better** (canine preprint; Seo P-wave degradation).\[5\]\[8\]
4. **Is preprocessing needed for deep classifiers?** The 2026 PTB-XL preprocessing study (Stud Health Technol Inform, doi 10.3233/SHTI260227) found CNNs best on raw input. A 2025 systematic review instead reported multi-stage denoising improving R-peak and classification results. Note that the review aggregates heterogeneous studies.
5. **Stochastic variance vs calibrated uncertainty:** open.
6. **DeScoD-ECG year:** 2023 in citing lists vs 2024 in the attached review; unresolved.

---

## 16. Comparison with the attached LLM review

### 16.1 Agreement matrix

| Topic | Independent review | Attached review | Reconciled evidence |
|---|---|---|---|
| Semi-synthetic NSTDB dominance | Yes | Yes | Corroborated |
| Morphology/downstream work exists | Yes | Yes | Corroborated (Lenis, Seo, Granese, DCPA-SNN) |
| Task dependence of benefit | Yes | Yes | Corroborated |
| Unpaired/uncertainty/multi-lead/embedded not novel per se | Yes | Yes | Corroborated |
| Novelty outside architecture | Yes | Yes | Corroborated as inference |
| Variance ≠ calibrated uncertainty | Yes | Yes | Corroborated as inference |

### 16.2 Disagreement matrix

| Claim | Attached review says | Independent evidence says | Resolution | Confidence |
|---|---|---|---|---|
| RQ2 novelty | "No direct counterexample"; "safest genuinely novel" | Seo 2026 severity-dependent help/harm and named missing ablation; Granese; Bender; SHTI 2026; Wang 2023\[5\]\[7\]\[38\]\[43\]\[44\] | Downgrade to partially addressed; factorial with adaptation + natural noise survives | Moderate |
| Liu self-supervised paper | 2025; 18,604 recordings | bioRxiv 2024 version shows package-denoised + Gaussian reference;\[28\] 18,604 not verified | Partially corroborated; target problem stronger | Moderate |
| Wearable-SQA uncertainty trust study 2026 | Exists | Not found | Insufficient evidence | Low |
| MC-dropout reconstruction 2026 | Exists | Not found | Insufficient evidence | Low |
| JBHI diffusion uncertainty maps | 2026 JBHI | AV-cDDPM PubMed record confirms content;\[22\] venue not verified | Partially corroborated | Moderate |
| Unpaired real-noise training | 2025–2026 development | Operational Cycle-GAN 2022 earlier\[20\] | Publication-period difference | Moderate |
| FPGA 1.09 ms / 426 mW | Stated | Only 5%/6% utilisation verified\[23\] | Partially corroborated | Moderate |

### 16.3 Claims corroborated

- DCPA-SNN (Sensors 2026; MIT-BIH+NSTDB; −6 to 4 dB).
- ECG-ARD's causal decoder and leakage-aware protocol.
- The clinician raw+denoised study (75.7% → 80.6%).
- Edge SQA+denoising with pruning/quantisation (PMC12693763).
- Granese harm.
- Lenis figures.
- The 2607.11450 trade-off.
- SimEMG as paired real EMG data.

### 16.4 Claims weakened or contradicted

- RQ2 as the "safest novel" question is weakened.
- "No prior study varies severity × raw vs denoised" is partly contradicted by Seo 2026, which found harm at 12 dB (at the waveform level).
- The user's preliminary observation (negative ΔSNR on clean wearable ECG) is independently corroborated in kind by Seo et al., so it cannot be the headline novelty.

### 16.5 Gaps missed by the attached review

- Noise-source leakage, tied to a noise-disjoint metric.
- Identity-training "do-no-harm" target design.
- Dependence of method rankings on the reference (RQ-F).
- Untuned classical baselines.
- PPG uncertainty-quantification methodology as a transferable calibration framework.

### 16.6 Gaps proposed by the attached review that do not survive verification

- Broad RQ1, RQ5, RQ6, RQ7 and RQ8 (as the attached review itself concluded).
- RQ2 in its "fully novel" framing. Only RQ2's factorial/adaptation/natural-noise core survives.

### 16.7 Final reconciled research landscape

Both reviews converge on reliability, validity and transfer as the open problems. This review adds emphasis on target and noise-provenance audits, a do-no-harm criterion and measured deployment frontiers. It also lowers confidence in RQ2's novelty.

---

## 17. Surviving research opportunities

| Research opportunity | Verified residual gap | Supporting evidence | Counterevidence | Research question | Required experiment | Key evaluation |
|---|---|---|---|---|---|---|
| Factorial help/harm map | Full factorial with adaptation | Seo; Granese; Bender | Canine; SHTI 2026 | RQ-A | Severity × type × task × adaptation | Δtask with CIs |
| Do-no-harm denoising | Clean-input degradation | Seo 12 dB | Canine identity pairs | Does identity regularisation remove harm without losing low-SNR gains? | Clean/mild tracks | ΔSNR ≥ 0; feature non-inferiority |
| Feature abstention | Feature-error calibration | AV-cDDPM variance | CPR routing; PPG UQ | RQ-B | Ensembles/diffusion | Feature ECE, AURC |
| Quality-gated selective denoising | Gates tied to task error | TBME 2020 tiers | PMC12693763 | Does Q(x) gating beat always-denoise? | Gate vs always vs never | Task Δ, coverage |
| Noise-disjoint benchmark | Noise-reuse leakage | ECG-ARD | — | How much do rankings shift? | Re-evaluate published models | Ranking change |
| Reference audit | Filtered-as-clean | Liu; PTB-XL flags | Simulation truth | RQ-F | Swap references | Kendall τ |
| Device transfer | No device axis | Thin natural evidence | ECG-ARD, TFCDiff | RQ-C | Leave-one-device-out | Feature error |
| Electrode-motion paired dataset | SimEMG EMG-only | SimEMG scope | — | Can a SimEMG-like design capture em? | New acquisition | Paired fidelity |
| Noisy-only envelope | Correlated artifacts | TP-interval | iPSD; Speckle2Self | RQ-D | Correlation sweep | Bias |
| Causal MCU Pareto | Incommensurable reporting | Pi, FPGA, SNN | DCPA-SNN | RQ-E | Same-board measurement | Fidelity vs RAM/energy |
| Look-ahead quantification | Unquantified look-ahead | ECG-ARD full-segment conditioning | Online ICA | Fidelity lost per ms of look-ahead? | Look-ahead sweep | Feature error vs delay |
| QT/QTc under natural noise | Not found | Level-3 simulated only | Lenis (ST) | Are QT errors within tolerance? | QTDB/LUDB + natural | QT error (ms) |
| Rhythm/ectopy fidelity | Beat windows distort RR\[15\] | TFCDiff critique | TFCDiff AF/PVC | Does denoising alter RR/HRV/ectopy? | Multi-beat vs beat | HRV, ectopy |
| Pathology stress testing | Fine features distort at extreme noise\[15\] | TFCDiff f-waves | — | Which pathologies fail first? | Stratified tests | Per-pathology non-inferiority |
| Reader presentation | Only combined-view evidence | PMC11417490 | — | Denoised-only vs combined vs raw? | Reader study | Accuracy, undiagnosable rate |

---

## 18. Limitations

- **Search:** 18 web searches plus one subagent (about 13 tool calls). No Scopus/WoS/IEEE exports and no registered protocol.
- **Databases:** several PMC and IEEE full texts were blocked. ECG-ARD was verified at abstract level only.
- **Terminology:** MA/EMG/motion are used inconsistently. Less-searched terms ("restoration", "enhancement") may hide counterexamples.
- **Publication period:** 2026 papers are very recent. TFCDiff, 2607.11450, 2605.03183, 2511.12478 and the Liu bioRxiv version are preprints.
- **Not verified from the retrieved evidence:**
  - the 1991 J Electrocardiology study;
  - wavelet–Wiener;
  - morphological filtering (2002);
  - EMD (2008);
  - SPARS 2011;
  - NMF;
  - IMU-NLMS;
  - BIBM 2025;
  - SC-CycleGAN;
  - ML-CDAE;
  - FGCT;
  - Galiger FISTA-Net;
  - the Frontiers lead-reconstruction study;
  - federated ECG;
  - the wearable-SQA uncertainty trust study;
  - the MC-dropout reconstruction paper.
- **Evidence quality:** many results come from single groups, are semi-synthetic, and lack CIs. No numbers were compared across studies.
- **Gap uncertainty:** the cross-device and QT gaps rest on evidence absence after limited searching.
- **Attached review:** it reports that it did not reach saturation, and several of its 2026 citations could not be located.
- **This review:** shares these limits; its [I] inferences need empirical testing.
- **Search-stop criterion: NOT reached.** The final searches still returned new relevant 2026 material.

## Sources

1. [DCPA-SNN, Direct-Coding-Physics-Aware Spiking Neural Network: A Framework for Wearable ECG Denoising Under Dynamic-Noise Conditions - PubMed](https://pubmed.ncbi.nlm.nih.gov/42590470/)
2. [A Deep Learning Framework Based on Denoising and 2D Image Encoding for Arrhythmia Classification - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13517396/)
3. [An efficient ECG denoising method by fusing ECA-Net and CycleGAN - PubMed](https://pubmed.ncbi.nlm.nih.gov/37501494/)
4. [ECG Signal Denoising Using Multi-scale Patch Embedding and Transformers](https://arxiv.org/pdf/2407.11065)
5. <https://ncbi.nlm.nih.gov/pmc/articles/PMC13517396>
6. [Fully-Gated Denoising Auto-Encoder for Artifact Reduction in ECG Signals](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11821071/)
7. [The Negative Impact of Denoising on Automated Classification of Electrocardiograms | ML Anthology](https://mlanthology.org/neuripsw/2023/granese2023neuripsw-negative/)
8. [Enhancing AI-Based ECG Delineation with Deep Learning Denoising Techniques](https://arxiv.org/pdf/2605.03183)
9. [Doi](https://doi.org/10.1109/jbhi.2026.3727288)
10. [Baseline wander removal methods for ECG signals: A comparative study](https://arxiv.org/pdf/1807.11359)
11. [ECG Beat Representation and Delineation by means of Variable Projection](https://arxiv.org/pdf/2109.13022)
12. [Artifact removal from ECG signals using online recursive independent component analysis - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2772415824000130)
13. [GitHub - ime-luebeck/ecg-removal: Algorithms and evaluation toolkit for removing strong cardiac interference from surface EMG measurements](https://github.com/ime-luebeck/ecg-removal)
14. [A novel approach for denoising electrocardiogram signals to detect cardiovascular diseases using an efficient hybrid scheme - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11064874/)
15. [TFCDiff: Robust ECG Denoising via Time-Frequency Complementary Diffusion](https://arxiv.org/pdf/2511.16627)
16. [IEEE Access (Jan 2019)](https://doaj.org/article/81f46f96755b468bacc652dd28c48c93)
17. [MECG-E: Mamba-based ECG Enhancer for Baseline Wander Removal](https://arxiv.org/pdf/2409.18828)
18. [Self-Supervised Electrocardiograph De-noising | bioRxiv](https://www.biorxiv.org/content/10.1101/2024.01.01.573833v1.full)
19. [A Paralleled Multi-Task Learning-Based Framework for Single-Lead ECG Fine-Grained Noise Localization, Denoising and Signal Quality Assessment](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12693763/)
20. [Blind ECG Restoration by Operational Cycle-GANs](https://arxiv.org/pdf/2202.00589)
21. [ECG-ARD: Autoregressive ECG Denoising With Dual-Domain Fusion and a Vector-Quantized Bottleneck - PubMed](https://pubmed.ncbi.nlm.nih.gov/42636122/)
22. [Antithetic Sampling Enhanced Probabilistic Diffusion for Denoising Cardiac Time Series - PubMed](https://pubmed.ncbi.nlm.nih.gov/42329950/)
23. [The Hardware-Architecture Design of a Hybrid DWT–ADTF-Based Real-Time ECG-Denoising System: An Optimized FPGA Implementation](https://doi.org/10.3390/sym18071189)
24. [Comparison of Baseline Wander Removal Techniques considering the Preservation of ST Changes in the Ischemic ECG: A Simulation Study](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5361052/)
25. [\[2511.12478\] Lightweight Deep Autoencoder for ECG Denoising with Morphology Preservation and Near Real-Time Hardware Deployment](https://arxiv.org/abs/2511.12478)
26. [\[2607.11450\] Comparative Study of ECG Denoising Methods for Wearable Applications](https://arxiv.org/abs/2607.11450)
27. [Evaluating the impacts of digital ECG denoising on the interpretive capabilities of healthcare professionals](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11417490/)
28. [Self-Supervised Electrocardiograph De-noising](https://www.biorxiv.org/content/10.1101/2024.01.01.573833v1.full.pdf)
29. [PTB-XL-Image-17K: A Large-Scale Synthetic ECG Image Dataset with Comprehensive Ground Truth for Deep Learning-Based Digitization](https://arxiv.org/pdf/2602.07446)
30. [A Deep Learning Framework Based on Denoising and 2D Image Encoding for Arrhythmia Classification](https://doi.org/10.3390/s26165183)
31. [Trustworthy deep domain adaptation for wearable photoplethysmography signal analysis with decision-theoretic uncertainty quantification](https://arxiv.org/pdf/2604.17480)
32. [Doi](https://doi.org/10.1109/tbme.2020.2969719)
33. [Self-Supervised Electrocardiograph De-noising](https://www.biorxiv.org/content/10.1101/2024.01.01.573833.full.pdf)
34. [Enabling Unsupervised Training of Deep EEG Denoisers With Intelligent Partitioning](https://arxiv.org/html/2605.06724)
35. [Speckle2Self: Self-Supervised Ultrasound Speckle Reduction Without Clean Data](https://arxiv.org/pdf/2507.06828)
36. [DCPA-SNN, Direct-Coding-Physics-Aware Spiking Neural Network: A Framework for Wearable ECG Denoising Under Dynamic-Noise Conditions](https://doi.org/10.3390/s26154695)
37. [Physics-Inspired Diffusion Probabilistic Models for Improved Denoising in Intracardiac Time Series - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13110842/)
38. [Comparative Assessment of Machine Learning Strategies for Electrocardiogram Denoising](https://link.springer.com/chapter/10.1007/978-981-99-8388-9_40)
39. [Cascade Skip-Connection BiLSTM Autoencoder for CPR Artifact Removal Prior to AED Shock Advisory - PubMed](https://pubmed.ncbi.nlm.nih.gov/42327859/)
40. [Fully-Gated Denoising Auto-Encoder for Artifact Reduction in ECG Signals](https://www.mdpi.com/1424-8220/25/3/801)
41. [\[2105.06293\] Electrocardio Panorama: Synthesizing New ECG Views with Self-supervision](https://ar5iv.labs.arxiv.org/html/2105.06293)
42. [Automated analysis of wearable ECG: machine learning methods, preprocessing pipelines, and benchmark datasets - PubMed](https://pubmed.ncbi.nlm.nih.gov/42456763/)
43. [IOS Press Ebooks - Architecture-Specific Impact of Preprocessing on Machine Learning Models for ECG Classification](https://ebooks.iospress.nl/doi/10.3233/SHTI260227)
44. <https://arxiv.org/pdf/2303.13915>
