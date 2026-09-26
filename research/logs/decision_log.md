# Decision log

One entry per decision point (D0–D7 in `Research_Plan.md`). Template:

```
### D# — <decision name>            Date: YYYY-MM-DD
- Question:
- Evidence looked at (link to log entries / result files):
- Options considered:
- Decision taken:
- Why:
- What would make me revisit this:
```

---

### D0 — Predictions locked            Date: 2026-09-26
- Question: What do we expect before running anything?
- Decision taken: These predictions are fixed and must not be edited afterwards.
  - **P1:** Cleaning helps when noise is moderate or heavy **and** the task model was trained only on clean signals.
  - **P2:** Cleaning makes little difference when the task model was trained on noisy signals.
  - **P3:** Cleaning **hurts** when the signal is already clean or nearly clean.
  - **Proven wrong if:** cleaning makes no difference anywhere, and the quality switch is no better than "never clean".
- Why: pre-registering stops us from reshaping the story after seeing results.

### Pipeline choices made while writing the Step 3–4 scripts   Date: 2026-09-26
Review these and confirm or change them when you log D2.
- **MIT-BIH split:** the standard inter-patient DS1 (train) / DS2 (test) split, with 4 DS1 records held out as validation. Record 202 is moved to train because it comes from the same patient as record 201. Paced records 102, 104, 107 and 217 are excluded.
- **QTDB:** records sel100–sel234 are excerpts of MIT-BIH records, so each one follows its MIT-BIH patient's split. The remaining QTDB records are split 60/20/20 at random (seed 0).
- **PTB-XL:** the official patient-wise folds: 1–8 train, 9 val, 10 test. Test ECGs flagged for drift, static noise, burst noise or electrode problems are skipped before noise is added, because they aren't a clean starting point.
- **NSTDB noise:** each noise recording is cut in time: 60% train, 20% val, 20% test.
- **SNR:** power ratio after removing the mean. The "mix" noise is bw + ma + em at equal power. The same noise segment is used at every SNR level for a given window, so the levels are directly comparable.
- **Windows:** non-overlapping 10 s windows from channel 0 (MIT-BIH, QTDB) or lead II (PTB-XL).
- **Evaluation only:** SimEMG and the own wearable data are held back for the Step 11 real-life check, so they get no split.
