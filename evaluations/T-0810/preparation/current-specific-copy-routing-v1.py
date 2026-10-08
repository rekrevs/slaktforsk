import pathlib,json,re,time,hashlib,importlib.util
R=pathlib.Path.cwd();P=R/'evaluations/T-0810/preparation';start=time.monotonic();main=R/'genealogy2/data/research.sqlite';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=sha(main)
s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);c=h.conn(main);assert h.state(c)=={'journal_head':473,'pending':0}
patterns={'Gertrud_dates':r'1942-03-31|1951-06-18|1948-06-21|1951-11-22|31\s*4/12|48\s*21/6|51\s*22/11','Gertrud_material':r'C-?0677|00205394_00087|00205396_00087','Nils_context':r'P-?0467|Nils August','Erik_C0939':r'C-?0939|00198500_00116','accepted_C0244':r'C-?0244|60\s*28/1|1860-01-28|1860-02-28'}
compiled={k:re.compile(v,re.I)for k,v in patterns.items()};out=[]
for row in c.execute('select r.id from revision r where not exists(select 1 from revision x where x.object_id=r.object_id and x.version>r.version)'):
 n=h.native(c,row[0]);hits=[]
 for section in ['data','caveat','rationale']:
  vals=n.get(section)
  vals=vals if isinstance(vals,dict)else {section:vals}
  for field,value in vals.items():
   if value is None:continue
   text=value if isinstance(value,str)else json.dumps(value,ensure_ascii=False)
   matched={key:[{'start':m.start(),'end':m.end(),'literal':m.group(),'context':text[max(0,m.start()-160):m.end()+160]}for m in pat.finditer(text)]for key,pat in compiled.items()};matched={k:v for k,v in matched.items()if v}
   if matched:hits.append({'section':section,'field':field,'exact_old_value':value,'matches':matched})
 if hits:
  supports=[]
  for e in n['evidence']:
   rid=e.get('depends_on');rid=rid or e.get('target_revision_id')
   if rid:
    sn=h.native(c,rid);head=h.current(c,sn['object_id']);supports.append({'edge':e,'bound_full_native':sn,'current_full_native':h.native(c,head)if head!=rid else None})
  out.append({'object_id':n['object_id'],'version':n['version'],'revision_id':n['id'],'literal_routes':hits,'full_current_native':n,'direct_support_and_current_stronger':supports})
owner=[]
for row in c.execute('select r.id from revision r where not exists(select 1 from revision x where x.object_id=r.object_id and x.version>r.version)'):
 n=h.native(c,row[0]);t=json.dumps(n,ensure_ascii=False)
 if 'OWNER_CONFIRMED'in t and re.search(r'P-?0467|P-?0247|P-?0253|Nils August|Gertrud',t,re.I):owner.append(n)
assert sha(main)==before
result={'task':'T-0810','main_sha256':before,'state':h.state(c),'qualification':'Mechanical literal current-field routing only; hits are not source decisions or absence proof. Full old native and ordered arrays preserved. Current stronger versions shown separately without automatic rebind.','patterns':patterns,'objects':out,'OWNER_literal_scope_candidates':owner,'elapsed_seconds':time.monotonic()-start}
f=P/'current-specific-copy-routing-v1.json';assert not f.exists();f.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'path':str(f.relative_to(R)),'sha256':sha(f),'objects':len(out),'OWNER_candidates':len(owner),'elapsed_seconds':result['elapsed_seconds']}))
