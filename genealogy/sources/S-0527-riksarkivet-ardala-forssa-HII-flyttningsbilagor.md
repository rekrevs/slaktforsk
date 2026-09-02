# S-0527: Riksarkivet — Årdala och Forssa H II, flyttningsbilagor

## Källbeskrivning

- Arkiv: Årdala kyrkoarkiv, `SE/ULA/11781`
- Serie: H II, Bilagor till flyttningslängderna t.o.m. 1967,
  `SE/ULA/11781/H II`
- Riksarkivet-id för serien: `LwX6bDX9rH6cxG02H087k3`
- Arkiv: Forssa kyrkoarkiv, `SE/ULA/10279`
- Volym: H II/1, Bilagor till flyttningslängderna 1851–1890,
  `SE/ULA/10279/H II/1`
- Riksarkivet-id för volymen: `iDJysMmaweZJTe018W43t3`
- Arkivinstitution: Riksarkivet i Uppsala
- Kontrollerad och bevarad: 2026-08-30
- [Årdala H II i katalogen](https://sok.riksarkivet.se/arkiv/LwX6bDX9rH6cxG02H087k3)
- [Forssa H II/1 i katalogen](https://sok.riksarkivet.se/arkiv/iDJysMmaweZJTe018W43t3)

## API-först och beståndsavgränsning

Riksarkivets records-API och exakta OAI-EAD-poster användes först. Årdala
H II:s OAI-post har en tom `dsc` och redovisar alltså ingen underordnad
volym. Det finns därmed ingen katalogiserad H II-volym att beställa eller
distansläsa för Eriks uppgivna inflyttning 1875. Detta är ett
katalog-/beståndsresultat, inte belägg för att ingen attest en gång
utfärdades eller mottogs.

Forssa H II/1 är däremot en exakt katalogiserad volym för 1851–1890 utan
åtkomstbegränsning. Records-API:t saknar bildlänk och markerar inte posten
som digitaliserat material. JSON-LD-posten har endast en fysisk, analog
instansiering och inget `schema:image`.

Efter dessa API-kontroller öppnades den exakta Forssa-posten i en ny styrd
flik i användarens redan inloggade Chrome-session. Sidan visade att
användaren var inloggad men omdirigerade direkt till ALTCHA. Kontrollrutan
berördes inte. Omdirigeringsadressen exponerade postens äldre Arkis-UUID
`b2fdd4b0-49d8-11d5-a6ed-0002440207bb`. Riksarkivets publika,
skrivskyddade `Tree/SubTree`-slutpunkt gav för UUID:n bara komponentens
standardkommentar och inget bildfilsbarn eller reproduktions-id. Inga
kakor, tokens eller andra sessionsdata lästes eller bevarades.

## Forskningsresultat och återaktiveringsväg

Årdala H II kan inte bära den sökta inkommande attesten från Forssa 1875 i
det nu katalogiserade beståndet. Forssa H II/1 kvarstår däremot som en ny,
exakt analog källväg: beställ volymen hos Riksarkivet i Uppsala och sök
efter den attest som motsvarar Forssa B/3 inflyttade post 14,
**Erik Carlsson**, mottagen 1876-04-30 från Årdala till Stafsjön, folio 87.
En sådan attest kan återge födelsedata, tidigare hemvist eller andra
identitetsuppgifter, men inget sådant innehåll får infereras innan
originalet är läst.

Resultatet löser inte uppgiften `från Forssa 75`, identifierar inga
föräldrar och är inget personnoll. Det ersätter en bred idé om
flyttningsbilagor med en bevaringslucka i Årdala och en exakt, sekretessfri
beställningsroute i Forssa.

## Lokalt bevarat metadataunderlag

| Fil | SHA-256 |
|---|---|
| [Årdala H II, exakt OAI-EAD](../media/S-0527-riksarkivet-ardala-HII-OAI.xml) | `bb1848f3a1383ccbe8b48c83401230d5871c51eae96de054fc6a1d69547ad5f0` |
| [Forssa H II/1, exakt OAI-EAD](../media/S-0527-riksarkivet-forssa-HII1-OAI.xml) | `4827b110e76ea61db35257a0b3103b7f9d947a24bf0c3542790d51cc6b2aef46` |
| [Forssa H II/1, JSON-LD](../media/S-0527-riksarkivet-forssa-HII1-jsonld.json) | `d7990f77322d48354305fcfd6c3dbc4d5a28aea51c99953f8436e13612987dce` |
| [Forssa H II/1, publikt trädsvar](../media/S-0527-riksarkivet-forssa-HII1-tree.html) | `9e1ce8d4c06d92fe3ecaf0615d38f1fb08cdf0030d402420507efe9b6fb5832f` |

Personrelevansen och slutsatsgränsen redovisas i
[C-0689](../citations/C-0689-ardala-forssa-HII-erik-karlsson-atkomst.md).
