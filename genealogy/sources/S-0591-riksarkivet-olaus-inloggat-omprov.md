# S-0591: Riksarkivet — Olaus Fredbergs analoga routes, inloggat omprov

## Källbeskrivning

Efter att användaren själv hade loggat in och besvarat den tidigare
CAPTCHA-utmaningen kördes P-0336:s spärrade katalogvägar om 2026-09-01 i
samma användarägda Chrome-session. Ingen ny CAPTCHA eller ALTCHA visades
eller hanterades. Inga kakor, tokens, local storage- eller session
storage-värden lästes. Den synliga inloggningsidentiteten användes inte och
har inte bevarats i projektet.

Den strukturerade arbetsavskriften finns i
[den bevarade observationen](../media/S-0591-riksarkivet-olaus-inloggat-omprov-observation.json).
Den återger bara synliga katalogfält, frågeparametrar och träffantal; den är
inte ett exporterat sessions- eller API-svar.

## Elva katalogvägar utan CAPTCHA men med läsesalsgräns

Samtliga tre prioriterade Göta-volymer och de åtta routes som tidigare
stannade vid CAPTCHA öppnades nu normalt:

| Route | Referenskod | Permanent id | Datering | Institution |
|---|---|---|---|---|
| Göta livgarde, namnregister 198 | `SE/KrA/0102/A/001:Ö/0/198` | `PCa4xje5Xak79xN0pDNIy7` | 1874–1927 | Riksarkivet i Täby, Krigsarkivet |
| Göta livgarde, rekryteringsjournal 240 | `SE/KrA/0102/A/001:Ö/0/240` | `66D6lRqjUKAwWXeFOaYLr2` | 1857–1877 | Riksarkivet i Täby, Krigsarkivet |
| Göta livgarde, avskedsjournal 241 | `SE/KrA/0102/A/001:Ö/0/241` | `vfgd7zChVI5OfGm5uEMxS2` | 1809–1907 | Riksarkivet i Täby, Krigsarkivet |
| Stora Lundby H V/2 | `SE/GLA/13505/H V/2` | `yRRo2b2xweZJUG018W43t3` | 1838–1870 | Riksarkivet i Göteborg |
| Stora Lundby H V/1 | `SE/GLA/13505/H V/1` | `yJRo2b2xweZJUG018W43t3` | 1777–1870 | Riksarkivet i Göteborg |
| Östra Fågelvik H II/5 | `SE/VA/13687/H II/5` | `9kiPAhymRY78EB7e8meLl7` | 1866–1887 | Värmlandsarkiv |
| SJ F 1 A/4 | `SE/GLA/16066/F 1 A/4` | `rDo1qLRPS4zQuWJM9cmUy5` | 1870–1944 | Riksarkivet i Göteborg |
| SJ D 4 A/1 | `SE/RA/420334/057/D/D 4/D 4 A/1` | `lMLgUcG1LKcymCK2zmfly8` | 1911–1915 | Riksarkivet i Stockholm/Täby |
| Svea livgarde D III/2 | `SE/KrA/0101/A/001:Ö/D III/2` | `QCR1qGzJtALSq7gx4GwI54` | 1875–1876 | Riksarkivet i Täby, Krigsarkivet |
| Livgardet till häst D VI/6 | `SE/KrA/0161/001:Ö/D VI/6` | `SD8qVn3ozQD1wOaPqMfWe0` | 1866–1882 | Riksarkivet i Täby, Krigsarkivet |
| Göta livgarde GMR 237 | `SE/KrA/0102/A/001:Ö/0/237` | `5gP5KYJ88KIGzaKtFwy1j3` | 1874–1880 | Riksarkivet i Täby, Krigsarkivet |

Varje post visade `Läsesal` och ingen digital bildkontroll. På den särskilt
inspekterade GMR 237-posten bar `Läsesal`-kontrollen postens äldre
Arkis-UUID. Riksarkivets egen beställningssida förklarar att knappen lägger material i en beställning för
läsning på plats. Ingen post lades till och ingen läsesals- eller
kopiebeställning skickades. Omprovet avlägsnar alltså det äldre
CAPTCHA-hindret men förändrar inte materialets analoga originalstatus.

## Fredric Jacobson — bouppteckningsregistret 1853–1854

Åtta exakta kombinationer av `Fredric`/`Fredrik` och
`Jacobson`/`Jacobsson`/`Jakobson`/`Jakobsson` med hemförsamlingen Stora
Lundby gav noll träffar. De följdes av förnamns-, efternamns-, jokerteckens-
och ortfrågor på Stora Lundby, Lundby, Hjällsnäs och Stannum utan målträff.

Kontrollfrågorna visar varför utfallet måste begränsas:

- en helt namnblank fråga på Stora Lundby 1853–1854 gav noll poster;
- en namnblank fråga på Lundby gav fem orelaterade poster;
- namnblanka Hjällsnäs- och Stannumfrågor gav noll;
- en landsomfattande `Fred*` + `Ja*`-fråga gav fyra orelaterade poster i
  Norra Vi, Bondkyrka och Visby.

Registret fungerade alltså och returnerade poster i andra kontexter, men gav
ingen akt-, datum-, gårds- eller sidnyckel för Fredric. Eftersom även den
namnblanka Stora Lundby-kontrollen är tom är resultatet register-,
normaliserings- och täckningsbundet. Det bevisar inte att Fredric saknades,
att ingen bouppteckning upprättades eller att F II a/9:s 1853-del saknar en
relevant akt. Marginalen `afl.53` är fortsatt källbelagd som avflyttning,
inte dödsfall.

## Slutsats och återaktivering

Den sakliga prioriteringen ändras inte. Göta 198 ska läsas först och en
eventuell registerträff routas till digitala volym 194; därefter följer
240/241 och de övriga militära läsesalsvägarna. Östra Fågelvik H II/5
förblir den mest direkta vägen till en äldre Lundby-/gårdsnyckel. H V/2 och
H V/1 kan pröva Fredric–Anna Brittas 1849-hypotes, och SJ F 1 A/4 samt
D 4 A/1 är fortsatt exakta yrkesvägar.

Upprepa inte samma bouppteckningsfrågor utan ny registertäckning, namnform,
ort eller aktnyckel. Bjärke F II a/9:s 524 bilder ska inte blindläsas utan
en sådan avgränsning.

## Bevarat underlag

| Fil | Byte | SHA-256 |
|---|---:|---|
| [Strukturerad åtkomst- och sökobservation](../media/S-0591-riksarkivet-olaus-inloggat-omprov-observation.json) | 6 197 | `041b4787ea41cbdea04fcbf25a3be54743f92340819b6df7945b499feefaea1d` |

## Stödda påståenden

A-2963–A-2965.
