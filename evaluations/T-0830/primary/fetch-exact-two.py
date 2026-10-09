import urllib.request,urllib.error,pathlib,json,hashlib,datetime
p=pathlib.Path('evaluations/T-0830/primary');out=[]
for image_id in ['C0005634_00013','C0005633_00014']:
 url='https://lbiiif.riksarkivet.se/arkis!'+image_id+'/full/max/0/default.jpg';start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Referer':'https://sok.riksarkivet.se/bildvisning/'+image_id})
 try:
  with urllib.request.urlopen(req,timeout=40) as r:data=r.read();status=r.status;headers=dict(r.headers);final=r.url
 except urllib.error.HTTPError as e:data=e.read();status=e.code;headers=dict(e.headers);final=e.url
 except urllib.error.URLError as e:data=str(e).encode();status='TRANSPORT_ERROR';headers={};final=url
 ext='.jpg' if status==200 and data[:2]==b'\xff\xd8' else '.response';f=p/(image_id+ext);f.write_bytes(data)
 out.append({'image_id':image_id,'request_url':url,'final_url':final,'requested_at':start,'status':status,'headers':headers,'provider_version':'unknown','path':str(f),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'referer':req.headers.get('Referer')})
 (p/'exact-two-fetch-receipts-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False))
