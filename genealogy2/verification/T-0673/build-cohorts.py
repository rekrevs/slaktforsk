import json,hashlib,collections,argparse
from pathlib import Path
parser=argparse.ArgumentParser(description='Reproduce cohort allocation without overwriting locked artifacts.')
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
if args.output.exists(): parser.error('Output must not exist.')
root=Path(__file__).resolve().parents[3];base=root/'genealogy2/verification/T-0673';raw=(base/'manifest.json').read_bytes();m=json.loads(raw)
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
sets={'citations':{x['id']:x for x in m['citations']},'legacy_sources':{x['id']:x for x in m['legacy_sources']},'records':{x['object_id']:x for x in m['records']},'sources':{x['object_id']:x for x in m['sources']},'searches':{x['object_id']:x for x in m['searches']},'imported_assets':{x['path']:x for x in m['imported_assets']},'native_assets':{x['id']:x for x in m['native_assets']}}
cohorts=[];owners={k:{} for k in sets}
def cohort(kind,scope):
 c={'cohort_key':f'G{len(cohorts)+1:03d}','kind':kind,'scope':scope,'members':{k:[] for k in sets},'cross_references':[]};cohorts.append(c);return c

def own(c,kind,id):
 assert id not in owners[kind],(kind,id);owners[kind][id]=c['cohort_key'];c['members'][kind].append(id)
def chunks(items,n):
 for i in range(0,len(items),n):yield items[i:i+n]
p={r:r for r in sets['records']}
def find(x):
 while p[x]!=x:p[x]=p[p[x]];x=p[x]
 return x
def union(a,b):p[find(b)]=find(a)
keys={}
for r in m['records']:
 for k in r['suggested_group_keys']:
  if k.startswith(('image_sha256:','source_locator:')):
   if k in keys:union(r['object_id'],keys[k])
   else:keys[k]=r['object_id']
components=collections.defaultdict(list)
for rid in p:components[find(rid)].append(rid)
def disposition(r):
 if r['disposition'] in ('retired','rejected'):return 'historical'
 if r['record_type'] in ('owner_report','owner_statement','family_statement','relayed_family_statement'):return 'owner'
 if any(t in r['record_type'] for t in ('catalog','archive_inventory','archival_title','register_description','volume_contents')):return 'metadata'
 return 'substantive'
def component_kind(ids):
 kinds={disposition(sets['records'][r]) for r in ids};return next(iter(kinds)) if len(kinds)==1 else 'substantive_mixed'
groups=collections.defaultdict(list)
for ids in components.values():groups[component_kind(ids)].append(sorted(ids))
component_rows=[]
for kind in sorted(groups,key=lambda x:(x not in ('substantive','substantive_mixed'),x)):
 c=None
 for ids in sorted(groups[kind],key=lambda ids:(sets['records'][ids[0]]['source_id'],ids[0])):
  if c is None or len(c['members']['records'])+len(ids)>50:
   c=cohort('record_'+kind,'At most 50 current records; complete relevant posts, with separate historical/owner/metadata outcomes. Shared-image/source-locator component stays intact.')
  for rid in ids:own(c,'records',rid)
  component_rows.append({'key':'RC-'+digest(ids)[:16],'record_ids':ids,'owner_cohort':c['cohort_key']})
# Citation scope must be reconciled even when record review already exists.
for cid,cit in sets['citations'].items():
 candidates=sorted({owners['records'][r] for r in cit['native_record_ids'] if r in owners['records']})
 if candidates:
  c=next(c for c in cohorts if c['cohort_key']==candidates[0]);own(c,'citations',cid)
for part in chunks(sorted(set(sets['citations'])-set(owners['citations'])),50):
 c=cohort('citation_scope','At most50 unmapped citations: reconcile whole claimed scope, other native targets, negatives/history/owner cases; do not treat missing direct record mapping as absence of research.')
 for cid in part:own(c,'citations',cid)
# Searches remain primary units, not absorbed into a citation's title disposition.
for outcome in sorted({s['outcome'] for s in m['searches']}):
 for part in chunks(sorted(s['object_id'] for s in m['searches'] if s['outcome']==outcome),40):
  c=cohort('search_'+outcome,'At most40 current searches: original scope/keys/coverage/access and registered conclusions; referenced record/image readings reused exactly, never counted as new independent evidence.')
  for sid in part:own(c,'searches',sid)
# Sources are description/dependence review, not another manual reread of all images.
for part in chunks(sorted(sets['sources']),100):
 c=cohort('source_description','At most100 native source descriptions plus mapped legacy descriptions: correct identity, coverage, provenance and dependence; exact original readings belong to record/image owners.')
 for sid in part:
  own(c,'sources',sid)
  for legacy in sets['sources'][sid]['legacy_source_ids']:
   if legacy not in owners['legacy_sources']:own(c,'legacy_sources',legacy)
for part in chunks(sorted(set(sets['legacy_sources'])-set(owners['legacy_sources'])),100):
 c=cohort('legacy_source_description','Unmapped legacy source descriptions remain explicitly owned and receive linkage/history disposition.')
 for sid in part:own(c,'legacy_sources',sid)
# One asset-content owner; aliases and references never imply independent evidence.
asset_groups=collections.defaultdict(list)
for kind in ('imported_assets','native_assets'):
 for id,a in sets[kind].items():asset_groups[a['sha256']].append((kind,id))
linked_by_sha=collections.defaultdict(set)
for r in m['records']:
 for kind,id in r['current_media']:
  asset=sets['imported_assets' if kind=='imported' else 'native_assets'][id]
  linked_by_sha[asset['sha256']].add(owners['records'][r['object_id']])
