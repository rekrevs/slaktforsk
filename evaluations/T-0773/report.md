# T-0773 — isolerad Sol-repetition av fem källposter

Sol byggde och provade ett konkret native-paket för alla fem poster, men nådde inte samma konsekvens- och konsolideringsomfång som det accepterade Astra-passet. Det isolerade provet klarade 67 exakta objektjämförelser, noll väntande granskningar och tre validatorer. Detta visar att paketet genomförde sina frysta förslag; det bevisar inte full källriktighet eller full forskningskvalitet. Ingen canonicalapply ingår i försöket.

Ägarens uttryckliga benchmarkundantag tillät endast gpt-6.1-sol för tolkning, oberoende läsning och slutbedömning i denna körning. Den vanliga modellfördelningen ändras inte av försöket.

## Design och frysning

Fas A bestod av två oberoende blinda läsningar av exakt fem ursprungsbilder och det offentliga uppgiftspaketet. Äldre svar, den kanoniska databasen och Astra-resultat var förbjudna. Primärens A–E-matriser och sammanfattningar finns under [sol-primary](sol-primary/); första råmatriserna har aldrig rättats i efterhand. Primärens manifest låstes 2026-10-01 11:00:23.837869 UTC, SHA256 `77009f85d0b55fe21cf9102ea9b0daa62881b775a1ca33f42749ff192221f61f`. Root har kontrollerat båda läsarnas manifest.

Efter båda låsen släpptes en exakt historisk baseline vid journal 227. Fas B jämförde läsningarna mot original och återbrukade tillräcklig äldre dokumentation. Svårläst text harmoniserades inte från canonicalnamn. Båda Sol-läsarna gjorde materiella första läsfel; bland annat primärens D1830/Hogstena och E30/Hogstena rättades efter originalgranskning före Astra-referens. Oberoende överensstämmelse användes inte som omröstning när båda läst fel. [Fältadjudikationerna](sol-primary/phase-b/field-adjudications-v1.json) bevarar 42 uttryckliga ändringar/reservationer. Antalet är inte ett antal unika sakfel.

Fem fullständiga operationer och besluten frystes före referenssläpp: [candidate manifest](sol-primary/phase-b/CANDIDATE-LOCKED-v1.sha256), SHA256 `a1455e27a3e43a0279888b26d14c1f976a3e4b37cccf26074c4dd190c7d9117b`, 2026-10-01 11:23:15.705264 UTC. Oberoende prereview gav villkorat klartecken för isolerat prov, med tydlig brist i bredare konsekvensgranskning. Kandidaten ändrades inte när Astra-referensen öppnades.

Referensen är accepterade slutliga implementationsspecifikationer, jämförelser och completion-resultat för C0020/C0021/C0023/C0024/C0025, med hashförteckning i [phase-c-reference.private.json](phase-c-reference.private.json). Första Astra-råmatriser är läshistorik, inte automatiskt facit.

## Omfång och mätetal

| Mått | Fryst Sol-kandidat | Accepterat Astra-passet |
|---|---:|---:|
| Exakta målposter | 5 | 5 |
| Native avgränsade person-/postadoptioner | 20 | 20 |
| Personer i adoptionerna | 13 | Samma person-post-omfång |
| Skapade/reviderade objekt | 67 | 57 |
| Nya native könspreciseringar | 10 | 7 |
| Registrerade konsekvenskandidater | 164 fallförekomster, 135 unika aktuella kandidater; bredare lucka |188 konsekvensobjekt;227 source-object-par |

Objektantal är inte ett kvalitetspoäng. Sol skapade 27 radobservationer, Astra fem sammanhållna råobservationer, och Astra reviderade fler befintliga prosa-/metodobjekt. Sols 67 ändringar är 57 nya objekt och 10 personrevisioner: fem transkriptioner, 27 radobservationer, 20 adoptioner och fem källgranskningar utöver könsrevisionerna.

Solmatriserna har 31 logiska rader, varav fyra ankarrader, och 570 strukturella poster inklusive blankfält, metadata och underdelningar. Dessa 570 kan inte jämföras direkt med Astras 256 nykontrollerade plus 63 återbrukade källfält. A och C är vardera en födelsenotis, uppdelad i barn/far/mor i Solmatrisen. B har tre målhushållsrader och fyra angränsande kontextrader; D fyra målhushållsrader; E tio administrativa hushållsrader (sju familj och tre tjänster). [scope-metrics](sol-primary/phase-b/scope-metrics-v1.json) preciserar nämnarna.

Sols utökade textsökningar gav 35/48/32/392/4100 aktuella träffvägar. Breda ort- och sifferträffar är inte sakligt stöd och lästes inte alla som fullständiga objekt. [Query screen](sol-primary/phase-b/expanded-query-screen-v1.json) och [candidate scope](sol-primary/phase-b/candidate-scope-v1.md) redovisar den begränsningen; klassgenerella retainmotiveringar ger inte samma styrka som full individuell sakprövning.

