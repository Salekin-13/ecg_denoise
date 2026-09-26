"""Shared helpers for the research scripts (Steps 2-4 of Research_Plan.md)."""
import datetime
import json
import subprocess
from fractions import Fraction
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
RESEARCH = REPO / "research"
CONFIG = RESEARCH / "config" / "paths.json"
DATA_OUT = RESEARCH / "data_out"  # large local arrays, git-ignored

NOISE_TYPES = ["bw", "ma", "em"]
DEFAULT_SNRS = ["clean", 24, 12, 6, 0, -6]


def load_paths():
    """Read dataset folder locations. Relative paths are resolved from the repo root."""
    if not CONFIG.exists():
        raise SystemExit(f"Missing {CONFIG}. Copy paths.example.json to paths.json and edit it.")
    raw = json.loads(CONFIG.read_text())
    out = {}
    for key, value in raw.items():
        if key.startswith("_") or not value:
            continue
        p = Path(value)
        out[key] = p if p.is_absolute() else (REPO / p)
    return out


def find_records(root):
    """Return WFDB record paths (without extension) found anywhere under root."""
    root = Path(root)
    if not root.exists():
        return []
    return sorted(h.with_suffix("") for h in root.rglob("*.hea"))


def git_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=REPO, stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "no-git"


def append_log(entry_id, name, question, outputs, numbers, problems="", next_step=""):
    """Append an entry to research/logs/experiment_log.md in the plan's template format."""
    log = RESEARCH / "logs" / "experiment_log.md"
    log.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    lines = [
        f"\n### {entry_id} — {name}        Date: {today}",
        f"- Question this run answers: {question}",
        f"- Settings file: research/config/paths.json          Code version (git commit): {git_commit()}",
        f"- Result file(s): {', '.join(outputs)}",
        "- What happened (numbers):",
        *[f"  - {n}" for n in numbers],
        f"- Surprises / problems: {problems or 'none noted by script — review manually'}",
        f"- What I'll do next: {next_step}",
        "",
    ]
    with log.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))


def resample(x, fs_in, fs_out):
    """Polyphase resampling between integer-ish sampling rates."""
    if fs_in == fs_out:
        return np.asarray(x, dtype=np.float64)
    from scipy.signal import resample_poly

    frac = Fraction(int(round(fs_out)), int(round(fs_in))).limit_denominator(1000)
    return resample_poly(x, frac.numerator, frac.denominator)


def power(x):
    x = np.asarray(x, dtype=np.float64)
    return float(np.mean((x - x.mean()) ** 2))


def noise_scale(clean, noise, snr_db):
    """Factor k so that 10*log10(P(clean) / P(k*noise)) == snr_db (mean-removed power)."""
    pn = power(noise)
    if pn == 0:
        return 0.0
    return float(np.sqrt(power(clean) / (pn * 10 ** (snr_db / 10))))


def snr_db(clean, added):
    return 10 * np.log10(power(clean) / power(added))


def build_noise(bank, noise_type, starts, length):
    """Cut a noise segment from the bank. 'mix' = unit-power bw+ma+em summed, /sqrt(3)."""
    if noise_type == "mix":
        parts = []
        for t in NOISE_TYPES:
            seg = bank[t][starts[t]: starts[t] + length]
            seg = seg - seg.mean()
            parts.append(seg / np.sqrt(max(power(seg), 1e-12)))
        return np.sum(parts, axis=0) / np.sqrt(3)
    seg = bank[noise_type][starts[noise_type]: starts[noise_type] + length]
    return seg - seg.mean()


def make_noisy(clean, bank, row):
    """Rebuild one noisy window exactly from a recipe row (dict-like)."""
    if row["snr_db"] == "clean":
        return np.asarray(clean, dtype=np.float64).copy()
    starts = {t: int(row[f"start_{t}"]) for t in NOISE_TYPES if row.get(f"start_{t}", -1) not in (-1, "", None)}
    n = build_noise(bank, row["noise_type"], starts, len(clean))
    return np.asarray(clean, dtype=np.float64) + float(row["scale"]) * n
