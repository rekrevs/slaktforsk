# S-0517: Riksarkivet — Ljustorp C/1–C/2 och A I/1–A I/3, familj 98-kontroll

## Källbeskrivning

- Arkiv: Ljustorps kyrkoarkiv, `SE/HLA/1010115`
- Födelse- och dopbok `C/1`, 1688–1813, Riksarkivet-id
  `FchSzeg0dw7FhPAbM28go0`, reproduktion `71000675`; volymen innehåller
  födda, vigda och döda och är enligt katalogen defekt i början
- Födelse- och dopbok `C/2`, 1814–1844, Riksarkivet-id
  `8nyLvJSPwIDMbr7wA6ain2`, reproduktion `C0033133`; volymen innehåller
  även vigselbok 1814–1846 och död- och begravningsbok 1814–1861
- Husförhörslängd `A I/1`, 1803–1812, Riksarkivet-id
  `OFvYi40A3KcsC9SZZeivk2`, reproduktion `C0033121`
- Husförhörslängd `A I/2`, 1812–1821, Riksarkivet-id
  `56SFKMsUMak9FE1IOjVAi2`, reproduktion `C0033122`; kataloganmärkning
  `Defekt i början`
- Husförhörslängd `A I/3`, 1821–1831, Riksarkivet-id
  `gEGb70ETbaI5KDqzMP2o35`, reproduktion `C0033123`
- Läst 2026-08-30 endast via Riksarkivets API, JSON-LD, IIIF och, för att
  identifiera bildvisarens anropskrav och hämta tre exakta C/2-bilder, den
  av ägaren uttryckligen tillåtna inloggade Chrome-sessionen

## Födelseföljder i C/1

Hela 1796 års följd ligger på bilderna `71000675_00232`–`_00235`.
Följden går från januari genom december utan någon Hindric/Henrik född
2 november och utan någon Cajsa vars föräldrar är Henrik Henriksson och
Anna Greta. Bild `_00235` fortsätter in i 1797. Den bevarade 1797-följden
är däremot inte komplett: bild `_00236` slutar efter en majpost och en stor
tom yta, medan senare bilder redan har nått 1798. Något helårsnoll för 1797
görs därför inte.

Hela 1801 års följd ligger på bilderna `_00251`–`_00254`. Den innehåller
ingen dotter Anna till det uppgivna föräldraparet. Hela 1804 års följd på
bilderna `_00257`–`_00260` innehåller en Mårten född 10 mars, men hans
föräldrar är bonden Anders Olofsson och Anna Brita Mårtensdotter, inte
Henrik Henriksson och Anna Greta. Inte heller någon annan Mårten i följden
har det uppgivna paret som föräldrar.

Riksarkivets födelseregister-API gav noll träffar för Hindric, Henrik,
Hindrik och Henric i Ljustorp 1796–1797 samt för Cajsa 1796, Anna 1801 och
Mårten 1804. API-resultaten är endast registertäckningsbundna kontroller;
originalbildernas kompletta årsföljder bär de avgränsade nollresultaten.

## Vigsel- och dödföljder i C/2

Bilderna `C0033133_00109`–`_00110` bildar den kompletta kronologiska
vigselföljden 1819 och fortsätter in i 1820. Där finns inget par Henrik eller
Hindric Henriksson och Brita Flinkberg och ingen sådan vigsel 1819-10-31.
Vigselregister-API:t gav noll både för den exakta namnfrågan och för alla
Ljustorpvigslar 1819, men även här är API-nollet endast en täckningskontroll.

Bild `C0033133_00136` innehåller hela dödföljden 1833 mellan slutet av 1832
och rubriken 1834 på motstående sida. Samtliga poster från januari till
december lästes utan någon Henrik/Hindric Henriksson. Helge Nybergs uppgift
att Henrik Henriksson d.ä. dog 1833 får därför inte behandlas som en
Ljustorpdöd verifierad i den ordinarie dödboken.

## Husförhör och exakt avgränsning

`A I/1`:s ortregister hänvisar Laxsjön till sida 12. Sidorna 12–13,
bilderna `C0033121_00056`–`_00057`, innehåller andra namngivna hushåll men
ingen Henrik Henriksson med Anna Greta och de uppgivna barnen. Sida 14,
bild `_00058`, börjar Lagfors och stänger det bevarade Laxsjönsintervallet.

I `A I/2` saknar registret en egen Laxsjönspost. Sida 15, bild
`C0033122_00011`, har förlorat hela namn- och födelsedelen genom volymens
fysiska skada. Sida 16, bild `_00012`, börjar Lagfors och visar endast en
bevarad fortsättning av ett annat hushåll. Frånvaron i denna volym är därför
inte ett familjenoll: målhushållet kan ha stått på det förstörda bladet.

`A I/3` sida 18, bild `C0033123_00033`, är Laxsjön. Den lilla bevarade
personmängden innehåller inte målfamiljen; sida 19, bild `_00034`, börjar
Lagfors. Sida 43, bild `_00060`, bekräftar däremot den yngre Hindric
Henriksson, Brita Flinkberg och deras döttrar, såsom tidigare läst i
[S-0488](S-0488-riksarkivet-ljustorp-lagfors-original-1821-1870.md).

## Evidensbedömning

Kontrollen falsifierar inte att en person med namnet Henrik Henriksson d.ä.
eller Anna Greta har existerat. Den visar däremot ett sammanhängande
konfliktmönster i Nybergs familj 98: de uppgivna barnåren 1796, 1801 och
1804 stöds inte av de kompletta originalföljderna; sonens alternativa år
1797 ligger i ett defekt intervall; vigseldatumet 1819-10-31 och dödsåret
1833 saknas i kompletta originalföljder; och familjen återfinns inte på de
bevarade Laxsjönssidorna. P-0461–P-0462 bevaras därför som uppgivna,
konfliktfyllda registerpersoner men ska inte längre räknas som verifierade
föräldrar till P-0451.

## Bild-API-diagnos

Bildvisarsidan bäddar in officiella IIIF-manifest med formen
`https://lbiiif.riksarkivet.se/arkis!<reproduktion>/manifest`. Ett direkt
anrop till exempelvis `C0033123` gav `403 Forbidden`, även i den inloggade
Chrome-sessionens egen manifestflik. Samma URI gav `200` från ett vanligt
API-anrop när `Referer` sattes till motsvarande Riksarkivet-bildvisarsida.
Manifest och exakta `full/max/0/default.jpg`-bilder kunde därefter hämtas
utan export av kakor eller sessionsdata. Problemet är alltså ett
Referer-krav i Riksarkivets äldre reproduktionsbaserade IIIF-led, inte ett
felaktigt manifest- eller bild-id. `C/1`-batchen `71000675` är samtidigt
publik utan detta krav.

## Lokalt material

Samtliga fem IIIF-manifest, sök- och register-API-svar, det direkta
403-svaret och 23 exakta originalbilder är checksummade och länkade i
[C-0678](../citations/C-0678-ljustorp-familj-98-originalkonflikter.md).
Inga webbläsarskärmbilder har bevarats som ersättning för original.
