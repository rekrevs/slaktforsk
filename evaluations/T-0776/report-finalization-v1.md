# Slutlig mätning T-0776

Samtliga tre arbetsagenter var avslutade före den slutliga logginsamlingen, inklusive deras sista svar. Förberedelse, implementation, sakbedömning, oberoende slutgranskning, rättelser och misslyckat skrivförsök räknas. Root är okänd, inte noll.

| Roll | Modell | Loggad input | Därav cache | Output |
|---|---|---:|---:|---:|
| hybrid_sol_lead | gpt-6.1-sol | 17603603 | 16948096 | 55469 |
| hybrid_astra_sources | gpt-6-astra | 10416942 | 10124544 | 32853 |
| hybrid_astra_final | gpt-6-astra | 13234924 | 12653312 | 33841 |

Input summeras över återkommande anrop och är till stor del cache; reasoning ingår i output. Dessa tal är inte ett belagt mått på debiterad veckobudget. Start39% är preliminär, slutavläsning väntar. Ingen halvering är visad.

Arbetsresultatet är tre accepterade poster,41 grupperade råfält och31 unika kunskapsobjekt (12 nya,19 reviderade), med32 revisionshändelser och6 individuella beroendedispositioner. G00133/40. Slutgranskningen fann tre formella materiella precisions-/täckningsbrister; upptäcktstider, ytterligare primära följdkorrigeringar och rättningar är bevarade.

Se [arbetsrapport](report.md), [sakgranskning](independent-final-review-v1.md), [slutlogg](usage-final-v1.json) och [mätkvitto](measurement-final-v1.json). Senare procentavläsning läggs i separat amendment.
