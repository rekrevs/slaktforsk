"""Sammanställ låsta betyg, mätningar och kalibrering; körs först efter grade-lock."""
import csv, hashlib, json, math, pathlib, statistics

b = pathlib.Path(__file__).resolve().parent
old = b.parent / 'T-0769'
lock = json.loads((b / 'grade-lock.json').read_text())
for name, h in lock['files'].items():
    assert hashlib.sha256((b.parent.parent / name).read_bytes()).hexdigest() == h, 'Grade changed after lock: ' + name
mapping = json.loads((b / 'blind-map.private.json').read_text())
reverse = {v: k for k, v in mapping.items()}
measure = json.loads((b / 'measurements.json').read_text())
review = {r['id']: r for r in json.loads((b / 'protocol-review.json').read_text())}
final = lambda cid: json.loads((b / 'scores' / f'{cid}.final.json').read_text())


def wilson(k, n, z=1.96):
    if not n:
        return None
    p = k / n; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [round(c - h, 3), round(c + h, 3)]


rows = []
for r in measure:
    cid = reverse[r['id']]; s = final(cid)
    rows.append({**{k: v for k, v in r.items() if k not in ('final_text',)}, 'blind_id': cid,
                 'passed': s['passed'], 'score': s['score'], 'maxScore': s['maxScore'],
                 'critical_errors': s.get('critical_errors', []),
                 'material_pass': s.get('material_pass', s['passed']),
                 'sensitivity_pass_without_F5': s.get('sensitivity_pass_without_F5'),
                 'formatting_only_failure': s.get('formatting_only_failure', False),
                 'strict_packet_compliance': review[r['id']]['strict_packet_compliance']})
(b / 'results.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')

summary = []
for task in 'xyz':
    for arm in ['opus55-medium', 'opus55-xhigh']:
        rs = [r for r in rows if r['task'] == task and r['arm'] == arm]
        n, k = len(rs), sum(r['passed'] for r in rs)
        clean = [r for r in rs if r['strict_packet_compliance']]
        out = {'task': task, 'arm': arm, 'started': n, 'passed': k, 'wilson95': wilson(k, n),
               'material_passed': sum(bool(r['material_pass']) for r in rs),
               'without_F5_passed': sum(bool(r['sensitivity_pass_without_F5']) for r in rs) if task == 'y' else None,
               'mean_score_fraction': statistics.mean(r['score'] / r['maxScore'] for r in rs),
               'critical_failed_runs': sum(bool(r['critical_errors']) for r in rs),
               'median_seconds': statistics.median(r['seconds'] for r in rs),
               'median_tool_calls': statistics.median(r['tool_calls'] for r in rs),
               'mean_output_tokens': statistics.mean(r['usage']['output_tokens'] for r in rs),
               'mean_standard_proxy_usd': statistics.mean(r['api_standard_proxy_usd'] for r in rs),
               'mean_no_cache_proxy_usd': statistics.mean(r['api_no_cache_proxy_usd'] for r in rs),
               'proxy_per_accepted_usd': sum(r['api_standard_proxy_usd'] for r in rs) / k if k else None,
               'clean_n': len(clean), 'clean_passed': sum(r['passed'] for r in clean)}
        summary.append(out)

old_map = json.loads((old / 'blind-map.private.json').read_text())
calibration = []
for cid, ref in mapping.items():
    if not ref.startswith('T-0769:'):
        continue
    bid = ref.split(':')[1]
    was = json.loads((old / 'scores' / f'{bid}.final.json').read_text()); now = final(cid)
    calibration.append({'blind_id': cid, 'T-0769_blind_id': bid, 'T-0769_run': old_map[bid], 'task': was['task'],
                        'old_passed': was['passed'], 'new_passed': now['passed'],
                        'old_score': was['score'], 'new_score': now['score'], 'maxScore': was['maxScore'],
                        'old_material': was.get('material_pass', was['passed']),
                        'new_material': now.get('material_pass', now['passed']),
                        'old_without_F5': was.get('sensitivity_pass_without_F5'),
                        'new_without_F5': now.get('sensitivity_pass_without_F5'),
                        'verdict_agrees': was['passed'] == now['passed']})
(b / 'summary.json').write_text(json.dumps({'summary': summary, 'calibration': calibration},
                                           ensure_ascii=False, indent=2) + '\n')
with (b / 'results.csv').open('w') as f:
    keys = ['id', 'task', 'arm', 'replicate', 'seconds', 'tool_calls', 'passed', 'material_pass', 'score', 'maxScore',
            'api_standard_proxy_usd', 'api_no_cache_proxy_usd', 'strict_packet_compliance']
    w = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore'); w.writeheader(); w.writerows(rows)
print('Summarized', len(rows), 'runs; calibration agreement',
      sum(c['verdict_agrees'] for c in calibration), '/', len(calibration))
