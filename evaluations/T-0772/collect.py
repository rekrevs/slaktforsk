"""Härled telemetry per försök ur logs/<id>.stream.jsonl; ändrar inga svar."""
import datetime, hashlib, json, pathlib

b = pathlib.Path(__file__).resolve().parent
prices = json.loads((b / 'prices.json').read_text())['claude-opus-5-5']
ts = lambda s: datetime.datetime.fromisoformat(s)


def proxy(u):
    cc = u.get('cache_creation', {})
    w1h, w5m = cc.get('ephemeral_1h_input_tokens', 0), cc.get('ephemeral_5m_input_tokens', 0)
    rest = u.get('cache_creation_input_tokens', 0) - w1h - w5m
    return (u.get('input_tokens', 0) * prices['input'] + u.get('output_tokens', 0) * prices['output']
            + u.get('cache_read_input_tokens', 0) * prices['cache_read']
            + (w1h + rest) * prices['cache_write_1h'] + w5m * prices['cache_write_5m']) / 1e6


def no_cache(u):
    total_in = u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0)
    return (total_in * prices['input'] + u.get('output_tokens', 0) * prices['output']) / 1e6


rows = []
for t in json.loads((b / 'schedule.json').read_text()):
    start_f, end_f = b / 'logs' / f"{t['id']}.start.json", b / 'logs' / f"{t['id']}.end.json"
    if not start_f.exists():
        continue
    rec = json.loads((end_f if end_f.exists() else start_f).read_text())
    events, calls, seen, init, result = [], [], set(), None, None
    for line in (b / 'logs' / f"{t['id']}.stream.jsonl").read_text().splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get('type') == 'system' and d.get('subtype') == 'init':
            init = d
        elif d.get('type') == 'result':
            result = d
        elif d.get('type') == 'assistant':
            for c in d['message'].get('content', []):
                if c.get('type') == 'tool_use' and c['id'] not in seen:
                    seen.add(c['id']); calls.append({'name': c['name'], 'input': c.get('input')})
    answer = b / 'runs' / t['id'] / 'answer.json'
    u = (result or {}).get('usage', {})
    row = {**t, 'start': rec['start'], 'end': rec.get('end'),
           'seconds': (ts(rec['end']) - ts(rec['start'])).total_seconds() if rec.get('end') else None,
           'reported_duration_s': result['duration_ms'] / 1000 if result else None,
           'returncode': rec.get('returncode'), 'timed_out': rec.get('timed_out'),
           'argv_model': rec['argv'][rec['argv'].index('--model') + 1],
           'argv_effort': rec['argv'][rec['argv'].index('--effort') + 1],
           'init_model': init and init.get('model'),
           'models_used': sorted((result or {}).get('modelUsage', {})),
           'num_turns': result and result.get('num_turns'), 'final_text': result and result.get('result'),
           'is_error': result and result.get('is_error'),
           'usage': {k: u.get(k, 0) for k in ['input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens', 'output_tokens']},
           'cache_creation': u.get('cache_creation', {}),
           'claude_code_list_usd': result and result.get('total_cost_usd'),
           'api_standard_proxy_usd': proxy(u) if result else None,
           'api_no_cache_proxy_usd': no_cache(u) if result else None,
           'tool_calls': len(calls),
           'answer_exists': answer.exists(),
           'answer_sha256': hashlib.sha256(answer.read_bytes()).hexdigest() if answer.exists() else None}
    (b / 'runs-telemetry').mkdir(exist_ok=True)
    (b / 'runs-telemetry' / f"{t['id']}.json").write_text(
        json.dumps({**row, 'calls': calls}, ensure_ascii=False, indent=2) + '\n')
    rows.append(row)
(b / 'measurements.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
done = [r for r in rows if r['end']]
print('started', len(rows), 'finished', len(done), 'answers', sum(r['answer_exists'] for r in rows),
      'errors', sum(bool(r['is_error']) or r['returncode'] != 0 for r in done))