## Källjämförelse mot accepterat slutresultat

Den oberoende [Phase C-jämförelsen](sol-independent/phase-c-independent-comparison-v1.json) kontrollerade alla 50 referenshashar och redovisar 19 namngivna fält-/konsekvensgrupper. Klassificeringen skiljer MATCH, VALID_ALTERNATIVE, UNRESOLVED, MATERIAL_ERROR och OMISSION. Grupperna aggregerar olika antal celler och är ingen noggrannhetsnämnare. Materiella första blinda fel redovisas separat från den slutligt frysta kandidatens resultat.

| Post | Slutligt fryst Sol-resultat |
|---|---|
| A | Korrekt målnotisgräns och försiktig år-/datum-/namnseparation. VALID_ALTERNATIVE för reserverad fadersmånad/modersnamn. OMISSION: nedre ögla vid kvinnlig tally och spår som korsar Gift/Trolofvad-gränser saknar explicit råbevarande. Dessa märken får inte bli nya status- eller barnfakta. |
| B | Slutliga kolumnrubriker, Charlotta 67/Lerbo, koder i tryckt modernkolumn samt nattvards-/upplösningsbetydelse matchar efter förhandsrättelser. Namn, prefix och vissa ortförslag förblir UNRESOLVED. Tre extra könspreciseringar är VALID_ALTERNATIVE; angränsande hushåll hålls separat. |
| C | Kön/äkta, moder 22, Ex. och odefinierad (1 år) bibehålls med rätt källa/slutsatsgräns. Nyläsningens inline-datum/36 kontra accepterat dokumentärt återbruk är UNRESOLVED, inte bevis för felaktig baseline. Fem befintliga prosa-/metodprecisioner är OMISSION. |
| D | Slutliga 1850/Kyrkefalla/ditto och reserverade gränsmärken matchar. Båda blinda läsarna hade 1830; felet rättades före referenssläpp. Agnes PK05-kvalificering är OMISSION. |
| E | Slutliga 58/Mofalla och barnens egna/ditto-församlingsfält håller källkonflikten öppen. Reserverade tjänstefolksnamn/orter är UNRESOLVED; originalomgranskningen ger Hornborga/Frid.../Grefbäck starkare stöd än Sols Huddinge/Frötuna/Carls...-förslag. Ingen identitet följer av dessa osäkra celler. Nio befintliga syskonprecisioner är OMISSION. |

Båda slutliga Sol-läsningarna ger rätt substantiell målgräns i alla fem poster. Det utplånar inte de bevarade första MATERIAL_ERROR-läsningarna eller slutliga täckningsluckor. Samma original läst av två modeller ger kvalitetskontroll, aldrig två oberoende historiska vittnen. [Independent actual review](sol-independent/phase-c-actual-payload-review-v1.json) bekräftar alla 67 objekt semantiskt, med sex rena ordningsskillnader i evidenslistor och inga bortfall av object/version/role/note.

## Konsekvenser i native-modellen efter referenssläpp

[Native comparison](sol-primary/native-comparison-v1.json) redovisar 27 MATCH, tre VALID_ALTERNATIVE och 15 OMISSION för just de bedömda native-besluten. Detta är ingen total fältpoäng.

De 27 matchningarna är samma 20 person-post-adoptioners person-/postomfång och existens, inte ett intyg om identiskt semantiskt innehåll eller full kvalitet, samt samma sju könspreciseringar i C–E. Sols tre ytterligare B-könspreciseringar för Arne/Karl/Charlotta är en giltig avgränsad alternativ implementering: uttryckliga ogift m./gift m./gift kv.-kolumner och äldre identitetskedjor ger stöd. Inga nya personer eller relationer skapades. Astrids angränsande hushåll adopterades inte; namnsökning räckte inte som identitetsbelägg.

De 15 uteblivna precisionerna är materiella konsekvensluckor:

- C: två aktuella berättelser fortsätter att ange en fysisk födelseplats utan den kvalificering som Astra förde in. Sols separata audit skiljer föräldrahemvist från fysisk födelsebyggnad men ändrar inte dessa prosekopior. Dessutom saknas tre precisioner i källväg, moderns notreservation och PK05 om vad som nu faktiskt prövats.
- D: Agnes PK05 får inte Astras uttryckliga kvalificering att en äldre blankbeskrivning inte betyder helt bläcktom cell. Sols råobservation reserverar kantmärket, men den befintliga kontraktskopian förblir oförändrad.
- E: tre syskons RESEARCH/PK03/PK08, nio objekt, får inte kända C0917-längddatum och rättad KP02-status införda. Astras redan kända uppgifter var inget nytt bildfynd; Sol behöll äldre motsägande prosa om odaterad person/oprövad väg i stället för att konsolidera den.

