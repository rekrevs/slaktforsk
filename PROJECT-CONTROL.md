# Project control log

- Protocol: `project-control/v0.1`

Aktuell rättelse 2026-09-05: se PCR-2026-09-05-001 och PCD-2026-09-05-001
längst ned. Tidigare måluppfyllelse/stopp efter T-0046 är inte styrkt.

## PCR-2026-08-19-001

- Record type: review
- Date: 2026-08-19
- Mode: direction-review
- Trigger: Ägaren bad om ett långsiktigt mål och en lämplig Wotan-plan för fortsatt släktforskning.
- Control judgement: continue, operate, preserve
- Current gate: Djup 2 är ännu inte helt källstängt och tidigare fynd behöver granskas mot den utvidgade regeln om opportunistisk personinsamling.
- Recommendation: Bedriv forskningen som ändliga generationsvågor från probanden, med en granskningspunkt mellan varje våg och egna personakter för alla namngivna personer i relevanta poster och hushåll.
- Owner decision required: Godkänn det öppna forskningsmålet och generationsvågorna som styrmodell.
- Evidence:
  - `genealogy/research-plan.md`
  - `genealogy/tree.md`
  - `wotan/backlog.json`
  - `wotan/dev-log/T-0002.md`
  - `wotan/dev-log/T-0003.md`
- Revisit when:
  - Djup 3 har granskats
  - En central föräldrarelation falsifieras
  - Samtliga öppna anlinjer når dokumenterade källslut

## PCD-2026-08-19-001

- Record type: decision
- Date: 2026-08-19
- Decides review: `PCR-2026-08-19-001`
- Owner: Sverker Adam Janson
- Decision: Kartlägg släktträdet bakåt så långt data finns och bevara opportunistiskt alla personer som nämns i relevanta målposter, hushåll och relationssammanhang med full provenans och relevanta källbilder.
- Disposition: approved
- Resulting Wotan tasks: `T-0005`, `T-0006`, `T-0007`, `T-0008`, `T-0009`
- Portfolio signal: Projektet är aktivt och ska fortsätta genom den befintliga Wotan-kön.
- Revisit when:
  - Djup 3 har granskats
  - En central föräldrarelation falsifieras
  - Samtliga öppna anlinjer når dokumenterade källslut

## PCR-2026-08-20-001

- Record type: review
- Date: 2026-08-20
- Mode: direction-review
- Trigger: Ägaren bad om en north star som omfattar både den egna och hustruns släkt samt ett lämpligt kontinuerligt arbetssätt.
- Control judgement: continue, redirect, preserve
- Current gate: Den befintliga forskningen omfattar bara en proband och dess automatiska anspetsrevision behöver först återfå tillförlitlighet efter ett upptäckt parserfel.
- Recommendation: Styr projektet mot ett balanserat, källstyrt arkiv för båda makarnas släkter, med breddförst forskning, systematisk prövning av relevanta nätkällor och exakt dokumenterade återaktiveringsvillkor.
- Owner decision required: Godkänn north star och avgör om ytterligare belägg för Bernhard–Arne-relationen ska vara ett forskningskrav.
- Evidence:
  - `genealogy/research-plan.md`
  - `genealogy/frontier.md`
  - `scripts/ancestor-audit.mjs`
  - `wotan/backlog.json`
  - Ägarens uppgift att north star ska omfatta både den egna och hustruns släkt
- Revisit when:
  - Den nuvarande generationsvågen genom djup 5 har granskats
  - Hustrun ska etableras som projektets andra proband
  - Nya källor eller åtkomstvägar väsentligt flyttar forskningsfronten

## PCD-2026-08-20-001

- Record type: decision
- Date: 2026-08-20
- Decides review: `PCR-2026-08-20-001`
- Owner: Sverker Adam Janson
- Decision: Godkänn `NORTH-STAR.md` som projektets långsiktiga riktning för både den egna och hustruns släkt. Bernhard Natanael Eliassons faderskap till Arne Godvig Jansson är fastställd projektinformation och kräver inga ytterligare belägg.
- Disposition: approved
- Supersedes decision: `PCD-2026-08-19-001` i fråga om projektets omfattning och kravet på ytterligare belägg för Bernhard–Arne; dess provenans- och insamlingsprinciper består.
- Resulting Wotan tasks: none; `T-0010` parkeras som `IDEA` och tas ur den aktiva kön
- Portfolio signal: Projektet är aktivt och ska fortsätta mot den verifierade forskningsfronten för två probander.
- Revisit when:
  - Den nuvarande generationsvågen genom djup 5 har granskats
  - Hustrun ska etableras som projektets andra proband
  - Nya källor eller åtkomstvägar väsentligt flyttar forskningsfronten

## PCR-2026-08-21-001

- Record type: review
- Date: 2026-08-21
- Mode: checkpoint
- Trigger: Djup 5 är avslutat och ägaren begärde ett kontinuerligt mål som både driver antavlorna bakåt genom den centrala källryggraden och systematiskt använder kompletterande källfamiljer för personberikning och ny personupptäckt.
- Control judgement: continue, redirect, operate, preserve
- Current gate: De befintliga slutstatusarna speglar främst kyrkoboksstopp; autentiserad Riksarkivet-åtkomst och person-för-person-täckning över kompletterande källfamiljer är inte systematiskt verifierade. Hustruns proband saknar ännu minsta identifieringsunderlag.
- Recommendation: Arbeta i en ändlig sekvens: verifiera autentiserad åtkomst och bygg en källtäckningsmatris; kör därefter en kompletterande återöppnings- och berikningsvåg på närmare blockerade anor; slutför sedan hela djup-6-vågen genom den centrala ryggraden. Håll hustruns startvåg separat blockerad tills integritetsminimerat underlag finns och skapa nästa generationsuppgift först efter våggranskning.
- Owner decision required: Godkänn det tvåspåriga kontinuerliga forskningsprogrammet och dess första ändliga Wotan-sekvens.
- Evidence:
  - `NORTH-STAR.md`
  - `genealogy/research-plan.md`
  - `genealogy/frontier.md`
  - `wotan/dev-log/T-0008.md`
  - Ägarens instruktion 2026-08-21 om djupare central ryggrad och kompletterande källfamiljer
- Revisit when:
  - T-0011 har avgjort om tidigare åtkomststopp ändras av autentiserad session
  - T-0012 och T-0013 har avslutat den första kombinerade källbredds- och djupvågen
  - Hustruns minsta identifieringsunderlag finns
  - En ny källtyp eller leverantör väsentligt flyttar en dokumenterad front

## PCD-2026-08-21-001

- Record type: decision
- Date: 2026-08-21
- Decides review: `PCR-2026-08-21-001`
- Owner: Sverker Adam Janson
- Decision: Bedriv kontinuerlig forskning för båda makarnas släkter genom att dels gå djupare i den centrala kyrko- och befolkningsryggraden för att bygga antavlorna så långt bakåt som data medger, dels använda relevanta kompletterande källfamiljer för att berika personer och hitta nya relationspersoner. Organisera arbetet som ändliga Wotan-vågor med full provenans och synliga åtkomsthinder; sök inte ytterligare belägg för Bernhard–Arne-relationen.
- Disposition: approved
- Related records: `PCD-2026-08-20-001`, `genealogy/research-plan.md`
- Resulting Wotan tasks: `T-0011`, `T-0012`, `T-0013`, `T-0014`
- Portfolio signal: Projektet är aktivt och begär kontinuerlig forskningsuppmärksamhet genom Wotan; hustruns delspår väntar separat på minsta identifieringsunderlag.
- Revisit when:
  - T-0011 har avgjort om tidigare åtkomststopp ändras av autentiserad session
  - T-0012 och T-0013 har avslutat den första kombinerade källbredds- och djupvågen
  - Hustruns minsta identifieringsunderlag finns
  - Samtliga öppna linjer har nått dokumenterade källslut över relevanta källfamiljer och leverantörer

## PCR-2026-08-21-002

- Record type: review
- Date: 2026-08-21
- Mode: checkpoint
- Trigger: Ägaren identifierade sin hustru Kristina Elisabeth Petronella Höök, gift Janson, och angav hennes föräldrar Evy Höök, född 1938 i Sundsvall, och Gunnar Höök, född 1934 i Lidingö, med exakta datum som forskningsidentifierare.
- Control judgement: continue, operate, preserve
- Current gate: Hustruns identifieringsblockerare är löst. Den kvarvarande begränsningen är att sannolikt levande personer ska dataminimeras och att laglig nätåtkomst för 1930-talets personmaterial kan vara begränsad.
- Recommendation: Flytta T-0014 till `READY`, avgränsa den till att etablera Kristina som andra proband, källpröva Evy och Gunnar genom djup 1 och endast registrera den resulterande djup-2-fronten. Låt T-0012 vänta på denna första balanserande hustruvåg samt T-0011.
- Owner decision required: none; ägaren har lämnat det underlag som den redan godkända riktningen krävde.
- Evidence:
  - Ägarens familjeuppgift 2026-08-21
  - `NORTH-STAR.md`
  - `genealogy/research-plan.md`
  - `wotan/dev-log/T-0014.md`
- Revisit when:
  - T-0014 har avslutat djup 1 eller stöter på en konkret integritets- eller åtkomstgräns
  - T-0011 har fastställt den gemensamma källtäckningsmatrisen

## PCR-2026-08-21-003

- Record type: review
- Date: 2026-08-21
- Mode: checkpoint
- Trigger: T-0014 har etablerat hustruns proband och djup-1-front men nått en konkret identifierings- och autentiseringsgräns; dess beroende blockerar nu hela den återstående Wotan-kön trots att Sverkers autentiserat återöppnade front är körbar.
- Control judgement: continue, operate, wait, preserve
- Current gate: Evys och Gunnars föräldrar kan inte identifieras säkert utan fullständiga födelsenamn/hemförsamlingar eller autentiserad Ancestry-, ArkivDigital- eller FamilySearch-sökning. Denna externa gate gäller hustrugrenen, inte Sverkers tio återöppnade djup-4/5-frontpersoner.
- Recommendation: Låt T-0014 förbli `BLOCKED` med de dokumenterade återaktiveringsvägarna, men ta bort det som körberoende för T-0012. Fortsätt den redan godkända kompletterande återöppnings- och berikningsvågen på Sverkers sida; återgå omedelbart till hustrugrenen när någon av gatevillkoren uppfylls.
- Owner decision required: none; detta tillämpar den godkända kontinuerliga riktningen i `PCD-2026-08-21-001` efter den uttryckliga checkpoint som `PCR-2026-08-21-002` föreskrev vid en konkret åtkomstgräns.
- Evidence:
  - `NORTH-STAR.md`
  - `genealogy/frontier.md`
  - `genealogy/source-coverage.md`
  - `genealogy/research-log/2026-08-21.md`
  - `wotan/dev-log/T-0011.md`
  - `wotan/dev-log/T-0014.md`
- Proposed actions:
  - Flytta T-0012 från `BLOCKED` till `READY` med T-0011 som uppfyllt beroende.
  - Behåll T-0014 oförändrat blockerad och synlig; skapa inte en falsk djup-2-front.
  - Fortsätt T-0012 breddförst över dess fastställda prioriteringskohort.
- Revisit when:
  - Ägaren bekräftar fullständiga födelsenamn eller hemförsamlingar för Evy eller Gunnar
  - En Ancestry-, ArkivDigital- eller FamilySearch-session autentiseras
  - T-0012 når sin verifierade våggranskning

## PCR-2026-08-22-001

- Record type: review
- Date: 2026-08-22
- Mode: direction-review
- Trigger: Ägaren vill ge sönerna Adam Jan Gunnar och Axel Ivar Malte en
  första, presenterbar och källstyrd släktutgåva med samma djup i alla grenar
  och så rika persondetaljer som lagligen åtkomliga Riksarkivskällor medger.
- Control judgement: continue, redirect, operate, preserve
- Current gate: Räknat från sönerna är alla anor kända genom djup 3 och 14 av
  16 på djup 4. De två öppna platserna är Ivar Hööks föräldrar; en osäker
  familjeledtråd säger att han kan ha varit född utom äktenskapet. Den
  biografiska täckningen är rik men ojämn, och levande personer kräver fortsatt
  dataminimering.
- Recommendation: Gör en gemensam privat syskonantavla till djup 4 som första
  ändliga utgåva. Acceptera ett exakt dokumenterat okänt föräldraled som ett
  korrekt källslut, men inte en konstruerad person. Ge varje avliden person i
  kohorten en källstödd kärnbiografi, bevara bilder och konflikter och leverera
  resultatet som en formgiven, visuellt verifierad PDF. Fortsätt därefter det
  långsiktiga forskningsprogrammet mot djup 5 och vidare.
- Owner decision required: Godkänn djup 4 som första utgåva och PDF som
  presentationsformat.
- Evidence:
  - Ägarens familjeuppgift 2026-08-22 om Sverker, Kristina, Adam och Axel
  - `NORTH-STAR.md`
  - `genealogy/tree.md`
  - `genealogy/frontier.md`
  - `genealogy/people/P-0239-ivar-hook.md`
  - `node scripts/ancestor-audit.mjs --through-depth=3`
  - `PROBAND=P-0210 node scripts/ancestor-audit.mjs --through-depth=3`
  - `wotan/dev-log/T-0014.md`
- Uncertainty: Ivars födelsenotis kan identifiera två föräldrar, endast modern
  eller ett annat föräldraläge. Utgåvan ska återge originalets faktiska
  evidensläge.
- Revisit when:
  - Den första PDF-utgåvan har visuellt och genealogiskt verifierats
  - Ivars födelse- eller föräldrakälla väsentligt ändrar djup-4-strukturen
  - Ägaren vill öppna den balanserade djup-5-vågen

## PCD-2026-08-22-001

- Record type: decision
- Date: 2026-08-22
- Decides review: `PCR-2026-08-22-001`
- Owner: Sverker Adam Janson
- Decision: Godkänn den föreslagna gemensamma första släktutgåvan för Adam
  Jan Gunnar och Axel Ivar Malte till jämnt djup 4, med dokumenterade
  källslut där en förälder inte kan identifieras. Formge utgåvan snyggt och
  leverera den som PDF med källstödda personporträtt och full provenans bakom
  innehållet.
- Disposition: approved
- Related records: `PCD-2026-08-21-001`, `genealogy/research-plan.md`
- Resulting Wotan tasks: `T-0015`, `T-0016`
- Portfolio signal: Projektet är aktivt; den första balanserade familjeutgåvan
  får företräde framför den bredare pågående återhämtningsvågen, som bevaras
  och återupptas efter utgåvan.
- Revisit when:
  - `T-0016` har levererat en visuellt verifierad PDF
  - Ivars födelsenotis kräver en strukturell omprövning av djup 4
  - Nästa jämna generationsvåg ska väljas

## PCR-2026-08-23-001

- Record type: review
- Date: 2026-08-23
- Mode: direction-review
- Trigger: Den första PDF-utgåvan är levererad. Ägaren har dels lagt fram en
  uttrycklig familjekälla från Ivars dotter Margareta som namnger Johannes
  Ivar Fredberg som farfar, dels begärt att fortsatt forskning prioriterar en
  jämn nästa utgåva en generation djupare med rika fler-källporträtt före
  djupdykning i enskilda grenar.
- Control judgement: continue, redirect, operate, preserve, wait
- Current gate: Nästa jämna utgåvedjup från Adam och Axel har 32 teoretiska
  positioner. Sexton personer är kända på Sverkers sida och tolv på Kristinas;
  fyra föräldrapositioner bakom Erik Jonas Henriksson och Johannes Ivar
  Fredberg är öppna. Källtäckningen är ojämn mellan de 28 kända personerna,
  och den påbörjade Motala-vägen för P-0123 ligger redan en generation djupare
  än nästa utgåvekohort.
- Recommendation: Rikta om T-0012 till den gemensamma djup-5-utgåvekohorten
  räknad från sönerna. Arbeta breddförst över de 28 kända personerna och de
  fyra öppna positionerna; använd den centrala källryggraden och alla sakligt
  relevanta Riksarkivskällor för både relationer och rika livsbilder. Pausa
  P-0123 och övriga djupare spetsar. När forskningsunderlaget är moget ska
  projektet stanna före ny PDF och hålla en ägardiskussion om innehåll,
  berättarstruktur, urval och visuell form. Skapa ingen PDF-uppgift före detta
  beslut.
- Owner decision required: Godkänn omstyrningen, Fredberg som
  familjedokumenterad far och den obligatoriska redaktionella grinden före
  nästa PDF.
- Evidence:
  - Ägarens instruktion och Margaretas ordagranna familjeuppgift 2026-08-23
  - `NORTH-STAR.md`
  - `genealogy/research-plan.md`
  - `genealogy/tree.md`
  - `genealogy/frontier.md`
  - `wotan/dev-log/T-0012.md`
  - `wotan/dev-log/T-0016.md`
  - `PROBAND=P-0004 node scripts/ancestor-audit.mjs --through-depth=4`
  - `PROBAND=P-0210 node scripts/ancestor-audit.mjs --through-depth=4`
- Uncertainty: De fyra öppna positionerna kan förbli exakt dokumenterade
  källslut även efter en full Riksarkivet-passage. Rik biografi betyder
  relevansstyrd källbredd, inte samma mekaniska källantal för varje person.
- Revisit when:
  - T-0012 har granskat hela nästa utgåvekohort och producerat en
    forskningsberedskapsöversikt
  - En av de fyra öppna positionerna löses och förändrar kohortens struktur
  - Omedelbart innan disposition, manifest eller rendering för nästa PDF

## PCD-2026-08-23-001

- Record type: decision
- Date: 2026-08-23
- Decides review: `PCR-2026-08-23-001`
- Owner: Sverker Adam Janson
- Decision: Prioritera nästa gemensamma familjeutgåva ett jämnt steg djupare
  genom breddförst forskning över hela dess personkohort. Använd relevanta
  Riksarkivskällor fullt ut för rika personbilder, inklusive folkräkningar,
  husförhörs-/församlingsböcker, flyttning och övriga centrala och
  kompletterande källor. Johannes Ivar Fredberg ska inte längre redovisas som
  okänd far utan som familjedokumenterad far enligt dottern Margaretas
  uppgift. Före nästa PDF ska arbetet stanna för en rejäl gemensam diskussion
  om vad utgåvan ska innehålla, hur den ska utformas och vilket kvalitativt
  steg den ska ta från version 1.
- Disposition: approved
- Supersedes decision: `PCD-2026-08-22-001` endast i fråga om klassificeringen
  av Ivars far och processen för den efterföljande utgåvan; den levererade
  version 1 består som historisk artefakt.
- Related records: `PCD-2026-08-21-001`, `wotan/dev-log/T-0012.md`,
  `genealogy/citations/C-0320-margareta-hook-om-farfar-johannes-fredberg.md`
- Resulting Wotan tasks: `T-0012` omriktas; `T-0013` förblir blockerad; ingen
  ny PDF-uppgift skapas före ägargrinden
- Portfolio signal: Projektet är aktivt och begär fortsatt
  forskningsuppmärksamhet, men inte formgivnings- eller renderingsarbete ännu.
- Revisit when:
  - T-0012 har granskat de 28 kända personerna och de fyra öppna positionerna
  - Forskningsberedskapen för nästa jämna utgåva kan diskuteras konkret
  - Omedelbart innan någon ny PDF-uppgift skapas

## PCD-2026-08-29-001

- Record type: decision
- Date: 2026-08-29
- Decides review: ingen formell PCR; ägarsvar på T-0012:s granskning av
  identitetsbryggor (forskningsloggen 2026-08-29)
- Owner: Sverker Adam Janson
- Decision: Johannes Ivar Fredbergs (P-0287) faderskap till Anders Ivar Höök
  (P-0239) är fastställd projektinformation enligt ägarens säkra
  familjekunskap (`#1 är 100% säker.`) och kräver inga ytterligare belägg.
  Fredbergsgrenen behöver inte frysas.
- Disposition: approved
- Supersedes decision: none; kompletterar `PCD-2026-08-20-001` med en andra
  ägarfastställd relation
- Resulting Wotan tasks: none; T-0012 fortsätter. Övriga bryggor (2–9) i
  granskningen väntar på ägarbeslut eller oberoende belägg; brygga 6 är
  kedjebelagd i batch 81.
- Portfolio signal: Projektet är aktivt.
- Revisit when:
  - En samtida faderskapshandling eller DNA-stöd påträffas (bokförs, ändrar
    inte beslutet)

## PCR-2026-09-03-001

- Record type: review
- Date: 2026-09-03
- Mode: direction-review
- Trigger: Ägaren bad att det kontinuerliga forskningsmålet skulle göras
  deklarativt och uttryckas genom största möjliga generationsdjup,
  breddförst balans och en seriös strävan efter all biografiskt relevant
  information per person. Den nya Riksarkivet-MCP:n behöver samtidigt bli en
  beständig del av projektets åtkomstordning inför en ren session.
- Control judgement: continue, redirect, preserve, wait
- Current gate: Den tidigare north star-texten har rätt skyddsräcken men gör
  inte generationsmåttet, den individuella arkivfronten eller innebörden av
  personmässig fullständighet tillräckligt tydliga. MCP-servern är globalt
  aktiverad och dess verktyg är synliga, men den nämns inte i projektets
  beständiga instruktioner.
- Recommendation: Ersätt north stars inledande mål med ett deklarativt mål för
  Adam och Axel, utan fast slutgeneration, där gemensamt djup och varje grens
  arkivfront redovisas separat. Behåll projektets tidigare evidens-,
  integritets-, sidogrens- och utgåvegrindar. Använd Riksarkivets MCP först där
  den har ett passande verktyg, men behandla den som åtkomstväg och bevara
  Riksarkivets egna källidentifierare och original enligt befintlig metod.
- Owner decision required: Godkänn den vässade målformuleringen och
  MCP-först-regeln inför nästa rena session.
- Evidence:
  - Ägarens instruktion och godkännande 2026-09-03
  - `NORTH-STAR.md`
  - `README.md`
  - `HANDOVER.md`
  - `genealogy/method-riksarkivet.md`
  - `PCD-2026-08-23-001`
  - `codex mcp get riksarkivet`
- Revisit when:
  - En full generationskohort når sin våggranskning
  - MCP-serverns täckning eller åtkomstläge förändras väsentligt
  - Projektets godkända åtkomstformer ska utvidgas bortom nätmaterial

## PCD-2026-09-03-001

- Record type: decision
- Date: 2026-09-03
- Decides review: `PCR-2026-09-03-001`
- Owner: Sverker Adam Janson
- Decision: Godkänn det deklarativa målet att föra Adam och Axels samtliga
  direkta anlinjer breddförst och balanserat till varje grens dokumenterade
  arkivfront, utan ett fast maximalt generationsantal, och att göra en seriös,
  relevansstyrd ansträngning efter en rik och källförankrad livsbild för varje
  person. Behåll de tidigare kvalitets- och integritetskraven. Använd
  Riksarkivets MCP först där dess verktyg täcker behovet och de befintliga
  API-/JSON-LD-/IIIF- och Chrome-vägarna som dokumenterade kompletteringar och
  reserver.
- Disposition: approved
- Supersedes decision: `PCD-2026-08-20-001` och `PCD-2026-08-21-001` endast i
  formuleringen av det övergripande målet och Riksarkivets åtkomstordning;
  deras provenansprinciper, ägarfastställda relationer och ändliga Wotan-vågor
  består.
- Related records: `PCD-2026-08-23-001`, `PCD-2026-08-29-001`,
  `NORTH-STAR.md`, `genealogy/method-riksarkivet.md`
- Resulting Wotan tasks: none; den pågående forskningen förblir pausad tills
  ägaren uttryckligen startar ett nytt kontinuerligt mål
- Portfolio signal: Projektet är förberett för en ren kontinuerlig session men
  begär ingen forskningsaktivitet före ägarens uttryckliga start.
- Revisit when:
  - En full generationskohort når sin våggranskning
  - MCP-serverns täckning eller åtkomstläge förändras väsentligt
  - Projektets godkända åtkomstformer ska utvidgas bortom nätmaterial

## PCR-2026-09-03-002

- Record type: review
- Date: 2026-09-03
- Mode: direction-review
- Trigger: Ägaren vill göra det kontinuerliga målet till ett deklarativt
  kvalitetskontrakt och motverka att flera arbetspass ackumulerar
  okonsoliderad information, sammanblandade identiteter eller vidare anor
  ovanpå en osäker person eller föräldrarelation.
- Control judgement: continue, redirect, preserve, evaluate
- Current gate: Projektet har stark provenans, beständiga observationer och
  evidensstatusar men saknar ett uttryckligt kontrakt mellan append-only
  evidens och reviderbar kanonisk kunskap. Personernas konsolidering är inte en
  fullständig färdiggrind. Reporoten saknar dessutom `AGENTS.md`, så Codex får
  projektets styrning endast indirekt via README och handover. Den gemensamma
  anparsern kan föra in en tabellrelation märkt `LEAD` eller `CONFLICT` om
  osäkerheten inte också står i relationsordet.
- Recommendation: Lägg de beständiga kvalitetsinvarianterna i north star,
  kunskapslagren och reglerna för rättelse/sammanföring/delning i
  `genealogy/README.md`, den upprepningsbara identitets- och
  konsolideringspassagen i forskningsprogrammet och aktuellt arbete i T-0012.
  Skapa en kort lokal `AGENTS.md` som routar Codex till dessa kanoniska filer.
  Filtrera uttryckligt osäkra relationsstatusar ur härledd antavla och täck
  beteendet med regressionstest.
- Owner decision required: Godkänn kvalitetskontraktet, dokumentfördelningen
  och att T-0012:s kohort måste identitets- och konsolideringsgranskas innan
  uppgiften eller nästa djup kan stängas.
- Evidence:
  - Ägarens analys, förtydligande och uttryckliga instruktion att implementera
    2026-09-03
  - `NORTH-STAR.md`
  - `genealogy/README.md`
  - `genealogy/research-plan.md`
  - `scripts/lib/genealogy-relations.mjs`
  - `wotan/backlog.json`
  - global `~/.codex/AGENTS.md` och avsaknaden av lokal `AGENTS.md`
- Revisit when:
  - T-0012:s utgåvekohort har genomgått första fulla konsolideringsgranskningen
  - En personakt behöver delas eller två kandidatakter sammanföras
  - Maskinella identitets- eller ledgerkontroller kan införas utan falsk
    säkerhet eller förlust av historik

## PCD-2026-09-03-002

- Record type: decision
- Date: 2026-09-03
- Decides review: `PCR-2026-09-03-002`
- Owner: Sverker Adam Janson
- Decision: Godkänn north star som projektets permanenta deklarativa
  kvalitetskontrakt: evidenshistoriken är append-only, den konsoliderade
  personmodellen är reviderbar, varje personakt ska avse en verklig person och
  materiellt osäkra identiteter eller föräldrarelationer får inte propageras
  som etablerade anled. Ackumulerade observationer räknas inte som framsteg
  förrän de har identitetsprövats, konsoliderats och evidensbedömts. Fördela
  implementeringen mellan north star, kunskapsmodell, forskningsprogram,
  maskinella spärrar och Wotan, med en lokal `AGENTS.md` som automatisk
  upptäcktsväg.
- Disposition: approved
- Supersedes decision: none; skärper kvalitetsinnebörden i
  `PCD-2026-09-03-001` och lämnar tidigare ägarfastställda familjefakta i
  Project Control i stället för i north star
- Related records: `PCD-2026-08-20-001`, `PCD-2026-08-29-001`,
  `PCD-2026-09-03-001`, `NORTH-STAR.md`, `AGENTS.md`,
  `genealogy/README.md`, `genealogy/research-plan.md`
- Resulting Wotan tasks: T-0012 är omformulerad så att kohorten ska
  konsolideras och identitetsgranskas före avslut; inget parallellt task
  skapas och T-0013 förblir blockerad
- Portfolio signal: Projektet är aktivt inom T-0012 men nästa arbetssteg är
  kvalitetsgranskning av den aktuella kohorten, inte ytterligare okontrollerad
  ackumulation eller ett nytt djup. Den första konkreta grinden är P-0006:s
  uttryckligt `LEAD`-märkta relationer till P-0001 och P-0002; den djupare
  bevarade grenen är inte verifierat ansluten förrän bryggan konsoliderats eller
  ägaren fattat ett uttryckligt beslut.
- Revisit when:
  - T-0012:s utgåvekohort har genomgått första fulla konsolideringsgranskningen
  - En bärande identitet eller relation försvagas
  - En ny utgåva eller nästa generationsvåg ska öppnas

## PCD-2026-09-03-003

- Record type: decision
- Date: 2026-09-03
- Decides review: direkt ägarrättelse under implementeringen av
  `PCD-2026-09-03-002`; ingen separat PCR
