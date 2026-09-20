# Modelltest i slaktforsk – T-0769

Genomfört 2026-09-19: **60 försök**, fem nya subagentkontexter per
X/Y/Z × Astra/Sol/Terra/Luna. Alla använde `medium`, identiska frysta
uppgiftspaket per uppgift och samma verktyg. Inga omförsök eller
rättningsrundor. Ordinarie forskning förblev pausad.

## Rekommenderad arbetsfördelning

- **Astra för svår originaltolkning.** Den enda modellen som klarade hela
  bildpaketet. Sol var inte ett tillförlitligt billigare alternativ här.
  Bevara riktad andra läsning och kontroll av rad-/kolumngränser även med Astra.
- **Astra för slutlig följdprövning där bevarande av befintlig kunskap är
  avgörande.** Y visar en skillnad i helhetsbevarande, men modellrankningen
  drivs starkt av ett enda fall. Använd inte detta som allmän bevisning för
  att billigare modeller saknar genealogisk analysförmåga.
- **Sol för genomförande av fastställda ändringsbeslut med automatisk
  införselkontroll.** Samma godkända andel som Astra i Z, cirka 34%lägre
  beräknad kandidatkostnad. Det är den tydligaste omedelbara besparingen
  utan sänkt godkänd andel i detta test.
- **Terra är en kandidat för mekaniska paket med exakt specificerade
  strängar och automatisk validering.** Alla fem Z-paket var sakligt rätt
  bortsett från en extra titelpunkt. Inför inte en generell normalisering
  av källtitlar; nästa specifikation bör citera det exakta värdet.
- **Luna för utkast och välkontrollerade rutinmoment.** Mycket billig, men
  två av fem Z-paket motiverade en följdprövning för fel objekt. Låt inte
  Luna ensam stänga evidensberoenden eller tolka svåra tabellbilder.

Detta är rekommendationer för uppmätta moment; ingen modellkonfiguration
eller permanent arbetsregel har ändrats. En kedja där en billig modell
gör utkast och Astra granskar är inte testad som sammanhängande arbetsflöde.

## Godkända hela svar

| Uppgift | Astra | Sol | Terra | Luna |
|---|---:|---:|---:|---:|
| X: originalutvinning | 5/5 | 0/5 | 0/5 | 0/5 |
| Y: följdprövning | 5/5 | 0/5 | 0/5 | 0/5 |
| Z: ändringspaket, strikt | 5/5 | 5/5 | 0/5 | 3/5 |

Ett underkänt svar kan innehålla många riktiga uppgifter. Genomsnittlig
poäng var X:100/88/78/81% och Y:100/94/93/94% i modellordningen ovan.
Höga medelvärden dolde fel som kunde knyta uppgifter till fel person eller
tappa befintlig kunskap. Därför används också hela-svaret-grindar.

**X:** Två verkliga bevarade källbilder, 25 fält: Robertsfors fol 658
rader 2–3 och Degerfors fol 1064 rader 8–12. Klara datum/tomma celler samt
överstrykningar, svag blyerts och radplacering. Alla 15 underkända svar
placerade husförhörstal på fel rad. Vissa hade dessutom säkra felläsningar
av namn eller datum. Rimliga Nicolaus/Nikolaus/Nickolaus- och 12/13-varianter
godtogs; de avgjorde inte underkännandet. Gate≥68/75 och inga kritiska fel.

**Y:** Syntetiserat mikrofall från verkliga projekttyper:16 objekt,9 requests,
tydlig datumrättelse, osäkert datum, källberoende, historik/namne,
ägaruppgift, hälsotomfält och hemort/dödsort. Alla 15 underkända svar
tappade den tidigare uppgiften om familjens boende i F5. Ett svar hade
requestfel och ett var otydligt om vilket kanoniskt datum som skulle
behållas. Ingen modell etablerade en ny säker föräldrarelation.

**Z:** Två stipulerade fall i ett paket: enkel titelrättelse och
datumrättelse med fyra objekt, gammalt+nytt medium, versionsbindningar och
två individuella resolve. Alla 20 paket kunde införas i en engångsdatabas.
Fem Terra-paket hade en extra punkt i titeln. Två Luna-paket hade
otillräckligt individuellt sakskäl för F-B-prövningen trots rätt data.

## Känslighetsanalyser och brister i testet

Bedömningsgränsfallen avgjordes och låstes **före modellnyckeln öppnades**.
Frysta instruktioner, råsvar och automatresultat är oförändrade.

| Alternativ avgränsning | Astra | Sol | Terra | Luna |
|---|---:|---:|---:|---:|
| Y utan enbart F5:s bevarandekrav | 5/5 | 5/5 | 3/5 | 5/5 |
| Z om enbart titelns slutpunkt tolereras | 5/5 | 5/5 | 5/5 | 3/5 |

Y:s F5 har inget separat bifogat boendebelägg; enda explicita support är
gravkortet. Huvudbedömningen kräver att den opåverkade bostadsuppgiften
bevaras, men ett annat synsätt på detta begränsade underlag påverkar
rankningen kraftigt. Y ger därför svagt stöd för generell rangordning.
Automatikens krav på exakt `retain` för P2 och tom persons-lista var också
för snäva: en datumbevarande konfliktannotering är sakligt giltig enligt
den offentliga policyn. Den blinda sakbedömningen godtog sådana svar.

Z:s titel stod i en löpande mening utan citattecken kring värdet. Att
kopiera meningspunkten är en formateringsavvikelse, inte ett genealogiskt
sakfel. Det strikta resultatet behålls men ska inte ensamt styra modellval.

18 försök avvek från paketavgränsningen:16 läste/försökte läsa allmänna
instruktioner (två även README/NORTH-STAR; ett även gitstatus), två skrev
egna bildderivat i tillfällig katalog. Ingen läsning av facit eller andra
svar observerades. Följande är huvudgodkännanden efter att dessa 18 uteslutits:

