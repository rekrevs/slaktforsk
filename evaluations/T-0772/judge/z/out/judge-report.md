# Blind sakgranskning Z — T-0772

AI-granskning, inte mänskligt certifierat facit. Ingen modellidentifiering har gjorts.

## Lästa underlag

Endast T-0769/z/public/TASK.md, T-0769/z/public/input.json (inklusive pendingReviews), T-0769/z/private/RUBRIC.md, T-0772/judge/STANDARD-Z.md samt följande 13 fullständiga svar i T-0772/blind/z/ och respektive T-0772/scores/Cnnn.auto.json:

C002, C010, C012, C015, C024, C025, C027, C030, C032, C034, C035, C039, C041.

Ingen evaluator, databasinförsel, nätverksåtkomst eller subagent har använts. Uppgifter om verklig införsel och verifieringar kommer från de tillåtna auto-filerna. Alla svar har lästs individuellt och i sin helhet; fältjämförelse mot det stipulerade beslutet har dessutom kontrollerats med lokal kod. Endast out/ har skrivits.

## Sakfel som automatiken inte fångade

C024 får automatiskt 15/15 men underkänns manuellt och materiellt. Request bf476e304a25fa029274e93a327cfd8a597e934def1d4eff4d298823e055b6ad gäller F-B@1. Dess skäl är ”R-B har rättats och O-B:s beroendeuppgift har samtidigt prövats mot R-B version 3.” Det saknar F-B:s egen omprövning eller datumrättelse. Korrekt F-B-revision och dess separata ändringsmotivering ersätter inte individuell resolve. Den andra resolven godtas: den anger O-B:s egen datumrättelse till 1930-10-23, även om den också nämner F-B:s uppdaterade bindning. Övriga motiveringar och datafält i C024 är godtagbara.

Inga ytterligare materiella fel hittades bland de övriga tolv svaren.

## Gränsfall

C010 har S-A.title = ”Provförsamlingen.”. Den extra slutpunkten ger strikt 13/15 och passed=false. Alla motiveringar, båda individuella resolves och övrig semantik godtas. Därför manual_pass=true, material_pass=true och formatting_only_failure=true enligt standarden. Paketkontrollen anger uttryckligen detta formatundantag; den strikta avvikelsen döljs inte.

C010:s korta resolve för O-B räcker: den anger rådatum och normaliserat datum som rättade utifrån R-B v3. C024:s korta ändringsmotiveringar och C041:s korta titelmotivering är också konkreta i respektive objektkontext. C032:s något komprimerade titelmotivering identifierar rätt måltitel. C012:s slutpunkt i rationale är vanlig interpunktion, inte en slutpunkt i title.

C041 identifierar resolve-objekten som ”Slutsatsen” respektive ”Observationen”; request-ID, underlag och datumrättelse gör dem entydiga. Inget krav på ett upprepat objekt-ID införs.

Hänvisningar till rättad R-B som stöd för F-B läses genom R-B → O-B → F-B, i synnerhet uttryckligen i C027 och C030. Evidensfälten använder rätt versioner. Avläsnings- och granskningsspråk i C002, C012, C015, C025, C027, C034, C035 och C039 tolkas enligt standarden som beskrivning av fastställt beslut, inte som påstående om en ny arkivundersökning.

## Resultat

Manuellt avser den manuella sakprövningen; godkänd kräver dessutom automatisk 15/15. Materiellt bortser endast från det angivna punktfelet i C010.

| Cnnn | auto/15 | manuellt | godkänd | materiellt |
|---|---:|---|---|---|
| C002 | 15/15 | ja | ja | ja |
| C010 | 13/15 | ja | nej | ja |
| C012 | 15/15 | ja | ja | ja |
| C015 | 15/15 | ja | ja | ja |
| C024 | 15/15 | nej | nej | nej |
| C025 | 15/15 | ja | ja | ja |
| C027 | 15/15 | ja | ja | ja |
| C030 | 15/15 | ja | ja | ja |
| C032 | 15/15 | ja | ja | ja |
| C034 | 15/15 | ja | ja | ja |
| C035 | 15/15 | ja | ja | ja |
| C039 | 15/15 | ja | ja | ja |
| C041 | 15/15 | ja | ja | ja |

13 svar: 11 strikt godkända, 12 manuellt och materiellt godkända. Automatisk totalsumma 193/195. Varje finalfil innehåller åtta konkreta manuella kontroller, totalt 104.
