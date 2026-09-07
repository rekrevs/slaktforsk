# North star — daterad uppfyllelserevision 2026-09-07

Denna revision prövar projektet mot **var och en** av de sex villkoren i
`NORTH-STAR.md`, avsnittet *Villkor för uppfyllelse*, och redovisar för varje
villkor det mätta läget, beläggen och den konkreta återstoden.

Revisionen är gjord efter batcharna 467–479 samma dag. Samtliga siffror är
avlästa ur `node scripts/goal-state.mjs`, `node scripts/research-inventory.mjs`
och `node scripts/validate-genealogy.mjs` vid revisionstillfället.

> **Sammanfattande utfall: north star är inte uppfylld.** Fyra villkor är
> otvetydigt ouppfyllda, ett är delvis uppfyllt men inte verifierat, och det
> sjätte kan därför inte uppfyllas. **Ingen av luckorna beror på ett
> konkret externt hinder** — samtliga har genomförbart arbete kvar.

## Mätt läge vid revisionen

| Indikator | Värde |
|---|---|
| Registrerat gemensamt djup | **5** |
| Djup 6 | 58 kända av 64, 51 källbredd-klara, **behandlad: nej** |
| Djup 7 | 44 kända av 128, 42 källbredd-klara, 1 osökt front ≤ djup |
| Djup 8 | 2 kända av 256, 2 öppna positioner, 1 osökt front ≤ djup |
| Personakter | 538 |
| Forskningsprofiler | **97** av 538 |
| Citat | 1 072 |
| Källor | 782 |
| Påståenden | 3 514 |
| Mediefiler med kontrollsumma | 4 835 |
| Wotan | 88 DONE, 1 ONGOING, 12 READY, 1 BLOCKED, 7 IDEA |

## Villkor 1 — Anlinjer

**Ouppfyllt.**

Registrerat gemensamt djup står på **5**. Djup 6 är inte behandlad: på
**Sverkers sida är 22 av 29 kända personer källbredd-klara**, mot Kristinas
**29 av 29**. De sju återstående är namngivna med sina oprövade celler:

| Person | Oprövade celler |
|---|---|
| P-0082 Jonas Andersson i Buberget | `F` `H` `V` `D` |
| P-0123 Johan Petter Urbom | `D` `B` `T` `O` |
| P-0126 Brita Kajsa Pehrsdotter | `D` `B` `T` `J` |
| P-0131 Adolf Fredrik Jansson | `D` `B` `T` |
| P-0132 Eva Lotta Jonsdotter | `D` `B` `T` |
| P-0519 Ulrika Lovisa Jonsdotter i Buberget | `F` `H` `V` `D` |
| P-0536 Maja Greta Larsdotter | **ingen matrisrad** |

Balanskravet är därmed **inte** uppfyllt på djup 6, och obalansen ligger
entydigt på Sverkers sida. Dagens arbete (batcharna 474–479) låg medvetet
där.

Två arkivfronter skrevs i dag — P-0082 och P-0519 — vilket förde
*anspetsar utan giltig arkivfront* på djup 6 från **2 till 0**. Det är en
delmängd av villkoret, inte villkoret.

Djup 7 och 8 är i praktiken oöppnade: 44 respektive 2 kända positioner, och
84 respektive 252 stängda. Batch 479 öppnade **två nya positioner på djup 7**
(Jan Andersson och Anna Stina Jonsdotter i Kartorp) som ännu inte är
registrerade; det arbetet ligger i `T-0109`.

## Villkor 2 — Livsbilder

**Ouppfyllt, och detta är projektets största enskilda lucka.**

`research-inventory` ger livsbildsläget:

| Läge | Antal |
|---|---|
| PÅGÅR | 84 |
| INTEGRITETSMINIMERAD | 7 |
| AVGRÄNSAD | 5 |
| **EJ BEDÖMT** | **442** |

**442 av 538 personer har ingen livsbildsbedömning alls**, och endast **97**
har en forskningsprofil där de tio temana kan bedömas. Villkoret kräver att
*varje identifierad person* har en konsoliderad livsbild som uppfyller
PK-01–12 över hela den kända livstiden.

Ingen person står som färdigbedömd på livsbildsnivån. Personkontraktets två
färdignivåer (PCD-2026-09-07-021) gör detta synligt i stället för att dölja
det: identitetsnivån kan vara godkänd medan livsbilden ligger efter, och den
gör det här i stor skala.

## Villkor 3 — Identiteter och kandidater

**Ouppfyllt.**

| Mått | Värde |
|---|---|
| identity PRÖVAT | 71 |
| identity OMSTRITT | **18** |
| identity OLÖST | 7 |
| identity EJ BEDÖMT | **442** |
| identityReview GODKÄND | 60 |
| identityReview UNDERKÄND | 36 |
| **treeEffect BÄRANDE** | **60** |
| treeEffect AVVAKTAR | **478** |

Endast **60 personer är `BÄRANDE`** — det vill säga: anlinjen får passera
dem. 478 avvaktar. Därtill bär **89 personakter minst en `CONFLICT`-rad**.

Villkoret kräver att bärande identiteter och relationer är prövade och att
kvarstående konflikter redovisas tillsammans med vilka slutsatser de
påverkar. Redovisningen finns i akterna, men **prövningen är gjord för en
minoritet**.

Dagens arbete illustrerar varför måttet inte får läsas som färdigt: A-3999
(Ture Alexius födelsedag, `⁷/₅` mot `⁷/₆`) och A-4018 (`gift 1831` mot en
tom vigselårgång) är två nya, oavgjorda konflikter som bevarats i stället
för att gissas bort.

## Villkor 4 — Källtäckning

