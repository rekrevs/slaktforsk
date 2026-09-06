# C-0956: Tre avgränsade nollor i Rotemansarkivet

## Källa

[S-0746](../sources/S-0746-rotemansarkivet-stockholm.md)

## Exakt lokalisering

Tre sökningar 2026-09-06 i T-0081, i den enkla respektive avancerade
sökformen.

## Utförda sökningar och utfall

### 1. Paret Ekholm före 1910

> `tbBirthday=1878-02-17` (alla namn, båda könen) → **200 rader**,
> alfabetiskt från `, Gösta Oscar Hjalmar` till `Östergren, Edit Augusta
> Kristina`, varav **fyra** bär namnet Ekholm:
> `Ekholm, Axel Vilhelm 1878-02-17 1912-1912` ·
> `Ekholm, Axel Wilhelm 1878-02-17 1910-1911` ·
> `Ekholm, Axel Wilhelm 1878-02-17 1911-1912` ·
> `Ekholm, Axel Wilhelm 1878-02-17 1912-1913`
>
> `tbLastname=Ekholm`, `tbFirstname=Hulda Amalia` → fyra poster, den
> tidigaste `Ålund, Hulda Amalia 1877-09-25 1899-1900`, därefter först
> 1910–1911.

**Utfall: avgränsat noll.** Ingen rotemanspost för paret eller för barnen
före inflyttningen till rote 23 den **1910-10-07**, trots att båda barnen
enligt samma register föddes i **Matteus församling 1907 och 1910**
([C-0955](C-0955-ekholm-alund-rotemansarkivet-1899-1913.md)). Familjen var
alltså bosatt i staden utan att vara förd i det rotematerial som databasen
omfattar, eller fördes under en namnform som inte fångas av vare sig
efternamnet eller makens exakta födelsedatum. Rote 27, varifrån de kom
1910, är den enda kända kopplingen till åren dessförinnan.

Denna nolla är avgränsad av databasens 200-radersavkortning: sökningen på
födelsedatum kan i princip ha fler träffar än de 200 visade. Namnsökningen
på `Ekholm` är däremot inte avkortad och bär nollan självständigt.

### 2. Ada Wilhelmina Jansson

> `tbFirstname=Ada Wilhelmina` (utan efternamn, utan datum) → **88 poster**,
> ingen född 1886; de närmaste är `Carlsdotter, Ada Wilhelmina 1885-11-20`
> och `Eriksson, Ada Wilhelmina 1885-11-03`.
> `tbFirstname=Ada`, `tbBirthday=1886-08-19` → **`NoResult`**.
> `tbLastname=Bergman`, `tbFirstname=Ada` → en enda post,
> `Bergman Engelbrektson, Ada An... 1876-01-27 1878-1879`.

**Utfall: avgränsat noll.** **Ada Wilhelmina Jansson, född 1886-08-19 i
Lerbo, förekommer inte i Rotemansarkivet 1878–1926** — varken under
flicknamnet Jansson, under namnet Bergman eller under enbart förnamnet Ada
med hennes födelsedatum.

### 3. Knut Bergman, rörmokare

> Avancerad sökning `tbLastname=Bergman`, `tbTitle=Rörmokare` → `NoResult`.
> `tbLastname=Bergman`, `tbFirstname=Knut` (utan titel) → **123 poster**,
> med minst nio skilda män födda 1880–1890.

**Utfall: avgränsat noll med metodförbehåll.** Ingen Bergman bär titeln
`Rörmokare` i databasen. Kontrollen `tbLastname=Ekholm`,
`tbFirstname=Axel Wilhelm`, `tbTitle=Lokeldare` gav rätt tre poster, så
titelfältet fungerar — men det matchar **hela** titelsträngen, och
rotemännens yrkesbeteckning för samma hantverk kan ha varit `Rörarbetare`,
`Rörläggare` eller `Rörmokaregesäll`. Nollan utesluter alltså stavningen
`Rörmokare`, inte yrket. Utan yrkesuppgift går de 123 posterna för `Knut
Bergman` inte att skilja åt.

## Normaliserad tolkning

