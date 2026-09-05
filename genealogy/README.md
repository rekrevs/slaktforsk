# Forskningsstruktur och provenans

## Mappar och identifierare

- `people/P-NNNN-*.md` — personakter med påståenden och evidensbedömning.
- `research-profiles/P-NNNN.md` — frågor, tio livsteman, söknycklar,
  källvägar och slutgranskning enligt [personkontraktet](person-contract.md).
- `source-contexts/` — återanvändbar ort-/tids-/arkivrouting när flera
  personer delar källor; aldrig personbelägg eller parallell arbetskö.
- `research-inventory.json` — härledd strukturell inventering av alla P-id:n;
  byggs med `node scripts/research-inventory.mjs --write`.
- `sources/S-NNNN-*.md` — bibliografisk beskrivning av en källa eller volym.
- `citations/C-NNNN-*.md` — exakt ställe i en källa och relevant avskrift.
- `research-log/YYYY-MM-DD.md` — kronologisk söklogg, även negativa resultat.
- `identity-review-YYYY-MM-DD.md` — tvärgående konsolideringsrevisioner av
  namnformer, personidentiteter, felaktiga sammanslagningar och skyddade
  kandidatgränser.
- `## Arbetsläge` i en personakt — maskinläsbart arbetsläge som
  `scripts/goal-state.mjs` läser (se nedan). Det är arbetsläge, inte fakta
  om personen.
- `media/` — hämtade bilder; filnamn börjar med citationens id och åtföljs av
  kontrollsumma i citationsakten.
- `exports/` — härledda utbyten, exempelvis GEDCOM. Exporter är inte
  evidensbärande original.

Identifierare återanvänds aldrig. En personakt kan innehålla flera motstridiga
påståenden; källorna avgör vilket som senare bedöms som bäst styrkt.

## Kunskapslager

Projektet skiljer fyra lager som inte får blandas ihop:

1. **Evidenshistorik:** källakter, citationsakter, forskningsloggar,
   strukturerade observationer och bevarade original med provenans och
   kontrollsummor.
2. **Konsoliderad personmodell:** personakterna med projektets aktuella bästa
   bedömning av identitet, händelser, relationer, konflikter och luckor.
3. **Härledda slutsatser:** den verifierade antavlan, rapporter, index och
   exporter som byggs från personmodellen.
4. **Arbetsläge:** Wotan, personprofiler, forskningsfront, täckningsmatris och
   personakternas `## Arbetsläge` som anger vad som ska göras eller
   granskas, inte vad som är sant om en person. Utförbart arbete och
   återupptagning hör till Wotan enligt [konventionen](../wotan/README.md).
   Registrerade indikatorer räknas ut med `node scripts/goal-state.mjs`;
   se `NORTH-STAR.md`, avsnittet Framstegsmått och deras begränsning.

Forskningsprofilernas kunskapsläge är skilt från Wotans utförandestatus.
De konkretiserar PK-01–12 och ska finnas för berörda akter vid ny forskning.
Alla akter, också de som ännu saknar profil, visas i `research-inventory`.
Den maskinella kontrollen prövar struktur, inte beläggens sakliga styrka.
Äldre GRANSKAD/KLAR tillgodoräknas endast för faktiskt styrkt omfång, inte
som ett automatiskt godkännande av nya krav. Se [arbetsprogrammet](research-plan.md).

### Avsnittet `## Arbetsläge`

Varje personakt får bära ett avsnitt `## Arbetsläge` med följande rader:

```markdown
## Arbetsläge

- Konsolidering: `GRANSKAD` 2026-09-04 (identity-review-2026-09-04.md)
- Källbredd: `INTEGRITETSMINIMERAD`
```

- `Konsolidering` är `GRANSKAD` med datum och hänvisning när identitets- och
  konsolideringspasset i forskningsprogrammet har gjorts och akten bedöms
  avse en enda verklig person, annars `EJ GRANSKAD`. Saknat avsnitt betyder
  `EJ GRANSKAD`. Om identiteten senare revideras sätts raden tillbaka till
  `EJ GRANSKAD` tills passet har gjorts om.
