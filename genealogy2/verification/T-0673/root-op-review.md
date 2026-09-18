# T-0673 rootoperation: oberoende kontroll före apply

Granskat `T-0673/root-pilot-v1`, 19 ändringar, mot aktuell huvuddatabas
(read-only), `blind-root.json`, `second-c.json` och operationens samtliga
fält. Ingen apply eller ny bildläsning genomförd av denna granskare.

## Rätta före apply

1. **Namnvariantens nya belägg saknas i faktats beroenden.**
   `F-P-0070-name_form-Hildur-Charlotta` får fältet
   `source_variant_census1900: Hildur Elisabetta`, men evidence innehåller
   endast de två äldre husförhörsposterna. Lägg till exakt stöd från
   `O-P-0070-census1900@2` eller `R-126171c8899cd464e47c503b@2`, uttryckligen
   avgränsat till 1900-variantens avläsning. Behåll husförhörsbeläggen för
   personens tidigare namnform. Annars ser det nya fältet maskinellt ut att
   stödjas av fel böcker och träffas inte av en framtida rättelse av utdraget.

2. **De nya rättelsenoterna skapar nya olänkade textberoenden.** Åtta objekt
   får P06-noten men har fortfarande tom evidence:
   `RESEARCH-P-0070-9d76f0343410`, `KEY-P-0070-70f9a99df603`,
   `PATH-P-0070-KP-01`, `P-0070/Q-01`, `P-0070/Q-02`, `BIO-P-0070`,
   `RESEARCH-P-0072-9d76f0343410`, `KEY-P-0072-1a778158c11c`.
   Lägg versionsbundet beroende till den nya observationen/avskriften/posten,
   med not att det gäller nytillagd rättelse och dess följdresonemang,
   inte automatisk beläggning av hela det återbrukade textblocket.

## Kontroller som passerade

- Alla expectedVersion-värden matchar aktuell databas; samtliga explicit
  åberopade versioner finns antingen redan eller skapas tidigare i samma
  operation. P09:s postversion 2 finns redan.
- Den rättade P06-postens bevarade medielänk finns kvar. Origins bevaras.
  De tre utbytta gamla postberoendena ersätts uttryckligen med postversion 2;
  inga andra gamla explicita beroenden tappas.
- Person P-0070 ändras inte. Husförhörens Hildur Charlotta och utdragets
  Hildur Elisabetta hålls åtskilda, liksom systern Hanna Matilda/Mathilda.
  Ingen ny person eller identifiering tillkommer. Namnvariant eller skrivfel
  i originalet avgörs uttryckligen inte av detta prov.
- Förstaläsningen reserverade namnändelsen; kontrolläsningen anger Elisabetta.
  Operationen bevarar den relevanta skillnaden mellan källor och hänvisar
  till båda läsningarna. Denna granskning är inte en tredje bildavläsning.
- Råår 78 bevaras separat från normaliserat 1878. Inga nya exakta dagar/månader
  eller barns patronymikon skapas. Fadern och sex barn, inga hustrur,
  kolumntomheter och angränsande hushållsgränser redovisas.
- P08:s audit reserverar bleka namn och begränsar noll till sida 263.
  Aktuell sökning säger redan ”återfanns inte”, utan helvolymsfrånvaro.
  P09–P12 skiljer sekundär vy, bevarad metadatasammanfattning, ägarutsaga
  och oläst åtkomstblockerat original; inga nya primära personfakta införs.
- Övriga textträffar, bland annat ASSESSMENT-P-0070 och PATH-P-0072-KP-01,
  befanns använda personnamnet eller äldre husförhörsläsning, inte uttryckligen
  återge den felaktiga 1900-raden. De behöver inte namnbytas mekaniskt.

## Teknisk begränsning

Operationen saknar explicit dependencyReviewVersion. Det är tillåtet via
ordinarie CLI `apply`, som tilldelar version 2; direkt anrop till
`applyOperation` utan flaggan skulle använda äldre version 1. Scratchprovet
måste därför använda samma policy som den avsedda skrivvägen.
Ingen körbar apply-validering ingick i detta read-only uppdrag. Provdatabas,
individuell följdprövning och huvuddatabasens postkontroller återstår hos root.

## Slutlig disposition 2026-09-18

Båda fynden rättades före apply: det reviderade faktat och samtliga åtta följdobjekt har avgränsade versionsbundna belägg. Operationen applicerades via CLI policy2; de55 följdprövningarna är individuellt avslutade i T-0673/root-resolve-v1.
