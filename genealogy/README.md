# Forskningsstruktur och provenans

## Mappar och identifierare

- `people/P-NNNN-*.md` — personakter med påståenden och evidensbedömning.
- `sources/S-NNNN-*.md` — bibliografisk beskrivning av en källa eller volym.
- `citations/C-NNNN-*.md` — exakt ställe i en källa och relevant avskrift.
- `research-log/YYYY-MM-DD.md` — kronologisk söklogg, även negativa resultat.
- `media/` — hämtade bilder; filnamn börjar med citationens id och åtföljs av
  kontrollsumma i citationsakten.
- `exports/` — härledda utbyten, exempelvis GEDCOM. Exporter är inte
  evidensbärande original.

Identifierare återanvänds aldrig. En personakt kan innehålla flera motstridiga
påståenden; källorna avgör vilket som senare bedöms som bäst styrkt.

## Evidensstatus

- `LEAD` — ledtråd som ännu inte verifierats i oberoende källa.
- `TRANSCRIBED` — avläst ur angiven källa men ännu inte identitetsprövad.
- `CORROBORATED` — stöds av minst två självständiga eller kompletterande belägg.
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

1. Registrera inkommande uppgift som `LEAD` med provenans.
2. Sök närmast primära källa och logga både träffar och relevanta nollresultat.
3. Skapa källakt och citationsakt innan påståendet uppgraderas.
4. Transkribera det som faktiskt står; normalisera först i ett separat fält.
5. Kontrollera identiteten i hushålls-, flyttnings- eller annan kompletterande
   källa innan personer med samma namn slås samman.
6. Exportera endast härledda, verifierade data till GEDCOM.

## Utgåvegrind för T-0012

Nästa gemensamma Adam/Axel-utgåva ska bli jämnt rikare och gå en balanserad
generation djupare än den första rapporten. Arbetet går därför breddförst över
den fasta 32-personerskohorten: varje person ska få en central källryggrad och
alla sakligt relevanta Riksarkivet-källfamiljer ska användas eller få ett exakt
dokumenterat hinder innan en lätt gren drivs djupare. Folkräkningar,
husförhör/församlingsböcker, flyttning, vigsel, död, bouppteckning, mantal och
yrkesutlösta serier används för biografiska helheter, inte bara ankoppling.

När kohorten är forskningsklar ska arbetet stanna. Ingen ny PDF, inget manifest
och ingen layout får påbörjas innan ägaren och forskningsarbetet har haft en
rejäl diskussion om innehåll, berättelse, personurval, källredovisning,
bildanvändning och visuell form. Den diskussionen ska uttryckligen ta nästa
steg från v1, inte bara upprepa dess mall.

## Integritet

Nu levande personer dokumenteras endast när de behövs för identifiering och då
med minsta nödvändiga detalj. Lösenord, aktiveringslänkar och privata kontodata
lagras aldrig i projektet.