- `Källbredd` är valfri och används bara när källtäckningsmatrisen inte har
  en rad för personen: `INTEGRITETSMINIMERAD` för sannolikt levande personer
  och `KLAR` med motivering i akten när ingen relevant källfamilj återstår.
  Annars avgör matrisraden den administrativa indikatorn: inga oprövade
  högprioriterade (`1`) celler. Saklig källbredd kräver även prövning av
  villkorliga vägar enligt NORTH-STAR.md. Ett KLAR-fält får inte åsidosätta
  öppna frågor i matrisen; avvikande kod ska rättas, inte legitimera avslut.
- Anspetsar och personer med bara en känd förälder bär dessutom
  `## Slutstatus` enligt reglerna i `scripts/lib/terminal-status.mjs`.

Slutstatusens strukturkontroll kräver exakt en Status-rad, en förväntad
källa, genomsökt omfång och ett icke-tomt `Återaktivera när`-fält.
`VERIFIERAD` kräver dessutom `Belägg` med en giltig länk till en befintlig
C-post; övriga statusar kräver `Negativ kontroll` med sådan länk.
Fortsättningsrader i fält ska vara indragna. Tomma värden kan inte ersättas
av nästa punkt eller ett senare avsnitt. Etiketten ensam räcker aldrig.
Detta testar struktur och referens, inte om källan faktiskt bär slutsatsen.
Personer med två etablerade föräldrar behöver ingen slutstatus för den
föräldrafrågan; `OWNER_CONFIRMED`-relationer består utan nya arkivkrav.

En befintlig källtäckningsrad har alltid företräde framför Källbredd-fältet,
även för `INTEGRITETSMINIMERAD`. Utan matrisrad får den etiketten användas
för integritetsminimerad behandling; `KLAR` kräver skriven motivering efter
etiketten, på samma eller en indragen fortsättningsrad. Ett datum ensamt är
ingen motivering. Frånvaro av prioritet 1 är endast en registrerad indikator;
villkorliga 2-celler kan fortfarande dölja materiellt arbete som måste prövas.

Vid en **ny personövergripande avslutsbedömning** krävs dessutom GODKÄND
kontraktsgranskning enligt PK-01–12. En begränsad källa eller temapassage
får vara genomgången medan personens övriga frågor består. Äldre KLAR och
matrisceller får behållas som registrerad historik men är inte en dispens
från detta krav. Inventeringen redovisar den skillnaden utan att ändra
etablerade släktrelationer.

Evidenshistoriken är append-only. När en bevarad observation visar sig vara
felavläst, felkopplad eller ofullständig ska den ligga kvar och en ny
korrigerande observation skapas med länk till det den ersätter eller motsäger.
En senare slutsats får inte tyst ändra källans tidigare ordalydelse eller
provenans. Rent tekniska rättelser som inte ändrar observationens innebörd kan
göras i filen, men semantiska rättelser ska lämna en synlig historik.

Personmodellen är däremot reviderbar och ska hållas konsoliderad. Nya belägg
ska vägas mot tidigare uppgifter, dubbletter ska förenas utan att evidens
försvinner och konflikter ska lösas eller lämnas uttryckligt öppna. Rapporter
och exporter får aldrig behandlas som fristående evidens när underliggande
personmodell har ändrats.

## Identitetsintegritet

En personakt motsvarar en verklig person, inte ett namn eller en sökträff.
Sammanföring kräver en dokumenterad bedömning av namnformer, datum och ålder,
geografi och flyttkedja, hushåll och familjerelationer samt yrke eller andra
identifierande omständigheter. Likhet i enstaka fält räcker inte.

Om uppgifter kan avse olika personer hålls kandidaterna i separata personakter
eller som tydligt åtskilda hypoteser tills identiteten är avgjord. Om en
sammanblandning upptäcks ska akten delas, varje observation knytas om med
synlig historik och alla beroende relationer och slutsatser granskas på nytt.
En möjlig sammanslagning får inte genomföras bara för att göra antavlan
komplett.