- Owner: Sverker Adam Janson
- Decision: Hillevi Zingmark (P-0006) är med 100 procents säkerhet dotter till
  Oskar Alfred Zingmark (P-0001) och Ebba Alfrida Andersson (P-0002).
  Relationerna ska tas som sanna projektfakta och märkas `OWNER_CONFIRMED`;
  de kräver inte ytterligare arkivbelägg. När ägaren uttryckligen anger att en
  familjeuppgift är säker ska Codex på motsvarande sätt godta den som sann
  projektinformation och bevara beslutet spårbart, inte nedgradera det därför
  att en originalhandling saknas.
- Disposition: approved
- Supersedes decision: `PCD-2026-09-03-002` endast i dess tillfälliga
  klassificering av P-0006:s föräldrabrygga som blockerande; det generella
  kvalitetskontraktet och spärren mot verkligt osäkra relationer består
- Related records: `PCD-2026-09-03-002`, `P-0006`, `A-0027`, `C-0001`
- Resulting Wotan tasks: ingen ny uppgift; T-0012 fortsätter med alla 32
  kohortpositioner verifierat anslutna och med normal konsolideringsgranskning
  före mer källinsamling
- Portfolio signal: P-0006 är inte en kvalitetsblockerare. Den fulla
  P-0004-baslinjen och dashboardens härledda relationer ska återställas, medan
  `LEAD`, `CONFLICT`, `REJECTED` och `UNKNOWN` fortsatt inte får propageras.
- Revisit when:
  - Ägaren själv rättar eller återkallar familjeuppgiften
  - Senare material skapar en uttrycklig konflikt som behöver redovisas för
    ägaren; konflikten får inte tyst skriva över detta beslut

## PCD-2026-09-03-004

- Record type: decision
- Date: 2026-09-03
- Decides review: direkt ägarbekräftelse under T-0012:s
  konsolideringsgranskning; ingen separat PCR
- Owner: Sverker Adam Janson
- Decision: Alfred Torgny Zingmark (P-0039), Jan Oskar Zingmark (P-0040) och
  Frithiof Urban Zingmark (P-0041) är med 100 procents säkerhet söner till
  Oskar Alfred Zingmark (P-0001) och Ebba Alfrida Andersson (P-0002), och
  därmed bröder till Hillevi Zingmark (P-0006). Relationerna ska märkas
  `OWNER_CONFIRMED` och kräver inte ytterligare arkivbelägg. Beslutet gäller
  relationerna, inte sekundärträdets födelse- eller dödsår.
- Disposition: approved
- Supersedes decision: tidigare `LEAD`-klassificering av just dessa
  relationer i P-0001, P-0002, P-0039, P-0040 och P-0041; den bevarade
  sekundärträdsobservationen C-0001 och dess obekräftade årtal ändras inte
- Related records: `PCD-2026-09-03-003`, `S-0634`, `C-0818`, `A-3118`–`A-3120`
- Resulting Wotan tasks: ingen ny uppgift; beslutet konsolideras inom T-0012
- Portfolio signal: de tre syskonrelationerna är inte kvalitetsblockerare och
  får ingå i härledda familjerelationer; övriga uttryckliga `LEAD`-relationer
  förblir filtrerade
- Revisit when:
  - Ägaren själv rättar eller återkallar någon av familjeuppgifterna
  - Senare material skapar en uttrycklig konflikt som behöver redovisas för
    ägaren; konflikten får inte tyst skriva över detta beslut

## PCD-2026-09-03-005

- Record type: decision
- Date: 2026-09-03
- Decides review: direkt ägarbekräftelse under T-0012:s
  konsolideringsgranskning; ingen separat PCR
- Owner: Sverker Adam Janson
- Decision: Lucy Gudrun Eliaesson (P-0012), Ann-Catherine Jonasson född
  Eliaesson (P-0013) och Maj-Grete Karlsson född Eliaesson (P-0014) är
  Bernhard Natanael Eliaessons (P-0010) tre döttrar. Lucy Gudruns och
  Maj-Gretes relationer anges uttryckligen som helt säkra; Ann-Catherines
  redan bevarade relation återbekräftas tillsammans med födelsedatumet
  1938-07-19 och den nutida bostadsorten Visby. Fadersrelationerna ska märkas
  `OWNER_CONFIRMED` och kräver inte ytterligare arkivbelägg.
- Disposition: approved
- Supersedes decision: tidigare `LEAD`-rad från P-0010 till P-0012/P-0014
  och `CORROBORATED`-klassificering av de tre fadersrelationerna; källornas
  tidigare observationer och Maj-Gretes födelseårskonflikt förblir intakta
- Related records: `S-0635`, `C-0819`, `C-0027`, `C-0263`,
  `A-3121`–`A-3123`
- Resulting Wotan tasks: ingen ny uppgift; beslutet konsolideras inom T-0012
- Portfolio signal: inga av Bernhards tre dotterrelationer är blockerare;
  uppgifter om levande P-0013 hålls fortsatt integritetsminimerade
- Revisit when:
  - Ägaren själv rättar eller återkallar någon av familjeuppgifterna
  - Senare material skapar en uttrycklig konflikt som behöver redovisas för
    ägaren; konflikten får inte tyst skriva över detta beslut

## PCR-2026-09-04-001

- Record type: review
- Date: 2026-09-04
- Mode: direction-review
- Trigger: Ägaren bad om en ordentlig genomgång av projektets setup: varför i
  north star, hur i styrfilerna och vad/var i Wotan och Project Control, med
  kravet att varför ska vara deklarativt och kunna användas som mål för
  kontinuerligt arbete.
- Control judgement: continue, redirect, operate, preserve
- Current gate: North star är deklarativt men saknar ett definierat mått;
  "behandlad" finns bara som prosa och generationerna räknas från Adam och
  Axel i north star men från P-0004/P-0210 i skript, front och Project
  Control. Projektet saknar ett kompakt, härledbart läge: varje batch skrivs
  tre gånger (forskningslogg, T-0012-logg, HANDOVER), forskningsprogrammet
  bär cirka 840 rader personspecifikt läge, HANDOVER är 3 565 rader och
  T-0012 har varit `ONGOING` sedan 2026-08-21 med 231 batchar och ett av tio
  acceptanskriterier uppfyllt. Nästa steg berättas i prosa i stället för att
  härledas ur målet.
- Recommendation: Ge north star ett beräkningsbart mått per anposition
  räknad från Adam och Axel och lyft urvalsregeln till egen styrregel.
  Inför ett maskinläsbart arbetsläge i personakterna och ett skript som
  räknar ut läget mot north star och föreslår nästa skiva. Skriv varje batch
  en gång i forskningsloggen; dev-loggen bär beslut, hinder och verifiering;
  HANDOVER blir en kort lägessida som skrivs om. Flytta läget ur
  forskningsprogrammet. Stäng T-0012 vid konsolideringsgrinden och driv
  programmet som ändliga M-uppgifter skurna ur måttets utdata. Lägg
  Wotan-konventionen i en repo-lokal fil som `AGENTS.md` routar till, och
  lägg till `CLAUDE.md` som importerar `AGENTS.md`.
- Owner decision required: Godkänn måttet, dokumentfördelningen,
  loggningsregeln och omskärningen av T-0012 till ändliga uppgifter.
- Evidence:
  - `NORTH-STAR.md`, `AGENTS.md`, `README.md`, `HANDOVER.md`
  - `genealogy/README.md`, `genealogy/research-plan.md`,
    `genealogy/frontier.md`, `genealogy/source-coverage.md`
  - `wotan/backlog.json`, `wotan/dev-log/T-0012.md`
  - `PROBAND=P-0004 node scripts/ancestor-audit.mjs --through-depth=5`
  - `PROBAND=P-0210 node scripts/ancestor-audit.mjs --through-depth=4`
  - Wotan- och Project Control-skillarnas kontrakt om repo-lokala
    konventioner och läsbara uppgiftsfiler
- Revisit when:
  - Mållägesskriptet ger ett gemensamt djup och en nästa skiva utan manuell
    omtolkning
  - Den första ändliga kohortuppgiften har nått `DONE`
  - En ny session kan starta från HANDOVER utan att läsa batchhistorik

## PCD-2026-09-04-001

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-001`
- Owner: Sverker Adam Janson
- Decision: Genomför rekommendationen i sin helhet ("vi kör på detta").
  North star får ett definierat mått räknat från Adam och Axel och en egen
  styrregel för kontinuerligt arbete. Wotan används som ändlig kö: uppgifter
  skärs ur mållägets utdata, en batch loggas en gång i forskningsloggen,
  dev-loggen bär beslut, hinder och verifiering, och HANDOVER är en kort
  lägessida. Konventionen ligger repo-lokalt i `wotan/README.md` och nås via
  `AGENTS.md` och `CLAUDE.md`. T-0012 stängs vid konsolideringsgrinden och
  återstående omfång fördelas på ändliga uppgifter.
- Disposition: approved
- Supersedes decision: `PCD-2026-09-03-002` endast i fråga om att T-0012
  ska vara den enda behållaren för kohortarbetet; kvalitetskontraktet,
  utgåvegrinden i `PCD-2026-08-23-001` och alla ägarfastställda familjefakta
  består oförändrade
- Related records: `PCD-2026-09-03-001`, `PCD-2026-09-03-002`,
  `NORTH-STAR.md`, `AGENTS.md`, `wotan/README.md`
- Resulting Wotan tasks: `T-0018`, `T-0019`, `T-0020`, `T-0021`
- Portfolio signal: Projektet är aktivt. Forskningsbatchar pausas tills
  styrlagret, måttet och omskärningen är på plats; därefter fortsätter
  kohortarbetet i ändliga uppgifter.
- Revisit when:
  - `T-0021` har omskurit T-0012 och den första kohortskivan är skapad
  - Måttet visar sig sakna en dimension som north star kräver
  - Nästa utgåvegrind eller generationsvåg ska öppnas

## PCR-2026-09-04-002

- Record type: review
- Date: 2026-09-04
- Mode: checkpoint
- Trigger: Djup-5-kohorten för Adam och Axel är färdigbehandlad och den
  obligatoriska redaktionella grinden i `PCD-2026-08-23-001` har nåtts. En
  visuell och innehållslig revision visar samtidigt att version 1 är välgjord
  men numera materiellt inaktuell.
- Control judgement: continue, operate, preserve, wait
- Current gate: none för en ny djup-5-utgåva; djup-6-forskningen bör däremot
  vänta tills den nya utgåvan är levererad och verifierad.
- Recommendation: Bevara version 1 oförändrad som historisk artefakt och skapa
  en separat, formgiven djup-5-utgåva. Behåll antavla, karta, tidslinje,
  källförklaring och exakta hänvisningar; lägg till en tydlig redovisning av
  vad som ändrats sedan version 1. Ge alla 32 personer på djup 5 kompakta
  porträtt men reservera längre berättelser för ett balanserat urval från
  båda sidor. Skilj grafiskt och språkligt mellan arkivbelägg,
  `OWNER_CONFIRMED`, kvarstående konflikter och dokumenterade arkivfronter.
- Owner decision required: Godkänn den separata djup-5-utgåvan och dess
  redaktionella principer eller välj att öppna djup 6 först.
- Evidence:
  - `PCD-2026-08-23-001`
  - `NORTH-STAR.md`
  - `genealogy/source-coverage.md`
  - `wotan/dev-log/T-0028.md`
  - `wotan/dev-log/T-0029.md`
  - `node scripts/goal-state.mjs`
  - `output/pdf/adam-och-axel-janson-fyra-generationer-v1.pdf`
- Uncertainty: De 32 kompakta porträtten kräver redaktionell komprimering;
  full akttext och fullständiga källkedjor ligger fortsatt i projektarkivet.
- Revisit when:
  - Den nya PDF-utgåvan har genealogiskt och visuellt verifierats
  - En uppgift i utgåvan står i konflikt med kanonisk personmodell
  - Djup-6-vågen ska öppnas

## PCD-2026-09-04-002

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-002`
- Owner: Sverker Adam Janson
- Decision: Genomför rekommendationen. Bevara version 1 oförändrad och skapa
  en ny, separat familjeutgåva till jämnt djup 5. Project Control får fatta
  återstående redaktionella och operativa ägarbeslut inom north star,
  kvalitetskontraktet, integritetsreglerna och repositoryts uttryckliga
  handlingsgränser utan ytterligare stoppfrågor.
- Disposition: approved
- Supersedes decision: `PCD-2026-08-23-001` endast genom att den obligatoriska
  redaktionella grinden nu är passerad; beslutets forskningsinriktning,
  evidenskrav och bevarande av version 1 består.
- Related records: `PCD-2026-09-04-001`, `PCR-2026-09-04-002`,
  `genealogy/editions/adam-axel-depth4-v1.json`
- Resulting Wotan tasks: `T-0030`; `T-0013` väntar på `T-0030`
- Portfolio signal: Projektet är aktivt i en avgränsad utgåveuppgift; ingen
  parallell djup-6-forskning ska startas.
- Revisit when:
  - `T-0030` har levererat en genealogiskt och visuellt verifierad PDF
  - En materiell konflikt kräver nytt ägarbeslut
  - Publicering, arkivbeställning, commit eller push övervägs; dessa åtgärder
    omfattas inte av detta beslut

## PCR-2026-09-04-003

- Record type: review
- Date: 2026-09-04
- Mode: checkpoint
- Trigger: `T-0030` har levererat och verifierat den godkända djup-5-utgåvan;
  villkoret för att åter öppna nästa generationsvåg är uppfyllt.
- Control judgement: continue, redirect, operate, preserve
- Current gate: Den historiska `T-0013` är en L-behållare för en hel våg och
  bygger på en äldre djupmodell. Dagens `goal-state` räknar från Adam och Axel
  och visar på djup 6: 55 kända personer, nio stängda positioner, 39 ogiltiga
  arkivfronter, en granskad person och noll källbreddsklara personer.
- Recommendation: Öppna djup 6 men kör inte den äldre monolituppgiften.
  Skär om `T-0013` till en ändlig M-uppgift för den första balanserade
  frontskivan: P-0123, P-0126, P-0131 och P-0132 på Sverkers sida samt
  P-0341, P-0342, P-0343 och P-0344 på Kristinas sida. Låt uppgiften ge var
  och en verifierade föräldrar eller giltig slutstatus och endast registrera,
  inte forska vidare på, eventuella nya djup-7-personer. Skär nästa uppgift ur
  nytt `goal-state` först efter verifiering.
- Owner decision required: none; detta är ett operativt vägval inom det
  uttryckligen delegerade mandatet i `PCD-2026-09-04-002`.
- Evidence:
  - `PCD-2026-09-04-002`
  - `wotan/dev-log/T-0030.md`
  - `wotan/dev-log/T-0013.md`
  - `wotan/README.md`
  - `node scripts/goal-state.mjs`
- Revisit when:
  - Den omskurna `T-0013` är verifierad
  - En bärande relation blir materiellt osäker eller motstridig
  - Måttet eller källåtkomsten kräver ett nytt strategiskt vägval

## PCD-2026-09-04-003

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-003`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt `PCD-2026-09-04-002`
- Decision: Öppna djup-6-programmet efter den verifierade utgåvan och skär om
  `T-0013` till den rekommenderade balanserade första frontskivan om åtta
  personer. Senare skivor skapas först ur det då aktuella målläget.
- Disposition: approved
- Supersedes decision: den äldre omfattningen i `T-0013` som en enda full
  djupvåg; riktningen mot djup 6 i `PCD-2026-08-21-001` består.
- Related records: `PCD-2026-09-04-002`, `wotan/dev-log/T-0030.md`,
  `wotan/dev-log/T-0013.md`, `wotan/README.md`
- Resulting Wotan tasks: `T-0013` omskuren och `READY`
- Portfolio signal: Projektet har en verifierad utgåva och begär nu
  forskningsuppmärksamhet för en enda balanserad djup-6-skiva.
- Revisit when:
  - `T-0013` är verifierad och nästa skiva ska väljas
  - En ny ägargrind eller extern åtkomstgräns uppstår

## PCR-2026-09-04-004

- Record type: review
- Date: 2026-09-04
- Mode: checkpoint
- Trigger: Ägarens direkta utvärdering av djup-5-utgåvan visar att kort,
  färgfält och överstor luft förbrukar papper utan motsvarande läsvärde och
  att släktträden inte ger tillräcklig överblick.
- Control judgement: redirect, operate, preserve
- Current gate: Utgåvans informationsarkitektur och pappersutnyttjande, inte
  dess genealogiska innehåll eller verifierade djup.
- Recommendation: Bevara version 1 och 2 oförändrade och skapa version 3 som
  en avskalad bruksversion: vit sida, svart/grå typografi, tunna funktionella
  skiljelinjer, inga dekorativa kort eller färgade panelytor och ingen
  omotiverad luft. Behåll läsbarheten men reducera sidantalet materiellt.
  Ersätt tabelliknande anlistor med två riktiga, sammanhängande släktträd i
  liggande format, ett per föräldrasida, med synliga förbindelser mellan fem
  generationer. Behåll samtliga 32 anor, evidensskillnader, berättelser,
  karta, tidslinje, källnärbilder och exakta referenser.
- Owner decision required: none; ägaren har uttryckligen angett både problemet
  och den önskade riktningen.
- Evidence:
  - Ägarens utvärdering 2026-09-04
  - `output/pdf/adam-och-axel-janson-fem-generationer-v2.pdf`
  - `genealogy/editions/adam-axel-depth5-v2.json`
  - `wotan/dev-log/T-0030.md`
- Uncertainty: Ett betydligt lägre sidantal får inte uppnås genom så liten
  grad eller så täta träd att familjen tappar faktisk läsbarhet.
- Revisit when:
  - Version 3 har renderats och varje sida har jämförts visuellt
  - Släktträden fortfarande kräver för mycket av läsaren
  - Något verifierat innehåll inte ryms utan redaktionell förlust

## PCD-2026-09-04-004

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-004`
- Owner: Sverker Adam Janson
- Decision: Genomför den avskalade version 3 enligt rekommendationen. Ta bort
  utgåvans dekorativa "bling-bling", använd papperet effektivare utan extrem
  komprimering och gör släktträden tydligt sammanhängande. Bevara version 1
  och 2 byte för byte.
- Disposition: approved
- Supersedes decision: `PCD-2026-09-04-002` endast beträffande den aktuella
  utgåvans visuella form; dess innehållsbeslut, provenienskrav och bevarande
  av version 1 består.
- Related records: `PCR-2026-09-04-004`, `PCD-2026-09-04-002`,
  `wotan/dev-log/T-0030.md`
- Resulting Wotan tasks: `T-0031`; `T-0013` återgår till `READY` tills den
  ägarbegärda utgåvekorrigeringen är verifierad.
- Portfolio signal: Version 3 är aktiv revisionsprioritet; djup-6-forskningen
  väntar utan att dess beslutade skiva ändras.
- Revisit when:
  - `T-0031` är visuellt och strukturellt verifierad
  - En materiell innehållskonflikt upptäcks

## PCR-2026-09-04-005

- Record type: review
- Date: 2026-09-04
- Mode: checkpoint
- Trigger: Ägaren vill ha ett mellanavstamp där de två släktträden visar
  levnadsår och relevant ort under namnen, utan kryptiska positionskoder och
  statuskommentarer, samt en komplett och innehållsrik personkatalog för alla
  personer som förekommer i träden.
- Control judgement: redirect, operate, preserve
- Current gate: Version 3:s träd prioriterar endast namn och använder den
  knappa andra raden till intern positionskod och evidensstatus. Dess
  persondel omfattar bara de 32 yttersta djup-5-personerna, trots att träden
  tillsammans visar 62 personer.
- Recommendation: Bevara version 1–3 byte för byte och skapa version 4. Låt
  varje trädruta visa namn, kända födelse-/dödsår och en relevant ort; flytta
  person-ID och evidenskommentarer ur träden. Ersätt den partiella
  persondelen med en komplett katalog i trädordning över samtliga 62 personer,
  två per sida, där varje post anger person-ID, trädposition, år, ort, kända
  föräldrar, partner och barn med namn och person-ID samt en källstyrd
  sammanställning med läsbara C-referenser. Redovisa okänt som okänt och
  propagera inga `LEAD`-, `CONFLICT`-, `REJECTED`- eller `UNKNOWN`-relationer.
- Owner decision required: none; ägaren har uttryckligen angett både innehåll,
  presentationsprincip och att den längre personkatalogen får ta flera sidor.
- Evidence:
  - Ägarens utvärdering och precisering 2026-09-04
  - `output/pdf/adam-och-axel-janson-fem-generationer-v3.pdf`
  - `scripts/build-family-edition-v3.py`
  - `genealogy/editions/adam-axel-depth5-v2.json`
  - `dashboard/public/data/project.json`
- Uncertainty: Katalogen måste vara fullständig som presentationslager utan
  att försöka återge varje rad i de fullständiga personakterna; urvalet per
  person ska därför täcka identitet, livstid, geografi, familj och de mest
  relevanta kända livsuppgifterna med spårbara källor.
- Revisit when:
  - Version 4 har renderats och alla träd- och katalogsidor har granskats
  - Ägaren vill ha full akttext snarare än en redaktionellt sammanställd katalog
  - En materiell genealogisk konflikt upptäcks

## PCD-2026-09-04-005

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-005`
- Owner: Sverker Adam Janson
- Decision: Genomför version 4 enligt rekommendationen. Träden ska prioritera
  namn, kända levnadsår och relevant ort framför interna ID:n och
  statuskommentarer. Lägg till en komplett, välformaterad och källstyrd katalog
  över alla personer i träden, med person-ID samt namngivna referenser till
  föräldrar, partner och barn. Katalogen får använda det antal sidor som den
  intressanta informationen behöver.
- Disposition: approved
- Supersedes decision: `PCD-2026-09-04-004` endast beträffande version 3 som
  aktuell bruksversion; dess avskalade formprincip och kravet att äldre
  versioner bevaras består.
- Related records: `PCR-2026-09-04-005`, `PCD-2026-09-04-004`,
  `wotan/dev-log/T-0031.md`
- Resulting Wotan tasks: `T-0032`; `T-0013` återgår till `READY` tills
  mellanavstampets version 4 är verifierad.
- Portfolio signal: Version 4 är aktiv revisionsprioritet; den pågående
  djup-6-skivan väntar med sitt redan insamlade källunderlag bevarat.
- Revisit when:
  - `T-0032` är visuellt, strukturellt och genealogiskt verifierad
  - En materiell innehållskonflikt upptäcks

## PCR-2026-09-04-006

- Record type: review
- Date: 2026-09-04
- Mode: checkpoint
- Trigger: `T-0013` har verifierat den första balanserade djup-6-skivan och
  Wotan-kön är tom; enligt styrregeln ska nästa ändliga skiva väljas ur
  det nya måttläget.
- Control judgement: continue, operate, preserve
- Current gate: Djup 6 är närmaste obehandlade generation. Av 64 positioner
  är 55 kända och nio stängda, men endast åtta kända personer är
  granskade och källbreddsklara; 31 anspetsar till och med djup 6 saknar
  giltig arkivfront.
- Recommendation: Fortsätt med en andra balanserad M-skiva om fyra
  frontpersoner per sida. Behandla P-0145, P-0214, P-0289 och P-0290 på
  Sverkers sida samt P-0350, P-0351, P-0360 och P-0361 på Kristinas sida.
  Ge varje person verifierade föräldrar eller en reproducerbar giltig
  slutstatus, konsolidera akterna och stäng berörda källtäckningsceller.
  Registrera men forska inte vidare på nya djup-7-personer.
- Owner decision required: none; valet följer den godkända styrregeln och
  ligger inom Project Controls operativa mandat i `PCD-2026-09-04-002`.
- Evidence:
  - `NORTH-STAR.md`
  - `PCD-2026-09-04-003`
  - `wotan/dev-log/T-0013.md`
  - `wotan/README.md`
  - `node scripts/goal-state.mjs`
- Uncertainty: En eller flera av de åtta fronterna kan sluta i en exakt
  klassificerad arkivfront i stället för nya föräldrar; det är ett fullgott
  utfall om relevanta lagliga nätvägar har prövats och återstartvillkoret är
  konkret.
- Revisit when:
  - Den andra djup-6-skivan är verifierad
  - En bärande identitet eller relation blir materiellt osäker
  - En extern åtkomstgräns kräver ett nytt strategiskt vägval

## PCD-2026-09-04-006

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-006`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt `PCD-2026-09-04-002`
- Decision: Fortsätt djup-6-programmet med den rekommenderade andra
  balanserade skivan om åtta personer. Skapa en enda ändlig Wotan-uppgift
  och välj inte därefter följande skiva förrän måttläget har verifierats på
  nytt.
- Disposition: approved
- Supersedes decision: none; verkställer den kontinuerliga riktningen i
  `PCD-2026-09-04-003` för nästa beräknade skiva.
- Related records: `PCR-2026-09-04-006`, `wotan/dev-log/T-0013.md`,
  `wotan/README.md`
- Resulting Wotan tasks: `T-0033`
- Portfolio signal: Projektet är aktivt och begär fortsatt
  forskningsuppmärksamhet för en avgränsad balanserad djup-6-skiva.
- Revisit when:
  - `T-0033` är verifierad och nästa skiva ska väljas
  - En ny ägargrind eller extern åtkomstgräns uppstår

## PCD-2026-09-04-007

- Record type: decision
- Date: 2026-09-04
- Decides review: direkt ägarinstruktion; ingen separat PCR
- Owner: Sverker Adam Janson
- Decision: Ändra GitHub-repot `rekrevs/slaktforsk` från privat till
  publikt och publicera det aktuella verifierade arbetsläget genom en
  mellan-commit och push. Beslutet omfattar Git-historiken, Git LFS-medierna
  och den integritetsminimerade familjeinformation som redan bevaras i repot.
- Disposition: approved
- Supersedes decision: den privata synligheten i T-0017 och dess
  bakomliggande ägarbeslut; Git LFS-, proveniens- och integritetsreglerna
  består.
- Related records: `wotan/dev-log/T-0017.md`, `MEDIA-PRESERVATION.md`,
  `PCD-2026-09-04-006`
- Resulting Wotan tasks: none; åtgärden utförs direkt och T-0033 förblir
  den aktiva forskningsuppgiften.
- Portfolio signal: Projektets källarkiv och fortsatta arbete är publikt på
  GitHub och förblir aktivt.
- Revisit when:
  - En konkret integritets- eller licenskonflikt upptäcks
  - Ägaren vill återgå till privat synlighet eller publicera material genom
    en annan kanal

## PCD-2026-09-04-008

- Record type: decision
- Date: 2026-09-04
- Decides review: direkt ägarinstruktion; ingen separat PCR
- Owner: Sverker Adam Janson
- Decision: Gå vid ett senare, avgränsat tillfälle igenom samtliga personer i
  projektet som sannolikt lever och försök korroborera deras genealogiskt
  relevanta grunduppgifter person för person mot den öppet åtkomliga tjänsten
  birthday.se. Uppgifter som faktiskt kan beläggas där får bevaras och
  publiceras i projektet med tydlig källhänvisning; öppet tillgänglig status
  ersätter inte kraven på säker identitetsmatchning, dataminimering eller
  åtskillnad mellan observation och slutsats.
- Disposition: approved
- Supersedes decision: none; förtydligar den praktiska användningen av öppna
  nutida personkällor under projektets befintliga integritets- och
  proveniensregler.
- Related records: `NORTH-STAR.md`, `PCD-2026-09-04-007`,
  `genealogy/research-plan.md`
- Resulting Wotan tasks: `T-0034`, parkerad som `IDEA` tills den aktiva
  arkivkohorten eller ett senare Project Control-avstamp aktiverar den.
- Portfolio signal: birthday.se är en uttryckligen tillåten korroboreringskälla
  för sannolikt levande personer; `T-0033` förblir aktivt forskningsarbete.
- Revisit when:
  - `T-0034` aktiveras och den exakta kohorten inventeras
  - En konkret åtkomst-, matchnings-, integritets- eller licenskonflikt uppstår

## PCR-2026-09-04-007

- Record type: review
- Date: 2026-09-04
- Mode: checkpoint
- Trigger: `T-0033` har verifierat den andra balanserade djup-6-skivan och
  den exekverbara Wotan-kön är åter tom; nästa ändliga skiva ska väljas ur
  det nya måttläget.
- Control judgement: continue, operate, preserve
- Current gate: Djup 6 är fortsatt närmaste obehandlade generation. De åtta
  målen i T-0033 är granskade och källbreddsklara; ogiltiga arkivfronter till
  och med djupet har minskat från 31 till 23. Djupet har 55 kända och nio
  stängda positioner samt 16 granskade och källbreddsklara personer.
