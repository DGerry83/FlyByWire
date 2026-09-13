#!/bin/bash
set -x
cd ~/flybywire-track2
# MISTRAL_API_KEY must be set in the environment before running (never hardcode keys in files)

echo '=== ARM A remaining 20 ==='
venv/bin/mini-extra swebench --subset data/slice28_ds --split train --slice 8:28   -c configs/stock_mistral.yaml -o runs/slice_A -w 2 2>&1 | tail -5

echo '=== ARM B remaining 20 ==='
venv/bin/mini-extra swebench --subset data/slice28_ds --split train --slice 8:28   -c configs/stock_mistral.yaml -c configs/skill_mistral.yaml -o runs/slice_B -w 2 2>&1 | tail -5

echo '=== merge preds ==='
python3 - <<'EOF'
import json
for arm in ['A','B']:
    merged = {}
    for src in [f'runs/pilot_{arm}/preds.json', f'runs/slice_{arm}/preds.json']:
        merged.update(json.load(open(src)))
    json.dump(merged, open(f'runs/all_{arm}_preds.json','w'), indent=1)
    print(arm, len(merged), 'instances')
EOF

venv/bin/python preds_to_patch.py runs/all_A_preds.json runs/all_A_patches.jsonl
venv/bin/python preds_to_patch.py runs/all_B_preds.json runs/all_B_patches.jsonl

echo '=== eval configs ==='
mkdir -p runs_evalA runs_evalB
python3 - <<'EOF'
import json
for arm in ['A','B']:
    cfg = json.load(open(f'configs/eval_pilot_{arm}.json'))
    cfg['workdir'] = f'~/flybywire-track2/runs_eval{arm}'
    cfg['patch_files'] = [f'~/flybywire-track2/runs/all_{arm}_patches.jsonl']
    cfg['output_dir'] = f'~/flybywire-track2/runs/eval_slice_{arm}'
    cfg['log_dir'] = f'~/flybywire-track2/runs/eval_slice_{arm}/logs'
    json.dump(cfg, open(f'configs/eval_slice_{arm}.json','w'), indent=2)
EOF

cd harness/multi-swe-bench
echo '=== EVAL ARM A ==='
~/flybywire-track2/venv/bin/python -m multi_swe_bench.harness.run_evaluation --config ~/flybywire-track2/configs/eval_slice_A.json 2>&1 | tail -4
echo '=== EVAL ARM B ==='
~/flybywire-track2/venv/bin/python -m multi_swe_bench.harness.run_evaluation --config ~/flybywire-track2/configs/eval_slice_B.json 2>&1 | tail -4
echo '=== DONE ==='
docker system df
