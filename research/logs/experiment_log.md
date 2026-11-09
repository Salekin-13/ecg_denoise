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
