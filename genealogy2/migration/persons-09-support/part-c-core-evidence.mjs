// Individuell omprövning av personkärnornas evidensstatus före T0660-frysning.
// Kör efter delens generering/refinements. Ändrar endast personrevisionerna i c.
import fs from 'node:fs';
export const coreEvidence = {
 'P-0429':['TRANSCRIBED','C0563→C0561→C0552 är en framförd husförhörskedja. Ingen egen födelse-/vigselpost eller bevarad mottagarrad759 ger självständig personkorroboration; makeuppslaget räknas inte.'],
 'P-0430':['CORROBORATED','Sävars familjeböcker och positiva egna ut-/inflyttposter C0554/C0571 binds genom födelsedag och Umeå landsförsamling till egna Degerforsrader C0574. C0573 bokutdrag räknas inte som oberoende.'],
 'P-0431':['TRANSCRIBED','C0563→C0561→C0552 är uttryckligen en informationsväg. Egen födelse- och utflyttningspost samt amerikansk fortsättning är olästa; tre framförda böcker räknas inte som tre oberoende identitetsbelägg.'],
 'P-0432':['TRANSCRIBED','Egen C0552rad och namnet i C0561s kollapsade barnrad hör till samma bokkedja. Den äldre raden tillför ingen självständig utvunnen identitetsprövning; egen födelse och fortsättning saknas.'],
 'P-0433':['CORROBORATED','Sävars familjerader C0552/C0554 binds via fullnamn, frånSävar och folio963 i egen C0571inflyttningspost till Konrad med samma födelsedag i C0574. B3s födelsecell förblir tom; C0573 räknas inte oberoende.'],
 'P-0434':['TRANSCRIBED','En egen rad i C0552 bär Nanny. Samma rads födelse-/dödskolumner och senare omläsningar är inte flera självständiga personbelägg.'],
 'P-0435':['CORROBORATED','Egen födelse-/doppost C0562 och egen senare hushållsrad C0561 med samma barn/födelsedag samt personlig hänvisning668 år1877 binder identiteten över skilda poster.'],
 'P-0436':['CORROBORATED','Egen födelse-/doppost C0562 och hushållskedjan C0685/C0563/C0561 binds genom samma dag, föräldrar, syskon och bokhänvisningar trots de skilda rånamnen Christina/Sophia/Cajsa.'],
 'P-0437':['CORROBORATED','Egen födelse-/doppost C0562 och senare familjerad/positiv Degerforshänvisning C0561 korroborerar Maria Elina; C0751 ger ytterligare avgränsad vuxen familj med fadern i sammanhanget.'],
 'P-0438':['TRANSCRIBED','En egen födelse-/doppost C0564 bär Sara Rebeckas existens, nöddop och dödsnot. Tvillingens egen post är inte en oberoende personpost för Sara; egen dödbok saknas.'],
 'P-0439':['CORROBORATED','Axels egen födelse-/doppost C0565 och egen död-/begravningspost C0566 binds genom namn, föräldrar och Botsmarkhushåll. Dödsålderns endagsavvikelse kvarstår utan identitetsbyte.'],
 'P-0440':['CORROBORATED','Sophia Beatas egen födelse-/doppost C0567 och senare egna hushållsrader C0685/C0563 med överföring599 binder samma dotter; uppgifterna är mer än en ensam källrad.'],
 'P-0441':['TRANSCRIBED','Endast Hildas egen rad18 i C0574 med familjeklammern är läst. Makens rader och senare jämförelser ger inga ytterligare självständiga egna personbelägg.'],
 'P-0442':['TRANSCRIBED','Endast Alvar Rudolfs egen rad19 i C0574 med familjeklammern är läst. Åldersberäkningen och familjejämförelsen bygger på samma rad.'],
 'P-0443':['TRANSCRIBED','Endast Anders Gideon Nikanors egen rad20 i C0574 med familjeklammern är läst. Samma familjs datum och jämförelser ger ingen självständig personkorroboration.'],
 'P-0444':['TRANSCRIBED','Gustaf Sjöberg är namngiven far i dotterns C0576födelsepost. Dotterns senare vigsel/död återbrukas som familjekontext, inte som separat belägg för hans egen identitet.'],
 'P-0445':['TRANSCRIBED','Stina Lotta är namngiven mor i dotterns C0576födelsepost. Samma cells åldersrättelse och dotterns senare familjeliv ger ingen separat egen personpost.'],
 'P-0446':['TRANSCRIBED','Den accepterade Karl August-identiteten bärs av C0579s egen rad. C0580s Carl August-födelsepost förblir kandidat och får inte räknas som accepterad korroboration.'],
 'P-0447':['CORROBORATED','Jöns egen hushållsrad C0590, egen vigselpost C1024 och hans namngivna fadersroll i sonens C0333födelsepost binder samma par i Hullsjön genom skilda händelseposter.'],
 'P-0448':['CORROBORATED','Cajsa Britas egen hushållsrad C0590, egen vigselpost C1024 och hennes namngivna modersroll i sonens C0333födelsepost binder samma par. Åldersavvikelsen och föräldraledets skuld hålls separata.'],
 'P-0449':['TRANSCRIBED','Endast Britas egen barnrad i C0590 identifierar henne. Föräldrarnas vigsel, broderns födelsepost och föräldrarnas nattvardsdagar är inga separata egna personbelägg.'],
 'P-0450':['TRANSCRIBED','Endast Magdalenas egen barnrad i C0590 identifierar henne. Föräldrarnas och broderns separata poster korroborerar familjen men inte hennes egen individuella identitet.']
};
const path='genealogy2/migration/persons-09-c.json',reviews=JSON.parse(fs.readFileSync(path));
if(reviews.length!==22||Object.keys(coreEvidence).length!==22)throw Error('Förväntade22 individuellt bedömda personkärnor.');
for(const p of reviews){const [status,basis]=coreEvidence[p.person]??[];if(!status)throw Error('Saknad individuell evidensbedömning:'+p.person);const cores=p.changes.filter(c=>c.id===p.person&&c.kind==='person');if(cores.length!==1)throw Error('Ej exakt en personkärna:'+p.person);cores[0].evidenceStatus=status;cores[0].rationale='Individuellt granskad evidensstatus för avgränsad personidentitet: '+basis+' Disposition och kontraktsbedömningar ändras inte.';}
fs.writeFileSync(path+'.tmp',JSON.stringify(reviews,null,2)+'\n');fs.renameSync(path+'.tmp',path);
console.log(Object.fromEntries(['TRANSCRIBED','CORROBORATED'].map(status=>[status,Object.keys(coreEvidence).filter(id=>coreEvidence[id][0]===status)])));
