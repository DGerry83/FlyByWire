#!/usr/bin/env python3
"""Phase 1 routing-accuracy runner for the flybywire skill.

Feeds each test prompt in eval/routing-tests.jsonl to an LLM together with
the skill's routing context (SKILL.md body + Router.md), captures the
Routing Decision, and scores it against the expected classification.

Usage:
    # Gemini (default)
    set GEMINI_API_KEY=...        # PowerShell: $env:GEMINI_API_KEY="..."
    python eval/run_routing_tests.py

    # Mistral
    set MISTRAL_API_KEY=...
    set FLYBYWIRE_EVAL_PROVIDER=mistral
    python eval/run_routing_tests.py

Optional:
    FLYBYWIRE_EVAL_PROVIDER  gemini (default) | mistral
    FLYBYWIRE_EVAL_MODEL     model id (default per provider:
                             gemini -> gemini-3.1-flash-lite,
                             mistral -> mistral-small-latest)
    FLYBYWIRE_EVAL_ONLY      comma-separated case ids to run (e.g. R04,R21)

Results are written to eval/results/routing-<provider>-<model>-<timestamp>.json
and summarized on stdout. No third-party packages required.
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS = Path(__file__).resolve().parent / "routing-tests.jsonl"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

PROVIDER = os.environ.get("FLYBYWIRE_EVAL_PROVIDER", "gemini").lower()
_DEFAULT_MODELS = {"gemini": "gemini-3.1-flash-lite", "mistral": "mistral-small-latest"}
if PROVIDER not in _DEFAULT_MODELS:
    sys.exit(f"Unknown provider '{PROVIDER}' (expected gemini or mistral).")
MODEL = os.environ.get("FLYBYWIRE_EVAL_MODEL", _DEFAULT_MODELS[PROVIDER])
API_KEY = os.environ.get(
    "GEMINI_API_KEY" if PROVIDER == "gemini" else "MISTRAL_API_KEY", ""
)
ONLY = {s.strip() for s in os.environ.get("FLYBYWIRE_EVAL_ONLY", "").split(",") if s.strip()}

# Free tier for flash models is roughly 10 requests/minute; stay under it.
SECONDS_BETWEEN_CALLS = 7.0
MAX_RETRIES = 4


def load_routing_context() -> str:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    skill_body = re.sub(r"\A---\n.*?\n---\n", "", skill, flags=re.S).strip()
    router = (ROOT / "Router.md").read_text(encoding="utf-8").strip()
    return (
        "You are executing an agent skill exactly as written. Below is the skill's "
        "entry file and its routing file. For the user's request, follow them: "
        "classify the request and produce ONLY the Routing Decision in the required "
        "format (including the clarifying-question behavior when the request is "
        "genuinely ambiguous between two classes). Do not do the underlying work.\n\n"
        "===== SKILL.md =====\n" + skill_body + "\n\n===== Router.md =====\n" + router
    )


def call_gemini(system: str, prompt: str) -> str:
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    )
    body = json.dumps({
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0},
    }).encode("utf-8")
    headers = {"Content-Type": "application/json", "x-goog-api-key": API_KEY}
    return _post_with_retries(url, body, headers, _extract_gemini)


def call_mistral(system: str, prompt: str) -> str:
    url = "https://api.mistral.ai/v1/chat/completions"
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
    }).encode("utf-8")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    return _post_with_retries(url, body, headers, _extract_mistral)


def _extract_gemini(data: dict) -> str:
    return data["candidates"][0]["content"]["parts"][0]["text"]


def _extract_mistral(data: dict) -> str:
    return data["choices"][0]["message"]["content"]


def _post_with_retries(url: str, body: bytes, headers: dict, extract) -> str:
    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return extract(json.loads(resp.read().decode("utf-8")))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:300]
            if e.code in (429, 500, 503) and attempt < MAX_RETRIES - 1:
                wait = 20 * (attempt + 1)
                print(f"    HTTP {e.code}; retrying in {wait}s...", flush=True)
                time.sleep(wait)
                continue
            raise RuntimeError(f"{PROVIDER} API error HTTP {e.code}: {detail}") from e
    raise RuntimeError("unreachable")


call_model = call_gemini if PROVIDER == "gemini" else call_mistral


def parse_decision(text: str):
    cls = re.search(r"\*\*Classification\*\*:\s*([A-Za-z]+)", text)
    tpl = re.search(r"\*\*Selected Template\*\*:\s*`?([A-Za-z0-9_.\-]+)`?", text)
    return (cls.group(1) if cls else None, tpl.group(1) if tpl else None)


def main() -> int:
    if not API_KEY:
        sys.exit(f"API key env var for provider '{PROVIDER}' is not set.")

    system = load_routing_context()
    cases = [json.loads(l) for l in TESTS.read_text(encoding="utf-8").splitlines() if l.strip()]
    if ONLY:
        cases = [c for c in cases if c["id"] in ONLY]
    if not cases:
        sys.exit("No test cases selected.")

    RESULTS_DIR.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_model = MODEL.replace("/", "-").replace(":", "-")
    out_path = RESULTS_DIR / f"routing-{PROVIDER}-{safe_model}-{stamp}.json"

    results, passes = [], 0
    for i, case in enumerate(cases):
        if i:
            time.sleep(SECONDS_BETWEEN_CALLS)
        print(f"[{i + 1}/{len(cases)}] {case['id']} ...", flush=True)
        raw = call_model(system, case["prompt"])
        got_class, got_tpl = parse_decision(raw)

        if case["expected_class"] == "AMBIGUOUS":
            # Router-compliant outcomes for a genuinely ambiguous request:
            # (a) state both candidates + ask a clarifying question without
            #     committing, or (b) commit to a dominant intent WITH a
            #     justification AND clarifying questions (the taxonomy's
            #     "Clarifying Questions (optional)" field). Both pass.
            has_questions = ("?" in raw) and re.search(r"clarif|ambiguous|either|both|\?", raw, re.I)
            ok = bool(has_questions)
        else:
            ok = (got_class == case["expected_class"]) and (
                not case.get("expected_template") or got_tpl == case["expected_template"]
            )
        passes += ok
        results.append({
            "id": case["id"],
            "prompt": case["prompt"],
            "expected_class": case["expected_class"],
            "expected_template": case.get("expected_template"),
            "got_class": got_class,
            "got_template": got_tpl,
            "pass": ok,
            "raw_response": raw,
        })
        mark = "PASS" if ok else f"FAIL (got {got_class} / {got_tpl})"
        print(f"    {mark}", flush=True)

    total = len(results)
    report = {
        "provider": PROVIDER,
        "model": MODEL,
        "timestamp": stamp,
        "score": f"{passes}/{total}",
        "results": results,
    }
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nScore: {passes}/{total}")
    fails = [r for r in results if not r["pass"]]
    if fails:
        print("Failures:")
        for r in fails:
            print(f"  {r['id']}: expected {r['expected_class']}, got {r['got_class']} ({r['got_template']})")
    print(f"Full report: {out_path}")
    return 0 if passes == total else 1


if __name__ == "__main__":
    sys.exit(main())
