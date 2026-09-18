# Frågeordförråd för deltagarroller och forskningsutfall

Läsande förberedelse inom T-0643, 2026-09-17. [Biblioteket](../lib/vocabulary.mjs)
normaliserar frågesvar utan att skriva om observationer, råomnämnanden,
deltaganden eller tidigare revisioner. [Tester](../test/vocabulary.test.mjs)
körs med `node --test genealogy2/test/vocabulary.test.mjs`.

## API och gränser

```js
canonicalParticipationRole('baptism_witness', 'baptism'); // 'witness'
findParticipations(db, {role: 'witness', eventType: 'baptism'});
questionOutcomeView(question); // full fråga + storedOutcome/canonicalOutcome/active
```

`baptism_witness` är alias till `witness` **endast för en baptism-händelse**.
Samma fråga med `role: 'baptism_witness', eventType: 'baptism'` ger samma träffar.
Alla andra rollord behåller sina uttryckliga koder. `principal`, `child` och
`baptized` blir inte vittnen; `witness` blir aldrig förälder eller släktrelation.
Aliasprövningen använder varje träffs aktuella händelsetyp. En felplacerad
`baptism_witness` på en annan händelsetyp behåller ordet med `knownRole: false`.

Varje träff innehåller hela aktuella deltagarobjektet från `readCurrent`,
`storedRole`, `canonicalRole`, `knownRole` samt separata fulla `event` och
`mention` (eller null). Disposition, evidensstatus, motivering, förbehåll,
ursprung, revisionsbundna belägg och väntande omprövningar följer med.
`mention.role_literal` och `name_literal` är oförändrade. Det är aktuella
objekt som visas; deltagandets bevarade belägg anger vilka revisioner det
ursprungligen band. En väntande omprövning får inte döljas av ordnormaliseringen.

`personId` matchar endast deltagandets uttryckliga `person_id`, inte dopbarnet
som råkar delta i samma dop, ett namn eller en identitetslänk till omnämnandet.
Alla dispositioner ingår; ett accepted-event godkänner inte automatiskt en
candidate-deltagare. Uteblivet filter, null, tom sträng och enbart blanksteg
ger ingen begränsning. Okända sökord matchas bokstavligt och okända lagrade
roller visas med `knownRole: false`. Endast aktuella revisioner listas.

`canonicalQuestionOutcome` är exakt den befintliga `researchOutcome`-funktionen
från domain. `questionOutcomeView` behåller hela frågan och råutfallet samt
visar kod eller null; `knownOutcome` anger om koden finns. `retired` ger
`active: false` oavsett råutfall. Ett fastställt utfall betyder inte att frågan
är avvecklad, och gammal råtext `ÖPPEN` återaktiverar inte en retired-fråga.
Null, tomma och okända utfall får ingen gissad kod. Inga synonymer har lagts
till i domänens mappning.

## Inventering av hela 538-aktersbasen

Alla aktuella participation.role och question.outcome lästes. Det finns
**2 501 deltaganden, 34 råroller, 1 306 frågor och 14 råutfall**. Alla
förekommande rollord är uttryckligt beskrivna i bibliotekets ordförråd.
Följande är ett daterat inventeringsresultat, inte frysta gränser för framtida data.

| Lagrad deltagarroll | Antal |
|---|---:|
| arriving | 3 |
| arriving_person | 1 |
| baptism_witness | 8 |
| baptized | 15 |
| bereaved_spouse | 2 |
| bride | 14 |
| brides_guardian | 1 |
| buried | 7 |
| child | 69 |
| consenting_mother | 2 |
| deceased | 9 |
| departing | 4 |
| departing_person | 3 |
| emergency_baptizer | 2 |
| estate_declarant | 1 |
| family_member | 33 |
| father | 81 |
| giftoman | 1 |
| groom | 17 |
| heir | 7 |
| household_child | 3 |
| household_member | 30 |
| migrant | 85 |
| minors_representative | 1 |
| mother | 92 |
| officiant | 10 |
| parent | 44 |
| party | 20 |
| principal | 1 288 |
| resident | 10 |
| spouse | 105 |
| subject | 59 |
| wife | 1 |
| witness | 473 |

Frågan efter dopvittnen ger **479 träffar: 471 witness + samtliga åtta
baptism_witness**. Två andra witness hör till vigslar och ingår inte.

| Rått frågeutfall | Antal | Befintlig kod |
|---|---:|---|
| AVVISAD | 5 | rejected |
| FASTSTÄLLD | 29 | established |
| FASTSTÄLLD. | 17 | established |
| OLÖST INOM PRÖVAT OMFÅNG | 45 | null |
| OLÖST INOM PRÖVAT OMFÅNG. | 26 | null |
| OMSTRIDD | 7 | disputed |
| OMSTRIDD. | 9 | disputed |
| OPEN | 3 | null |
| STÖDD | 45 | null |
| STÖDD. | 22 | null |
| negative | 2 | null |
| open | 5 | null |
| ÖPPEN | 731 | open |
| ÖPPEN. | 360 | open |

**1 158 frågor har kod och 148 saknar kod**; ingen har lagrat null som råutfall.
De okodade orden bevaras uttryckligen och är inte liktydiga med saknad forskning.
**76 retired-frågor är inaktiva**. Kodningen har inte breddats till exempelvis
`STÖDD → supported` eller `open → open`; en sådan ändring behöver ett eget
uttryckligt beslut om innebörden.

## Två konkreta vittnesfall och verifiering

- `EP-E-baptism-P-0028-Carl-Andersson@1`: lagrad `baptism_witness`, frågeroll
  `witness`, disposition `recorded`, person_id null. Omnämnandet behåller
  `Carl Andersson` och rårollen `dräng i Botsmark, dopvittne` samt sitt
  förbehåll om att inget person- eller släktskapsbeslut följer.
- `EP-E-baptism-P-0383-Olof@1`: lagrad och kanonisk roll `witness`, disposition
  `accepted`, person_id null. Omnämnandet behåller `Olof Anderss[on]` och tom
  råroll. Det är ett namngivet vittne, inte Svens principal-deltagande eller
  ett påstått faderskap.

Åtta tester passerar i en isolerad minnesdatabas, inklusive okända roller,
tomma filter, aktuella kontra äldre revisioner, candidate/accepted,
fulla skilda bedömningar, frågenullor och avveckling. Ett separat läsprov mot
hela 538-basen kontrollerade alla 2 501 fulla deltagarobjekt och råroller,
479 dopvittnen inklusive de åtta äldre, samtliga 1 306 frågeutfall och de
76 avvecklade frågorna. Anslutningen rapporterade **0 databasskrivningar**.
CLI och domänmodell är inte ändrade av denna förberedelse.
