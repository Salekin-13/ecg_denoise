"""Step 3 — Fair train/val/test splits (by patient, and by noise segment).

Run from the repo root:  python research/scripts/step3_splits.py [--seed 0]
Outputs: research/splits/{mitdb,qtdb,ptbxl,nstdb_noise}.csv, research/splits/split_check.txt

Rules
- MIT-BIH: inter-patient DS1/DS2 split of de Chazal et al. (2004). DS1 -> train (+ a few
  records held out for validation), DS2 -> test. Records 201 and 202 come from the SAME
  patient but sit in DS1 and DS2 in the original split; we move 202 to train to avoid leakage.
  Paced records 102, 104, 107, 217 are excluded (AAMI convention).
- QTDB: records named sel1xx/sel2xx are excerpts of MIT-BIH records, so they inherit the
  MIT-BIH record's split. The rest are split 60/20/20 by record.
- PTB-XL: authors' patient-wise strat_fold: 1-8 train, 9 val, 10 test.
- NSTDB noise (bw, ma, em): each recording cut in time: first 60% train, next 20% val, last 20% test.
- SimEMG / own wearable data: evaluation-only (Step 11), no split.
"""
import argparse
import re

import numpy as np
import pandas as pd
import wfdb

from common import RESEARCH, append_log, find_records, load_paths

DS1 = [101, 106, 108, 109, 112, 114, 115, 116, 118, 119, 122, 124, 201, 203, 205, 207, 208,
       209, 215, 220, 223, 230]
DS2 = [100, 103, 105, 111, 113, 117, 121, 123, 200, 202, 210, 212, 213, 214, 219, 221, 222,
       228, 231, 232, 233, 234]
PACED = [102, 104, 107, 217]
SAME_SUBJECT = {202: 201}  # record -> record it shares a patient with
N_VAL_MITDB = 4
OUT = RESEARCH / "splits"


def mitdb_group(rec):
    rec = int(rec)
    return f"mitdb_{SAME_SUBJECT.get(rec, rec)}"


def split_mitdb(rng):
    train = [r for r in DS1] + [202]
    test = [r for r in DS2 if r != 202]
    candidates = [r for r in train if r not in (201, 202)]
    val = sorted(rng.choice(candidates, N_VAL_MITDB, replace=False).tolist())
    rows = []
    for r in sorted(set(train) | set(test) | set(PACED)):
        split = "excluded_paced" if r in PACED else "val" if r in val else "train" if r in train else "test"
        rows.append({"dataset": "mitdb", "record": str(r), "group": mitdb_group(r), "split": split})
    return pd.DataFrame(rows)


def split_qtdb(recs, mitdb_df, rng):
    mit_split = dict(zip(mitdb_df["group"], mitdb_df["split"]))
    rows, others = [], []
    for r in recs:
        m = re.fullmatch(r"sel(\d{3})", r.name)
        if m and 100 <= int(m.group(1)) <= 234:
            g = mitdb_group(m.group(1))
            rows.append({"dataset": "qtdb", "record": r.name, "group": g,
                         "split": mit_split.get(g, "excluded_paced"),
                         "has_q1c": r.with_suffix(".q1c").exists()})
        else:
            others.append(r)
    order = rng.permutation(len(others))
    n = len(others)
    cut1, cut2 = int(round(0.6 * n)), int(round(0.8 * n))
    for rank, i in enumerate(order):
        r = others[i]
        split = "train" if rank < cut1 else "val" if rank < cut2 else "test"
        rows.append({"dataset": "qtdb", "record": r.name, "group": f"qtdb_{r.name}",
                     "split": split, "has_q1c": r.with_suffix(".q1c").exists()})
    return pd.DataFrame(rows)


