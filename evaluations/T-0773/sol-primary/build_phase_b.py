import json,copy,pathlib,hashlib,datetime,re
root=pathlib.Path('evaluations/T-0773');out=root/'sol-primary/phase-b';out.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text())
def wr(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def field(raw,state='read',qualifier=''):return dict(raw=raw,state=state,qualifier=qualifier)
adjudications=[]; matrices={}
def setf(c,r,k,raw,state='read',why=''):
 old=copy.deepcopy(matrices[c]['rows'][r]['fields'].get(k))
 matrices[c]['rows'][r]['fields'][k]=field(raw,state,why)
 adjudications.append(dict(case=c,row=matrices[c]['rows'][r]['row_id'],field=k,first=old,phase_b=matrices[c]['rows'][r]['fields'][k],basis=why))
for c in 'ABCDE':
 matrices[c]=read(root/f'sol-primary/{c}-raw.json');matrices[c]['phase']='B v1; both frozen raw files retained; original reread and older baseline consulted'
 matrices[c]['independent_frozen_matrix_sha256']=hashlib.sha256((root/f'sol-independent/{c}-raw.json').read_bytes()).hexdigest()
 matrices[c]['same_original_rule']='Two readings/crops are quality control, not independent historical witnesses.'
# Correct plainly disproved raw proposals and hold genuinely uncertain cells.
setf('A',4,'birth_month','3?','uncertain','Both raw readers suggest3; crossed ink remains; old C0028 correction20March reused separately, not forced into newSCBcertainty.')
setf('A',5,'maiden_name','f.[?] Ålund[?]','uncertain','First independent segmentation proposed residence; phaseB image reinspection supports maiden-name/änka proposal but reserves segmentation.')
setf('B',1,'name','Karl [Fredrik/Ludvik?] [Jansson/Godvik?]','uncertain','Different blind proposals remain; no name/person identity revision. Existing chain of563 household,61/Mellösa,marriage86,Charlotta andArne reused.')
setf('B',2,'birthplace','Lerbo; 〃','read','B-phaseB-birthplaces.png has own Lerbo word; ditto is county from Södl. on precedingrow, not placeMellösa.')
setf('B',2,'birth_year','67','read','B-phaseB-birthplaces.png shows67; independent69 remains first-pass history.')
setf('B',3,'name','Arne Godvig [Jansson/Ingvar?]','uncertain','Do not copy canonicalJansson as assured diplomatic reading; raw finalname remains uncertain.')
setf('B',4,'birthplace','Skedevi, Östg.l.','read','Own phaseBbirthplacecrop has Östg.l.; first Vstl. proposal disproved by ownglyphs.')
setf('B',6,'birthplace','Östermalm,Sthm (struket)','read','Rödtext physically after500 reads Sthm.[?], notFlens; no changed parish normalized.')
setf('B',6,'mother_registration_place','500; rött Sthm.[?]','uncertain','Underprintedcolm; no codekey or actualmotherparishconclusion.')
for i,code in enumerate(['213','000','232','X-','242','X-']):
 setf('B',i,'mother_registration_place',code,'read','Physically inside printed m-column in B-phaseB-headerbirth.png; statistical-looking rawcode, NOT a normalised assertion of motherregistrationplace.')
for i in range(7):
 old=matrices['B']['rows'][i]['fields'].pop('book_year')
 setf('B',i,'marriage_dissolution_year',old['raw'],'read' if old['raw'] else 'empty','Correct printed header: År för äktenskapets upplösning, not församlingsbokyear.')
 old=matrices['B']['rows'][i]['fields'].pop('baptism_sv_kyrkan')
 setf('B',i,'communion_sv_kyrkan','—' if i==3 else 'm/n-liknande tecken','read' if i==3 else 'uncertain','Correct printed headercol12: Inom sv.kyrkan begått nattv.; no baptism fact.')
setf('B',4,'marriage_year','','empty','25 lies upplösningsår beside franskildkv slash, notvigselår.')
setf('B',4,'marriage_dissolution_year','25','read','Direct header-grid alignment, cannot become a full exactdivorcedate.')
matrices['B']['headers']['12']='Inom sv.kyrkan begått nattv.';matrices['B']['headers']['9-10']='År för äktenskapets upplösning; sist inflyttad från plats och år'
matrices['B']['boundary_notes'].append('PhaseB: targetisKarl/Charlotta/Arne; Anna and Astrid/Emmy/KarlIngvar are separate administrative groups retained only for fullphysicalboundarycontext. No adjacentpersonadoption.')
setf('C',2,'residence','i Djursätra Westerg.[?]','uncertain','Own parentcrop and Dheading support Westerg.-proposal over firstMellang.; suffix not forcedfull.')
setf('D',0,'birth_year','1850','read','Both firstblindreaders1830 were wrong. Independent D-phaseB-detail.png viewed; flat top thenroundedlowerdigit supports5, compare1831 onprecedingrow.')
setf('D',1,'birthplace','Kyrkefalla Skarab.','read','IndependentD-phaseB-detail.png viewed; own Hogstena and secondHyrkefalla firstproposals rejected; initialK withyrkefalla.')
for i in [2,3]:setf('D',i,'birthplace','d:o','read','Ditto to ownKyrkefalla onAugusta row, no majoritynormalizationtoVärsås.')
matrices['D']['boundary_notes']=[x.replace('Djursätra Mellangården','Djursätra Westergården').replace('Hogstena','Kyrkefalla') for x in matrices['D']['boundary_notes']]
matrices['D']['uncertainties']=[x.replace('Djursätra Mellangården och Hogstena-läsning har smärre ortografisk reservation.','First Mellangården/Hogstena proposals rejected at phaseB; rawcorrected toWestergården/Kyrkefalla.') for x in matrices['D']['uncertainties']]
setf('E',0,'birth_year','58','read','IndependentE-phaseB-year.png viewed; own30 and earlier38 visualproposal rejected; upper5hook andtwo8loops. Existing1858/1850sourceconflict retained.')
setf('E',1,'birth_year','67[?]','uncertain','Own63 is not assured; re-viewed glyph may67. Older1867representation retained asold claim, not newtwo-readerexactverification.')
setf('E',1,'birthplace','Mofalla, Skarab.l.','read','IndependentE-phaseB-year.png viewed; ownHogstena/secondKyrkefalla firstproposals rejected; ownMo-falla glyph.')
setf('E',8,'name','[Brita/Brita?] [Herma/Johanna?] Fride[?]','uncertain','Dräng row and ogiftm remain raw; full personalname not resolvable atimagequality.')
setf('E',9,'name','Sofia [Afia/Carolina?]','uncertain','Competing frozen forms; no newidentity.')
setf('E',9,'birthplace','[Carls…/Carlskyrka?], d:o','uncertain','Competing forms andlowresolution; countyditto only.')
matrices['B']['uncertainties']=[x.replace('Arnes baptismkolumn visar streck; inte evidens för ej döpt.','Arnes nattvardskolumn visar streck; ingen dopuppgift i denna kolumn.') for x in matrices['B']['uncertainties']]
matrices['E']['boundary_notes']=[x.replace('moderns Hogstena','moderns Mofalla') for x in matrices['E']['boundary_notes']]
matrices['E']['uncertainties']=[x.replace('30,63,86','58,67[?],86') for x in matrices['E']['uncertainties']]
for c,d in matrices.items():wr(out/f'{c}-adjudicated-v1.json',d)
wr(out/'field-adjudications-v1.json',adjudications)
print('matrices',len(matrices),'explicitfielddecisions',len(adjudications))
# Bounded, individually attributable retention decisions; no inferred dependencies from text hits.
initial={};bycase={};bindings={}
for c,cit in zip('ABCDE',['C-0020','C-0021','C-0023','C-0024','C-0025']):
 d=read(root/f'baseline-context/{cit}-current-objects.json');bycase[c]=d['current'];initial.update(d['current']);bindings[c]=read(root/f'baseline-context/{cit}-record-binding.json')
full=read(root/'baseline-context/full-objects.json');pc=read(root/'baseline-context/person-core-exact-support.json')
heads={}
for k,v in {**full,**pc}.items():
 id=v['revision']['object_id']
 if id not in heads or v['revision']['version']>heads[id]['revision']['version']:heads[id]=v
personsex={'B':{'P-0003':('male','563-4','ogift_m'),'P-0042':('male','563-2','gift_m'),'P-0043':('female','563-3','gift_kv')},'C':{'P-0010':('male','14-child','sex_m')},'D':{'P-0020':('male','D-1','gift_m'),'P-0021':('female','D-2','gift_q'),'P-0022':('female','D-4','ogift_q')},'E':{'P-0023':('male','E-5','ogift_m'),'P-0024':('male','E-6','ogift_m'),'P-0025':('female','E-7','ogift_q')},'A':{}}
sexdecision={k:(c,v) for c,ps in personsex.items() for k,v in ps.items()}
limits={
'A':'May11/name/levföddkv are readable. Year1920 and completefatherdateMarch20 are earlier C0028/contextreuse, not assured solely fromthisimage. Parentnames appear but sourcehasno marriagebetweenparents; circledänka andogift tick are retained together. No certainfatherresidence expansion, no changeofacceptedparentlinks/dates/gates.',
'B':'TargetisKarl/Charlotta/Arne at563, not allsevenphysicalrows. Polerare andexplicit ogiftm onArne, giftm/Karl andgiftkv/Charlotta; Baptist belongsCharlotta. col12nattvard, notbaptism;23/25 are marriageupplösningsyears. codes213/000/232 physicallyincolm, undecoded statistics, no assertionmotherparish. Existing900educationexpansion retained onlydocumentarily. Foster/d.s.prefix uncertain; old maternalgrandparentchain reused, no firstactualcaredate. AdjacentAstrid/Emmy/Karl have no newpersonadoption.',
'C':'BirthApril19/1886, male/äkta, parentnames/22/modern giftandEx. are readable. Inline1:[?] is not newlyverifiedbaptismMay1. Father36 crossedboundaryfigure not anewcertainfatherage; old36 andMay1claims remainpriorinterpretations with explicit reservation. (1år) is rawparenthesis without exactmarriagedate. Westerg.[?] suffix remainsreserved. No ownerconfirmedfathersuppression.',
'D':'Fourtargetrows, separatefrom precedingdräng. Sourceyear1850 andwife1863, Kyrkefalla own andchildditto, Westergården correctedfromblinderrors. Bernhard/Agnesbirthparishconflict is retained, not majorityresolved toVärsås. Giftm/q andogiftm/q giveexplicitsex. Nohealth/religionorabsence meaningfromboundarydots. Householdtitles do notprove propertyownership.',
'E':'Tenadministrativerows, sevenfamily andthreetjänster; no newservantidentities. Sourcefather58corrected fromblind30, mother67[?]/Mofalla retainedwithuncertainty; existing1858/1850 and1867/1863conflicts remain. Childrenbirthplaceown Bernhardförs. then ditto. Middle/namevariants notchangedintocanonicalfullname; sex fromm/q columns. Noage/completionorhealthfromblankfields. Noindependentvotesfor parishbookextracts1900/1910.'}

def reason(c,id,v):
 kind=v['kind'];d=v['data'];prop=d.get('property','');sub=d.get('subject_id','');crit=d.get('criteria','')
 if id in sexdecision:return 'Revise only null sex from explicit sourcecolumn; accepted identity/displayname/legacy_state retained; exact old supports individually carried forward with five explicit stale-record reviews.'
 if id=='E-baptism-P-0010' or 'baptism-P-0010' in id:return 'Retain prior May1 baptism as older interpretation, not freshly verified. New inline1:[?] uncertainty is an audit reservation; no competing exactdate or evidence ofwrongperson to justify replacingevent/participation.'
 if id=='O-P-0010-C0023-parent-ages':return 'Retain old36/22 observation historically; newfullmatrix separates struckfatherline36? from actualprintedmotherage22. Do not count old/newsameoriginal as corroboration or newlyverifyfatherage.'
 if id=='F-P-0020-source_conflict-census1900-1910-birth-years':return 'Retain explicit CONFLICT with no accepteddatechange: EphaseBre-read58 supports oldraw1858, wife67?doesnot refute old1867;1900and1910are dependent extracts.'
 if prop in ['birth_place_report','birth_report'] and c in ['D','E']:return 'Retain ownsourceparish/yearreport, not acceptedphysicalbirthplace: DdittoKyrkefalla / Eownförs. orMofalla remains sourcebound; conflictinglaterparish doesnot overrule thisrow.'
 if kind=='relation':return 'Retain recorded_parent relation and unknownrelationaldate; targeth./s./d.familyroles with existingcorrelation supportadministrativeparentreading, not biologicaltotal, newmarriageornewunresolvedidentity.'
 if prop=='family_account':return 'Retain narrator JanChrister/unknownfirstCareDate. Formal1930household cannot verify beginningofactualcare; earlierregisteredarrival1918 andmemoir stay separate.'
 if prop=='census_fields':return 'Retain older school/income normalization only asdocumented oldinterpretation; ownsourcehas school3 and9/— with no newcodekey. Supplementalrawobservation makes exactlimitsvisible.'
 if kind in ['source','record','transcription']:return 'Retain sourceidentity/postboundary/oldertext anddatedcaveats. Append separatelyversioned fullrawreading, not overwriteoriginalwitness or retroactivelyupgradelegacytranscription.'
 if kind=='person':return 'Retain existingidentity status andallfields unless separate explicitsexdecision applies. No newpersonfrom uncertainadjacentname orlocator; no ownerconfirmedknowledge revised.'
 if kind in ['event','participation']:return 'Retain existingdatedevent/explicitrole; same-image reread isnot extra historicalwitness. Newfielduncertaintydoesnot introduce competingnewnormalizeddate orchangeeventidentity.'
 if kind=='mention' or kind=='identity':return 'Retain Bernhardnamedchild/existingacceptedlink;1886/April19/parentpair coincide, no competingpersonintroduced. No arbitrarycanonicalnamecopied to rawuncertainfields.'
 if kind in ['assessment','question','narrative']:
  if id.startswith('ASSESSMENT-') or 'PK-' in id:return 'Retain exact pre-existing criterion/outcome/date andidentity/life/tree distinctions. Newboundedsourceadoption covers touchedrow only; no full-contract re-review orgateupgrade. Sourceuncertainties documented separately; otherpersonlife claimsoutside fiveposts not revalidated.'
  if 'KEY-' in id:return 'Retain existing scopedsearchkey and dependence barrier. Rawvariant/ditto is not a newindependentvote; newuncertainty listed separately without withdrawingolderkey.'
  if 'P-0022/Q-01' in id:return 'Retain openAgnesbirthparishquestion: DownKyrkefalladitto versus Eförs.;brotherbirthnotis cannot decide sistersourceconflict.'
  if 'P-0010/Q-04' in id:return 'Retain openundeodedfields. Add sourceaudit for inline1:[?]/struckfatherfigure/1år; no codecountorhealth/marriageinference.'
  if 'PATH-P-0042-KP-03' in id or 'THEME-P-0042-EKO' in id:return 'Retain open/limited economicpath; blankKarl1930income isnot zero andArne9 isnot Karlsincome; no newbouppteckning read.'
  if 'PATH-P-0042-KP-05' in id or 'THEME-P-0042-SAM' in id:return 'Retain personbounds: BaptistCharlotta doesnot assignKarlreligion; owncol12nattvardmark israw withreservation, no complete socialtheme.'
  return 'Retain statedolderunderstanding withinexactsourcebounds; new fullfields add reservations/adoption, not retrospective changeofunrelatedwholeprofile. '+limits[c]
 if kind=='fact':return 'Retain current '+prop+' for '+sub+' onexactexistingrecords; relevantownrow/name/status/household are compatible afterphaseBcorrections; no changednormalizedvalue proved. '+limits[c]
 return 'Retain; no substantive fivepostchange supported; text/provenance route isnot newevidence.'

dispositions=[]
for c,items in bycase.items():
 for id,v in items.items():
  dispositions.append(dict(case=c,object=id,current_version=v['revision']['version'],kind=v['kind'],decision='revise_sex_only' if id in sexdecision else 'retain',reason=reason(c,id,v),data_review=v['data'],exact_evidence=v['evidence'],scope_limit='Bounded five-sourcepost consequence scrutiny. Unrelated profilebiography/contract/sourcepaths are not newlyverified; no blanket evidence rebinding.'))
wr(out/'candidate-dispositions-v1.json',dispositions)
# Expose individually reviewed stale support bindings, not an automatic version-loop.
rebind_review={
'R-301274634b1d64bcd8934ad1':'C0914@2 unchanged source/locator/nameidentitycontext; adds registration-versusphysicalvenue, officialaddress andreserved8clarification. Bernhardidentitysupport remains, not a newvenuefact.',
'R-c66825545c5b93a96a19898a':'C0915@2 same Bernhard1208row/source/locator; revised military23937/06?, occupationparenthesis andblankcells unrelated toacceptedidentity. Preserve these reservations; no harmonized military/occupationconclusion.',
'R-bbe424c723e313d730a6f028':'C0034@2 sameArne/Maj1938entry16/source/locator. Updatesuncertainconsent/officiant andcolumn13mapping, notArneidentity; preserve exactuncertainties.',
'R-79718825d117bf31d16b4fe7':'C0923@2 sameArne1915-02-21 identitykey andgrave; adds exactURL/newdatedcapturehash while oldercapturedebtpersists. No independentbirth/relationalvote orphysicaldeathplace.',
'R-70eeff109bc651dce649a0ee':'C0008@2 sameArne1915birthentry/source/locator andblankfather. Corrected witnessoccupation/name priority doesnotchangechildidentity; ownerconfirmedfatherstatusnot touched.'}
wr(out/'five-support-rebind-reviews-v1.json',rebind_review)

def ev(id,version=1,role='supports',note='Same source, no extra independent historicalwitness.'):
 return dict(object=id,version=version,role=role,note=note)
def change(id,kind,data,evidence=None,**kw):
 return dict(id=id,kind=kind,expectedVersion=None,disposition='recorded',evidenceStatus='TRANSCRIBED' if kind in ['transcription','observation'] else None,rationale='T-0773 AC: own fullsourcefields, explicit reservations and bounded consequence/adoption in isolated historicalj227 trial.',caveat='TwoSolreads ofsameoriginal arequalitycontrol; noextraindependentwitness. No canonicalapply.',data=data,origins=[],evidence=evidence or [],**kw)
rows_for_people={'A':{'P-0007':'15-child','P-0015':'15-father','P-0016':'15-mother'},'B':{'P-0042':'563-2','P-0043':'563-3','P-0003':'563-4'},'C':{'P-0010':'14-child','P-0020':'14-father','P-0021':'14-mother'},'D':{'P-0020':'D-1','P-0021':'D-2','P-0010':'D-3','P-0022':'D-4'},'E':{'P-0020':'E-1','P-0021':'E-2','P-0010':'E-3','P-0022':'E-4','P-0023':'E-5','P-0024':'E-6','P-0025':'E-7'}}
ops=[]
for c in 'ABCDE':
 d=matrices[c];r_id=next(iter(bindings[c]));r_version=bindings[c][r_id]['revision']['version'];trid=f'T0773-TR-{c}';changes=[]
 changes.append(change(trid,'transcription',dict(record_id=r_id,text=json.dumps(d,ensure_ascii=False,indent=2),reading_note='Bothblindrawmatrices arefrozen; phaseBexplicit42fieldcorrections/reservations areinfield-adjudications-v1.json. '+limits[c]),[ev(r_id,r_version,'derived_from')]))
 row_ids=[]
 for r in d['rows']:
  if 'anchor' in r['row_id']:continue
  id=f"T0773-O-{c}-{r['row_id']}";row_ids.append(id)
  changes.append(change(id,'observation',dict(record_id=r_id,mention_id=None,property='full_source_row_fields',value_literal=r['row_id']+': '+limits[c],value_json=dict(row=r,image_sha256=d['image_sha256'],scope=d['scope'],boundary_notes=d['boundary_notes'],uncertainties=d['uncertainties'])),[ev(r_id,r_version,'derived_from'),ev(trid,1,'derived_from')]))
 for pid,(sex,rid,col) in personsex[c].items():
  v=heads[pid];id=f'T0773-O-{c}-{rid}';old=v['evidence'];new=[]
  for e in old:
   x=copy.deepcopy(e)
   if x['object'] in rebind_review:
    hv=heads[x['object']]['revision']['version'];assert hv==2
    x['version']=2;x['note']+= ' T0773 individual old/current review: '+rebind_review[x['object']]
   new.append(x)
  new.extend([ev(id),ev(trid)])
  cv=v['revision']['caveat']+'\nT-0773: onlysex null→'+sex+' from'+rid+'.'+col+'; former"no sexchange"clause ishistorical. Identitydisplayname/legacy_state andgates unchanged. '+limits[c]
  x=change(pid,'person',{**v['data'],'sex':sex},new)
  x.update(expectedVersion=v['revision']['version'],disposition=v['revision']['disposition'],evidenceStatus=v['revision']['evidence_status'],rationale='T-0773 AC: explicit '+col+' sourcecolumn on '+rid+' permits '+sex+'; existingidentity retained. No sexfromname/role. All oldsupports reviewed at theidentity-supportlevel, with fiveexplicitstaleversiondecisions only.',caveat=cv,origins=v['origins'])
  changes.append(x)
 for pid,rid in rows_for_people[c].items():
  changes.append(change(f'ADOPT-T0773-{c}-{pid}','assessment',dict(subject_id=pid,criteria='bounded_source_adoption/1',outcome='reviewed_with_limits',body=f'T-0773 case{c}: existing{pid} adopts ownsource row{rid}. '+limits[c]+'\nIdentity/personmatching reused from exact olderperson chain; no claim that the uncertaindiplomaticname now independentlyproves it. '+('Sex core precision accepted explicitly from '+personsex[c][pid][2]+'.' if pid in personsex[c] else 'No coresex/person revision inthiscase.')+'\nNativeTR/O storefullraw/logicalfields; firstblinderrors remain in frozenfiles. Existingidentity, treeandlife gates keep exactoutcomes/dates; this is bounded sourceleveladoption, not fullten-theme life review.'),[ev(f'T0773-O-{c}-{rid}'),ev(trid)]))
 relevant=[x for x in dispositions if x['case']==c]
 auditbody=json.dumps(dict(case=c,source_limits=limits[c],retention_decisions=relevant,first_phase_errors_preserved=True,full_legacy_person_life_audit=False),ensure_ascii=False,indent=2)
 changes.append(change(f'T0773-AUDIT-{c}','assessment',dict(subject_id=r_id,criteria='source_record_review/1',outcome='reviewed_with_reservations',body=auditbody),[ev(r_id,r_version,'derived_from'),ev(trid)]+[ev(x) for x in row_ids]))
 op=dict(id=f'T-0773/{c}-sol-candidate-v1',actor='gpt-6.1-sol',reason='T-0773 ownerbenchmarkexception AC: fiveexactsourceposts independentlyread/frozen, source/canonicaljudgement separated, boundedpersonsex/adoption and individually reasoned retention; isolated j227 only.',dependencyReviewVersion=2,changes=changes)
 wr(out/f'{c}-operation-v1.json',op);ops.append(op)
print('Initialcaseobjects', {c:len(v) for c,v in bycase.items()},'unique',len(initial),'dispositions',len(dispositions),'ops',len(ops),'changes',sum(len(op['changes']) for op in ops),'personsex',len(sexdecision))