**Ouppfyllt.**

Källtäckningsmatrisen är en **kompakt äldre indikator**
(PCD-2026-09-05-013), inte hela täckningskontraktet, och den täcker de 32
namngivna kohortpersonerna plus djup-6-raderna. Utanför den saknar **442
personer** en bedömd källstrategi (`strategy: EJ BEDÖMT 442`).

Inom matrisen kvarstår sju personer med `1`-celler (tabellen under villkor 1),
och **P-0536 saknar helt matrisrad** — en representationslucka, inte ett
forskningsresultat.

I dag flyttades fyra celler från `1` till `N` med utskrivet omfång och
citatlänkar (P-0131 och P-0132, kolumnerna `M` och `V`). Det är rätt sorts
åtgärd, men den gäller två personer av sju.

## Villkor 5 — Spårbarhet

**Delvis uppfyllt — infrastrukturen är på plats, verifieringen är det inte.**

Det som **är** styrkt:

- 3 514 påståenden, samtliga med beläggslänk; 1 072 citat; 782 källor.
- `validate-genealogy` grön: 3 514 påståenden, 2 527 poster, Wotan-JSON giltig.
- `media-manifest --check` grön: **4 835 mediefiler med kontrollsummor**.
- 36 regressionstester gröna.
- Forskningsloggen är append-only med en batch per läsning.

Det som **inte** är styrkt är villkorets andra hälft: *"Granskningen visar
både att uppgifterna är konsistenta och att beläggen faktiskt bär
slutsatserna."*

**Enbart under 2026-09-07 påträffades tio skilda varianter av citat som var
korrekt formulerade men sakligt fel**, flera av dem månader gamla:

| # | Variant | Exempel |
|---|---|---|
| 1 | för snävt dagintervall | C-0145, C-0306 |
| 2 | fel år | C-1023 |
| 3 | fel uppslag | C-0424 |
| 4 | angivet läsomfång ≠ sidans innehåll | C-0151 |
| 5 | rätt sida, fel söknyckel | C-0336 |
| 6 | gräns en dag för kort | C-0433 |
| 7 | rätt sida, fel namnform | C-0144 |
| 8 | rätt sida, rätt noll, **fel volym i kedjan** | C-0896 |
| 9 | **en enda felläst siffra** i ett korrekt citat | A-3946 → A-3977 |
| 10 | **ett felläst ortnamn som flyttade hela sökningen till fel socken** | A-3202 → A-4027 |

Variant 10 kostade **nio kompletta årgångar i fyra serier** och ledde
dessutom till en falsk slutsats (A-4024) om att källan var opålitlig — som
fick dras tillbaka samma dygn.

**Slutsats:** felfrekvensen är inte försumbar, och den upptäcks bara vid
omläsning. Villkor 5 kan inte kallas styrkt förrän en **systematisk**
omläsningsgranskning har gjorts av de citat som bär bärande slutsatser.
Uppgiften `T-0080` (kvarvarande lässtopp i C-poster) är närmast, men den
täcker inte detta.

## Villkor 6 — Avslutningsrevision

**Kan inte uppfyllas.** Denna revision är daterad och prövar varje villkor,
men den visar att villkor 1–4 är ouppfyllda och att villkor 5 är
overifierat. Villkoret kräver att revisionen visar att **ingen materiell,
genomförbar och motiverad forskningsåtgärd återstår**. Det gör den inte.

## Konkreta externa hinder — och vad de inte förklarar

Följande hinder är verkliga och dokumenterade:

- **ArkivDigital är förbjudet** för agenten (PCD-2026-09-05-011).
- **ALTCHA/CAPTCHA får inte lösas** utan ägarens uttryckliga besked.
- **Läsesalsbundna volymer**, bland annat P-0339:s bouppteckningsvolym
  `SE/HLA/1040061/F II/5` och Anders Jonssons `F II/7`.
- **Generalmönsterrullan** `SE/KrA/0125/030:Ö/D/2` saknar exponerad
  reproduktion.
- **Stora Malm `C/8`** (1848–1859) gav ingen reproduktion på batchsidan;
  digitaliseringsläget är oavgjort, inte spärrat.

**Inget av dessa hinder förklarar någon av luckorna i villkor 1–5.** Varje
namngiven lucka ovan har genomförbart arbete kvar, och Wotan har tolv
READY-uppgifter plus en ONGOING. Enligt north stars egen formulering är
målet därför **ofullbordat, inte hindrat**.

## Vad som skulle flytta måttet mest

I värdeordning, som underlag för Project Control:

1. **Livsbildsvågen (villkor 2).** 442 personer utan bedömning är den
   största enskilda posten i hela kontraktet. `T-0099` och `T-0098` äger den.
2. **Djup 6:s sju återstående matrisrader (villkor 1 och 4).** `T-0083`,
   ONGOING; nästa steg är Eva Lotta Jonsdotters födelsenotis i Stora Malm
   `C/6`, samma volym där makens notis hittades i dag.
3. **En systematisk omläsningsgranskning av bärande citat (villkor 5).**
   Existerar inte som uppgift i dag och bör skapas; dagens tio felvarianter
   är underlaget.
4. **P-0536:s saknade matrisrad** — en ren representationslucka som kan
   åtgärdas utan ny forskning.

## Verifiering vid revisionen

```
node scripts/goal-state.mjs             → gemensamt djup 5; djup 6 ej behandlad
node scripts/research-inventory.mjs     → Strukturfel: 0
node scripts/validate-genealogy.mjs     → OK: 3514 påståenden; 2527 poster
node --test scripts/                    → 36 pass, 0 fail
node scripts/media-manifest.mjs --check → OK: 4835 mediefiler
```
