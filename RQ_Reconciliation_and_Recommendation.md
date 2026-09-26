# Reconciling the two reviews: the most feasible publishable research question

Inputs compared:
- `denoise_slr.md` (**SLR**): scoping survey with gaps G1–G11 and RQ1–RQ9, followed by a counterexample pass whose verdict is "RQ2 is the safest genuinely novel RQ".
- `Evidence_Audited_Research_Landscape.md` (**Audit**): an independent, evidence-labelled review that adversarially re-checks the SLR, proposes RQ-A to RQ-F, and includes a disagreement matrix (§16).

Neither review reached search saturation, and both say so. The novelty verdicts below are therefore "no counterexample found in two independent passes". They are not proofs of novelty.

---

## 1. Where the two reviews agree (high-confidence ground)

| Point | SLR | Audit | Implication |
|---|---|---|---|
| A new architecture on QTDB/MIT-BIH + NSTDB is not a contribution | §5.7, §9.6 | §2, §10.7 | Don't lead with a model |
| Semi-synthetic (clean ECG + added NSTDB) evaluation dominates | §1.2, G2 | §1, §6.2 | A natural-noise track differentiates the work |
| Morphology-aware, downstream, unpaired, uncertainty, multi-lead and embedded work all exist | §6 "not accepted as gaps" | §11 | Broad "no one has done X" claims will be rejected |
| Denoising benefit is task-dependent; both help and harm are reported | G6, §13 | §6.5, §15.1 | The conditions of help/harm are the open question |
| Stochastic variance ≠ calibrated uncertainty | §13 | §10.5 | Only feature-error-calibrated abstention is open |
| Clean-input "do-no-harm" test and an L1–L8 evaluation hierarchy | §11.4–11.5 | §13 | Adopt as protocol in any paper |
| Three data tracks: synthetic / semi-synthetic / natural | §11.2 | §13 | Same benchmark skeleton |

## 2. Where they disagree (and which side the evidence favours)

| Issue | SLR says | Audit says | Resolution |
|---|---|---|---|
| **RQ2 novelty** (help vs harm) | "No direct counterexample", 🟢 safest novel RQ | Only *partially addressed*. Seo et al. 2026 (Sensors, 10.3390/s26165183) shows help at −12 dB and harm at 12 dB; Granese 2023 reports up to 40 pp accuracy harm; Bender 2023 finds raw models robust; SHTI 2026 finds CNNs best on raw input | **The Audit is right.** The SLR's own counterexample pass did not surface Seo, Granese-in-that-role, Bender or SHTI 2026. What survives is the **full factorial with downstream-model adaptation on natural noise**. Seo explicitly calls the fixed-classifier ablation "still-missing", which gives you a citable gap statement. |
| Your preliminary result (learned denoisers give −ΔSNR on clean wearable ECG) | "extremely useful" motivation | Corroborated in kind by Seo 2026, so it cannot be the headline | Use it as a **replication/motivation figure**, not the claim |
| RQ5 (uncertainty) | Broad version killed by three 2026 papers; feature-specific version survives | Two of those three citations (wearable-SQA trust study, MC-dropout reconstruction) **could not be located**; AV-cDDPM confirmed | Same surviving narrow RQ either way (feature-level calibrated abstention). Verify or drop the two unlocated citations |
| RQ8 (causal low-power) | Broad version killed; Pareto survives | Agrees, and adds that no measured MCU energy or peak RAM exists for any *denoiser* | Narrow Pareto survives, with stronger support |
| Specific facts | FPGA 1.09 ms / 426 mW; Liu 2025, 18,604 records; DeScoD 2024 | Only 5%/6% utilisation verified; Liu bioRxiv 2024 uses a package-denoised + Gaussian reference; DeScoD year unresolved | Re-verify before citing |

## 3. What each review has that the other lacks

**Only in the Audit.** These are all cheap to add and strengthen any paper:
- **Noise-source leakage.** NSTDB has three noise records, and they are reused across splits. ECG-ARD introduced channel separation. Patient-disjoint splits are not noise-disjoint.
- **Target validity (RQ-F).** "Clean" references are filtered or package-denoised, so method rankings may just track the reference.
- **Identity (clean→clean) training** as a do-no-harm mechanism (canine preprint 2605.03183).
- **Untuned classical baselines.** DWT gets only ~1 dB in some papers.
- **Look-ahead quantification.** ECG-ARD's "causal" decoder still conditions on the full segment.
- **Help/harm evidence:** Bender 2023, SHTI 2026 and the explicit ablation gap in Seo 2026.

