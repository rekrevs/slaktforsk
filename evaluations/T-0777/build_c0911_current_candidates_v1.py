import pathlib,json,sqlite3,hashlib,copy
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1]
connection=sqlite3.connect('file:'+str(B/'clone/research-pre.sqlite')+'?mode=ro',uri=True);connection.row_factory=sqlite3.Row
exec((B/'native_payload.py').read_text())
base=json.loads((B/'source-review/C-0911-current-decisions-v1.json').read_text());amend=json.loads((B/'source-review/C-0911-current-amendment-v2.json').read_text());roles=json.loads((B/'source-review/C-0911-role-metadata-amendment-v3.json').read_text());name=json.loads((B/'source-review/C-0911-older-name-support-decision-v4.json').read_text())
decisions={}
for d in base['decisions']:
 decisions[d['object']]=copy.deepcopy(d)
for d in amend['decisions']+[name]:
 oid=d['object']
 if oid not in decisions:decisions[oid]=copy.deepcopy(d)
 else:
  fields={f['field'].removeprefix('data.'):f for f in decisions[oid]['fields']}
  for f in d['fields']:fields[f['field'].removeprefix('data.')]=f
  decisions[oid]['fields']=list(fields.values())
  decisions[oid].update({k:v for k,v in d.items() if k!='fields'})
for d in roles['decisions']:
 oid=d['object']
 if oid not in decisions:decisions[oid]=copy.deepcopy(d)
 else:decisions[oid]['fields']+=d['fields'];decisions[oid]['role_reason']=d['reason']
mids={d['object'] for d in roles['decisions']};meta=[];current=[];table=[]
for oid,d in decisions.items():
 if oid=='R-5fcb723c98597da6131ddbea':continue # already separate metadata stage
 obj=existing(oid,d['version']);cur=json.loads((B/'current'/('inspect-'+oid.replace('/','__')+'.json')).read_text())['current'];old_evidence=copy.deepcopy(obj['evidence'])
 for f in d['fields']:
  k=f['field'].removeprefix('data.');assert cur[k]==f['old_full_field'],(oid,k,'old exactfield mismatch');assert 'new_full_field' in f,(oid,k,'approved replacement missing')
  target=obj['data'] if k in obj['data'] else obj;new=f['new_full_field'];target[k]=json.loads(new) if k.endswith('_json') else new
  table.append({'source':'C-0911','object':oid,'version':d['version'],'field':f['field'],'old_full_field':f['old_full_field'],'approved_new_full_field':new,'old_support':old_evidence,'full_current_context':cur,'disposition':'revise','reason':d.get('reason','Exact primary current source/name/date metadata amendment'),'exact_fullfield_match':True})
 for e in obj['evidence']:
  if e['object']=='R-5fcb723c98597da6131ddbea' and e['version']==1:e['version']=2
  if oid=='O-P-0043-related125-household_role_report' and e['object']=='M-P-0043-related125' and e['version']==1:e['version']=2
 audit='AUDIT-T0777-C0911-Torvald' if 'P-0045' in oid or oid=='READ-1d10384d6b063c8a24278ea7' else 'AUDIT-T0777-C0911-main'
 obj['evidence'].append({'object':audit,'version':1,'role':'supports','note':'T-0777 AC3: egna source-bound name/date/rolefält med ersatt läshistorik; äldre andra-källors reservationer och identiteter består.'})
 if oid=='F-P-0043-family_context-Elin-household-sequence':obj['evidence'].append({'object':'AUDIT-T0777-C0911-Ture','version':1,'role':'supports','note':'Eget senare äktenskapshushåll16–17, inte r9:s råroll.'})
 for e in d.get('append_evidence',[]):
  o,v=e.rsplit('@',1)
  if not any(x['object']==o and x['version']==int(v) for x in obj['evidence']):obj['evidence'].append({'object':o,'version':int(v),'role':'supports','note':'Explicit primary approved stronger existing C0035 own-name support.'})
 if oid in mids:meta.append(obj)
 else:current.append(obj)
for tag,changes in [('role-metadata',meta),('consequence',current)]:
 op={'id':f'T-0777/C0911-{tag}-candidate-v1','actor':'Codex Sol exact approved individual Astra dispositions','reason':f'T-0777 AC3–5: C0911 {tag} source-specific current corrections and approved same-row record/mention bindings; full metadata/evidence/origins retained, individual remaining dependency review later; canonical-ready after independent final review.','dependencyReviewVersion':2,'changes':changes};out=B/f'C-0911-{tag}-candidate-operation-v1.json';out.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n')
for row in table:
 change=next(x for x in meta+current if x['id']==row['object']);row['new_support']=copy.deepcopy(change['evidence']);row['operation']='T-0777/C0911-role-metadata-candidate-v1' if row['object'] in mids else 'T-0777/C0911-consequence-candidate-v1'
out=B/'C-0911-consequence-table-v1.json';out.write_text(json.dumps({'task':'T-0777','rows':table,'individually_revised_objects':len(meta)+len(current),'metadata_record_revision_separate':True,'new_roles':len(meta),'other_current_revisions':len(current)},ensure_ascii=False,indent=2)+'\n')
files=[B/f'C-0911-{t}-candidate-operation-v1.json' for t in ['role-metadata','consequence']]+[out]
(B/'C-0911-first-current-freeze-v1.json').write_text(json.dumps({'task':'T-0777','files':[{'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],'merged_explicit_primary_specs':['current-v1','currentamendment-v2','rolemetadata-v3','oldernamesupport-v4'],'record_M_support_rebinds_explicitly_approved':True},ensure_ascii=False,indent=2)+'\n')
print(len(meta),'M metadata revisions;',len(current),'other current revisions')
