import pathlib,subprocess,json,hashlib,datetime,concurrent.futures
D=pathlib.Path('evaluations/T-0809/originals');ids=['C0005986_00067','C0005986_00140','C0008071_00031','C0008071_00283','C0018074_00019','F0004585_00026'];log=[]
def fetch(url,stem,ref):
 p=D/stem;headers=D/(stem+'.headers');args=['curl','-sS','-L','--max-time','60','-e',ref,'-D',str(headers),'-o',str(p),'-w','%{http_code}',url];r=subprocess.run(args,capture_output=True,text=True);entry={'url':url,'referer':ref,'date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':r.returncode,'http':r.stdout,'stderr':r.stderr,'body_path':str(p),'headers_path':str(headers)};log.append(entry)
 if r.returncode or r.stdout!='200':raise RuntimeError(json.dumps(entry))
 return p
for rep in dict.fromkeys(x.split('_')[0] for x in ids):
 if rep=='C0005986':continue
 fetch('https://lbiiif.riksarkivet.se/arkis!'+rep+'/manifest',rep+'-manifest-referer.json','https://sok.riksarkivet.se/bildvisning/'+next(x for x in ids if x.startswith(rep)))
def unit(i):
 rep=i.split('_')[0];m=json.loads((D/(rep+'-manifest-referer.json')).read_text());canvas=next(x for x in m['items'] if x['id'].endswith(i+'/canvas'));ref='https://sok.riksarkivet.se/bildvisning/'+i
 info=fetch('https://lbiiif.riksarkivet.se/v2/arkis!'+i+'/info.json',i+'-info.json',ref);ip=json.loads(info.read_text());img=fetch(canvas['items'][0]['items'][0]['body']['id'],i+'.jpg',ref)
 return {'image_id':i,'manifest_canvas':canvas,'info':ip,'original_path':str(img),'sha256':hashlib.sha256(img.read_bytes()).hexdigest(),'bytes':img.stat().st_size,'width':ip['width'],'height':ip['height'],'provider_version':'unknown','provenance':'T-0809 exact adopted six-image scope; Riksarkivet IIIF full/max download with own viewer Referer; Sol metadata acquisition only, no own-row interpretation.'}
try:
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:units=list(pool.map(unit,ids))
 (D/'six-acquired-media-v1.json').write_text(json.dumps({'units':units,'http_requests':log},ensure_ascii=False,indent=2)+'\n');print([(x['image_id'],x['width'],x['height'],x['sha256']) for x in units])
finally:(D/'actual-http-log-v1.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
