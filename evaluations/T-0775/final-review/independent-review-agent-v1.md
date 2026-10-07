# T-0775: oberoende slutgranskning

**Slutomdöme: PASS för C-0026, C-0027 och C-0035, efter nedan dokumenterade rättelser.** Godkännandet gäller endast den exakta frysta kandidaten vid journal 248, inte de tidigare kandidaterna eller personernas fullständiga livsbild. Inga kända materiella fel återstår inom den genomförda granskningen. Detta är inte ett bevis för felfrihet.

Granskaren har inte skrivit till canonical, ändrat original, dashboard, Wotan eller grindar, gjort externa arkivsökningar eller startat subagenter. CLI-försökets `independent-review-v1.md` har inte behandlats som ett godkännande eller som facit.

## Exakt granskat resultat

- Manifest: `candidate-freeze-v1.json`, SHA-256 `6dc6f8610df1aa1e4efa70a9eec7c4d43763ffceff7f5106d9c3010f7800ac31`.
- Databas: `candidate-frozen-v1.sqlite`, SHA-256 `63bb63348ebd077dddf571eaaad17587a0d6caad0357abb12ef4f280d9f19578`, journal 248, baseline journal 237.
- Alla 50 filer som manifestets databas-, käll-, operations-, kontroll- och underlagslistor binder har hashkontrollerats av denna granskare: inga avvikelser.
- Manifestets elva operationer i angiven ordning ingår. De ursprungliga kandidatoperationerna nedan räcker alltså **inte** ensamma för detta PASS.

| Scope | Ursprunglig kandidatoperation | SHA-256 | Slututfall |
|---|---|---|---|
| C-0026 | `C-0026-candidate-operation-v2.json` | `42629fb2815614b75b477ae4b236930629b33bb8c0d89abf6d7c4d284fa81e85` | PASS efter independent-copy-amendment v1 och v4 |
| C-0027 | `C-0027-candidate-operation-v2.json` | `fadf920b6b4c64f238ea1dc91c90aedbb9c5a112c59ad27532f6631144e61ac7` | PASS efter independent-copy-amendment v1 |
| C-0035 | `C-0035-candidate-operation-v1.json` | `afbd59e8e8f9a9f00ed7e45d78cd2a30d21f0b9e1004397250d8d2068e313007` | PASS efter C0035-text-amendment v2 och independent-copy-amendment v2/v3 |

Rättningsfilerna är hashbundna i manifestet: independent-copy-amendment v1 `93c2e715fe74b046e82cfabbd58965aae47659d25312f4d07a4abc9ce923bb5d`, v2 `36ea4650cf5382d3eb11aa5623b87af39cba10137f2e4635b194d7aff520a2e0`, v3 `66c2cc7cb93f323ed4be3e63c2f95cc34761cd855b639db6d6e05b27c5121811`, v4 `5e6bcd66ef62cad0968d8c9cbe75170148df1e2a5bcea01fa88fc6203189c7ad`; C0035-text-amendment v2 `f5b636cb0ea2ebc8a3c444ed5092b2565e51da1b332d2c11475cd6e3524ef9e1`.

## Arbetssätt och täckning

Läst norm: shared principles, repository/Genealogy2-instruktioner, README och NORTH-STAR, den aktuella arbetsvägen och personkontraktets käll-/kopiekrav, relevant forskningsprogram/källstrategi, Wotankonvention, T-0775:s logg och backlogpost, rubric-v1, urvalslås och metadataamendment. Ägarmandatet PCD-2026-10-01-001 och ägarbekräftelsen PCD-2026-09-03-005 kontrollerades direkt.

Alla tre originalhelbilder öppnades före läsning av första Astras källslutsatser. Därefter kontrollerades deras matriser, kandidater och utpekade äldre nativeobjekt. Den preliminära kopiegranskningen skedde medan C35 ännu färdigställdes; det gemensamma manifestet tillkom efter dessa rättelser. Slutkontrollen och PASS ovan är däremot bundna till den frysta databasen. C26/C27:s tidigare enskilda freeze och rättningsoperationerna bevarar granskningsförloppet. Ingen tidigare ofärdig rörlig kandidat har godkänts.

Självständiga sökningar gjordes i faktisk `current_revision` förenad med native narrative, assessment, observation, question och search, inte endast i Sols träfflista eller ett FTS-index. Sökningar omfattade både sakfält och förbehåll: gruppuppgift/ditto/individuellt yrkesbelägg, religion/trosbekännelse, okänd eller oläst födelseort, födelseår/ålder, m-kolumn/tomfält, 353, 6900/6 900, två egna rader/värnplikt, enda egna efternamnsform, tre barn/yrkesbefordran/yrkesbana, konfirmation/nattvard, och den kvarstående Flenluckan 1900–1914. Träffar lästes i sammanhang, med fulla berörda objekt vid sakbeslut; de stora initiala sökutskrifterna var routing och inte fullständig läskvittensering. Där utskrifter trunkerades följde riktade läsningar av de relevanta objekten.