**Only in the SLR:**
- Auxiliary-sensor gating (RQ7).
- Multi-lead shared-electrode corruption (RQ6).
- Patient-identity preservation in unpaired restoration.
- Venue tiering.
- A PICO-style novelty-matrix recommendation.

The SLR has more dataset detail (LUDB, BUT PDB, MIMIC-IV-ECG, BUT QDB with accelerometer). Several SLR-only citations were not independently verified by the Audit: SC-CycleGAN, BIBM 2025, ML-CDAE, FGCT and FISTA-Net.

## 4. Feasibility scoring of the surviving (narrowed) RQs

Scores are 1–5, where 5 is best. **Novelty** is the reconciled view (the lower of the two reviews). **Feasibility** assumes public data plus your existing benchmark and wearable setup.

| RQ (narrowed) | Novelty (reconciled) | Data available now | Compute / engineering | Time to 1st paper | Risk of null | Ceiling venue | **Overall** |
|---|---|---|---|---|---|---|---|
| **A. Factorial help/harm × downstream adaptation + selective (gated) denoising** (SLR RQ2 ≈ Audit RQ-A + "quality-gated" row) | 3.5 | 5 (MIT-BIH, NSTDB, QTDB, LUDB, PTB-XL, SimEMG, BUT QDB) | 4 | 5 (~3–5 mo) | Low: a null result is still publishable, see §6 | JBHI / BSPC | **★ best** |
| B. Feature-specific error-calibrated abstention (RQ5 ≈ RQ-B) | 4.5 | 4 (QTDB/LUDB fiducials) | 3 (ensembles/diffusion, calibration) | 3 | Medium (uncertainty may just track noise level) | TBME / JBHI | Strong 2nd paper |
| F. Target-validity audit (reference swap → Kendall τ) | 4.5 | 5 | 4 | 4 | Medium (τ may be > 0.9) | BSPC / Physiol Meas | Good short/side paper |
| E. Measured causal fidelity–RAM–energy Pareto (RQ8 ≈ RQ-E) | 4 | 5 | 3 (needs board + power monitor) | 3 | Low | TBioCAS / BioCAS | Good if you have the hardware |
| C. Corruption model → cross-device transfer (RQ3 ≈ RQ-C) | 4.5 | 2 (needs own multi-device paired recordings) | 2 | 2 | Medium | TBME | Later / PhD core |
| D. Noisy-only validity envelope (RQ4 ≈ RQ-D) | 4 | 4 | 3 | 2 | Medium | TBME / TSP-type | Harder, more theoretical |
| RQ6 multi-lead, RQ7 aux sensors | 2.5–3 | 2–3 | 2 | 2 | — | — | Deprioritise |

## 5. Recommendation

### Primary research question (paper 1)

> **Under which combinations of artifact type, artifact severity (including clean input), downstream task, and downstream-model adaptation does ECG denoising improve, leave unchanged, or degrade analysis relative to raw ECG — and does a signal-quality-gated *selective* denoiser dominate both "always denoise" and "never denoise"?**

**Why this is the most feasible and publishable choice:**
1. **Both reviews converge on it.** It is the SLR's top pick, and the Audit keeps its factorial core as surviving opportunity #1.
2. **The gap is stated by prior authors.** Seo 2026 calls the fixed-classifier ablation "still-missing", and Granese, Bender and SHTI 2026 disagree in ways that only an adaptation factor can reconcile (Audit §10.3). You extend published results instead of claiming a vacuum, which reviewers accept more readily.
3. **It runs entirely on public data plus your existing benchmark.** Your −ΔSNR-on-clean finding becomes the motivating figure.
4. **It has a constructive contribution, not only an analysis.** The three-way gate from SLR §"Contribution 2":
   `D(x) = x if Q(x) > τ1; f(x) if τ2 < Q(x) ≤ τ1; abstain if Q(x) ≤ τ2`
