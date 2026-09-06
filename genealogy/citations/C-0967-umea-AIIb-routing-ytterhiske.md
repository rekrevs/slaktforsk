# C-0967: Fastighetslängderna för Umeå stad är digitaliserade — routing mot Ytterhiske

## Källa

[S-0755](../sources/S-0755-umea-stadsforsamling-AIIb-fastighetslangder.md)

## Exakt lokalisering

Manifestetiketter för batcherna `00177468`, `00177469` och
`00178886`–`00178899`, hämtade 2026-09-06 i T-0084, samt fyra lästa uppslag:

- `00177469_00005` (`A II b/3`) — kvarteret **ARKEN** N:r 1, gårdsägare
  J. Carlssons sterbhus, med änkefru Ester Maria Matilda Carlsson f. Wall
  född 1867-12-11 i Nysätra och hennes hushåll
- `00178889_00005` (`A II b/5`) — kvarteret **Skaren** N:r 2, Nygatan 63
- `00178896_00005` (`A II b/12`) — kvarteret **Sadelmakaren** N:r 1 samt
  **stadsägorna 1041, 1047, 1049 och 1057**
- `00178897_00005` (`A II b/13`) — avdelningen **`På församlingen skrivna`**
- `00178898_00006` (`A II b/14`) — maskinskrivet kortregister över
  gatunamn och fastighetsbeteckningar

## Utfall

**Serien är i sin helhet digitaliserad**, volymerna 1–14, och batchkartan
är nu skriven i S-0755. Det var inte känt före denna omprövning: den
ordinarie metadatasökningen returnerade bara fem av volymerna, medan en
genomgång av manifestetiketterna i nummerserien gav alla fjorton.

**Uppslagens form är fastställd.** Varje fastighet har en egen sida med
gårdsägare, hela hushållet, födelseår, födelsedag, födelseort, civilstånd,
in- och utflyttningsanteckningar och — avgörande — **församlingsbokens
sidnummer**. Serien är alltså både en boendekälla och en korsreferens.

**Ytterhiske är ännu inte lokaliserat.** Fyra volymer är stickprovslästa.
Innerstadens fastigheter står under **kvartersnamn**, medan fastigheter
utanför kvartersindelningen står under **bara ett stadsägonummer**;
`A II b/12` visar numren **1041, 1047, 1049 och 1057**. Zingmarks gård har
stadsägonummer **1258** ([C-0916](C-0916-zingmark-ytterhiske-umea-stad-1925-1941.md)),
alltså ett högre tal i samma numrering, vilket placerar den längre fram i
`A II b/12` eller i `A II b/13`.

Detta är en **routingobservation, inte ett nollresultat**: ingen sida med
stadsäga 1258 har lästs och avvisats, och ingen volym är genomgången.

## Betydelse

Fastighetslängden är den enda kända källa som kan visa **vilka som bodde på
Ytterhiskegården år för år 1925–1946** och binda dem till
församlingsbokens sidor. Den gäller därmed direkt den enskilt största
ekonomiska och sociala uppgiften i
[P-0028](../people/P-0028-johan-oskar-zingmark.md)s och
[P-0029](../people/P-0029-ida-sofia-andersdotter.md)s liv — gården med
**⅛ mantal nr 2 och ¹¹/₆₄ mantal nr 1** — och den är genomförbar utan
captcha, inloggningsspärr eller beställning.

## Stödda påståenden

Källvägen KP-04 i [P-0028](../research-profiles/P-0028.md) och KP-02 i
[P-0029](../research-profiles/P-0029.md).

## Tillägg 2026-09-06: Ytterhiskes avdelning lokaliserad i `A II b/13`

Efter routingen ovan söktes stadsäga 1258 systematiskt med en
**rubrikmontage-teknik**: för varje uppslag hämtas bara den översta
remsan över IIIF:s regionparameter, `0,0,<bredd>,<0,13·höjd>`, och sex
sådana remsor ritas samman i en canvas. Ett skärmavtryck visar då
**sex uppslagsrubriker samtidigt**. `pct:`-syntaxen stöds inte av
servern och ger `501`; absolut region fungerar.

**Ytterhiskes avdelning ligger i `A II b/13`, batch `00178897`, omkring
uppslagen 77–95.** Lästa rubriker:

