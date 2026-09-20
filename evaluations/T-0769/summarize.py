import pathlib,json,statistics,math,csv
b=pathlib.Path(__file__).resolve().parent
measure=json.loads((b/'measurements.json').read_text());mapping=json.loads((b/'blind-map.private.json').read_text());reverse={v:k for k,v in mapping.items()};rates=json.loads((b/'prices.json').read_text())['rates'];protocol={r['id']:r for r in json.loads((b/'protocol-review.json').read_text())};rows=[]
for r in measure:
 bid=reverse[r['id']];p=b/'scores'/f'{bid}.final.json';score=json.loads(p.read_text()) if p.exists() else {}
 u=r['usage'];ip,cp,op=rates[r['model']];cost=((u.get('input_tokens',0)-u.get('cached_input_tokens',0))*ip+u.get('cached_input_tokens',0)*cp+u.get('output_tokens',0)*op)/1e6
 no_cache=(u.get('input_tokens',0)*ip+u.get('output_tokens',0)*op)/1e6
 rows.append({**r,'blind_id':bid,'passed':score.get('passed'),'score':score.get('score'),'maxScore':score.get('maxScore'),'critical_errors':score.get('critical_errors',[]),'material_pass':score.get('material_pass',score.get('passed')),'sensitivity_pass_without_F5':score.get('sensitivity_pass_without_F5'),'strict_packet_compliance':protocol.get(r['id'],{}).get('strict_packet_compliance'), 'formatting_only_failure':score.get('formatting_only_failure',False),'api_standard_proxy_usd':cost,'api_no_cache_proxy_usd':no_cache})
(b/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
summary=[]
for task in ['x','y','z']:
 for model in rates:
  rs=[r for r in rows if r['task']==task and r['model']==model];done=[r for r in rs if r['passed'] is not None];n=len(done);k=sum(r['passed'] for r in done)
  if not rs:continue
  z=1.96;ph=k/n if n else 0;den=1+z*z/n if n else 1;c=(ph+z*z/(2*n))/den if n else 0;h=z*math.sqrt(ph*(1-ph)/n+z*z/(4*n*n))/den if n else 0
  out={'task':task,'model':model,'started':len(rs),'scored':n,'passed':k,'wilson95':[c-h,c+h] if n else None,'median_seconds':statistics.median(r['seconds'] for r in rs if r['seconds'] is not None),'mean_standard_proxy_usd':statistics.mean(r['api_standard_proxy_usd'] for r in rs),'proxy_per_accepted_usd':sum(r['api_standard_proxy_usd'] for r in done)/k if k else None,'mean_no_cache_proxy_usd':statistics.mean(r['api_no_cache_proxy_usd'] for r in rs),'mean_score_fraction':statistics.mean(r['score']/r['maxScore'] for r in done) if done else None,'critical_failed_runs':sum(bool(r['critical_errors']) for r in done)}
  out['material_passed']=sum(bool(r['material_pass']) for r in done);out['without_F5_passed']=sum(bool(r['sensitivity_pass_without_F5']) for r in done) if task=='y' else None;clean=[r for r in done if r['strict_packet_compliance']];out['clean_n']=len(clean);out['clean_passed']=sum(r['passed'] for r in clean);out['clean_material_passed']=sum(bool(r['material_pass']) for r in clean);out['material_proxy_per_accepted_usd']=sum(r['api_standard_proxy_usd'] for r in done)/out['material_passed'] if out['material_passed'] else None;summary.append(out)
(b/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
with (b/'results.csv').open('w') as f:
 keys=['id','task','model','replicate','seconds','tool_calls','passed','score','maxScore','api_standard_proxy_usd','api_no_cache_proxy_usd'];w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(rows)
print('Summarized',len(rows),'runs;final scored',sum(r['passed'] is not None for r in rows))