### C-0026

Original `C-0026-riksarkivet-folkrakning-1910-varsas-bild-11.jpg`, SHA `0aa43e0c7f2ea630e39664d9c10927e8b12ddb16ad585750d1c5ea6aa9dc0e7c`, 799×1239. Kontrollerat: huvudet Värsås/1910/sida11, namn/familjeroller, yrke/stam/lyte, år/ort, civilstånd, den smala nattvardskolumnen och den separata sista trosbekännelse/nationalitet/frånvarokolumnen. Postgränsen omfattar Per Vilhelm–Alma/Alva och två tjänsterader; nästa Anders Jonsson-grupp hålls utanför.

Agnes markering ligger i nattvardskolumnen, inte sista religionskolumnen. U/l-formen behöver inte avkodas säkert. Föräldrarnas 50/63 ändrar inte eller tyst löser äldre 58/67-uppgifter i C0025. Bernhard86, Johan91, Ragnar93, Rut95, Sven01 och yngsta04 är förenliga med den reserverade utvinningen. Ragnars yrkesditto och Svens oavgjorda tecken är skilda observationer. Barnens tomma nattvardsceller ger ingen livslång frånvaro. Tjänstepersonernas svaga namn/ort och Alma/Alva-normalisering lämnas reserverade.

Äldre stöd som faktiskt lästs inkluderar aktuella BIO/Q/KP-objekt för syskonen och deras C0917-tillägg med exakta längddagar, flytt- och militärnycklar. Dessa uppgifter har inte ersatts av censusårtal. Agnes andra originalbundna C0024-reservation är en annan cell och behålls. Aliasfrågan P0295 förblir historiskt avvecklad och skapar ingen åttonde person.

### C-0027

Original `C-0027-riksarkivet-folkrakning-1930-limhamn-bild-532.jpg`, SHA `5eb6e6aa40e23bf8cb48dc232ffe854329bacdcfcbad9d0a88583f563795f1a3`, 6621×4958. Kontrollerat: tryckt huvud, folio3365, familjeklammern r30–33 och samtliga grupper av tryckta fält till högermarginalen. Grannrader görs inte till Bernhards familj.

R30 Värsås/86, r31 Oskarshamn/98 och r32–33 förs./24/27 står i födelsekolumnerna. 353/572/X−/fortsättningsstrecket ligger i separat tryckt m-kolumn. Denna position är belagd; en kodnyckel eller moderns faktiska ort är inte avkodad. Bernhards kassör/Kraftverk, gift/23, ankomst Oskarshamn/23, skol5, barnkod och 69— bevaras rått. Hustruns vigsel/ankomst är dittoburen. Barnens yrkesställnings5 blir varken ålder eller skolbildning. Hustruns yrkestecken är prövat men inte säkert läst. Gräns-/kodspår tillskrivs inte automatiskt rätt eller fel person.

Kontrollerade äldre nativebedömningar: P0014/Q01 och BIO-P0014 bevarar 1927 mot familjens1925; P0012/Q01 skiljer känd församling/år från oläst egen födelsenotis; P0011:s datum kommer från egen vigselpost och Oskarshamn är uppgiven ort från SCB, inte bevisat genom ännu oläst födelsebok. P0010/Q04 och KP07 har kvar verkligt odekodade koder men visar att rubrik-/positionskontrollen är gjord. P0013:s okända födelseort1938 är korrekt kvarstående osäkerhet och kan inte fyllas från föräldrarnas1930rad. Ägarbekräftade fadersrelationer står kvar.

### C-0035

Original `C-0035-riksarkivet-SE-ULA-10257-AIIa3b-bild-122-sida-420.jpg`, SHA `4083597f4d80485431a3617293dcef5fa4a244d65f13a65a2baaa9ecb56c5697`, 5699×4020. Kontrollerat: båda sidornas18kolumner över r1–6, fosterbarnen r8–9 och Torvalds eget hushåll r10–12, samt den svaga mellanradsposten vid r3/4. Den orelaterade senare ägargruppen ingår inte.

Rå v under rubrikens två alternativ är inte ett vaccinationsdatum. Kunskap/nattvard, tomt eget husförhör, Adas attest/äktenskapstext och Astrids konfirmation15/5/1912 med första nattvard16/5 hålls isär. Militärnumren r4/r5/r10 är söknycklar utan tjänstgöringsslutsats. Torvald återkommer r10 med eget Jansson, snickeriarb., giftdatum12 23/6, annan internhänvisning/ofvanr3 och12 23/4, samt utgående p352/13 12/9. Ingen tyst harmonisering mellan dessa datum görs. Emma Karlsson[?] mot senare Rhodin[?] förblir källvariant, inte ny kvinna eller säkert namnbyte. Maudr12 och fosterbarnens egna modertexter är kontext, inte automatiskt nya accepterade person-/föräldranoder.

