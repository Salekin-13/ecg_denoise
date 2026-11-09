# Experiment log

One entry per run. The scripts in `research/scripts/` append their own entries here automatically; add your own notes under each one. Template (from `Research_Plan.md`, Part D):

```
### E#-run## — <short name>        Date: YYYY-MM-DD
- Question this run answers:
- Settings file: configs/<file>          Code version (git commit): <hash>
- Data + split used:
- Random seed(s):
- Result file: results/<file>.csv (rows added: <n>)
- What happened (numbers):
- Surprises / problems:
- What I'll do next:
```

---

### E0-data-check — Step 2 data inventory        Date: 2026-11-09
- Question this run answers: What data and labels do we have?
- Settings file: research/config/paths.json          Code version (git commit): deeeccd
- Result file(s): research/results/data_inventory.csv, research/data_inventory.md
- What happened (numbers):
  - mitdb: status = found
  - mitdb: wfdb_records = 48
  - mitdb: total_labelled_beats = 109494
  - nstdb: status = found
  - nstdb: wfdb_records = 15
  - qtdb: status = found
  - qtdb: wfdb_records = 105
- Surprises / problems: none noted by script — review manually
- What I'll do next: Fill task checklist in data_inventory.md, log Decision D2

### E0-split-check — Step 3 splits + leakage check        Date: 2026-11-09
- Question this run answers: Are train/val/test disjoint by patient and by noise segment?
- Settings file: research/config/paths.json          Code version (git commit): deeeccd
- Result file(s): research/splits/*.csv, research/splits/split_check.txt
- What happened (numbers):
  - seed=0
  - PASS: 133 patient groups, each in exactly one split (checked across MIT-BIH and QTDB together).
  - PASS: noise 'bw' train/val/test ranges do not overlap
  - PASS: noise 'em' train/val/test ranges do not overlap
  - PASS: noise 'ma' train/val/test ranges do not overlap
  - mitdb: {'test': '21 records / 21 patients', 'train': '19 records / 18 patients', 'val': '4 records / 4 patients'}
  - qtdb: {'test': '27 records / 27 patients', 'train': '57 records / 57 patients', 'val': '19 records / 19 patients'}
- Surprises / problems: none noted by script — review manually
- What I'll do next: Step 4: build noisy test signals

### E0-noise-build-test — Step 4 noisy signals (test)        Date: 2026-11-09
- Question this run answers: Are the noisy signals built correctly at the intended SNR levels?
- Settings file: research/config/paths.json          Code version (git commit): deeeccd
- Result file(s): research/results/E0_noise_build_test.csv, research/recipes/, research/figures/noise_examples/
- What happened (numbers):
  - mitdb: 3780 windows from 21 records @ 360 Hz; 75600 noisy signals; max |achieved-target SNR| = 7.11e-15 dB
  - qtdb: 2422 windows from 27 records @ 250 Hz; 48440 noisy signals; max |achieved-target SNR| = 7.11e-15 dB
  - seed=0, window=10.0s, SNRs=['clean', 24, 12, 6, 0, -6], ptbxl_skip_flagged=True
- Surprises / problems: none noted by script — review manually
- What I'll do next: Look at the example figures by eye, then Step 5 (cleaners)

### E0-noise-build-val — Step 4 noisy signals (val)        Date: 2026-11-09
- Question this run answers: Are the noisy signals built correctly at the intended SNR levels?
- Settings file: research/config/paths.json          Code version (git commit): deeeccd
- Result file(s): research/results/E0_noise_build_val.csv, research/recipes/, research/figures/noise_examples/
- What happened (numbers):
  - mitdb: 720 windows from 4 records @ 360 Hz; 14400 noisy signals; max |achieved-target SNR| = 7.11e-15 dB
  - qtdb: 1698 windows from 19 records @ 250 Hz; 33960 noisy signals; max |achieved-target SNR| = 7.11e-15 dB
  - seed=0, window=10.0s, SNRs=['clean', 24, 12, 6, 0, -6], ptbxl_skip_flagged=True
- Surprises / problems: none noted by script — review manually
- What I'll do next: Look at the example figures by eye, then Step 5 (cleaners)

### E1-preview-filter-mitdb — Step 5 preview: standard filter on Step 4 test set        Date: 2026-11-09
- Question this run answers: Does the simplest cleaner improve SNR, and does it distort clean signals (P3)?
- Settings file: research/config/paths.json          Code version (git commit): 4b466a4
- Result file(s): research/results/E1_preview_filter_mitdb.csv, research/figures/E1_preview_filter_mitdb.png
- What happened (numbers):
  - 300 random test windows, seed=0, fs=360
  - bw @  -6 dB: median out   8.3 dB, gain +14.3 dB, worse in   0% of windows
  - bw @   0 dB: median out  10.4 dB, gain +10.4 dB, worse in   0% of windows
  - bw @   6 dB: median out  11.3 dB, gain  +5.3 dB, worse in  19% of windows
  - bw @  12 dB: median out  11.4 dB, gain  -0.6 dB, worse in  54% of windows
  - bw @  24 dB: median out  11.5 dB, gain -12.5 dB, worse in 100% of windows
  - em @  -6 dB: median out  -4.1 dB, gain  +1.9 dB, worse in   2% of windows
  - em @   0 dB: median out   1.2 dB, gain  +1.2 dB, worse in  14% of windows
  - em @   6 dB: median out   6.1 dB, gain  +0.1 dB, worse in  47% of windows
  - em @  12 dB: median out   9.5 dB, gain  -2.5 dB, worse in  84% of windows
  - em @  24 dB: median out  11.3 dB, gain -12.7 dB, worse in 100% of windows
  - ma @  -6 dB: median out   0.4 dB, gain  +6.4 dB, worse in   0% of windows
  - ma @   0 dB: median out   5.2 dB, gain  +5.2 dB, worse in   1% of windows
  - ma @   6 dB: median out   8.7 dB, gain  +2.7 dB, worse in  23% of windows
  - ma @  12 dB: median out  10.7 dB, gain  -1.3 dB, worse in  67% of windows
  - ma @  24 dB: median out  11.4 dB, gain -12.6 dB, worse in 100% of windows
  - mix @  -6 dB: median out  -1.3 dB, gain  +4.7 dB, worse in   0% of windows
  - mix @   0 dB: median out   3.7 dB, gain  +3.7 dB, worse in   1% of windows
  - mix @   6 dB: median out   8.0 dB, gain  +2.0 dB, worse in  28% of windows
  - mix @  12 dB: median out  10.3 dB, gain  -1.7 dB, worse in  69% of windows
  - mix @  24 dB: median out  11.4 dB, gain -12.6 dB, worse in 100% of windows
  - CLEAN input: filter output SNR vs original = 11.5 dB median (min 0.7); relative distortion 0.267 median, 98% of windows changed by >10% RMS
- Surprises / problems: Caveat: the 'clean' reference records themselves contain baseline wander below 0.5 Hz and content above 40 Hz, so part of the measured change on clean input is the filter removing real reference content, not only distortion. Needs a cleaner reference (or in-band metrics) in Step 5 proper.
- What I'll do next: Step 5 proper: tune DWT on val split, train FCN-DAE; then E1 on all cleaners

### E1-preview-filter-qtdb — Step 5 preview: standard filter on Step 4 test set        Date: 2026-11-09
- Question this run answers: Does the simplest cleaner improve SNR, and does it distort clean signals (P3)?
- Settings file: research/config/paths.json          Code version (git commit): 4b466a4
- Result file(s): research/results/E1_preview_filter_qtdb.csv, research/figures/E1_preview_filter_qtdb.png
- What happened (numbers):
  - 300 random test windows, seed=0, fs=250
  - bw @  -6 dB: median out   9.3 dB, gain +15.3 dB, worse in   0% of windows
  - bw @   0 dB: median out  11.6 dB, gain +11.6 dB, worse in   1% of windows
  - bw @   6 dB: median out  12.9 dB, gain  +6.9 dB, worse in   8% of windows
  - bw @  12 dB: median out  13.2 dB, gain  +1.2 dB, worse in  42% of windows
  - bw @  24 dB: median out  13.3 dB, gain -10.7 dB, worse in  99% of windows
  - em @  -6 dB: median out  -4.3 dB, gain  +1.7 dB, worse in   1% of windows
  - em @   0 dB: median out   1.4 dB, gain  +1.4 dB, worse in   9% of windows
  - em @   6 dB: median out   6.6 dB, gain  +0.6 dB, worse in  33% of windows
  - em @  12 dB: median out  10.7 dB, gain  -1.3 dB, worse in  75% of windows
  - em @  24 dB: median out  13.1 dB, gain -10.9 dB, worse in 100% of windows
  - ma @  -6 dB: median out   0.6 dB, gain  +6.6 dB, worse in   0% of windows
  - ma @   0 dB: median out   5.7 dB, gain  +5.7 dB, worse in   1% of windows
  - ma @   6 dB: median out   9.8 dB, gain  +3.8 dB, worse in  13% of windows
  - ma @  12 dB: median out  12.2 dB, gain  +0.2 dB, worse in  50% of windows
  - ma @  24 dB: median out  13.3 dB, gain -10.7 dB, worse in 100% of windows
  - mix @  -6 dB: median out  -1.0 dB, gain  +5.0 dB, worse in   0% of windows
  - mix @   0 dB: median out   4.4 dB, gain  +4.4 dB, worse in   2% of windows
  - mix @   6 dB: median out   8.9 dB, gain  +2.9 dB, worse in  16% of windows
  - mix @  12 dB: median out  11.8 dB, gain  -0.2 dB, worse in  51% of windows
  - mix @  24 dB: median out  13.3 dB, gain -10.7 dB, worse in 100% of windows
  - CLEAN input: filter output SNR vs original = 13.4 dB median (min -0.4); relative distortion 0.215 median, 94% of windows changed by >10% RMS
- Surprises / problems: Caveat: the 'clean' reference records themselves contain baseline wander below 0.5 Hz and content above 40 Hz, so part of the measured change on clean input is the filter removing real reference content, not only distortion. Needs a cleaner reference (or in-band metrics) in Step 5 proper.
- What I'll do next: Step 5 proper: tune DWT on val split, train FCN-DAE; then E1 on all cleaners
