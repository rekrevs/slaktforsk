import pathlib,json,sys
b=pathlib.Path(__file__).resolve().parent;cid=sys.argv[1];d=json.loads((b/(cid+'-impact.json')).read_text());rows=[]
for item in d['review']['items']:
 oid=item['object_id'];p=b/'current'/('inspect-'+oid.replace('/','__')+'.json');x=json.loads(p.read_text());cur=x['current'];row={'id':oid,'version':x['currentVersion'],'kind':x['kind'],'reasons':item['reasons'],'current':{k:v for k,v in cur.items() if k in ['property','criteria','value_literal','value_json','outcome','decision','subject_id','record_id','mention_id','person_id','date_json','role']},'capture':str(p),'source_spans':{}}
 for k in ['body','markdown','caveat','rationale','text']:
  v=cur.get(k)
  if isinstance(v,str):
   terms=[cid.lower(),cid.lower().replace('-',''),'1930','kyrkobok','födelse','blank','okän'] if cid=='C-0027' else [cid.lower(),cid.lower().replace('-',''),'mineberg','420','1900','1907']
   lines=[l for l in v.splitlines() if any(t in l.lower() for t in terms)]
   if lines:row['source_spans'][k]=lines
 rows.append(row)
(b/(cid+'-dependency-disposition-input.json')).write_text(json.dumps({'rows':rows,'truncated_relevant_spans':False,'excluded_unmatched_fields':'Complete fields and history at each capture path; no substantive judgement implied.'},ensure_ascii=False,indent=2)+'\n');print(cid,len(rows),'rows')
