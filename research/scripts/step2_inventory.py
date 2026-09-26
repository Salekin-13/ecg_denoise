"""Step 2 — Data inventory: what is in each dataset folder and which labels exist.

Run from the repo root:  python research/scripts/step2_inventory.py
Outputs: research/results/data_inventory.csv, research/data_inventory.md
"""
import ast
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import wfdb

from common import RESEARCH, append_log, find_records, load_paths

# Annotation file extensions worth knowing about (PhysioNet conventions).
ANN_EXT = {
    "atr": "reference beat labels",
    "q1c": "manual wave boundaries (cardiologist 1)",
    "q2c": "manual wave boundaries (cardiologist 2)",
    "pu": "automatic wave boundaries",
    "pu0": "automatic wave boundaries ch0",
    "pu1": "automatic wave boundaries ch1",
    "man": "manual beat annotations",
    "qrs": "QRS annotations",
    "ecg": "ECG annotations",
}
BEAT_SYMBOLS = set("NLRBAaJSVrFejnE/fQ?")

rows = []  # (dataset, item, value)


def add(ds, item, value):
    rows.append((ds, item, value))


def file_types(root):
    c = Counter(p.suffix.lower() or "(none)" for p in Path(root).rglob("*") if p.is_file())
    return ", ".join(f"{k}:{v}" for k, v in c.most_common(12))


def scan_wfdb(ds, root, max_headers=None):
    recs = find_records(root)
    add(ds, "wfdb_records", len(recs))
    if not recs:
        return recs
    sample = recs if max_headers is None else recs[:max_headers]
    fs, nsig, dur, names = Counter(), Counter(), [], Counter()
    for r in sample:
        try:
            h = wfdb.rdheader(str(r))
        except Exception as e:  # noqa: BLE001
            add(ds, f"header_error:{r.name}", str(e)[:80])
            continue
        fs[h.fs] += 1
        nsig[h.n_sig] += 1
        if h.sig_len and h.fs:
            dur.append(h.sig_len / h.fs)
        for s in h.sig_name or []:
            names[s] += 1
    add(ds, "sampling_rates_hz", dict(fs))
    add(ds, "n_channels", dict(nsig))
    add(ds, "channel_names_top", ", ".join(n for n, _ in names.most_common(12)))
    if dur:
        add(ds, "duration_sec_min/median/max", f"{min(dur):.1f} / {np.median(dur):.1f} / {max(dur):.1f}")
        add(ds, "total_hours", round(sum(dur) / 3600, 2))
    ann = Counter()
    for r in recs:
        for ext in ANN_EXT:
            if r.with_suffix("." + ext).exists():
                ann[ext] += 1
    for ext, n in ann.items():
        add(ds, f"records_with_.{ext} ({ANN_EXT[ext]})", n)
    return recs


def mitdb_extra(recs):
    beats = 0
    for r in recs:
        if r.with_suffix(".atr").exists():
            a = wfdb.rdann(str(r), "atr")
            beats += sum(s in BEAT_SYMBOLS for s in a.symbol)
    add("mitdb", "total_labelled_beats", beats)
    add("mitdb", "record_names", " ".join(r.name for r in recs))


def nstdb_extra(recs):
    names = {r.name: r for r in recs}
    for t in ["bw", "ma", "em"]:
        if t in names:
            h = wfdb.rdheader(str(names[t]))
            add("nstdb", f"noise_{t}", f"present, {h.sig_len / h.fs / 60:.1f} min @ {h.fs} Hz, {h.n_sig} ch")
        else:
            add("nstdb", f"noise_{t}", "MISSING — needed for Step 4")


