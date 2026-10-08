"""Read-only validation by default. Root alone may supply exact reviewed authorization for --apply."""
import pathlib,json,hashlib,argparse,os
R=pathlib.Path.cwd();D=R/'evaluations/T-0819/candidate-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.load(open(p));a=argparse.ArgumentParser();a.add_argument('--apply',action='store_true');a.add_argument('--authorization');args=a.parse_args();m=load(D/'literal-manifest-v1.json')
for pin in m['pins']:assert sha(R/pin['path'])==pin['sha256'],pin['path']
base=load(D/'baseline-backlog.json');candidate=load(D/'backlog.json');assert (R/'wotan/backlog.json').read_bytes()==(D/'baseline-backlog.json').read_bytes();assert [t for t in candidate['tasks']if t['id']not in ['T-0820','T-0821']]==base['tasks'];assert candidate['next_id']==822
assert sha(R/'genealogy2/data/research.sqlite')==m['main_sha256'];assert sha(R/'wotan/node-links.json')==m['node_links_sha256'];assert (R/'wotan/dev-log/T-0255.md').read_bytes()==(D/'T-0255-preimage.md').read_bytes()
for tid in ['T-0820','T-0821']:assert not(R/f'wotan/dev-log/{tid}.md').exists()
if not args.apply:
 print('READONLY PASS; no allocation performed');raise SystemExit(0)
assert args.authorization,'Root-reviewed exact authorization required';auth=load(pathlib.Path(args.authorization));assert auth['root_authorized_queue_allocation']is True;assert auth['manifest_sha256']==sha(D/'literal-manifest-v1.json');assert len(auth['final_source_gates'])==2
for pin in auth['final_source_gates']:assert sha(R/pin['path'])==pin['sha256'];load(R/pin['path'])
# Only these reviewed bytes are allocated. No task completion, checkpoint, PC or database writes.
for tid in ['T-0820','T-0821']:(R/f'wotan/dev-log/{tid}.md').write_bytes((D/f'{tid}.md').read_bytes())
(R/'wotan/dev-log/T-0255.md').write_bytes((D/'T-0255.md').read_bytes())
tmp=R/'wotan/.T0819-reviewed-backlog.tmp';assert not tmp.exists();tmp.write_bytes((D/'backlog.json').read_bytes());os.replace(tmp,R/'wotan/backlog.json');assert sha(R/'genealogy2/data/research.sqlite')==m['main_sha256'];print('ROOT exact queue allocation complete; T0819 completion and factual checkpoints remain separate root actions')