Relationer med status `LEAD`, `CONFLICT` eller `REJECTED` får inte ingå i den
verifierade antavlan. `TRANSCRIBED` beskriver vad en källa säger men räcker
inte ensamt när själva identiteten eller relationskopplingen är materiellt
osäker. `OWNER_CONFIRMED` är däremot fastställd projektinformation när ägaren
uttryckligen har sagt att uppgiften är säker. Den behöver inget ytterligare
arkivbelägg för att användas, men måste länkas till ett Project Control Decision
och förbli spårbar som ägarkunskap.

## Evidensstatus

- `LEAD` — ledtråd som ännu inte verifierats i oberoende källa.
- `TRANSCRIBED` — avläst ur angiven källa; identitetsbedömningen redovisas
  separat och får inte antas enbart av denna status.
- `CORROBORATED` — stöds av minst två självständiga eller kompletterande belägg.
  Etiketten är inte en fullständig bevisstandard: redovisa beroende per
  informationsuppgift, relevanta alternativ och konflikter i frågans bedömning.
- `OWNER_CONFIRMED` — uttryckligen säker familjekunskap från projektägaren,
  bevarad i ett Project Control Decision; sann i projektets kanoniska modell.
- `CONFLICT` — motsägs av annan uppgift och kräver analys.
- `REJECTED` — prövad och bedömd felaktig; behålls för spårbarhet.

Tillförlitlighet anges separat som `hög`, `medel` eller `låg`. En exakt avskrift
kan exempelvis vara säker samtidigt som kopplingen till rätt person är osäker.

## Påståenden

Varje personakt har en tabell med följande fält:

| ID | Påstående | Status | Tillförlitlighet | Belägg | Kommentar |
|---|---|---|---|---|---|

Påståenden formuleras atomärt: namn, datum, plats, relation och yrke är skilda
uppgifter när källan tillåter det. Slutsatser och normaliseringar skiljs från
ordalydelsen i källan.

## Biografisk täckning

Personakterna ska bevara alla sakligt relevanta uppgifter som påträffas om de
undersökta personerna, inte bara födelse, vigsel och död. När källorna medger det
registreras även:

- samtliga namnformer, smeknamn, patronymikon och namnbyten,
- föräldrar, makar, barn, syskon, faddrar, vittnen och andra dokumenterade
  relationer,
- boställen, fastigheter, adresser, gårds- och bynamn samt flyttningar,
- yrken, titlar, arbetsgivare, utbildning, läskunnighet och ekonomisk ställning,
- militärtjänst, värnplikt, sjömanshus och tjänstenummer,
- kyrkliga händelser, konfirmation, nattvard och anmärkningar,
- medborgarskap, migration, emigration och resor,
- bouppteckning, arv, jord, skulder och andra egendomsuppgifter,
- domstols-, fattigvårds- och kommunala handlingar,
- sjukdom, funktionsnedsättning och dödsorsak när det framgår av historisk källa,
- fotografier, signaturer, brev, nekrologer och muntliga minnen,
- tidslinje, hushållssammansättning och en källstödd biografisk berättelse.

Även ovanliga detaljer sparas när de hjälper identifikation eller livsberättelse.
Varje uppgift får ett eget påstående eller en tydligt avgränsad källnot. Frånvaro
i en källa formuleras aldrig som faktisk frånvaro utan särskild analys.

Insamlingen är opportunistisk: när en källa visar namngivna föräldrar, makar,
syskon eller barn skapas personakter även om personerna ligger utanför den
aktuella kärnantavlan. Grunduppgifterna och källrelationen bevaras direkt så
att sidogrenar inte behöver återskapas senare. Privatmarkerade eller sannolikt
levande personer dokumenteras fortfarande enligt minimeringsregeln nedan.

## Full Riksarkivet-hänvisning

En citationsakt för en digital kyrkobok ska så långt materialet medger innehålla:

1. arkivinstitution och arkivbildare,
2. arkivets referenskod,
3. serie och volymsignum,
4. volymens tidsomfång,
5. uppslag/sida samt Riksarkivets bildnummer,
6. beständigt bild-id och direkt URL,
7. datum då bilden lästes,
8. ordagrann eller diplomatisk avskrift,
9. normaliserad tolkning,
10. läsosäkerheter markerade med `[?]` och oläsligt som `[…]`,
11. lokal bildfil och SHA-256 om en kopia hämtas,
12. vilka atomära påståenden som belägget stöder eller motsäger.

