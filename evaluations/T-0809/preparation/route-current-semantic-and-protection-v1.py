import pathlib,json,hashlib,time,sqlite3,datetime
R=pathlib.Path.cwd();D=R/'evaluations/T-0809/preparation';start=time.monotonic();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();main=R/'genealogy2/data/research.sqlite';before=h(main);c=sqlite3.connect(f'file:{main}?mode=ro',uri=True);c.row_factory=sqlite3.Row
records=['R-1061d792a13da3adb41953c7','R-e4fb8c8d6bd1ceda4f046c8b','R-10becdc13438f7b60b2a4651','R-c18a188429c70523967e6b67','R-660c906eba5561b5cb998a5a','R-95b35d37c2e50f97f8ae7fac'];citations=['C1056','C1057','C1059','C1065','C1068','C1070','C-1056','C-1057','C-1059','C-1065','C-1068','C-1070'];keys=['P-0009',*records,*citations];heads=list(c.execute('select r.*,o.kind from current_revision cr join revision r on r.id=cr.id join object o on o.id=r.object_id'))
def native(rr):
 n=dict(rr);data=dict(c.execute('select * from '+rr['kind']+' where revision_id=?',(rr['id'],)).fetchone());n['data']=data;n['origins']=[dict(x) for x in c.execute('select * from origin where revision_id=? order by rowid',(rr['id'],))];n['evidence']=[dict(x) for x in c.execute('select * from dependency where revision_id=? order by rowid',(rr['id'],))];return n
routes=[];relations=[]
for rr in heads:
 n=native(rr);data=n['data'];raw=json.dumps(data,ensure_ascii=False);basis=[e['basis_revision_id'].split('@')[0] for e in n['evidence']];hits=[k for k in keys if k in raw or k in rr['object_id']];direct=[r for r in records if r in basis]
 if not hits and not direct:continue
 fields=[]
 for field,value in data.items():
  if value is None:continue
  val=json.dumps(value,ensure_ascii=False) if not isinstance(value,str) else value
  if any(k in val for k in keys) or field in ['body','caveat','outcome','status','scope_json','value_json','value_literal','reason','rationale']:
   fields.append({'field':field,'exact_current_value':value,'literal_keys':[k for k in keys if k in val]})
 routes.append({'object_id':rr['object_id'],'version':rr['version'],'literal_keys':hits,'direct_record_basis':direct,'fields':fields,'full_current_native':n})
 if rr['kind']=='relation' and ('P-0009' in raw):relations.append(n)
out=D/'current-semantic-routing-and-relation-ledger-v1.json';out.write_text(json.dumps({'routing_only':True,'no_disposition_or_certified_people_list':True,'exact_six_record_ids':records,'routes':routes,'all_direct_current_Ada_relations':relations,'parent_relations':[n['object_id'] for n in relations if n['data'].get('relation_type')=='parent'],'note':'All matching current fields and full metadata/raw serialized structured data/evidence/origins retained. Historical/current distinctions and necessary corrections belong to Astra.'},ensure_ascii=False,indent=2)+'\n')
paths=['evaluations/T-0808/actual-main-stage-comparison-v1.json','evaluations/T-0808/implementation/stage471-sequence-v1/actual-all50.json','evaluations/T-0808/implementation/stage471-sequence-v1/inventory-full.json','evaluations/T-0808/root-after-3-v1.json','evaluations/T-0808/root-after-4-v1.json','evaluations/T-0808/root-after-5-v1.json','wotan/dev-log/T-0237.md','evaluations/T-0809/T0237-exact-atom-partition-v1.json']
proof={'current_main_sha256':before,'reused_current471_exact_comparison':True,'qualification':'Stage471 all50 baseline comparison is qualified only for its two operation.recorded_at runtime timestamps, as exact root canonical comparison records; current axes/default readers reusable unchanged. No recomputation or normalization of native knowledge.','pins':[{'path':p,'sha256':h(R/p)} for p in paths],'routing_pin':{'path':str(out.relative_to(R)),'sha256':h(out)},'actual_relation_count':len(relations),'elapsed_seconds':time.monotonic()-start,'failures':[],'main_unchanged':h(main)==before}
assert proof['main_unchanged'];p=D/'bounded-mechanical-protection-preparation-v1.json';p.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(h(p));print('routes',len(routes),'relations',len(relations),'seconds',proof['elapsed_seconds'])