- Recommendation: Fortsätt med en tredje balanserad M-skiva om fyra
  frontpersoner per sida. Behandla P-0329, P-0330, P-0470 och P-0471 på
  Sverkers sida samt P-0362, P-0363, P-0371 och P-0372 på Kristinas sida.
  Ge varje person verifierade föräldrar eller en reproducerbar giltig
  slutstatus, konsolidera akterna och stäng berörda källtäckningsceller.
  Registrera men forska inte vidare på nya djup-7-personer.
- Owner decision required: none; valet följer north stars prioriteringsordning
  och det delegerade operativa mandatet. T-0034 bevaras som separat `IDEA`:
  ägaren bad om birthday.se-genomgången vid ett senare avgränsat tillfälle,
  medan den närmaste obehandlade an-generationen har styrföreträde.
- Evidence:
  - `NORTH-STAR.md`
  - `PCD-2026-09-04-003`
  - `wotan/dev-log/T-0033.md`
  - `genealogy/research-log/2026-09-04.md`, batch 259
  - `node scripts/goal-state.mjs`
- Uncertainty: Flera kandidater har redan senare födelseuppgifter men saknar
  parentbärande original. Utfallet kan därför bli klassificerade fronter i
  stället för nya föräldrar utan att skivans värde minskar.
- Revisit when:
  - Den tredje djup-6-skivan är verifierad
  - T-0034 ska aktiveras som avgränsad levandepersonsrevision
  - En bärande identitet eller extern åtkomstgräns kräver nytt vägval

## PCD-2026-09-04-009

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-007`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt ägarens instruktion och `PCD-2026-09-04-002`
- Decision: Fortsätt djup-6-programmet med den rekommenderade tredje
  balanserade skivan om åtta personer. Skapa en enda ändlig Wotan-uppgift och
  lämna birthday.se-revisionen som separat parkerad uppgift tills dess
  avgränsade tillfälle väljs.
- Disposition: approved
- Supersedes decision: none; verkställer den kontinuerliga riktningen i
  `PCD-2026-09-04-003` och bevarar `PCD-2026-09-04-008`.
- Related records: `PCR-2026-09-04-007`, `PCD-2026-09-04-008`,
  `wotan/dev-log/T-0033.md`, `wotan/README.md`
- Resulting Wotan tasks: `T-0035`; `T-0034` förblir `IDEA`.
- Portfolio signal: Projektet fortsätter breddförst och balanserat genom
  djup 6; modern öppenkällekorroborering är godkänd men inte ihopblandad med
  den aktiva arkivskivan.
- Revisit when:
  - `T-0035` är verifierad och nästa skiva ska väljas
  - Ägaren uttryckligen aktiverar T-0034 tidigare
  - En konkret integritets-, licens- eller åtkomstkonflikt uppstår

## PCR-2026-09-04-008

- Record type: review
- Date: 2026-09-04
- Mode: checkpoint
- Trigger: `T-0035` har verifierat den tredje balanserade djup-6-skivan och
  den exekverbara Wotan-kön är åter tom; nästa ändliga skiva ska väljas ur
  det nya måttläget.
- Control judgement: continue, operate, preserve
- Current gate: Djup 6 är fortsatt närmaste obehandlade generation. De åtta
  målen i T-0035 är granskade och källbreddsklara; ogiltiga arkivfronter till
  och med djupet har minskat från 23 till 15. Djupet har 55 kända och nio
  stängda positioner samt 24 granskade och källbreddsklara personer.
- Recommendation: Fortsätt med en fjärde balanserad M-skiva om fyra
  frontpersoner per sida. Behandla P-0102, P-0103, P-0124 och P-0125 på
  Sverkers sida samt P-0375, P-0376, P-0383 och P-0384 på Kristinas sida.
  Ge varje person verifierade föräldrar eller en reproducerbar giltig
  slutstatus, konsolidera akterna och stäng berörda källtäckningsceller.
  Registrera men forska inte vidare på nya djup-7-personer.
- Owner decision required: none; valet följer north stars närhets- och
  balansregel samt det delegerade operativa mandatet. T-0034 förblir separat
  `IDEA`: den öppna birthday.se-källan är godkänd, men uppgiften avser en
  annan kohort och ska inte blandas in i denna arkivskiva.
- Evidence:
  - `NORTH-STAR.md`
  - `PCD-2026-09-04-003`
  - `wotan/dev-log/T-0035.md`
  - `genealogy/research-log/2026-09-04.md`, batch 260
  - `node scripts/goal-state.mjs`
- Uncertainty: De utvalda akterna varierar från redan relationstunga till
  helt matrislösa. Resultatet kan därför bli en blandning av nya föräldrar
  och klassificerade arkivfronter; båda är giltiga om källvägen och
  återstartvillkoret är reproducerbara.
- Revisit when:
  - Den fjärde djup-6-skivan är verifierad
  - T-0034 ska aktiveras som avgränsad levandepersonsrevision
  - En bärande identitet eller extern åtkomstgräns kräver nytt vägval

## PCD-2026-09-04-010

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-008`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt ägarens instruktion och `PCD-2026-09-04-002`
- Decision: Fortsätt djup-6-programmet med den rekommenderade fjärde
  balanserade skivan om åtta personer. Skapa en enda ändlig Wotan-uppgift och
  lämna birthday.se-revisionen som separat parkerad uppgift tills dess
  avgränsade tillfälle väljs.
- Disposition: approved
- Supersedes decision: none; verkställer den kontinuerliga riktningen i
  `PCD-2026-09-04-003` och bevarar `PCD-2026-09-04-008`.
- Related records: `PCR-2026-09-04-008`, `PCD-2026-09-04-008`,
  `wotan/dev-log/T-0035.md`, `wotan/README.md`
- Resulting Wotan tasks: `T-0036`; `T-0034` förblir `IDEA`.
- Portfolio signal: Projektet fortsätter breddförst och balanserat genom
  djup 6; modern öppenkällekorroborering är godkänd men hålls avgränsad från
  den aktiva arkivskivan.
- Revisit when:
  - `T-0036` är verifierad och nästa skiva ska väljas
  - Ägaren uttryckligen aktiverar T-0034 tidigare
  - En konkret integritets-, licens- eller åtkomstkonflikt uppstår

## PCR-2026-09-04-009

- Record type: review
- Date: 2026-09-04
- Mode: checkpoint
- Trigger: `T-0036` har verifierat den fjärde balanserade djup-6-skivan och
  den exekverbara Wotan-kön är åter tom.
- Control judgement: continue, operate, preserve
- Current gate: Djup 6 är fortsatt närmaste obehandlade generation. De åtta
  målen i T-0036 är granskade och källbreddsklara; ogiltiga arkivfronter till
  och med djupet har minskat från 15 till 11. Djupet har 55 kända och nio
  stängda positioner samt 32 granskade och källbreddsklara personer.
- Recommendation: Fortsätt med en femte balanserad M-skiva. Behandla P-0148,
  P-0158, P-0159 och P-0215 på Sverkers sida samt P-0386, P-0387, P-0388 och
  P-0389 på Kristinas sida. Ge varje person verifierade föräldrar eller en
  reproducerbar giltig slutstatus och stäng samtliga prioritet-1-celler utan
  att forska vidare på nya djup-7-spetsar.
- Owner decision required: none; urvalet är den första återstående
  obehandlade fyrgruppen per sida i `goal-state` och följer delegerat mandat.
  T-0034 förblir separat `IDEA` enligt ägarens formulering "vid tillfälle".
- Evidence:
  - `NORTH-STAR.md`
  - `PCD-2026-09-04-003`
  - `wotan/dev-log/T-0036.md`
  - `genealogy/research-log/2026-09-04.md`, batch 261
  - `node scripts/goal-state.mjs`
- Uncertainty: Flera av akterna har äldre dokumenterade konflikter eller
  arkivluckor; ett reproducerbart terminalt utfall kan därför vara mer
  källkritiskt korrekt än en ny föräldrarelation.
- Revisit when:
  - Den femte djup-6-skivan är verifierad
  - T-0034 ska aktiveras som avgränsad levandepersonsrevision
  - En bärande identitet eller extern åtkomstgräns kräver nytt vägval

## PCD-2026-09-04-011

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-009`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt ägarens instruktion och `PCD-2026-09-04-002`
- Decision: Fortsätt djup-6-programmet med den rekommenderade femte
  balanserade skivan om åtta personer. Skapa en enda ändlig Wotan-uppgift och
  behåll birthday.se-revisionen parkerad som ett separat senare arbete.
- Disposition: approved
- Supersedes decision: none; verkställer `PCD-2026-09-04-003` och bevarar
  `PCD-2026-09-04-008`.
- Related records: `PCR-2026-09-04-009`, `PCD-2026-09-04-008`,
  `wotan/dev-log/T-0036.md`, `wotan/README.md`
- Resulting Wotan tasks: `T-0037`; `T-0034` förblir `IDEA`.
- Portfolio signal: Projektet fortsätter balanserat genom djup 6 med en ny
  avgränsad arkivskiva.
- Revisit when:
  - `T-0037` är verifierad och nästa skiva ska väljas
  - Ägaren uttryckligen aktiverar T-0034 tidigare
  - En konkret integritets-, licens- eller åtkomstkonflikt uppstår

## PCR-2026-09-04-010

- Record type: review
- Date: 2026-09-04
- Mode: checkpoint
- Trigger: `T-0037` har verifierat den femte balanserade djup-6-skivan och
  den exekverbara Wotan-kön är åter tom.
- Control judgement: continue, operate, preserve
- Current gate: Djup 6 är fortsatt närmaste obehandlade generation. Skivan
  höjde antalet granskade och källbreddsklara personer från 32 till 40 och
  minskade ogiltiga arkivfronter till och med djupet från 11 till sju.
  Sverkers sida har två återstående ogiltiga fronter och Kristinas fem.
- Recommendation: Fortsätt med en sjätte balanserad M-skiva om två
  frontpersoner per sida: P-0472 Petter Reinhold Pehrsson i Ånäset och
  P-0474 Carl Fredrik Grill på Sverkers sida samt P-0403 Nils Pehrsson och
  P-0404 Lisa Stina Larsdotter på Kristinas sida. Ge varje person verifierade
  föräldrar eller en reproducerbar giltig slutstatus, konsolidera akterna och
  stäng berörda prioritet-1-celler. Registrera men forska inte vidare på nya
  djup-7-personer.
- Owner decision required: none; urvalet behandlar samtliga återstående
  ogiltiga fronter på den mindre sidan och samma antal på den andra, i
  enlighet med north stars närhets- och balansregel samt delegerat mandat.
  T-0034 förblir en separat `IDEA` enligt ägarens formulering "vid tillfälle".
- Evidence:
  - `NORTH-STAR.md`
  - `PCD-2026-09-04-003`
  - `wotan/dev-log/T-0037.md`
  - `genealogy/research-log/2026-09-04.md`, batch 262
  - `node scripts/goal-state.mjs`
- Uncertainty: Flera av akterna har redan äldre sekundära uppgifter eller
  dokumenterade sökvägar. Ett reproducerbart terminalt utfall är fullgott om
  ingen säker personbärande nyckel kan nås; osäkra kandidater får inte
  propageras för att fylla den återstående generationen.
- Revisit when:
  - Den sjätte djup-6-skivan är verifierad
  - De tre återstående ogiltiga fronterna på Kristinas sida ska väljas
  - T-0034 ska aktiveras som avgränsad levandepersonsrevision
  - En bärande identitet eller extern åtkomstgräns kräver nytt vägval

## PCD-2026-09-04-012

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-010`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt ägarens instruktion och `PCD-2026-09-04-002`
- Decision: Fortsätt djup-6-programmet med den rekommenderade sjätte
  balanserade skivan om fyra personer. Skapa en enda ändlig Wotan-uppgift,
  registrera endast eventuella nya djup-7-föräldrar och behåll
  birthday.se-revisionen som separat senare arbete.
- Disposition: approved
- Supersedes decision: none; verkställer `PCD-2026-09-04-003` och bevarar
  `PCD-2026-09-04-008`.
- Related records: `PCR-2026-09-04-010`, `PCD-2026-09-04-008`,
  `wotan/dev-log/T-0037.md`, `wotan/README.md`
- Resulting Wotan tasks: `T-0038`; `T-0034` förblir `IDEA`.
- Portfolio signal: Projektet fortsätter balanserat genom djup 6 med en
  avgränsad fyrpersonersskiva som tömmer Sverkers återstående ogiltiga
  fronter utan att gå djupare där.
- Revisit when:
  - `T-0038` är verifierad och nästa skiva ska väljas
  - Ägaren uttryckligen aktiverar T-0034 tidigare
  - En konkret integritets-, licens- eller åtkomstkonflikt uppstår

## PCR-2026-09-04-011

- Record type: review
- Date: 2026-09-04
- Mode: checkpoint
- Trigger: `T-0038` har verifierat den sjätte djup-6-skivan och den
  exekverbara Wotan-kön är åter tom.
- Control judgement: continue, operate, preserve
- Current gate: Djup 6 är fortsatt närmaste obehandlade generation. Skivan
  höjde antalet granskade och källbreddsklara personer från 40 till 44 och
  minskade ogiltiga arkivfronter till och med djupet från sju till tre.
  Sverkers sida har nu noll sådana fronter; Kristinas sida har P-0451 Hindric
  Henriksson/Vinroth, P-0452 Brita Flinkberg och P-0454 James Schölin kvar.
- Recommendation: Behandla de tre kvarvarande ogiltiga fronterna tillsammans
  som en sista avvikelseutjämnande S-skiva. Ge varje person verifierade
  föräldrar eller en reproducerbar giltig slutstatus, konsolidera akterna och
  stäng deras prioritet-1-celler. Registrera men forska inte vidare på
  eventuella nya djup-7-personer. Återgå därefter till ett nytt balanserat
  urval bland ännu ogranskade men redan giltiga djup-6-personer.
- Owner decision required: none; Sverkers motsvarande ogiltiga frontkö är
  uttömd, och att sluta de tre återstående på Kristinas sida återställer
  saklig balans utan att fördjupa den redan färdiga sidan. T-0034 förblir
  separat `IDEA`; ägarens nya förtydligande bekräftar `PCD-2026-09-04-008`
  att belagda birthday.se-uppgifter får publiceras med källhänvisning men
  aktiverar inte det uttryckligen senare arbetstillfället.
- Evidence:
  - `NORTH-STAR.md`
  - `PCD-2026-09-04-003`
  - `PCD-2026-09-04-008`
  - `wotan/dev-log/T-0038.md`
  - `genealogy/research-log/2026-09-04.md`, batch 263
  - `node scripts/goal-state.mjs`
- Uncertainty: De tre akterna kan mynna ut i klassificerade källfronter i
  stället för nya föräldrar. Ingen namnlik kandidat får propageras utan en
  personbärande kedja.
- Revisit when:
  - Den sista ogiltiga djup-6-fronten är behandlad
  - Nästa balanserade granskningsskiva ska väljas
  - T-0034 ska aktiveras som avgränsad levandepersonsrevision
  - En bärande identitet eller extern åtkomstgräns kräver nytt vägval

## PCD-2026-09-04-013

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-011`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt ägarens instruktion och `PCD-2026-09-04-002`
- Decision: Fortsätt djup-6-programmet med den rekommenderade sista
  ogiltiga frontskivan om P-0451, P-0452 och P-0454. Skapa en enda ändlig
  Wotan-uppgift, registrera endast eventuella nya djup-7-föräldrar och behåll
  birthday.se-revisionen som separat senare arbete under
  `PCD-2026-09-04-008`.
- Disposition: approved
- Supersedes decision: none; verkställer `PCD-2026-09-04-003` och bevarar
  `PCD-2026-09-04-008`.
- Related records: `PCR-2026-09-04-011`, `PCD-2026-09-04-008`,
  `wotan/dev-log/T-0038.md`, `wotan/README.md`
- Resulting Wotan tasks: `T-0039`; `T-0034` förblir `IDEA`.
- Portfolio signal: Projektet behandlar den sista kända gruppen ogiltiga
  arkivfronter genom djup 6 innan nästa balanserade granskningsskiva väljs.
- Revisit when:
  - `T-0039` är verifierad
  - Ägaren uttryckligen aktiverar T-0034 tidigare
  - En konkret integritets-, licens- eller åtkomstkonflikt uppstår

## PCR-2026-09-04-012

- Record type: review
- Date: 2026-09-04
- Mode: checkpoint
- Trigger: `T-0039` har verifierat den sista ogiltiga arkivfronten genom
  djup 6 och den exekverbara Wotan-kön är åter tom.
- Control judgement: continue, operate, preserve
- Current gate: Djup 6 har 55 kända och nio korrekt stängda positioner samt
  noll ogiltiga fronter. Åtta kända personer återstår att konsolidera och
  källbreddsklassa: exakt fyra per probandsida. När de är behandlade uppfyller
  hela djupet north stars personmässiga fullständighetsmått.
- Recommendation: Fortsätt med en sista balanserad M-skiva om P-0230 Anders
  Nilsson, P-0231 Magdalena Eriksdotter, P-0473 Beata Jonsdotter och P-0475
  Johanna Jansdotter på Sverkers sida samt P-0415 Jonas Nordlund, P-0416
  Gertrud Olofsdotter, P-0447 Jöns Abrahamsson och P-0448 Brita Jonsdotter
  på Kristinas sida. Konsolidera varje akt och dess källfamiljer utan att
  återöppna giltiga terminala fronter utan ny nyckel. Registrera men forska
  inte vidare på eventuella nya djup-7-föräldrar.
- Owner decision required: none; kohorten är exakt den återstående
  balanserade mängden på närmaste obehandlade generation och följer det
  delegerade mandatet. T-0034 förblir separat `IDEA` tills ett efterföljande
  styravstamp väljer dess avgränsade tillfälle.
- Evidence:
  - `NORTH-STAR.md`
  - `PCD-2026-09-04-003`
  - `wotan/dev-log/T-0039.md`
  - `genealogy/research-log/2026-09-04.md`, batch 264
  - `node scripts/goal-state.mjs`
- Uncertainty: Personerna har redan giltiga arkivfronter eller verifierade
  relationer men varierande biografisk bredd. Uppgiften ska göra deras
  evidensläge komplett och jämförbart, inte skapa fler relationer för att
  förbättra ett mått.
- Revisit when:
  - Den sista balanserade djup-6-skivan är verifierad
  - Gemensamt djup 6 har nåtts och nästa strategiska prioritet ska väljas
  - T-0034 ska aktiveras som avgränsad levandepersonsrevision

## PCD-2026-09-04-014

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-012`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt ägarens instruktion och `PCD-2026-09-04-002`
- Decision: Fortsätt djup-6-programmet med den rekommenderade sista
  balanserade åttapersonersskivan. Konsolidera de åtta kvarvarande kända
  personerna och deras källbredd; registrera endast eventuella nya
  djup-7-föräldrar och håll T-0034 separat.
- Disposition: approved
- Supersedes decision: none; verkställer `PCD-2026-09-04-003` för den sista
  återstående djup-6-kohorten.
- Related records: `PCR-2026-09-04-012`, `PCD-2026-09-04-008`,
  `wotan/dev-log/T-0039.md`, `wotan/README.md`
- Resulting Wotan tasks: `T-0040`; `T-0034` förblir `IDEA`.
- Portfolio signal: Projektet arbetar mot att göra gemensamt djup 6 helt
  behandlat innan nästa strategiska prioritet väljs.
- Revisit when:
  - `T-0040` är verifierad
  - En konkret integritets-, licens- eller åtkomstkonflikt uppstår

## PCR-2026-09-04-013

- Record type: review
- Date: 2026-09-04
- Mode: milestone-review
- Trigger: `T-0040` har gjort gemensamt djup 6 helt behandlat och den
  exekverbara Wotan-kön är åter tom.
- Control judgement: continue, operate, preserve
- Current gate: Djup 6 har 55 kända och nio stängda positioner; samtliga 55
  kända personer är granskade och källbreddsklara och inga ogiltiga fronter
  finns genom djupet. Djup 7 är nu närmaste obehandlade generation med 29
  kända personer på Sverkers sida och 13 på Kristinas. Båda sidor har tydliga
  första frontpersoner och kan fortsatt behandlas balanserat.
- Recommendation: Öppna en första balanserad djup-7-skiva om fyra personer
  per sida. Behandla P-0149 Anna Catharina Andersdotter, P-0160 Jakob
  Isaksson, P-0161 Anna Stina Andersdotter och P-0162 Olof Larsson på
  Sverkers sida samt P-0417 Olof Stefansson, P-0418 Sigrid Jonsdotter,
  P-0502 Lars Larsson och P-0503 Anna Jonsdotter på Kristinas sida. Ge varje
  person verifierade föräldrar eller reproducerbar giltig slutstatus och gör
  källbredden komplett utan att forska vidare på nya djup-8-spetsar.
- Owner decision required: none; urvalet är den första återstående
  fyrgruppen på vardera sidan i `goal-state` och följer north stars närhets-
  och balansregel samt delegerat mandat. T-0034 förblir separat `IDEA`:
  ägaren har godkänt källan men uttryckligen lagt genomgången till ett senare
  avgränsat tillfälle.
- Evidence:
  - `NORTH-STAR.md`
  - `PCD-2026-09-04-003`
  - `PCD-2026-09-04-008`
  - `wotan/dev-log/T-0040.md`
  - `genealogy/research-log/2026-09-04.md`, batch 265
  - `node scripts/goal-state.mjs`
- Uncertainty: Flera personer har äldre grundbelägg men oprövad egen
  föräldrageneration. Skivans giltiga utfall kan därför vara nya minimala
  djup-8-föräldrar, klassificerade fronter eller en blandning.
- Revisit when:
  - Den första djup-7-skivan är verifierad
  - T-0034 ska aktiveras som avgränsad levandepersonsrevision
  - En bärande identitet eller extern åtkomstgräns kräver nytt vägval

## PCD-2026-09-04-015

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-013`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt ägarens instruktion och `PCD-2026-09-04-002`
- Decision: Fortsätt det balanserade anprogrammet med den rekommenderade
  första djup-7-skivan om åtta personer. Skapa en enda ändlig Wotan-uppgift,
  registrera endast eventuella nya djup-8-föräldrar och håll T-0034 separat.
- Disposition: approved
- Supersedes decision: none; förlänger den verifierade riktningen i
  `PCD-2026-09-04-003` från gemensamt djup 6 till nästa generation.
- Related records: `PCR-2026-09-04-013`, `PCD-2026-09-04-008`,
  `wotan/dev-log/T-0040.md`, `wotan/README.md`
- Resulting Wotan tasks: `T-0041`; `T-0034` förblir `IDEA`.
- Portfolio signal: Projektet har nått gemensamt djup 6 och fortsätter nu
  balanserat in i djup 7.
- Revisit when:
  - `T-0041` är verifierad
  - Ägaren uttryckligen aktiverar T-0034 tidigare
  - En konkret integritets-, licens- eller åtkomstkonflikt uppstår

## PCR-2026-09-04-014

- Record type: review
- Date: 2026-09-04
- Mode: milestone-review
- Trigger: `T-0041` har behandlat den första balanserade djup-7-skivan och
  den exekverbara Wotan-kön är åter tom.
- Control judgement: continue, operate, preserve
- Current gate: Djup 7 har 42 kända personer. Tio är granskade, åtta är
  källbreddsklara och 33 fronter är ännu ogiltiga. Närmast i den balanserade
  kön står P-0163–P-0166 på Sverkers sida och P-0504, P-0505, P-0508 samt
  P-0513 på Kristinas sida.
- Recommendation: Öppna en andra balanserad djup-7-skiva om fyra personer
  per sida. Ge varje person verifierade föräldrar eller reproducerbar giltig
  slutstatus; registrera endast eventuella nya djup-8-föräldrar och forska
  inte vidare på dem i samma uppgift.
- Owner decision required: none; urvalet följer north stars närhets- och
  balansregel och ryms inom ägarens delegerade mandat. T-0034 förblir en
  separat `IDEA`: Birthday.se är godkänt som öppen korroboreringskälla, men
  ägaren har uttryckligen lagt genomgången till ett senare tillfälle.
- Evidence:
  - `NORTH-STAR.md`
  - `PCD-2026-09-04-003`
  - `PCD-2026-09-04-008`
  - `wotan/dev-log/T-0041.md`
  - `genealogy/research-log/2026-09-04.md`, batch 266
  - `node scripts/goal-state.mjs`
- Uncertainty: De åtta fronterna varierar från nyligen återfunnet
  Storbäckenhushåll till äldre födelse- och hushållsuppgifter. Säkra utfall
  kan därför vara nya minimala djup-8-föräldrar eller klassificerade fronter.
- Revisit when:
  - Den andra djup-7-skivan är verifierad
  - T-0034 ska aktiveras som avgränsad levandepersonsrevision
  - En bärande identitet eller extern åtkomstgräns kräver nytt vägval

## PCD-2026-09-04-016

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-014`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt ägarens instruktion och `PCD-2026-09-04-002`
- Decision: Fortsätt djup-7-programmet med den rekommenderade andra
  balanserade åttapersonersskivan. Skapa en enda ändlig Wotan-uppgift,
  registrera endast eventuella nya djup-8-föräldrar och håll T-0034 separat.
- Disposition: approved
- Supersedes decision: none; verkställer den fortsatta riktningen i
  `PCD-2026-09-04-003` efter T-0041:s verifierade delresultat.
- Related records: `PCR-2026-09-04-014`, `PCD-2026-09-04-008`,
  `wotan/dev-log/T-0041.md`, `wotan/README.md`
- Resulting Wotan tasks: `T-0042`; `T-0034` förblir `IDEA`.
- Portfolio signal: Projektet fortsätter balanserat på närmaste obehandlade
  generation; levandepersonskorroborering är godkänd men inte aktiverad.
- Revisit when:
  - `T-0042` är verifierad
  - Ägaren uttryckligen aktiverar T-0034 tidigare
  - En konkret integritets-, licens- eller åtkomstkonflikt uppstår

## PCR-2026-09-04-015

- Record type: steering review
- Date: 2026-09-04
- Trigger: T-0042 är verifierad och Wotans aktiva kö är tom i kontinuerligt
  läge.
- North-star check: gemensamt djup 6 består. Djup 7 har 42 kända och 86
  stängda positioner; T-0042 ökade granskade personer från 10 till 18,
  källbreddsklara från 8 till 16 och minskade ogiltiga fronter från 33 till
  25 utan osäker propagation.
- Result check: den fasta åttapersonersskivan avslutades reproducerbart.
  Umeå landsförsamling C/3:s kompletta år 1764 och 1768 avvisade två privata
  datumprofiler; sex andra fronter kunde konsolideras från befintliga
  personbundna original. Inga djup-8-personer skapades.
- Assumption check: den bärande antagelsen — att nästa jämna djup-7-skiva
  ger mer målnytta än djupare eller redan väldokumenterad forskning — står
  kvar. Nästa närliggande kohort bör samtidigt hålla ihop redan öppnade
  familjepar där det minskar upprepning.
- User-value check: fortsatt jämn behandling förbättrar det framtida
  trädets och personkatalogens tillförlitlighet och fullständighet utan att
  utlösa en ny PDF före ägargrinden.
- Related-work / outside-change check: ingen ny extern förändring kräver
  omprioritering. Birthday.se är genom `PCD-2026-09-04-008` godkänt som
  öppen korroboreringskälla, men T-0034 är uttryckligen ett senare separat
  arbete och ska inte blandas in i arkivfrontskivan.
- Options considered:
  - fortsätt med en tredje balanserad djup-7-skiva;
  - aktivera T-0034 nu;
  - pausa för ny PDF eller djup-8-forskning.
- Recommendation: fortsätt med en tredje fast åttapersonersskiva. Välj på
  Sverkers sida P-0221 Erik Andersson, P-0222 Anna Ersdotter och paret
  P-0232 Nils Nilsson–P-0233 Magdalena Andersdotter. Välj på Kristinas sida
  P-0514 Britta Andersdotter, paret P-0515 Olof Nilsson–P-0516 Maja
  Jonsdotter samt P-0517 Samuel Bökelund. Anna Ersdotter har redan
  verifierade föräldrar men saknar granskning/källbredd; hennes konsolidering
  balanserar paret mot den svårare Erik-fronten.
- Evidence:
  - `NORTH-STAR.md`
  - `PCD-2026-09-04-003`
  - `PCD-2026-09-04-008`
  - `wotan/dev-log/T-0042.md`
  - `genealogy/research-log/2026-09-04.md`, batch 267
  - `node scripts/goal-state.mjs`
