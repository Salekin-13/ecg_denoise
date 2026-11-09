# Pipeline status (2026-11-09)

Where the code side stands relative to `../Research_Plan.md`. Step 1 (novelty reading) is still in progress in parallel.

| Step | State | Evidence |
|---|---|---|
| 2 Data inventory | **Done** for MIT-BIH, NSTDB, QTDB. PTB-XL, SimEMG, wearable: not yet downloaded. | `data_inventory.md`, `results/data_inventory.csv` |
| 3 Fair splits | **Done.** Leakage check **PASS**: 133 patient groups, each in one split; NSTDB noise cut 60/20/20 in time. | `splits/split_check.txt`, `splits/*.csv` |
| 4 Noisy test sets | **Done** for test + val splits. 6 levels (clean, 24, 12, 6, 0, −6 dB) × 4 noise types (bw, ma, em, mix). Achieved SNR matches target to 1e-14 dB. | `results/E0_noise_build_*.csv`, `recipes/*.csv.gz`, `figures/noise_examples/*.png` |
| 5 Cleaners | **Preview only.** Cleaner #2 (Butterworth 0.5–40 Hz + notch) run on 300 random test windows per dataset. | `results/E1_preview_filter_*.csv`, `figures/E1_preview_filter_*.png` |

## What the Step 5 preview shows (MIT-BIH test, median over 300 windows)

| Input SNR | bw gain | ma gain | em gain | mix gain |
|---|---|---|---|---|
| −6 dB | +14.3 | +6.4 | +1.9 | +4.7 |
| 0 dB | +10.4 | +5.2 | +1.2 | +3.7 |
| 6 dB | +5.3 | +2.7 | +0.1 | +2.0 |
| 12 dB | −0.6 | −1.3 | −2.5 | −1.7 |
| 24 dB | −12.5 | −12.6 | −12.7 | −12.6 |

- The filter **helps** below roughly 10 dB input SNR and **hurts** above it. The crossover is around 6–12 dB for every noise type. Output SNR saturates near 11–13 dB regardless of input.
- On already-clean input the filter changes 98% of windows by more than 10% RMS (median output SNR vs original ≈ 11.5 dB). This is the direction prediction **P3** expects, but see the caveat.
- Baseline wander (bw) is the easiest noise for this filter; muscle artefact (em) the hardest, as expected since it overlaps the QRS band.

**Caveat (logged in `experiment_log.md`):** the MIT-BIH/QTDB "clean" references themselves contain baseline wander below 0.5 Hz and content above 40 Hz. Part of the measured "change on clean input" is the filter removing real reference content. Step 5 proper needs either an in-band metric or a cleaner reference before P3 can be claimed from this cleaner.

## Next
1. Finish Step 1 reading table → Decision D1.
2. Download PTB-XL and rerun Steps 2–4 with it (`--datasets ptbxl`).
3. Step 5 proper: tune DWT on the val split, train FCN-DAE, run E1 on all cleaners with the same script pattern as `step5_preview_filter.py`.
