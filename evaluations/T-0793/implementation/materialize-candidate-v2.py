import json,re,hashlib
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0793';I=D/'implementation'
p=json.loads((D/'primary-front-assessment-v4.json').read_text());transfer=json.loads((D/'fixed160-successor-transfer-v1.json').read_text());app=(D/'proposed-T0813-full-life-rest-appendix-v1.md').read_text()
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
pins='\n'.join(f'- `{x}` SHA256 `{sha(D/x)}`' for x in ['primary-front-assessment-v4.json','first-T0806-settled-spec-v2.json','fixed160-successor-transfer-v1.json'])
new=[];parts=[];append={}
for t in p['proposed_tasks']:
 tid=t['id'];summary='Individuell identitetsbedömning: '+', '.join(t['persons'])
 entry=dict(id=tid,status='READY',size='M',after=[],summary=summary,priority='CORE_IDENTITY',priority_basis='PCD-2026-10-07-003; T-0793 SOURCE-prövad avgränsad närfront. Accepterat återbruk först; V3 individuella källenheter styr, ingen generell originalpromovering eller kontinuerligt körmandat.')
 text=f'# {tid}: {summary}\n\n**Status**: READY | **Size**: M\n\n## Exakt beslutsunderlag och mandat\n\n'+pins+'\n\n'+p['execution_interpretation']+'\n\n'+t['execution_authority']+'\n'
 for title,key in [('Bedömningsordning','stages'),('Scope och kandidatens övre gräns','scope'),('Accepterat återbruk','reuse'),('Förlustfri partition och restägare','partition'),('Utanför','exclusions')]:
  text+='\n## '+title+'\n\n'+'\n'.join('- '+v for v in t[key])+'\n'
 text+='\n## Styrande individuella källenhetsbeslut\n\n```json\n'+json.dumps([u for u in p['individual_source_unit_dispositions'] if u['task']==tid],ensure_ascii=False,indent=2)+'\n```\n'
 text+='\n## Acceptance Criteria\n\n'+'\n'.join(f'{n}. {v}' for n,v in enumerate(t['acceptance'],1))+'\n\n## Återupptagning\n\nEj påbörjad. Första steg är aktuell individuell bedömning enligt bedömningsordningen, inte att öppna kandidatens original. Endast T-0806 har aktuellt startmandat efter godkänd T-0793-kö; övriga kräver faktiskt utförandemandat.\n'
 new.append({'entry':entry,'devlog_text':text})
 for s in t['partition']:
  parts.append({'new_owner':tid,'literal_partition':s})
  # Leading old owner identifies the appendix destination; no scope interpretation.
  m=re.match(r'(T\d{4})',s)
  if m: append.setdefault('T-'+m[1][1:],[]).append((tid,s))
# Explicit other old owners named by approved partition statements get reference-only appendices.
for tid in ['T-0214','T-0215','T-0227','T-0241','T-0420']:
 for part in parts:
  if tid.replace('-','') in part['literal_partition'] and (part['new_owner'],part['literal_partition']) not in append.setdefault(tid,[]):append[tid].append((part['new_owner'],part['literal_partition']))
s=p['successor'];entry=dict(id='T-0813',status='READY',size='M',after=[],summary='Fast 160-anors planeringsägarskap och nästa avgränsade vågcheckpoint',priority='CORE_SUPPORT',priority_basis='PCD-2026-10-07-003; exakt T-0793 fast160-överföring och fulla livsbildsrester. Aktiv planeringsägare; ingen djupare forskningsauktorisation eller krav att alla sju identitetsuppdrag är DONE.')
text='# T-0813: Fast 160-anors planeringsägarskap\n\n**Status**: READY | **Size**: M\n\n## Exakt beslutsunderlag\n\n'+pins+'\n\n'
for title,key in [('Scope','scope'),('Återstartvillkor','trigger'),('Första avgränsade checkpoint','first_bounded_checkpoint'),('Livsbild och tidigare ägare','life')]:text+='## '+title+'\n\n'+s[key]+'\n\n'
text+='## Acceptance Criteria\n\n1. Exakt fast160-union och samtliga individuella planposter bevaras enligt den hashbundna överföringen; inga bortfall eller nya personer.\n2. Första checkpoint utförs enligt ovan utifrån faktiskt resultat/hinder, balanserat på närmaste nivå; djupare130 är planering, inte godkänt källutförande.\n3. Alla äldre livsbildsfrågor och ägare bevaras ordagrant nedan; ingen taskstatus eller fullkontraktsuppfyllelse härleds av denna överföring.\n\n## Återupptagning\n\nEj påbörjad. READY aktiv planeringsägare; väljs enligt faktiskt mandat och återstartvillkor, inte automatiskt efter alla sju.\n\n'+app
new.append({'entry':entry,'devlog_text':text})
apps=[]
for tid,items in append.items():
 if not items:continue
 txt='\n\n## T-0793 förlustfri närfrontsplanering 2026-10-07\n\nÄldre full scope, AC, checkpoint och status ovan bevaras. V3:s individuella källenhetsbeslut styr över kandidatens tak; ingen ännu ej utförd originalenhet överförs ovillkorligt. Eventuell nödvändig enhet kräver exakt SOURCE/oberoende godkänd ändring före utförande.\n\n'+'\n'.join(f'- {owner}: {s}' for owner,s in items)+'\n'
 apps.append({'task_id':tid,'append_text':txt})
proposal={'new_tasks':new,'next_id':814,'insert_before_id':'T-0217','existing_log_appends':apps,'fixed160_ownership':transfer,'scope_partitions':{'governing_v3_sha256':sha(D/'primary-front-assessment-v4.json'),'execution_interpretation':p['execution_interpretation'],'partitions':parts,'individual_source_unit_dispositions':p['individual_source_unit_dispositions']}}
f=I/'literal-wotan-proposal-v2.json';f.write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n');print(sha(f));print([x['task_id'] for x in apps])
