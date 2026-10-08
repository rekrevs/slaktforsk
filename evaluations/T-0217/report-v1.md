# T-0217: avgränsat Sol-test, källutfall och överlämning

2026-10-08. Axel=P-0241; Emma=P-0246. Initial namn/P-id-omkastning rättad som uppdragsmetadata, ingen identitetsändring. Wotan är ONGOING tills root godkänt liveinförande och avslut.

## Sakresultat

| Passage | Verifierad metadata | Personbunden originalpost | Rest |
|---|---|---|---|
| Emma1963 | FIIa65(1963), SE/HLA/1040237; alfabetiskt CIIc1(1930–1964), A–Ö i häften, Härnösand, Läsesal | Ingen läst | Egen registerrad, aktnummer och bouppteckning olästa. |
| Axel1983 | Sundsvalls tingsrätt SE/HLA/1040239/F/FII listar1983volymer90–99 med96a/b,98a/b; DIVd1(1972–1985), A–Ö i häften, Härnösand, Läsesal | Ingen läst | Egen registerrad/aktnummer och exakt jurisdiktion ofastställda;1983volymdetaljer oprövade. |
| Axel28965/21 | Katalogen har Ro65=Sundsvalls västra; kandidatväg Io5/Io21. Io5D2 börjar1927; Io21D3 listar1902–1926 men saknar1919–1922; Io21D2 slutar1918; H/F täcker1898–1915. | Ingen läst; ingen1921enhet identifierad | Nummerformatets personkorrelation,1921placering och förband förblir olösta. |

Läsesal och saknad bildlänk är prövade katalogfält, inte terminal EJ DIGITALISERAD eller källuttömning. Katalogexistensen av1983material omprövar den äldre generella uteslutningen från RA, som redan kvalificerades i C0936/T0119; den lokaliserar inte en egen Axelakt. Inget ekonomiskt ägande, militär tjänst, ny identitet eller relation har härletts.

## Bevarande och återbruk

C0936/S0733 och aktuella fulla person/research-objekt återbrukade. Accepterade T0787/T0792 egna läsningar och grindar har inte upprepats. De tre `sources/*catalogue-extract-v1.txt` bevarar hela relevanta utvunna metadatafält med uttrycklig normaliserad whitespace; dessa är extraktrepresentationer, inte fulla DOM/faksimil eller olästa original. SHA256 och mediaförankring avser just respektive bevarat extrakt. Separata faktiska MCPsvar finns som JSON; det första nollsvaret har native search-memory/1 och exakt frågesträng/parametrar. Leverantörens Senast ändrad är bunden till namngiven katalogpost; bild-/indexversion är uttryckligen okänd där den inte exponeras.

API före browser: Emma två JSON-LD-endpoints gav sandboxDNS följt av Errno54 connection reset; AxelFII gav403; Ro65metadata gav TLS-handshake-timeout. Inloggad katalogreserv fungerade. Dessa åtkomstfel är inte söknoll. Browser content export var ej stödd; relevanta synliga DOMfält lästes och bevarades som kvalificerade extrakt. MCP-årsfiltret gav synliga felårsträffar och används inte som certifierad1921avgränsning.

## Faktiskt arbete och caps

- Emma:4katalogsidor (FIIaserie,65detalj,CIIcserie,1detalj); materialcap2katalogenheter+1namnregister med dess serieledning.0namnregister-original och0bouppteckning lästa.
- Axel1983:3katalogsidor (FIIserie,DIVdserie,DIVd1detalj);2katalogenheter+1register.0original och ingen godtycklig1983volymdetalj öppnad.
- Militär:7riktade länkade hierarki-/serielistsidor;0identifierade1921volymer eller original öppnade, cap högst2identifierade1921enheter. Ingen distrikts- eller volymsvepning.
-6MCPmetadatafrågor totalt:2bouppteckningsupptäckter,4militära upptäckter/omformuleringar;1initial exaktfrågenoll med senare positiv Ro65kontroll,1årfilterinkonklusiv.2externa primärkällesökfrågor för nummerguide gav ingen läst/bärande guide.
-4unika API-URLs;6networkanrop plus2sandboxDNSförsök.3native routingoperationer,23ändringsrevisioner för21objekt;7befintliga aktuella objekt revideras,14nya objekt;3individuella livsbildsretains.3textmedier.

