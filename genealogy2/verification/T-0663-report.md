# T-0663: slutlig restavstämning

Verifierad 2026-09-17. Alla 3 717 importerade dokument, 5 067 medier och
97 854 importenheter har ett spårbart utfall. Huvuddatabasen och den
journalåterspelade kopian har samma kanoniska export:
`1fc97543096073e048136e12bcb0d26cca357f60bb962a248b1cb0ca9366ecba`.
Samtliga 532 332 tidigare datarader är oförändrade.

| Aktuellt enhetsutfall | Antal | Innebörd |
|---|---:|---|
| mapped_complete | 35 109 | Explicit avgränsad strukturerad representation |
| preserved_text | 47 734 | Sökbar, bevarad text; inte full semantisk konvertering |
| preserved_history | 6 797 | Daterad historik utan nya aktuella sakgodkännanden |
| pending_interpretation | 8 214 | Bevarat tolkningsbehov med uttrycklig fråga |
| Utan beslut | 0 | Ingen teknisk redovisningsrest |

Enheterna överlappar: exempelvis finns både textavsnitt och kuraterade
ursprungsspann. De 8 214 frågebärande enheterna har 2 704 olika frågetexter;
de är varken lika många personer eller nya uppdrag. Varje äldre frågetext
och dess tillstånd är oförändrade. Kunskapsmodellen har dessutom 1 306
versionerade forskningsfrågor. Enhetstäckning, olösta sakfrågor och Wotans
utförande hålls isär. Noll väntande tekniska beroendeomprövningar betyder
inte att forskningen är klar.

## Granskade rättelser

Det versionerade paketet omfattar 111 ändringar: 22 observationers
post-/syntesgränser eller senare reservationer med relaterade slutsatser;
44 individuellt prövade, importorsakade evidensetiketter; samt tre
lysningshändelser med sex deltaganden och tre separata månadstolkningar.
Kön, ägarbekräftelse och accepterad personidentitet har inte härletts ur
importregler. De tre råa lysningsdagarna 5, 12 och 19 har oskriven månad;
april består som uttrycklig tolkning och vigseln 1 maj står kvar.

25 beroendepar har egna dokumenterade beslut om oförändrad slutsats.
Andra berörda objekt har fått nya, sakprövade versionsbindningar. Alla
äldre revisioner står kvar. 35 semantiska riskgrupper passerar både före
införsel, efter införsel och efter återställning. De 77 granskningssignalerna
och två uttryckligt avgränsade syskonobjekten är redovisade i auditfilerna;
detta påstås inte vara en ny generell sakgranskning av alla observationer.

51 hela dokument i research-context kan läsas via `context` med verifierade
byte, hash, historiskt syfte och exakta dokumentanknytningar. Äldre källvägar,
söknoll, program, utgåveunderlag och loggar förblir åtkomliga. Gamla
nästa-steg-notiser blir ingen konkurrerande utförandekö. Fem oanvända
ursprungsspann har individuellt prövats mot 31 befintliga mål och fått
uttryckligt textbevarande; inget nytt faktagodkännande följer.

## Verifiering och återbruk

- Slutligt paketförprov, full export/restore och 35 riskgrupper: PASS.
- Två CLI-införslar, identisk omkörning och två journalåterspelningar: PASS.
- Huvuddatabas och återspelad kopia: 39 journalposter, identisk export,
  0 tekniska pending och alla äldre rader/frågor bevarade.
- Fyra kontexttester, käll-/mediehashar och äldre validator: PASS.
- Första paketförslaget och dess godkända prov är bevarade separat. En
  reproduktionskontroll upptäckte fem överflödiga enhetsrevisioner i det
  första förslaget. Slutversionen utan dem har provats på nytt i sin helhet.
  Det för tidiga apply-försöket mot en då saknad slutfil skrev ingenting.

Exakta resultat finns i [T-0663-result.json](T-0663-result.json).
[Granskningsmanifestet](../migration/T-0663-support/review-manifest.json)
binder byggare, individuella bedömningar och slutoperationer;
[verifieringsmanifestet](../migration/T-0663-support/verification-manifest.json)
binder även loggar, resultat och basens radhashar. För en senare omkörning av
`T-0663-proof.mjs verify` används dess bevarade förberedelsefil
`migration/T-0663-support/logs/T0663-prior-row-hashes.json` på skriptets
deklarerade `/private/tmp/T0663-prior-row-hashes.json`. Kör inte `prepare`
mot en databas där T0663 redan är infört.

## Kvarvarande skiftesgrind

Ingen konkret konverteringsrest kräver ett nytt migrationsberoende.
T-0643 återstår med läsbar standardvy, gemensamt frågeordförråd,
identitetsgrind, full slutbackup med verkliga medier, samlad regression och
entydiga läs-/skrivinstruktioner. Sakfrågor och textmaterial ovan består
som uttryckligt redovisad kunskap efter skiftet. Detta resultat startar
ingen ordinarie forskningsuppgift.