5. **Every outcome is publishable:**
   - If H1–H3 hold, you get a regime map plus a gate that beats both fixed policies.
   - If Δ ≈ 0 everywhere for adapted models, that is a strong "denoising is unnecessary for raw-robust models" result, consistent with Bender and SHTI 2026 but now factorial and on natural noise.

**What makes it novel beyond Seo, Granese and Bender.** No single prior study combines all of these:
- **downstream adaptation as an explicit factor**: frozen clean-trained, noise-augmented raw, retrained on denoised, joint;
- **multiple tasks on the same cohorts**;
- a **clean-input do-no-harm arm**;
- **noise-disjoint NSTDB splits**;
- a **natural-noise track**;
- **quality-gated selective denoising** evaluated on task Δ vs coverage.

### Minimal experimental design

| Factor | Levels |
|---|---|
| Artifact | bw, ma, em, mixed (NSTDB, **time-segment-disjoint** train/val/test), natural (SimEMG, BUT QDB, own wearable) |
| Severity | clean, 24, 12, 6, 0, −6 dB |
| Denoiser | none; Butterworth + notch; **tuned** DWT; FCN-DAE or DeepFilter; optionally one diffusion model (DeScoD) if compute allows; each ± identity-pair training |
| Task | R-peak detection (MIT-BIH); delineation/QT/QRS duration (QTDB, LUDB); rhythm/AF classification (PTB-XL or similar) |
| Downstream adaptation | frozen clean-trained · noise-augmented raw · retrained on denoised · jointly fine-tuned |
| Policy | never / always / Q(x)-gated (SQI thresholds tuned on validation only) |

- **Endpoints:**
  - Δtask (F1, Se/PPV, AUROC, calibration);
  - feature error in ms/mV (QT, QRS, ST, P);
  - clean-input distortion;
  - coverage of the gate;
  - added latency.
- **Statistics:** patient-level mixed effects; prespecified non-inferiority margins; a regime map with CIs.
- **Falsification:** Δtask ≈ 0 in every cell, and the gate is no better than never-denoise.

### Follow-on papers (one PhD arc)

1. **Paper 2 (RQ-B):** replace the gate's "abstain" branch with **feature-specific, error-calibrated** uncertainty (U_QT, U_QRS, U_ST, U_R). Evaluate with feature ECE, AURC, and coverage at |ΔQT| ≤ 10 ms. This reuses paper 1's pipeline.
2. **Paper 3 (RQ-E or RQ-C):**
   - If you have hardware: measure the causal gated denoiser's fidelity–RAM–energy–look-ahead Pareto on one Cortex-M board (BioCAS/EMBC first, then TBioCAS).
   - If you have multi-device acquisition: leave-one-device-out transfer (TBME).
3. **Cheap side result (RQ-F + noise-leakage):** how much published rankings shift under noise-disjoint splits and swapped references. This can be a section of paper 1 or a short EMBC paper.

### Venue path

- **Now:** EMBC/BioCAS 4-pager on a subset of the factorial (e.g. R-peak + QT tasks, NSTDB + SimEMG, frozen vs retrained).
- **Then:** the full factorial plus the gate in **IEEE JBHI** (best fit: trustworthy preprocessing + downstream + wearable) or **BSPC** (safer).
- **Then:** papers 2 and 3 toward TBME or TBioCAS.

## 6. Before you commit: verification to-dos

1. **Read Seo et al. 2026 in full** (doi 10.3390/s26165183), along with Granese 2023, SHTI 2026 (10.3233/SHTI260227) and arXiv 2605.03183. Build the SLR-recommended PICO novelty matrix: population, artifact, intervention, comparison, outcome, generalisation condition. Confirm that none crosses adaptation × task × severity × natural noise.
2. **Run a targeted search** for 2026 work on "denoising necessity", "preprocessing ablation" and "raw vs denoised ECG classifier". The Audit found SHTI 2026 late, so the area is moving.
3. **Resolve the SLR's unlocated citations** before citing them: the wearable-SQA uncertainty trust study 2026, the MC-dropout reconstruction 2026, and the FPGA 1.09 ms / 426 mW figures. Also fix the Liu 2024/2025 year and the DeScoD 2023/2024 year.
4. **Check that your natural tracks have usable task labels.** Confirm the BUT QDB annotation coverage for R-peaks, and SimEMG fiducials. Otherwise, derive references from the clean simultaneous channel.
