import json,pathlib,sqlite3,datetime,hashlib,native_payload
B=pathlib.Path(__file__).resolve().parent;native_payload.connection=sqlite3.connect('file:'+str(B/'clone/research-candidate-v5.sqlite')+'?mode=ro',uri=True);native_payload.connection.row_factory=sqlite3.Row
op=json.loads((B/'independent-IF2-operation-v1.json').read_text());d=next(x for x in json.loads((B/'independent-findings-decisions-v2.json').read_text())['findings'] if x['id']=='IF3');obj=native_payload.existing(d['object'],d['version']);assert obj['data'][d['field']]==d['old_quote'];obj['data'][d['field']]=d['approved_replacement'];obj['rationale']+=' T-0776 AC3: '+d['reason']
for binding in d['evidence']:
 oid,ver=binding.rsplit('@',1)
 if not any(e['object']==oid and e['version']==int(ver) for e in obj['evidence']):obj['evidence'].append({'object':oid,'version':int(ver),'role':'supports','note':'T-0776: individuellt Astra-prövad befintlig familjerad och bokföringsankare.'})
op['changes'].append(obj);op['id']='T-0776/independent-IF2-IF3-amendment-v1';op['reason']='T-0776 AC3–4: exakt rättelse av falsk oläst-beskrivning och separat vägutfall; kontrollerad kanonisk införsel efter självständig slutgranskning.'
p=B/'independent-IF2-IF3-operation-v1.json';p.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');(B/'independent-IF2-IF3-freeze-v1.json').write_text(json.dumps({'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[{'path':str(q),'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for q in [p,B/'independent-findings-decisions-v2.json']]},indent=2)+'\n')
a=sqlite3.connect('file:'+str(B/'clone/research-candidate-v5.sqlite')+'?mode=ro',uri=True);b=sqlite3.connect(B/'clone/research-candidate-v6.sqlite');a.backup(b);b.close()
print('2 independent exact corrections frozen')
