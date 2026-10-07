from pathlib import Path
import json,importlib.util
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);c=h.conn(R/'genealogy2/data/research.sqlite');main=h.pin(R/'genealogy2/data/research.sqlite');assert h.state(c)=={'journal_head':444,'pending':0}
oldindex=R/'evaluations/T-0788/preparation/complete-exact744-current444-media-and-accepted-reuse-lock-v1.json';prev=json.loads(oldindex.read_text());assert prev['actual_main_pin']==main
viewp=R/prev['whole_person_pins']['P-0007']['path'];assert h.sha(viewp)==prev['whole_person_pins']['P-0007']['sha256'];v=json.loads(viewp.read_text())
objects={};roots={'P-0007','S-0689','S-0694','AUDIT-T0676-20'}
for key in ['requirements','reviews']:
 for x in v['research'][key]:roots.add(x['object_id'])
for table,field in [('record','source_id')]:
 for r in c.execute('select cr.object_id from current_revision cr join record x on x.revision_id=cr.id where x.source_id=?',('S-0694',)):roots.add(r[0])
for oid in list(roots):
 rid=h.current(c,oid);objects[rid]=h.native(c,rid)
for rid,n in list(objects.items()):
 if n['kind']=='record':
  for table,field in [('transcription','record_id'),('assessment','subject_id')]:
   for r in c.execute('select cr.id from current_revision cr join '+table+' x on x.revision_id=cr.id where x.'+field+'=?',(n['object_id'],)):objects[r[0]]=h.native(c,r[0])
# Direct support of graveaudit and captured reviews, kept as complete actual native objects.
for n in list(objects.values()):
 for e in n['evidence']:objects[e['basis_revision_id']]=h.native(c,e['basis_revision_id'])
units={};docs={}
for n in objects.values():
 for e in n['origins']:
  u=dict(c.execute('select * from unit where id=?',(e['unit_id'],)).fetchone());units[u['id']]=u;d=dict(c.execute('select * from document where path=?',(u['document_path'],)).fetchone());docs[d['path']]=d
native=h.write(O/'Maj-current-native-PK-review-register-source-and-accepted-grave-inputs-v1.json',{'objects':objects,'origin_units':units,'documents':docs,'native_evidence_origins_order':'Native rowid order; rawsourceJSON unchanged','no_new_source_grade':True})
rows=[]
for reproduction,year,expectedJ,expectedK in [('00023815',1945,'00098','00120'),('00023816',1946,'00106','00131')]:
 p=R/('genealogy/media/S-0689-manifest-'+reproduction+'.json');d=json.loads(p.read_text());found=[]
 def find(v,path=''):
  if isinstance(v,dict):
   if 'Mantalsregister-J' in json.dumps(v.get('label'),ensure_ascii=False) or 'Mantalsregister-K' in json.dumps(v.get('label'),ensure_ascii=False):found.append((path,v))
   for k,w in v.items():find(w,path+'/'+k)
  elif isinstance(v,list):
   for i,w in enumerate(v):find(w,path+'/'+str(i))
 find(d)
 jp,jr=next((p,r) for p,r in found if 'Mantalsregister-J' in json.dumps(r['label']));kp,kr=next((p,r) for p,r in found if 'Mantalsregister-K' in json.dumps(r['label']));canvasID=jr['items'][0]['items'][0]['id'];assert canvasID.endswith(reproduction+'_'+expectedJ+'/canvas');assert kr['items'][0]['items'][0]['id'].endswith(reproduction+'_'+expectedK+'/canvas');i,canvas=next((i,x) for i,x in enumerate(d['items']) if x['id']==canvasID);image=canvas['items'][0]['items'][0]['body'];imageID=reproduction+'_'+expectedJ
 local=[h.pin(p) for p in (R/'genealogy/media').rglob('*'+imageID+'*') if p.is_file()];asset=[dict(r) for r in c.execute('select * from asset where path like ?',('%'+imageID+'%',))];na=[dict(r) for r in c.execute('select * from native_asset where original_name like ? or provenance like ?',('%'+imageID+'%','%'+imageID+'%'))]
 rows.append({'year':year,'manifest_pin':h.pin(p),'manifest_ID':d['id'],'manifest_label':d['label'],'canvas_count':len(d['items']),'exact_J_structure_pointer':jp,'whole_J_structure':jr,'exact_next_K_structure_pointer':kp,'whole_next_K_structure':kr,'exact_J_start_canvas_pointer':'/items/'+str(i),'whole_J_start_canvas_metadata':canvas,'known_full_image_URL':image['id'],'known_viewer_URL':'https://sok.riksarkivet.se/bildvisning/'+imageID,'known_dimensions':[canvas['width'],canvas['height']],'local_exact_filename_matches':local,'current_asset_ID_metadata_matches':asset,'current_native_asset_ID_provenance_matches':na,'Maj_own_record_canvas':'NOT_ESTABLISHED; J start is only exact metadata routing, not personhit','no_J_block_or_remote_read':True})
knownlocals=[]
for imageID in ['00023815_00099','00023816_00107']:
 p=R/('genealogy/media/C-0883-riksarkivet-'+imageID+'.jpg');knownlocals.append({'pin':h.pin(p),'bytes':p.stat().st_size,'scope':'Existing Arne original, not Maj own1945/46hit; no Sol imageopening'})
manifest=h.write(O/'two-exact-AIIc33-34-J-register-start-canvas-metadata-and-local-media-lock-v1.json',{'rows':rows,'existing_Arne_originals_excluded_as_Maj_hits':knownlocals,'scope':'At most one ownMaj1945 and1946 post plus relevantownregister; no broad20+page J sweep','current_access_status':'NOT_RECHECKED_BY_SOL','no_remote_fetch_or_original_opening':True})
loc=R/'evaluations/T-0784/mechanical-current442-preparation-v2/bounded-prior-accepted-source-receipt-and-current-native-locator-index-v1.json';old=json.loads(loc.read_text());receipts=old['groups']['T-0676'];assert all(h.sha(R/p['path'])==p['sha256'] for p in receipts)
assert main==h.pin(R/'genealogy2/data/research.sqlite') and h.state(c)=={'journal_head':444,'pending':0}
index=h.write(O/'complete-Maj-current444-accepted-grave-and-two-register-routing-lock-v1.json',{'task':'T-0789','actual_main_pin':main,'actual_state':h.state(c),'Maj_whole_current444_view_pin':h.pin(viewp),'whole_view_exact_acceptedT0784_reuse':True,'previous_full_current_and_protected42_lock_pin':h.pin(oldindex),'current_native_source_grave_input_pin':native,'two_register_manifest_media_route_pin':manifest,'existing_T0676_accepted_grave_receipt_pins':receipts,'current_grave_audit_revision_id':h.current(c,'AUDIT-T0676-20'),'current_grave_full_native_pointer':'/objects/'+h.current(c,'AUDIT-T0676-20'),'no_grave_original_or_other_source_read':True,'no_native_Wotan_status_or_source_grade_change':True,'next_unperformed':'Root exactJstart publicIIIF/referrer/access check; Astra must locate ownMajrow before any person claim','usage':'UNKNOWN pending root collector'});print(json.dumps({'index_pin':index,'native_count':len(objects),'known_J_start_full_image_URLs':[r['known_full_image_URL'] for r in rows]}));c.close()
