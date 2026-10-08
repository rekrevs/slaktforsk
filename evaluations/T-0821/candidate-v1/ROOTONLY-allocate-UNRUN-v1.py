import pathlib,json,hashlib,sys
R=pathlib.Path.cwd();C=R/'evaluations/T-0821/candidate-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();m=C/'literal-manifest-v1.json';x=json.load(open(m))
for f in x['files']:assert sha(R/f['path'])==f['sha256']
assert (R/'wotan/backlog.json').read_bytes()==(C/'before-backlog.json').read_bytes();assert not (R/'wotan/dev-log/T-0822.md').exists();proof=json.load(open(C/'preservation-proof-v1.json'));assert sha(R/'genealogy2/data/research.sqlite')==proof['native_sha256'];b=json.load(open(C/'before-backlog.json'));q=json.load(open(C/'backlog.json'));assert [r for r in q['tasks']if r['id']!='T-0822']==b['tasks'];assert q['next_id']==823;assert q['tasks'][next(i for i,r in enumerate(q['tasks'])if r['id']=='T-0217')+1]['id']=='T-0822'
if '--apply'not in sys.argv:print('READONLY candidate guards PASS; no writes');raise SystemExit()
a=json.load(open(sys.argv[sys.argv.index('--authorization')+1]));assert a['rootApproved']is True and a['manifestSha256']==sha(m)
for g in a['SOURCEgates']:
 assert sha(R/g['path'])==g['sha256'];gate=json.load(open(R/g['path']));assert gate['ready_for_root_allocation']is True
assert len(a['SOURCEgates'])==2
(R/'wotan/dev-log/T-0822.md').write_bytes((C/'T-0822.md').read_bytes());(R/'wotan/backlog.json').write_bytes((C/'backlog.json').read_bytes());print('Root authorized exact allocation only complete; no task execution')
