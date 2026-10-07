"""Settled root-authorized postactual10 Wotan administration only; no research or canonical write."""
import datetime,hashlib,json,shutil,sqlite3,subprocess
from pathlib import Path
B=Path('evaluations/T-0780');W=B/'implementation/postactual-ten-owner-administration-v1';assert not W.exists()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def readpin(p):
 q=Path(p['path']);assert sha(q)==p['sha256'];return json.loads(q.read_text())
def ptr(x,p):
 for k in p.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
 return x
def save(n,d):
 p=W/n;assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return pin(p)
planp=B/'implementation/resumed-future-owner-Wotan-append-only-plan-v2/finite-individual-Wotan-append-only-administrative-review-plan-v2.json';assert sha(planp)=='76409c6bcb890d2ea078a9705839643ac7310a16967662ac89d66514baa93976';plan=json.loads(planp.read_text())
reviewp=B/'root-future-owner22-append-review-v2.json';review=json.loads(reviewp.read_text());assert review['plan_sha256']==sha(planp);reviews={x['owner']:x for x in review['reviews']}
ledger=readpin(plan['source_ledger_pin']);ownp=B/'fresh-independent-review/resumed-all45-future-owner-independent-component-index-v1.json';assert sha(ownp)=='1b917baa436fec3304cb553fda5abda1197d6e26eee40e7e9d8f50fb5481e1c9';own=json.loads(ownp.read_text());assert own['source_ledger_pin']==plan['source_ledger_pin'] and own['count']==45 and not own['open_findings']
ap=B/'root-actual-canonical-ten-program-acceptance-v1.json';rp=B/'actual-ten-accepted-remaining21-reconciliation-v1.json';r=json.loads(rp.read_text());a=readpin(r['actual_root_acceptance_receipt_pin']);assert r['actual_root_acceptance_receipt_pin']==pin(ap)
assert a['approved_for_program_acceptance'] is a['actual_stage_comparison_pass'] is a['independent_exact_hash_final_pass'] is a['protected_knowledge_and_review_state_pass'] is True
assert a['actual_canonical_state']==r['actual_canonical_state']=={'journal_head':425,'pending':0};assert r['actual_accepted_count']==10 and r['remaining_count']==21 and r['fixed_total_citation_scopes']==31
assert [x['citation'] for x in r['actual_individually_accepted_receipts']]==a['accepted_citation_scopes']
for x in r['actual_individually_accepted_receipts']:
 receipt=readpin(x['receipt_pin']);assert receipt['root_acceptance_receipt']==pin(ap) and receipt['journal']==425 and receipt['pending']==0 and receipt['citation']==x['citation']
for x in [a['primary_final_review'],a['independent_final_review'],a['actual_stage_comparison'],a['actual_all50_and_ordered_native_comparison']]:readpin(x)
main=Path('genealogy2/data/research.sqlite');mainpin=pin(main);c=sqlite3.connect(main.resolve().as_uri()+'?mode=ro',uri=True);assert c.execute('select max(sequence) from operation_payload').fetchone()[0]==425 and c.execute('select count(*) from pending_review').fetchone()[0]==0;c.close()
backlogp=Path('wotan/backlog.json');backlogbytes=backlogp.read_bytes();backlog=json.loads(backlogbytes);assert backlog['next_id']==782;tasks={x['id']:x for x in backlog['tasks']};assert 'T-0782' not in tasks and not Path('wotan/dev-log/T-0782.md').exists()
entries=plan['selected_individual_append_candidates'];assert len(entries)==len({x['owner'] for x in entries})==22
checked=[]
for x in entries:
 owner=x['owner'];source=ptr(ledger,x['source_individual_disposition_pointer']);assert source['owner']==owner
 assert x['literal_settled_source_disposition']==source['disposition']
 p=Path(x['actual_tasklog_pin']['path']);old=p.read_bytes();assert sha(p)==x['actual_tasklog_pin']['sha256']==x['preserved_current_before_pin']['sha256']
 append=Path(x['append_text_pin']['path']);proposed=Path(x['complete_proposed_tasklog_pin']['path']);assert sha(append)==x['append_text_pin']['sha256'] and sha(proposed)==x['complete_proposed_tasklog_pin']['sha256']
 assert proposed.read_bytes()==old+append.read_bytes()
 assert tasks[owner]['status']==x['current_backlog_status'] and tasks[owner].get('after',[])==x['current_backlog_after']
 assert reviews[owner]['append_sha256']==sha(append) and reviews[owner]['root_full_append_read'] is reviews[owner]['prefix_exact'] is True
 checked.append({'owner':owner,'current_tasklog_pin':pin(p),'exact_append_pin':pin(append),'expected_full_after_pin':pin(proposed),'current_backlog_entry':tasks[owner],'root_prior_individual_review':reviews[owner],'source_individual_disposition_pointer':x['source_individual_disposition_pointer']})
