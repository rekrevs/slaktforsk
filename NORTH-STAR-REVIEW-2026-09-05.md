# North star som uppfyllelsemål — granskning 2026-09-05

Status: granskningens förslag har antagits och införts i NORTH-STAR.md genom
ägarens instruktion och PCD-2026-09-05-002. Texten nedan bevarar underlaget.
Implementeringsluckorna kvarstår; ingen ny forskning startas vid sessionsbytet.

## Bedömning och förbättringar

Målets värde, balans och evidenskrav är tydliga. Dokumentet blandar däremot
önskat resultat, arbetsordning och administrativa mått. Registrerade avslut
kan därför bli bevis för sitt eget berättigande.

1. Skilj löpande underhåll från en daterad uppfyllelsebedömning för dagens
   källäge. Framtida digitalisering är inte ett ändligt acceptanskriterium.
2. Definiera arkivfront som gränsen för fortsatt beläggbar utvidgning.
   Belagd föräldrarelation innebär normalt fortsatt arbete med föräldern;
   den är inte i sig skäl att avsluta grenen. Nuvarande definition är tvetydig.
3. Skilj olöst kunskapsfråga, dokumenterat hinder och uttömda fortsättningar.
   IDENTITET OLÖST bevisar inte att fortsatt identitetsarbete saknas.
   Åtkomstfel kräver bedömning av tillåtna alternativ och är inte källslut.
4. Kräv konkret beroende för varje villkorlig källväg: vad saknas, varför
   behövs det och går det att ta reda på nu? Namn, barn, ort och tid kan ge
   en avgränsad sökning även utan eget exakt födelsedatum.
5. Gör personernas livsbilder till ett eget krav med tillämpliga teman och
   motiverade luckor. Nuvarande mått täcker främst direkta anpositioner.
6. Skilj källfamilj från leverantör. Redovisa relevanta identifierade
   nätleverantörer, prövat omfång och verklig åtkomstgräns. En betaltjänst
   utan tillgänglig åtkomst är ett hinder, inte en genomsökt källa.
7. Kräv en avslutningsrevision där återstående materiella frågor har
   undersökts eller fått källstyrkta hinder efter prövning av rimliga
   alternativ. Tom kö, registrerade statusar och gröna tester räcker inte.

Arbetsordning och verktygsdetaljer kan flyttas till forskningsplan/Wotan.
Mått ska uttryckligen vara indikatorer för styrning, inte ersätta evidens.

## Konkreta implementeringsluckor

- scripts/goal-state.mjs: coverageOverride med KLAR kan åsidosätta matrisens
  prioritet-1-celler. Frånvaro av 1 innebär annars klarstatus utan prövning
  av om villkor i 2 redan kan uppfyllas.
- scripts/lib/terminal-status.mjs: citationens existens kontrolleras men
  inte beläggets räckvidd. Återaktiveringsfältet krävs i text men inte i kod.
  VERIFIERAD accepteras utan motsvarande innehållskontroller.
- Sannerby C-0863: äldre ortsavsnitt läst; vigseloriginal oläst efter 403.
  Det räcker inte till slutsatsen att vidare relevanta vägar är uttömda.

Kod kan kontrollera struktur och vissa motsägelser. Saklig källuttömning
kräver också en dokumenterad evidensbedömning. En ny statusetikett ensam
löser inte problemet.

## Förslag till deklarativt uppfyllelsekontrakt

Projektet uppfyller målet för det dokumenterade källäget vid ett angivet
granskningsdatum när samtliga följande villkor är styrkta:

- Direkta anlinjer har följts balanserat så långt tillräckliga belägg
  medger. Varje kvarvarande föräldrafråga har ett källgrundat hinder efter
  att tillämpliga, rimligt avgränsade fortsättningar prövats.
- Varje identifierad person har en konsoliderad, källförankrad livsbild.
  Relevanta luckor och konflikter är undersökta eller konkret motiverade.
- Materiellt relevanta kandidater är prövade till identifiering, avvisning
  eller dokumenterat hinder; osäkra relationer ingår inte i säkert träd.
- Relevanta källfamiljer och identifierade nätleverantörer är prövade inom
  dokumenterat omfång. Återstående beroenden kan inte lösas genom fortsatt
  tillåtet och rimligt avgränsat arbete i det aktuella källäget.
- Belägg, kontroller, identitetsbedömningar och original är spårbara och
  bevarade. Granskningen kontrollerar att de faktiskt bär slutsatserna.
- En avslutningsrevision visar att ingen materiell, genomförbar och
  motiverad forskningsåtgärd inom målets omfattning återstår. Externa
  spärrar och behov av nytt mandat redovisas separat, inte som uppfyllelse.

Praktisk fullständighet avser materiella frågor och rimligt avgränsade
källvägar; varje omnämnande på internet behöver inte hittas. Project Control
motiverar avgränsningar med evidens och förväntat kunskapsvärde, inte enbart
arbetsmängd. Underhåll återöppnas av nya källor, ändrad åtkomst eller nya
uppgifter. Inför inga nya publiceringskrav utan separat beslut.

## Kopierbart mål för nästa session

> Uppfyll projektets north star enligt NORTH-STAR.md, med dokumenterad
> evidens för samtliga uppfyllelsekrav. Arbeta kontinuerligt inom mitt
> befintliga mandat tills kraven är styrkta eller fortsatt framdrift är
> beroende av ett konkret externt hinder. Projektets persistenta tillstånd
> är utgångspunkten; redan utfört och verifierat arbete gäller fortsatt om
> inget nytt belägg eller identifierat granskningsfel motiverar omprövning.
> Övriga ägarbeslut är delegerade till Project Control.

Målet anger ett önskat slutläge, inte en startsekvens att upprepa.
Läsordning och återupptagning regleras i [Wotan-konventionen](wotan/README.md).
Denna granskning är ett daterat beslutsunderlag, inte en parallell backlog.
Konkreta kvarstående arbeten har avgränsats i
[T-0048](wotan/dev-log/T-0048.md) och [T-0049](wotan/dev-log/T-0049.md).
Texten startar inte en ny målkörning vid sessionsbytet.
