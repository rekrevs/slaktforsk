# Wotan-konvention för detta projekt

Wotan är projektets enda exekveringskö och minne för avbrutet arbete.
Läs denna fil före uppgiftsval, skapande och återupptagning; det är en
obligatorisk del av startvägen i [AGENTS.md](../AGENTS.md).
Datamodell, statusar och storlekar följer Wotan-skillen. Denna repo-lokala
konvention kompletterar den och preciserar särskilt kontinuerliga mål.

## Ansvar och läsordning

- [NORTH-STAR.md](../NORTH-STAR.md) äger målet och uppfyllelsekraven.
- [PROJECT-CONTROL.md](../PROJECT-CONTROL.md) äger styrbedömningar,
  ägarbeslut, mandat och undantag; det är ingen parallell uppgiftskö.
- [backlog.json](backlog.json) äger uppgiftsordning, status och beroenden.
  `dev-log/T-NNNN.md` äger uppgiftens omfång, resultat, verifiering och
  återupptagningsläge. Eventuella statusrader där hålls synkade med backloggen.
- Personakter, forskningsfront och täckningsmatris äger sak- och kunskapsläge.
  De ersätter inte en uppgift för beslutat utförbart arbete.
- [Personkontraktet](../genealogy/person-contract.md),
  [programmet](../genealogy/research-plan.md) och
  [källstrategin](../genealogy/source-strategy.md) styr utförandet.
  Personprofiler äger frågor, söknycklar, teman och källvägsbedömningar;
  den härledda inventeringen visar alla P-id:n utan att vara en andra kö.
- Ingen separat HANDOVER.md, sessionsstartuppgift eller parallell
  nästa-steg-lista används. Historiska handover-hänvisningar är historik,
  inte aktiva läsinstruktioner.

Vid start av taskarbete:

1. Läs kontexten enligt AGENTS, inklusive denna fil, och aktuellt mandat.
2. Läs backloggen. Välj uttryckligen begärd uppgift, annars första
   `ONGOING`, annars första `READY` med uppfyllda beroenden.
3. Läs den valda uppgiftens dev-log och dess senaste `Återupptagning`.
   Läs äldre uppgiftsloggar eller forskningsbatchar bara när det behövs
   för en konkret referens, ett belägg eller en avvikelse.
4. Kör `git status --short`, `node scripts/goal-state.mjs` och
   `node scripts/research-inventory.mjs`.
   Stäm av delvis utförda ändringar mot arbetsytan innan nästa åtgärd.
   Sakkraven i north star gäller framför missvisande måttutdata.
5. Fortsätt från kvarvarande arbete i aktuell fas, inte från planens början.
   Om ingen uppgift kan väljas, tillämpa körläget nedan.

Att läsa en instruktion eller dev-log igen innebär inte att dess åtgärder
ska utföras igen. DONE är historiskt slutfört arbete, inte en startinstruktion.

## Ändliga uppgifter, även för ett öppet mål

Varje uppgift ska före start ange:

- ett konkret kunskapsresultat eller en leverans;
- en avgränsad mängd personer, källvägar, filer eller frågor, och vad som
  uttryckligen ligger utanför;
- verifierbara acceptanskriterier och hur de kontrolleras;
- beroenden, mandat och kända hinder.

Välj S/M/L efter omfång, risk och osäkerhet; använd M vid tvekan. En
fast personkohort kan vara en uppgift om både frågor och källpassage är
avgränsade. ”Uppfyll north star”, ”fortsätt forskningen” eller ”allt som
återstår” är inte godtagbara uppgiftsomfång. Antal batchar är varken
acceptanskriterium eller bevis för källuttömning.

Nyupptäckta frågor utökar inte automatiskt uppgiften. Bevara fyndet och
lägg beslutat återstående arbete i separata ändliga uppgifter med
beroenden och referenser; obestämda möjligheter kan parkeras som IDEA.
En omfattningsändring ska motiveras och få reviderade acceptanskriterier
före vidare utförande. Dela en växande uppgift innan den blir en behållare
för en hel fortlöpande verksamhet. Dölj inte ofärdiga kriterier genom att
sänka dem efteråt.

Forskningsuppgifter följer närmaste sakligt obehandlade generation,
balanserat mellan Sverkers och Kristinas sida. Använd goal-state som
indikator, och väg in dokumenterade granskningsfel även där måttet visar
”behandlad”. När ingen generationsskiva återstår prövar Project Control
övriga uppfyllelsekrav, däribland livsbilder och relevant källtäckning.
Styrning och nödvändiga kodrättningar får egna avgränsade leveranser;
de behöver inte låtsas vara en generationsskiva.

## Forskningsuppgiftens kontrakt

Använd [forskningsmallen](templates/research-task.md) för nya forsknings-
och införandeuppgifter. Även återupptagen äldre forskning ska stämmas av
mot dessa krav, utan att redan utförda passager repeteras:

