# T-0643: sakgranskning av föräldrarelationernas nature-koder

Granskad 2026-09-17 mot aktuell 538-personersbas, med databasen öppnad
`readOnly:true`. Omfång: fullständig kodinventering och sakprövning av exakt
tre relationer för P-0287, P-0451 och P-0452. Rapporten ändrar inga data,
bedömningar, profiler eller antavleregler. Inga originalbilder eller nya
arkivkällor har öppnats.

**Rekommendation:** tillåt `biological_parent` → `biological` som uttryckligt
läs-/frågealias. Den enda aktuella förekomsten är ett redan ägarbekräftat
biologiskt faderskap. Bevara lagrad kod och `OWNER_CONFIRMED`. Låt däremot
`correlated_parent` fortsätta vara en egen kod utan ny anlinjepassage eller
gradering: de två förekomsterna bär en särskild, dokumenterad invändning mot
den äldre bevisgraden. Detta är inget generellt godkännande av parent-koder
som synonymer.

## Fullständig inventering

677 aktuella `relation_type='parent'`: 633 `accepted`, 42 `candidate`, en
`recorded` och en `rejected`. Fyra lagrade nature-koder förekommer;
`biological` har noll förekomster.

| Lagrad nature | Disposition | Evidence status | Antal |
|---|---|---|---:|
| biological_parent | accepted | OWNER_CONFIRMED | 1 |
| correlated_parent | accepted | CORROBORATED | 2 |
| recorded_parent | accepted | CORROBORATED | 424 |
| recorded_parent | accepted | OWNER_CONFIRMED | 16 |
| recorded_parent | accepted | TRANSCRIBED | 190 |
| recorded_parent | candidate | CONFLICT | 2 |
| recorded_parent | candidate | CORROBORATED | 1 |
| recorded_parent | candidate | LEAD | 18 |
| recorded_parent | recorded | TRANSCRIBED | 1 |
| recorded_parent | rejected | REJECTED | 1 |
| reported_parent | candidate | CONFLICT | 1 |
| reported_parent | candidate | LEAD | 20 |

Kodtotaler: `biological_parent` 1, `correlated_parent` 2,
`recorded_parent` 653, `reported_parent` 21. Urvalet omfattar aktuella
revisioner, inte alla historiska versioner. Reproducerbar läsfråga:

```sql
SELECT x.nature, r.disposition, r.evidence_status, count(*) AS n
FROM current_revision r JOIN relation x ON x.revision_id = r.id
WHERE x.relation_type = 'parent'
GROUP BY x.nature, r.disposition, r.evidence_status
ORDER BY x.nature, r.disposition, r.evidence_status;
```

## Exakta relationer och riktning

Alla tre har okänd relationstid och inga väntande omprövningar. Riktningen
är **förälder → barn**. Ett födelseår är inte automatiskt relationens
exakta startdatum.

| Aktuell revision | Förälder → barn | Lagrad nature | Disposition / evidens | Rekommenderad frågebehandling |
|---|---|---|---|---|
| REL-parent-P-0287-P-0239@1 | Johannes Ivar Fredberg → Anders Ivar Höök | biological_parent | accepted / OWNER_CONFIRMED | Läsalias biological; hela bedömningen och råkoden består. |
| REL-parent-P-0451-P-0338@1 | Hindric Henriksson/Vinroth → Henrik Henriksson, född 1829 | correlated_parent | accepted / CORROBORATED | Egen kod består; ingen synonym till biological eller recorded_parent. |
| REL-parent-P-0452-P-0338@1 | Brita Flinkberg → Henrik Henriksson, född 1829 | correlated_parent | accepted / CORROBORATED | Egen kod består; ingen synonym till biological eller recorded_parent. |

### P-0287: uttryckligt biologiskt faderskap