R10:s svagare dagtecken får inte sänka äldre starkare egen rad: `O-P-0045-A-3933-reported_birth@1` lästes i baseline, med Blacksta A I/16 s59 `88 ³/₈`, Wadsbro, och uttrycklig oläst egen födelsenotis. BIO-P0045@3:s förbehåll och källbundna två yrkestitlar lästes. Tures maj/junikonflikt, överstrukna äldre avgång och Adas svaga interlinjära not behålls. Noten fastställer ingen mor, barnidentitet eller födelse-/dödhändelse. Astrids äldre allmänna tomfältsbeskrivning ersätts utan att hennes redan belagda konfirmation tappas.

## Oberoende fynd och slutlig disposition

**F1, materiellt, C26: dittotecken blev felaktigt ett förbud mot personuppgift.** I kandidatens `BIO-P-0024@2.markdown` stod: “jordbruksarbetare är därmed en gruppuppgift och inte en anteckning om honom”. `RESEARCH-P-0024-9d76f0343410@3.body` bar samma argument. Originalets Ragnarrad har eget dittotecken under Johans utskrivna Jordbruksarbetare, ungefär x273–391/y875–896. Det upprepar uppgiften på Ragnars rad; det tar inte bort hans personbundna attribution.

Ytterligare aktuella kopior: CONTRACT-P0024-PK06@2 “han har ingen egen yrkesanteckning”; PK07@2 spärrar Jordbruksarbetare som egen yrkesuppgift; PK09@2 säger att dittot inte blir egen uppgift; KEY-P0024-a8ace2e6328f@2 “Spärrad som individuellt belägg”; THEME-P0024-ARB@2 bevarar den äldre personbegränsningen; O-P0024-census-1910-fields@2.caveat begränsar yrket till gruppuppgift. Detta var **behållna äldre fel**, inte en ny påhittad Soltolkning. C26-dispositionernas explicita retain av nyckeln och PK-kopiorna var otillräcklig.

Rättelse: egen dittoburen yrkesuppgift1910; inte eget utskrivet ord, bestämd arbetsgivare, anställningsform eller yrkesvaraktighet. Historisk nedgradering finns kvar som historik. Slutkontrollerat i BIO@3, RESEARCH@4, PK06/07/09@3, KEY@3, THEME-ARB@3, O@3. Ingen grind eller generell evidensuppgradering. Delat förbehåll i andra Ragnarobjekt om “inte ny självständig yrkesanteckning” kan stå kvar som skillnad mellan upprepning och självständigt utskrivet ord/oberoende belägg; det är inte samma uttryckliga individuella spärr.

**F2, precision, C27: missad födelseortsnyckel.** `KEY-P-0011-5a3111f7ed7b@1.body`: “Originalbelagd i vigselboken; födelseförsamlingen är inte läst.” Den fanns inte i C27:s dispositionslista. C27r31:s födelseort Oskarshamn står separat från m572. Slutlig @2 begränsar den olästa delen till egen födelsepost/säker församlingstillhörighet och bevarar uppgiven SCB-ort. Det accepterade datumet ändras inte.

**F3, precision, C35: yrkesbana respektive faktisk källbunden titel.** `RESEARCH-P-0045-9d76f0343410@1.body` sade “en yrkesbana från snickeriarbetare till verkmästare”, medan primärspecifikationens söksträng “en yrkesbefordran” inte fanns där. Källans r10 har Snickeriarb.; äldre BIO@3 skiljer redan senare verkmästare från bestämd befordran. Slutlig RESEARCH@3 anger källuppgifter om titlarna utan belagd bestämd befordran. Samma passage har två namngivna döttrar och separat systerson; ingen tredje barnrelation skapas.

**F4, precision, C35: kvarvarande två-radersräkning.** `PATH-P-0045-KP-04@1.body`: “belagt i två av hans egna rader”. Den motsvarande Q/MIL-texten var rättad men denna kopia återstod. C35r4/r10 har samma inskrivningsnyckel i förkortad/full1908form. Slutlig PATH@2 säger flera egna rader med C35ankare. Själva inskrivningslängden står fortsatt EJ UNDERSÖKT, korrekt; flera bokceller blir inga självständiga tjänstgöringsbelägg.

