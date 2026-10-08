import pathlib,subprocess,json,hashlib,datetime,concurrent.futures,time
R=pathlib.Path.cwd();D=R/'evaluations/T-0810/originals';start=time.monotonic();ids=['00205394_00087','00205396_00087'];log=[]
def request(url,stem,ref=None):
 p=D/stem;hdr=D/(stem+'.headers');args=['curl','-sS','-L','--max-time','60','-D',str(hdr),'-o',str(p),'-w','%{http_code}'];
 if ref:args+=['-e',ref]
 r=subprocess.run(args+[url],capture_output=True,text=True);entry={'url':url,'referer':ref,'date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':r.returncode,'http':r.stdout,'stderr':r.stderr,'body_path':str(p.relative_to(R)),'headers_path':str(hdr.relative_to(R))};log.append(entry);return p,entry
def fetch(url,stem,ref):
 p,e=request(url,stem)
 if e['exit']==0 and e['http']=='200':return p
 if e['exit']==0 and e['http']in ['401','403']:
  p,e=request(url,stem+'.referer',ref)
  if e['exit']==0 and e['http']=='200':return p
 raise RuntimeError(json.dumps(e))
def unit(image):
 rep=image.split('_')[0];mp=next((R/'genealogy/media').glob('*'+rep+'*manifest*.json'));m=json.load(open(mp));cv=next(x for x in m['items'] if x['id'].endswith(image+'/canvas'));ref='https://sok.riksarkivet.se/bildvisning/'+image;info=fetch('https://lbiiif.riksarkivet.se/v2/arkis!'+image+'/info.json',image+'-info.json',ref);ip=json.load(open(info));url=cv['items'][0]['items'][0]['body']['id'];assert image in url and '/full/max/'in url;img=fetch(url,image+'.jpg',ref);u={'image_id':image,'existing_manifest_path':str(mp.relative_to(R)),'manifest_sha256':hashlib.sha256(mp.read_bytes()).hexdigest(),'exact_manifest_canvas':cv,'info_path':str(info.relative_to(R)),'info':ip,'original_path':str(img.relative_to(R)),'sha256':hashlib.sha256(img.read_bytes()).hexdigest(),'bytes':img.stat().st_size,'width':ip['width'],'height':ip['height'],'provider_version':'unknown','provenance':'T-0810 exact source/independent/root-adopted Gertrud own-row material; full/max IIIF acquisition. Sol preserves copy metadata only, no image interpretation.'};return u
try:
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:units=list(pool.map(unit,ids))
 (D/'two-acquired-originals-v1.json').write_text(json.dumps({'units':units,'elapsed_seconds':time.monotonic()-start},ensure_ascii=False,indent=2)+'\n');print([(u['image_id'],u['width'],u['height'],u['sha256'])for u in units])
finally:(D/'actual-http-attempts-v1.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
