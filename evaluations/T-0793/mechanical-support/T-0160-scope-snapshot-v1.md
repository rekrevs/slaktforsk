# T-0160: Konsolidera befintliga akter, djup 5 sida K från P-0337

**Status**: DONE | **Size**: M

## Context och mandat

PCD-2026-09-07-026, T-0114. Sammanhängande ägarbeställd granskning av
befintliga akter; person-dossier/v1 och person-research/v1 gäller.
Maskinell risk-/djupsignal styr urval, inte sakligt utfall. Närliggande hushåll prioriteras inom samma nivå; därefter explicit restkohort. Alla personerna ska läsas individuellt mot sina befintliga källor.

## Kohortmedlemmar

P-0337, P-0367, P-0395, P-0396

## Scope och underlag

Exakt dessa 4 akter och deras profiler, med befintliga personbundna
citationer, källnoter och senare rättelser. 35 assertioner vid baslinjen.
Baslinje: T-0114-inventory.json; den anger inledande profiler, formatfel och
maskinella risksignaler. Frånvaro av signal är inget friande resultat.

Första citationsindex: C-0326, C-0371, C-0381, C-0382, C-0383, C-0384, C-0385, C-0445, C-0446, C-0447, C-0473, C-0474, C-0477, C-0478, C-0479, C-0649, C-0651, C-0806, C-0827, C-0828, C-0945, C-0989.
Följ relevanta befintliga rättelser och familjehänvisningar. Beroenden: T-0114.
Utanför: nya arkivsökningar, nya generationer och osäkra identitetssammanslagningar.
Följdfel i annan kohort rapporteras till dess befintliga Wotan-ägare.

## Acceptance Criteria

- [x] Varje akt/profil följer pilotprövat format; individuell text och länkar, inga förlorade A-id:n eller historiska observationer.
- [x] Alla personbundna aktuella slutsatser är avstämda mot relevanta befintliga belägg/rättelser, särskilt namn, datum, relationer, tidslinje och berättelse.
- [x] Varje profil har tio individuella teman och PK-01–12 med beläggsmotivering; båda färdignivåerna hålls åtskilda och verkliga luckor syns.
- [x] Personbunden eftergranskning samt följdpåverkan på anhöriga utförd. Beslutat konkret följdarbete får en avgränsad Wotan-ägare före DONE; inga tomma mallar godkänns.
- [x] Per-personutfall enligt granskningsmallen dokumenterat med granskat underlag, rättelser och kvarstående gränser.
- [x] Formatkontroll för kohorten, validator, inventering, tester och mediekontroll passerar; saklig efterkontroll redovisad separat.

## Approach

Läs wotan/templates/person-review-task.md. Inventera aktens samtliga
sakuppgifter och senare citationer; konsolidera, därefter läs färdig text
mot underlaget. Bevara kandidatgränser och OWNER_CONFIRMED. En källbunden
oläslighet är inte samma sak som aldrig utvunnen kolumn. Logga passagen en
gång med dess kriterium. Tillgodoräkna tidigare tillräckligt arbete.

## Granskningsutfall