| Uppgift | Astra | Sol | Terra | Luna |
|---|---:|---:|---:|---:|
| X | 5/5 | 0/4 | 0/2 | 0/1 |
| Y | 5/5 | 0/5 | 0/2 | 0/2 |
| Z | 5/5 | 4/4 | 0/4 | 3/3 |

Isoleringen var nya kontexter och instruktioner i gemensamt filsystem,
inte separata OS-sandboxar. Modellnamn fanns i körkatalogen, men de blinda
granskarna fick slump-ID. Exakta modellalias/medium verifierades i
körloggarna; modellvikterna kunde inte låsas till daterad snapshot.

## Tid och kostnad

USD-värdena nedan är **beräknad standard-API-kostnad**, inte faktisk
Codex-debitering eller abonnemangskvot. De använder uppmätt input, cached
input och output; reasoning är del av output och dubbelräknas inte.
Prisunderlag kontrollerat 2026-09-19: [Astra/Sol/Terra](https://developers.openai.com/api/docs/models/compare)
och [Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna).
Priser per miljon tokens, input/cache/output:10/1/50,4/0,4/20,
2/0,2/12 och 0,2/0,02/1,2. Ingen request passerade 272 000 tokens.

| Uppgift/modell | Median sekunder | Medelkostnad per försök | Kandidatkostnad per strikt godkänt svar |
|---|---:|---:|---:|
| X / Astra | 108 | $0.6063 | $0.6063 |
| X / Sol | 124 | $0.3951 | — inget godkänt |
| X / Terra | 106 | $0.3006 | — inget godkänt |
| X / Luna | 90 | $0.0217 | — inget godkänt |
| Y / Astra | 80 | $0.2915 | $0.2915 |
| Y / Sol | 87 | $0.1741 | — inget godkänt |
| Y / Terra | 79 | $0.0967 | — inget godkänt |
| Y / Luna | 76 | $0.0112 | — inget godkänt |
| Z / Astra | 38 | $0.2069 | $0.2069 |
| Z / Sol | 55 | $0.1370 | $0.1370 |
| Z / Terra | 55 | $0.0811 | — inget godkänt |
| Z / Luna | 63 | $0.0098 | $0.0163 |

De 60 kandidatsvaren kostade tillsammans cirka$11.66 enligt denna
prisproxy. Separata granskaragenter cirka$4.36, paketbyggande
agenter cirka$2.63. Huvudagentens uppmätta delsumma för planering,
orkestrering, kontroll och rapportarbete var $32.08
vid uttaget (slutrapportens sista steg tillkommer). Detta är engångskostnad
för studien och ska inte döljas eller fördelas som om det vore normal
produktionskostnad per paket.

Med lika fördelning av Z-granskarens faktiska studiearbete över 20 svar blir
kostnaden per strikt godkänt Z-svar ungefär Astra $0.272, Sol $0.202, Luna $0.124.
Det är en transparent fördelningsmodell, inte uppmätt produktionskostnad
för varje modells efterarbete. Ingen rättningsrunda genomfördes och
framtida mänsklig granskning/reparation är inte prissatt. Luna kan därför
vara ekonomisk som granskat utkast, men dess lägre kandidatpris bevisar
inte lägst total kostnad för självständig leverans.

Astra var snabbare än Sol i dessa medianer; billigare tokenpris betydde
inte kortare väntetid. Cacheandelen är hög. `results.json` redovisar även
en beräkning utan cachebesparing; den ändrar inte vilka svar som är
godkända. Avgränsade agentuppdrag och kort överlämnad kontext är därför
viktiga även när modellen väljs rätt. Orkestrering av 60 små uppdrag i en
lång huvudtråd var en betydande del av just denna studies kostnad.

## Vad slutsatserna håller för

Detta är fem isolerade upprepningar på samma lilla material, inte fem
oberoende genealogiska problem per modell. 5/5 är ingen felfrihetsgaranti
(en beskrivande 95%Wilsonintervall är ungefär 57–100%); 0/5 bevisar inte
att modellen aldrig kan klara momentet. Mellanfall, andra dokumenttyper,
andra resonemangsnivåer och stora akter har inte testats.

Sakgranskningen utfördes av separata modellblinda Astra-kontexter med
rootens efterprövning, inte en oberoende mänsklig granskare. Det kan ge
modellfamiljsbias. Observerbara rad-/databevarandefel och faktisk native
införsel ger starkare stöd än en allmän AI-poängsättning, men eliminerar
inte begränsningen.

## Bevarande och verifiering

Alla 60 svar, indata, kontrollsummor, modellval, tider, tokenposter,
verktygsanrop, blindbedömningar och individuella fel finns bevarade.
Se [README](README.md), [protokoll](PROTOCOL.md), [resultat per försök](results.csv),
[sammanställning](summary.json), [rootens adjudikation](ROOT-ADJUDICATION.md)
och [slutverifiering](verification.json).

Referenspaketet klarar 15/15 och testaren upptäcker åtta injicerade fel.
Samtliga 60 inputkopior och blindkopior verifierade;188 skyddade
databas-/journal-/mediefiler samt filuppsättningen oförändrade.
Arkiv-/Wotanvalidator:5130 assertions,3035 Markdown,5065 media, godkänd.
Den upptäckte först fleraONGOING eftersom äldre pauser stod som aktiva.
T-0675/T-0676 står nu BLOCKED av ägarens paus med sparad fas och exakt
återstartpunkt; inget forskningsarbete återupptogs. Ingen arkivsnapshot
uppdaterades för att få kontrollen att passera.

Inget commit/push, ingen dashboarduppdatering och ingen live-apply.
