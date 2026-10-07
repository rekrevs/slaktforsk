import json,sqlite3,re,datetime
from pathlib import Path
b=Path('evaluations/T-0780/preparation');s=b/'selected';c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row;current={r['object_id']:dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version)')};data={}
for k in set(r['kind'] for r in current.values()):
 for r in c.execute('select * from '+k):
  rr=dict(r);rid=rr['revision_id'];oid=rid.rsplit('@',1)[0]
  if oid in current and current[oid]['id']==rid:data[oid]=rr
package=json.load(open(s/'complete-current-impact-and-support-package-v1.json'));pk={r['object_id']:r for r in package['objects'] if r['current']};cards=[]
for p in s.glob('C-*-impact-v1.json'):
 cid=p.name[:6];card=json.load(open(b/(cid+'-routing-v2.json')));impact=json.load(open(p));ids={r['object_id'] for r in impact['review']['items'] if r.get('current')};persons=set(card['metadata_person_routing']);records={r['object_id'] for r in card['current_records']}
 for cl in card['actual_j281_accepted_graph_claims']:persons.update(v for k,v in cl['data'].items() if k in ['person_id','from_person','to_person'])
 ids.update(o for o,d in data.items() if d.get('subject_id') in persons and current[o]['kind'] in ['assessment','question','narrative','fact']);ids.update(persons);terms=set()
 for o,d in data.items():
  if d.get('record_id') in records:
   if d.get('name_literal') and len(d['name_literal'])>=4:terms.add(d['name_literal'])
   terms.update(re.findall(r'\b\d{4}-\d{2}-\d{2}\b',json.dumps(d,ensure_ascii=False)))
 for pid in persons:
  if pid in data and len(data[pid].get('display_name',''))>=4:terms.add(data[pid]['display_name'])
 candidates=[]
 for oid,d in data.items():
  r=current[oid];fields={**d,'caveat':r['caveat'],'rationale':r['rationale'],'disposition':r['disposition'],'evidence_status':r['evidence_status']}
  hits=[]
  for field,value in fields.items():
   if not isinstance(value,str):continue
   found=[t for t in terms if t in value]
   if found:hits.append({'field':field,'terms':sorted(found),'old_wording':value})
  if hits:
   ids.add(oid);candidates.append({'object_id':oid,'revision_id':r['id'],'kind':r['kind'],'matches':hits,'evidence':[dict(x) for x in c.execute('select * from dependency where revision_id=?',(r['id'],))],'Astra_disposition':None,'Astra_rationale':None})
 out=[]
 for oid in sorted(ids):
  if oid not in current:continue
  r=current[oid];out.append({'object_id':oid,'revision_id':r['id'],'kind':r['kind'],'disposition':r['disposition'],'evidence_status':r['evidence_status'],'rationale':r['rationale'],'caveat':r['caveat'],'data':data[oid],'evidence':[dict(x) for x in c.execute('select * from dependency where revision_id=?',(r['id'],))]})
 (s/(cid+'-deduplicated-current-context-v1.json')).write_text(json.dumps({'scope':cid,'metadata_person_routing':sorted(persons),'whole_fields_no_adjudication':True,'objects':out,'complete_original_origins_and_older_supports':str(s/'complete-current-impact-and-support-package-v1.json')},ensure_ascii=False,indent=2)+'\n')
 (s/(cid+'-semantic-consequence-input-v1.json')).write_text(json.dumps({'scope':cid,'terms':sorted(terms),'literal_search_all_current_fields':True,'limitations':'Mechanical exact literal search cannot certify all semantic copies. Astra must search independently and dispositions including retain remain unsettled.','candidates':candidates},ensure_ascii=False,indent=2)+'\n');cards.append({'citation':cid,'terms':len(terms),'candidate_objects':len(candidates),'unit_context_objects':len(out)})
(s/'semantic-input-index-v1.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'units':cards},ensure_ascii=False,indent=2)+'\n');print(cards)