proposal=ledger['new_bounded_owner_proposals'][0];assert proposal==plan['new_Carl_owner_proposal_deferred_no_ID_reserved'][0] and proposal['person']=='P-0435';assert own['Carl_proposal']['exact_source_pointer']=='/new_bounded_owner_proposals/0'
# Fresh narrow exact route duplicate check, not a new source/evidence judgment.
cmd=['rg','-n','P-0435|Carl Reinhold|folio.?668|målfolio668','wotan/backlog.json','wotan/dev-log','--glob','*.md'];scan=subprocess.run(cmd,capture_output=True,text=True);assert scan.returncode in [0,1]
routehits=[line for line in scan.stdout.splitlines() if ('folio668' in line or 'folio 668' in line or 'målfolio668' in line)]
assert all(line.startswith('wotan/dev-log/T-0780.md:') for line in routehits),'Unexpected existing finite route candidate; return Astra'
assert not any('folio668' in json.dumps(t,ensure_ascii=False) or 'folio 668' in json.dumps(t,ensure_ascii=False) for t in backlog['tasks'] if t['id']!='T-0780'),'Unexpected backlog route candidate'
# Preserve all unrelated tasklogs and every existing backlog entry, including root-owned task checkpoints.
alllogpins={str(p):sha(p) for p in Path('wotan/dev-log').glob('*.md')};affected={x['actual_tasklog_pin']['path'] for x in entries}
now=datetime.datetime.now(datetime.timezone.utc).isoformat();newtask={'id':'T-0782','status':'BLOCKED','size':'M','after':['T-0780'],'summary':'Carl Reinhold P-0435: egen fortsättningspost på Sävarfolio668','note':'Ändlig följdägare från T-0780:s source/independent-granskade ledger /new_bounded_owner_proposals/0 efter faktisk G00210acceptance. C0561 egen668,1877 23[?]/11; målfolio endast. Ingen automatisk kedja eller researchstart inom ägarens nästa exakt2 G002-mandat.','blocker':'T-0780:s administrativa slutförande; själva källpassagen startas först inom ett separat beslutat körmandat.'}
log=f'''# T-0782: Carl Reinholds egen fortsättningspost på folio668

**Status**: BLOCKED | **Size**: M
**Phase**: -

## Context och mandat

Root har efter T-0780:s faktiska tiopostersacceptans auktoriserat registrering av den individuellt källbedömda och oberoende granskade följdägaren. Detta är endast administration; inget nytt original öppnas eller forskningsarbete startar. T-0780 är föregångare. Ägarens efterföljande exakt två G002-poster i T-0781 ger inget körmandat för denna uppgift.

Läs wotan/README.md, genealogy2/README.md och genealogy2/docs/working.md samt docs/research/person-contract.md, research-program.md, source-strategy.md och riksarkivet-access.md vid framtida start. Aktuell kunskap läses och skrivs i genealogy2; äldre profiler är arkivunderlag. Astra avgör käll-/identitets-/följdfrågor, Sol implementerar explicit avgjorda ändringar och separat Astra granskar.

## Scope och befintligt underlag

Person: P-0435 Carl Reinhold; ingen ny generation eller annan syskonpassage. Fråga: {proposal['question']}

Exakt godkänt omfång: {proposal['scope']}

Egen söknyckel: {proposal['source_key']} Känd personkorrelation: Carl Reinhold1853-01-21. Återbruka T-0780:s accepterade fulla C-0561-post och TR-T0780-C0561-fullpost@1 samt aktuella person-/research-/supportobjekt med deras faktiska versioner och reservationer. Ingen tyst latest-rebind eller ny oberoende evidensröst. Den befintliga egna födelse-/identitetsforskningen tillgodoräknas; saknade nya mallfält kräver inte rutinomläsning.

Stoppgräns: {proposal['stop']}

Utanför: automatisk vidare folio-/flyttkedja, andra syskons original, amerikanska källor, antagen fysisk flyttdag från bokdatum eller strykning, full person-/identitets-/livsbildsuppgradering utan eget omfång; arkivbeställning, ArkivDigital, dashboard, PDF, publicering, commit/push. Om målfoliot inte kan säkert identifieras eller flera konkurrerande poster kräver större omfång, stanna och bevara exakt följdfråga.

Dubblettavstämning: source-ledgerns individuella förslag och separat granskare fann ingen befintlig ändlig folio668ägare. T-0197:s kohortrouting till T-0616 ger inte denna uppgift dess mandat; T-0616:s övriga egna passager bevaras. Färsk exakt routingkontroll vid registreringen fann endast T-0780:s administrativa förslag. T-0781 äger redan nästa exakt två G002-poster och används inte för denna passage.

## Acceptance Criteria

- [ ] Aktuell P-0435/person/research, äldre tillräckliga original, accepterad C-0561-post och starkare stöd avstämda; aktuella versioner, exakt käll-/plats-/tidsomfång och målfolio668 låsta före ny originaltolkning.
- [ ] Rätt måloriginal identifierat via tillåten källrouting. Hela relevanta person-/familjerader, rubriker, egna dittos, blankfält och marginaler utvunna eller olästa delar exakt redovisade, med originalhash och provenans.
- [ ] Korrelationsalternativ och datum-/platsgränser individuellt bedömda av Astra; strykning eller bokdag är inte ensam fysisk flytt. Positivt, exakt avgränsat negativt eller olöst utfall har rätt räckvidd.
- [ ] Nya egna söknycklar prövade mot berörda currentcopy-/supportberoenden och anhörigkontext. Berörd research får native adoption eller exakt tillräckligt återbruk; gamla supportversioner och OWNER_CONFIRMED bevaras. Följdbehov utanför målfoliot får separat ändlig ägare, ingen automatisk kedja.
- [ ] Separat Astra granskar käll- och följdutfall, starkare äldre stöd och den exakta korrigerade paketversionen. Kontrollerad versionerad apply/journal med task/AC och individuellt avgjorda beroenden; tillämpliga validators, inventory och verifiedpedigree.
- [ ] Kunskapsresultat, begränsningar, vad task-DONE inte avslutar och konkret följdägare dokumenterade. Alla förberedelser, granskningar, initiala försök, reparationer och faktisk tillgänglig modellusage redovisade; okänd usage anges okänd.

## Approach

Återbruka först tillräcklig tidigare forskning och den exakt accepterade egen668nyckeln. Identifiera därefter endast målfoliot och korrelera den egna relevanta raden till P-0435. Utför inga andra personers eller fortsatta sidors forskning genom denna registrering.

## Återupptagning

Uppdaterat: {now}. Utfört: framtida ägare registrerad från T-0780:s faktiskt accepterade resultat, utan ny källpassage. Godkänt underlag: [source-ledger v4](../../evaluations/T-0780/source-review/resumed-all10-finite-future-owner-ledger-v4.json), exakt /new_bounded_owner_proposals/0; [oberoende komponentgranskning](../../evaluations/T-0780/fresh-independent-review/resumed-all45-future-owner-independent-component-index-v1.json); [actualtenacceptance](../../evaluations/T-0780/root-actual-canonical-ten-program-acceptance-v1.json). Nästa ej utförda steg: efter föregångaren och separat körmandat, aktuell scope-/version-/reuseavstämning och målfolio668routing. Hinder: T-0780:s administrativa slutförande. Inga original lästa eller canonicaländringar genom denna taskregistrering.

## Verification

Sakgranska slutsatser mot fulla relevanta original och alternativa korrelationer med separat Astra. Kör relevanta kommandon i wotan/README.md när uppgiften faktiskt utförs; gröna tester är ingen källgranskning. Registreringen verifieras separat i T-0780:s administrativa kvitto.

## Outcome

Ej utfört. Endast ändlig framtida ägare registrerad; inga nya sourceclaims, granskningstillstånd eller programkvitton.
'''
W.mkdir();(W/'current-backlog-before-administration-v1.json').write_bytes(backlogbytes);(W/'fresh-Carl782-duplicate-routing-hits-v1.txt').write_text(scan.stdout);(W/'fresh-Carl782-duplicate-routing-stderr-v1.txt').write_text(scan.stderr)
amendment={'task':'T-0780','at_utc':now,'root_delegated_authorization':'Exact22 append texts and Carl782 allocation after actualtenacceptance; no other task/status/rootlog or canonical changes.','prior_plan_pin':pin(planp),'historical_whole_backlog_pin':plan['current_backlog_pin'],'fresh_current_backlog_pin':pin(backlogp),'preserved_fresh_backlog_pin':pin(W/'current-backlog-before-administration-v1.json'),'reason':'Whole backlog changed through root-controlled task checkpoints/phases; historic pin remains provenance, not fresh current equality claim. Each22 tasklog fullprefix/status/after and exact appendix independently unchanged.','actual10_acceptance_pin':pin(ap),'actual_remaining21_reconciliation_pin':pin(rp),'source_ledger_pin':plan['source_ledger_pin'],'independent45_owner_index_pin':pin(ownp),'prior_root22_individual_review_pin':pin(reviewp),'exact22_individual_fresh_guards':checked,'freshnext_id':782,'Carl_proposal_pointer':'/new_bounded_owner_proposals/0','fresh_duplicate_exact_route_existing_owner_IDs':['T-0780'],'no_new_source_judgment':True}
save('fresh-individual22-prefix-status-after-and-historical-backlog-metadata-amendment-v1.json',amendment)
# All acceptance, source, duplicate, prefix and allocation guards have passed before any Wotan mutation.
applied=[]
for x in entries:
 p=Path(x['actual_tasklog_pin']['path']);assert sha(p)==x['actual_tasklog_pin']['sha256']
 with p.open('ab') as f:f.write(Path(x['append_text_pin']['path']).read_bytes())
 assert sha(p)==x['complete_proposed_tasklog_pin']['sha256'];applied.append({'owner':x['owner'],'before_pin':x['actual_tasklog_pin'],'append_pin':x['append_text_pin'],'after_pin':pin(p),'historical_prefix_exact':True})
 save('append-receipts/'+x['owner']+'-exact-authorized-append-v1.json',applied[-1])