Sols C-audit reserverar inline-datumet och det överstrukna 36-talet, men accepterad exakt dopdag 1886-05-01 och äldre typade fadersåldersobjekt 36 står kvar utan direkt metadatakvalificering. Detta lämnar en olöst skillnad mellan nya läsreservationer och äldre typade uppgifters metadata/query-resultat. Det visar begränsad konsolidering, men den svagare nyavläsningen gör inte de äldre accepterade uppgifterna falska eller logiskt motsägande i sig. [Residual semantics](sol-primary/phase-b/residual-semantics-v1.md) dokumenterades redan före Astra-slutjämförelsen. Artefaktens dåvarande ord ”semantisk inkonsistens” ska läsas med begränsningen ovan: en auditreservation ensam upphäver inte tidigare bättre stödda typed facts. Astras accepterade C återbrukade äldre exakt datum/åldersprövning; Sols svagare nyavläsning gör inte automatiskt detta återbruk felaktigt.

Fem äldre personstöd jämfördes individuellt mot sina aktuella recordrevisioner innan de reboundes; detta var inte automatisk versionshöjning. Äldre evidenskedjor, OWNER_CONFIRMED-faderskap och identity/life/tree-grindar bevarades. Inga accepterade namn, födelsedatum, födelseförsamlingar eller föräldralänkar ändrades i Sol-kandidaten. D/E-källkonflikterna förblir öppna och församlingsboksutdragen behandlas inte som oberoende röster.

## Faktiskt isolerat prov

Root provade exakt de fem frysta operationerna på en ny SQLitebackup av baseline 227, med separat journal. [Receipt](t0773-sol-test-j134q7u0-receipt.json) visar 67 matchande distinkta fullobjekt, inga data-/metadata-/origins-/evidence-avvikelser, pending=[] och PASS för verify, verify-assets, verify-source. Primären kontrollerade actual-full-objects-strukturen och läste de tio faktiska personrevisionernas kön/evidens; root jämförde samtliga 67 fullobjekt exakt mot förslagen. [Actual gate comparison](actual-gate-view-comparison.json) visar exakt samma inventory, 20 verifierade paths/edges och 34 personers sakliga grindutfall. Full pedigree-JSON är inte byteidentisk eftersom nya adoptioner och aktuella personhuvuden ändrar diagnostiken; historiska grindar uppgraderades inte. Dessa tekniska resultat är kompatibla med de materiella luckorna ovan.

[Final protection](protection-final.json) visar vid 11:34:41 UTC att 1840 skyddade filer har samma hash och filuppsättning: kanonisk databas/journal/operationer samt alla skyddade T-0677-artifakter. Kanonisk journal är fortsatt 237. De fem originalbilderna och frysta kopiorna har oförändrade SHA256, baseline är oförändrad, och båda första råmatrislåsen samt kandidatens v1-lås är intakta. Ingen dashboard-/arkivändring, commit eller push ingår.

## Tids-/resursjämförelse och slutsats

Astra-referensen registrerade 5692 sekunder för sitt fempostarbete och en delad budgetmätare 17→33 procent. Den 16-punktsförändringen var inte isolerad tokenanvändning och kunde påverkas av parallellexekvering. Ägarens korrigerade Sol-avläsning är 33→34 procent: en procentenhet för fem upprepade källscope, eller 0,2 procentenheter per scope. Uppgiften66 procent återtogs uttryckligen och används inte. Den observerade mätarökningen är en sextondel av Astra-passets16 procentenheter (93,75 procent lägre), men detta är ingen verifierad token- eller effektivitetsbesparing: mätaren är avrundad, det äldre passet kunde ha parallell förbrukning och Sols följdhantering var mindre fullständig. Inga tillförlitliga tokenräknare finns, och inga tokens, modellkostnader eller isolerade effektivitetskvoter har konstruerats. Solkörningen mättes från 10:48:56 till 11:39:22 UTC: 50.4 minuter, inklusive förberedelse, två läsare, paketprov och jämförelse. Referensen tog 94,9 minuter. Sols kortare tid avser ett mindre fullständigt konsekvensarbete och kan därför inte räknas som samma arbetsresultat för halva resursen. [Mätjournalen](measurement.json) redovisar gränser, moment och ägarens korrigerade slutmätning.

Fas A tvingade fram blind omutvinning före återbrukskontext, medan Astra-passet hade annan informationsordning. Körningen är därför inte ett rent kontrollerat modellkostnadstest. Den visar att Sol med två läsare kan bygga en tekniskt korrekt isolerad kandidat och rätta flera egna bildfel före referenssläpp. Den visar samtidigt materiella första läsfel och ett svagare fullständigt genomförande av konsekvenser i redan befintlig kunskap. Detta femfallsförsök motiverar inte att ersätta Astra för projektets öppna käll-/identitets-/evidensbedömningar. Den nuvarande fördelningen mellan tolkning och avgränsad implementation bör bevaras; försöket fastställer ingen allmän modellrangordning.

[Oberoende Phase C-rapport](sol-independent/phase-c-independent-report-v1.md) redovisar källgrupper och faktisk payloadgranskning. Ingen efter-referensrättelse räknas som förbättring av den frysta kandidaten.
