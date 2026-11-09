"""Step 5 preview — the simplest cleaner (Butterworth band-pass + 60 Hz notch) on the Step 4 test set.

A quick first look at Experiment E1 with cleaner #2 ("standard filter") only. It answers two
questions on a random sample of noisy test windows:
  1. How much SNR does the filter gain at each input SNR, per noise type?
  2. How much does it change an already CLEAN signal (prediction P3: cleaning can hurt)?

Run from the repo root (after step4_make_noisy.py):
    python research/scripts/step5_preview_filter.py [--dataset mitdb] [--n-windows 300]
Outputs: research/results/E1_preview_filter_<dataset>.csv, research/figures/E1_preview_filter_<dataset>.png
"""
import argparse

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import butter, iirnotch, sosfiltfilt, filtfilt

from common import DATA_OUT, DEFAULT_SNRS, NOISE_TYPES, RESEARCH, append_log, make_noisy, power, snr_db


def standard_filter(x, fs, lo=0.5, hi=40.0, notch_hz=60.0):
    """Zero-phase 4th-order Butterworth band-pass (0.5-40 Hz) + notch at the mains frequency."""
    sos = butter(4, [lo, hi], btype="bandpass", fs=fs, output="sos")
    y = sosfiltfilt(sos, x)
    b, a = iirnotch(notch_hz, Q=30, fs=fs)
    return filtfilt(b, a, y)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="mitdb")
    ap.add_argument("--split", default="test")
    ap.add_argument("--n-windows", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)

    clean = np.load(DATA_OUT / f"{args.dataset}_{args.split}_clean.npz")
    X, fs = clean["X"].astype(np.float64), int(clean["fs"])
    bank = dict(np.load(DATA_OUT / f"noise_bank_{args.split}_{fs}.npz"))
    recipes = pd.read_csv(RESEARCH / "recipes" / f"{args.dataset}_{args.split}.csv.gz")
    pick = rng.choice(len(X), size=min(args.n_windows, len(X)), replace=False)

    rows = []
    for wid in pick:
        x = X[wid]
        sub = recipes[recipes.window_id == wid]
        for r in sub.itertuples():
            noisy = make_noisy(x, bank, r._asdict())
            cleaned = standard_filter(noisy, fs)
            snr_in = np.inf if r.noise_type == "none" else snr_db(x, noisy - x)
            rows.append({"window_id": wid, "record": r.record, "noise_type": r.noise_type,
                         "snr_db": r.snr_db, "snr_in_db": snr_in, "snr_out_db": snr_db(x, cleaned - x),
                         "rmse_noisy": float(np.sqrt(np.mean((noisy - x) ** 2))),
                         "rmse_cleaned": float(np.sqrt(np.mean((cleaned - x) ** 2))),
                         # mean-removed, so a DC-offset change alone does not count as distortion
                         "rel_distortion": float(np.sqrt(power(cleaned - x) / power(x)))})
    df = pd.DataFrame(rows)
    df["snr_gain_db"] = df["snr_out_db"] - df["snr_in_db"]

    out_csv = RESEARCH / "results" / f"E1_preview_filter_{args.dataset}.csv"
    df.to_csv(out_csv, index=False)

    # --- summary table -------------------------------------------------------------------
    noisy = df[df.noise_type != "none"].copy()
    noisy["snr_db"] = noisy["snr_db"].astype(int)
    summ = noisy.groupby(["noise_type", "snr_db"]).agg(
        snr_out_db=("snr_out_db", "median"), snr_gain_db=("snr_gain_db", "median"),
        frac_worse=("snr_gain_db", lambda g: float((g < 0).mean()))).reset_index()
    cl = df[df.noise_type == "none"]
    clean_line = (f"CLEAN input: filter output SNR vs original = {cl.snr_out_db.median():.1f} dB median "
                  f"(min {cl.snr_out_db.min():.1f}); relative distortion {cl.rel_distortion.median():.3f} median, "
                  f"{(cl.rel_distortion > 0.1).mean() * 100:.0f}% of windows changed by >10% RMS")

    # --- figure --------------------------------------------------------------------------
    levels = [s for s in DEFAULT_SNRS if s != "clean"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for t in NOISE_TYPES + ["mix"]:
        g = summ[summ.noise_type == t].set_index("snr_db").reindex(levels)
        axes[0].plot(levels, g["snr_out_db"], marker="o", label=t)
        axes[1].plot(levels, g["snr_gain_db"], marker="o", label=t)
    axes[0].plot(levels, levels, "k--", lw=0.8, label="no change")
    axes[0].set_xlabel("input SNR (dB)"); axes[0].set_ylabel("output SNR after filter (dB), median")
    axes[0].set_title(f"{args.dataset} {args.split}: Butterworth 0.5–40 Hz + notch")
    axes[1].axhline(0, color="k", lw=0.8, ls="--")
    axes[1].set_xlabel("input SNR (dB)"); axes[1].set_ylabel("SNR gain (dB), median")
    axes[1].set_title(f"clean input: median output SNR {cl.snr_out_db.median():.0f} dB, "
                      f"{(cl.rel_distortion > 0.1).mean() * 100:.0f}% windows changed >10% RMS", fontsize=9)
    for ax in axes:
        ax.invert_xaxis(); ax.grid(alpha=0.3); ax.legend(fontsize=8)
    fig.tight_layout()
    out_png = RESEARCH / "figures" / f"E1_preview_filter_{args.dataset}.png"
    fig.savefig(out_png, dpi=110)

    lines = [f"{r.noise_type} @ {r.snr_db:>3} dB: median out {r.snr_out_db:5.1f} dB, gain {r.snr_gain_db:+5.1f} dB, "
             f"worse in {r.frac_worse * 100:3.0f}% of windows" for r in summ.itertuples()]
    caveat = ("Caveat: the 'clean' reference records themselves contain baseline wander below 0.5 Hz and "
              "content above 40 Hz, so part of the measured change on clean input is the filter removing "
              "real reference content, not only distortion. Needs a cleaner reference (or in-band metrics) in Step 5 proper.")
    print("\n".join(lines)); print(clean_line); print(caveat)
    append_log(f"E1-preview-filter-{args.dataset}", "Step 5 preview: standard filter on Step 4 test set",
               "Does the simplest cleaner improve SNR, and does it distort clean signals (P3)?",
               [str(out_csv.relative_to(RESEARCH.parent)), str(out_png.relative_to(RESEARCH.parent))],
               [f"{len(pick)} random {args.split} windows, seed={args.seed}, fs={fs}"] + lines + [clean_line],
               problems=caveat, next_step="Step 5 proper: tune DWT on val split, train FCN-DAE; then E1 on all cleaners")


if __name__ == "__main__":
    main()