Exempel på kortform i löptext:

> Riksarkivet, Vindelns kyrkoarkiv (Degerfors kyrkoarkiv),
> SE/HLA/1010028, C:volym, uppslag/sida, bild-id, läst 2026-08-19.

## Anspetsrevision

`node scripts/ancestor-audit.mjs` räknar probandens anor per generation och
listar varje ana som saknar kända föräldrar. När en avslutad våg granskas men
nästa djup redan har registrerats används exempelvis
`node scripts/ancestor-audit.mjs --through-depth=5`; då krävs slutstatus genom
djup 5 medan djup 6 redovisas som öppen front. Utan flaggan granskas alla djup.

## Reproducerbar åtkomst

Hur Riksarkivets sök-API, IIIF-manifest och bildhämtning används, vilka
volymer som är fritt åtkomliga respektive kräver inloggning samt
volymkoderna för folkräkningen beskrivs i
[`method-riksarkivet.md`](method-riksarkivet.md).

## Arbetsflöde

Detta är evidenshanteringen inom [forskningsprogrammets](research-plan.md)
person-/hushållscykel. Val av källor och följdsökningar styrs av
[källstrategin](source-strategy.md); resultatet prövas mot PK-01–12.

1. Registrera inkommande uppgift som `LEAD` med provenans.
2. Sök närmast primära källa och logga både träffar och relevanta nollresultat.
3. Skapa källakt och citationsakt innan påståendet uppgraderas.
4. Transkribera det som faktiskt står; normalisera först i ett separat fält.
5. Kontrollera identiteten i hushålls-, flyttnings- eller annan kompletterande
   källa innan personer med samma namn slås samman.
6. Konsolidera nya observationer mot personens hela akt: hitta dubbletter,
   pröva kronologi och geografi, väga konflikter och uppdatera den aktuella
   slutsatsen utan att skriva om evidenshistoriken.
7. Om identiteten eller en bärande relation ändras, identifiera och återpröva
   antavla, personer och andra slutsatser som beror på den.
8. Exportera endast härledda, verifierade data till GEDCOM.

## Utgåvegrind

Utgåvor är separata, uttryckligen beslutade leveranser med fast omfång i
Wotan. Historisk djup-5-kohort och dess passerade utgåvegrind finns i
PCD-2026-08-23-001 och PCD-2026-09-04-002 i
[Project Control](../PROJECT-CONTROL.md). T-0012 är inte en aktuell
startinstruktion. För kommande utgåvor gäller följande principer.

Arbeta breddförst över utgåvans beslutade kohort: varje person ska få en
central källryggrad och alla sakligt relevanta Riksarkivet-källfamiljer
ska användas eller få ett exakt
dokumenterat hinder innan en lätt gren drivs djupare. Folkräkningar,
husförhör/församlingsböcker, flyttning, vigsel, död, bouppteckning, mantal och
yrkesutlösta serier används för biografiska helheter, inte bara ankoppling.

Kohorten är inte forskningsklar bara för att observationer har samlats in.
Varje person ska också ha genomgått en identitets- och konsolideringsgranskning:
akten ska avse en person, bärande relationer ska vara prövade, observationer
och slutsatser ska gå att skilja åt, och materiella konflikter eller luckor ska
vara lösta eller uttryckligt redovisade. Ingen osäker relation får öppna nästa
anled som etablerad.

Ingen ny PDF, inget manifest och ingen layout får påbörjas innan
innehåll, berättelse, personurval, källredovisning, bildanvändning och visuell
form har beslutats enligt [forskningsprogrammets utgåvegrind](research-plan.md#utgåvegrind).
Ett redan dokumenterat beslut ska inte efterfrågas igen utan saklig anledning.

## Integritet

Nu levande personer dokumenteras endast när de behövs för identifiering och då
med minsta nödvändiga detalj. Lösenord, aktiveringslänkar och privata kontodata
lagras aldrig i projektet.
