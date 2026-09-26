# When does cleaning an ECG actually help?

A quick map:

```
Step 0 Setup ─► Step 1 Novelty check ─◆D1─► Step 2 Data check ─◆D2─► Step 3 Splits
   ─► Step 4 Noisy test sets ─► Step 5 Cleaners (E1) ─◆D3─► Step 6 Task models
   ─► Step 7 Pilot (E2) ─◆D4─► [short paper] ─► Step 8 Full run (E3) ─► Step 9 Analysis ─◆D5
   ─► Step 10 Switch (E4) ─◆D6─► Step 11 Real-life check (E5) ─► Step 12 Write-up ─◆D7
```

(◆ = decision point · E# = experiment)

---

### Step 0: Set up the workspace (≈ 1–2 days)

- **Do:**
  - Create the `research/` folders and log files from Part D.
  - Set up the Python environment: the `wfdb` package for PhysioNet data, plus PyTorch.
  - Copy the three predictions (P1–P3) into `decision_log.md` as "D0 — predictions locked".
- **Inputs:** this plan.
- **Outputs:** empty logs; environment file (`requirements.txt`).
- **Experiment?** No.
- **Log:** `decision_log.md`, entry D0.
- **Decision?** No. The predictions are simply fixed.

---

### Step 1: Final novelty check (≈ 1–2 weeks)

- **Do:** Read these papers in full and fill in a comparison table. There is one row per paper, and the columns are: which patients/data, which noise, which cleaner, what it was compared against, what outcome was measured, and whether the model preparation was varied.
  - Must-read:
    - Seo 2026 (Sensors, doi 10.3390/s26165183);
    - Granese 2023 (NeurIPS workshop);
    - Bender 2023 (Stud Health Technol Inform 302:977–981);
    - SHTI 2026 preprocessing study (doi 10.3233/SHTI260227);
    - canine delineation preprint (arXiv 2605.03183);
    - Cardio-NAFNet (medRxiv 2022);
    - Memory Classifiers (2023);
    - Sci Rep 2026 QRS benchmark;
    - clinician study (PMC11417490).
  - Run one fresh search for 2026 papers on "is denoising necessary", "raw vs denoised ECG classifier" and "preprocessing ablation ECG".
- **Inputs:** the three review `.md` files; the paper PDFs.
- **Outputs:** `research/novelty_table.md`.
- **Experiment?** No.
- **Log:** one entry per paper in `reading_log.md`.
- **◆ Decision D1: Go / Narrow / Pivot.**
  - **Go:** no paper varies model preparation *and* noise level *and* task together.
  - **Narrow:** a paper covers part of it. Drop that part and keep the rest, e.g. keep real-life noise and the switch.
  - **Pivot:** someone has already done it all. Switch to the backup question: "can the cleaner tell us, per measurement (QT, QRS, ST), when its output can't be trusted?" See RQ-B in `Evidence_Audited_Research_Landscape.md`.

---

### Step 2: Get the data and check what labels exist (≈ 1 week)

- **Do:** Download each dataset, then check what "answer labels" it has for each task. Tick off this table:

| Dataset | Use | Needed labels | Check |
|---|---|---|---|
| MIT-BIH Arrhythmia | Heartbeat detection | Beat positions | ☐ |
| NSTDB | Noise source (bw, ma, em) | none | ☐ |
| QTDB, LUDB | Wave timing (QT, QRS width) | P/QRS/T start and end points | ☐ |
| PTB-XL | Rhythm classification (e.g. AF) | Rhythm labels + patient IDs | ☐ |
| SimEMG | Real muscle noise with a clean twin recording | Clean channel present? Beat positions? | ☐ |
| BUT QDB | Real everyday noise | Quality labels; beat positions available? | ☐ |
| Your own wearable data | Real device noise | What labels exist? | ☐ |

- **Inputs:** PhysioNet (and your own recordings).
- **Outputs:** `research/data_inventory.md`, with dataset, version, number of records and patients, sampling rate, and available labels.
- **Experiment?** No. You only count and inspect.
- **Log:** `reading_log.md` (data section), or a note in `experiment_log.md` as "E0 data check".
- **◆ Decision D2: Which tasks and which real-life datasets are in?**
  - Rule: keep a task only if it has trustworthy labels on at least one "added noise" set **and** one real-life set.
  - Aim for **3 tasks**: heartbeat detection, wave timing, and rhythm classification.
  - Fewer is fine for the pilot.

---

### Step 3: Make fair train/validation/test splits (≈ 3–4 days)

- **Do:**
  - **Split by patient.** No patient appears in more than one of train, validation and test.
  - **Split the noise too.** NSTDB has only three noise recordings, so cut each one in time: the first 60% for training, the next 20% for validation, and the last 20% for testing. The test noise is then never seen during training.
  - Save the lists as files so anyone can repeat the split.
- **Inputs:** the datasets from Step 2.
- **Outputs:** `research/splits/*.csv` (record/patient → train/val/test; noise segment → train/val/test).
- **Experiment?** Only a small check: a script that confirms no patient ID or noise time-range appears in two splits.
- **Log:** `experiment_log.md`, entry "E0-split check" with the script output.
- **Decision?** No.

---

### Step 4: Build the noisy test signals (≈ 3–4 days)

- **Do:** Take clean test signals and add test-split noise at every level: **clean (no noise), 24, 12, 6, 0 and −6 dB**, for each of bw, ma, em and a mix. Save the exact recipe for each signal: which noise segment, the start point and the scaling.
- **Inputs:** clean signals plus noise segments from the Step 3 splits.
- **Outputs:** the noisy dataset files and `research/configs/noise_recipe.json`.
- **Experiment?** No, but plot 5 random examples per level and check them by eye.
- **Log:** `experiment_log.md`, entry "E0-noise build", with the plots saved in `figures/`.
- **Decision?** No.

---

### Step 5: Set up the cleaners and check they work properly (≈ 2–3 weeks)

- **Do:** Prepare 4–5 cleaners, from simple to advanced. Each neural cleaner gets two versions: a normal one, and one also trained on clean→clean pairs so it learns to leave clean signals alone.
  1. **None** (raw signal).
  2. **Standard filter:** Butterworth band-pass plus notch.
  3. **Wavelet cleaner (DWT), properly tuned** on validation data. Don't use default settings; the literature often under-tunes this.
  4. **FCN-DAE or DeepFilter**, a common neural cleaner with public code.
  5. *(Optional, if compute allows)* **One diffusion model** (e.g. DeScoD-ECG).
- **Inputs:** training splits and noise training segments.
- **Outputs:** saved cleaner models in `research/models/`.
- **🧪 Experiment E1: cleaner check.**
  - Run each cleaner on the standard benchmark and compare its noise-reduction score with the published number.
  - Also measure how much each cleaner changes an already **clean** signal. This repeats your earlier finding that some neural cleaners make clean signals worse.
- **Log:** `experiment_log.md` (E1 runs) and `results/E1_cleaner_check.csv`.
- **◆ Decision D3: Are the cleaners trustworthy?**
  - If our numbers are within about 10% of the published ones, keep the cleaner.
  - If they are far off, fix it or drop it. Don't publish results that rest on a broken re-implementation.

---

### Step 6: Set up the task models in 4 preparation modes (≈ 2–3 weeks)

- **Do:** For each task, use one standard, simple model. Examples:
  - heartbeat detection: a standard detector and/or a small neural network;
  - wave timing: an existing delineator;
  - rhythm: a 1D ResNet.

  Train each in the four preparation modes:
  1. **Clean-trained, frozen:** trained on clean ECG, then never changed.
  2. **Noise-trained raw:** trained on raw ECG with added noise.
  3. **Re-trained on cleaned:** trained on the output of each cleaner.
  4. **Joint:** cleaner and task model fine-tuned together.

  Use validation data only to pick settings.
- **Inputs:** splits; noisy training data; cleaners from Step 5.
- **Outputs:** saved task models.
- **Experiment?** Only a basic check: each model scores sensibly on clean validation data.
- **Log:** `experiment_log.md`, entries "E0-task model check".
- **Decision?** No.

---

### Step 7: Pilot experiment, a small slice (≈ 2 weeks)

- **Do:** Run a reduced grid:
  - 1–2 tasks (heartbeat detection + wave timing);
  - 2 noise types (ma, em);
  - all noise levels;
  - 3 cleaners (none, filter, DAE);
  - preparation modes 1 and 2 only.

  For every combination, compute the **gain** (score with cleaning minus score without).
- **Inputs:** everything from Steps 3–6.
- **Outputs:** `results/E2_pilot.csv` and a first heat-map figure (noise level × cleaner, coloured by gain).
- **🧪 Experiment E2: pilot.**
- **Log:** `experiment_log.md` (E2 runs).
- **◆ Decision D4: Is it worth running the full study?**
  - **Continue** if the gains clearly differ between conditions, for example positive at −6 dB and negative on clean input, with confidence intervals that don't all overlap zero.
  - **Also:** if the pilot is clean and clear, **write it up now as a 4-page conference paper** (EMBC or BioCAS). This protects against the scooping risk from Part A.
  - **Rethink** if everything is close to zero. Check the noise levels and the task choice, then decide whether "cleaning doesn't matter" is itself the story.

---

### Step 8: Full experiment (≈ 4–6 weeks, mostly compute time)

- **Do:** Run the complete grid:
  - all kept noise types, **including real-life noise**;
  - all noise levels;
  - all cleaners, with and without clean→clean training;
  - all kept tasks;
  - all four preparation modes;
  - 3 random seeds.
- **Inputs:** the same as Step 7.
- **Outputs:** `results/E3_full.csv`.
- **🧪 Experiment E3: full grid.**
- **Log:** `experiment_log.md` (E3 runs). Also note any runs that crashed and were re-run.
- **Decision?** No. Just run it.

---

### Step 9: Analyse: where does cleaning help, do nothing, or hurt? (≈ 2–3 weeks)

- **Do:**
  - Treat **each patient as one unit** so thousands of heartbeats from one person don't inflate confidence. Use a mixed-effects model, or bootstrap by patient.
  - Label every combination as **helps**, **no real difference** or **hurts**. "No real difference" means within an agreed margin, e.g. ±1% F1 or ±10 ms QT error.
  - Draw the "regime map": one heat-map per task, with noise level on one axis and preparation mode on the other.
  - Check P1, P2 and P3 against the map.
- **Inputs:** `results/E3_full.csv`.
- **Outputs:** `research/figures/regime_map_*.png` and `research/analysis_summary.md`.
- **Experiment?** No new runs; this is analysis only.
- **Log:** `experiment_log.md`, entry "A1-analysis", including the exact scripts and commits.
- **◆ Decision D5: What is the main message?** Record which predictions held, which failed, and what the one-sentence headline of the paper is.

---

### Step 10: Build and test the "clean only when needed" switch (≈ 2–3 weeks)

- **Do:**
  1. Compute a signal-quality score for each segment. Start with standard ECG quality indices; a small learned quality model is optional.
  2. Set two thresholds using **validation data only**:
     - quality high → **leave it alone**;
     - quality medium → **clean it**;
     - quality very low → **reject it as unusable**.
  3. Compare three policies on the test data: **never clean**, **always clean**, and **switch**.
- **Inputs:** cleaners and task models; quality score; the Step 9 findings on where cleaning hurts.
- **Outputs:** `results/E4_switch.csv`, plus a plot of task score vs % of data kept.
- **🧪 Experiment E4: switch vs always vs never.**
- **Log:** `experiment_log.md` (E4 runs).
- **◆ Decision D6: Is the switch a contribution?**
  - **Yes** if it beats both fixed policies, or matches the best one while rejecting only a small share of data.
  - **If not**, report it honestly as a negative result and let the regime map carry the paper.

---

### Step 11: Real-life check (≈ 2–4 weeks, depending on your own data)

- **Do:** Run the final setup (best cleaners, the switch, and all preparation modes) **without any re-tuning** on:
  - SimEMG, which has real muscle noise with a clean twin channel;
  - BUT QDB (everyday noise);
  - your own wearable recordings.

  Where no clean reference exists, judge by task success, e.g. heartbeat detection against labels, not by noise-reduction scores.
- **Inputs:** real-life datasets; models from earlier steps (frozen).
- **Outputs:** `results/E5_reallife.csv`.
- **🧪 Experiment E5: real-life noise.**
- **Log:** `experiment_log.md` (E5 runs).
- **Decision?** It feeds into D7. Note whether the regime map from computer-added noise **matches** real life. Either answer is a finding.

---

### Step 12: Write up and choose the venue (≈ 4–6 weeks)

- **Do:**
  - Write the paper around the regime map, the switch and the real-life check.
  - Release the code, split files, noise recipe and settings, so anyone can repeat the work.
  - Add a clear limitations section covering the small datasets, simulated noise, and the fact that we only tested the listed cleaners and tasks.
- **Inputs:** everything in `research/`.
- **Outputs:** paper draft and a public code repository.
- **Experiment?** No, apart from any extra runs reviewers ask for. Log those as E6.
- **◆ Decision D7: Where to submit?**

  | If… | Submit to |
  |---|---|
  | Strong regime map + working switch + real-life confirmation | **IEEE JBHI** |
  | Solid results but real-life part is thin | **Biomedical Signal Processing and Control** |
  | Only pilot-level results so far | **EMBC / BioCAS** (4 pages) |

---

## Sources

- [Seo et al. 2026, Sensors 26(16):5183 — doi 10.3390/s26165183](https://doi.org/10.3390/s26165183) · [PMC13517396](https://pmc.ncbi.nlm.nih.gov/articles/PMC13517396/) · [PubMed 42655490](https://pubmed.ncbi.nlm.nih.gov/42655490/)
- [Granese et al. 2023, "The Negative Impact of Denoising on Automated Classification of Electrocardiograms"](https://mlanthology.org/neuripsw/2023/granese2023neuripsw-negative/)
- [Cardio-NAFNet, medRxiv 2022](https://www.medrxiv.org/content/10.1101/2022.10.26.22281565v1)
- [Canine delineation preprint, arXiv 2605.03183](https://arxiv.org/abs/2605.03183)
- [Memory Classifiers for Robust ECG Classification against Physiological Noise (2023)](https://www.researchgate.net/publication/372498054_Memory_Classifiers_for_Robust_ECG_Classification_against_Physiological_Noise)
- [Reproducible benchmark of QRS detection algorithms, Sci Rep 2026](https://www.nature.com/articles/s41598-026-53724-9)