| Person | Datum/version | Granskat underlag | Format | Konsolidering | Identitetsbedömning | Livsbildsbedömning | Rättelser/luckor och följduppgift |
|---|---|---|---|---|---|---|---|
| P-0337 Brita Stina | 2026-09-09, person-dossier/v1 | 26 äldre A samt C-0384, C-0385, C-0446, C-0474, C-0651, C-0866, C-0989 | 0 fel | A 26→33, nya A-6100–A-6106 | UNDERKÄND / AVVAKTAR | UNDERKÄND | **Överdriven oberoendeklaim återtagen:** dödsdagen 1886-10-01 sades vara bekräftad i tre oberoende kedjor; rotemansposten anger uttryckligen `Enl Db` och lysningsakten är en senare sammanställning i samma församling — dagen bärs av **en** originalpost. Tre överspelade lydelser om att ingen bouppteckningsserie kunde identifieras rättade; C-0989 pekar sedan 2026-09-06 ut volym och register. Fyra propageringsluckor slutna. Ny PK-11-brist: C-0384 och C-0385 saknar all reproduktion. T-0444, T-0445 |
| P-0367 Robert Nicolaus Fredberg | 2026-09-09, person-dossier/v1 | 3 äldre A samt C-0323, C-0382, C-0800 | 0 fel | A 3→13, nya A-6110–A-6119, första profilen | **GODKÄND / BÄRANDE** | UNDERKÄND | **Kohortens största fynd.** C-0323 och C-0800 var aldrig hänvisade i akten trots att båda bär hans egna rader; hans kända liv slutade 1888. Egen rad läst kolumn för kolumn: inflyttning från Kungsholm 1896-12-29 nr 316, koppympning, `Icke Konfirmerad`, och **utflyttning till Norra Amerika 1898-08-27**. Den påstådda födelsedagskonflikten är ett avskriftsfel — bilden läser `78 7/6`, inte 1878-06-08. `1:a b. i g. 1877` är en tryckt kolumn, inte en klammernotering. T-0443, T-0447 |
| P-0395 Frida Elisabeth Fredberg | 2026-09-09, person-dossier/v1 | 4 äldre A samt C-0473, C-0651, C-0774, C-0800, C-0945 | 0 fel | A 4→8, nya A-6150–A-6153, första profilen | **GODKÄND / BÄRANDE** | UNDERKÄND (PK-08) | Akten hänvisade inte till **tre** citationer som bär hennes egna hushållsrader. Hennes egen rad i den sparade 1900-bilden läst kolumn för kolumn: tom yrkescell, ogiftmarkering, födelseort `Här` — originalets eget stöd för Kungsholm, som registret dittills bar ensamt. Överspelad lydelse borttagen: fortsättningen efter faderns hushåll var mycket riktigt inte följd, men påståendet dolde att tre citationer redan fanns. T-0446, T-0447 |
| P-0396 Ruth Fredrika Fredberg | 2026-09-09, person-dossier/v1 | 2 äldre A samt C-0322, C-0323, C-0324, C-0651, C-0800 | 0 fel | A 2→10, nya A-6160–A-6167, första profilen | **GODKÄND / BÄRANDE** | UNDERKÄND (PK-08) | Hela Hudiksvallstiden låg oläst i en sparad bild: inflyttning 1896-12-29 nr 317, konfirmation 1900-04-27, nattvard 29/4, och **utflyttning till N. Amerika 1900-08-22 nr 93**. Akten påstod att fortsättningen efter 1895 inte följts. Falsk modersuppgift i själva källan fångad och hållen som `CONFLICT`. C-0322 identifierad som utdrag ur den bok den skulle bekräfta. T-0443, T-0447 |

### Vad kohorten faktiskt visade

**Två utvandringar låg olästa i projektets eget material.** C-0323:s sparade
fullbild bär tre brorsbarnsrader. Citationens avskrift behandlar uttryckligen
bara födelseuppgiften för två av dem och lämnar deras egna kolumner orörda.
I de kolumnerna står hela deras Hudiksvallstid och slutet på den: Robert
Nikolaus utflyttad till **Norra Amerika 1898-08-27**, Ruth Fredrika till
**N. Amerika 1900-08-22 med utflyttningsnummer 93**, båda inflyttade från
Kungsholm samma dag 1896-12-29 med löpnumren 316 och 317. Hans akt slutade
1888; hennes påstod att fortsättningen efter 1895 inte följts. Två oberoende
agenter läste samma bild och kom till samma resultat, och läsningen är
därefter kontrollerad centralt vid förstoring. **Ingen ny arkivpassage
behövdes för att flytta två personers kända liv med tolv respektive fem år.**

**Källan innehöll själv ett släktskapsfel.** Under Robert Nikolaus rad står
noteringen `Dotter of Stationskarlsförm. Olaus Fredriksson Fredberg o. h. h.
Johanna Charlotta Jansson`. Den avser Ruth och namnger **styvmodern som mor**.
Brita Stina dog 1886-10-01 och vigseln med Johanna Charlotta ägde rum
1888-12-08, så uppgiften kan inte stämma. Den är förd som `CONFLICT` och
propageras inte. Det är skrivarens fel, inte avskrivarens, och det är just
sådana fel den kanoniska modellen ska kunna bära utan att ta över dem.

**En påstådd källkonflikt var ett avskriftsfel.** Robert Nikolaus födelsedag
har stått som 1878-06-08 i C-0323 mot 7 juni i födelseposten. Bilden läser
`78 7/6`, i samma kolumn och hand som syskonens `80 24/6` och `85 7/2`. Det är
tredje gången i programmet en registrerad konflikt visar sig vara ett fel i
projektets egen avskrift snarare än en motsägelse mellan källor.

**En dödsdag som sades vila på tre oberoende kedjor vilar på en.**
Rotemansposten för P-0337 anger uttryckligen `Enl Db` och är alltså en
avskrift av dödboken; lysningsakten 1888 är en senare sammanställning i samma
församling. Dagen 1886-10-01 är inte osäker, men den bärs av **en**
originalpost, och akten och profilen sade något annat.

**Två nollresultat utan bevarad bild.** C-0384 och C-0385 har ingen
reproduktion alls, trots exakt angivna bild-id. Ett noll som ingen kan
efterpröva är svagare än ett som kan öppnas igen — och nollresultat har i detta
program sex gånger visat sig gälla fel folio, rad, jurisdiktion, månad eller
dag. Tillsammans med de sexton saknade Hemsjökopiorna är detta enda skälet
till att P-0337:s identitetsnivå är underkänd; föräldrabindningen i sig bärs av
två oberoende samtida original.