| Uppslag | Rubrik |
|---|---|
| 69 | `Sandaktern`, stadsägan **1251 A**, gårdsäg. E. A. Reström |
| 70 | `Sandaktern`, stadsägan **1251 B** |
| 71 | stadsägan **1251 6**, gårdsäg. F. A. Viberg |
| 73 | `Östermalm` N:r 1383, stadsäg. **1252 d** |
| 75 | `Östermalm` N:r 1252, Högatan |
| 76 | `Sandaktern`, stadsägan **1254**, gårdsäg. Josefina Danielsson |
| 77 | **`Ytterhiske`**, stadsäg. **1265 + 1206 + 1422 + 1485**, gårdsäg. Joh. och Aro Dahlgren |
| 78 | **`Ytterhiske`**, stadsäg. **1270**, gårdsäg. E. C. Dahlgren |
| 79 | **`Ytterhiske`**, stadsägan **1274**, gårdsäg. J. E. Lundgren |
| 80 | **`Ytterhiske`**, stadsäg. **1282**, gårdsäg. J. T. Westin |
| 82 | **`Ytterhiske`**, stadsäg. **1304**, gårdsäg. J. Bodén, Holmsund |
| 84 | **`Ytterhiske`**, stadsäg. **1307**, gårdsäg. Karl Eriksson |
| 86 | **`Ytterhiske`**, stadsäg. **1333** |
| 88 | **`Ytterhiske`**, stadsäg. **1338**, gårdsäg. N. L. Hansson |
| 90 | **`Ytterhiske`**, stadsäg. **1276**, gårdsäg. N. P. Westberg |

**Numreringen är inte strikt stigande** — 1282 kommer före 1276 — och
Ytterhiskeuppslagen står blandade med kvarteren Sandaktern och Östermalm i
samma nummerintervall. **Stadsäga 1258 finns inte bland de femton lästa
rubrikerna.** Det är ett avgränsat noll för just dessa uppslag, inte för
volymen: `A II b/13` har 406 uppslag, och Ytterhiskeavdelningen fortsätter
efter uppslag 90.

Nästa åtgärd är att läsa rubrikerna för uppslagen **91–130** med samma
teknik, och därefter `A II b/12`:s senare del, innan ett volymnoll får
bokföras.

## Tillägg 2026-09-06, andra passagen: Ytterhiskeblockets nummerintervall

Rubrikerna för uppslagen **91–96** är lästa med samma teknik och fortsätter
Ytterhiskeavdelningen: **1289** (91), **1292** (92), **1347** (93),
**1353** (94) och **1354** (95).

Därmed är hela Ytterhiskeblockets nummerintervall känt. De tjugoen lästa
rubrikerna i uppslagen 69–96 ger:

- under `Sandaktern` och `Östermalm`: **1251 A, 1251 B, 1251 6, 1252, 1252 d,
  1254** och egnahemsområdets **12516**;
- under `Ytterhiske`: **1265, 1270, 1274, 1276, 1282, 1289, 1292, 1304,
  1307, 1333, 1338, 1347, 1353, 1354**.

**Stadsäga 1258 saknas i hela detta intervall**, och den ligger dessutom i
gapet mellan Sandakterns 1254 och Ytterhiskeblockets lägsta nummer 1265.
Nollan är därmed **skärpt men fortfarande avgränsad**: den gäller uppslagen
69–96 i `A II b/13`, båda sidorna, och säger ingenting om volymens övriga
310 uppslag eller om de tretton andra volymerna.

### Fortsatt svepning och en avgörande omläsning av nyckeln

Rubrikerna för uppslagen **96–101** är också lästa och fortsätter uppåt:
`Ytterhiske` **1357** (96, gårdsäg. J. H. Öhman), **1360 B** (97, K. E.
Lindgren), **1363** (98 och 99, Karlsson-Holmgren, Ängsvägen 18) och
**1364** (100, Olsson). **Ingen gårdsägare Zingmark** förekommer bland de
tjugosju lästa rubrikerna i uppslagen 69–101, och numren stiger
monotont bort från 1258 efter uppslag 91.

**Nyckeln själv måste omprövas.** Församlingsbokens anteckning lyder
`Stad äg. 1258 **m.m.**`
([C-0916](C-0916-zingmark-ytterhiske-umea-stad-1925-1941.md)) — alltså
*stadsäga 1258 med mera*. Gården bestod av flera stadsägor, precis som
uppslag 77 visar med sitt sammansatta huvud `Stadsäg. 1265 + 1206 + 1422 +
1485`. Fastighetslängdens uppslag för gården kan därför vara rubricerat
med **vilket som helst** av dess nummer, inte nödvändigtvis 1258.

Det ändrar sökstrategin: **sök gårdsägarnamnet, inte numret.**
Gårdsägarfältet står i samma förtryckta huvud som numret och läses i samma
rubrikmontage, så en svepning av `A II b/12` och `A II b/13` efter namnet
**Zingmark** är lika billig som en numerisk sökning och tål att gården har
flera nummer.

Nollan omfattar därmed uppslagen **69–101** i `A II b/13`, båda sidorna:
varken stadsäga 1258 eller en gårdsägare Zingmark. Volymens övriga 305
uppslag och de tretton andra volymerna är oprövade.