## Kvalitet och rättelsebörda

Root påtalade och sakgodkände3paketrättelser: bouppteckningsklass K14; temporalbindning av T0119 no-searchtext; exakt blanksteg/parametrar i MCP-materialidentifieraren. Tidigare faktiska accepterade klonrequests med CLIpolicy och receipts bevaras i preserved-stage-attempts/; inte påstådda ursprungliga råinputs. Tekniskt fanns1ineffektiv skyddsjämförelse som avbröts och ersattes med Set; ingen dataeffekt.3klonrundor med3sekventiella apply vardera, inga applyfel; sista rundan binder slutpaketet. Initial uppdragsnamnomkastning är separat upptäckt metadatareparation.

## Verifiering och exakt slutpaket

Slutklon: `/private/tmp/T0217-approvedstage.sqlite`. verify-db-v2, verify-assets-v2 och verify-source-v1 har `ok:true`. Kloninventory har oförändrade mått216identityPassed/68treeSupporting/68identityGatePassed/1explicitNativeLifePassed.3utlösta beroenden prövades individuellt: båda daterade LIFE-T0792 failed behålls, eftersom inga egna ekonomi-/militäroriginal lästs och personlivsrester kvarstår. Identitet/träd/OWNER/relationer ändras inte. Hela44477baselinehuvuden utanför7befintliga ändringsobjekt är identiska; pending0.

Ingen kod-/modelländring: fulltestsuite har inte omkörts. Root kompletterar liveverifiering efter canonicalapply. verify-source-v1 återbrukas för oförändrat fryst källunderlag och oförändrade staged media/pathbindings; sista rättelserna ändrar endast native metadata. Root har också registrerat ett felaktigt read-only kolumnnamn utan dataeffekt, därefter rättat fråga.

| Operation | SHA256 filinnehåll |
|---|---|
| evaluations/T-0217/emma-routing-v1.json | `27db8350840977d878ff1c7a90b4d9fe7b3a21de22b972bd69eea4d4455cfdea` |
| evaluations/T-0217/axel-routing-v1.json | `b82a7185edaf7a41acb6c9493905f5f90677cd6d17ca07fca10130c99a6566bb` |
| evaluations/T-0217/mil-routing-v1.json | `e4ff2627daf592ada8ed0be38949f0f7f8ea48638ea935bf5da1bb325388678c` |

`stage-proof-v1.json` namnger representationerna. BaselineSQLite FILHASH=`ac9a24ebf62d03c8b349c7973343629941689cc5020342e44a60690eb1df3361`, unchanged. canonical(exportData)baseline=`ffbc69292cde3411ed61ffcbb8b7193f19ab1d998f2b4fada83f0864db936449`; stage=`7342a29ba7d8b373a91323e2af40a0ec8e0a3b48be1ead2cb592cb72ba3645eb`. SQLoperation-rowcount492→495 inkluderarbootstrap; journal latestsequence491→494. Ingen liveapply/commit/push utförd av worker.

## Restägare och produktion

T0822 har sparad första-resultattrigger och planeringsansvar för exakta olästa register-/akt-/1921placeringar; den har inte exekverats. T0216 äger senare boende/dödsrouting; T0793 separat fortsatt livsbildsplanering. Originalutvinning eller beställning kräver separat ändligt scope/mandat. Återstart: tillgänglig exakt egen CIIc1/DIVd1rad eller självständigt nummerguidebelagd1921volym. Ingen ny uppgift startas här.

Rootstart17:05:49UTC; workerrapport färdig omkring17:24UTC, cirka18min inklusive läsning, primär metadataåtkomst, förberedelse, tre klonrundor, rättelser och verifiering; root har tillkommande egen produktion. Faktisk worker-token/cache/output-usage samlas av root efter FINAL. Rotens osynliga usage är okänd; inga besparingsanspråk.

## Beständigt sökminne — kompletterat kvittopaket

