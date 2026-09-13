# Phase A — Multi-SWE-bench pipeline smoke (one instance: cli__cli-278)

Date: 2026-07-30. Host: Windows 11 + WSL2 Ubuntu (docker only inside WSL). All work in `~/flybywire-track2/` (WSL home).

## What worked

- **uv install in WSL**: `curl -LsSf https://astral.sh/uv/install.sh | sh` → `~/.local/bin/uv` (0.12.0). Clean.
- **venv + packages**: `uv venv ~/flybywire-track2/venv` (CPython 3.12.3); `uv pip install --python venv/bin/python mini-swe-agent datasets pyyaml` → mini-swe-agent 2.4.6, datasets 4.x. Clean.
- **harness**: `git clone --depth 1 https://github.com/multi-swe-bench/multi-swe-bench ~/flybywire-track2/harness/multi-swe-bench`; `uv pip install --python venv/bin/python -e harness/multi-swe-bench`. Clean.
- **flash dataset**: curl from HF, 300 lines / 84 MB, schema has `language` (not `lang`), `difficulty` (java instances have `difficulty: null`).
- **images**: `mswebench/cli_m_cli:pr-278` (1.63 GB), helper `mswebench/nix_swe:v1.0` (1.5 GB), `mswebench/cli_m_cli:base` (1.49 GB) + `golang:latest` all pulled without issues.
- **scoring**: `run_evaluation` produced `final_report.json` for arm A (1 submitted / 1 completed / 1 unresolved — expected, the arm-A patch was empty).

## Gotchas / workarounds (all applied)

1. **`-c` replaces the default config entirely** (mini-swe-agent v2: "If you set this option, the default config file will not be used"). So `configs/stock.yaml` is a full copy of the builtin `swebench.yaml` with edits, not a diff.
2. **`datasets` 4.x cannot `load_dataset()` a bare `.jsonl` path.** `make_dataset.py` additionally emits `data/one_inst_ds/train.jsonl` and `data/slice28_ds/train.jsonl`; pass the *directory* as `--subset` with `--split train`.
3. **litellm cost tracking crashes on unknown models** (`gemini-3.1-flash-lite` not in its price map): fixed with `model.cost_tracking: "ignore_errors"` in stock.yaml (env alternative: `MSWEA_COST_TRACKING=ignore_errors`).
4. **harness `specifics` filter matches harness ids (`org/repo:pr-N`), not SWE-bench ids** (`org__repo-N`). eval configs use `"specifics": ["cli/cli:pr-278"]`.
5. **harness patch JSONL uses key `fix_patch`** with `{org, repo, number, fix_patch}`; `preds_to_patch.py` does the conversion from mini-swe-agent `preds.json`.
6. **Gemini free tier = 500 requests/day/project/model** (`GenerateRequestsPerDayPerProjectPerModel-FreeTier`). Two smoke runs + litellm retries exhausted it mid-run for arm B (RateLimitError after 147 trajectory messages). This is the main Phase B blocker — see below.

## Deviations from plan

- `stock.yaml` instance_template: the one "/testbed" mention was reworded to "/home …" to match Multi-SWE-bench image layout (repos live at `/home/<repo>`); plan already set `environment.cwd: /home`.
- Two eval configs (`eval_smoke_A.json`, `eval_smoke_B.json`) instead of one, since `patch_files`/`output_dir` differ per arm. `max_workers_build_image`/`max_workers_run_instance` also set to 1.
- Arm B retried once with `--redo-existing -c model.model_kwargs.num_retries=10` after the 429 kill.

## Smoke results