1. Ange P-id:n, hushåll/kohort, djup och sidor, utgångsläge samt vilka
   PK-01–12 och materiella frågor uppgiften ska förbättra.
2. Ange befintliga underlag, söknycklar och KP-vägar samt varför vald
   passage prioriteras: identitetsrisk, nya söknycklar, materiell livslucka
   eller annan motiverad källbredd. Planera både träd och livsbild i vågen.
3. Ge konkret tid/plats/källomfång och stoppgräns. En logisk kedja får
   rymmas i samma uppgift; skapa inte task per klick eller positiv sida.
   Nya generationer, andra livsfrågor och obegränsade svep ingår inte tyst.
4. Skapa/uppdatera berörda personprofiler först. Tillgodoräkna tidigare
   tillräcklig forskning; saknade nya fält gör inte äldre fakta osäkra.
5. Ange hur hela relevanta poster ska utvinnas och hur nya söknycklar
   prövas mot beroenden i samtliga berörda profiler. Källnoll ska ha exakt
   omfång; en oläst originalpost får inte döljas av positiv katalogrouting.
6. Kräv konsoliderad personmodell, tidslinje/livsbild i berörda delar,
   synliga öppna teman och ett motiverat frågeutfall. Ett införandepass
   får lämna sakfrågor öppna men inte kalla tomma mallar genomförd bedömning.
7. Verifiera sakligt mot belägg och strukturellt med kontrollerna nedan.
   Spara beslutat följdarbete som ändliga tasks före DONE. Återstående
   person-/projektkrav ska framgå även när uppgiften är klar.

Alla profiler behöver inte införas samtidigt. Införandet följer en
reproducerbar kohortregel: närmaste ej sakligt bedömda generation på båda
sidor, sedan nästa; befintliga kandidater och sidopersoner som hör till
undersökta hushåll behandlas i samma passage där det är relevant. Vid varje
våggranskning jämförs hela inventeringen med den behandlade kohorten så att
också äldre fristående sidopersoner/kandidater återtas i ändliga grupper.
Dokumentera vilka grupper som skjuts upp, varför och vid vilken konkret
våggranskning de återprövas. Ingen permanent exkludering genom låg prioritet.

När ett nytt närmare materiellt behov upptäcks under införandet ska det få
företräde framför djupare forskning. Ändra beroenden/ordning uttryckligen
och spara checkpointen i en omprioriterad task; lägg inte ett osynligt
stoppkrav i en personakt. Avslut av en styrimplementation startar inte i
sig en obegränsad forskningskörning.

## Spara arbete där det hör hemma

Forskningsloggen `genealogy/research-log/YYYY-MM-DD.md` är den enda
batchloggen och är append-only. Dev-loggen länkar till datum och batch,
inte en kopia av samma innehåll. Personakter, frontier och källtäckning
uppdateras med relevanta fynd; metodfiler ska inte bära aktuell uppgift.

Håll en kort `## Återupptagning` i pågående uppgifts dev-log aktuell vid
betydande delresultat, fasbyte och före ett planerat avbrott:

- **Uppdaterat:** datum; tid om ordningen annars är oklar.
- **Utfört:** uppfyllda delresultat med fil-, batch- eller beläggshänvisningar.
- **Delvis utfört:** berörda ändringar/artefakter och vad som ännu inte är säkert.
- **Aktuella frågor och beroenden:** profilens Q-/KP-id:n, nya söknycklar,
  ändrade förutsättningar och vilka följdvägar som faktiskt har omprövats.
- **Nästa ej utförda steg:** konkret fortsättning inom uppgiftens omfång.
- **Verifiering:** vad som körts, utfallet och vad som återstår.
- **Hinder:** exakt beroende, prövade alternativ och villkor för återstart,
  eller inga.

Sektionen beskriver senaste arbetsläget och får skrivas om; beslut,
utförandelogg och verifieringshistorik bevaras. Anpassa mängden text efter
uppgiften. Ingen ny uppgift behövs enbart för att spara eller läsa status.

Ett sessionsavbrott lämnar uppgiften ONGOING i rätt fas. BLOCKED betyder
att ett faktiskt beroende hindrar fortsatt utförande, inte att sessionen
tar slut. Vid återstart kontrolleras filer, sparade resultat och eventuella
externa effekter innan osäkert arbete upprepas. Om en effekt inte går att
fastställa, redovisa osäkerheten och avgör en säker fortsättning.

Filbaserad status ger ingen teknisk exakt-en-gång-garanti: ett abrupt
avbrott kan ske mellan åtgärd och loggning. Täta men meningsfulla
checkpoints och avstämning mot faktiska artefakter begränsar den risken.
Verifierad forskning upprepas bara vid nytt belägg, ändrad relevant
förutsättning eller identifierat granskningsfel, med dokumenterad orsak.