Root identifierade efter första FINAL en bevarandelucka:6MCPfrågor men5sparade svar, samt två utförda webupptäcktsfrågor utan individuella kvitton. Inga sökningar upprepades. Det saknade exaktaårssvaret fanns i retained toolstore och har nu sparats som mil-exactyear-discovery-v1.json. Den tidigare Medelpads-inskrivningsfrågan och årfilterfrågan har separata inkonklusiva kvitton med sina exakt faktiskt skickade parametrar och fulla bevarade MCPsvar.

De två webfrågorna var `site.riksarkivet.se "65" "rullföringsområde"` och `site.riksarkivet.se inskrivningsnummer 1921 rullföringsområde`, skickade samtidigt med response_length=short. Resultat fanns; inget primärt nummerguideoriginal öppnades/lästes. Båda har nu separata inkonklusiva kvitton. numbering-guide-web-discovery-v1.json bevarar exakt frågebatch och samtliga16visade titlar/URLs som trogen screeningrepresentation. Det råa strukturerade svarobjektet sparades inte vid första anropet; byte-exakt råkopia, snippets och fördelning av den gemensamma resultatlistan mellan de två frågorna är uttryckligen otillgängliga, inte rekonstruerade. En gemensam extrakthash påstås inte identifiera två separata primärkällor.

Exakt tid för ursprungliga anrop var inte bevarad; faktiskt utförande ligger inom17:05:49–17:14:05UTC, medan svarets lokala bevarande/observedtime anges separat. Okända leverantörsversioner är explicit UNKNOWN. Detta är dokumentär receiptskomplettering, inga nya externsökningar, inga noll eller originaltolkningar. Den kompletta nya operationen `T-0217/discovery-receipts-v1` har7nya objekt (3sources,4search),3medier och inga befintliga revisionsändringar. Den tidigare3operationers exakta hashes består. Appended till samma slutklon; focused4receiptfält/kopiehash/outcome +3nya mediahashar PASS,pending0. `stage-proof-v2.json` binder4operationspaketet och ny slutstagehash; tidigare djupare protection/db/assets/sourceverifiering återbrukas.

Detta tillför en uppdagad kvittotäckningsreparation och ungefär5–6min workerproduktion efter förstaFINAL, inklusive bevarande,7objektspreparation, en klonapply och fokuserad verifiering; inga gamla3apply eller källpass återupprepades. Totalt4operationspassager men fortsatt endast3sakliga routingpassager. Faktisk usage för både workerturns samlas av root efter senasteFINAL.

Slutlig total:4operationer,30ändringsrevisioner för28unika objekt (7befintliga,21nya),6medier. Journal latestsequence495, SQLoperation-rowcount496 inklusivebootstrap. Slutstage canonical(exportData)-SHA256=`6fd30246fd393acbd5f7ab1848ab29622ab4c1a59910b6b3e38f5da3bad44a27`. Fjärde operationsfil SHA256=`27e48b9a6b8f08d4fc018736b613a8a275383a91e24ad2506beb495ee78e10e8`. stage-proof-v2 är kombinerad4opspinning med återbrukad44477protected-headproof och explicit new-only fjärdedelta. Root har läst och sakgodkänt receiptskompletteringen. Ingen ny original-/sökpassage eller sakresultat tillkom.


## Root — faktiskt infört och verifierat

2026-10-08T17:34:05.322098+00:00: Canonical journal492–495,pending0. Fyra exakt granskade operationer tillämpade; faktisk export med38 auktoritativa tabeller är lika slutklonen bortsett från exakt fyra operationstidsstämplar, arrayordning bevarad. Liveverify/db/assets/source PASS. T0217 DONE, T0822-trigger sparad utan taskexecution. Total tid från rootstart till verifierat avslut 28.3min; inkluderar Sol, rootgranskning, rättelser, bevarande, införande och verifiering, före Gitfinalisering. Faktisk Sol usage i usage-snapshot.json; root okänd. Metadata-testet visar genomförbart arbete med lokala dokumentationsrättelser; originaltolkning och jämförande modellkvalitet/kostnad har inte testats.
