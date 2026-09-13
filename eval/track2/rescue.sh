#!/bin/bash
set -e
cd ~/flybywire-track2
# MISTRAL_API_KEY must be set in the environment before running (never hardcode keys in files)

echo '=== build rescue dataset (3 instances) ==='
mkdir -p data/rescue_ds
python3 - <<'PYEOF'
import json
want = {'catchorg__Catch2-2288','BurntSushi__ripgrep-954','iamkun__dayjs-1953'}
out = []
for l in open('data/multi_swe_bench_flash.jsonl'):
    r = json.loads(l)
    if r['instance_id'] in want:
        repo = r['repo']
        out.append({
            'instance_id': r['instance_id'],
            'problem_statement': 'The repository is checked out at /home/%s. Start by running cd /home/%s before doing anything else.\n\nPR title: %s\n\nPR body:\n%s\n\nResolved issues:\n%s' % (repo, repo, r['title'], r['body'], r['resolved_issues']),
            'image_name': ('mswebench/%s_m_%s:pr-%s' % (r['org'], repo, r['number'])).lower(),
        })
with open('data/rescue_ds/train.jsonl','w') as f:
    for o in out: f.write(json.dumps(o)+'\n')
print('wrote', len(out), 'instances')
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

echo '=== fresh eval workdirs ==='
mkdir -p runs_evalA2 runs_evalB2
python3 - <<'PYEOF'
import json
for arm, wd in [('A','runs_evalA2'),('B','runs_evalB2')]:
    cfg = json.load(open('configs/eval_slice_%s.json' % arm))
    cfg['workdir'] = '~/flybywire-track2/' + wd
    cfg['output_dir'] = '~/flybywire-track2/runs/eval_final_' + arm
    cfg['log_dir'] = cfg['output_dir'] + '/logs'
    json.dump(cfg, open('configs/eval_final_%s.json' % arm,'w'), indent=2)
PYEOF

cd harness/multi-swe-bench
echo '=== EVAL ARM A (all 28) ==='
~/flybywire-track2/venv/bin/python -m multi_swe_bench.harness.run_evaluation --config ~/flybywire-track2/configs/eval_final_A.json 2>&1 | tail -3
echo '=== EVAL ARM B (all 28) ==='
~/flybywire-track2/venv/bin/python -m multi_swe_bench.harness.run_evaluation --config ~/flybywire-track2/configs/eval_final_B.json 2>&1 | tail -3
echo '=== RESCUE DONE ==='
