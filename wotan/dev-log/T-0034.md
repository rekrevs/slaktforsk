# T-0034: Korroborera sannolikt levande personer mot birthday.se

**Status**: READY | **Size**: M
**Phase**: -

## Context och mandat

Aktiverad av [PCD-2026-09-09-029](../../PROJECT-CONTROL.md#pcd-2026-09-09-029).
Uppgiften godkändes ursprungligen i PCD-2026-09-04-008 men parkerades som
`IDEA` i väntan på ett senare avstamp. Ägaren har 2026-09-09 beslutat att
projektet ska vara fritt att använda öppet tillgänglig information på nätet om
nu levande personer, och vägen är därmed en öppen och genomförbar passage.

## Scope, underlag och stoppgräns

Sju sannolikt levande personer: **P-0004, P-0005, P-0006, P-0041, P-0210,
P-0269 och P-0270**. Korroborera deras genealogiskt relevanta grunduppgifter
person för person mot den öppet åtkomliga tjänsten birthday.se.

**Två personer är beroende av utfallet.** P-0004 och P-0210 har 2026-09-09
fått PK-08 sänkt till `EJ STYRKT` och `Kontraktsgranskning` till `UNDERKÄND`,
eftersom deras tidigare grund var att ingen väg stod öppen **inom
dataminimeringen** — en avgränsning som beslutet tar bort. Deras livsbildsnivå
återfås när denna uppgift är utförd.

**Fem personer är det inte.** P-0005, P-0006, P-0041, P-0269 och P-0270 står
kvar `STYRKT` på den kvarvarande grunden att vägen saknar diskriminerande
värde för dem. Den bedömningen är inte omprövad; **denna uppgift prövar den i
praktiken**, och ett positivt utfall kan ändra PK-08 för dem.

Utanför: personer som inte står i listan ovan, och varje slutsats som går
utöver vad tjänsten faktiskt visar.

## Acceptance Criteria

- Varje person har ett uttryckligt utfall: korroborerad, inte funnen, eller
  funnen men utan säker identitetsmatchning. Ett åtkomsthinder är inget
  personresultat.
- **Öppet tillgänglig status ersätter inte kraven på säker
  identitetsmatchning, dataminimering eller åtskillnad mellan observation och
  slutsats** (PCD-2026-09-04-008, vars sakregler består oförändrade).
- Uppgifter som faktiskt kan beläggas bevaras med tydlig källhänvisning; det
  som inte kan beläggas skrivs inte in.
- PK-08 och `Kontraktsgranskning` omprövas för alla sju, inte bara för de två
  som är sänkta.
- En batchlogg, oberoende sakprövning och relevanta format-, validator-,
  inventerings-, test- och mediekontroller passerar.

## Approach

Läs `genealogy/person-contract.md` och de sju profilernas källvägsavsnitt
först. Följ projektets integritetsregler: **dataminimeringen i vad som
publiceras består oförändrad** — beslutet gäller vad som får användas, inte
vad som får spridas. Inga beställningar, ingen dashboardändring, ingen PDF och
ingen commit eller push utan ägarens ord.

## Återupptagning

- Uppdaterat: 2026-09-09.
- Utfört: uppgiften aktiverad från `IDEA` till `READY` genom
  PCD-2026-09-09-029; omfånget preciserat till sju namngivna personer.
- Nästa ej utförda steg: läs de sju profilernas källvägsavsnitt och börja med
  P-0004 och P-0210, vars livsbildsnivå hänger på utfallet.
- Hinder: inga.
