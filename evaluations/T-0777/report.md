# T-0777 — fem nya G001-poster

Exakt **C-0084, C-0402, C-0573, C-0896 och C-0911** är accepterade och införda efter separat hashbundet Astra-godkännande. G001 är **38/40**. T-0677 fortsätter; C-1047 och C-1060 återstår utanför denna fempostersomgång.

C-0084:s felaktiga direkta köns-, antal- och civilståndsattributioner rättades. Erik Axels kön behålls med sitt starkare 1910-stöd; identitet, moder, okänd far och födelse-/dopdatum består. C-0402 behåller den tidigare accepterade avläsningen Hildur Elisabetta; första färskförslagens Charlotta avvisades. Andra böckers namnformer och personidentiteten ändrades inte. C-0573:s egna yrkesankare skiljs nu från obruten anställning. C-0896 tillför Astrids källbundna 1926-/1930-ankare och råa inkomstuppgift utan antagen enhet eller kontinuerlig vistelse. Barnen bevaras som omnämnanden med sina identitetsgränser.

C-0911 rättar Karl Harrys dag till 17/9, Elins registrerade ankomst till 16/10, Emmas namnform till Karlsson och döds-/änkedatum till 2 juli. Följderna når observationer, aktuella berättelser, frågor, livsteman och relationsförbehåll. Torvalds ålder vid änkeblivandet preciseras till 26 och dotterns till nästan två. Ett kronologiskt omöjligt alternativ tas bort utan att lösa modersfrågan. Astrids svårlästa egen dag [21/31] reserveras; hennes starkare födelsebelägg 21 mars består.

Källtäckningen är 28 heterogena post-/personrader (1/7/2/6/12), inte 28 nya personer eller fakta. Tillräcklig tidigare forskning återbrukades, bland annat 81 logiska C-0021-celler. Fem bildkontroller gäller endast sidetiketter. Hela relevanta rubriker, rader, ditton, blankfält och marginaler samt gränser är dokumenterade i [källunderlagen](source-review/primary-handoff-index-v2.json) och efterföljande amendments.

14 kontrollerade operationer förde huvuddatabasen från journal 255 till 269: 38 nya och 90 reviderade objekt, 19 avgränsade adoptioner och 33 individuella beroendebeslut. Faktisk 128/128 fullobjektsmatch inkluderar ordnade strukturerade data, metadata, evidens och ursprung. Alla 44 174 aktuella revisioner motsvarar den granskade kopian; samtliga review-request/resolutionrader och de 14 nya journalbegärandena stämmer också. Pending 0 och verify/verify-assets/verify-source PASS. Aktuell inventory har oförändrade granskningssummor; standardverifierad pedigree P-0269 har samma 20 vägar och 19 kanter. Identiteter, relationer, kön, ägarbekräftelser och granskningsgrindar har inte uppgraderats.

Första förslagen var inte felfria. Ursprungliga läsningar, oberoende fynd, rättningar, saknade beläggskopplingar, missade text-/statuskopior och två avvisade klonförsök är bevarade. De är skilda från vad som faktiskt infördes. Se [oberoende slutgranskning](independent-review/final-review-v1.md) och [faktiskt kanoniskt kvitto](canonical-apply/canonical-result.json). Slutgranskningens formulering om 20 kanter preciseras till 20 vägar/19 kanter i [separat måttamendment](review-metric-amendment-v1.json); dess original och paketgodkännande är oförändrade.

Samtliga avslutade arbetsagenters verkliga nya turer, även återaktiveringar och slutrapporter, ingår i [usage](usage-final-v1.json). Input är summerad över upprepade anrop och till stor del cache; reasoning ingår i output och läggs inte till igen.

| Roll | Modell | Loggad input | Därav cache | Output |
|---|---|---:|---:|---:|
| Oberoende slutgranskning | gpt-6-astra | 26514202 | 25938432 | 47798 |
| Förberedelse och avgjord implementation | gpt-6.1-sol | 24309976 | 23992576 | 67823 |
| Källor och evidens | gpt-6-astra | 24017570 | 23489024 | 58290 |

Det observerade intervallet från första worker-start till denna slutregistrering är cirka 74.6 minuter, med parallellt arbete. Roots tidigare förberedelse och separat tid/tokenförbrukning är okända, inte noll. Färsk budgetstart och slutavläsning saknas; historiska 43% används inte som sessionsbaslinje. Ingen kostnads- eller kvalitetsöverlägsenhet hävdas. Alla förberedelser, granskningar, reparationer, misslyckanden och avslut räknas som produktion. Se [mätning](measurement-final-v1.json).

Stopp efter exakt fem. Inga nya original för de två återstående scopes, arkiv-/dashboardändringar, PDF, commit eller push. Arbetet är lokalt sparat på main.
