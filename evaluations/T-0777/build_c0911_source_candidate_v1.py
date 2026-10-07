import pathlib,json,hashlib
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1]
src=B/'source-review/C-0911-source-v1.md';text=src.read_text();headers=text.split('## Printed columns\n\n',1)[1].split('## All own-row cells',1)[0].strip();raw=text.split('## All own-row cells\n\n',1)[1].split('## Settled corrections',1)[0].strip();decision=text.split('## Settled corrections and implications\n\n',1)[1]
assert raw.count('h.Emma Wilhelmina Rhodin[?]')==1
raw=raw.replace('h.Emma Wilhelmina Rhodin[?]','h.Emma Wilhelmina Karlsson').replace('97 21/3 Skedevi,Östergötl.l.','97 [21/31]/3 Skedevi,Östergötl.l.')
decision=decision.replace('Existing1888-04-27/Jäder/nameRhodin[?] stay source-bound','Existing1888-04-27/Jäder stay source-bound; own surname Karlsson supersedes older Rhodin[?] reading history')
changes=[]
def ev(o,v,n):return {'object':o,'version':v,'role':'supports','note':n}
limit='Samma församlingsboks-/attestkedja; daterade registreringar är inte resdag eller fysisk kontinuitet. Inget nytt identitets-/föräldrabeslut eller P för sidopersoner. Historiska TR-läsningar bevaras men nya egna datum och namn ersätter7/9,15/10,3juli och Rhodin[?] för denna post. C0910:s2[?]/7förblir egen reservation, utan bestämd dagkonflikt. Astrids egen dag[21/31] reserverad; starkare1897-03-21original behålls.'
def add(oid,kind,data,bases,caveat):changes.append({'id':oid,'kind':kind,'expectedVersion':None,'data':data,'origins':[],'evidence':bases,'disposition':'recorded','evidenceStatus':None,'rationale':'T-0777 AC2–4: full own-row extraction with exact source amendments and bounded existing-person adoption, no new identity judgments.','caveat':caveat})
groups=[('main','R-c2061a9ef8456576c3564fbf',[1,2,3,4,6,7,9]),('Torvald','R-5fcb723c98597da6131ddbea',[11,12,13]),('Ture','R-836c129ec57720e26352a023',[16,17])]
recordbases={}
for tag,rid,nums in groups:
 bases=[ev(rid,1,'Avgränsade egna rader på Ljungbacka402.'),ev('S-0733',1,'Källmetadata from ownR; actual source ID must be mechanically verified.')];recordbases[tag]=bases
 # Keep exact source printed headers and own selected table rows only.
 lines=raw.splitlines();selected=[line for line in lines if not line.startswith('|') or line.startswith('|Row/') or line.startswith('|---') or any(line.startswith('|'+str(n)+' ') for n in nums)]
 tr=f'TR-T0777-C0911-{tag}-fullfields';audit=f'AUDIT-T0777-C0911-{tag}'
 add(tr,'transcription',{'record_id':rid,'text':headers+'\n\n'+'\n'.join(selected),'reading_note':limit},bases,limit)
 add(audit,'assessment',{'subject_id':rid,'criteria':'original_revision/1','outcome':'reviewed_with_limits','body':json.dumps({'own_rows':nums,'settled_source_decisions':decision,'amendments':[json.loads((B/'source-review/C-0911-source-amendment-v2.json').read_text()),json.loads((B/'source-review/C-0911-source-amendment-v3.json').read_text())]},ensure_ascii=False,indent=2)},bases+[ev(tr,1,'Tryckta rubriker och samtliga egna celler.')],limit)
for pid,tag,rows in [('P-0042','main',[1]),('P-0043','main',[2]),('P-0047','main',[4]),('P-0045','Torvald',[11,12,13]),('P-0046','main',[3,9])]:
 bases=recordbases[tag]+[ev('AUDIT-T0777-C0911-'+tag,1,'Avgjord fullpostgranskning.')]
 if pid=='P-0046':bases+=recordbases['Ture']+[ev('AUDIT-T0777-C0911-Ture',1,'Eget nya äktenskapshushållr16–17, hustruns egen giftcell tom.')];rows+=[16,17]
 add('ADOPT-T0777-C0911-'+pid,'assessment',{'subject_id':pid,'criteria':'bounded_source_adoption/1','outcome':'reviewed_with_limits','body':json.dumps({'person':pid,'own_source_context_rows':rows,'source':'Ljungbacka402, tre avgränsade grupper','limits':limit,'individual_bound':'Inga sidopersoner sammanförs till nya P; make/hustruassociation från källroller och egen huvudpersons datum är inte egna blankcellers ditto.'},ensure_ascii=False,indent=2)},bases,limit)
# Replace speculative metadata label with exact existing source IDs.
cards=json.loads((B/'selection.json').read_text())['cards'];ownids={r['id']:r['source_id'] for card in cards if card['citation']=='C-0911' for r in card['records']}
for ch in changes:
 for e in ch['evidence']:
  if e['object']=='S-0733':
   own=next(e['object'] for e in ch['evidence'] if e['object'] in ownids);e['object']=ownids[own];e['note']='Versionsbunden faktisk source_id för den egna källposten.'
op={'id':'T-0777/C0911-source-candidate-v1','actor':'Codex Sol mechanical settled source implementation','reason':'T-0777 AC2–4: all13occupied own rows in three source records with corrected rawdates/name and ownblank/reserved fields; five existing-person bounded adoptions; canonical-ready after independent final review.','dependencyReviewVersion':2,'changes':changes};out=B/'C-0911-source-candidate-operation-v1.json';out.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');(B/'C-0911-first-source-freeze-v1.json').write_text(json.dumps({'task':'T-0777','files':[{'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [src,B/'source-review/C-0911-source-amendment-v2.json',B/'source-review/C-0911-source-amendment-v3.json',out]],'first_source_candidate':True},ensure_ascii=False,indent=2)+'\n');print(len(changes),'new source objects')