- Uncertainty: P-0221:s närmaste födelsevolym är odigitaliserad hos
  Riksarkivet, medan flera av de övriga endast har barnbärande original utan
  eget datum. Utfallet kan därför bli en blandning av verifierad
  föräldralänk och klassificerade terminaler.
- Revisit when:
  - Den tredje djup-7-skivan är verifierad
  - T-0034 ska aktiveras som avgränsad levandepersonsrevision
  - En bärande identitet eller extern åtkomstgräns kräver nytt vägval

## PCD-2026-09-04-017

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-015`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt ägarens instruktion och `PCD-2026-09-04-002`
- Decision: Fortsätt djup-7-programmet med den rekommenderade tredje
  balanserade åttapersonersskivan. Skapa en enda ändlig Wotan-uppgift,
  registrera endast eventuella nya djup-8-föräldrar och håll T-0034 separat.
- Disposition: approved
- Supersedes decision: none; verkställer den fortsatta riktningen i
  `PCD-2026-09-04-003` efter T-0042:s verifierade delresultat.
- Related records: `PCR-2026-09-04-015`, `PCD-2026-09-04-008`,
  `wotan/dev-log/T-0042.md`, `wotan/README.md`
- Resulting Wotan tasks: `T-0043`; `T-0034` förblir `IDEA`.
- Portfolio signal: Projektet fortsätter balanserat på närmaste obehandlade
  generation; levandepersonskorroborering är godkänd men inte aktiverad.
- Revisit when:
  - `T-0043` är verifierad
  - Ägaren uttryckligen aktiverar T-0034 tidigare
  - En konkret integritets-, licens- eller åtkomstkonflikt uppstår

## PCR-2026-09-04-016

- Record type: review
- Date: 2026-09-04
- Mode: milestone-review
- Trigger: `T-0043` är verifierad och den exekverbara Wotan-kön är åter
  tom.
- Control judgement: continue, operate, preserve
- Current gate: Djup 7 har 42 kända personer. Tjugosex är granskade, 24 är
  källbreddsklara och 18 fronter är ännu ogiltiga. Kristinas sida har endast
  P-0518 kvar obehandlad; Sverkers sida har 17 ogiltiga fronter.
- Recommendation: Öppna en fjärde åttapersonersskiva som först tar den sista
  Kristina-fronten och därefter de sju närmaste Sverker-positionerna:
  P-0518, P-0234–P-0235, P-0264–P-0267 och P-0476. Detta håller tre
  familjepar samman och accepterar den nödvändiga sidobalansen först efter
  att Kristinas kö är tömd.
- Owner decision required: none; sidobalansen följer direkt av att ena
  probandsidans aktuella kö har en enda person kvar och ryms inom delegerat
  mandat. T-0034 förblir separat `IDEA` för den senare Birthday.se-revisionen.
- Evidence:
  - `NORTH-STAR.md`
  - `PCD-2026-09-04-003`
  - `PCD-2026-09-04-008`
  - `wotan/dev-log/T-0043.md`
  - `genealogy/research-log/2026-09-04.md`, batch 268
  - `node scripts/goal-state.mjs`
- Uncertainty: P-0267 har tre konflikterande exakta datum och P-0234–P-0235
  en olokaliserad `N:o 63`-nyckel. Kohorten kan kräva riktad originalläsning;
  osäkra datum eller nummer får inte propageras.
- Revisit when:
  - Den fjärde djup-7-skivan är verifierad
  - T-0034 ska aktiveras som avgränsad levandepersonsrevision
  - En bärande identitet eller extern åtkomstgräns kräver nytt vägval

## PCD-2026-09-04-018

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-016`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt ägarens instruktion och `PCD-2026-09-04-002`
- Decision: Fortsätt med den rekommenderade fjärde djup-7-skivan. Töm den
  sista Kristina-fronten och behandla därefter de sju närmaste
  Sverker-positionerna i samma ändliga Wotan-uppgift. Registrera endast
  eventuella nya djup-8-föräldrar och håll T-0034 separat.
- Disposition: approved
- Supersedes decision: none; verkställer den fortsatta riktningen i
  `PCD-2026-09-04-003` efter T-0043:s verifierade delresultat.
- Related records: `PCR-2026-09-04-016`, `PCD-2026-09-04-008`,
  `wotan/dev-log/T-0043.md`, `wotan/README.md`
- Resulting Wotan tasks: `T-0044`; `T-0034` förblir `IDEA`.
- Portfolio signal: Kristinas djup-7-kö töms först; därefter fortsätter
  kvarvarande Sverker-front i närhetsordning.
- Revisit when:
  - `T-0044` är verifierad
  - Ägaren uttryckligen aktiverar T-0034 tidigare
  - En konkret integritets-, licens- eller åtkomstkonflikt uppstår

## PCR-2026-09-04-017

- Record type: review
- Date: 2026-09-04
- Mode: checkpoint
- Trigger: `T-0044` är verifierad och den exekverbara Wotan-kön är åter
  tom.
- Control judgement: continue, operate, preserve
- Current gate: Djup 7 har 42 kända personer. Trettiotvå är granskade och
  källbreddsklara; de tio återstående ogiltiga fronterna finns samtliga på
  Sverkers sida. Kristinas djup-7-kö är helt behandlad.
- Recommendation: Öppna en sista djup-7-skiva med de tio återstående
  personerna: P-0477–P-0479, P-0500, P-0506–P-0512. Behandla dem i en
  ändlig uppgift, håll familjeparen samman och registrera endast säkra nya
  djup-8-föräldrar. Gör därefter en ny kontrollpunkt innan djup 8.
- Owner decision required: none; detta fullföljer den redan delegerade,
  närhetsstyrda djup-7-vågen. T-0034 förblir separat `IDEA` för den senare
  Birthday.se-revisionen.
- Evidence:
  - `NORTH-STAR.md`
  - `PCD-2026-09-04-003`
  - `PCD-2026-09-04-008`
  - `wotan/dev-log/T-0044.md`
  - `genealogy/research-log/2026-09-04.md`, batch 269
  - `node scripts/goal-state.mjs`
- Uncertainty: P-0477 har en stark men ännu obunden Helena/Lena-kandidat,
  medan flera övriga endast har en parentbärande barnnotis. Den sista skivan
  kan därför ge både säkra nya föräldrar och reproducerbara terminaler;
  kandidatlikhet får inte propageras.
- Revisit when:
  - Den sista djup-7-skivan är verifierad
  - T-0034 ska aktiveras som avgränsad levandepersonsrevision
  - En bärande identitet eller extern åtkomstgräns kräver nytt vägval

## PCD-2026-09-04-019

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-017`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt ägarens instruktion och `PCD-2026-09-04-002`
- Decision: Fortsätt djup-7-programmet med den rekommenderade sista
  tiopersonersskivan. Behandla P-0477–P-0479, P-0500 och P-0506–P-0512 i
  en enda ändlig Wotan-uppgift, registrera endast säkra nya
  djup-8-föräldrar och håll T-0034 separat.
- Disposition: approved
- Supersedes decision: none; fullföljer riktningen i
  `PCD-2026-09-04-003` efter T-0044:s verifierade delresultat.
- Related records: `PCR-2026-09-04-017`, `PCD-2026-09-04-008`,
  `wotan/dev-log/T-0044.md`, `wotan/README.md`
- Resulting Wotan tasks: `T-0045`; `T-0034` förblir `IDEA`.
- Portfolio signal: Projektet fortsätter genom de tio sista kända
  djup-7-fronterna; levandepersonskorroborering är godkänd men inte
  aktiverad.
- Revisit when:
  - `T-0045` är verifierad
  - Ägaren uttryckligen aktiverar T-0034 tidigare
  - En konkret integritets-, licens- eller åtkomstkonflikt uppstår

## PCR-2026-09-04-018

- Record type: review
- Date: 2026-09-04
- Mode: checkpoint
- Trigger: `T-0045` har gjort djup 7 helt behandlat och den exekverbara
  Wotan-kön är tom.
- Control judgement: continue, operate, preserve
- Current gate: Gemensamt behandlat djup är 7. På djup 8 finns endast två
  kända personer, paret P-0226 Erik Larsson–P-0227 Brita Andersdotter i
  Sannerby; båda har en exakt äldre hushållsrutt men är ännu ogranskade och
  har prioritet-1-celler.
- Recommendation: Öppna en enda ändlig uppgift för Sannerbyparet. Läs först
  det redan identifierade äldre A I/3-uppslaget och använd därefter endast
  personbundna födelse-, vigsel-, död-, mantals- eller bouppteckningsnycklar.
  Registrera säkra djup-9-föräldrar minimalt och stanna för ny kontrollpunkt
  efter paret.
- Owner decision required: none; detta är den enda närmaste kända fronten
  och följer north stars bredd- och närhetsregel. T-0034 förblir separat
  `IDEA`.
- Evidence:
  - `NORTH-STAR.md`
  - `PCD-2026-09-04-003`
  - `PCD-2026-09-04-008`
  - `wotan/dev-log/T-0045.md`
  - `genealogy/research-log/2026-09-04.md`, batch 270
  - `node scripts/goal-state.mjs`
- Uncertainty: hushållsåren 1768 och omkring 1772 kan vara avrundade eller
  överförda. Sannerbyuppslaget kan ge en brygga men behöver inte namnge
  föräldrar; ingen bred födelsesökning ska starta på årtalen ensamma.
- Revisit when:
  - Sannerbyparet är verifierat eller har reproducerbara terminaler
  - T-0034 ska aktiveras som avgränsad levandepersonsrevision
  - En ny personbunden nyckel väsentligt ändrar fronten

## PCD-2026-09-04-020

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-018`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt ägarens instruktion och `PCD-2026-09-04-002`
- Decision: Fortsätt med en avgränsad Sannerbyuppgift för P-0226 Erik
  Larsson och P-0227 Brita Andersdotter. Börja i den exakta äldre
  hushållsrutten, skapa endast säkra minimala djup-9-föräldrar och håll
  T-0034 separat.
- Disposition: approved
- Supersedes decision: none; fortsätter närhetsregeln efter att djup 7 blivit
  helt behandlat.
- Related records: `PCR-2026-09-04-018`, `PCD-2026-09-04-008`,
  `wotan/dev-log/T-0045.md`, `wotan/README.md`
- Resulting Wotan tasks: `T-0046`; `T-0034` förblir `IDEA`.
- Portfolio signal: Projektet fortsätter med sin enda kända djup-8-front och
  behöver ingen parallell ny riktning.
- Revisit when:
  - `T-0046` är verifierad
  - Ägaren uttryckligen aktiverar T-0034 tidigare
  - En konkret integritets-, licens- eller åtkomstkonflikt uppstår

## PCR-2026-09-04-019

- Record type: review
- Date: 2026-09-04
- Mode: checkpoint
- Trigger: `T-0046` har behandlat den enda kända djup-8-fronten och den
  exekverbara Wotan-kön är tom.
- Control judgement: wait, preserve, do nothing
- Current gate: Gemensamt behandlat djup är 8. Alla då nåbara kända personer
  är granskade och källbreddsklara, samtliga anspetsar har giltig
  arkivfront och båda balanserade anspetsrevisionerna rapporterar noll
  ogiltiga slutstatusar. Erik född 1770 i äldre Sannerby är uttryckligen en
  obunden kandidat och öppnar ingen säker djup-9-position.
- Recommendation: Bevara det verifierade läget och öppna ingen ny
  arkivuppgift utan en ny personbunden identitetsnyckel eller förändrad
  digital åtkomst. Låt T-0034 ligga kvar som godkänd framtida
  levandepersonsrevision; ägarens formulering ”vid tillfälle” och senare
  publiceringsförtydligande ger tillstånd och ramar men inte en omedelbar
  starttidpunkt.
- Owner decision required: none; ägaren har delegerat övriga beslut till
  Project Control, och vänteläget undviker både omotiverad breddsökning och
  en oavsiktlig aktivering av ett separat integritetskänsligt arbetsområde.
- Evidence:
  - `NORTH-STAR.md`
  - `PCD-2026-09-04-008`
  - `PCD-2026-09-04-020`
  - `wotan/dev-log/T-0046.md`
  - `genealogy/research-log/2026-09-04.md`, batch 271
  - `genealogy/citations/C-0863-ardala-AI3-aldre-sannerby-1784-1793.md`
  - `node scripts/goal-state.mjs`
- Uncertainty: Nya digitaliseringar eller en personbunden vigsel-, flytt-,
  döds-, boupptecknings- eller hushållsrad kan flytta en enskild front.
  Birthday.se-revisionens exakta personkohort och publiceringsfält är ännu
  inte aktiverade som körbar uppgift.
- Revisit when:
  - En ny personbunden nyckel eller ändrad arkivåtkomst framkommer
  - Ägaren uttryckligen aktiverar T-0034, T-0009 eller T-0010
  - En bärande identitet eller relation ifrågasätts

## PCD-2026-09-04-021

- Record type: decision
- Date: 2026-09-04
- Decides review: `PCR-2026-09-04-019`
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt ägarens instruktion och `PCD-2026-09-04-002`
- Decision: Avsluta den nuvarande balanserade anlinjevågen vid dess
  verifierade online-arkivfronter. Skapa ingen ny Wotan-uppgift nu; invänta
  en ny personbunden källnyckel, förändrad digital åtkomst eller ägarens
  uttryckliga aktivering av ett separat IDEA-spår.
- Disposition: approved
- Supersedes decision: none; fullbordar riktningen i
  `PCD-2026-09-04-020` efter T-0046:s verifierade resultat.
- Related records: `PCR-2026-09-04-019`, `PCD-2026-09-04-008`,
  `wotan/dev-log/T-0046.md`, `genealogy/research-log/2026-09-04.md`
- Resulting Wotan tasks: none; T-0034, T-0009 och T-0010 förblir `IDEA`.
- Portfolio signal: Projektet är i verifierat vänteläge, inte blockerat.
  Anlinjernas nu nåbara kohort är behandlad; nya riktningar kräver nyckel
  eller uttrycklig aktivering.
- Revisit when:
  - En ny personbunden nyckel eller ändrad arkivåtkomst framkommer
  - Ägaren uttryckligen aktiverar T-0034, T-0009 eller T-0010
  - En bärande identitet eller relation ifrågasätts

## PCR-2026-09-05-001

- Record type: review
- Date: 2026-09-05
- Mode: direction-review
- Trigger: Ägaren ifrågasätter stoppet och begär att omprövning och
  projekttillstånd bevaras inför sessionsbyte.
- Control judgement: evaluate, redirect, preserve
- Revises review: PCR-2026-09-04-019
- Current gate: Saklig tillräcklighet hos avsluten är inte verifierad.
  Målverktygets complete-markering var för tidig och får inte styra återstart.
- Recommendation: Revidera avslutsbedömningar balanserat från närmaste
  generation och pröva genomförbara fortsättningar. Styr mot hela north star,
  inklusive livsbilder och relevant leverantörstäckning.
- Owner decision required: none för att bevara rättelsen; måltextens
  förbättringar är förslag inför nästa session, inte antagna ändringar.
- Evidence:
  - NORTH-STAR.md
  - NORTH-STAR-REVIEW-2026-09-05.md
  - genealogy/citations/C-0863-ardala-AI3-aldre-sannerby-1784-1793.md
  - scripts/goal-state.mjs
  - scripts/lib/terminal-status.mjs
  - node scripts/goal-state.mjs: djup 8 enligt befintliga klassificeringar
- Uncertainty: Alla tidigare avslut har inte sakgranskats på nytt. Vi vet
  att uppfyllelsebeskedet saknar stöd, inte att varje enskilt avslut är fel.
- Revisit when: Nästa session återupptar arbetet eller målkontraktet revideras.

## PCD-2026-09-05-001

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-001
- Owner: Sverker Adam Janson; begärd persistens och sessionspaus, med
  tidigare delegerat Project Control-mandat för operativ rättelse.
- Decision: Bevara att north star inte är visad uppfylld och ersätt det
  tidigare generella stoppbeslutet med behov av avslutsrevision. Pausa nu
  för ägarens sessionsbyte. Behåll originalobservationer och historiska
  uppgiftsresultat; inga nya forskningsbatchar startas i denna överlämning.
- Disposition: modified
- Supersedes decision: PCD-2026-09-04-021
- Resulting Wotan tasks: none vid sessionsbytet; nästa session skär en
  ändlig revisionsuppgift ur den sakligt omprövade fronten.
- Portfolio signal: Ofullbordat projekt, pausat för sessionsbyte; inte
  avslutat i väntan på nya digitaliseringar.
- Revisit when: Ägaren återupptar kontinuerligt arbete i nästa session.

## PCD-2026-09-05-002

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-001
- Owner: Sverker Adam Janson
- Decision: Ägaren instruerar att vässa NORTH-STAR.md enligt granskningens
  förslag. Inför daterade, sakliga uppfyllelsekrav för anlinjer, livsbilder,
  kandidater, källtäckning, spårbarhet och avslutningsrevision. Förtydliga
  att administrativa mått inte bevisar uppfyllelse, att villkorliga vägar
  kräver prövade beroenden och att kontinuerligt arbete kan fortsätta genom
  Project Control inom befintligt mandat. Separera externa hinder från
  uppfyllelse och framtida underhåll från bedömning av dagens källäge.
- Disposition: approved
- Related records: NORTH-STAR.md, NORTH-STAR-REVIEW-2026-09-05.md,
  HANDOVER.md, PCD-2026-09-05-001
- Resulting Wotan tasks: none; denna ändring gäller styrtext och överlämning.
  Kodändringar och sakrevision av avslut återstår inför fortsatt forskning.
- Portfolio signal: Skärpt uppfyllelsekontrakt antaget; projektet kvarstår
  ofullbordat och pausat för sessionsbyte.
- Revisit when: Nästa session återupptar arbetet enligt det skärpta målet.

## PCR-2026-09-05-002

- Record type: review
- Date: 2026-09-05
- Mode: checkpoint
- Trigger: Ägaren ifrågasätter separat HANDOVER.md, obegränsade tasks och
  risken för upprepat arbete vid sessionsbyte och begär en fungerande lösning.
- Control judgement: redirect, preserve
- Current gate: Ingen extern gate för styrändringen. Läsordning och
  återupptagningskontrakt är otydliga, medan den konkreta avslutsrevisionen
  och kända kodluckor ännu saknar egna körbara uppgifter.
- Recommendation: Gör wotan/README obligatorisk före uppgiftsval. Låt
  backlog och respektive dev-log bära all exekveringskontinuitet och
  återupptagning, med ändligt omfång, verifierbara resultat och aktuella
  checkpoints. Ta bort HANDOVER och gamla instruktioner som återaktiverar
  T-0012. Bevara beslut och kunskap på sina kanoniska platser.
- Owner decision required: Godkänn repo-lokal ändring och borttagning av
  separat handover; lämna globala skills och historiska loggar oförändrade.
- Evidence:
  - Ägarens instruktioner 2026-09-05 om att inte migrera gammal handover-prosa,
    avgränsa tasks och spara avbrutet arbete i respektive task
  - AGENTS.md, README.md, wotan/README.md, wotan/backlog.json
  - genealogy/README.md och genealogy/research-plan.md har fortfarande
    avslutade T-0012 som aktuell utgåveinstruktion
  - PCD-2026-09-05-001, PCD-2026-09-05-002,
    NORTH-STAR-REVIEW-2026-09-05.md
- Uncertainty: Markdown-baserade checkpoints ger ingen teknisk
  exakt-en-gång-garanti vid abrupt avbrott. Agenten måste stämma av faktiska
  artefakter och externa effekter innan ett osäkert steg upprepas.
- Revisit when: Återupptagning tappar delresultat, samma arbete upprepas utan
  saklig anledning, en task växer över sin gräns eller kontinuerlig målkörning
  stannar på tom kö utan saklig uppfyllelsebedömning.

## PCD-2026-09-05-003

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-002
- Owner: Sverker Adam Janson; uttryckligt godkännande ”läser projektet
  wotan/README.md? förtydliga. och lös resten så att det fungerar bra.”
- Decision: Avskaffa separat HANDOVER.md och gör återupptagning till en
  normal del av varje avgränsad Wotan-uppgift. Förtydliga AGENTS läskedja,
  uppgiftsavgränsning, avbrottsstatus och hur redan verifierat arbete består.
  Kontinuerlig north-star-körning använder Project Control vid tom/blockerad
  kö och kan skapa motiverat ändligt arbete inom befintligt mandat utan
  nytt rutinmedgivande. Enstaka uppdrag behåller sitt beställda omfång.
  Bevara denna sessions konkreta kvarstående arbete i separata uppgifter;
  kopiera inte den gamla handover-historiken till en ny lägessida.
- Disposition: approved
- Supersedes decision: PCD-2026-09-04-001 endast beträffande separat
  handover, obligatorisk M-storlek och måttdelta som tillräcklig färdiggrind;
  PCD-2026-09-05-001/002 endast beträffande att uppgifter ska skapas först
  i nästa session. Sessionspausen, rättelsen av för tidigt stopp och
  NORTH-STAR.md:s skärpta sakkrav består.
- Related records: PCD-2026-09-04-002, PCD-2026-09-05-001,
  PCD-2026-09-05-002, wotan/README.md
- Resulting Wotan tasks: T-0047 genomför kontinuitetsändringen; T-0048
  sakgranskar de fyra närmaste föräldrafronterna; T-0049 rättar tre
  avgränsade mått-/validatorbrister. T-0034 och övriga IDEA-spår består.
- Portfolio signal: Projektet är ofullbordat och förbereds för sessionsbyte.
  Forsknings-/målkörningen återstartas inte av styrfilsarbetet. Nästa körning
  väljer arbete genom vanlig backlogstatus, utan en separat handover-task.
- Revisit when: T-0048 eller T-0049 ger skäl att omprioritera, en konkret
  återupptagningsbrist upptäcks eller målets avslutningsrevision ska göras.

Tidigare hänvisningar till HANDOVER.md och T-0012 är bevarade som historiska
belägg, inte aktiva läsinstruktioner. Ingen ny handover-arkivkopia skapas;
tidigare versioner finns i Git och tidigare bevarad forskningshistorik.

## PCR-2026-09-05-003

- Record type: review
- Date: 2026-09-05
- Mode: checkpoint
- Trigger: Ägaren har återupptagit det kontinuerliga målet; T-0048 finner
  specifika oprövade fortsättningar i de fyra närmaste föräldrafronterna.
- Control judgement: continue, evaluate, preserve
- Current gate: Källprövning återstår. Tidigare saknade egna födelsedatum
  har behandlats som vänteskäl trots användbara hushålls- och familjenycklar.
  Vissa andra exakta original har dokumenterade läsesalshinder.
- Options considered: invänta externa nycklar; återköra stora tidigare
  sökningar; eller pröva fyra ändliga källpassager från befintliga ankare.
- Recommendation: Välj de fyra riktade passagerna. T-0049 rättar först
  indikatorernas kända fel enligt befintlig kö. Därefter prövas Augusta
  och Olaus före de två återstående Sverkerfronterna. Behåll alla tidigare
  avgränsade noll och analoga hinder, men använd dem inte som generellt stopp.
- Owner decision required: none; ägaren delegerar övriga beslut till Project
  Control inom befintliga handlingsgränser och har uttryckligen återstartat.
- Evidence:
  - `genealogy/research-log/2026-09-05.md`, batch 272
  - `genealogy/citations/C-0417-folkrakning-1930-augusta-alva-smuleberg.md`
  - `genealogy/citations/C-0756-pitea-porsnas-olof-pehrsson-1858-olost.md`
  - `wotan/dev-log/T-0048.md`, `wotan/dev-log/T-0049.md`
  - `NORTH-STAR.md`, `PCD-2026-09-05-003`
- Uncertainty: Passagerna kan ge nya identitetsnycklar, avvisade kandidater,
  avgränsade noll eller faktiska externa hinder. Revisionen bevisar inte
  att någon viss förälder kommer att identifieras eller att alla andra
  materiella livsbilds- och leverantörsfrågor redan är undersökta.
- Revisit when: Varje avgränsad passage är verifierad, ett verkligt hinder
  blockerar den, eller T-0049 visar ytterligare materiella granskningsfel.

## PCD-2026-09-05-004

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-003
- Owner: Sverker Adam Janson; delegerat operativt mandat utövat genom
  Project Control enligt det återupptagna kontinuerliga målet och
  PCD-2026-09-04-002.
- Decision: Genomför de fyra avgränsade fortsättningarna efter T-0048:s
  verifiering: Augustas Smulebergshushåll 1930, Olaus mantalsuppgift 1877,
  Porsnäskandidatens barnhushåll 1854–1856 och Anders Bubergetkedja före 1867.
  Kör T-0049 enligt befintlig kö. Bevara kandidatgränser och tidigare
  källäsningar; inga beställningar, kontoköp, meddelanden, nya PDF:er eller
  publicerings-/Gitåtgärder medges genom detta beslut.
- Disposition: approved
- Resulting Wotan tasks: T-0050, T-0051, T-0052, T-0053.
- Portfolio signal: Projektet är aktivt och ofullbordat. Konkreta
  genomförbara forskningsåtgärder finns; inget generellt externt hinder
  mot fortsatt framdrift är visat. IDEA-spåren förblir parkerade.
- Revisit when: De fyra passagerna har gett verifierade resultat eller
  hinder, eller ett nytt sakligt granskningsfel kräver ändrad ordning.

## PCR-2026-09-05-004

- Record type: review
- Date: 2026-09-05
- Mode: checkpoint
- Trigger: T-0049:s regressionstester och korrigerade mått exponerar 96
  bristfälliga Slutstatus-sektioner och fyra tidigare dolda matrisrader.
- Control judgement: continue, evaluate, preserve
- Current gate: Skillnaden mellan dokumentationsbrist och sakligt olöst
  forskningsfråga är ännu inte avgjord för den inventerade mängden.
- Recommendation: Slutför koduppgiften och behåll de fyra närmare
  forskningspassagerna först. Gör därefter en separat avgränsad avstämning
  mot befintliga belägg. Automatiskt ifyllda återstartfraser skulle dölja
  luckorna; omkörning av all forskning saknar motivering.
- Owner decision required: none; inom ägarens delegerade mandat.
- Evidence: `wotan/dev-log/T-0049-structural-gaps.md`,
  `scripts/goal-state.test.mjs`, `genealogy/source-coverage.md` och
  `node scripts/goal-state.mjs` efter rättningen.
- Uncertainty: De 79 aktiva formellt ogiltiga fronterna är inte därmed
  falsifierade personidentiteter. De fyra matrisraderna kan innehålla både
  sakligt kvarstående arbete och osynkroniserad äldre status.
- Revisit when: De närmare passagerna är verifierade eller avstämningen
  ger en konkret ny materiell forskningsfråga.

## PCD-2026-09-05-005

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-004
- Owner: Sverker Adam Janson; Project Control utövar delegerat mandat
  enligt det kontinuerliga målet och PCD-2026-09-04-002.
- Decision: Skapa T-0054 för exakt den inventerade mängden om 96
  Slutstatus-sektioner och fyra matrisrader, med avstämning mot befintliga
  belägg och utan ny extern forskning. Kör efter T-0050–T-0053. Behåll
  osäkra eller sakligt otillräckliga avslut öppna; kräv inte gröna etiketter.
- Disposition: approved
- Resulting Wotan tasks: T-0054.
- Portfolio signal: Projektet fortsätter aktivt med närmare forskning
  före den större dokumentationsavstämningen. Inget generellt hinder finns.
- Revisit when: Föregångarna ändrar inventeringens beläggsläge, eller
  T-0054 identifierar behov av nästa balanserade forskningsskiva.

## PCD-2026-09-05-006

- Record type: decision
- Date: 2026-09-05
- Owner: Sverker Adam Janson, uttrycklig instruktion.
- Decision: Vid tillfällig utloggning/captcha hos Riksarkivet ska den exakta
  väntande åtgärden bevaras i Wotan. Fortsätt med annat godkänt arbete,
  exempelvis MCP, medan ägaren loggar in. Återuppta den sparade passagen
  när ägaren meddelar att åtkomsten är återställd.
- Disposition: approved
- Resulting Wotan tasks: Befintliga T-0050, T-0051 och T-0053; ingen ny uppgift.
- Evidence: Ägarens meddelande 2026-09-05 och åter synlig originalbild
  00081273_00026 i Chrome efter inloggningen.
- Revisit when: Åtkomsten åter bryts; tillämpa återupptagningsrutinen i wotan/README.md.


## PCR-2026-09-05-005

- Record type: review
- Date: 2026-09-05
- Mode: checkpoint
- Trigger: T-0050 har återfunnit Augustas direkta Skövdehushåll; dess
  avgränsade bakåtbrygga är utförd men två materiella livsfrågor återstår.