## Färdig betyder verifierad inom omfånget

DONE kräver uppfyllda acceptanskriterier, dokumenterat resultat och lästa
verifieringsutfall. En ändlig undersökning kan vara klar med ett korrekt
avgränsat negativt eller olöst resultat; det gör inte personen, grenen
eller projektets north star färdig. En uppgift vars utlovade resultat
hindras av ett beroende förblir BLOCKED. Redan beslutat konkret följdarbete
ska finnas i egna uppgifter innan den aktuella avslutas; framtida ännu
obestämda generationsvågor behöver inte förhandsallokeras.

För forskning redovisas sakligt kunskapsresultat och effekt på måtten.
Nya etiketter, färre prioritet-1-celler och gröna tester bevisar inte
saklig källuttömning. Öppna frågor, kandidater och åtkomstspärrar får inte
döljas för att förbättra måttet.

Verifieringskommandon efter ändringar:

```sh
node scripts/goal-state.mjs
node scripts/research-inventory.mjs --write
node scripts/research-inventory.mjs --check
node scripts/validate-genealogy.mjs
node --test scripts/
node scripts/media-manifest.mjs --check
```

Komplettera med uppgiftsspecifika kontroller och anspetsrevision för
berörda forskningskohorter. Uppdatera forskningsinventering och andra obligatoriska
härledningar före kontroller som jämför dem med kanoniska filer. Dashboarden är
ett uttryckligt undantag: den får bara uppdateras på ägarens uttryckliga begäran
(PCD-2026-09-05-014). Task-DONE, forskning, tester, byggen, sessionsbevarande och
commit/push medför ingen sådan begäran. Vanliga tester kontrollerar dashboardens
sparade ögonblicksbild internt utan krav på aktualitet. Kontrollera aktualitet
separat efter en beställd dashboarduppdatering enligt dashboard/README.md.
Rapportera utfall och kvarvarande luckor.
DONE nollställer aktiv fas; efterföljare blir READY när alla beroenden
är uppfyllda. Historiskt DONE-arbete återöppnas inte enbart vid sessionsbyte;
en saklig rättelse kan få en ny, hänvisande uppgift.

## Kökörning och kontinuerligt uppfyllelsemål

- **En uppgift eller en begränsad kökörning:** avsluta vid beställt omfång,
  tasktak eller tömd körbar kö enligt Wotan-skillen.
- **Uttryckligt kontinuerligt mål enligt NORTH-STAR.md:** tom eller helt
  blockerad körbar kö utlöser Project Control, inte automatiskt avslut.
  Pröva kvarvarande krav och alternativa genomförbara arbeten. Finns
  motiverat arbete inom delegerat mandat, skapa eller uttryckligen
  aktivera nästa avgränsade uppgift och fortsätt utan nytt rutinmedgivande.
  Detta preciserar skillens generella stoppregel för tom kö.
- En enskild blockerad uppgift stoppar inte andra körbara uppgifter.
  IDEA startas aldrig tyst: bedöm, avgränsa och ändra status först.
  Ägarens särskilda reservationer består.
- Avsluta målkörningen först vid dokumenterat styrkt uppfyllelse, ägarens
  paus/ändrade instruktion, eller ett konkret externt hinder/mandatbehov
  när inget annat motiverat arbete kan föra målet framåt. Vid hinder
  redovisas målet som ofullbordat, med återstartvillkor.
- Project Control får besluta att vänta eller avstå där evidensen
  motiverar det. Skapa inte en task bara för en styrbedömning eller för
  att hålla kön fylld.

Att läsa projektet eller förbereda sessionsbyte startar inte i sig en ny
forsknings- eller målkörning. Beställ inte arkivmaterial, publicera,
rendera PDF eller committa/pusha utan ägarens tillstånd för åtgärden.

## Tillfällig utloggning hos Riksarkivet

Ägarinstruktion 2026-09-05: När inloggning eller captcha avbryter åtkomsten,
spara exakt volym, bild/sida, URL, syfte och nästa ej utförda steg i den
berörda uppgiftens Återupptagning. Bevara redan lästa original och resultat.
Informera ägaren om behovet och fortsätt under väntan med annat godkänt,
avgränsat arbete, exempelvis via Riksarkivets MCP. En tillfällig
inloggningsspärr stoppar bara den åtkomstberoende passagen. När ägaren
meddelar att inloggning/captcha är klar, kontrollera den sparade passagen
och återuppta den utan att börja om eller kräva nytt rutinmedgivande.


## Ägarförbud: ArkivDigital,2026-09-05

Agenten får inte besöka eller använda ArkivDigital, inklusive dess webbplats
eller program, för sökning, katalogkontroll eller originalåtkomst. Ägaren kan
själv lämna utdrag för jämförelse med projektets källor. Ett sådant utdrag
medger inte åtkomst till tjänsten. Se PCD-2026-09-05-011.