assert backlogp.read_bytes()==backlogbytes,'Concurrent backlog change; stop before allocation'
newlog=Path('wotan/dev-log/T-0782.md');assert not newlog.exists();newlog.write_text(log)
backlog['tasks'].append(newtask);backlog['next_id']=783;backlogp.write_text(json.dumps(backlog,ensure_ascii=False,indent=2)+'\n')
after=json.loads(backlogp.read_text());before=json.loads(backlogbytes);assert after['tasks'][:-1]==before['tasks'] and after['tasks'][-1]==newtask and after['next_id']==783
for path,h in alllogpins.items():
 if path not in affected:assert sha(path)==h,('Unrelated/root tasklog changed',path)
assert sha(main)==mainpin['sha256'],'Canonical DB changed during administration'
result={'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual10_acceptance_pin':pin(ap),'actual_remaining21_reconciliation_pin':pin(rp),'fresh_guard_and_backlog_amendment_pin':pin(W/'fresh-individual22-prefix-status-after-and-historical-backlog-metadata-amendment-v1.json'),'source_ledger_pin':plan['source_ledger_pin'],'independent45_owner_index_pin':pin(ownp),'root_prior_exact22_review_pin':pin(reviewp),'exact22_append_receipts':applied,'allocated_Carl_task':newtask,'allocated_Carl_log_pin':pin(newlog),'exact_source_proposal_pointer':'/new_bounded_owner_proposals/0','fresh_duplicate_hit_pin':pin(W/'fresh-Carl782-duplicate-routing-hits-v1.txt'),'backlog_before_pin':pin(W/'current-backlog-before-administration-v1.json'),'backlog_after_pin':pin(backlogp),'prior781_entries_exact':True,'all_other_existing_tasklogs_unchanged':True,'existing_status_after_or_scope_changes':0,'canonical_DB_pin_unchanged':mainpin,'new_research_or_canonical_execution':False,'actual_model_usage':None,'usage_observability':'Parent collects actual new-turn usage after worker final; unavailable here'}
p=save('actual22-appends-and-Carl782-allocation-administrative-completion-receipt-v1.json',result);print(json.dumps({'receipt_pin':p,'appended':len(applied),'new_task':'T-0782','new_status':'BLOCKED','next_id':783,'canonical_unchanged':True},indent=2))