- Control judgement: continue, preserve
- Current gate: Den konkreta äldre bokhänvisningen och närmast följande
  Smulebergsbok är oprövade. Tillfällig utloggning är inte längre hindret.
- Recommendation: Behåll den ursprungliga gränsen för T-0050 och skapa
  två separata ändliga passager: äldre bokhushåll från Skövde sida 768,
  respektive nästa Smulebergsbok för Augustas egen död/flytt. Kör den
  redan beslutade Anderspassagen T-0053 före nya Augustauppgifter.
  Återkom till Olaus på Kristinas sida när dess exakta original blir åtkomligt.
- Owner decision required: none; inom det kontinuerliga delegerade mandatet.
- Evidence: C-0868/S-0680, A-3265–A-3269, T-0050, batch 279–280,
  NORTH-STAR.md och PCD-2026-09-05-004/006.
- Uncertainty: Samma födelsedatum identifierar inte Mofallakandidaten.
  Tomma dödsfält är ingen överlevnadsuppgift. Ingen föräldrabrygga finns än.
- Revisit when: Den avgränsade passagen ger nya belägg eller konkret hinder;
  ompröva ordningen om Kristinas Olausoriginal blir tillgängligt.

## PCD-2026-09-05-007

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-005
- Owner: Sverker Adam Janson; Project Control utövar uttryckligen delegerat
  operativt mandat enligt det aktiva kontinuerliga målet.
- Decision: Genomför T-0055 och T-0056 inom deras ändliga källpassager
  efter T-0053. Behåll H/D öppna för Augusta och alla kandidatgränser.
  Bevara tidigare Värsås-/födelseboksnoll; ingen blind omläsning medges.
  Inga beställningar, meddelanden, kontoköp, PDF:er eller publicerings-/Gitåtgärder.
- Disposition: approved
- Resulting Wotan tasks: T-0055, T-0056.
- Portfolio signal: Projektet är aktivt och ofullbordat; närmaste generation
  har konkret körbart arbete utan att djupare välbelagda grenar prioriteras.
- Revisit when: T-0053 eller de nya passagerna ger belägg som ändrar ordningen.


## PCR-2026-09-05-006

- Record type: review
- Date: 2026-09-05
- Mode: checkpoint
- Trigger: T-0053 har belagt Anders föräldrar och falsifierat det äldre
  barndomsavslutet. Egen födelsenotis och dagkonflikt består.
- Control judgement: continue, preserve
- Current gate: En konkret positiv familjenyckel finns nu, men tidiga
  hushåll och dess betydelse för C-0107:s födelsenoll är oprövade.
- Recommendation: Avsluta den ändliga T-0053-passagen efter verifiering.
  Behåll redan beslutade T-0055/T-0056 först; skapa T-0057 för Anders
  egen kvarstående födelsefråga. Skjut föräldrarnas egna anexpeditioner
  till närmare djup-5-frågor har prövats. Att stanna vid ett känt felaktigt
  bynoll är inte försvarbart; att genast driva de nya anorna djupare skulle
  bryta den balanserade ordningen. Olaus åtkomstvillkor kvarstår separat.
- Owner decision required: none; uttryckligen delegerat kontinuerligt mandat.
- Evidence: C-0869, A-3270–A-3295, P-0065/P-0082/P-0519,
  batch283–284, PCD-2026-09-05-004/007, NORTH-STAR.md.
- Uncertainty: Föräldralängderna är kompletterande belägg med möjlig
  datumkopiering. De löser relationen men inte egen födelsenotis.
- Revisit when: T-0057 ger belägg eller hinder, eller Olaus original blir åtkomligt.

## PCD-2026-09-05-008

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-006
- Owner: Sverker Adam Janson; Project Control utövar delegerat mandat
  enligt det aktiva kontinuerliga målet.
- Decision: Skapa T-0057 efter T-0055/T-0056 för högst två tidigare
  Bubergetshushåll och en familjenyckelstyrd kontroll av redan bevarade
  C-0107-original. Det nya föräldraparet och det påvisade äldre
  avgränsningsfelet motiverar kontrollen, inte ett sessionsbyte.
  Inga föräldrars egna föräldrar söks inom uppgiften. Behåll alla
  tidigare observationer och låt rättelser vara nya poster.
- Disposition: approved
- Resulting Wotan tasks: T-0057.
- Portfolio signal: Aktiv närmare forskning; två nya anfronter är öppna,
  inte uppfyllda. Ingen ägarfråga eller generell inloggningsspärr.
- Revisit when: Den avgränsade passagen har gett resultat eller konkret hinder.


## PCR-2026-09-05-007

- Record type: review
- Date: 2026-09-05
- Mode: checkpoint
- Trigger: T-0055 har använt sina två direkta poster och säkrat flytten1924;
  en ny exakt Kyrkefallasida623 återstår oläst.
- Control judgement: continue, preserve
- Current gate: Äldre hushållsbrygga saknas trots att en konkret sidnyckel finns.
- Recommendation: Bevara T-0055:s gräns och skapa en separat passage
  från623. Kör först redan beslutade T-0056 och T-0057. Att fortsätta
  hela kedjan inom T-0055 skulle bryta dess tvåpostgräns; att invänta ny
  ägaruppgift saknar sakskäl när det finns en läsbar originalhänvisning.
- Owner decision required: none; delegerat kontinuerligt mandat.
- Evidence: C-0870, S-0682, A-3296–A-3299, batch285, T-0055,
  PCD-2026-09-05-007/008 och NORTH-STAR.md.
- Uncertainty: Hustrun är onamngiven i utflyttningsposten men identifierad
  av mottagarhushållet. Ortens första led på623-hänvisningen är oläst.
  Skärmbilder bevarar originalets läsbara uppgifter; full-JPG overifierad.
- Revisit when: T-0058 ger identitetsbrygga eller konkret hinder, eller
  Olaus spärrade original på Kristinas sida åter blir åtkomligt.

## PCD-2026-09-05-009

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-007
- Owner: Sverker Adam Janson; Project Control utövar delegerat mandat
  enligt det aktiva kontinuerliga målet.
- Decision: Skapa T-0058 för Kyrkefallahushållet folio623 före
  utflyttningen1924 och högst en ytterligare explicit bakåthänvisning.
  Kör efter T-0056/T-0057. Inga fria födelseårssökningar eller vidare
  Mofallaanor medges; kandidatgränsen består tills identiteten bärs.
- Disposition: approved
- Resulting Wotan tasks: T-0058.
- Portfolio signal: Aktiv forskning på närmaste öppna generation;
  framsteg men ingen styrkt måluppfyllelse eller generell åtkomstspärr.
- Revisit when: Den avgränsade passagen ger resultat eller hinder.

## PCR-2026-09-05-008

- Record type: review
- Date: 2026-09-05
- Mode: checkpoint
- Trigger: T-0056–T-0058 ger senare flytt1941, rättad Andersfödelse och
  identifierat Kyrkefallahushåll1924; kvarvarande kö är åtkomstberoende.
- Control judgement: continue, preserve
- Current gate: Augusta saknar barndomsbrygga och egen död. Två
  konkreta fortsatt oprövade vägar finns; Olaus separata original hindrat.
- Recommendation: Pröva först Vämb/Bergshamra1941 genom mottagande
  original och högst en direkt senare döds-/flytthänvisning (T-0059).
  Pröva därefter en föregående Kyrkefallabok för den identifierade
  familjen och högst en explicit bakåthänvisning (T-0060). Behåll Olaus
  T-0051:s återstart; skapa inte om analogt spärrat arbete. Att stanna
  eller driva nya djup6-föräldrar vidare skulle lämna närmare genomförbara
  livs- och identitetsfrågor oprövade. Ingen bred extern omvärldssökning
  behövs för detta beslut; de nya personbundna originalnycklarna styr.
- Owner decision required: none; uttryckligen delegerat kontinuerligt mandat.
- Evidence: C-0871–C-0873, batch286–288, T-0051/T-0054/T-0056–T-0058,
  NORTH-STAR.md och målindikator30/32 på djup5 (inte uppfyllelsebevis).
- Uncertainty: Mofallakandidaten förblir obunden. Folio623 saknar explicit
  äldre fält; tidigare bok måste identifieras via tids-, orts- och
  familjesamband, inte antaget konstant sidnummer. Skärmbilder har begränsning.
- Revisit when: T-0059/T-0060 ger resultat eller hinder, eller Olaus
  original blir åtkomligt. Revidera återstående källkrav före djupare forskning.

## PCD-2026-09-05-010

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-008
- Owner: Sverker Adam Janson; Project Control utövar delegerat mandat
  enligt det aktiva kontinuerliga målet.
- Decision: Genomför T-0059 och T-0060 i denna ordning och inom deras
  högst två positiva postpassager. Bevara kandidatgränser och alla
  äldre observationer. Olaus spärr väntar på konkret originalåtkomst;
  ingen beställning, meddelande, kontoköp, PDF, publicering eller Gitåtgärd.
- Disposition: approved
- Resulting Wotan tasks: T-0059, T-0060.
- Portfolio signal: Aktiv närmare forskning; målet ofullbordat och
  kvarstående beroenden är inte bevis för uttömda källor.
- Revisit when: Någon av passagerna ändrar kunskapsläget eller blir hindrad.


## PCD-2026-09-05-011

- Record type: decision
- Date:2026-09-05
- Owner: Sverker Adam Janson, uttrycklig instruktion.
- Decision: Agenten får inte titta på eller använda ArkivDigital.
  Förbudet omfattar även katalog- och alternativåtkomstkontroller.
  Ägarens inklistrade utdrag får jämföras lokalt; de ger inte åtkomstmandat.
- Disposition: approved, gäller omedelbart och tills ägaren ändrar beslutet.
- Evidence: Ägarens meddelande ”där får du inte titta”, följt av
  avgränsningen till Arne Godvig Janssons sista registerpost.
- Impact: T-0059:s historiska kontroll behålls som utförd observation,
  men ArkivDigital tas bort som tillåten återaktiveringsväg för agenten.
  T-0060:s pågående RA-arbete sparas inför ägarens lokala stickprov.
- Resulting Wotan tasks: inga nya; åtkomstregel för befintliga uppgifter.
- Revisit when: Ägaren uttryckligen ändrar åtkomstmandatet.


## PCR-2026-09-05-009

- Record type: review
- Date:2026-09-05
- Mode: checkpoint
- Trigger: Ägarens stickprov av endast den sista registerposten för
  Arne Godvig Jansson, följt av fråga om mantalslängder hos Riksarkivet
  och begäran om persistent projektläge inför sessionsbyte.
- Control judgement: preserve, evaluate
- Current gate: P-0003 har äldre Källbredd: KLAR, men stickprovet pekar på
  oprövade mantalsuppgifter för en materiell del av hans vuxna liv.
  Den äldre utgåvebedömningen bevisar inte NORTH-STAR:s fullständiga livsbild.
- Evidence supplied by owner: Inklistrat registerutdrag, inte agentbesök
  eller eget original. Svbef1950, genväg r1.p6142017; Arne Godvig Jansson,
  född1915-02-21 i Flen, gift1938-05-15, polerare, värnpliktsnr22-44-35,
  mantalsskriven Södertälje, Tranbäret1, Frödingsv15, fältnummer33.
  Tidigare mantal1948 Södertälje ”Ö omr stg452+mf”,1949 Tranbäret1.
  Angiven originalkälla: Mantalslängder1951,2828(1951),bild620/sida260.
  Länktips Flen C:8(1895–1915). Hushåll listar Maj Amalia samt de tre
  redan kända barnen; övriga sökträffar i ägarens meddelande är uteslutna.
  Registerutdraget är inte ett uttryckligt OWNER_CONFIRMED-beslut om varje fält.
- Local comparison: C-0008 belägger födelse i samma angivna födelsebok;
  C-0034 belägger vigsel1938-05-15 och polerare1938. C-0267 bevarar
  Frödingsvägen15 i Jan-Christers minnen, inte mantalskontroll1950.
  Exakt1951-längd, fastighets-/mantalsuppgifter1948–1949 och
  värnpliktsnummer hittades inte i projektets Markdownunderlag.
  Hushållet1950 är inte tidigare verifierat genom den nämnda längden.
- Access discovery: MCP search_metadata, keyword=Södertälje mantalslängder,
  year_min=year_max=1951,offset0,limit8,only_digitised=false,dedup=false,
  gav serien SE/SSA/2896P/F I aa, Kronokamreraren i Södertälje,
  förvarad Stockholms stadsarkiv:
  https://sok.riksarkivet.se/arkiv/6OTWuHRXzYBI0H4FMqzIY9.
  Även en ovidkommande äldre volym returnerades trots årsfiltret; filtreringen
  belägger därför inte1951-täckning. Exakt referenskodsfråga med mellanslag
  gav noll; endast frågeutfall. Webbläsningsverktygets öppning av serien
  avvisades som ”not safe to open (non-retryable error)”; inget innehåll läst
  där och ingen omväg prövad efter beskedet. Digital1951-åtkomst overifierad.
- General access evidence: Riksarkivet anger digitala mantalslängder bland
  sitt tillgängliga material, men endast delar av beståndet är digitaliserade:
  https://riksarkivet.se/utforska-och-bestall/sok-i-arkiv-och-samlingar/borja-forska-i-arkiven/vad-finns-online.
  Detta belägger inte att Arnes1951-post är digital hos RA.
- Recommendation: Pröva en separat bounded mantalspassage för Arne via
  tillåtna arkiv och omvärdera berörd källbredd mot NORTH-STAR. Bevara först
  T-0060:s exakta pågående punkt; utvidga inte den uppgiften med Arne.
  Att enbart behålla KLAR och kalla denna konkreta källa valfri berikning
  skulle lämna ägarens sakligt relevanta stickprov obesvarat.
- Owner decision required: Ingen ny generell mandatfråga; operativ styrning
  är delegerad. Ny uppgift och ändring av källbreddsstatus är ännu inte
  genomförda eftersom ägaren begärde sessionsförberedelse innan dess.
- Resulting Wotan tasks: none; ingen extra startlista eller handover skapas.
- Revisit when: Nästa styrbedömning efter återupptagning av T-0060 eller
  ägarens fortsatta stickprov. Skapa då avgränsad uppgift före personforskning.
- Constraint: PCD-2026-09-05-011 förbjuder all agentåtkomst till ArkivDigital;
  kopierade utdrag ger inte tillstånd att besöka tjänsten. Inga beställningar.


## PCR-2026-09-05-010

- Record type: review
- Date:2026-09-05
- Mode: direction-review
- Trigger: Ägaren vill pröva en tydligare källstrategi efter Arne-stickprovet.
- Control judgement: evaluate, preserve
- Current gate: Skriven metod finns, men källval, källberoenden och
  administrativa avslut behöver prövas mot konkreta forskningsfrågor.
- Evidence: PCR-2026-09-05-009, P-0003:s Källbredd:KLAR, T-0057/C-0872,
  genealogy/README.md, research-plan.md, scripts/lib/genealogy-relations.mjs.
  Metodjämförelsen använde ICAPGens Research Logs (2018) och E.S.Mills
  Evidence Analysis: A Process Map, https://www.historicpathways.com/download/hpprocessmap.pdf.
- Recommendation: Begränsat tvåfallstest: prospektiv mantalsfråga för Arne
  och retrospektiv prövning av Anders födelsekonflikt. Skriv tydliga frågor,
  alternativ, källval, beroenden och slutsatser; utvärdera metodnyttan innan
  bred migrering. Den retrospektiva delen kan inte bevisa bättre sökprestanda.
- Owner decision required: none; ägaren har godkänt det begränsade testet.
- Revisit when: Testet har två dokumenterade utfall och jämförbar utvärdering.

## PCD-2026-09-05-012

- Record type: decision
- Date:2026-09-05
- Decides review: PCR-2026-09-05-010
- Owner: Sverker Adam Janson, ”ok gör ett sådant begränsat test”.
- Decision: Genomför T-0061 med Arne och Anders som två begränsade fall.
  Det får företräde framför T-0060, vars checkpoint bevaras. Ingen fortsatt
  kökörning efter testet utan att testresultatet först redovisas.
- Disposition: approved
- Resulting Wotan tasks: T-0061
- Portfolio signal: Metodtest på verkligt material; fullständighetsmålet kvar.
- Revisit when: T-0061 redovisar resultat, begränsningar och rekommendation.


## PCR-2026-09-05-011

- Record type: review
- Date: 2026-09-05
- Mode: evaluation
- Trigger: Det av ägaren godkända tvåfallstestet T-0061 har utförts.
- Control judgement: evaluate, preserve
- Evidence: genealogy/source-strategy-pilot-2026-09-05.md; C-0876/S-0688
  med två inloggat bekräftade läsesalsvolymer; C-0877 med sju återlästa
  original och kvalificerad avläsningskonflikt; batch 291.
- Result: Arnes mantalsfråga fortfarande öppen trots avslutat katalogprov.
  Källbredd KLAR omprövad till PÅGÅR inom pilotens mandat. Anders
  födelseidentitet består; säker originalavvikelse ersätts i aktuell
  bedömning av olöst 14/16-avläsning. Inga identiteter/kanter ändrade.
- Recommendation: Använd en kort fråga–källval–beroende–slutsats–återstart
  i nästa godkända avgränsade uppgift. Inför inte generell datamigrering,
  nya statusar eller stor källtaxonomi på grundval av två fall. En eventuell
  maskinell identitetsgrind behöver separat prövning, inklusive reglerna
  för OWNER_CONFIRMED.
- Limits: Retrospektiva Andersfallet var inte blint eller oberoende.
  Ingen tidsvinst, fullständig källuttömning eller GPS-certifiering visad.
- Owner decision required: none för leveransen; redovisa resultatet innan
  vidare kökörning enligt PCD-2026-09-05-012.
- Resulting Wotan tasks: none; T-0061 avslutas efter kontroller. T-0060:s
  återupptagningspunkt är bevarad, inte utförd i piloten.
- Revisit when: En senare styrbedömning väljer fortsatt rutinanvändning
  eller avgränsat implementeringsarbete; beakta Arnes återöppnade
  närmare källbreddsfråga före ny djupare forskning.


## PCR-2026-09-05-012

- Record type: review
- Date: 2026-09-05
- Mode: direction-review
- Trigger: Ägaren vill att hela analysen av trädbyggande, effektiv källordning
  och systematisk komplettering av alla personakter implementeras beständigt
  och kan genomföras efter kontextkompaktering utan stöd av chatthistorik.
- Control judgement: redirect, operate, preserve
- Current gate: Befintliga styrfiler har bred ambition men svagare operativa
  slutkrav. Äldre GRANSKAD/KLAR, generella källceller och isolerade frågor
  visar inte hela livsbildens täckning eller vilka fynd som öppnar nästa källa.
  Samma brist gäller nya, halvfärdiga, röriga och tidigare avslutade akter.
- Evidence: NORTH-STAR.md; genealogy/research-plan.md; genealogy/README.md;
  genealogy/source-coverage.md; genealogy/templates/person.md;
  genealogy/source-strategy-pilot-2026-09-05.md; T-0060/T-0061;
  scripts/goal-state.mjs och scripts/lib/genealogy-relations.mjs.
  Baslinje: 528 personer, 2793 påståenden; registrerat djup 2 efter Arnes
  återöppnade källbredd, utan ändrad antavla. Metodkällor och exakta
  begränsningar bevaras i genealogy/source-strategy.md.
- Alternatives considered: Enbart längre metodtext skulle inte synliggöra
  alla äldre akters bedömningsluckor eller skapa utförbar ordning. Automatisk
  masskonvertering av gamla KLAR skulle sakna saklig grund. Omedelbar full
  omforskning av 528 personer skulle upprepa tillräckligt arbete och överskrida
  den beställda styrimplementationen. Välj fullständigt program/kontrakt,
  gemensam källkatalog, individuella profiler, heltäckande strukturell
  inventering och stegvis sakligt införande i ändliga Wotan-kohorter.
- Recommendation: Inför PK-01–12, tio obligatoriskt bedömda livsteman och
  källvägar med söknycklar/beroenden/åtkomst/omfång. Skilj källobservation,
  bevisargument, personmodell och utförandestatus. Gör upptäcktskontroller
  för okända spår och ompröva följdvägar efter fynd. Utvärdera träd och
  livsbild separat inom varje balanserad generationsvåg. Återanvänd gammal
  forskning och bevara osäkra identiteter, ägarkunskap och källhistorik.
- Revises review: PCR-2026-09-05-011:s försiktiga rekommendation om ingen
  bred implementering på grundval av två fall. Det nya beslutet bygger på
  ägarens uttryckliga bredare mål och analys, inte på påstådd pilotbevisad
  tidsvinst eller certifierad bevisning.
- Owner decision required: none; ägaren har uttryckligen beställt full
  implementation i styrfiler, Wotan och vid behov skärpt north star.
- Resulting Wotan tasks: T-0062 implementation, T-0063 närmaste fasta
  införandekohort och T-0064 Arnes avgränsade bostads-/arbetsfrågor.
  T-0060 bevaras med sida 531/bild 261 och uttryckligt ändrade föregångare.
- Revisit when: T-0063:s sexton individuella utfall och T-0064:s faktiska
  källresultat finns, vid upptäckt av närmare identitetsrisk/livslucka eller
  när inventeringen visar att en persongrupp annars faller ur arbetsordningen.

## PCD-2026-09-05-013

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-012
- Owner: Sverker Adam Janson
- Evidence supplied by owner: ”vi måste nu gå vidare och implementera denna
  ansats i sin helhet i styrfiler och wotan och förmodligen också med en
  skärpning av north star”; dokumenten ska stå på egna ben, fungera för nya,
  halvfärdiga och röriga personakter och ge mycket tydliga krav på slutresultatet.
- Decision: Genomför hela styrimplementationen nu. North star konkretiseras
  genom PK-01–12, tio livsteman, bred relevansstyrd källstrategi och effektiv
  ordning där tidiga fynd öppnar fortsatt forskning. Samma resultatkrav
  gäller alla personakter. Trädsäkerhet, livsbild, källtäckning och task-DONE
  bedöms separat. Skapa beständiga mallar, synlig inventering av alla P-id:n,
  relevanta kontroller och ändliga Wotan-uppgifter för fortsatt tillämpning.
- Disposition: approved
- Implementation judgement within mandate: T-0062 har företräde framför
  pågående personforskning. T-0063 inför kontraktet i sönernas två akter och
  de fjorton närmaste personerna på djup 1–3 med befintliga underlag och
  integritetsminimering. T-0064 prövar Arnes bostads-/arbetsnycklar 1943–1951.
  T-0060 inväntar dem, behåller sitt ursprungliga sakomfång och sin exakta
  olästa punkt. Vid nya närmare materiella behov ska kö/beroenden omprövas
  uttryckligen innan djupare arbete återupptas. Resterande personer kvarstår
  i inventeringen och återtas enligt programmets kohort- och balansregel.
- Preserved constraints: Append-only evidens; reviserbar personmodell;
  OWNER_CONFIRMED; inga osäkra propagerande identiteter; opportunistisk
  relevant personutvinning och minimering för levande; Riksarkivets
  åtkomstordning; sparat återupptagningsläge vid utloggning; absolut förbud
  mot agentåtkomst till ArkivDigital enligt PCD-2026-09-05-011. Inga nya
  beställnings-, kontakt-, publicerings-, PDF- eller commit/push-medgivanden.
- Supersedes decision: PCD-2026-09-05-012:s tillfälliga ordning för pilotens
  företräde ersätts efter redovisat test av den nu beslutade ordningen.
  Pilotens avgränsning och resultat består som historik. Äldre utgåve-KLAR
  är inte ett undantag från de nya resultatkraven; giltiga fakta består.
- Resulting Wotan tasks: T-0062, T-0063, T-0064; T-0060:s checkpoint
  bevarad och beroenden uppdaterade. T-0051/T-0054:s sakomfång består.
- Portfolio signal: Aktiv styrimplementation följd av explicit avgränsat
  sakligt införande. Denna beställning innebär inte att alla personakter
  redan har omforskats eller att en obegränsad forskningskörning startar nu.
- Revisit when: Första införandekohorten och källpassagen är sakligt
  utvärderade, nya söknycklar ändrar ordningen eller äldre akter riskerar
  att förbli obearbetade trots programmets återkommande revisioner.

## PCR-2026-09-05-013

- Record type: review
- Date: 2026-09-05
- Mode: direction-review
- Trigger: Ägaren preciserar dashboardens uppdateringsregel under beställd
  commit/push av det persistenta projektläget.
- Control judgement: operate, preserve
- Evidence: dashboard/package.json hade automatisk datagenerering före
  dev/build/test; scripts/dashboard-data.test.mjs krävde aktuella filantal och
  aktuell Wotan-uppgift. Detta tvingade fram en uppdatering vid förkontrollen.
- Recommendation: Ta bort automatiska uppdateringar och skilj test av sparad
  ögonblicksbild från uttrycklig aktualitetskontroll. Behåll kanoniska filer och
  Wotan som aktuellt projekttillstånd. Ändra inte forskningskön.
- Owner decision required: none; ägarens uttryckliga instruktion nedan styr.
- Resulting Wotan tasks: none; begränsad rättelse under versionssäkringen,
  dokumenterad i T-0062:s avslutande uppföljning.
- Revisit when: Ägaren uttryckligen beställer en dashboarduppdatering eller
  ändrar denna regel.

## PCD-2026-09-05-014

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-013
- Owner: Sverker Adam Janson
- Evidence supplied by owner: ”dashboarden skall bara uppdateras när jag
  explicit ber om det”. Föregående begäran var ”är vårt projekttillstånd
  persistent? committa och pusha”.
- Decision: Dashboarden, inklusive genererade data, uppdateras enbart på
  uttrycklig beställning. Forskning, task-DONE, test, bygge, sessionsbevarande
  och commit/push medför ingen sådan beställning. Ordinarie kontroller måste
  acceptera en äldre internt konsistent snapshot. Särskild aktualitetskontroll
  används efter en beställd uppdatering. Commit/push av det samlade sparade
  projektläget är uttryckligen auktoriserat och ska slutföras.
- Disposition: approved
- Implementation: AGENTS.md, README.md, wotan/README.md, dashboard/README.md,
  npm-kommandon och regressionstester. Den dashboarduppdatering som redan
  gjordes före denna instruktion bevaras; ingen ny generering görs.
- Preserved constraints: Kanoniska personakter, evidens och Wotan styr fortsatt
  arbete. Forskningsinventering och mediemanifest behåller sina aktualitetskrav.
  Ingen ny publicering/deploy av dashboarden beställs.
- Resulting Wotan tasks: none; T-0063 är fortsatt nästa READY.
- Revisit when: Ny uttrycklig dashboardbeställning; endast ändrat ägarbeslut
  ersätter regeln om att uppdateringar kräver uttrycklig begäran.

## PCD-2026-09-05-015

- Record type: decision
- Date: 2026-09-05
- Decides review: direkt ägarinstruktion efter automatisk avvisning av push
- Owner: Sverker Adam Janson
- Evidence supplied by owner: ”jag godkänner”, efter uttrycklig information om
  att granskningen krävde godkännande av hela commiten inklusive minimerade
  uppgifter om levande personer till det publika GitHub-repot.
- Decision: Godkänn push av hela det committade projektläget, inklusive
  minimerade uppgifter om levande personer och källmedier via Git LFS, till
  publika `rekrevs/slaktforsk`, befintlig origin/main. Innehållscommit c499b54
  och tillhörande bevarande-/auktorisationsanteckningar omfattas.
- Disposition: approved
- Related records: PCD-2026-09-04-007, PCD-2026-09-05-014, T-0062
- Resulting Wotan tasks: none; slutför den redan beställda versionssäkringen.
- Preserved constraints: Dashboarden uppdateras fortsatt endast på separat
  uttrycklig begäran. Ingen dashboard-deploy eller ny forskningskörning beställs.
- Revisit when: Payload eller destination ändras materiellt eller ägaren
  ändrar publiceringsbeslutet.

## PCR-2026-09-05-014

- Record type: review
- Date: 2026-09-05
- Mode: checkpoint
- Trigger: T-0063 har infört personkontraktet i de sexton närmaste akterna
  och lämnar en utfallsbedömning med nya närmare materiella behov på båda
  sidor; enligt PCD-2026-09-05-013 ska kö och beroenden då omprövas
  uttryckligen innan djupare arbete återupptas.
- Control judgement: continue, operate, preserve
- Current gate: Sju levande personer är GODKÄND inom integritetsminimerat
  omfång. Nio avlidna på djup 2–3 är UNDERKÄND med prövad identitet men
  oprövade genomförbara livsbildsvägar; deras äldre KLAR är omprövad till
  PÅGÅR, varför det registrerade gemensamma djupet sjunker från 2 till 1.
  Ingen relation eller observation har ändrats. Måttet speglar nu
  north stars krav på livsbilder, inte ett nytt sakligt problem.
