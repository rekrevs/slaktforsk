"""Tillägg efter ägarens bedömning 2026-09-27 av B r9:s födelsedag.

Ägaren: cellen läses troligen 5/3 men är så svårläst att svaret borde ha en
särskild kommentar om att den är tvetydig. Låsta betyg ändras inte; detta
räknar om endast cellen B.r9.birth för alla X-svar i T-0769 och T-0772.

- mild: 31/3 och 5/3 ger båda innehållspoäng; saknad tvetydighetsmarkering
  (uncertain med alternativ) kostar statuspoängen men är inget kritiskt fel.
- strikt: säker läsning utan tvetydighetsmarkering är kritiskt, samma
  allvarsgrad som den frysta rubriken gav säker 5/3.
Övriga celler, poäng och kritiska fel (t.ex. radfel) behålls oförändrade.
"""
import collections, json, pathlib, re

e = pathlib.Path(__file__).resolve().parent.parent


def rescore(final, answer, strict):
    f = {x['id']: x for x in answer['fields']}['B.r9.birth']
    flagged = f['state'] == 'uncertain' and bool(f['alternatives'])
    content = 2 if re.sub(r'[^0-9/]', '', f['raw']) in ('190131/3', '19015/3') else 0
    old = {c['id']: c for c in final['field_scores']}['B.r9.birth']
    score = final['score'] - old['content'] - old['state'] + content + int(flagged)
    crit = [c for c in final['critical_errors'] if not c.startswith('B.r9.birth')]
    if strict and not flagged:
        crit.append('B.r9.birth: säker läsning utan tvetydighetsmarkering')
    return {'passed': score >= 68 and not crit, 'score': score, 'critical_errors': crit}


rows = []
for study, bmap in [('T-0769', 'T-0769/blind-map.private.json'), ('T-0772', 'T-0772/blind-map.private.json')]:
    for bid, run in json.loads((e / bmap).read_text()).items():
        if run.startswith('T-0769:') or run[0] != 'x':
            continue
        final = json.loads((e / study / 'scores' / f'{bid}.final.json').read_text())
        answer = json.loads((e / study / 'blind' / 'x' / f'{bid}.json').read_text())
        cell = {x['id']: x for x in answer['fields']}['B.r9.birth']
        rows.append({'study': study, 'run': run, 'model': run.split('_')[1], 'blind_id': bid,
                     'raw': cell['raw'], 'state': cell['state'], 'alternatives': cell['alternatives'],
                     'frozen': {'passed': final['passed'], 'score': final['score']},
                     'mild': rescore(final, answer, False), 'strict': rescore(final, answer, True)})
summary = collections.defaultdict(lambda: {'n': 0, 'frozen': 0, 'mild': 0, 'strict': 0, 'flagged': 0})
for r in rows:
    s = summary[r['model']]; s['n'] += 1; s['flagged'] += r['state'] == 'uncertain' and bool(r['alternatives'])
    for k in ('frozen', 'mild', 'strict'):
        s[k] += r[k]['passed']
(e / 'T-0772' / 'owner-ambiguity-rescore.json').write_text(
    json.dumps({'summary': summary, 'runs': rows}, ensure_ascii=False, indent=2) + '\n')
for m, s in summary.items():
    print(m, dict(s))
