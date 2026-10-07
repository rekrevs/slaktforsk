import pathlib,json
P=pathlib.Path(__file__).resolve().parent;B=P.parent;x=json.loads((P/'C1047-individual-consequence-table-DRAFT-v1.json').read_text());retains={}
for n,key in [('C-1047-individual-retains-v1.json','rows'),('C-1047-initial49-final-retains-v2.json','rows'),('C-1047-current-source-decisions-v1.json','retains')]:
 for d in json.loads((B/'source-review'/n).read_text())[key]:retains[d['object']]={**d,'source_spec':n}
revisions={r['object']:r for r in json.loads((P/'C1047-current-consequence-table-v1.json').read_text())['rows']}
for r in json.loads((P/'C1047-metadata-consequence-table-v1.json').read_text()):revisions[r['object']]=r
out=[]
for r in x['rows']:
 oid=r['object'];assert (oid in retains)!=(oid in revisions),(oid,'missing or overlapping disposition');out.append({**r,'source_disposition':'revise' if oid in revisions else 'retain','settled_decision':revisions.get(oid,retains.get(oid))})
result={'task':'T-0778','baseline':277,'rows':out,'revise':sum(r['source_disposition']=='revise' for r in out),'retain':sum(r['source_disposition']=='retain' for r in out)};(P/'C1047-initial49-complete-consequence-table-v2.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(len(out),result['revise'],result['retain'])