- Evidence: `genealogy/research-log/2026-09-05.md` batch 292; sexton
  profiler i `genealogy/research-profiles/`; `node scripts/research-inventory.mjs`
  (16 profiler, 7 GODKÄND, 0 strukturfel); `node scripts/goal-state.mjs`;
  `wotan/dev-log/T-0063.md`.
- Options considered: fortsätta direkt till djup 4-införande (skulle bryta
  närhetsregeln när kända olästa sidor och fria SCB-passager finns för djup
  2–3); en enda stor forskningsuppgift för alla nio (skulle bli en behållare);
  balanserade M-uppgifter per sida före nästa införandegrupp.
- Recommendation: Behåll T-0064 som första körbara uppgift. Skapa T-0065
  (Kristinas sida: SCB-utdrag och folkräkning 1930 för Höök/Henriksson
  1903–1944, inklusive Gunnars rapporterande församling) och T-0066
  (Sverkers sida: Oskar/Ebba 1909–1997) som READY efter T-0063, T-0067
  (Arne/Maj: Flen s. 860, utflyttning 1943, grav, namnärende) efter T-0064,
  och T-0068 (djup 4-införande, sexton personer) efter T-0065–T-0067. Låt
  obeslutade katalogvägar (missionsarkiv/biografier om paret Höök,
  läkar-/seminariematriklar, frikyrkoarkiv, inskrivningsrullor,
  företagsregister) förbli EJ BESLUTAT UTFÖRANDE tills de närmare
  passagerna är klara. T-0060 behåller sina beroenden.
- Owner decision required: none; inom det delegerade operativa mandatet i
  PCD-2026-09-04-002 och PCD-2026-09-05-013.
- Uncertainty: SCB-utdragens och församlingsböckernas digitala täckning för
  1930–1949 kan variera per församling; noll i kandidatförsamlingar är ett
  avgränsat noll, inte frånvarobevis. Gunnars vuxenliv beror på ägaruppgift.
- Revisit when: T-0064–T-0067 är verifierade och T-0068 ska starta; en
  bärande identitet blir osäker; ett externt åtkomsthinder stoppar en hel
  sida.

## PCD-2026-09-05-016

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-014
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt PCD-2026-09-04-002 och PCD-2026-09-05-013 under det pågående
  kontinuerliga målet.
- Decision: Genomför rekommendationen. Registrera T-0065–T-0068 med angivna
  beroenden; kör T-0064 först, därefter T-0065 och T-0066 balanserat, sedan
  T-0067 och först därefter T-0068. Bevara omprövningen KLAR→PÅGÅR med
  historik och godta att det registrerade djupet sjunker.
- Disposition: approved
- Supersedes decision: none; verkställer PCD-2026-09-05-013:s kohort- och
  närhetsregel efter första införandekohorten.
- Related records: PCR-2026-09-05-014, PCD-2026-09-05-013,
  `wotan/dev-log/T-0063.md`, `wotan/dev-log/T-0065.md`–`T-0068.md`
- Resulting Wotan tasks: T-0065, T-0066, T-0067, T-0068; T-0064 READY.
- Portfolio signal: Projektet är aktivt och ofullbordat; närmaste
  generationers livsbilder har konkreta körbara passager på båda sidor.
  Inga beställningar, publicering, PDF, dashboarduppdatering eller commit/push
  följer av detta beslut.
- Revisit when: T-0064–T-0067 verifierade; T-0068 ska öppnas; nytt
  ägarbesked om Gunnar Hööks liv eller Hillevis namnform.

## PCR-2026-09-05-015

- Record type: review
- Date: 2026-09-05
- Mode: checkpoint
- Trigger: Den kontinuerliga målkörningen har efter T-0063 kört T-0064,
  T-0066 och T-0065 så långt fri åtkomst medger. Alla tre är nu BLOCKED på
  samma externa hinder: Riksarkivets bilder från 1910-talet och framåt ger
  `401` utan inloggad session, folkräkningen 1930 möter människoverifiering,
  och Claude-in-Chrome-tillägget är inte anslutet i sessionen, så metodens
  inloggade reserv kan inte användas. Riksarkivets MCP saknas också.
- Control judgement: wait, preserve
- Current gate: Inloggad bildåtkomst. Inget annat körbart arbete återstår i
  kön: T-0067 och T-0068 väntar på föregångare enligt beslutad ordning,
  T-0060/T-0051/T-0054 har egna äldre hinder, IDEA-spåren är parkerade.
- Evidence: batch 293–295; S-0689–S-0692; C-0878–C-0880; dev-loggarna
  T-0064–T-0066 med exakta återupptagningspunkter; `node scripts/goal-state.mjs`.
- Results within the run: Södertälje kyrkoarkivs digitaliserade mantals-,
  kvarters- och adressregister 1936–1955 identifierade som ny väg för Arne;
  Oskars och Ebbas död och grav belagda (Burträsk BT 08 13, 1963 och 1997);
  Ivars födelsenotis 1903 läst med fri åtkomst. Registrerat gemensamt djup
  är oförändrat 1; inga identiteter eller relationer ändrade.
- Options considered: öppna T-0068 (djup 4-införande, lokalt arbete utan
  bildåtkomst) trots att dess föregångare är blockerade; fortsätta med
  katalogarbete för djupare skivor; eller pausa. Att kringgå den beslutade
  ordningen skulle upprepa mönstret att djupare arbete tränger undan
  närmare, och katalogarbete utan läsning ger liten kunskapsvinst nu.
- Recommendation: Pausa målkörningen med målet redovisat som ofullbordat.
  Återstart: ägaren ansluter Claude-in-Chrome och loggar in hos Riksarkivet
  (eller gör Riksarkivets MCP med bildvisning tillgänglig); därefter återupptas
  T-0064, T-0066 och T-0065 från sina sparade passager i den ordningen.
  Om hindret kvarstår länge får Project Control ompröva om T-0068 ska
  släppas fram som rent lokalt arbete.
- Owner decision required: none för pausen; åtkomståtgärden är ägarens.
- Revisit when: Inloggad bildåtkomst finns, eller ägaren väljer att släppa
  T-0068 före de blockerade passagerna.

## PCD-2026-09-05-017

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-015
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt PCD-2026-09-04-002 och PCD-2026-09-05-013.
- Decision: Pausa den kontinuerliga målkörningen vid det konkreta externa
  hindret. Bevara T-0064, T-0065 och T-0066 som BLOCKED med exakta
  återupptagningspunkter; T-0067 och T-0068 behåller sina beroenden. North
  star är inte uppfylld; ingen avslutningsrevision görs.
- Disposition: approved
- Supersedes decision: none.
- Related records: PCR-2026-09-05-015, PCD-2026-09-05-016, PCD-2026-09-05-006
- Resulting Wotan tasks: none nya.
- Portfolio signal: Projektet är aktivt och ofullbordat; nästa framsteg beror
  på ägarens åtkomståtgärd. Inga beställningar, publicering, PDF,
  dashboarduppdatering eller commit/push följer av detta beslut.
- Revisit when: Åtkomsten är återställd eller ägaren ändrar ordningen.

## PCR-2026-09-05-016

- Record type: review
- Date: 2026-09-05
- Mode: checkpoint
- Trigger: Riksarkivets MCP är nu tillgänglig men häver inte inloggningskravet
  (batch 296); Chrome-tillägget ansluts fortfarande inte. T-0064–T-0066
  är BLOCKED på samma externa hinder. Det kontinuerliga målet gäller.
- Control judgement: continue, operate, preserve
- Current gate: Bildpassagerna kräver ägarens åtgärd. Övrigt arbete som för
  north star framåt utan bildåtkomst är kontraktsinförandet för djup 4
  (T-0068), som PCD-2026-09-05-016 lade efter T-0065–T-0067 av
  närhetsskäl.
- Options considered: fortsatt paus (ingen framdrift medan hindret består);
  släppa T-0068 nu (lokalt arbete ur befintliga akter, ingen konkurrens om
  bildåtkomst); nya katalogsvep för djupare skivor (lågt värde).
- Recommendation: Släpp T-0068 nu. Närhetsregeln syftar till att hindra att
  djupare forskning tränger undan närmare; här är de närmare passagerna
  externt blockerade, inte bortprioriterade, och T-0068 gör inga
  källpassager. T-0064–T-0066 återupptas före T-0068:s följdarbete så snart
  åtkomsten finns. Ändra T-0068:s beroende till enbart T-0063 och notera
  ändringen i dev-loggen.
- Owner decision required: none; wotan/README.md anger att en blockerad
  uppgift inte stoppar andra körbara uppgifter och att annat godkänt
  avgränsat arbete fortsätter under väntan.
- Evidence: batch 296; T-0064–T-0066 dev-loggar; `wotan/README.md`
  (Kökörning och kontinuerligt uppfyllelsemål); PCD-2026-09-05-016.
- Revisit when: Bildåtkomsten är återställd (återgå till T-0064 först), eller
  T-0068 är verifierad.

## PCD-2026-09-05-018

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-016
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt PCD-2026-09-04-002 och PCD-2026-09-05-013.
- Decision: Släpp T-0068 nu med beroende endast på T-0063. T-0064–T-0066
  behåller sina sparade passager och företräde framför T-0068:s följdarbete
  när bildåtkomst finns. PCD-2026-09-05-017:s paus ersätts av fortsatt
  lokalt arbete.
- Disposition: approved
- Supersedes decision: PCD-2026-09-05-017 (pausen) och PCD-2026-09-05-016
  endast i fråga om T-0068:s ordningsberoende.
- Related records: PCR-2026-09-05-016, PCD-2026-09-05-006
- Resulting Wotan tasks: T-0068 READY.
- Portfolio signal: Projektet är aktivt; bildpassagerna väntar på ägarens
  åtkomståtgärd medan livsbildsinförandet fortsätter lokalt.
- Revisit when: T-0068 verifierad eller åtkomsten återställd.

## PCR-2026-09-05-017

- Record type: review
- Date: 2026-09-05
- Mode: checkpoint
- Trigger: T-0068 har infört personkontraktet i djup 4-kohorten (batch 297)
  och visar att ett flertal materiella vägar på djup 2–4 inte kräver
  inloggning: gravregister, kyrkoböcker före omkring 1905, SCB-batcher före
  1918 (att pröva), lokal omläsning och MCP-katalogkontroller.
- Control judgement: continue, operate, preserve
- Current gate: Inloggad bildåtkomst saknas fortfarande för 1910+.
- Recommendation: Kör ett ändligt fritt svep (T-0069, M) över dessa vägar
  balanserat mellan sidorna innan djup 5-införandet (T-0070, L). När
  åtkomsten återställs återupptas T-0064–T-0066 före T-0070:s följdarbete.
- Owner decision required: none; inom delegerat mandat.
- Evidence: batch 297; 32 profiler; `node scripts/research-inventory.mjs`
  (32 profiler, 7 GODKÄND, 0 strukturfel); `wotan/dev-log/T-0068.md`.
- Revisit when: T-0069 verifierad; åtkomst återställd.

## PCD-2026-09-05-019

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-017
- Owner: Sverker Adam Janson; operativt mandat utövat genom Project Control
  enligt PCD-2026-09-04-002 och PCD-2026-09-05-013.
- Decision: Registrera T-0069 READY efter T-0068 och T-0070 BLOCKED efter
  T-0069. Bevara T-0064–T-0066:s företräde vid återställd åtkomst.
- Disposition: approved
- Supersedes decision: none; verkställer närhetsregeln.
- Related records: PCR-2026-09-05-017, PCD-2026-09-05-018
- Resulting Wotan tasks: T-0069, T-0070.
- Portfolio signal: Aktivt; lokala och fria passager fortsätter medan
  bildåtkomsten väntar. Inga beställningar, publicering, PDF,
  dashboarduppdatering eller commit/push.
- Revisit when: T-0069 verifierad eller åtkomst återställd.

## PCR-2026-09-05-018

