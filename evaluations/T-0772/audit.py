"""Triage av försökens verktygsanrop mot paketavgränsningen; Bash granskas även manuellt."""
import hashlib, json, pathlib, re

b = pathlib.Path(__file__).resolve().parent
root = b.parent.parent
frozen = json.loads((b / 'frozen-manifest.json').read_text())['files']
issues = [n for n, h in frozen.items()
          if (root / n).exists() and hashlib.sha256((root / n).read_bytes()).hexdigest() != h]
missing = [n for n in frozen if not (root / n).exists()]
TERMS = ['rubric', 'reference.json', 'blind', '/private', 'judge', 'genealogy', 'wotan', 'AGENTS.md', 'CLAUDE.md',
         'README', 'NORTH-STAR', 'agent-principles', '.claude/', '.codex', '/tmp/', '/T-0769/', 'T-0769/', 'logs/', 'git ',
         'curl', 'http']
rows = []
for r in json.loads((b / 'measurements.json').read_text()):
    rd = str((b / 'runs' / r['id']).resolve())
    calls = json.loads((b / 'runs-telemetry' / f"{r['id']}.json").read_text())['calls']
    findings = []
    for c in calls:
        inp = c.get('input') or {}
        paths = [v for k, v in inp.items() if k in ('file_path', 'path') and isinstance(v, str)]
        outside = [p for p in paths if p.startswith('/') and not p.startswith(rd)]
        text = json.dumps(inp, ensure_ascii=False)
        own_free = text.replace(rd, '<RUN_DIR>')
        hits = [t for t in TERMS if t in own_free]
        if c['name'] == 'Bash':
            abs_paths = [p for p in re.findall(r'(/(?:Users|private|tmp|var|etc)[^\s\'"]*)', inp.get('command', ''))
                         if not p.startswith(rd)]
            outside += abs_paths
        if outside or hits:
            findings.append({'tool': c['name'], 'outside_paths': outside, 'terms': hits, 'input': inp})
    rows.append({'id': r['id'], 'tool_calls': len(calls), 'findings': findings,
                 'bash_commands': [c['input'].get('command') for c in calls if c['name'] == 'Bash']})
(b / 'audit.json').write_text(json.dumps({'frozen_changed': issues, 'frozen_missing': missing, 'runs': rows},
                                         ensure_ascii=False, indent=2) + '\n')
print('frozen changed', len(issues), 'missing', len(missing), 'runs', len(rows),
      'flagged', [r['id'] for r in rows if r['findings']])
