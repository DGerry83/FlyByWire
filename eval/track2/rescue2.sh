#!/bin/bash
set -e
cd ~/flybywire-track2
# MISTRAL_API_KEY must be set in the environment before running (never hardcode keys in files)

echo '=== purge empty-patch preds ==='
python3 - <<'PYEOF'
import json
for arm, ids in [('A', ['catchorg__Catch2-2288','BurntSushi__ripgrep-954','iamkun__dayjs-1953']),
                 ('B', ['catchorg__Catch2-2288','BurntSushi__ripgrep-954'])]:
    p = 'runs/slice_%s/preds.json' % arm
    d = json.load(open(p))
    for i in ids:
        d.pop(i, None)
    json.dump(d, open(p, 'w'), indent=1)
    print(arm, 'preds now', len(d))
PYEOF

echo '=== ARM A rescue ==='
venv/bin/mini-extra swebench --subset data/rescue_ds --split train -c configs/stock_mistral.yaml -o runs/slice_A -w 2 2>&1 | tail -3
echo '=== ARM B rescue ==='
venv/bin/mini-extra swebench --subset data/rescue_ds --split train -c configs/stock_mistral.yaml -c configs/skill_mistral.yaml -o runs/slice_B -w 2 2>&1 | tail -3

echo '=== merge + patches ==='
python3 - <<'PYEOF'
import json
for arm in ['A','B']:
    merged = {}
    for src in ['runs/pilot_%s/preds.json' % arm, 'runs/slice_%s/preds.json' % arm]:
        merged.update(json.load(open(src)))
    json.dump(merged, open('runs/all_%s_preds.json' % arm,'w'), indent=1)
    print(arm, len(merged), 'instances')
PYEOF
venv/bin/python preds_to_patch.py runs/all_A_preds.json runs/all_A_patches.jsonl
venv/bin/python preds_to_patch.py runs/all_B_preds.json runs/all_B_patches.jsonl

echo '=== fresh eval workdirs (v3) ==='
mkdir -p runs_evalA3 runs_evalB3
python3 - <<'PYEOF'
import json
for arm, wd in [('A','runs_evalA3'),('B','runs_evalB3')]:
    cfg = json.load(open('configs/eval_slice_%s.json' % arm))
    cfg['workdir'] = '~/flybywire-track2/' + wd
    cfg['output_dir'] = '~/flybywire-track2/runs/eval_v3_' + arm
    cfg['log_dir'] = cfg['output_dir'] + '/logs'
    json.dump(cfg, open('configs/eval_v3_%s.json' % arm,'w'), indent=2)
PYEOF

cd harness/multi-swe-bench
echo '=== EVAL ARM A ==='
~/flybywire-track2/venv/bin/python -m multi_swe_bench.harness.run_evaluation --config ~/flybywire-track2/configs/eval_v3_A.json 2>&1 | tail -3
echo '=== EVAL ARM B ==='
~/flybywire-track2/venv/bin/python -m multi_swe_bench.harness.run_evaluation --config ~/flybywire-track2/configs/eval_v3_B.json 2>&1 | tail -3
echo '=== RESCUE2 DONE ==='
