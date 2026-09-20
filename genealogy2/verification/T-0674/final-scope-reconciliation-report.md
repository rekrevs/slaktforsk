# T-0674: slutlig omfångsavstämning

Slut-snapshot genom **journal 94**, `T-0674/S0156-sevenR-dependency-review-v1`. Alla **36 faktiskt införda T-0674-operationer** återfinns i JSON-rapporten. Snapshot 80:s metadata, filhashar och dåvarande pending23 är bevarade under `snapshot_history`; tidigare `scope-reconciliation.json` är orörd.

Den låsta unionen stämmer exakt: **50 poster, 28 citationer, 31 ursprungsmedier + 11 tillförda källfiler = 42 unika bevarade filer**. Samtliga filhashar matchar. De elva tillförda filerna stämmer mot faktisk journal, och överlappar inte ursprungsmedierna. Alla50 poster har aktuella R-versioner, revisionshistorik, faktiska post-/stödoperationer, aktuella stöd-/följdversioner samt läst/oläst omfång och restägare. Inga förslag eller återställda misslyckade apply-försök räknas som införda operationer.

**Pending0** är kontrollerat i databasen. Efter snapshot80 är journal81–94 införda: gruppC:s23-följd,17 exakta textkopior, Albert/Charlotta32, Ånäset22, gruppA35 med17resolve, Albert9resolve, last96-granskningens25 ändringar, S0166:s5 ändringar/164resolve, census2/37, S0156:s7/97 samt de avslutande64+1+138 individuella resolve. Namnet last96 anger granskade objekt, inte96 revisioner. Inga obearbetade sakföljder har identifierats i de slutliga individuella dispositionerna; tekniskt pending0 används inte ensamt som sakbevis.

Restfördelningen täcker exakt50 poster utan överlapp i huvudägandet:

- **T-0766:33 poster.** Endast uttryckliga kvarfält och reserverade avgörande tecken. Ånäset335:10 rader×1843–1847;399:17 rader×1848–1857. Post29 på402 ingår redan och omfattar endast sina uttryckliga kvarfält i valt hushåll; inga andra402-rader eller nya406/408-svep. Post14 är Lugnet479;480 bevaras som historisk locator.
- **T-0725:2 positiva C0216-poster.** Endast målradssammanhang på bild51/s41 och171/s147 är omlästa. Bild11–50,52–170,172–221 samt andra rader på51/171 återstår i det historiska sökomfånget. Äldre bild193-noll och220/221:s blank-/slutstatus är inte nyverifierade. C0217 hör till befintlig separat sökomfångsrevision och utökar inte50-posterunionen.
- **T-0767:2 webbposter.** C0236/C0237 är inte omverifierade efter verktygsfel och Chrome-tilläggsruta. Återstart kräver ändrad åtkomstförutsättning; hindret är inget källnoll.
- **T-0214:5 C0240/Sättna-poster.** Tillgodoräkna redan bevarade/adopterade original och kvarvarande råreservationer. **T-0242** tillgodoräknar samma Sättna-mediearbete utan ny hämtning.
- **T-0367:1 Carlman1900-indexpost.** Separat original och sex rader adopterade; namn-/årsreservationer består. Grav2020056B är separat återstående passage i dess task.
- **7 grav-/PDF-/LIBRIS-poster:** avgränsat läs- eller återbruksutfall utan identifierad ytterligare obligatorisk fältpassage. PDF-utdrag är inte hela verk. C0235 återbrukar T0110.

GruppA/B:s osäkra rådagar, folionummer och överstrukna år förblir reserverade enligt de individuella protokollen. Barnets död10/9 86 är avgjord till **10 september1886**; första10/12 är historiskt avfört, inte ett jämnstarkt kvaralternativ. Carl Eriks månad i85 9/[1/7?] är fortsatt olöst. Beatas21/3 1852 är preliminär medan endast året1852 normaliseras. Ånäsets syskon-/namnkonflikter och olästa årsceller följer T0766; inga säkra personrättelser eller nya släktlänkar uppstår ur osäkra råförslag.

Kohortkorsreferenserna är bevarade, inklusive C0243:s andra gruppindex och C0314:s andra post. T0764:s tre isolerade Vännäskopior är separata samordningsobjekt. Alla sex relevanta överlämningsloggar finns och deras aktuella hashvärden är sparade. Ingen unionsförlust eller rest utan angiven ägare upptäckt. **T-0765:s programslutrevision har både T-0766 och T-0767 som uttryckliga beroenden**, verifierat i backlog och logg. T0674:s avslut kan därmed inte ensamt stänga dessa rester; originalunionen utökas inte. Aktuell backloghash är sparad; T0674 var fortfarande ONGOING vid kontrollen.

Root har rapporterat **133/133 och67/67 tester godkända** och genomför slutlig verify-, media- och payloadkontroll samt Wotan-avslut. Denna kontroll är läsande och uppdaterar endast verifieringsrapporter; inga databas-/backlogändringar eller person-/träd-/livsbildsgodkännanden görs här.
