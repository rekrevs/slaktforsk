import pathlib,json
B=pathlib.Path(__file__).resolve().parent
rows=json.loads((B/'C-0911-exact-old-date-candidates-v1.json').read_text())['rows'];out=[]
shared_old='Dagkonflikten1915-07-03 mot2[?]/7, orterna Rhodin[?]/Darby[?]/Värnamo[?] och Maggis obelagda mor kvarstår.'
shared_new='C-0911 visar hustruns dödsdatum och Torvalds änkedatum1915-07-02; C-0910:s egen2[?]/7-reservation består utan en bestämd3-mot2-konflikt. Emma har källformen Karlsson i C-0911, jämte Karlsson[?] i C-0035; det äldre Rhodin[?]-förslaget är en ersatt läsning, inget namnbyte. Darby[?]/Värnamo[?] och Maggis obelagda mor kvarstår.'
for x in rows:
 changes=[]
 for f in x['fields']:
  old=f['old_full_quote'];new=old
  if x['object']=='O-C0910-Karl-Harry-row5':
   new=old.replace('Den separata C-0911-observationen O-P-0043-related122-household_role_report@2 bevarar 1906-09-07. Den källskillnaden är olöst här; ingen rättelse av ett ej omläst original eller ny identitetsprövning.','C-0911:s egen rad6 har nu lästs1906-09-17 och stämmer med denna C-0910-rads17/9; den tidigare7-mot17-skillnaden är ersatt läshistorik. Ingen ny P-identitet eller föräldraprövning följer.')
  elif x['object']=='F-P-0043-family_context-Karl-Harry-sequence':
   new=old.replace('T-0676 läser C-0910 rad 5 som 06 17/9; C-0911-observationen O-P-0043-related122-household_role_report@2 bevarar 1906-09-07. Dagskillnaden är olöst här och påverkar inte genom automatisk harmonisering den redan införda källföljden.','C-0910rad5 och den nu direktlästa C-0911rad6 ger båda06 17/9. Det äldre7/9-förslaget är ersatt läshistorik, ingen kvarstående bestämd dagkonflikt; källföljden förblir beroende.')
  else:
   new=new.replace(shared_old,shared_new).replace('1906-09-07','1906-09-17').replace('1914-10-15','1914-10-16').replace('14 15/10','14 16/10').replace('1915-07-03','1915-07-02').replace('Emma Wilhelmina Rhodin[?]','Emma Wilhelmina Karlsson')
   if x['object'] in ['P-0045/Q-02','PATH-P-0045-KP-02']:
    new=new.replace('död 1915-07-02 enligt C-0911 men\n  `2[?]/7` enligt C-0910.','död1915-07-02 enligt den nu egna C-0911-läsningen;\n  C-0910:s kopierade `2[?]/7` är fortfarande reserverad, utan en bestämd dagkonflikt.')
    new=new.replace('den\n  senare avgörande mellan de två dagarna.','den\n  senare kan ge händelsens egen originaluppgift, plats och orsak; en bestämd3-mot2-skillnad mellan hushållsböckerna kvarstår inte.')
    new=new.replace('De två änkedagarna bevaras båda och normaliseras\n  inte.','C-0911:s döds- och änkedatum2juli ersätter den äldre3juli-läsningen; C-0910:s egen2[?]/7-reservation bevaras. Den egna dödsakten är fortsatt oläst.')
    new=new.replace('Karlsson[?] är en reserverad källform jämte senare Rhodin[?], inte ett beslutat namnbyte eller en ny kvinna.','Karlsson[?] i C-0035 stämmer med nu läst Karlsson i C-0911. Det äldre Rhodin[?]-förslaget är ersatt läshistorik, inget namnbyte eller ny kvinna.')
    new=new.replace('dödsdagen1915 förblir olösta.','dödsaktens egen uppgift1915 förblir oprövad; C-0911 ger ett källbundet2juli-ankare.')
    new=new.replace('vilket avgör läsosäkerheterna `Rhodin[?]` och\n  `Darby[?]`','vilket kan ge egen namnuppgift och pröva\n  `Darby[?]`').replace('vilket avgör\n  konflikten mellan C-0911 och C-0910','vars originaluppgift ännu inte är läst; bestämd\n 3-mot2-dagkonflikt mellan hushållsböckerna kvarstår inte').replace('änkedagen1915-07-02 eller `2[?]/7`','källbundet änkedatum1915-07-02, jämte kopierad `2[?]/7`').replace('änkedagen 1915-07-02 eller `2[?]/7`','källbundet änkedatum1915-07-02, jämte kopierad `2[?]/7`').replace('namnet med båda efternamnsformerna','Emma Karlsson med äldre reserverad Karlsson[?]-form').replace('två\n  läsosäkerheter, en bevarad konflikt och en öppen moderskapsfråga','kvarstående\n  ursprungsuppgifter, plats/orsak och en öppen moderskapsfråga')
  if new!=old:changes.append({'field':f['field'],'old_full_field':old,'proposed_new_full_field':new,'expected_whole_field_match':True})
 if changes:out.append({'object':x['object'],'version':x['version'],'kind':x['kind'],'fields':changes,'full_current':x['full_current'],'disposition':'PROPOSED_REVISE_REQUIRES_ASTRA','reason':'Mechanical exact source-specific dates and replacement-history precision under settled C0911-v1/v2; no independent interpretation.'})
# Existing named firstwife own mention and own observations may not have old date matches.
m=json.loads((B/'current-manifest.json').read_text());caps={x['id']:x for x in m['captures'] if x['view']=='inspect'}
for oid in ['M-P-0045-wife1']:
 cap=caps[oid];d=json.loads(pathlib.Path(cap['path']).read_text());cur=d['current'];old=cur['name_literal'];assert old=='Emma Wilhelmina Rhodin[?]'
 out.append({'object':oid,'version':d['currentVersion'],'kind':d['kind'],'fields':[{'field':'name_literal','old_full_field':old,'proposed_new_full_field':'Emma Wilhelmina Karlsson','expected_whole_field_match':True}],'full_current':cur,'disposition':'PROPOSED_REVISE_REQUIRES_ASTRA','reason':'C0911-v2 settled own name; no person identity/namechange event.'})
(B/'C-0911-exact-replacement-proposals-v1.json').write_text(json.dumps({'task':'T-0777','status':'TEXT_PROPOSALS_ONLY_NOT_APPROVED_NOT_IMPLEMENTED','rows':out,'count':len(out)},ensure_ascii=False,indent=2)+'\n')
print(len(out),'exact current object proposals for Astra approval')
