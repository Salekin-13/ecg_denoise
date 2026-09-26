"""Step 4 — Build noisy signals from clean windows + held-out NSTDB noise.

Run from the repo root:
    python research/scripts/step4_make_noisy.py                 # test split, all datasets
    python research/scripts/step4_make_noisy.py --split val     # validation split

What it does
- Cuts each clean record of the chosen split into non-overlapping 10 s windows (1 channel:
  MIT-BIH/QTDB channel 0, PTB-XL lead II).
- For every window and noise type (bw, ma, em, mix) it draws ONE random noise segment from the
  split's own part of NSTDB (Step 3), resampled to the dataset's sampling rate, and scales it
  to each SNR level. The same noise segment is used at every SNR, so levels are paired.
- SNR = 10*log10(P_clean / P_noise), powers computed after removing the mean.
- 'mix' = bw + ma + em, each scaled to unit power, summed and divided by sqrt(3).

Outputs
- research/recipes/<dataset>_<split>.csv.gz   exact recipe per noisy signal (commit this)
- research/data_out/<dataset>_<split>_clean.npz and noise_bank_<split>_<fs>.npz (local only)
- research/results/E0_noise_build_<split>.csv  achieved-SNR check
- research/figures/noise_examples/<dataset>_<type>.png   5 random windows x all levels
Use common.make_noisy(clean_window, bank, recipe_row) to rebuild any noisy signal exactly.
"""
import argparse

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import wfdb

from common import (DATA_OUT, DEFAULT_SNRS, NOISE_TYPES, RESEARCH, append_log, build_noise,
                    find_records, load_paths, make_noisy, noise_scale, power, resample, snr_db)

SPLITS = RESEARCH / "splits"
NOISE_FLAG_COLS = ["baseline_drift", "static_noise", "burst_noise", "electrodes_problems"]


def windows_from_signal(sig, fs, win_sec, max_windows):
    L = int(round(win_sec * fs))
    out = []
    for start in range(0, len(sig) - L + 1, L):
        w = sig[start:start + L]
        if np.isnan(w).any() or power(w) == 0:
            continue
        out.append((start, w))
        if max_windows and len(out) >= max_windows:
            break
    return out


def load_clean(ds, split, paths, args):
    """Return (fs, list of dict(record, start, x))."""
    items, fs = [], None
    if ds in ("mitdb", "qtdb"):
        table = pd.read_csv(SPLITS / f"{ds}.csv", dtype={"record": str})
        wanted = set(table.loc[table["split"] == split, "record"])
        for r in find_records(paths[ds]):
            if r.name not in wanted:
                continue
            rec = wfdb.rdrecord(str(r), channels=[0])
            fs = rec.fs
            for start, w in windows_from_signal(rec.p_signal[:, 0], rec.fs, args.window_sec,
                                                args.max_windows_per_record):
                items.append({"record": r.name, "start_sample": start, "x": w})
    elif ds == "ptbxl":
        table = pd.read_csv(SPLITS / "ptbxl.csv", dtype={"record": str})
        table = table[table["split"] == split]
        csv = next(paths["ptbxl"].rglob("ptbxl_database.csv"))
        base = csv.parent
        if args.ptbxl_skip_flagged:
            db = pd.read_csv(csv, dtype={"ecg_id": str})
            flagged = db[db[[c for c in NOISE_FLAG_COLS if c in db.columns]].notna().any(axis=1)]
            table = table[~table["record"].isin(set(flagged["ecg_id"]))]
        col = "filename_hr" if args.ptbxl_fs == 500 else "filename_lr"
        if args.ptbxl_limit:
            table = table.head(args.ptbxl_limit)
        for rid, fn in zip(table["record"], table[col]):
            rec = wfdb.rdrecord(str(base / fn), channel_names=[args.ptbxl_lead])
            fs = rec.fs
            for start, w in windows_from_signal(rec.p_signal[:, 0], rec.fs, args.window_sec, 1):
                items.append({"record": rid, "start_sample": start, "x": w})
    return fs, items


