from pathlib import Path
import urllib.request, urllib.error, hashlib, json, datetime, concurrent.futures
base=Path(__file__).resolve().parent
ids=['00081278_00100','00081309_00091','C0033097_00044','C0033097_00045','C0033097_00046','00201572_00038','00201572_00039','00201572_00042','00201572_00043']+[f'00201547_{n:05d}' for n in [10,11,13,14,15,16,17,18,19]]
def fetch(image_id):
 url=f'https://lbiiif.riksarkivet.se/arkis!{image_id}/full/max/0/default.jpg'
 r={'image_id':image_id,'url':url,'fetched_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'provider_version':'unknown','method':'GET exact known Image API URL; Referer sameimage viewer; no discovery search','read_status':'not yet visually read'}
 path=base/(image_id+'.jpg')
 if path.exists():
  data=path.read_bytes();r.update(status='existing_do_not_redownload',sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),path=str(path));return r
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Referer':f'https://sok.riksarkivet.se/bildvisning/{image_id}'})
  with urllib.request.urlopen(req,timeout=40) as response:
   data=response.read();r.update(status=response.status,final_url=response.url,headers=dict(response.headers.items()))
  if not data.startswith(b'\xff\xd8'):raise ValueError('Response is not JPEG; preserve separately, do not claim original')
  path.write_bytes(data);r.update(sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),path=str(path))
 except Exception as e:
  r.update(outcome='access_problem',error=str(e))
  if isinstance(e,urllib.error.HTTPError):
   data=e.read();ep=base/(image_id+'-access-response.bin');ep.write_bytes(data);r.update(status=e.code,response_path=str(ep),response_sha256=hashlib.sha256(data).hexdigest(),headers=dict(e.headers.items()))
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:receipts=list(ex.map(fetch,ids))
out={'task':'T-0828','exact_original_units':18,'results':receipts}
(base/'original-fetch-receipts-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps([{'id':r['image_id'],'status':r.get('status'),'error':r.get('error'),'bytes':r.get('bytes')} for r in receipts]))
