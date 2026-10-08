import pathlib,json,hashlib,importlib.util,re,subprocess
R=pathlib.Path.cwd();P=R/'evaluations/T-0812/preparation';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);c=h.conn(R/'genealogy2/data/research.sqlite');objects=[h.native(c,x[0])for x in c.execute("select r.id from revision r where r.evidence_status='OWNER_CONFIRMED' and not exists(select 1 from revision x where x.object_id=r.object_id and x.version>r.version)")];bases={}
for n in objects:
 for e in n['evidence']:bases[e['basis_revision_id']]=h.native(c,e['basis_revision_id'])
pcids=sorted(set(re.findall(r'PCD-\d{4}-\d{2}-\d{2}-\d{3}',json.dumps(objects+list(bases.values()),ensure_ascii=False))));lines=(R/'PROJECT-CONTROL.md').read_text().splitlines();sections=[]
for pid in pcids:
 starts=[i for i,l in enumerate(lines)if l.startswith('## ')and pid in l];assert len(starts)==1;start=starts[0];end=next((i for i in range(start+1,len(lines))if lines[i].startswith('## ')),len(lines));sections.append({'decision_id':pid,'full_exact_section':'\n'.join(lines[start:end])+'\n'})
(P/'all-current-OWNER-scope-v1.json').write_text(json.dumps({'OWNER_full_native':objects,'direct_bound_owner_basis':list(bases.values()),'exact_PC_sections':sections,'PC_pin':{'path':'PROJECT-CONTROL.md','sha256':sha(R/'PROJECT-CONTROL.md')},'qualification':'All45current OWNER scopes for Astra relevance decision; ownliteral0 never absence claim.'},ensure_ascii=False,indent=2)+'\n')
support=json.load(open(P/'exact-support-native-v1.json'))['revisions'];units=[]
for code in ['0274','0456']:
 records=[]
 for n in support:
  if n['kind']!='record':continue
  origins=[]
  for o in n['origins']:
   u=c.execute('select *from unit where id=?',(o['unit_id'],)).fetchone()
   if u and ('C-'+code+'-'in u['document_path']or u['legacy_id']in ['C-'+code,'C'+code]):origins.append(dict(u))
  if origins:
   assets=[]
   for a in n['assets']:
    ar=dict(c.execute('select *from asset where path=?',(a['asset_path'],)).fetchone());p=R/ar['path'];ar['local_exists']=p.exists()
    if p.exists():ar['actual_sha256']=sha(p);ar['actual_bytes']=p.stat().st_size;assert ar['actual_sha256']==ar['sha256'];ar['dimension_metadata']=subprocess.run(['sips','-g','pixelWidth','-g','pixelHeight',str(p)],capture_output=True,text=True,check=True).stdout
    assets.append({'record_edge':a,'asset':ar})
   records.append({'record':n,'origins':origins,'local_original_metadata':assets,'native_media':n['media']})
  
 units.append({'citation':'C-'+code,'records':records,'qualification':'Proposed source ceiling metadata only, no images viewed or promoted.'})
(P/'proposed-two-unit-media-metadata-v1.json').write_text(json.dumps({'units':units,'images_opened':0,'metadata_only':True},ensure_ascii=False,indent=2)+'\n');print('OWNER',len(objects),'bases',len(bases),'PC',len(sections),'unitsrecords',[(x['citation'],len(x['records']))for x in units])
