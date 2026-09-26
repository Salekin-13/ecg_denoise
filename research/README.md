# Research pipeline: Steps 2–4

These scripts implement Steps 2, 3 and 4 of `../Research_Plan.md`. Run them **on the computer that holds the datasets**. They write small outputs (tables, split lists, recipes, figures, log entries) into this folder, so you can commit and push them for review. Large arrays go to `research/data_out/`, which git ignores.

## One-time setup

1. **Unzip what is still zipped** inside `datasets/`:
   - `mit-bih-arrhythmia-database-1.0.0.zip`: required, because Steps 3 and 4 read the MIT-BIH records;
   - `MedalCare-XL.zip`: optional, not used in Steps 2–4.

   A folder that holds the unzipped zip's contents is fine. The scripts search subfolders for the records.
2. **Install the Python packages** (Python 3.9+):
   ```
   pip install -r research/requirements.txt
   ```
3. **Tell the scripts where the data is:**
   ```
   copy research\config\paths.example.json research\config\paths.json
   ```
   Then open `paths.json` and check each folder. Paths are relative to the repo folder (`ecg_denoise`), and the defaults match your `datasets\` folder. `paths.json` is git-ignored because it is specific to your PC.

## Run (from the `ecg_denoise` folder)

| Step | Command | Time | Look at afterwards |
|---|---|---|---|
| 2 — data inventory | `python research/scripts/step2_inventory.py` | ~1 min | `research/data_inventory.md` |
| 3 — fair splits | `python research/scripts/step3_splits.py` | seconds | `research/splits/split_check.txt` (must say PASS) |
| 4 — noisy test set | `python research/scripts/step4_make_noisy.py` | ~5–20 min (PTB-XL is the slow part) | `research/figures/noise_examples/*.png`, `research/results/E0_noise_build_test.csv` |
| 4 — noisy val set | `python research/scripts/step4_make_noisy.py --split val` | same | same |

Useful options for Step 4:
- `--datasets mitdb qtdb`: skip PTB-XL for a quick first run.
- `--ptbxl-limit 200`: use only the first 200 PTB-XL test ECGs.
- `--save-noisy`: also save every noisy signal as an array. By default only the recipe is saved, and `common.make_noisy()` rebuilds any signal exactly from it.

Each script appends an entry to `research/logs/experiment_log.md`. Add your own notes under it.

## After running: decisions for you

- **D2 (Step 2):**
  - Open `research/data_inventory.md` and fill in the task checklist at the bottom.
  - The SimEMG and `wear` formats aren't known yet. If the inventory says "format needs a manual look", describe the files (or share one example) so a loader can be written.
  - Log D2 in `logs/decision_log.md`.
- **Step 3:** if `split_check.txt` says FAIL, stop and fix it before going on.
- **Step 4:** look at the example figures. The noisy signals should get visibly worse from 24 dB down to −6 dB, and the orange clean trace should line up under them.

## Then share

```
git add research
git commit -m "Run steps 2-4 on local data"
git push
```

`paths.json` and `data_out/` stay on your PC.