- **Arm A (stock)**: exit `Submitted` in ~1:47 wall (agent loop ~2 min, 38 messages). BUT submission empty: the model created a valid `patch.txt` inside `/home/cli` and then submitted with `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt` from cwd `/home` (subshells don't persist cd), so `cat` failed and mini-swe-agent recorded an empty patch. Scored unresolved. Model discipline issue, not a pipeline issue; consider a template line reminding the submit command needs the cd prefix for flash-lite.
- **Arm B (skill)**: skill delivery verified — `grep -c "Workflow Router" runs/smoke_B/...traj.json` = 2 and the trajectory's system message contained the full skill bundle (checked at 18:56 UTC). First attempt died on the free-tier **daily** 429 (500 req/day) after 147 messages / ~13 min of progress; a retry with `num_retries=10` never got a single command into the container (confirmed via `docker exec … ps aux`) and was killed after 15 min of pure backoff. The retry wiped the v4 trajectory (mini-swe-agent unlinks per-instance files on start), so the on-disk traj is gone; `runs/smoke_B/preds.json` was restored manually with the honest v4 outcome (`model_patch: ""`). `configs/skill.yaml` round-trip verified to contain the bundle.
- Wall-clock per instance: ~2 min agent (arm A) + ~3 min image pull (first time) + ~4 min eval harness = **~6 min/instance steady state** (image cached).
- Disk after smoke: `docker system df` → 4.63 GB images, 957 MB volumes. WSL ext4: 953 GB free.

## Resume behavior

`mini-extra swebench` skips instance_ids already present in `<out>/preds.json` unless `--redo-existing`. Interrupt mid-run → completed instances are kept on re-run; the in-flight instance restarts from step 0 (no mid-instance checkpointing).

## Exact commands (from Git Bash)

Smoke arms:
```
wsl -d Ubuntu -- bash -lc "cd ~/flybywire-track2 && OPENAI_API_KEY='…' venv/bin/mini-extra swebench \
  --subset ~/flybywire-track2/data/one_inst_ds --split train \
  -c configs/stock.yaml -o runs/smoke_A -w 1"
wsl -d Ubuntu -- bash -lc "cd ~/flybywire-track2 && OPENAI_API_KEY='…' venv/bin/mini-extra swebench \
  --subset ~/flybywire-track2/data/one_inst_ds --split train \
  -c configs/stock.yaml -c configs/skill.yaml -o runs/smoke_B -w 1"
```

Scoring:
```
venv/bin/python preds_to_patch.py runs/smoke_A/preds.json runs/smoke_A/patches.jsonl
cd harness/multi-swe-bench && ~/flybywire-track2/venv/bin/python -m multi_swe_bench.harness.run_evaluation \
  --config ~/flybywire-track2/configs/eval_smoke_A.json
```

## Phase B pilot commands (8 instances — first 8 lines of slice28_ds)

Requires fresh Gemini quota (free tier resets daily) or a paid key. Background from Git Bash:

```
# Arm A (stock)
wsl -d Ubuntu -- bash -lc "cd ~/flybywire-track2 && OPENAI_API_KEY='…' venv/bin/mini-extra swebench \
  --subset ~/flybywire-track2/data/slice28_ds --split train --slice 0:8 \
  -c configs/stock.yaml -o runs/pilot_A -w 2 2>&1 | tail -30"

# Arm B (skill)
wsl -d Ubuntu -- bash -lc "cd ~/flybywire-track2 && OPENAI_API_KEY='…' venv/bin/mini-extra swebench \
  --subset ~/flybywire-track2/data/slice28_ds --split train --slice 0:8 \
  -c configs/stock.yaml -c configs/skill.yaml -o runs/pilot_B -w 2 2>&1 | tail -30"

# Convert + score (per arm, after agent run finishes)
wsl -d Ubuntu -- bash -lc "cd ~/flybywire-track2 && \
  venv/bin/python preds_to_patch.py runs/pilot_A/preds.json runs/pilot_A/patches.jsonl && \
  cd harness/multi-swe-bench && ~/flybywire-track2/venv/bin/python \
  -m multi_swe_bench.harness.run_evaluation --config ~/flybywire-track2/configs/eval_pilot_A.json 2>&1 | tail -15"
```

Note: an `eval_pilot_A.json`/`eval_pilot_B.json` must be created (copy of `eval_smoke_A.json`, drop `specifics`, point `patch_files`/`output_dir`/`log_dir` at the pilot dirs). Interrupted agent runs resume via preds.json skip (no `--redo-existing`).

## Phase B prep (2026-07-30, follow-up)

- **Model switch for the pilot: Mistral.** Gemini free tier is 500 requests/day (exhausted during Phase A smoke). Pilot uses `mistral/mistral-small-latest` (native litellm provider, key from `MISTRAL_API_KEY` env var; free tier ~1 req/sec, 1B tokens/month, no daily call cap). Gemini configs (`stock.yaml`/`skill.yaml`) untouched for later use.
- New configs: `configs/stock_mistral.yaml` (stock.yaml with model swapped; Gemini-specific `api_base` removed; `drop_params: true`, `temperature: 0.0`, `cost_tracking: "ignore_errors"`, step_limit 100, pull_timeout 900, cwd /home kept) and `configs/skill_mistral.yaml` (overlay identical to skill.yaml — it carries only `agent.system_template`, so the instance template below is inherited from whichever stock config is passed first; always pair `-c configs/stock_mistral.yaml -c configs/skill_mistral.yaml`).
- **Fresh-shell reminder added to the instance template** in `stock.yaml` and `stock_mistral.yaml` (identical wording; skill overlays inherit it): "REMINDER: Every command runs in a fresh shell starting from /home, so prefix EVERY command that needs the repository with `cd /home/<repo> &&` — this includes the final submit command, e.g. `cd /home/<repo> && echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt`." This fixes the Phase A arm-A empty-patch failure mode.
- **Mistral sanity check passed**: direct `litellm.completion(model="mistral/mistral-small-latest", "reply with OK")` from the venv returned `'OK'` (usage: 20 tokens) and `litellm.completion_cost` succeeded (1.44e-06 USD) — cost tracking will not crash on this model.
- New eval configs `configs/eval_pilot_A.json` / `eval_pilot_B.json`: clones of the smoke eval configs without `specifics` (scores every instance in the patch file), patch_files at `runs/pilot_{A,B}/patches.jsonl`, output/log dirs `runs/eval_pilot_{A,B}`.