reading=[];unlinked=[]
for sha,members in sorted(asset_groups.items()):
 candidates=sorted(linked_by_sha[sha])
 if candidates:
  assert len(candidates)==1,(sha,candidates)
  c=next(c for c in cohorts if c['cohort_key']==candidates[0])
  for kind,id in members:own(c,kind,id)
  reading.append({'sha256':sha,'owner_cohort':c['cohort_key'],'asset_refs':[{'kind':k,'id':id} for k,id in members],'mode':'shared_record_reading','status':'unperformed'})
 else:unlinked.append((sha,members))
for part in chunks(unlinked,200):
 c=cohort('media_scope','At most200 distinct content hashes: classify provenance and exact relevant scope, reuse linked originals; explicit metadata/derivative/duplicate/historical disposition or bounded original reading. JSON/support files are not automatically separate manual original tasks.')
 for sha,members in part:
  for kind,id in members:own(c,kind,id)
  reading.append({'sha256':sha,'owner_cohort':c['cohort_key'],'asset_refs':[{'kind':k,'id':id} for k,id in members],'mode':'media_scope_triage_then_required_reading','status':'unperformed'})
# Exact cross references to the single owners; no second task owns these units.
bykey={c['cohort_key']:c for c in cohorts}
def ref(frm,to,reason,entity):
 if frm!=to:bykey[frm]['cross_references'].append({'cohort':to,'reason':reason,'entity':entity})
for cid,cit in sets['citations'].items():
 co=owners['citations'][cid]
 for rid in cit['native_record_ids']:
  if rid in owners['records']:ref(co,owners['records'][rid],'record_scope',rid)
 for path in cit['legacy_media_paths']:
  if path in owners['imported_assets']:ref(co,owners['imported_assets'][path],'media_provenance_only',path)
for r in m['records']:
 co=owners['records'][r['object_id']];ref(co,owners['sources'][r['source_id']],'source_description',r['source_id'])
 for cid in r['citation_ids']:ref(co,owners['citations'][cid],'whole_citation_scope',cid)
for s in m['searches']:
 co=owners['searches'][s['object_id']];ref(co,owners['sources'][s['source_id']],'search_source',s['source_id'])
 for cid in s['citation_ids']:ref(co,owners['citations'][cid],'search_citation_scope',cid)
 for d in s['dependencies']:
  if d['basis_object_id'] in owners['records']:ref(co,owners['records'][d['basis_object_id']],'exact_dependency_revision:'+d['basis_revision_id'],d['basis_object_id'])
# Association rows are secondary provenance, not extra primary reading tasks.
support_rows={}
for key in ('document_object_associations','record_media_associations','known_T0110_audits','duplicate_content_paths'):
 support_rows[key]=[]
 for i,row in enumerate(m[key]):
  if key=='document_object_associations':co=owners['records'].get(row['object_id']) or owners['sources'][row['object_id']]
  elif key=='record_media_associations':co=owners['records'][row['object_id']]
  elif key=='known_T0110_audits':co=owners['citations'][row['object_id'].split('AUDIT-T0110-')[1]]
  else:co=next(r['owner_cohort'] for r in reading if r['sha256']==row['sha256'])
  support_rows[key].append({'manifest_index':i,'row_sha256':digest(row),'owner_cohort':co})
checks={}
for kind,items in sets.items():
 allocated=[id for c in cohorts for id in c['members'][kind]]
 checks[kind]={'manifest_count':len(items),'allocated_count':len(allocated),'unique_allocated_count':len(set(allocated)),'missing':sorted(set(items)-set(allocated)),'extra':sorted(set(allocated)-set(items))}
 assert len(allocated)==len(set(allocated))==len(items) and set(allocated)==set(items)
for c in cohorts:
 for kind in c['members']:c['members'][kind].sort()
 c['cross_references']=sorted({json.dumps(x,sort_keys=True):x for x in c['cross_references']}.values(),key=lambda x:(x['cohort'],x['reason'],x['entity']))
 c['member_counts']={k:len(v) for k,v in c['members'].items() if v}
result={'schema':'genealogy2-original-revision-cohort-proposal/1','task':'T-0673','state':'proposal_not_execution_state','manifest_sha256':hashlib.sha256(raw).hexdigest(),'constraints':{'max_records':50,'max_unmapped_citations':50,'max_searches':40,'max_native_source_descriptions':100,'max_unlinked_content_hashes':200,'wotan_ids_allocated':False,'bearing_priority':'Not derivable from this manifest. Before execution, assess actual identity/relation dependency and sole-support status in current native graph; reorder bounded tasks without dropping any units. Genre is not proof of bearing status.','pilot_reuse':'No pilot/audit auto-pass; task owner must compare exact scope, revisions and continuing uncertainties before reusing reading.','shared_image_rule':'One primary reading owner per SHA256, with explicit references and separate exact record/citation/search scope checks; mandatory independent second readings remain permitted and are not duplicate primary scheduling.','baseline_support':'53 operations and baseline hashes are immutable provenance, not manual review units.'},'cohorts':cohorts,'record_components':sorted(component_rows,key=lambda r:r['key']),'content_reading_owners':sorted(reading,key=lambda r:r['sha256']),'support_association_owners':support_rows,'union_checks':checks,'summary':{'cohort_count':len(cohorts),'cohorts_by_kind':dict(collections.Counter(c['kind'] for c in cohorts)),'record_components':len(component_rows),'max_component_records':max(len(r['record_ids']) for r in component_rows),'distinct_content_hashes':len(reading),'planned_final_independent_review_tasks':1}}
with args.output.open('x') as handle:
 handle.write(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print(json.dumps(result['summary'],indent=2));print(json.dumps(checks,indent=2))