def ptbxl_extra(root):
    csvs = list(Path(root).rglob("ptbxl_database.csv"))
    if not csvs:
        add("ptbxl", "ptbxl_database.csv", "NOT FOUND")
        return
    db = pd.read_csv(csvs[0])
    add("ptbxl", "ptbxl_database.csv", str(csvs[0]))
    add("ptbxl", "n_ecgs", len(db))
    add("ptbxl", "n_patients", db["patient_id"].nunique())
    add("ptbxl", "has_strat_fold", "strat_fold" in db.columns)
    codes = db["scp_codes"].apply(ast.literal_eval)
    for code in ["NORM", "SR", "AFIB", "AFLT", "STACH", "SBRAG", "PVC"]:
        add("ptbxl", f"ecgs_with_{code}", int(codes.apply(lambda d: code in d).sum()))
    for col in ["baseline_drift", "static_noise", "burst_noise", "electrodes_problems"]:
        if col in db.columns:
            add("ptbxl", f"ecgs_flagged_{col}", int(db[col].notna().sum()))
    # check the waveform files the CSV points to actually exist
    base = csvs[0].parent
    for col in ["filename_hr", "filename_lr"]:
        if col in db.columns:
            ok = sum((base / f).with_suffix(".hea").exists() for f in db[col].head(50))
            add("ptbxl", f"{col}_files_found_(first50)", ok)


def main():
    paths = load_paths()
    for ds, root in paths.items():
        if not root.exists():
            add(ds, "status", f"MISSING PATH {root}")
            continue
        add(ds, "status", "found")
        add(ds, "path", str(root))
        if root.is_file():
            add(ds, "note", "this is a file (zip?) — extract it first")
            continue
        add(ds, "file_types", file_types(root))
        big = ds in ("ptbxl", "ptbxl_plus", "medalcare")
        recs = scan_wfdb(ds, root, max_headers=300 if big else None)
        if ds == "mitdb" and recs:
            mitdb_extra(recs)
        if ds == "nstdb":
            nstdb_extra(recs)
        if ds == "ptbxl":
            ptbxl_extra(root)
        if ds in ("simemg", "wear", "ptbxl_plus", "medalcare") and not recs:
            add(ds, "note", "no WFDB records found — format needs a manual look (see file_types)")

    df = pd.DataFrame(rows, columns=["dataset", "item", "value"])
    out_csv = RESEARCH / "results" / "data_inventory.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)

    md = ["# Data inventory (auto-generated by step2_inventory.py)\n"]
    for ds, g in df.groupby("dataset", sort=False):
        md.append(f"\n## {ds}\n\n| Item | Value |\n|---|---|")
        md += [f"| {i} | {str(v).replace('|', '/')} |" for i, v in zip(g["item"], g["value"])]
    md.append(
        "\n\n## Task checklist (fill in by hand after reading the above — Decision D2)\n\n"
        "| Task | Added-noise dataset with labels | Real-life dataset with labels | Keep? |\n"
        "|---|---|---|---|\n"
        "| Heartbeat detection | MIT-BIH (.atr) | SimEMG / wear ? | ☐ |\n"
        "| Wave timing (QT, QRS width) | QTDB (.q1c) | ? | ☐ |\n"
        "| Rhythm classification (AF) | PTB-XL (scp_codes) | PTB-XL noise-flagged ECGs? | ☐ |\n"
    )
    (RESEARCH / "data_inventory.md").write_text("\n".join(md), encoding="utf-8")

    key = df[df["item"].isin(["status", "wfdb_records", "n_ecgs", "n_patients", "total_labelled_beats"])]
    nums = [f"{d}: {i} = {v}" for d, i, v in key.itertuples(index=False)]
    missing = [f"{d}: {v}" for d, i, v in df.itertuples(index=False) if "MISSING" in str(v)]
    append_log("E0-data-check", "Step 2 data inventory", "What data and labels do we have?",
               [str(out_csv.relative_to(RESEARCH.parent)), "research/data_inventory.md"], nums,
               problems="; ".join(missing), next_step="Fill task checklist in data_inventory.md, log Decision D2")
    for n in nums:
        print(n.encode("ascii", "replace").decode())
    print(f"\nWrote {out_csv} and research/data_inventory.md")


if __name__ == "__main__":
    main()