**F5, materiellt, C35: Charlottas nya daterade ankare nådde inte hennes aktuella luckbeskrivningar.** `BIO-P-0043@4.markdown` kallade “åren1900–1914 mellan folkräkningarna och Ljungbacka” kvarvarande lucka. THEME-P0043-BO@1.body, CONTRACT-P0043-PK03@1.body och P0043/Q01@1.body återgav samma odelade period utan1908ankaret; deras caveats löste inte det. Originalets egen r2, ungefär y734–863, har ditto i kol9/10 efter r1 p335/08 16/10 och i16/17 efter p402/14 30/10.

Slutkontrollerat i BIO@5, THEME-BO@2, PK03@2 och Q01@2: känd bokföring1908-10-16 och1914-10-30 uttryckligen tillgodoräknad; mellanleden1900–1908 och andra luckor kvarstår. Ingen obruten fysisk vistelse eller full livsbild härleds. Den daterade preciseringen ersätter uttryckligen den för vida äldre luckformuleringen. PATH-P0043-KP05:s egna andra sju källor är fortfarande oprövade inom sitt namngivna omfång och ska inte gröntvättas av denna C35läsning.

## Slutkontroller och kvarvarande gränser

Det hashbundna fullobjektsprovet visar98/98 aktuella objekt med korrekt data, arrayordning, metadata, underlag, ursprung och version; pending0. verify, verify-assets och verify-source har lästs med exit0/ok. Dessa tekniska resultat ersätter inte fyndprövningen ovan.

Egen direkt jämförelse av baseline mot den **frysta** slutdatabasen visar exakt oförändrade aktuella revisioner för4019 person-/relations-/identitets-/identity_resolution-objekt,42 OWNER_CONFIRMED och527 legacy/native granskningshuvuden; inga nya objekt i dessa jämförda kategorier. Pending0 har också kontrollerats direkt i fryst SQLite. Identitet, trädverkan och livsbild slås alltså inte ihop av ändringarna.

Ingen ny originalkontroll har gjorts av arkivhandlingar utanför de tre valda bilderna. Äldre starkare belägg har lästs som aktuella nativeobjekt/proveniens, inte utgetts för ny omläsning av deras original. Kodnyckeln1930, svaga bokstavsformer, vissa marginaldateringar, biologisk attribution av blyertsnoten och kvarvarande egna födelse-/vigsel-/dödposter är inte lösta. Dessa är synliga käll- eller forskningsgränser, inte kvarvarande upptäckta materiella fel i den nu godkända begränsade kandidaten. Canonicalapply och dess efterkontroll ingår inte i detta granskarresultat.

## Tillägg: granskning av metadata inför kanoniskt införande

**PASS även för de exakt hashbundna staged-operationerna.** `evaluations/T-0775/canonical-ready/stage-freeze-v1.json`, SHA256 `1fd013eb97e24f4f289c53f365ee748ccfb6a90f777f2939ebd6511d46729d52`, binder de elva operationerna i tillämpningsordning. Metadata-manifestet har SHA256 `9a5078474e1760daef9323388e738c7952e76061e27f37d90b6dc80edb888fcc`. Det knyter an till ursprunglig kandidatfreeze SHA256 `6dc6f8610df1aa1e4efa70a9eec7c4d43763ffceff7f5106d9c3010f7800ac31`; dess frysta databas förblir oförändrad.

Egen strukturell jämförelse av samtliga elva gamla och nya operationer visar endast det yttre `reason` ändrat i tre källoperationer. Formuleringen om exklusiv klonanvändning ersätts av kontrollerat kanoniskt införande efter självständig slutgranskning. Alla övriga värden är identiska, inklusive id, actor, ändringar, underlag, ursprung, enskilda motiveringar och resolutions. Åtta operationer är byteidentiska. De tre ändrade staged-filerna under `genealogy2/operations/` har följande verifierade SHA256:

- `T-0775-C-0026-candidate-v2.json`: `884eb45483c23d9e7beeebee8dfc9164f50ee9443661865df5304d8528814dc4`.
- `T-0775-C-0027-candidate-v2.json`: `17bc267929538a03e7fc9d0764ec3256cf9a44155275e663fd84f455f7c2d3bf`.
- `T-0775-C-0035-candidate-v1.json`: `65ba84bf73f7375028ee5361ff1403eef3b6599ef08c044fe328f2789e5294bf`.

Ny sekventiell replay från j237 ger j248, 98/98 fullständiga objektmatchningar, pending0, tre godkända validatorer och oförändrade skyddade invariants. Resultatfilerna har lästs och deras hash kontrollerats. Staged-databasens verifierade SHA256 är `571a38d9c44474abd87482401bdb9dba580ce9138415fcfb1261b70ebbbad705`; pending0 har även kontrollerats direkt där. Denna metadataändring påverkar inte den sakliga prövningen ovan och kräver ingen ny källtolkning. Godkännandet avser exakt detta paket, inte framtida ändringar. Kanonisk tillämpning har inte utförts av granskaren och dess efterkontroll återstår hos utföraren.