def noise_bank(split, fs, paths):
    ranges = pd.read_csv(SPLITS / "nstdb_noise.csv")
    recs = {r.name: r for r in find_records(paths["nstdb"])}
    bank = {}
    for t in NOISE_TYPES:
        row = ranges[(ranges["noise_record"] == t) & (ranges["split"] == split)].iloc[0]
        rec = wfdb.rdrecord(str(recs[t]), channels=[0], sampfrom=int(row.start_sample),
                            sampto=int(row.end_sample))
        bank[t] = resample(rec.p_signal[:, 0], rec.fs, fs)
    return bank


def build_recipes(ds, split, items, bank, fs, snrs, rng):
    L = len(items[0]["x"])
    rows = []
    for wid, it in enumerate(items):
        base = {"dataset": ds, "split": split, "window_id": wid, "record": it["record"],
                "start_sample": it["start_sample"], "fs": fs}
        rows.append({**base, "noise_type": "none", "snr_db": "clean", "start_bw": -1, "start_ma": -1,
                     "start_em": -1, "scale": 0.0, "achieved_snr_db": np.inf})
        for t in NOISE_TYPES + ["mix"]:
            used = NOISE_TYPES if t == "mix" else [t]
            starts = {k: (int(rng.integers(0, len(bank[k]) - L)) if k in used else -1) for k in NOISE_TYPES}
            n = build_noise(bank, t, {k: v for k, v in starts.items() if v >= 0}, L)
            for s in snrs:
                if s == "clean":
                    continue
                k = noise_scale(it["x"], n, float(s))
                rows.append({**base, "noise_type": t, "snr_db": s, **{f"start_{k2}": v for k2, v in starts.items()},
                             "scale": k, "achieved_snr_db": snr_db(it["x"], k * n)})
    return pd.DataFrame(rows)