[P-0287:s akt](../../genealogy/people/P-0287-johannes-ivar-fredberg.md), A-1617,
anger uttryckligen biologisk far. A-2413 och
[PCD-2026-08-29-001](../../PROJECT-CONTROL.md#pcd-2026-08-29-001) fastställer
faderskapet som säker projektinformation och ersätter kravet på en separat
faderskapshandling. Den fulla [C-0545](../../genealogy/citations/C-0545-agarens-uppgift-johannes-ivar-fredberg-ar-ivars-far.md)
bevarar ägarsvaret och beslutets exakta omfattning. Äldre kyrkoposters tomma
fadersfält upphäver inte det beslutet.

Relationens native evidence har tre `supports`-bindningar:

| Exakt basisrevision | Källa och innebörd |
|---|---|
| R-249199a82fde432f693b1dd2@1 | C-0545, `owner_statement`, S-0434: ägarens säkra uppgift 2026-08-29. |
| R-6f983503f83108ffc538a6de@1 | C-0259, `relayed_family_statement`, S-0108: tidigare uppgift från annan släktforskning. |
| R-e6cef8fd83b378bfc281edeb@1 | C-0320, `family_statement`, S-0249: Margareta Hööks förmedlade uppgift om sin farfar. |

Den direkta origins-enheten i C-0545, rader 9–25, är
`7172f5c23d24d761d2530e3cb350e574bdb08f03c8b79c19478d022726e2e33e`.
Övriga origins återger P-0239:s rader 68, 70, 73 och 101. De tre R-posterna
är olika dokumenterade utsagor, inte ett påstående om tre oberoende
arkivbevis. Relationens eget förbehåll anger dessutom att Hudiksvall omkring
1902 är berättelsens sammanhang, inte en exakt relationsstart.

Här ändrar aliaset endast kodstavningen i en läsvy. Det innebär varken
nedgradering till `TRANSCRIBED`, ny arkivbekräftelse, nytt familjefaktum eller
godkänd personprofil. Familjeberättelsens äktenskapshinder är fortfarande en
separat uppgift.

### P-0451 och P-0452: bevarad korrelation med senare gradinvändning

Hela akterna för [P-0451](../../genealogy/people/P-0451-hindric-henriksson-vinroth.md)
och [P-0452](../../genealogy/people/P-0452-brita-flinkberg.md), inklusive
historik, skiljer vuxenpersonernas identitet från deras relation till Henrik
1829. Föräldrauppgiften är uttrycklig i Nybergs sekundära familj 99,
[C-0623](../../genealogy/citations/C-0623-nyberg-familj-99-henrik-brita-foraldrar.md).
Akterna bevarar äldre `CORROBORATED`, medan C-0623:s tillägg T-0201,
2026-09-10, invänder att den explicita släktskapskällan fortfarande är en
sekundär röst. Tillägget drar inte tillbaka relationerna.

De fulla citerade texterna, inklusive senare tillägg, ger dessa gränser:

- [C-0594](../../genealogy/citations/C-0594-ljustorp-AI6-bredsjo-lagfors-rundbacken-ledtradar.md)
  identifierar Jonas och Cecilia och deras sidkedjor. Den namnger inte
  Henriks föräldrar och anger uttryckligen att originalen inte visar
  syskonskapet. T-0201 upprepar denna gräns.
- [C-0470](../../genealogy/citations/C-0470-ljustorp-martha-brita-fodd-och-dod-1856.md)
  visar Jonas och Cecilia som dopvittnen. Den senare analysen av vittnenas
  orter är omständighetsstöd, inte ett nytt biologiskt syskonbevis.
- [C-0624](../../genealogy/citations/C-0624-ljustorp-AI3-hindric-brita-original.md)
  visar Hindric, Brita och tre äldre döttrar före 1829. Den korroborerar
  parets identitet men är inte Henriks egen föräldrapost.
- [C-0626](../../genealogy/citations/C-0626-lagfors-AI1-rundbacken-original.md)
  har ett senare Rundbackenankare. Henriks frånvaro i en bok som börjar
  1860 motbevisar inte hans ursprung före utflyttningen 1850; Britas frånvaro
  ger ingen egen dödsdag.

Detta är föräldraslutsatser med ett beskrivet korrelationsunderlag, inte
bara alternativa ord för en direkt avläst eller biologiskt fastställd
föräldralänk. En synonymregel skulle dölja en relevant osäkerhetsgräns.

Båda native relationerna har tom `evidence`-lista. Deras genealogiska
provenans finns i origins till [P-0338:s akt](../../genealogy/people/P-0338-henrik-henriksson-lagfors.md):

| Omfång | Exakt origins-unit |
|---|---|
| Båda: rad 54, A-2536, det äldre kandidatsteget med hänvisning till senare A-2591 | f30b92b47c2338deaee413900386316daee7e8aa9d00a36bd14a901506ebfb64 |
| Båda: rad 64, A-2591, den bevarade föräldrabedömningen | 8cfcdccd2dfc26c9628e227d79f54d816f2a54b33c5c38e9edcf5257478bedc1 |
| P-0451: rad 92, uttrycklig far | 51b3414c8d46252dbf76b8ccf7024d85f29305e457ae55629426c8e591a1e65c |
| P-0452: rad 93, uttrycklig mor | 63cd0ca3cca6b7048b598bec0472e673bdeec59c9f581070f05d42b089ffb7b0 |

Det generella relationsförbehållet, att ingen ospecificerad biologisk art
eller tidsgräns fylls i, ersätter inte den specifika gradinvändningen.
Invändningen är redan native och sökbar i två aktuella F-objekt:

| Aktuell revision | Subjekt och väsentliga fält |
|---|---|
| F-P-0338-identity_assessment-parents-and-secondary-conflicts@1 | P-0338: `direct_own_birth_parent_record_read:false`, `explicit_relation_source:Nybergfamilj99`, `original_witness_role_is_sibling_proof:false`, `late_2026_09_10_grade_objection_preserved:true`, `retained_existing_grade:CORROBORATED`, båda föräldrarnas P-id. |
| F-P-0451-source_assessment-family99-grade-objection@1 | P-0451: `explicit_relation_only:Nybergfamilj99`, `originals_C0594_C0470_prove_identity_and_witness_not_kinship:true`, `secondary_not_independent:true`, `relation_not_withdrawn:true`, `late_note:T0201,2026-09-10`. Origins omfattar även P-0452:s A- och relationsrader. |

De är personbundna fakta, inte fakta med relationerna som `subject_id`.
Ingen av de tre granskade relationerna har sådana relationsegna F-objekt.
En läsare som bara hämtar relationens evidence eller dess direkta
relationsegna fakta missar därför de två korrelationslänkarnas senare
invändningar. De fulla F-objekten kan redan hämtas med `readCurrent(db,id)`
eller `node genealogy2/cli.mjs inspect <F-id>`; origins visar de fulla
källtilläggen. Rapporten inför inga nya bindningar.

## Profiler och kvarstående spärrar

Native `identityGate` har kontrollerats separat. Samtliga fyra nedan har
`identity_review:failed`, `tree_effect:waiting` och `passed:false` enligt
`ASSESSMENT-P-NNNN@1`. Även livsbildens granskning är underkänd, men den
utgör en separat axel.

| Person/profil | Aktuell profilgranskning | Identitetsnivå / trädverkan | Relevant avgränsning |
|---|---|---|---|
| [P-0287](../../genealogy/research-profiles/P-0287.md) | 2026-09-07 | UNDERKÄND / AVVAKTAR | Fullfält-/kopierester är skilda från det ägarfastställda faderskapet. Senare redan bevarade rättelser får inte tappas. |
| [P-0451](../../genealogy/research-profiles/P-0451.md) | 2026-09-08 | UNDERKÄND / AVVAKTAR | PK-05/11: egen C-0626-fullfältsrest och konkreta historiska kopierester. Vuxenpersonens avgränsning är prövad. |
| [P-0452](../../genealogy/research-profiles/P-0452.md) | 2026-09-08 | UNDERKÄND / AVVAKTAR | PK-11: senare Rundbackensidors kopierest; de fem egna tidiga raderna är fullprövade. Okända föräldrar görs inte till en ny identitet. |
| [P-0338](../../genealogy/research-profiles/P-0338.md) | Profil och ASSESSMENT-P-0338@1 | UNDERKÄND / AVVAKTAR | Äldre accepterad föräldrabedömning innebär inte en godkänd identitetsgrind. |

Aliaset för P-0287 får därför inte ensamt ge passage i läget `verified`.
`typed` kan redovisa ägarens relation utan att låtsas godkänna profilen.
`correlated_parent` behåller sin separata naturspärr även i `typed`.
Aktuell `accepted/CORROBORATED` för de två länkarna bevaras som lagrad
bedömning; denna rapport gör varken en ny uppgradering eller nedgradering.

Det finns också fyra `recorded_parent`-länkar från P-0451/P-0452 till
P-0463/P-0464 som redan bevarar motsvarande sena gradinvändning. Kodnamnet
`recorded_parent` garanterar alltså inte en direkt originalpost. De länkarna
är en avgränsande jämförelse, inte ett nytt omprövningsuppdrag.
`REL-parent-P-0461-P-0451@1` och `REL-parent-P-0462-P-0451@1` är
`candidate/CONFLICT`, även om deras nature är `recorded_parent`.
Familj 99 får inte återföra familj 98 till antavlan.

## Kontrollkrav för eventuell frågeintegration

1. Aliaset visar både lagrad `biological_parent` och frågekoden `biological`,
   med oförändrad riktning, revision, `accepted` och `OWNER_CONFIRMED`.
2. Ingen rå revision skrivs om; faderskapets ägarsäkerhet kräver ingen ny
   arkivhandling. Profilspärren i `verified` består.
3. `correlated_parent`, `reported_parent` och okända koder faller inte genom
   någon generell parent-normalisering. De två granskade korrelationslänkarna
   får ingen ny anlinjepassage eller evidensgrad.
4. Relationerna och deras redan befintliga sakinvändningar och profiler är
   fortsatt åtkomliga, även när antavlevyn utesluter en kant.
5. Disposition, väntande omprövningar och åberopade osäkra identiteter
   prövas som tidigare. En kodöversättning får inte acceptera kandidater.

Verifiering av rapportunderlaget: alla 677 aktuella parent-rader räknade;
de tre exakta relationernas origins, evidence och pending lästa; båda
begränsande F-objekten och fyra native identitetsgrindar kontrollerade.
Endast denna rapport har skapats i deluppgiften. Root avgör och testar
eventuell läs-/frågeintegration i T-0643.
