import argparse,pathlib,json,sqlite3,copy
B=pathlib.Path(__file__).resolve().parent;a=argparse.ArgumentParser();a.add_argument('spec');a.add_argument('name');args=a.parse_args();c=sqlite3.connect(B/'clone/c1060-candidate-v2.sqlite');c.row_factory=sqlite3.Row;ns={'connection':c};exec((B/'native_payload.py').read_text(),ns);cs=[];rows=[]
for d in json.loads((B/'source-review'/args.spec).read_text())['changes']:
 ch=ns['existing'](d['object'],d['expectedVersion']);old=copy.deepcopy(ch)
 for f in d['fields']:
  p=ch if f['field'] in ch else ch['data'];assert p[f['field']]==f['before'],(d['object'],f['field'],'wholefield mismatch');p[f['field']]=f['after']
 for e in d.get('append_supports',[]):ch['evidence'].append({**e,'note':e.get('note','T-0778 AC2/5: individuellt avgjord aktuell kopieprecisering med accepterat källstöd.')})
 for e in d.get('approved_evidence_rebinds',[]):
  oid,v=e['before'].rsplit('@',1);dst,nv=e['after'].rsplit('@',1);found=[z for z in ch['evidence'] if z['object']==oid and z['version']==int(v)];assert len(found)==1,(d['object'],e,'rebindmatches');found[0].update(object=dst,version=int(nv))
 cs.append(ch);rows.append({'object':d['object'],'version':d['expectedVersion'],'exact_fields':d['fields'],'old_full_payload':old,'new_full_payload':ch,'source_decision':args.spec,'disposition':'revise','approved_rebinds':d.get('approved_evidence_rebinds',[])})
x={'id':'T-0778/'+args.name,'actor':'Codex Sol mechanical implementation of exact Astra decisions','reason':'T-0778 AC2/5: avgjorda individuella kopieprecisioner; daterad tidigare läsning och övriga fält bevaras.','dependencyReviewVersion':2,'changes':cs};(B/(args.name+'-operation-v1.json')).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');(B/(args.name+'-consequence-table-v1.json')).write_text(json.dumps({'task':'T-0778','revisions':rows},ensure_ascii=False,indent=2)+'\n');print(len(cs),'candidatechanges')
