#!/usr/bin/env python3
"""Transform Multi-SWE-bench-flash records into mini-swe-agent JSONL format.

Emits:
  data/one_inst.jsonl        - single easy Go instance (smoke test)
  data/slice28.jsonl         - 4 instances per language x 7 languages, easiest tier,
                               spread across repos
  data/slice28_manifest.json - chosen ids + difficulty
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "multi_swe_bench_flash.jsonl"

LANGS = ["go", "java", "javascript", "typescript", "rust", "c", "c++"]
DIFF_ORDER = {"≤15mins": 0, "15mins - 1h": 1, "1h - 4h": 2, "≥4h": 3}
SMOKE_ID = "cli__cli-278"


def load():
    with open(DATA) as f:
        return [json.loads(line) for line in f]


def to_msas(rec):
    """mini-swe-agent format: instance_id, problem_statement, image_name."""
    repo = rec["repo"]
    issues_text = "\n\n".join(
        f"Issue #{i.get('number')}: {i.get('title', '')}\n\n{i.get('body', '')}"
        for i in (rec.get("resolved_issues") or [])
    )
    parts = [
        f"The repository is checked out at /home/{repo}. "
        f"Start by running `cd /home/{repo}` before doing anything else.",
        "",
        f"PR title: {rec.get('title', '')}",
        "",
        "PR body:",
        rec.get("body") or "(empty)",
    ]
    if issues_text.strip():
        parts += ["", "Resolved issues:", issues_text]
    return {
        "instance_id": rec["instance_id"],
        "problem_statement": "\n".join(parts),
        "image_name": f"mswebench/{rec['org']}_m_{repo}:pr-{rec['number']}".lower(),
    }


def diff_rank(rec):
    return DIFF_ORDER.get(rec.get("difficulty"), len(DIFF_ORDER))


def pick_slice(recs, n=4):
    """Per language: sort by (difficulty, patch size), prefer distinct repos."""
    by_lang = {}
    for r in recs:
        by_lang.setdefault(r["language"], []).append(r)
    chosen = []
    for lang in LANGS:
        cands = sorted(by_lang.get(lang, []), key=lambda r: (diff_rank(r), len(r.get("fix_patch") or "")))
        picked, seen_repos = [], set()
        for r in cands:  # first pass: distinct repos
            if r["repo"] not in seen_repos:
                picked.append(r)
                seen_repos.add(r["repo"])
            if len(picked) == n:
                break
        for r in cands:  # fill up if fewer repos than n
            if len(picked) == n:
                break
            if r not in picked:
                picked.append(r)
        chosen.extend(picked[:n])
    return chosen


def main():
    recs = load()
    by_id = {r["instance_id"]: r for r in recs}

    # smoke instance: cli__cli-278 if present, else easiest go instance
    if SMOKE_ID in by_id:
        smoke = by_id[SMOKE_ID]
    else:
        gos = sorted(
            (r for r in recs if r["language"] == "go"),
            key=lambda r: (diff_rank(r), len(r.get("fix_patch") or "")),
        )
        smoke = gos[0]
    one_line = json.dumps(to_msas(smoke)) + "\n"
    with open(ROOT / "data" / "one_inst.jsonl", "w") as f:
        f.write(one_line)
    # datasets 4.x can't load a bare .jsonl path; it needs a directory with
    # split-named files (train.jsonl) for load_dataset(dir, split="train").
    (ROOT / "data" / "one_inst_ds").mkdir(exist_ok=True)
    (ROOT / "data" / "one_inst_ds" / "train.jsonl").write_text(one_line)
    print(f"smoke: {smoke['instance_id']} difficulty={smoke.get('difficulty')}")

    slice28 = pick_slice(recs)
    lines = [json.dumps(to_msas(r)) + "\n" for r in slice28]
    with open(ROOT / "data" / "slice28.jsonl", "w") as f:
        f.writelines(lines)
    (ROOT / "data" / "slice28_ds").mkdir(exist_ok=True)
    (ROOT / "data" / "slice28_ds" / "train.jsonl").write_text("".join(lines))
    manifest = [
        {"instance_id": r["instance_id"], "language": r["language"],
         "difficulty": r.get("difficulty"), "repo": f"{r['org']}/{r['repo']}"}
        for r in slice28
    ]
    with open(ROOT / "data" / "slice28_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    for m in manifest:
        print(f"  {m['language']:11s} {m['instance_id']:45s} {m['difficulty']}")


if __name__ == "__main__":
    main()
