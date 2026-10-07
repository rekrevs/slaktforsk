import json,pathlib,sqlite3,hashlib,time
b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0561-final-expanded-queue-v1';start=time.time()
def h(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':h(p)}
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
prior=json.load(open(b/'implementation/C0561-second-settled-queue-v1/combined-current-C0561-partial-sequence-proposal-v1.json'));r=json.load(open(w/'settled-module-receipt-v1.json'));new=[p for p in r['candidate_modules'] if 'operation-' in p['path']];seq=prior['sequence'][:-1]+new+prior['sequence'][-1:];pre=json.load(open(b/'implementation/C0685-C0563-split-proposal-v2/concrete-sequence-and-preservation-receipt-v2.json'))['sequence'];versions={x['object_id']:x['version'] for x in c.execute('select r.object_id,max(r.version) version from revision r group by r.object_id')};viol=[];seen=set();fan=[]
for s in pre+seq:
 assert h(s['path'])==s['sha256'];o=json.load(open(s['path']));
 for ch in o['changes']:
  assert ch['id'] not in seen;seen.add(ch['id']);assert versions.get(ch['id'])==ch['expectedVersion']
  for e in ch['evidence']:
   assert set(e)=={'object','version','role','note'}
   if versions.get(e['object'])!=e['version']:viol.append({'target':ch['id'],'basis':e,'actual':versions.get(e['object'])})
 for ch in o['changes']:versions[ch['id']]=(ch['expectedVersion'] or 0)+1
for s in new:
 o=json.load(open(s['path']));s['operation_id']=o['id'];s['targets']=[{'id':z['id'],'expectedVersion':z['expectedVersion'],'payload_sha256':hashlib.sha256(json.dumps(z,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()} for z in o['changes']]
 for ch in o['changes']:
  rows=[dict(z) for z in c.execute('select d.*,r.version,r.object_id,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',(ch['id'],))];fan.append({'target':ch['id'],'all_historical_and_current_incoming':rows,'primary_disposition':None})
p=save('all-history-fanout-and-concrete-sequence-proposal-v1.json',{'scope':'C0561 partial only; source hash approval required','sequence':seq,'unique_C0561_targets':85,'new_revisions_this_phase':11,'prior_candidates_preserved':True,'static_violations':viol,'all_history_fanouts':fan,'incoming_count':sum(len(z['all_historical_and_current_incoming']) for z in fan),'additional_C0563_TR_support_preserved': ['BIO-P-0431','BIO-P-0438'],'no_apply':True});assert not viol
save('bounded-phase-handoff-v1.json',{'receipt':r,'proposal':p,'overlap_return':{'path':str(b/'implementation/C0561-final-expanded-overlap-return-v1.json'),'sha256':h(b/'implementation/C0561-final-expanded-overlap-return-v1.json')},'failed_attempts':0,'elapsed_finalization_seconds':time.time()-start,'total_elapsed_unknown_before_context_compaction':True,'source_sequence_binding_pending':True});print(p)
