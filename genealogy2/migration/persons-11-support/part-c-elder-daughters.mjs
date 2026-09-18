import {person,fact,event,assertion,save,section,own,cs,communion,reuse,childBase} from './part-c-children-common.mjs';
for(const [id,isAnna]of[['P-0520',true],['P-0521',false]]){
 const name=isAnna?'Anna Johanna':'Lisa Catharina';
 const p=person(id,'Hela akt, profil och relevanta hela C1072/0872/0869/1055/0064 lästa. Fyra egna bokrader hålls som en informationsväg; v, kunskap, årstecken, tomfält och hänvisningar knyts till rätt R. Egen födelsekonflikt består, inga orter från olästa mottagarsidor. Profilens sju syskon rättas sakligt till de åtta namngivna; äldre profiletiketter bevaras separat. '+(isAnna?'1832/1833 gäller två läsningar av samma överskrivna AI6-cell.':'Eva Catharina är avvisat avskriftsfel, inte namnvariant eller annan person; 6mars/6december och44[4/7?] kvarstår.'));
 const{os,house,limits,family,targets}=childBase(p,['AI3s262','AI4s310','AI5bs16','AI6bs474']);
 const a3=own(p,'AI3',name,'',{birth_literal:isAnna?'1833':'6/12 1834'},os,'Ingen separat råroll utvunnen. Tidigare avskrift, bild saknas och egna övriga kolumner är outvunna.');
 const common={smallpox_sign:'v',knowledge_sign:'grafiskt läs-/kunskapstecken',empty_fields:['giftoår','Hvarifrån','dödsår','anmärkningar']};
 const a4=own(p,'AI4',name,'',{birth_literal:isAnna?'5/2 1833':'6/12 1834',...common},os,'Ingen separat råroll utvunnen; moderns egna kolumner överförs inte.');
 const a5=own(p,'AI5',name,'',{birth_literal:isAnna?'5/2 1833':'6/[kompakt oavgjord månad] 1834',...common,annual_fields:'tomma'},os,'Ingen separat råroll utvunnen. '+(isAnna?'':'December eller mars kan inte avgöras i den kompakta cellen.'));
 const communionRaw=isAnna?{1848:['25/6','2/10'],1849:['4/4','24/6','tredje tal med reserverad dag'],1850:['24/6','6/10'],1851:['22/6','oktobertal med reserverad dag'],1852:['24/6','två oktobertal med reserverade dagar']}:{1851:['24/6 f.g.','andra reserverat tal'],1852:['24/6','7/11','februarital med reserverad dag'],1853:['24/6','apriltal med reserverad dag'],1854:['reserverat januarital','reserverat decembertal']};
 const a6=own(p,'AI6',name,'Dott.',{birth_literal:isAnna?'5/2 1832/1833[?]':'6/3 1834',...common,struck:true,destination_reference:isAnna?'478':'44[4/7?]',communion:communionRaw,empty_annual_fields:isAnna?'1853–1857':'1848–1850 och1855–1857',...(isAnna?{birth_year_cell_overwritten_and_struck:true}:{})},os,'Läsreservationer bevaras; strykning och destination ger inte död, exakt avgångsdag eller läst ny ort.');
 const values=isAnna?['1832-02-05','1833-02-05']:['1834-03-06','1834-12-06'];
 const birth=event(p,'birth',{precision:'alternatives',values,literal:values.join(' eller ')},os,'Senare längduppgifter; inget alternativ avgörs av en majoritet i bokkedjan och egen födelsepost oläst.',null,'CONFLICT');
 const assessment=fact(p,'birth_assessment','book-readings',isAnna?{AI3:'1833',AI4:'5/2 1833',AI5:'5/2 1833',AI6:'5/2 med överskrivet/korsat1832/1833[?]',conflict_is_two_readings_of_same_AI6_cell:true,not_two_independent_year_sources:true,chosen_year:null}:{AI3:'6/12 1834',AI4:'6/12 1834',AI5:'6 med kompakt oavgjort månadstecken1834',AI6:'6/3 1834',chosen_month:null},os,'CONFLICT');
 const absence=fact(p,'source_scope','later-parent-households',{absent_from:[{book:'AI7b',page:400,period:'1858–1860',only_earlier_transcription_image_missing:true},{book:'AI8b',page:536,period:'1861–1865'},{book:'AI9c',page:85,period:'1866–1876'}],no_own_death_inferred:true,no_destination_inferred:true,no_parishwide_absence:true},os);
 const forward=fact(p,'source_reference','unread-destination',{book:'AI6b',page:474,literal:isAnna?'478':'44[4/7?]',older_reading:isAnna?null:'444',destination_unread:true,destination_place:null,last_own_annual_year:isAnna?1852:1854,approx_departure_hypothesis:isAnna?'omkring1852/1853':'omkring1854/1855',exact_departure_unknown:true,...(isAnna?{register_Westerliden477_not_proof_of_own478_place:true}:{AI6a_route_hypothesis_only:true})},os,'TRANSCRIBED','Sista årstecken är inte i sig en exakt fysisk flyttdag.');
 const church=fact(p,'church_activity','own-annual-fields',{communion:communionRaw,empty_years:isAnna?'1853–1857':'1848–1850 och1855–1857',no_calendar_fill:true,no_continuous_presence:true,...(!isAnna?{fg_literal:'f.g.',fg_interpretation:'första gången',interpretation_not_confirmation_event:true}:{})},os);
 const dates=isAnna?['1848-06-25','1848-10-02','1849-04-04','1849-06-24','1850-06-24','1850-10-06','1851-06-22','1852-06-24']:['1851-06-24','1852-06-24','1852-11-07','1853-06-24'];
 const es=communion(p,dates,os,'Övriga egna dagtal förblir reserverade; ingen konfirmationshändelse skapas.');
 const count=fact(p,'source_assessment','sibling-count',{old_prose:'sju syskon',actual_named_siblings:8,nine_children_in_known_family:true,no_lifetime_total:true},os);
 let correction=[];
 if(!isAnna){const f=fact(p,'name_form','Eva-rejected',{accepted:'Lisa Catharina',rejected:'Eva Catharina',rejected_form_is_transcription_error_not_source_variant:true,AI5_own_image_read_Lisa:true,AI3_AI4_AI6_also_Lisa:true,possible_confusion_with_sister_Eva_Lovisa_is_hypothesis_only:true,old_filename_kept_as_archive_path:true},['A-6660',cs('C-0872'),cs('C-0869')]);correction=[f];assertion(p,'A-6660',[...a5,f],'Lisa i egenAI5rad; Eva avvisas som avskriftsfel och kvarvarande filnamn historiseras.');}
 const base=isAnna?3280:3282;
 assertion(p,'A-'+base,[...birth,assessment,...a3,...a4,...a5,...a6,...correction],'Födelseuppgiften och dess exakta konfliktgrund bevaras utan vald dag/årskombination.');
 assertion(p,'A-'+(base+1),[...targets['P-0082'],...targets['P-0519'],house,family],'Föräldrar från samma bokkedja, ingen oberoende egen födelsenotis.');
 if(isAnna)assertion(p,'A-6650',[...a4,...a5,...a6,assessment],'Dag/månad5/2 återges medan året förblir konflikt.');
 else assertion(p,'A-6661',[...a3,...a4,...a5,...a6,...birth,assessment],'6och1834 stabila; december/mars och AI5olösttecken förblir olika källäsningar.');
 const start=isAnna?6651:6662;
 assertion(p,'A-'+start,[...a4,...a5,...a6,limits],'Eget v i tre rader, ingen exakt vaccination eller diagnos.');
 assertion(p,'A-'+(start+1),[...a6,forward],'Egen överstruken rad och reserverad destinationshänvisning utan ort/död.');
 assertion(p,'A-'+(start+2),[...a6,church,...es],'Hela årsföljden, råreservationer och tomma egna år hålls skilda från närvaroinferens.');
 assertion(p,'A-'+(start+3),[absence,forward],'Tre exakt avgränsade senare hushållsfrånvaron, inga vidare personslutsatser.');
 assertion(p,'A-'+(start+4),[...a4,...a5,...a6,limits],'Alla namngivna egna tomfält som källgräns, inte negativ personhistoria.');
 p.pending.push({origin:section(p,'Biografisk sammanfattning'),question:'Akten och profilen räknar sju syskon trots åtta namngivna relationsrader utöver personen. Nio kända barn ger åtta kända syskon; ingen livstidstotal påstås.'});
 save(p);
}