För **P-0009 Ada Wilhelmina Jansson** är detta ett materiellt resultat, inte
bara en frånvaro. Familjeuppgiften är att hon gifte sig med rörmokaren Knut
Bergman **i Stockholm** ([C-0263](C-0263-jan-christer-om-arne-anki-och-sidogrenar.md)).
Rotemansarkivet är den enda samlade personförteckningen över Stockholms hela
befolkning under sin period, och hon saknas i den. Slutsatsen är att hon
**inte var mantalsskriven i Stockholm vid någon tidpunkt 1878–1926**. En
Stockholmsvigsel med Knut Bergman måste därför ligga **efter 1926** — vilket
står i konflikt med familjeuppgiften att dottern Maj-Britt föddes 1922
(A-1655). Konflikten bevaras. Den förenas enklast med den belagda
utflyttningen till **Østre Aker i Kristiania 1918-10-29**
([C-0918](C-0918-ada-utflyttning-norge-ostre-aker-1918.md)) och
anteckningen daterad 1921-11-28: äktenskapet och dotterns födelse kan ha
ägt rum **i Norge**, och paret kan ha kommit till Stockholm först senare.

För **P-0016** stänger nolla 1 den bekväma hypotesen att paret skulle gå att
följa bakåt i roteregistret till vigseln. Vägen till vigselposten går i
stället genom **Matteus församlings** egna böcker, eller genom rote 27.

## Stödda påståenden

A-3598–A-3599 (P-0009), A-3600 (P-0299), A-3593 (P-0016).

## Rättelse 2026-09-06: två av de tre nollorna vilade delvis på ett fält som ger falska nollor

Efter att posten skrivits prövades sökformuläret med positivkontroller, och
`tbBirthday` visade sig ge **falska nollor**: `1877-09-25` ensamt ger
`NoResult` trots att fyra kända poster bär det datumet, och `tbFirstname` +
`tbBirthday` respektive `tbFirstname` + `tbBirthplace` ger `NoResult` också
på personer som bevisligen finns. Se rättelsen i
[S-0746](../sources/S-0746-rotemansarkivet-stockholm.md).

Följande delar av avskriften ovan **utgår som bevis**:

- sökningen `tbBirthday=1878-02-17` (nolla 1) — den fungerade, men eftersom
  fältet kan ge falska nollor duger den inte som självständigt negativt
  belägg;
- sökningen `tbFirstname=Ada`, `tbBirthday=1886-08-19` → `NoResult`
  (nolla 2) — **ogiltig**, resultatet säger ingenting.

**Nollorna står ändå kvar, men på enbart namnsökningar**, som är
positivkontrollerade:

1. **Paret Ekholm före 1910.** `tbLastname=Ekholm` + `tbFirstname=Axel
   Wilhelm` → tre poster (1910–1913); `tbLastname=Ekholm` +
   `tbFirstname=Hulda Amalia` → fyra poster, den tidigaste `Ålund, Hulda
   Amalia 1899-1900`. Ingen post för paret före 1910-10-07. Nollan gäller
   dessa namnformer.
2. **Ada Wilhelmina Jansson.** `tbFirstname=Ada Wilhelmina` (ensamt) → 88
   poster, ingen född 1886; `tbLastname=Jansson` + `tbFirstname=Ada` → **84
   poster**, ingen född 1886-08-19 (närmast `Jansson, Ada Josefina
   1886-12-03` och `Jansson, Ada Linnéa Viktoria 1886-07-19`);
   `tbLastname=Bergman` + `tbFirstname=Ada` → en enda post, född 1876.
   Nollan är alltså **oförändrad i sak** och vilar nu på tre giltiga
   namnsökningar.
3. **Knut Bergman, rörmokare.** Kombinationen `tbLastname` + `tbTitle` utan
   förnamn är **inte** positivkontrollerad; den kontroll som gjordes
   (`Ekholm` + `Axel Wilhelm` + `Lokeldare`) hade två namnfält. Nollan för
   `Bergman` + `Rörmokare` **nedgraderas därför till oprövad** och får inte
   åberopas. Kvar står bara att `Bergman` + `Knut` ger 123 poster som inte
   går att skilja åt utan yrkesuppgift.

Slutsatsen om P-0009 i tolkningen nedan ändras inte: hon saknas i registret
under alla prövade namnformer.
