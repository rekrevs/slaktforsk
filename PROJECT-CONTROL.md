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