- Record type: review
- Date: 2026-09-05
- Requested by: agent under det kontinuerliga målet
- Trigger: Ägaren skrev i chatten att han själv löst captchan på
  sok.riksarkivet.se ("jag har svarat på en captcha på riksarkivet igen så
  den skall vara öppen"). Den captcha-spärrade personsökningen i
  folkräkningen 1930 hörde till T-0065:s passage och låg kvar som följdväg i
  T-0072 (IDEA). Sessionen är tidsbegränsad.
- Options considered: vänta tills T-0072 formellt aktiveras (risk att
  sessionen stängs); använda sessionen omedelbart för den avgränsade
  sökningen och bokföra i T-0072; avstå.
- Recommendation: Använd sessionen omedelbart för den avgränsade
  sökningen (Henriksson/Larsson 1930, kontroll Höök), bokför som batch 302
  under T-0072 och sätt T-0072 READY. Agenten löser aldrig captchan själv
  (PCD-2026-09-05-011-villkoren oförändrade).

## PCD-2026-09-05-020

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-018
- Owner: Sverker Adam Janson; ägarens direkta chattbesked om den lösta
  captchan, operativt tillämpat genom Project Control enligt PCD-2026-09-04-002.
- Decision: Genomför rekommendationen. Batch 302 bokförs i T-0072, som
  blir READY efter T-0067. Ägarens egen captcha-lösning är den enda
  tillåtna vägen in i captcha-skyddade söktjänster; agenten ber om den vid
  behov och löser den aldrig själv.
- Related records: PCD-2026-09-05-011, PCD-2026-09-05-018, PCD-2026-09-05-019.
- Resulting Wotan tasks: T-0072 READY (batch 302 utförd i förväg); T-0074 IDEA
  (följdvägar från T-0067).
- Portfolio signal: T-0064–T-0067 DONE i inloggad session; kön fortsätter
  med T-0069 (fritt svep) före T-0070 (djup 5).
- Revisit when: T-0069 är DONE eller ägaren ändrar ordningen.

## PCR-2026-09-05-019

- Record type: review
- Date: 2026-09-05
- Requested by: ägaren, direkt fråga i chatten ("skall vi inte ändra t-0064
  mm till ongoing eftersom de inte är fullföljda?")
- Trigger: T-0064–T-0067 sattes DONE efter genomförd forskningsläsning, men
  fulloriginalen till C-0882–C-0900 är inte speglade i `genealogy/media/`.
  Alla tidigare positiva läsningar i projektet har lokal källbild; posterna
  har därför verifierbar men inte självbärande provenans.
- Options considered: låta uppgifterna stå DONE och lägga speglingen i en ny
  uppgift (obligationen lossnar från den passage som skapade den, och
  DONE-räkningen överdriver läget); sätta dem ONGOING (fel token — arbetet
  kan inte drivas vidare av agenten); sätta dem BLOCKED med exakt hinder.
- Recommendation: BLOCKED. Kontrollmätning 2026-09-05 visar 401 anonymt för
  samtliga 58 bild-id, och de tre alternativa uthämtningsvägarna är prövade
  och uteslutna, så villkoret är en ägaråtgärd — vilket är definitionen av
  BLOCKED i denna konvention.

## PCD-2026-09-05-021

- Record type: decision
- Date: 2026-09-05
- Decides review: PCR-2026-09-05-019
- Owner: Sverker Adam Janson; direkt invändning i chatten.
- Decision: Genomför rekommendationen. T-0064, T-0065, T-0066 och T-0067
  återgår till BLOCKED med identiskt formulerat hinder och exakt
  återupptagningssteg; T-0072 blir BLOCKED på beroendet. Det uppfyllda
  forskningsinnehållet står kvar i Outcome, och acceptanskriteriet om
  C-poster med original och SHA-256 är avbockat igen. Principen som
  fastställs: lokal källbild ingår i evidenskontraktet för en positiv
  läsning, och en uppgift som saknar den är inte fullföljd även om
  bild-id och SHA-256 är fjärrverifierade.
- Related records: PCD-2026-09-05-013, PCD-2026-09-05-020.
- Resulting Wotan tasks: inga nya; T-0069 kvarstår ONGOING och är den enda
  uppgift som kan drivas vidare utan ägaråtgärd.
- Portfolio signal: fem uppgifter väntar nu på en och samma ägaråtgärd
  (läsrätt till en nedladdningskatalog). Det är projektets enskilt största
  flaskhals just nu.
- Revisit when: nedladdningsvägen är löst, eller ägaren beslutar att
  fjärrverifierad SHA-256 räcker som provenans för inloggade bilder.

## PCD-2026-09-06-001

- Record type: decision
- Date: 2026-09-06
- Decides review: PCR-2026-09-05-019 (uppföljning av PCD-2026-09-05-021)
- Owner: Sverker Adam Janson; uppdrag i chatten att lösa de två föreslagna
  ägaråtgärderna.
- Decision: Ingen av åtgärderna behövdes. Fulloriginalen är speglade genom en
  uthämtningsväg inom sidans egen policy (formulärpost; `form-action` saknas
  och ärver inte från `default-src`), med ägarens befintliga session och utan
  ändring i Chrome eller macOS. T-0064–T-0067 återgår till DONE och T-0072
  till READY. Principen i PCD-2026-09-05-021 står fast: lokal källbild ingår i
  evidenskontraktet — den är nu uppfylld i stället för efterskänkt.
- Related records: PCD-2026-09-05-021, PCD-2026-09-05-011.
- Resulting Wotan tasks: inga nya; T-0069 fortsätter som ONGOING.
- Portfolio signal: flaskhalsen som blockerade fem uppgifter finns inte
  längre; framtida inloggningsberoende läsningar kan speglas direkt.
- Revisit when: Riksarkivet ändrar sin CSP eller bildtjänstens åtkomstmodell.

## PCR-2026-09-06-002

- Record type: review
- Date: 2026-09-06
- Mode: direction-review
- Requested by: ägaren ("kör") efter inventeringen av kvarstående arbete
- Trigger: Speglingsvägen i batch 304 och den inloggade sessionen hävde ett
  hinder som pausat ett dussin källvägar. Frågan är vad detta bör betyda för
  riktningen, inte bara för kön.

### Kontrolläge

- Värdet projektet skapar: en balanserad, källförankrad släkthistoria med två
  samtidiga resultatkrav — antavla och livsbild för varje identifierad person.
- Vad arbetet nyligen faktiskt fastställde: Södertäljekedjan 1943–1947,
  Zingmark/Andersson 1910–1950, Ivars utresa till Kashgar 1931, Flen s. 860
  och uppslag 720, samt Carlman i Kalmar 1930. Fyrtioen fulloriginal är
  speglade med verifierad SHA-256, vilket stärker uppfyllelsevillkor 5.
- Antaganden som ändrats: att inloggningsskyddade bilder inte kunde speglas
  lokalt visade sig falskt (`form-action` saknas i sidans CSP). Att paret
  Henriksson skulle finnas i folkräkningen 1930 visade sig falskt — nationellt
  indexnoll. Att Gunnar Hööks födelse rapporterades i en svensk församling
  1933 är försvagat: fem utdrag är nollprövade och fadern var utrest.
- Den begränsande grinden: **P-0212 Gunnar Ivar Emanuel Höök.** `goal-state`
  registrerar gemensamt djup 1; djup 2 kräver att han blir källbredd-klar och
  han är den enda som saknas. Det nyöppnade dussinet källvägar ligger på djup
  3–4 och flyttar därför inte djupindikatorn.
- Missförhållande mellan aktivitet och kunskapsvärde: nej. Sex batcher gav
  materiella fynd, inte bara fler anteckningar.
- Ägarägda grindar: P-0212/KP-03 (ägarens familjekunskap om Gunnars liv
  1933–2017) och T-0051:s ALTCHA-skyddade katalog.

### Bedömning

Riktningen är fortsatt rätt. Två saker bör dock inte behandlas lika: det
nyöppnade breddarbetet på djup 3–4 tjänar uppfyllelsevillkor 2, medan
djupindikatorn hänger på en enda person vars avgörande källväg redan ligger i
T-0072. North star förbjuder uttryckligen att biografiska luckor skjuts undan
av nya anor, så breddarbetet ska inte köas bakom djup 5 — men det ska heller
inte tränga undan den enda uppgift som kan flytta djupmåttet.

Alternativ som övervägdes: (a) en enda stor uppgift för hela den nyöppnade
ytan — avvisad, den blir obegränsad och bryter mot kravet på avgränsat omfång;
(b) köa allt bakom T-0070 djup 5 — avvisad, strider mot närhetsregeln;
(c) dela i en djupkritisk väg och två balanserade breddspår plus en
evidensåtgärd — vald.

## PCD-2026-09-06-002

- Record type: decision
- Date: 2026-09-06
- Decides review: PCR-2026-09-06-002
- Owner: Sverker Adam Janson; uppdrag i chatten att genomföra styrgenomgången,
  inom det delegerade mandatet enligt det pågående kontinuerliga målet.
- Decision: Fortsätt, med prioritetsordning. T-0069 avslutas först eftersom
  den är ONGOING och har nedladdat material oläst. Därefter T-0072, som nu
  uttryckligen bär djupindikatorn genom P-0212. Därefter T-0075 och T-0076,
  som delar den nyöppnade ytan i en balanserad passage per sida. T-0077 är
  en liten evidensåtgärd som kan läggas in när som helst. T-0060 återgår till
  READY eftersom dess åtkomsthinder är hävt och dess företrädesskäl upphört.
  T-0051:s blockering omformuleras till en ägarägd grind i stället för ett
  tekniskt hinder.
- Related records: PCD-2026-09-05-019, PCD-2026-09-05-021, PCD-2026-09-06-001.
- Resulting Wotan tasks: T-0075 (Sverkers sida), T-0076 (Kristinas sida),
  T-0077 (spegling av tretton äldre läsningar); T-0060 READY; T-0072
  kompletterad med P-0212-kriteriet; T-0051 omformulerad.
- Owner decision outstanding: P-0212/KP-03 kräver ägarens familjekunskap om
  Gunnar Hööks liv 1933–2017. Utan den kan hans livsbild inte fullbordas ens
  om födelseposten hittas, och djup 2 kan då dröja på en grind som inget
  arkivarbete löser.
- Portfolio signal: projektet är aktivt och har just fått en materiell
  kapacitetsökning; kön har fem READY-uppgifter och en ONGOING.
- Revisit when: T-0072 är DONE och P-0212:s källbreddsläge kan avgöras, eller
  ägaren lämnar familjekunskapen om Gunnar.

## PCR-2026-09-06-003

- Record type: review
- Date: 2026-09-06
- Mode: checkpoint
- Trigger: Vid T-0075:s tredje passage gav Floda församlingsbok det första
  arkivbelägget för Bernhard Natanael Eliasson efter 1910, och perioden
  avviker från en familjeuppgift som ligger nära ett ägarfastställt
  faderskap.
- Control judgement: continue; en ägarfråga uppstår men inget arbete stannar.
- Current gate: En bevarad konflikt mellan familjekrönika och samtida
  kyrkobok som bara ägaren kan tolka.
- Evidence:
  - `genealogy/citations/C-0912-bernhard-natanael-bokhallare-okna-1916-1917.md`
    — Floda `A II a/11` uppslag 592 rad 12: bokhållare vid Ökna säteri,
    inflyttad från Värsås **1916-11-22**, utflyttad till Oskarshamns
    stadsförsamling nr 98 **1917-11-03**.
  - `genealogy/citations/C-0913-okna-sateri-1910-1914-utan-bernhard.md`
    — avgränsat noll på Ökna säteris samtliga uppslag 591–611 i
    `A II a/8` (1910–1914); bokhållaren där var Gustaf Sigfrid Pettersson.
  - `genealogy/citations/C-0909-ada-och-arne-okna-floda-1915-1918.md`
    — Ada Wilhelmina var skriven vid Ökna till 1918-10-28.
  - A-1646 och A-1678 (familjekrönikans `1911–1916` och fotot 1914);
    A-3430–A-3433.
- Observation: Bernhard och Ada var samtidigt kyrkobokförda vid Ökna endast
  **1916-11-22–1917-11-03**, alltså efter sonen Arne Godvigs födelse
  1915-02-21. Familjens tidsangivelse `1911–1916` motsägs för sin tidiga del.
- Vad detta **inte** ändrar: faderskapet är fastställd projektinformation
  enligt PCD-2026-08-20-001 och demoteras inte av att ett arkivoriginal
  saknas. Konflikten gäller omständigheten, inte relationen.
- Öppna förklaringar: (a) han vistades vid Ökna som lantbrukselev eller
  praktikant före november 1916 utan att kyrkobokföras i Floda — vanligt vid
  tiden och förenligt med både fotot 1914 och krönikan; (b) årtalet 1911 är
  en minnesförskjutning och paret möttes på annan ort; (c) något annat som
  bara familjen känner till.
- Owner decision required: Hur ska familjeuppgiften A-1646 hanteras — kvarstå
  oförändrad med konflikten bevarad, preciseras av ägaren, eller kompletteras
  med ägarens kunskap om hur Bernhard och Ada möttes? Ingen ändring görs utan
  ägarens svar.
- Recommendation: Bevara konflikten som den är, fortsätt med KP-02
  (Oskarshamn nr 98, 1917-11-03), och lyft frågan till ägaren utan att röra
  vare sig faderskapet eller familjeuppgiftens status.
- Resulting Wotan tasks: none; arbetet fortsätter inom T-0075.
- Portfolio signal: projektet är aktivt; den nyöppnade bildåtkomsten
  producerar nu materiella fynd i takt.
- Revisit when: Ägaren svarar på frågan om Öknatjänsten.

### Tillägg samma dag: konflikten skärpt av Värsås församlingsbok

Efter att den felaktiga bedömningen att Värsås `A II a` slutade 1907 rättats
lästes `A II a/2` folio 134
(`genealogy/citations/C-0917-bernhard-i-foraldrahemmet-djursatra-1907-1916.md`).
Bernhard var **kyrkobokförd i föräldrahemmet på Djursätra Västergård i Värsås
hela perioden 1907 till 1916-11-22**, då han utflyttade till Floda samma dag
som Floda anger för inflyttningen. Två oberoende kyrkoböcker säger nu samma
sak, och Floda saknar honom före november 1916.

Familjekrönikans `1911–1916` vid Ökna står därmed mot samtida myndighetsposter
för hela sin tidiga del. Faderskapet är ägarfastställd projektinformation och
berörs inte. Kvar för ägaren är samma fråga som ovan, nu med starkare
underlag: vistades han vid Ökna före november 1916 utan att kyrkobokföras där,
eller möttes han och Ada på annat håll? Oskarshamns församlingsbok är läst och
tillför inget till just den frågan (C-0914, C-0915).

## PCR-2026-09-06-004

- Record type: review
- Date: 2026-09-06
- Mode: checkpoint
- Trigger: Efter T-0081 och T-0082 saknades en redovisning av vad det utförda
  arbetet betyder för north starens sex uppfyllelsevillkor. Rapporteringen
  hade beskrivit uppgiftsresultat, inte måluppfyllelse.
- Control judgement: **continue** — målet är **ofullbordat**, och den
  bindande grinden är villkor 2, livsbilderna.

### Lägesrevision mot uppfyllelsevillkoren

Bedömd för källäget **2026-09-06**, mätt ur `node scripts/goal-state.mjs`,
`node scripts/research-inventory.mjs` och personakternas egna belägg. Detta
är en **lägesrevision, inte avslutningsrevisionen enligt villkor 6**:
materiella, genomförbara åtgärder återstår.

**1. Anlinjer — ej styrkt, i planerad framdrift.** Registrerat gemensamt
djup är **5** (var 3 vid passagens början). Djup 1–5 är behandlade: 32 av 32
positioner på djup 5 är granskade och källbredd-klara, balanserat 16/16
mellan sidorna. Djup 6 är påbörjat: **57 av 64 positioner kända** (Sverker
28, Kristina 29), **51 källbredd-klara** (22 + 29). Obalansen ligger på
Sverkers sida och adresseras av T-0083. Villkorets andra led — att varje
kvarvarande föräldrafråga har en källgrundad avgränsning — är **inte**
uppfyllt: **38 anspetsar saknar giltig arkivfront**, 15 på Sverkers och 23
på Kristinas sida, de flesta med `IDENTITET OLÖST: saknar
återaktiveringsvillkor`. Enligt north star beskriver den statusen
kunskapsläget och bevisar inte uttömda undersökningar.

**2. Livsbilder — ej styrkt; detta är den bindande grinden.** Av **535
personakter** har **32** en profil enligt personkontraktet, och av dessa är
**7 GODKÄNDA** och **25 UNDERKÄNDA**. **503 akter saknar profil**, alltså
`ej bedömt enligt kontraktet`. 157 akter bär den äldre kombinationen
GRANSKAD + källbredd, som north star uttryckligen inte godtar som
automatiskt godkännande av PK-01–12. Avståndet till villkor 2 är därmed
storleksordningar större än avståndet till villkor 1, och det växer med
varje ny position. Den befintliga kön har bara **T-0070** (djup 5-kohorten,
32 personer) för detta, och den är BLOCKED bakom T-0069.

**3. Identiteter och kandidater — delvis styrkt.** Regeln följs i det
arbete som görs: konkurrerande identiteter hålls åtskilda och konflikter
bevaras — P-0535 Knut Sigfrid Bergersen förs separat från
familjeuppgiftens P-0299 (A-3606, A-3607), 1796 års Jonas i Sandssjön förs
som LEAD och inte som fastställd (A-3616), och avgjorda konflikter
redovisas som avgjorda med skäl (A-3592, makens födelseuppgift). Men
villkoret gäller **alla** bärande identiteter, och de 38 anspetsarna utan
giltig front samt de 503 obedömda akterna är inte prövade mot det.

**4. Källtäckning — delvis styrkt, med ett namngivet externt hinder.**
Katalogprovet i C-0961 ger en dokumenterad disposition för `B`, `T`, `J`
och `O` för samtliga åtta positioner på djup 4, Sverkers sida, och C-0950
gör detsamma för Kristinas åtta. Men **ett hinder lämnar ett materiellt
krav oprövat**: Riksarkivets **bouppteckningsregister och dödregister**
täcker både Södermanland och Västerbotten men ligger bakom **ALTCHA**, och
under passagen omfattade spärren hela katalogen — `/arkiv/<id>`, `/nad`,
`/bouppteckningar`, `/dodregister` och mantalssöket omdirigerades till
`/captcha`, medan IIIF-API:et svarade `200`. Därtill: **Sveriges Dödbok
1901–2013** är en köpprodukt utanför projektets åtkomst (C-0960), och
ArkivDigital är utesluten genom PCD-2026-09-05-011. North star är entydig:
lämnar ett sådant hinder ett materiellt uppfyllelsekrav oprövat är målet
ofullbordat. Det gäller i dag `B` för P-0015, P-0016, P-0028, P-0029,
P-0048 och P-0049 samt `D` för P-0009 och P-0010.

**5. Spårbarhet — starkast av villkoren, men inte färdigt.** Validatorn
räknar **3 096 assertions, 2 312 markdown-poster och 4 836 mediefiler** med
bevarade kontrollsummor; `node --test scripts/` ger 29 gröna. Evidensledgern
är append-only i praktiken: batch 341:s rättelse av Rotemansarkivets nollor
lades till som `## Rättelse`-avsnitt i S-0746 och C-0956 utan att skriva
över den ursprungliga avskriften. Villkorets andra led — att granskningen
visar att beläggen **bär** slutsatserna — prövas per person i
kontraktsprofilen, och den saknas för 503 akter.

**6. Avslutningsrevision — inte möjlig i dag.** Materiella, genomförbara
och motiverade åtgärder återstår: T-0083 pågår, T-0079, T-0080, T-0060,
T-0069 och T-0077 står READY, T-0073 och T-0074 är IDEA, och 503 akter
saknar kontraktsbedömning.

### Sakförändring i ett befintligt block

**T-0051** är blockerad på att den vanliga katalogen ligger bakom ALTCHA.
C-0963 upphäver blockeringen delvis: **hela årgången 1877 av Stockholms
mantalslängder är digitaliserad** — `SE/SSA/0031/06/G 1 BA/G 1 BA:76/1`
till `76/42`, batcherna `A0057718`–`A0057757` — och nås över det öppna
IIIF-API:et utan katalog och utan captcha. Läsesalskravet i C-0649 gäller
**mantalsuppgifterna** i `G 1 BB`, inte mantalslängden. Kvar är en
lokaliseringsfråga inom öppet material: vilken av de fyrtiotvå volymerna
upptar Kungsholmens kvarter.

- Current gate: **villkor 2, livsbilderna** — 503 av 535 akter saknar
  kontraktsbedömning. Styrregeln ger dock generationsskivan företräde så
  länge en sådan återstår, och djup 6 återstår.
- Recommendation: fortsätt T-0083 till djup 6 är behandlat, och lyft
  därefter kontraktsinförandet från en blockerad enstaka uppgift (T-0070)
  till en löpande skiva som följer varje generationsvåg, så att
  livsbildsskulden slutar växa fortare än den betalas av.
- Owner decision required: **ALTCHA.** Ägaren har tidigare visat att
  captchan kan öppnas på begäran (PCD-2026-09-05-020). Öppnas Riksarkivets
  katalog och specialsök i den inloggade webbläsaren faller `B` för sex
  personer på djup 4 samman till en enda arbetspassage, `D` för P-0009 kan
  prövas i samma svep, och T-0051 och T-0054 kan tas ur BLOCKED.
- Evidence:
  - `NORTH-STAR.md`, villkoren 1–6
  - `node scripts/goal-state.mjs` 2026-09-06: registrerat gemensamt djup 5
  - `genealogy/research-inventory.json`: 535 akter, 32 profiler, 7 GODKÄND,
    25 UNDERKÄND, 503 utan profil
  - `genealogy/citations/C-0950-katalogprov-djup-4-kristinas-sida.md`
  - `genealogy/citations/C-0961-katalogprov-djup-4-sverkers-sida.md`
  - `genealogy/citations/C-0960-bernhard-eliasson-malmo-gravnoll-2026-09-06.md`
  - `genealogy/citations/C-0963-mantalslangd-1877-digitaliserad.md`
  - `genealogy/source-coverage.md`, de två personmatriserna för djup 4
- Resulting Wotan tasks: none nya i denna post; T-0083 fortsätter.
- Portfolio signal: projektet är aktivt och gör mätbar framdrift i villkor 1;
  villkor 2 växer snabbare än det betalas av.
- Revisit when:
  - djup 6 är behandlat, eller
  - ägaren öppnar ALTCHA, eller
  - kontraktsinförandet får en löpande skiva.

## PCD-2026-09-06-003

- Record type: decision
- Date: 2026-09-06
- Decides review: `PCR-2026-09-06-004`
- Owner: Project Control inom delegerat mandat (ägarens stående direktiv
  delegerar övriga ägarbeslut till Project Control)
- Decision: **Livsbildsskivan ska löpa parallellt med generationsskivan,
  inte efter den.** Varje generationsvåg som producerar nytt material ska
  omedelbart följas av en kontraktsomprövning av de personer vågen
  berörde, innan arbetet går djupare.
- Disposition: approved

### Skäl

PCR-2026-09-06-004 visade att villkor 2 är den bindande grinden och att den
växer snabbare än den betalas av. Inventeringen ger nu skälet i klartext:

> Av de 32 personakter som har en kontraktsprofil är **7 GODKÄNDA — och
> samtliga sju är `INTEGRITETSMINIMERAD`**, alltså personer där
> dataminimeringen i sig uppfyller livsbildskravet. Alla **25 övriga har
> `Livsbildsläge: PÅGÅR` och `Kontraktsgranskning: UNDERKÄND`.**
> **Ingen avliden person i projektet har ännu passerat
> livsbildskravet.**

North star är uttrycklig på denna punkt: *"Biografiska luckor får inte
skjutas undan på obestämd tid av nya anor"* och *"Både träd och livsbilder
ingår i varje våg"*. Att köra T-0083 vidare mot djup 6 medan de åtta
personer som T-0081 nyss fyllde med material ligger kvar som UNDERKÄNDA är
just det som villkoret förbjuder.

### Sakläget som gör omprövningen mogen nu

T-0081 besvarade merparten av de frågor som fällde djup 4-profilerna
2026-09-05. För P-0016 var granskningen UNDERKÄND på PK-03, PK-04, PK-08,
PK-10 och PK-12, alla bundna till Q-01 och Q-02. Sedan dess är **maken
identifierad** (Axel Vilhelm Ekholm, född 1878-02-17 i Åsbo, död
1913-03-11), **hennes död belagd** (1964-03-15, gravsatt i Flen) och
**luckan 1900–1913 till stor del sluten** genom Rotemansarkivet. Samma sak
gäller i olika grad P-0009, P-0010, P-0015, P-0028, P-0029, P-0048 och
P-0049.

### Verkställighet

- **T-0083 pausas som READY** med sin återupptagningspunkt intakt. Den är
  inte övergiven; den återupptas när livsbildsskivan för samma våg är
  gjord.
- **T-0084 skapas och startas**: kontraktsomprövning av djup 4-kohorten på
  Sverkers sida, åtta personer, mot det material T-0081 och T-0082 lade
  till.
- **T-0070:s beroende av T-0069 upphör** som skäl att hålla den BLOCKED;
  den blir READY och är livsbildsskivan för djup 5.

- Resulting Wotan tasks: `T-0084` (ny, ONGOING); `T-0083` → READY;
  `T-0070` → READY.
- Portfolio signal: projektet byter takt så att villkor 2 börjar röra sig
  för första gången för en avliden person.
- Revisit when: T-0084 är klar och andelen GODKÄNDA profiler har mätts om.

## PCR-2026-09-06-005 — Checkpoint efter T-0084: villkor 2 har rört sig

- Datum: 2026-09-06
- Utlösare: T-0084 avslutad (batcherna 353–364). Reaktiveringsvillkoret i
  PCD-2026-09-06-003 var uttryckligen "T-0084 är klar och andelen GODKÄNDA
  profiler har mätts om".
- Läge: `research-inventory` ger **9 GODKÄNDA och 23 PÅGÅR** av 32 profiler,
  mot 7/25 när beslutet fattades. `goal-state` ger registrerat gemensamt
  djup 5, oförändrat.

### Kontrolldom: fortsätt

Beslutet i PCD-2026-09-06-003 var att låta livsbildsskivan gå parallellt med
djupforskningen, med motiveringen att villkor 2 växte snabbare än det
betalades av. **Det har gett utdelning, och den är av rätt slag.**
**P-0048 Anders Alfred Andersson och P-0049 Anna Fredrika Jakobsdotter är
projektets första avlidna personer som passerar personkontraktet.** De sju
tidigare godkända är samtliga levande och integritetsminimerade, alltså
godkända på ett integritetsminimerat omfång — inte på ett fullgånget
livslopp. Villkor 2 i NORTH-STAR.md har därmed **för första gången rört sig
på det sätt villkoret faktiskt kräver**.

### Evidens

- Trettiofyra ej styrkta kontraktskrav i kohorten har blivit nio.
- Två profiler passerade, och tre av de kvarvarande sex står på **en enda
  namngiven, genomförbar åtgärd** var (P-0016, P-0028, P-0029).
- Fyra läsningar i original tillkom: Burträsk 1946–1948, Ytterhiskeblocket i
  Umeå, Flen 1933–1955 och kartläggningen av Matteus vigselbok.
- Ett hinder avfärdades och ett tillkom: Umeås fastighetslängder har inget
  register, och Flens församlingsböcker slutar 1955.

### Aktuell grind

Villkor 2 är fortfarande den bindande grinden, men den har flyttat karaktär:
från "ingen avliden har passerat" till "tre personer står på tre namngivna
läsningar". Det är inte längre en strukturell fråga utan en arbetsmängd.

### Verkställighet inom delegerad myndighet

Restposterna är för stora för att hänga kvar som svans på T-0084 och splittas
enligt AGENTS.md:

- **T-0085 (READY, M)** — vigseln Ekholm–Ålund 1900–1906. Enda kvarvarande
  materiella åtgärd för P-0016; kostnaden är bestämd i batch 364.
- **T-0086 (READY, L)** — systematisk rubrikgenomgång av Umeås
  fastighetslängder `A II b` efter Zingmarks gård. Enda kvarvarande
  materiella åtgärd för P-0028 och P-0029.

Ingen ny strategisk riktning fattas här; båda uppgifterna ligger inom det
program PCD-2026-09-06-003 redan godkände.

### Ägarbeslut som fortfarande väntar

**ALTCHA.** Bouppteckningsregistret, `/nad`, `/arkiv/<id>`, `/dodregister`
och Stockholms mantalslängdssök ligger bakom en captcha som agenten inte får
lösa. Den spärrar dödsboet efter P-0048 och P-0049, bouppteckningen efter
P-0016 samt lagfart och inskrivningsprotokoll för P-0028 och P-0029. Ägaren
kan häva den genom att öppna sidorna i sin egen inloggade Chrome.

- Resulting Wotan tasks: `T-0085` (ny, READY); `T-0086` (ny, READY);
  `T-0084` → DONE.
- Portfolio signal: north star villkor 2 har mätbart rört sig för första
  gången för en avliden person.
- Revisit when: T-0085 och T-0086 är utförda, eller när ägaren häver ALTCHA.

## PCD-2026-09-06-004 — Splittring av T-0084:s restposter

- Datum: 2026-09-06
- Beslutsunderlag: PCR-2026-09-06-005
- Beslut: **godkänd inom delegerad myndighet.** T-0084 avslutas som DONE,
  och dess två kvarvarande materiella åtgärder skapas som egna avgränsade
  uppgifter, T-0085 och T-0086, med uttryckligt omfång, uttryckliga
  uteslutningar och verifierbara utfall. Ingen uppgift tillåts växa vidare
  utan eget beslut.
- Resulting Wotan tasks: `T-0084` → DONE; `T-0085` READY; `T-0086` READY.
- Reaktiveringsvillkor: när T-0085 eller T-0086 avslutas mäts andelen
  GODKÄNDA profiler om.

## PCD-2026-09-06-005 — Ägaren hävde ALTCHA; hindret upphör och en hinderbeskrivning rättas

- Datum: 2026-09-06
- Trigger: **ägaren löste själv ALTCHA-verifieringen** i sin inloggade
  Chrome, mitt under T-0085, och meddelade det i sessionen.
- Beslut och verkställighet: hindret **ALTCHA** utgår som blockerande skäl
  för denna session. `/nad`, `/arkiv/<id>`, `/bouppteckningar` och
  `/dodregister` svarar `200`
  ([C-0977](genealogy/citations/C-0977-altcha-havd-och-bouppteckningsregistrets-tackning.md)).

### Vad hävningen gav omedelbart

**NAD-trädet är den auktoritativa förteckningen, och det visar serier som
metadatasökningen inte returnerar.** Första användningen gav Adolf Fredriks
`E IV` Register till lysnings- och vigselböcker, 1903–1943 i en volym, och
med den löstes **vigselfrågan för P-0016** — den enda materiella lucka som
stått öppen i hennes livslopp sedan 2026-09-05. Vigseln skedde
**1903-05-01 i Adolf Fredriks församling**.

### En rättelse som ägaren bör känna till

Fem profiler har beskrivit bouppteckningarna som "blockerade av ALTCHA".
Med spärren hävd kunde registrets täckning prövas, och den **slutar 1910
för Burträsk och 1908 för Hyltinge**. De fyra efterfrågade
bouppteckningarna — 1913, 1947, 1949 och 1964 — låg alltså **utanför
registrets omfång**. Hindret var felbeskrivet i god tro. Rättelsen är
införd i P-0016, P-0028, P-0029, P-0048 och P-0049, och den rätta vägen är
domsagornas egna häradsrättsarkiv.

### Vad som fortfarande gäller

Regeln står fast: **agenten löser aldrig en ALTCHA eller annan
människoverifiering.** Hävningen gäller den inloggade sessionen; återkommer
spärren bokförs den som hinder och lämnas till ägaren.

**T-0051 och T-0054**, som stått BLOCKED på ALTCHA sedan 2026-09-05, bör
prövas om mot den öppna katalogen vid nästa tillfälle. De ändras inte i den
här batchen, eftersom de ligger utanför T-0085:s omfång.

- Resulting Wotan tasks: `T-0085` → DONE. `T-0051` och `T-0054` kvarstår
  BLOCKED tills de prövas om.
- Portfolio signal: det enskilt största externa hindret i projektet är
  hävt, och den första frågan det öppnade var också den som höll en profil
  tillbaka.
- Revisit when: T-0051 och T-0054 prövas om mot den öppna katalogen, eller
  när spärren återkommer.

## PCR-2026-09-06-006 — Villkor 2 rör sig tredje gången på en dag

- Datum: 2026-09-06
- Utlösare: T-0087 avslutad. Reaktiveringsvillkoret i PCD-2026-09-06-004 var
  att andelen GODKÄNDA profiler mäts om när T-0085 eller T-0086 avslutas;
  T-0085 gav upphov till T-0087, som nu är klar.
- Läge: `research-inventory` ger **10 GODKÄNDA och 22 PÅGÅR** av 32
  profiler, mot **7 / 25** vid dagens början. `goal-state` ger registrerat
  gemensamt djup 5, oförändrat.

### Kontrolldom: fortsätt

**Tre avlidna personer har passerat personkontraktet på en dag** — P-0048
och P-0049 i T-0084, och nu **P-0016 Hulda Amalia Ekholm, född Ålund**, som
dessutom är **den första på Kristinas sida**. Vid dagens början hade ingen
avliden person passerat; de sju godkända var alla levande och
integritetsminimerade. Villkor 2 i NORTH-STAR.md har alltså rört sig från
noll till tre på det sätt villkoret kräver.

### Evidens

- P-0016: samtliga tolv krav STYRKT, tidslinjen materiellt obruten
  1877–1955 med belagd slutpunkt 1964. Den sista luckan slöts av Hyltinges
  flyttningsbok, den näst sista av Adolf Fredriks lysnings- och vigselbok.
- Dagens fyra avgörande fynd kom alla ur **routing, inte uthållighet**:
  uppslagshänvisningen `5/I` i Burträsks inflyttningsbok, moderns aldrig
  utvunna rad på en bild som redan låg speglad i repot, Adolf Fredriks
  `E IV`-register som NAD visade så snart ALTCHA var hävd, och Hyltinges
  årskarta.
- Ett hinder föll (ALTCHA), ett visade sig felbeskrivet
  (bouppteckningsregistrets täckning) och två nya är namngivna (Flens
  församlingsböcker efter 1955; kommunala socialakter).

### Aktuell grind

Villkor 2 är fortfarande den bindande grinden, men karaktären har ändrats
igen: från "tre personer står på tre namngivna läsningar" till **"tjugotvå
profiler PÅGÅR, varav de flesta på egna, ännu okartlagda återstoder"**. Det
är inte längre enskilda läsningar utan en arbetsmängd som ska planeras.

### Kvarvarande kö

`T-0086` (READY, L) — Umeås fastighetslängder för P-0028 och P-0029, den
enda kvarvarande åtgärden för två profiler. `T-0070` (READY, L) —
livsbildsskivan för djup 5, 32 personer. `T-0083`, `T-0080`, `T-0079`,
`T-0077`, `T-0069`, `T-0060`, `T-0051` READY; `T-0054` BLOCKED på T-0051.

- Resulting Wotan tasks: `T-0087` → DONE. Inga nya.
- Portfolio signal: north star villkor 2 har gått från noll till tre
  godkända avlidna personer på en dag, och båda ättegrenarna är
  representerade.
- Revisit when: T-0086 avslutas, eller när andelen GODKÄNDA mäts om nästa
  gång.

## PCR-2026-09-06-007 — Fem avlidna har passerat, och djup 4-kohorten är nästan färdig

- Datum: 2026-09-06
- Utlösare: T-0088 avslutad. Reaktiveringsvillkoret i PCR-2026-09-06-006 var
  att andelen GODKÄNDA mäts om när T-0086 avslutas; T-0086 gav upphov till
  T-0088, som nu är klar.
- Läge: `research-inventory` ger **12 GODKÄNDA och 20 PÅGÅR** av 32
  profiler, mot **7 / 25** vid dagens början. `goal-state` ger registrerat
  gemensamt djup 5, oförändrat.

### Kontrolldom: fortsätt

**Fem avlidna personer har passerat personkontraktet under dagen** —
P-0048, P-0049, P-0016, P-0028 och P-0029 — mot noll vid dess början. Båda
ättegrenarna är representerade. Av djup 4-kohorten på Sverkers sida
återstår **P-0009, P-0010 och P-0015**; av Kristinas sida är P-0016 klar.

### Evidens

Dagens sex avgörande fynd kom alla ur **routing eller omprövad
källbedömning**, inte ur uthållighet:

1. Uppslagshänvisningen `5/I` i Burträsks inflyttningsbok gav paret
   Anderssons hushållssida.
2. Moderns aldrig utvunna rad på en bild som legat speglad i repot sedan
   augusti gav Flenåren och band maken till henne i en enda källa.
3. Adolf Fredriks `E IV`-register, som NAD visade så snart ägaren hävt
   ALTCHA, gav vigseln 1903-05-01 på tre läsningar.
4. Hyltinges årskarta gav luckan 1900–1902.
5. `A II b/14`, tidigare avfärdad som ett gatunamnsregister, visade sig
   rymma ett stadsägeregister som gav Zingmarks sju stadsägor **och**
   rättade söknyckeln 1258 → 1268.
6. NAD:s fritextsökning avgjorde att sågverket i Rosinedal aldrig lämnat
   något arkiv.

Två felbeskrivningar rättades i god tro: bouppteckningsregistrets täckning
och `A II b/14`:s innehåll. Ett hinder föll (ALTCHA), och fem nya är
namngivna: Flens församlingsböcker efter 1955, Umeå stadsförsamlings
dödböcker 1930–1950, inskrivningsdomarens fastighetsböcker,
egnahemsnämndens volym, och de kommunala socialakterna i Flens kommunarkiv.

### Aktuell grind

Villkor 2 är fortfarande den bindande grinden. Karaktären har ändrats igen:
**tjugo profiler PÅGÅR**, och **503 av 535 personakter saknar profil helt**.
Det senare är nu den dominerande posten och kräver planering, inte enskilda
läsningar. `T-0070` — livsbildsskivan för djup 5, 32 personer — är den
uppgift som svarar mot det.

- Resulting Wotan tasks: `T-0088` → DONE. Inga nya.
- Portfolio signal: north star villkor 2 har gått från noll till fem
  godkända avlidna personer på en dag, och djup 4-kohorten är nästan
  färdigbehandlad.
- Revisit when: `T-0070` påbörjas eller avslutas, eller när andelen
  GODKÄNDA mäts om nästa gång.

## PCR-2026-09-06-008 — Ett systematiskt metodfel i de negativa kontrollerna

- Record type: review
- Date: 2026-09-06
- Mode: checkpoint
- Trigger: Kontraktsgranskningen av fyra par i `T-0070` (batch 372–375) fann samma metodfel sex gånger, varav fyra i ett enda par.
- Control judgement: continue — men med en namngiven, återkommande felkälla som nu är dokumenterad och åtgärdad genom två uppgifter.

### Iakttagelsen

Projektets negativa kontroller är genomgående **korrekt avgränsade i
citatet** och **felaktigt generaliserade i praktiken**. Mönstret är:

> En uppgift ur en hushållslängd — ett födelse- eller dödsdatum — används som
> söknyckel. Kontrollen utförs troget mot den nyckeln, citatet skriver
> uttryckligen att omfånget är dagen och dess omedelbara omgivning, och sedan
> behandlas frågan i praktiken som uttömd. **Hypotesen att nyckeln själv är
> fel prövas aldrig.**

Sex belagda instanser:

| Person | Fråga | Kontrollerat omfång | Möjligt omfång |
|---|---|---|---|
| P-0423 | dödsdag 1868-08-14 | datumfönster i 27 församlingsranger | hela årgångar; brudens hemförsamling |
| P-0021 | vigsel juni 1885 | **fel församling** — endast brudgummens | brudens församling |
| P-0050 | födelse 1835-07-19 | 14 juli → 28 augusti 1835 | hela 1834–1836 |
| P-0050 | död 1899-06-22 | **17–22 juni 1899, sex dagar** | hela 1899–1900 |
| P-0051 | födelse 1830-02-24 | 23 → 26 februari, Bygdeå C/4 | hela 1830 |
| P-0051 | födelse 1830-02-14/24 | dagarna kring båda, Lövånger C/5 | hela 1830 |

### Varför det spelar roll

Två av instanserna gäller personer vars **identitet är olöst** — P-0021 och
P-0051 — och i båda fallen är den ogjorda läsningen den som skulle kunna lösa
den. För P-0051 är den dessutom den **enda som prövar rätt hypotes**: hon är
antecknad som `oäkta`, och ett utomäktenskapligt barn kan vara bokfört under
moderns namn, vilket ingen namn- och datumbunden sökning någonsin kan hitta.

Felet är inte slarv. Varje enskilt citat är metodiskt korrekt skrivet och
anger sin egen gräns. Felet ligger i **övergången från citat till
arbetsläge**: en avgränsad negativ kontroll har fått stänga en fråga som den
inte kan stänga. Personkontraktets krav PK-08 och PK-12 är precis det
instrument som fångar detta, och det gjorde det — i fyra av åtta granskade
personer.

### Evidens

- `genealogy/research-log/2026-09-06.md`, batch 372, 373 och 375
- `genealogy/research-profiles/P-0050.md`, `P-0051.md`, `P-0021.md`, `P-0423.md`
- `genealogy/citations/C-0433`, `C-0144`, `C-0145`, `C-0306`, `C-0420`

### Aktuell grind

Oförändrad: villkor 2, och inom det de 495 personakter som saknar profil.
Denna iakttagelse ändrar inte grinden men **höjer värdet av
kontraktsgranskningen som instrument** — den producerar inte bara bedömningar
utan hittar konkret, utförbar forskning som annars hade förblivit dold bakom
ett tillsynes uttömt kunskapsläge.

- Resulting Wotan tasks: `T-0089` (fem ohindrade läsvägar, skapad i batch 373)
  och `T-0090` (tre datumbundna nollresultat, skapad i batch 375). Båda READY.
- Owner decision required: ingen. Båda uppgifterna ligger inom delegerad
  mandat och kräver varken beställning, läsesal eller publicering.
- Portfolio signal: åtta av 32 personer i djup 5-kohorten är granskade; ingen
  har blivit GODKÄND, men **åtta konkreta ohindrade läsvägar** har
  identifierats, varav två kan lösa en olöst identitet.
- Revisit when: `T-0089` eller `T-0090` är utförd, eller när nästa fyra par i
  `T-0070` är granskade och mönstret kan mätas om.

## PCR-2026-09-06-009 — Daterade åtkomstbesked som aldrig omprövats

- Record type: review
- Date: 2026-09-06
- Mode: checkpoint
- Trigger: Kontraktsgranskningen av par 7 i `T-0070` (batch 378) fann ett andra systematiskt mönster, skilt från det datumbundna i PCR-2026-09-06-008.
- Control judgement: continue — mönstret är namngivet och åtgärdat genom `T-0092`.

### Iakttagelsen

> Ett åtkomstbesked formuleras korrekt vid sin tidpunkt — `saknar bildlänk`,
> `ej fjärråtkomlig`, `stannade vid orörd ALTCHA` — och blir sedan stående som
> om det vore permanent, **även när förutsättningarna ändras**.

Beskeden är inte felaktiga. Repots egen metodnot i `genealogy/method-riksarkivet.md`
säger uttryckligen att avsaknad av bildlänk visar att volymen inte kan nås på
distans **men inte varför**. Det som saknas är omprövningen.

Att mönstret är verkligt visas av att samma slutsats **redan har rivits upp
tre gånger** — varje gång utan att någon gick igenom de övriga:

| Person | Volym | Äldre besked | Utfall |
|---|---|---|---|
| P-0020 | Värsås A I/7–A I/8 | ej digitaliserad | öppnades inloggat 2026-09-03 |
| P-0050 | Nysätra C/4, E I/1 | ej digitaliserad | öppnades inloggat 2026-08-21 |
| P-0253 | Sättna F/1, Holm B/2, Ljustorp E I/3 | `401` på bildnivå | upplösta 2026-09-05 |

En genomgång av samtliga personakter visar **fem kvarvarande besked** av den
här typen. Ett av dem, Bygdeås bilageserier för P-0051, är omprövat inloggat
2026-09-05 och står fast som `Läsesal`. De övriga fyra är inte omprövade, och
**två av dem har uppenbart ändrade förutsättningar**: Gryts C- och E-serier
för P-0110 daterar sig till 2026-08-20, och Forssa H II/1 för P-0133 blockeras
uttryckligen av en **ALTCHA som ägaren hävde 2026-09-06**.

### Varför det spelar roll

Gryt-kontrollen kostar en uppslagning och skulle kunna ge **två av P-0110:s
tre saknade hörnstenar** samtidigt — hans egen födelsenotis 1850 och parets
vigsel omkring 1876 — samt besvara samma vigselfråga för P-0111.

Mönstret har också en generell konsekvens för hur kön ska prioriteras: en
**omprövning av ett hinder** kan vara billigare och ge mer än en ny läsning,
och den bör därför komma före sveparbete.

### Evidens

- `genealogy/research-log/2026-09-06.md`, batch 378
- `genealogy/research-profiles/P-0110.md`, `P-0111.md`
- Påståendena A-0489, A-2719, A-2751, A-2737/A-2953 samt de upphävda A-0622,
  A-0662, A-0663, A-2407

### Aktuell grind

Oförändrad. Iakttagelsen ändrar inte grinden men **prioriteringsordningen i
kön**: hinderomprövningar först, sedan olästa årgångar, sedan sveparbete.

- Resulting Wotan tasks: `T-0092` (tre daterade åtkomstbesked, READY) och
  `T-0091` väg 5–7 (Ålundparets ohindrade läsningar).
- Owner decision required: ingen. Samtliga ligger inom delegerat mandat.
- Portfolio signal: fjorton av 32 personer i djup 5-kohorten är granskade;
  **nitton ohindrade forskningsvägar** ligger nu i kön, mot noll när
  granskningen började.
- Revisit when: `T-0092` är utförd, eller när nästa fyra par är granskade.

### Rättelse 2026-09-06 till PCR-2026-09-06-009

Granskningen av par 8 samma dag visar att **omfattningen ovan var för stor**.
Två av de tre volymgrupper som beskrevs som oprövade var **redan omprövade**;
felet var att endast det äldre påståendet i personakten lästes, inte det
senare som upphäver det:

- **Forssa H II/1** för P-0133 är omprövat inloggat 2026-09-05 tillsammans med
  Villåttinge C II b/5 och F II/59, Flen P I/1 och D14/10. CAPTCHA-hindret
  försvann, men samtliga visar fortsatt endast `Läsesal` (A-2954, C-0757).
- **P-0336:s spärrade rutter** öppnades efter ägarens egen CAPTCHA-lösning;
  samtliga elva visade `Läsesal` (A-2963, C-0762).

Mönstret i sig kvarstår — det är belagt av tre upphävda besked — men efter
kontroll återstår **en** oprövad volymgrupp: **Gryts C- och E-serier** för
P-0110 och P-0111, daterade 2026-08-20.

`T-0092` är rättad i enlighet med detta och har fått ett andra utfall: en
**förteckning över vilka åtkomstbesked som är aktuella och vilka som är
daterade**, så att en redan gjord kontroll inte upprepas. Just den
förteckningen är sannolikt uppgiftens mest bestående värde.

## PCR-2026-09-06-010 — Djup 5-kohorten är genomgången; kön har fyllts med utförbar forskning

- Record type: review
- Date: 2026-09-06
- Mode: checkpoint
- Trigger: `T-0070` avslutad. Hela djup 5-kohorten om 32 personer har fått en första kontraktsgranskning i batcherna 372–387.
- Control judgement: continue — men med **omprioriterad ordning**: utför den kö granskningen skapade innan nästa kohort påbörjas.

### Vad som gjordes

Samtliga **32 personer** i djup 5 har nu tidslinje, biografisk sammanfattning
och en första kontraktsgranskning mot `person-research/v1`. Projektets
profiler gick från **32 till 64**.

**Ingen av de 32 blev GODKÄND.** Det är det väntade utfallet av en
förstagångsgranskning av en tidigare oprövad kohort, och **ingen
legacy-`KLAR` eller `GRANSKAD` konverterades**.

### Evidens: granskningens verkliga produkt

Värdet ligger inte i bedömningarna utan i att granskningen **hittade
utförbar forskning som låg dold bakom ett till synes uttömt kunskapsläge** —
omkring **37 ohindrade vägar**, registrerade som `T-0089`–`T-0093`.

Fem mönster återkom, alla dokumenterade med instanser:

1. **Det datumbundna nollresultatet** (nio instanser). Ytterlighetsfallet:
   en dödbok kontrollerad i **sex dagar** av fjorton möjliga år.
2. **Vigseln sökt i fel församlingar** (tre instanser). Metodiskt korrekt i
   brudgummens och brudens födelseförsamling — men aldrig i den socken där
   **brudens föräldrar bodde**.
3. **Det daterade åtkomstbeskedet** (fyra redan upprivna, två kvar).
4. **Screening som inte är läsning** — OCR-pass och översiktsläsningar
   korrekt märkta i citaten men utan uppföljning.
5. **Oförklarade anteckningar som aldrig lagts bredvid varandra** — odöpta
   barn i **två obesläktade hushåll** i samma anlinje.

Kohorten visade också något om sig själv: **sex personer saknar egen
födelsenotis** och tre av dem har därför `Identitetsläge: OLÖST`; **tre
saknar bekräftad dödsdag** trots att en hushållskälla anger en; och det
finns **en enda konkret väg till PER-temat** i hela kohorten.

### Aktuell grind

Villkor 2 är fortfarande den bindande grinden, men dess karaktär har ändrats
igen. Det som nu hindrar godkännanden är inte okunskap om vad som fattas —
**det är att den identifierade forskningen inte är utförd**.

### Owner decision required

Ingen. Samtliga fem uppgifter ligger inom delegerat mandat och kräver varken
beställning, läsesal eller publicering. Det som **skulle** kräva ägarbeslut —
bouppteckningar och läsesalsvolymer — är genomgående markerat som
hinderbundet och ligger utanför uppgifterna.

### Rekommendation

**Utför `T-0089`–`T-0093` före djup 6.** Skälen:

- Flera vägar kan **omedelbart lösa en `OLÖST` identitet** — Kyrkefallas
  vigselbok 1885 för P-0021, Lövångers grannår för P-0051, Gryts serier för
  P-0110.
- Några kostar **en enda uppslagning**: Indal F/2 ger dödsorsakerna för två
  personer; bouppteckningen `A0033199_00234` ligger redan nedladdad med bara
  sin första sida läst.
- Att i stället påbörja djup 6 skulle lägga **64 nya personer** ovanpå en kö
  som just har fyllts, och upprepa samma mönster en generation längre bak.

- Resulting Wotan tasks: `T-0070` → DONE. `T-0089`–`T-0093` READY, samtliga
  skapade ur granskningen.
- Portfolio signal: profilerna fördubblades på en dag, och projektet har för
  första gången **en kö av konkret, ohindrad forskning** i stället för en kö
  av hinder.
- Revisit when: `T-0089`–`T-0093` är utförda, eller när djup 6 påbörjas.

## PCR-2026-09-06-011

- Record type: review
- Date: 2026-09-06
- Mode: checkpoint
- Trigger: `T-0092` utförd i sin helhet — fem sakmoment plus förteckningen.
- Control judgement: continue

### Evidens

`T-0092` var formulerad som en omprövning av **ett** daterat åtkomstbesked,
efter att rättelsen samma dag hade visat att två av tre redan var omprövade.
Den växte till fem sakmoment. **Samtliga fem gav positivt utfall — och inget
av de fem antagna åtkomsthindren var ett åtkomsthinder.**

| Antaget hinder | Vad det verkligen var |
|---|---|
| Gryt `C/1–C/4` ej digitaliserade | Bildlänken saknas i **sökträffen**; detaljvyn anger `Reproducerad på: C0006497`, 234 bilder |
| Gryts vigselböcker före 1895 ej digitaliserade | Serien `E I` **finns inte** före 1895; vigslarna 1861–1894 ligger i `C/5` |
| Ölands `F II` saknar årsvolym 1901 | `F II` slutar 1881 och hänvisar i egna rader till `A II c/17` |
| `SE/VALA/01959` exponerar ingen årsvolym | `F I a` har **årliga** mantalslängder 1845–1910 |
| Ingen efterträdarserie efter 1903 | **Tingslaget upphörde 1903**; Bråbygdens domsaga tog över |
| Ingen serie för Stockholms bouppteckningar 1886 | Arkivet heter `SE/SSA/0145A` och innehåller inte ordet bouppteckning |

Fem påståenden är satta till `REJECTED` med bevarad historik — A-0489,
A-3162, A-3176, A-3164, A-3169 — och ett är i stället **bekräftat med nytt
datum**, A-3163 via A-3679.

### Vad som faktiskt vanns

- **Två hörnstenar.** P-0110:s egen födelsenotis 1850 (Hornet i Gryt, döpt
  15 september, fadern skriven `Bond.`) och parets vigsel **1876-06-24**.
- **En fråga avgjord genom att svaret inte finns.** Indals dödbok har tomma
  dödsorsakskolumner **även i originalet**. HAL går till `GENOMGÅNGET` för
  P-0315 och P-0316; det är ett avslut, inte ett nollresultat att lämna
  öppet. Läsningen gav dessutom att båda dog på hemorten och
  begravningsdagarna.
- **Mönster 2 i granskningen är belagt, inte längre en hypotes.** Ålundparets
  vigsel förrättades i **Husby-Oppunda**, brudens familjs gamla socken — inte
  i Västra Vingåker, hennes födelseförsamling, där en hel årgång en gång
  lästes utan träff. Nollresultatet står kvar och är nu **förklarat**.
- **Fyra exakta volymer** där det tidigare stod att ingen kunde identifieras.

### Aktuell grind

Oförändrad i sak: villkor 2, den identifierade forskningen är inte utförd.
Men **grindens karaktär har skärpts**. `T-0092` visar att en del av det som
räknats som hinder inte var hinder utan **vår egen läsning av
arkivförteckningen**. Det betyder att köns återstående "hinderbundna" poster
inte kan tas för givna.

### Ny varaktig kontroll

`genealogy/access-register.md` är skriven och länkad från
`method-riksarkivet.md` och `source-coverage.md`. Den samlar alla kända
åtkomstbesked och kräver att **fem kontroller** är gjorda innan ett nytt
negativt besked skrivs: detaljvyns `Reproducerad på:`, detaljvyns
`Innehåller även:`, serieförteckningens `Se:`-rader, myndighetspostens
verksamhetstid, och att arkivbildarens namn inte behöver motsvara
handlingstypen. Upphävda besked raderas inte utan flyttas med sitt datum
bevarat.

### Owner decision required

Ingen. Allt utfört ligger inom delegerat mandat: inga beställningar, ingen
läsesal, ingen publicering, inget löst captcha. Det som **skulle** kräva
ägarbeslut — `A II c/17`, `F II/75`, `SE/VALA/01529/F II/10` och
`SE/SSA/0145A/F 1 A/700–703` — är genomgående lämnat som identifierat men
oläst.

### Rekommendation

**Fortsätt med `T-0089`–`T-0091` och `T-0093`, men tillämpa
`access-register.md`:s fem kontroller på varje väg som är märkt hinderbunden
innan den avfärdas.** `T-0092` gör det sannolikt att fler poster i de
listorna är felmärkta på samma sätt.

- Resulting Wotan tasks: `T-0092` → DONE. Inga nya uppgifter skapade.
- Portfolio signal: projektet har för första gången ett **stående
  åtkomstregister**, och en dags arbete visade att fem av fem antagna hinder
  var läsfel. Det är ett kunskapstillskott om **metoden**, inte bara om
  släkten.
- Revisit when: `T-0089`–`T-0091` och `T-0093` är utförda, eller när ett nytt
  negativt åtkomstbesked skrivs utan att registrets fem kontroller är gjorda.

## PCR-2026-09-06-012

- Record type: review
- Date: 2026-09-06
- Mode: checkpoint
- Trigger: `T-0089` utförd i sin helhet — samtliga sju läsvägar.
- Control judgement: continue

### Evidens

Sju arkivläsningar som kontraktsgranskningen funnit **ohindrade men aldrig
utförda** är nu gjorda. Utfallet fördelar sig i tre slag och är ovanligt
konkret.

**Tre positiva fynd.**

| Fynd | Betydelse |
|---|---|
| Vigseln **1885-06-19** i Mofalla annexförsamling | Folio 18 gav Augusta Viktorias hushåll vid ¼ mtl Bjerg och **en far vid namn Johannes Eriksson** — första källbundna förklaringen till patronymikonet `Johansdotter` |
| Vigseln **1850-11-24** i Degerfors | **Brudens föräldrar namnges i originalet**: `Bond. Pett. R. Pehrsson o. H:u Beata Jonsd:r ifrån Ånäset`. Starkaste enskilda belägget hittills för Sara Sophia Pehrsdotters äldre identitet — en samtida ministerialpost i stället för en hushållsrad |
| `SE/GLA/11027/F II/12` och `SE/GLA/13628/C/5` | Två exakta volymer för 1949 där ingen tidigare kunnat pekas ut |

**Tre avgränsade noll med utskrivet omfång:** Sättnas hela 1872, Bygdeås
1861–1863 och Degerfors hela dödsfönster 1868-02-13 – 1870-07-02.

**En rättelse av tidigare arbete:** Bygdeås vigselår 1861 var **inte
färdigläst**. Kontrollen hade läst 23 poster; årgången löper till 28, och
posterna 24–28 låg på nästa bild. Nollet är komplett först nu.

### Två metodresultat värda att behålla

**1. Mönster 2 är prövat sju gånger och gäller inte alltid.** Att söka
vigseln där brudens familj hörde hemma löste Mofalla, Degerfors och —
tidigare samma dag — Gryt. Det höll **inte** för Sättna, där tre
församlingar nu är uttömda. Ett mönster vars gränser är kända är mer värt än
ett som antas gälla överallt.

**2. `access-register.md` bar frukt omedelbart.** Två av dagens
seriestrukturfynd — Sättnas `E I` som börjar 1895 och Våmbs `F` som börjar
1951 — hittades genom registrets kontroll nr 2, skriven samma dag i T-0092.
Registret är alltså inte dokumentation av gjort arbete utan ett verktyg som
används.

### Aktuell grind

Oförändrad i sak: den identifierade forskningen är inte utförd. Men kön
krymper med hög utdelning, och **en `OLÖST` identitet står nu inom räckhåll**
— P-0021:s ursprung har gått från *vem var hon* till *när föddes Johannes
Erikssons dotter Augusta Victoria*, med en exakt nästa källa.

### En premiss som behöver ses över

`T-0060` heter `Identifiera Augustas familj i föregående Kyrkefallabok före
1922`. Batch 392 visar att hon kom från **Mofalla**, inte Kyrkefalla, och att
hennes hushåll är ¼ mtl Bjerg. Uppgiftens premiss är alltså delvis överspelad
och bör omformuleras innan den utförs.

### Owner decision required

Ingen. Allt utfört ligger inom delegerat mandat. Det som kräver ägarbeslut är
identifierat och lämnat oläst: bouppteckningen `SE/GLA/11027/F II/12` och
dödboken `SE/GLA/13628/C/5`, som saknar exponerad åtkomstväg i katalogen.

### Rekommendation

**Ta `T-0060` härnäst, men omformulera den först** mot Mofalla `A I/4` via
ortregistret — den väg som kan lösa ursprungsfrågan. Därefter `T-0091`,
`T-0090` och `T-0093`.

- Resulting Wotan tasks: `T-0089` → DONE. Inga nya uppgifter skapade;
  `T-0060` bör omformuleras vid start.
- Portfolio signal: tre positiva originalfynd på en dag, varav två löser
  frågor som stått öppna sedan augusti, och ett tidigare nollresultat
  rättat.
- Revisit when: `T-0060`, `T-0090`, `T-0091` och `T-0093` är utförda, eller
  när P-0021:s identitet går från `OLÖST` till prövad.

## PCR-2026-09-06-013

- Record type: review
- Date: 2026-09-06
- Mode: direction-review
- Trigger: Uttrycklig prövning mot `NORTH-STAR.md` — är uppfyllelsevillkoren
  styrkta?
- Control judgement: continue

### Svaret är nej, och det är inte nära

Detta är en **uppfyllelsebedömning enligt villkor 6**, inte en
avslutningsrevision. Den visar att **målet inte är uppfyllt** och exakt var
gapen ligger. Bedömningen gäller källäget 2026-09-06.

Indikatorerna som bär bedömningen kommer ur projektets egna reproducerbara
mätningar: `node scripts/research-inventory.mjs` och
`node scripts/goal-state.mjs`.

### Villkor för villkor

| # | Villkor | Läge | Evidens |
|---|---|---|---|
| 1 | **Anlinjer** | **Delvis.** Gemensamt djup är **5** — samtliga 32 positioner på djup 5 är kända, granskade, källbredd-klara och bär giltig arkivfront. Djup 6 är **inte** behandlat: av 64 positioner är 57 kända, **6 är inte källbredd-klara** och **44 anspetsar saknar giltig arkivfront**. | `goal-state.mjs` |
| 2 | **Livsbilder** | **Nej, med bred marginal.** Av **535 personakter** har **65 en profil**; **471 är `EJ BEDÖMT`** mot PK-01–12. Av de 64 registrerade är endast **12 `GODKÄND`**, och de kräver sakrevision vid avslut. `biography: PÅGÅR 52, AVGRÄNSAD 5, INTEGRITETSMINIMERAD 7`. | `research-inventory.mjs` |
| 3 | **Identiteter och kandidater** | **Delvis.** `identity: PRÖVAT 61, OMSTRITT 1, OLÖST 2, EJ BEDÖMT 471`. De prövade är prövade på riktigt — dagens arbete flyttade P-0021 från `OLÖST` till en enda kvarstående faderskonflikt — men 471 akter är obedömda. | `research-inventory.mjs` |
| 4 | **Källtäckning** | **Delvis.** `strategy: GENOMGÅNGEN 64, EJ BEDÖMT 471`. Källtäckningsmatrisen har kvarvarande öppna och villkorliga celler, och kön innehåller nio READY-uppgifter med identifierad, genomförbar forskning. | `source-coverage.md`, `backlog.json` |
| 5 | **Spårbarhet** | **Uppfyllt för det som är gjort.** 3 191 påståenden, 2 390 markdownposter, 4 836 mediefiler; validator, mediemanifest och 29 tester gröna; evidensledet är append-only och dagens fem tillbakadragna påståenden är bevarade som `REJECTED` med historik. Detta villkor gäller kvaliteten på befintligt arbete, inte dess omfattning. | validator, `--test scripts/` |
| 6 | **Avslutningsrevision** | **Kan inte göras.** Villkor 1–4 är inte styrkta, så en revision som visar att ingen materiell åtgärd återstår vore osann. Nio READY-uppgifter och en ONGOING står i kön, alla med konkret identifierad forskning. | `backlog.json` |

### Det dominerande gapet

**Villkor 2.** 471 av 535 personakter saknar helt en bedömning mot
personkontraktet. Det är inte ett dokumentationsproblem utan ett
forskningsproblem: north star kräver en prövad livsbild för **varje
identifierad person**, och de 471 är i huvudsak sidopersoner och äldre
akter som aldrig har prövats mot PK-01–12.

Det är också det gap som växer när nya generationer läggs på. Villkor 2:s
egen formulering — *biografiska luckor får inte skjutas undan på obestämd
tid av nya anor* — talar direkt mot att gå vidare mot djup 6 innan
livsbildsskulden har en plan.

### Vad dagens arbete faktiskt flyttade

- **Gemensamt djup 4 → 5.** Djup 5:s sista ogiltiga arkivfront, P-0021, fick
  en giltig sådan sedan hennes födelsenotis identifierats.
- **`OLÖST` 3 → 2** i identitetsmåttet.
- Två personer fick sina första samtida vigselposter, en fick sin
  födelsenotis, och fem påståenden — inklusive tre av mina egna från samma
  dygn — upphävdes på ny evidens.

En regression infördes och rättades i samma pass: statusen
`IDENTITET OMSTRIDD` finns inte i north stars vokabulär och gjorde djup 5
obehandlat tills den rättades till `IDENTITET OLÖST` med uttrycklig
förklaring att statusen avser **faderns** identitet, inte hennes egen.

### Owner decision required

Ingen för fortsatt arbete. Men **en riktningsfråga bör lyftas** när
nuvarande kö är tömd: villkor 2 kräver antingen en systematisk
livsbildsvåg över de 471 obedömda akterna eller en uttrycklig, motiverad
avgränsningsregel för sidopersoner. North star tillåter en
kohort-/omprövningsregel men **förbjuder permanent dispens**. Vilken väg som
väljs är en styrningsfråga, inte en rutinåtgärd.

### Rekommendation

Fortsätt kön i denna ordning: **`T-0060`:s Attebysteg** (avgör P-0021:s
faderskap), därefter **`T-0091`**, **`T-0090`** och **`T-0093`**, som alla
är ohindrade och härrör ur kontraktsgranskningen. Ta upp
livsbildsfrågan för de 471 när kön är tömd.

- Resulting Wotan tasks: inga nya. `T-0060` fortsätter.
- Portfolio signal: gemensamt djup ökade för första gången sedan
  kontraktsgranskningen infördes.
- Revisit when: kön är tömd, eller när villkor 2:s avgränsningsregel ska
  beslutas.

## PCR-2026-09-07-014

- Record type: review
- Date: 2026-09-07
- Mode: checkpoint
- Trigger: T-0060 avslutade en generationsfråga och införde en ny generation i
  modellen. Ny prövning mot `NORTH-STAR.md` för källäget 2026-09-07.
- Control judgement: continue, redirect

### Svaret är fortfarande nej, men gapet har flyttat form

Detta är en **uppfyllelsebedömning enligt villkor 6**, inte en
avslutningsrevision. Bedömningen gäller källäget 2026-09-07 och bygger på
`node scripts/goal-state.mjs` och `node scripts/research-inventory.mjs`.

### Villkor för villkor

| # | Villkor | Läge | Evidens |
|---|---|---|---|
| 1 | **Anlinjer** | **Delvis.** Gemensamt djup är **5**. Djup 6: av 64 positioner är **58 kända**, **58 granskade** (var 57), **51 källbredd-klara** och **38 anspetsar saknar giltig arkivfront** (var 44 den 6:e, 39 i morse). Djup 7 har 44 kända, två fler än i går. | `goal-state.mjs` |
| 2 | **Livsbilder** | **Nej, med bred marginal och oförändrad proportion.** Av **538 personakter** har **67 en profil**; **471 är `EJ INFÖRT`** mot PK-01–12. Av de 67 registrerade är **12 `GODKÄND`** och **55 `UNDERKÄND`**. Bland de bedömdas 670 temaceller är **185 `ÖPPET`**. | `research-inventory.mjs` |
| 3 | **Identiteter och kandidater** | **Delvis.** `identity: PRÖVAT 64, OMSTRITT 1, OLÖST 2, EJ BEDÖMT 471`. Dagens arbete gjorde en `OLÖST` fråga fastställd — P-0536:s ursprung — utan att skapa någon ny. | `research-inventory.mjs` |
| 4 | **Källtäckning** | **Delvis.** Sju personer på djup 6 är inte källbredd-klara, varav tre är dagens tre nya akter. Kön har nio READY och en ONGOING, alla med identifierad genomförbar forskning. | `source-coverage.md`, `backlog.json` |
| 5 | **Spårbarhet** | **Uppfyllt för det som är gjort.** 3 236 påståenden, 2 410 markdownposter, 4 836 mediefiler; validator, mediemanifest och 29 tester gröna. Dagens två rättelser fördes in som **tillagda avsnitt** i C-1001 och C-1005, inte som ändrad avskrift, och det upphävda A-3743 står kvar som `SUPERSEDED`. | validator, `--test scripts/` |
| 6 | **Avslutningsrevision** | **Kan inte göras.** Villkor 1–4 är inte styrkta. | `backlog.json` |

### Det som ändrades i dag, och vad det visade

Åtta forskningspass i T-0060 stängde en generationsfråga: P-0021:s mor fick
akt, ursprung, föräldrar och en fastställd härkomst. Måttet flyttade sig
måttligt — djup 6 gick från 39 till 38 osökta fronter — men **passet blottade
var djup 6 faktiskt sitter fast**.

**Av de 38 anspetsarna saknar 35 enbart `återaktiveringsvillkor`.** Två saknar
hela `## Slutstatus`, och en (P-0474) saknar flera fält. Det ser ut som
formalia och är det inte: north star kräver av varje front att den anger
**förväntad källa, genomsökt omfång, bevarad negativ kontroll och
återaktiveringsvillkor**. Utan det sista säger fronten inte vad som skulle
öppna den igen — och en front som inte kan återöppnas är inte en front utan
ett avslut.

Det är därför **djup 6 är blockerat av 38 personer som var och en behöver en
saklig frontprövning**, inte av ny arkivforskning.

### Aktuell grind

Styrregeln pekar entydigt: nästa skiva är **djup 6**. Den skivan har två
delar, och den ena är mycket större än den andra:

- **38 anspetsar utan giltig arkivfront** — 15 på Sverkers sida, 23 på
  Kristinas. Ohindrat, materiellt, och det som ensamt håller gemensamt djup
  kvar på 5.
- **7 personer som inte är källbredd-klara** — sex av dem täcks redan av
  `T-0083`, den sjunde är dagens P-0536.

### Villkor 2 kvarstår oförändrat

De 471 obedömda akterna är exakt lika många som i går. Dagens tre nya
profiler höjde `withProfile` från 64 till 67 därför att tre **nya** personer
skapades med profil — inte därför att skulden minskade. Riktningsfrågan från
PCR-2026-09-06-013 står kvar och blir mer angelägen för varje generation som
läggs på: **systematisk livsbildsvåg eller uttrycklig kohortregel.** North
star tillåter det senare men förbjuder permanent dispens.

### En metodvinst värd att bevara

Tre pass i rad avgjordes av samma sak i olika skepnad: **läs källans egen
ingång innan du bläddrar.** Blanketten före texten (C-1003), den avgörande
raden i närbild (C-1006), registret i stället för volymen (C-1007). Det sista
kostade en onödig kartläggning av 167 bilder. Regeln är införd i
[C-1007](genealogy/citations/C-1007-arebolet-hushallet-funnet-ursprunget-faststallt.md)
och i källakten för volymen.

### Owner decision required

Ingen för fortsatt arbete. Riktningsfrågan om villkor 2 kvarstår enligt
PCR-2026-09-06-013.

### Rekommendation

**Byt fokus från enskild gren till skivan.** T-0060 har levererat sitt
kunskapsresultat och bör avslutas när dess kvarvarande steg omfördelas.
Skapa två avgränsade uppgifter för djup 6:s frontprövning, en per sida, och
kör dem före de kvarvarande READY-uppgifterna — de är det enda som kan flytta
gemensamt djup från 5 till 6.

- Resulting Wotan tasks: se PCD-2026-09-07-014.
- Portfolio signal: djup 6:s granskningsgrad är nu 58 av 58; det som återstår
  där är fronter, inte konsolidering.
- Revisit when: djup 6 är behandlat, eller när villkor 2:s avgränsningsregel
  ska beslutas.

## PCD-2026-09-07-014 — Två avgränsade uppgifter för djup 6:s arkivfronter

- Datum: 2026-09-07
- Beslutsunderlag: PCR-2026-09-07-014
- Beslut: **godkänd inom delegerad myndighet.** Djup 6:s 38 anspetsar utan
  giltig arkivfront delas i två uppgifter efter sida, så att ingen uppgift
  växer obegränsat och balansen mellan föräldrarnas släkter kan mätas:
  - **T-0094 (M)** — Sverkers sida, 15 anspetsar: P-0082, P-0125, P-0126,
    P-0131, P-0132, P-0145, P-0148, P-0159, P-0214, P-0289, P-0470, P-0471,
    P-0472, P-0474, P-0519.
  - **T-0095 (M)** — Kristinas sida, 23 anspetsar: P-0341, P-0342, P-0343,
    P-0350, P-0351, P-0361, P-0362, P-0363, P-0371, P-0372, P-0375, P-0376,
    P-0384, P-0386, P-0387, P-0403, P-0404, P-0415, P-0447, P-0448, P-0451,
    P-0452, P-0454.
- **Omfång:** varje person får en **saklig** frontprövning som avgör om den
  redovisade avgränsningen håller, och därefter en `## Slutstatus` med alla
  fyra fält north star kräver.
- **Uttryckliga uteslutningar:** ingen ny arkivforskning bakåt om föräldrar
  inom dessa uppgifter; ingen ändring av statusklass utan nytt belägg; ingen
  mallformulering av återaktiveringsvillkor. Om en frontprövning visar att en
  status är sakligt fel skapas det som eget arbete och ändras inte i
  förbigående.
- **Verifierbart utfall:** `node scripts/goal-state.mjs` visar noll anspetsar
  utan giltig arkivfront på respektive sida på djup 6, **och** varje ändrad
  akt har en daterad motivering i forskningsloggen som visar vad som prövades.
- Resulting Wotan tasks: `T-0094` READY; `T-0095` READY.
- Reaktiveringsvillkor: när båda är DONE mäts gemensamt djup om. Om det inte
  går från 5 till 6 ska skillnaden förklaras innan nytt arbete väljs.