**Täckningsöversikten visste mer än akterna — och tvärtom.**
`genealogy/source-coverage.md` listade båda systrarna korrekt på raden för
folkräkningen 1890, medan **ingen av deras akter hänvisade till citationen**.
Samma tabells rad för Hudiksvallssidan listade omvänt bara en av de tre
personer vars egna rader står på uppslaget. Iakttagelsen gav upphov till en
maskinell mätning över hela korpusen: **404 (person, citation)-par i 138 akter**
där täckningstabellen kopplar en källa till en person vars akt inte hänvisar
till den. Det är en kandidatlista, inte en fellista — en rad kan gälla en
negativ kontroll — men det är den första maskinella signalen som pekar ut var
programmets vanligaste defektklass sannolikt sitter. Förd till T-0115.

## Verification och Outcome

Kört 2026-09-09 efter att samtliga fyra akter, fyra profiler och de centrala
följdrättelserna var på plats:

- `node scripts/person-format.mjs P-0337 P-0367 P-0395 P-0396` — **0 formatfel**.
- Kohortkontroll (A-id-behållning mot HEAD, H2-ordning, profilfält, kvarvarande
  `EJ BEDÖMT`/`EJ GRANSKAT`, sammantryckt text, bruten påståendetabell,
  relationstabell utan `Tid/plats`) — **OK** för alla fyra.
- `node scripts/validate-genealogy.mjs` — **OK: 4364 assertions; 2731
  Markdown-poster; 5065 mediefiler; Wotan-JSON giltig.**
- `node scripts/research-inventory.mjs --check` — **Strukturfel: 0.**
  Identitetsgranskning GODKÄND 80. Trädverkan BÄRANDE 78.
- `node --test scripts/` — **50 av 50 passerar.**
- `node scripts/media-manifest.mjs --check` — **OK**, 5064 mediefiler.
- Falska släktkanter, båda klasserna — **0 kvarstående**.
- A-id-behållning i hela `genealogy/people` mot HEAD — **inget A-id förlorat.**

Tre läsningar i C-0323 är oberoende kontrollerade centralt mot originalbilden:
de två utflyttningscellerna till Nordamerika, inflyttningsdagen 29/12 1896 för
båda syskonen, och födelsedagen `78 7/6`. Alla tre bekräftades. Att två
agenter oberoende av varandra läste samma rader och kom till samma resultat
väger tyngre än en enskild läsning.

**Outcome.** Kohortens fyra akter följer person-dossier/v1 och har var sin
profil. **Tre av fyra når identitetsnivån.** P-0337 gör det inte, och hennes
spärr är uteslutande bevarandeskuld — två nollresultat utan bild och sexton
saknade kopior — inte någon osäkerhet om föräldrabindningen. **Uppgiften är
klar; personerna är det inte:** livsbildsnivån är underkänd för alla fyra.
Fem avgränsade följduppgifter T-0443–T-0447 är skapade, samtliga BLOCKED bakom
T-0115. Nio citationstillägg och en rättad rad i
`genealogy/source-coverage.md` med bevarad ersatt lydelse. En ny maskinell
mätning av propageringsluckor är förd till slutrevisionen T-0115.

## Återupptagning — avslutad

- Uppdaterat: 2026-09-09.
- Utfört: samtliga fyra akter och profiler konsoliderade och verifierade;
  fem följduppgifter skapade; batch 565 loggad; uppgiften DONE.
- Nästa ej utförda steg: inget inom denna uppgift. T-0443 följer de två
  utvandringarna vidare och T-0444 stänger P-0337:s enda kvarvarande spärr
  utan ny arkivåtkomst.
- Hinder: inga.


## Följdavstämning T-0128, 2026-09-08

P-0367 A-2066 rättad i kommentaren: egen dopdag8 juli1878, C-0474:s möjliga
7/7 avvikande. C-0382:s fulla fadderfält och faderns datum4 september1852
är omlästa. P-0395 A-3553 jämförs med senare familjeförteckning C-0474,
inte en oläst egen födelsenotis. C-0474 ger även prövade dopnoter för
Johannes/Frida/Ruth; dessa får inte behandlas som nyöppnade doporiginal.
Fulla profiler införs här; ingen av dessa minimala följder räknas fullgranskad.

## Återupptagning — minimal anhörigföljd från T-0136

2026-09-08: P-0337: fem syskon rättade enligt C-0446, eget dopnätverk utvunnet C-0445, överlagrat hushållsdatum inte oberoende exakt dagstöd. Föräldrabokperiod1849–1860 ej till1877. Full individuell prövning kvar.
Detta är inte full individuell granskning och räknas inte ytterligare i538-täckningen.
