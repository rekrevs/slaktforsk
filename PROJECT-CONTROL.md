# Project control log

- Protocol: `project-control/v0.1`

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
