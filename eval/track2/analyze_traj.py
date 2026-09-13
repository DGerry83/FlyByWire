#!/usr/bin/env python3
"""Trajectory analysis helpers for Phase D flip analysis."""
import json
import re
import sys
from pathlib import Path

RUNS = Path("~/flybywire-track2/runs")


def load(run, iid):
    return json.load(open(RUNS / run / iid / f"{iid}.traj.json"))


def assistant_steps(t):
    """Yield (step_no, content, [commands])."""
    n = 0
    for m in t["messages"]:
        if m["role"] != "assistant":
            continue
        n += 1
        acts = [a["command"] for a in (m.get("extra") or {}).get("actions", [])]
        yield n, m.get("content") or "", acts


def cmd_show(run, iid, pattern=None, maxn=30, ctx=380):
    t = load(run, iid)
    print(f"### {run}/{iid} exit={t['info']['exit_status']} msgs={len(t['messages'])}")
    for n, content, acts in assistant_steps(t):
        if n > maxn:
            break
        if pattern and not re.search(pattern, " ".join(acts) + content):
            continue
        print(f"--- step {n}: {content[:ctx]!r}")
        for a in acts:
            print(f"    $ {a[:180]}")


def cmd_markers(run, iid):
    t = load(run, iid)
    pat = re.compile(r"Routing Decision|Classification:|Workflow Router|FlyByWire")
    for i, m in enumerate(t["messages"]):
        if m["role"] == "assistant" and pat.search(m.get("content") or ""):
            print(f"  {run}/{iid} msg#{i}: {(m['content'] or '')[:200]!r}")
            return True
    return False


def cmd_tail(run, iid, n_last=6, ctx=350):
    t = load(run, iid)
    steps = list(assistant_steps(t))
    print(f"### {run}/{iid} exit={t['info']['exit_status']} steps={len(steps)}")
    for n, content, acts in steps[-n_last:]:
        print(f"--- step {n}: {content[:ctx]!r}")
        for a in acts:
            print(f"    $ {a[:180]}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "show":
        cmd_show(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None,
                 int(sys.argv[5]) if len(sys.argv) > 5 else 30)
    elif cmd == "markers":
        cmd_markers(sys.argv[2], sys.argv[3])
    elif cmd == "tail":
        cmd_tail(sys.argv[2], sys.argv[3])
    elif cmd == "markers_all":
        for run in ["pilot_B", "slice_B"]:
            d = RUNS / run
            for sub in sorted(d.iterdir()):
                if sub.is_dir() and (sub / f"{sub.name}.traj.json").exists():
                    if not cmd_markers(run, sub.name):
                        print(f"  {run}/{sub.name}: no markers")