def split_ptbxl(root):
    csvs = list(root.rglob("ptbxl_database.csv"))
    if not csvs:
        return None
    db = pd.read_csv(csvs[0])
    split = db["strat_fold"].map(lambda f: "test" if f == 10 else "val" if f == 9 else "train")
    return pd.DataFrame({"dataset": "ptbxl", "record": db["ecg_id"].astype(str),
                         "group": "ptbxl_p" + db["patient_id"].astype(int).astype(str),
                         "split": split, "filename_hr": db["filename_hr"], "filename_lr": db["filename_lr"]})


def split_noise(recs):
    names = {r.name: r for r in recs}
    rows = []
    for t in ["bw", "ma", "em"]:
        if t not in names:
            raise SystemExit(f"NSTDB noise record '{t}' not found — check paths.json")
        h = wfdb.rdheader(str(names[t]))
        n = h.sig_len
        bounds = [0, int(0.6 * n), int(0.8 * n), n]
        for split, a, b in zip(["train", "val", "test"], bounds[:-1], bounds[1:]):
            rows.append({"noise_record": t, "split": split, "start_sample": a, "end_sample": b,
                         "fs": h.fs, "minutes": round((b - a) / h.fs / 60, 2)})
    return pd.DataFrame(rows)


def check(frames, noise):
    """Leakage check: no patient group in two splits; noise ranges do not overlap."""
    lines, ok = [], True
    allrec = pd.concat([f[["dataset", "record", "group", "split"]] for f in frames])
    allrec = allrec[allrec["split"].isin(["train", "val", "test"])]
    multi = allrec.groupby("group")["split"].nunique()
    bad = multi[multi > 1]
    if len(bad):
        ok = False
        lines.append(f"FAIL: {len(bad)} patient groups appear in more than one split: {list(bad.index)[:10]}")
    else:
        lines.append(f"PASS: {allrec['group'].nunique()} patient groups, each in exactly one split "
                     "(checked across MIT-BIH and QTDB together).")
    for t, g in noise.groupby("noise_record"):
        g = g.sort_values("start_sample")
        if (g["start_sample"].values[1:] < g["end_sample"].values[:-1]).any():
            ok = False
            lines.append(f"FAIL: noise '{t}' ranges overlap")
        else:
            lines.append(f"PASS: noise '{t}' train/val/test ranges do not overlap")
    for f in frames:
        c = f[f["split"].isin(["train", "val", "test"])].groupby("split")
        counts = {s: f"{len(g)} records / {g['group'].nunique()} patients" for s, g in c}
        lines.append(f"{f['dataset'].iloc[0]}: {counts}")
    return ok, lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    paths = load_paths()
    OUT.mkdir(parents=True, exist_ok=True)

    frames = []
    mit = split_mitdb(rng)
    have = {r.name for r in find_records(paths.get("mitdb", OUT / "none"))}
    mit["file_found"] = mit["record"].isin(have)
    frames.append(mit)
    if "qtdb" in paths:
        q = split_qtdb(find_records(paths["qtdb"]), mit, rng)
        if len(q):
            frames.append(q)
    if "ptbxl" in paths:
        p = split_ptbxl(paths["ptbxl"])
        if p is not None:
            frames.append(p)
    noise = split_noise(find_records(paths["nstdb"]))

    for f in frames:
        f.to_csv(OUT / f"{f['dataset'].iloc[0]}.csv", index=False)
    noise.to_csv(OUT / "nstdb_noise.csv", index=False)

    ok, lines = check(frames, noise)
    missing = int((~mit["file_found"]).sum())
    if missing:
        lines.append(f"WARNING: {missing} MIT-BIH records listed in the split were not found on disk")
    lines.insert(0, f"seed={args.seed}")
    (OUT / "split_check.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    append_log("E0-split-check", "Step 3 splits + leakage check",
               "Are train/val/test disjoint by patient and by noise segment?",
               ["research/splits/*.csv", "research/splits/split_check.txt"], lines,
               problems="" if ok else "LEAKAGE CHECK FAILED — do not continue",
               next_step="Step 4: build noisy test signals")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
