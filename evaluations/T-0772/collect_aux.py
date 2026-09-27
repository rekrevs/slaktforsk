"""Granskarnas och rootsessionens förbrukning, redovisas separat från försöken."""
import json, pathlib, sys

b = pathlib.Path(__file__).resolve().parent
astra = json.loads((b.parent / 'T-0769' / 'prices.json').read_text())['rates']['gpt-6-astra']
opus = json.loads((b / 'prices.json').read_text())['claude-opus-5-5']
rows = []
for t in 'xyz':
    u = [json.loads(l)['usage'] for l in (b / 'judge' / t / 'events.jsonl').read_text().splitlines()
         if json.loads(l).get('type') == 'turn.completed'][-1]
    ip, cp, op = astra
    cost = ((u['input_tokens'] - u['cached_input_tokens']) * ip + u['cached_input_tokens'] * cp + u['output_tokens'] * op) / 1e6
    e = json.loads((b / 'judge' / t / 'end.json').read_text())
    rows.append({'agent': f'judge_{t}', 'model': 'gpt-6-astra', 'effort': 'medium', 'start': e['start'], 'end': e['end'],
                 'usage': u, 'standard_api_proxy_usd': cost})
# Rootsessionens transkript (Claude Code) ges som argument; varje API-svar räknas en gång per message-id.
if len(sys.argv) > 1:
    seen, tot = set(), {'input_tokens': 0, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0, 'output_tokens': 0}
    for line in pathlib.Path(sys.argv[1]).read_text().splitlines():
        d = json.loads(line); m = d.get('message') or {}
        if d.get('type') == 'assistant' and m.get('usage') and m.get('id') not in seen and m.get('model') == 'claude-opus-5-5':
            seen.add(m['id'])
            for k in tot:
                tot[k] += m['usage'].get(k, 0)
    cost = (tot['input_tokens'] * opus['input'] + tot['output_tokens'] * opus['output'] + tot['cache_read_input_tokens'] * opus['cache_read']
            + tot['cache_creation_input_tokens'] * opus['cache_write_1h']) / 1e6
    rows.append({'agent': 'root_session_until_measurement', 'model': 'claude-opus-5-5', 'effort': 'xhigh', 'responses': len(seen),
                 'usage': tot, 'standard_api_proxy_usd': cost,
                 'note': 'Planering, pilot, orkestrering, kontroll och rapportarbete fram till uttaget; cacheskrivning räknad som 1h.'})
(b / 'auxiliary-measurements.json').write_text(json.dumps(rows, indent=2) + '\n')
for r in rows:
    print(r['agent'], round(r['standard_api_proxy_usd'], 2))