def plot_examples(ds, items, bank, recipes, fs, snrs, rng):
    outdir = RESEARCH / "figures" / "noise_examples"
    outdir.mkdir(parents=True, exist_ok=True)
    pick = rng.choice(len(items), size=min(5, len(items)), replace=False)
    show = int(3 * fs)
    t = np.arange(show) / fs
    for ntype in NOISE_TYPES + ["mix"]:
        fig, axes = plt.subplots(len(pick), len(snrs), figsize=(3 * len(snrs), 1.8 * len(pick)),
                                 sharex=True, squeeze=False)
        for i, wid in enumerate(pick):
            for j, s in enumerate(snrs):
                if s == "clean":
                    row = recipes[(recipes.window_id == wid) & (recipes.noise_type == "none")].iloc[0]
                else:
                    row = recipes[(recipes.window_id == wid) & (recipes.noise_type == ntype)
                                  & (recipes.snr_db.astype(str) == str(s))].iloc[0]
                y = make_noisy(items[wid]["x"], bank, row.to_dict())
                ax = axes[i, j]
                ax.plot(t, y[:show], lw=0.7)
                ax.plot(t, items[wid]["x"][:show], lw=0.5, alpha=0.6)
                if i == 0:
                    ax.set_title(f"{s} dB" if s != "clean" else "clean")
                if j == 0:
                    ax.set_ylabel(str(items[wid]["record"]), fontsize=7)
        fig.suptitle(f"{ds} — {ntype} (blue: noisy, orange: clean), first 3 s")
        fig.tight_layout()
        fig.savefig(outdir / f"{ds}_{ntype}.png", dpi=90)
        plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="test", choices=["train", "val", "test"])
    ap.add_argument("--datasets", nargs="+", default=["mitdb", "qtdb", "ptbxl"])
    ap.add_argument("--window-sec", type=float, default=10.0)
    ap.add_argument("--max-windows-per-record", type=int, default=0, help="0 = all windows")
    ap.add_argument("--ptbxl-fs", type=int, default=500, choices=[100, 500])
    ap.add_argument("--ptbxl-lead", default="II")
    ap.add_argument("--ptbxl-limit", type=int, default=0, help="0 = all records in split")
    ap.add_argument("--ptbxl-skip-flagged", action=argparse.BooleanOptionalAction, default=True,
                    help="skip PTB-XL ECGs flagged for drift/static/burst noise/electrode problems")
    ap.add_argument("--save-noisy", action="store_true", help="also save all noisy arrays (large)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    snrs = DEFAULT_SNRS
    rng = np.random.default_rng(args.seed)
    paths = load_paths()
    DATA_OUT.mkdir(parents=True, exist_ok=True)
    (RESEARCH / "recipes").mkdir(parents=True, exist_ok=True)

    summary, numbers = [], []
    for ds in args.datasets:
        if ds not in paths or not (SPLITS / f"{ds}.csv").exists():
            print(f"skip {ds}: no path or no split file")
            continue
        fs, items = load_clean(ds, args.split, paths, args)
        if not items:
            print(f"skip {ds}: no windows")
            continue
        bank = noise_bank(args.split, fs, paths)
        np.savez_compressed(DATA_OUT / f"noise_bank_{args.split}_{int(fs)}.npz", **bank)
        X = np.stack([it["x"] for it in items]).astype(np.float32)
        np.savez_compressed(DATA_OUT / f"{ds}_{args.split}_clean.npz", X=X,
                            record=np.array([it["record"] for it in items]),
                            start_sample=np.array([it["start_sample"] for it in items]), fs=fs)
        rec = build_recipes(ds, args.split, items, bank, fs, snrs, rng)
        rec.to_csv(RESEARCH / "recipes" / f"{ds}_{args.split}.csv.gz", index=False)
        if args.save_noisy:
            for t in NOISE_TYPES + ["mix"]:
                arr = {}
                for s in snrs[1:]:
                    sub = rec[(rec.noise_type == t) & (rec.snr_db.astype(str) == str(s))]
                    arr[f"snr_{s}"] = np.stack([make_noisy(items[r.window_id]["x"], bank, r._asdict())
                                                for r in sub.itertuples()]).astype(np.float32)
                np.savez_compressed(DATA_OUT / f"{ds}_{args.split}_{t}.npz", **arr)
        noisy = rec[rec.noise_type != "none"]
        err = (noisy["achieved_snr_db"] - noisy["snr_db"].astype(float)).abs()
        s = {"dataset": ds, "split": args.split, "fs": fs, "windows": len(items),
             "records": len({it["record"] for it in items}), "noisy_signals": len(noisy),
             "max_snr_error_db": float(err.max())}
        summary.append(s)
        numbers.append(f"{ds}: {s['windows']} windows from {s['records']} records @ {fs} Hz; "
                       f"{s['noisy_signals']} noisy signals; max |achieved-target SNR| = {s['max_snr_error_db']:.2e} dB")
        plot_examples(ds, items, bank, rec, fs, snrs, rng)
        print(numbers[-1])

    out = RESEARCH / "results" / f"E0_noise_build_{args.split}.csv"
    pd.DataFrame(summary).to_csv(out, index=False)
    bad = [s for s in summary if s["max_snr_error_db"] > 0.01]
    append_log(f"E0-noise-build-{args.split}", f"Step 4 noisy signals ({args.split})",
               "Are the noisy signals built correctly at the intended SNR levels?",
               [str(out.relative_to(RESEARCH.parent)), "research/recipes/", "research/figures/noise_examples/"],
               numbers + [f"seed={args.seed}, window={args.window_sec}s, SNRs={snrs}, "
                          f"ptbxl_skip_flagged={args.ptbxl_skip_flagged}"],
               problems="SNR mismatch > 0.01 dB in " + ", ".join(b["dataset"] for b in bad) if bad else "",
               next_step="Look at the example figures by eye, then Step 5 (cleaners)")


if __name__ == "__main__":
    main()
