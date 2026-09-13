#!/usr/bin/env python3
"""Convert mini-swe-agent preds.json to the multi-swe-bench harness patch JSONL.

mini-swe-agent preds.json: {instance_id: {"model_patch": str, ...}, ...}
harness patch JSONL: {"org":..., "repo":..., "number":..., "fix_patch":...} per line
instance_id format: {org}__{repo}-{number}

Usage: preds_to_patch.py <preds.json> <out.jsonl>
"""
import json
import sys
from pathlib import Path


def main(preds_path, out_path):
    preds = json.loads(Path(preds_path).read_text())
    n = 0
    with open(out_path, "w") as f:
        for iid, entry in preds.items():
            patch = entry.get("model_patch") or ""
            org_repo, number = iid.rsplit("-", 1)
            org, repo = org_repo.split("__", 1)
            f.write(json.dumps({
                "org": org,
                "repo": repo,
                "number": int(number),
                "fix_patch": patch,
            }) + "\n")
            n += 1
    print(f"wrote {n} patches to {out_path}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
