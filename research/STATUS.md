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

- Below about 6 dB input SNR the filter clearly **helps**; the gain is largest for bw and smallest for em (electrode motion, which overlaps the QRS band). ma = muscle artefact.
- Above about 12 dB the measured output SNR is *lower* than the input, by the same amount for every noise type. This is **not** evidence that the filter hurts: see the caveat.
- On already-clean input the filter output sits at a median 11.5 dB (mitdb) / 13.4 dB (qtdb) SNR against the original. Per-record medians range from about 4 to 18 dB (mitdb).

**Caveat (worked through in `notebooks/01_results_steps2to5.ipynb`, logged in `experiment_log.md`):** the filter is linear, so error = (Hx - x) + Hn. The first term, what the filter does to the "clean" reference itself, caps the output SNR at about 11.5 / 13.4 dB and dominates the error at every input SNR of 12 dB and above (and at all levels for bw). About 58% of that removed power is the reference's own baseline wander below 0.5 Hz, about 29% is in-band attenuation. On top of that, filtering 10 s windows adds a start-up transient (edge error about 2.5x the middle), and the 60 Hz notch misses the 50 Hz mains in the QTDB `sele*` records. So the high-SNR "loss" and the clean-input change cannot be read as support for P3 yet. Step 5 proper needs: an in-band metric (or cleaner reference), filtering of whole records before windowing, per-record mains frequency, and per-record aggregation (300 windows from 21 records are not 300 samples).

## Next
1. Finish Step 1 reading table → Decision D1.
2. Download PTB-XL and rerun Steps 2–4 with it (`--datasets ptbxl`).
3. Step 5 proper: tune DWT on the val split, train FCN-DAE, run E1 on all cleaners with the same script pattern as `step5_preview_filter.py`.
