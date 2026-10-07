# T-0784 — slutrapport

Tre centrala personer och deras 21 identitetskrav har omprövats med redan accepterade läsningar. Arbetet är infört i Genealogy2, journal **443**, med **0** öppna följdgranskningar. **18 av 21 krav** är uppfyllda. Inga nya originalavläsningar, källanskaffningar eller personer ingår.

| Person | Aktuell identitetsgranskning | Trädverkan | Exakt återstående spår |
|---|---|---|---|
| Evy P-0211 | GODKÄND | BÄRANDE | Befintligt underlag räcker för identitetsnivån. |
| Arne P-0003 | UNDERKÄND | AVVAKTAR | Den direkta hänvisningen från den redan använda inflyttningsposten C-0882 nr 132, 1943-11-24, till egen församlingsboksrad på uppslag 15. Gemensam insats hos T-0379; Arne-följder hos T-0227. |
| Maj P-0007 | UNDERKÄND | AVVAKTAR | Eget uppslag 15 och egna mantalsrader 1945–1946 hos T-0379; relevant redan åberopad Flen AIIa/7c fol 744 rader 9–10 behöver bevaras och radens kolumner 9–13 fullutvinnas, samordnat hos T-0237/T-0377. |

Arnes och Majs personidentiteter och accepterade relationer består. De underkända utfallen gäller identitetsnivåns konkreta kvalitetskrav. Uppslag 15 behandlas en gång för båda personerna. Majs bildkrav är avgränsat till den faktiskt använda familjeposten; de övriga tre folierna i moderuppdraget finns kvar i den lägre prioriterade kön. Den exakta volymen, åtkomsten och Majs egna registerrader är ännu oprövade. Inloggning eller kataloguppgift lovar inget innehåll eller onlineåtkomst.

| Mått för den registrerade kärnan | Före | Efter |
|---|---:|---:|
| Registrerade anor | 160 | 160 |
| Godkänd identitetsgranskning | 75 | 76 |
| Egen passerad identitets-/trädgrind | 49 | 50 |
| Obruten verifierad antavla, Adam | 19 | 20 |
| Obruten verifierad antavla, Axel | 19 | 20 |

Evy är den enda nytillkomna personen i de verifierade vyerna. Livsbildens granskningsutfall är separat och bevarat; ingen ny livsbildsgranskning har gjorts. Antavlorna intygar inte att hela kärnträdet är färdigforskat.

Införandet omfattar en kontrollerad operation med nio objekt: sex nya native identitets-/trädbedömningar och tre nödvändiga Maj-rättelser. Rättelserna kvalificerar födelseår kontra exakt datum, Södertäljevägens åtkomst/egna rader samt den äldre felaktiga fol16-slutsatsen i biografin. Äldre PK-granskningar, starkare relationsstöd, OWNER_CONFIRMED, avvisade alternativ, historik och ordnade bevis-/ursprungsfält är bevarade. Inga relationer har uppgraderats av ett nytt granskningsutfall.

Både primär och separat Astra har granskat det exakta paketet och det faktiska resultatet på kopian. Huvuddatabasen matchar den granskade kopian över alla 50 tabeller, råa JSON/BLOB-värden och native ordningsföljder; endast den nya operationens registreringstid skiljer. Relevanta 19 regressionstester och aktuella validatorer har passerat. Tidigare 12 accepterade G002-kvitton har oförändrade hashvärden; G002 har fortsatt 19 poster kvar. Detta pass tillför ingen ny källpost.

Återbruket och resterna är sparade append-only i fem befintliga Wotan-uppgifter: T-0214, T-0227, T-0237, T-0377 och T-0379. Alla gamla loggbytes, scopes, acceptanskriterier, beroenden och backlogposter är bevarade. Wotan är fortsatt ensam utförande- och återupptagningskö. Ingen ny uppgift eller automatisk prioritetspromotion har gjorts. Passet slutar efter T-0784. Nästa ej utförda steg är Project Control för en ny avgränsad kärnfront; ingen automatisk DEFERRED-fallback.

Metod och verkligt arbete: båda ursprungliga bedömningarna och de additiva omprövningarna är bevarade. Den oberoende initiala Arne-bedömningen ändrades efter att den direkta egna hänvisningen prövats. Primär skickade kandidatmetadata före den oberoende filfrysningen; exponeringen och tidigare egna lässpår redovisas explicit, utan blindhetsanspråk. Den separata fullständiga paket-/resultatgranskningen är bevarad. Stoppade format-/parser-/pin-försök och reparationer ingår i produktionen.

Observerad förlupen tid från det sparade körmandatet till denna rapport: **68.1 minuter**, inklusive förberedelser, båda Astra-rollerna, implementation, felaktiga försök, reparationer, kontroller och slutadministration. Roller arbetade parallellt; detta är väggtid.

Observerbara nya workerturns efter fasgränsen: **1 743 910 ej cachade inputtoken**, **48 608 640 cachade inputtoken**, **163 682 outputtoken**. Av output är 22 917 reasoningtoken, redan inkluderade. Totalt observerad workerinput är 50 352 550 och input plus output 50 516 232. Rootens användning är **UNKNOWN, inte noll**; delad budgetförbrukning och monetär kostnad är inte härledda. Ingen kostnadsbesparing påstås.

Verifierbara underlag:

- [Faktisk rootacceptans](root-actual-three-person-canonical-acceptance-v1.json).
- [Exakta kärn- och antavlemått](implementation/actual-three-person-core-and-both-pedigree-before442-after443-metrics-v1.json).
- [Faktiska fem ägaruppdateringar](implementation/actual-five-owner-append-only-administration-receipt-v1.json).
- [Faktisk workeranvändning](actual-final-three-worker-new-turn-usage-v1.json).
- [Wotan T-0784](../../wotan/dev-log/T-0784.md).

Rapporttidpunkt: 2026-10-05T17:58:38.088483+00:00. Slutlig Wotan-status och sista återupptagning bokförs av root efter dessa kontroller.
