# Gemensam standard för personakter

Version: `person-dossier/v1`, införd 2026-09-07 i T-0112 enligt
PCD-2026-09-07-026. Prövas i T-0113 före utrullningen.
[Personkontraktet](person-contract.md) äger sakkraven och färdignivåerna;
denna standard äger presentationen. [Personmallen](templates/person.md)
och [profilmallen](templates/research-profile.md) anger tabellkolumnerna.
Standardinförande är inte genealogiskt godkännande.

## Filernas ansvar

| Information | Kanonisk plats |
|---|---|
| Aktuell person, namn, sakpåståenden, relationer, kronologi och berättelse | `people/P-NNNN-*.md` |
| Identitetsargument, söknycklar, tio teman, Q-/KP-frågor, källstrategi och daterad PK-bedömning | `research-profiles/P-NNNN.md` |
| Källinnehåll, läsomfång, reproduktioner och provenans | Befintliga citationer, källposter och media |
| Ursprungliga observationer och senare rättelser | Append-only evidens- och forskningslogg |
| Kohort, utförande, verifiering och nästa ej utförda steg | Wotan-backlog och uppgiftens dev-log |
| Härledd överblick | Forskningsinventeringen; ingen egen arbetskö |

Akten länkar sin profil från Arbetsläge. Profilen länkar aktens tidslinje
och biografiska sammanfattning. Undvik dubbla aktiva bedömningar: hänvisa
till profilens daterade argument när en kort sammanfattning räcker.

## Rubriker och tabeller

H1 är `P-NNNN: Fullständigt namn`. Följande H2 finns exakt en gång, i
ordningen nedan. Tabellernas rubriker och kolumnordning följer personmallen.

1. Arbetsläge
2. Identitet
3. Namnformer
4. Påståenden
5. Relationer
6. Tidslinje
7. Boställen och flyttar
8. Yrke, utbildning och ekonomi
9. Militärt, civilt och rättsligt
10. Hälsa och död
11. Media och personliga källor
12. Biografisk sammanfattning
13. Forskningsfrågor och konflikter
14. Historik och rättelser

De särskilda H2 `Integritetsnot` och `Slutstatus` får förekomma efter
Forskningsfrågor och konflikter och före Historik och rättelser, med sina
befintliga sakregler. Slutstatus skapas bara när frontreglerna medger det.
Övrigt individuellt material placeras under lämplig rubrik, vid behov som
H3. Flyttning får inte förlora innehåll, länkmål eller historisk innebörd.

Ett avsnitt utan sakuppgifter får en kort individuell förklaring, till
exempel vilket underlag som saknas eller vilken integritetsavgränsning som
gäller. Behåll tabellhuvudet men skapa inga påhittade rader. `—` betyder
saknad uppgift i en cell; det betyder aldrig ett genomfört negativt fynd.
Ingen levande person behöver en fabricerad dödspost eller generell utfyllnad.

Profilens sex H2 och tabeller följer profilmallen exakt. Q-/KP-id:n är
stabila inom personen; uppdatera utfall i befintlig fråga när den besvaras.
Skapa inte samma fråga på nytt. Extra daterade resonemang får underrubriker
under rätt huvudavsnitt. Obligatoriska statusfält ska förekomma exakt en gång.

## Namn, datum och text

- Använd ett motiverat visningsnamn; redovisa belagda stavningar,
  patronymikon och familjenamn med användningstid och belägg i Namnformer.
  Källcitat behåller sin stavning. Varken förälders namn eller makes namn
  bevisar automatiskt personens eget namn, namnbyte eller namnbytesdatum.
- Skriv säkra fullständiga datum `ÅÅÅÅ-MM-DD` i tabeller. År får stå ensamt
  när precisionen stannar där; skriv `omkring`, `före`, `efter` eller ett
  uttryckligt intervall vid osäkerhet. Fyll aldrig en saknad dag med 01.
  I löptext får datum skrivas naturligt på svenska.
- Ange plats så precist som belägget tillåter, med socken/församling när
  det behövs för att skilja likalydande orter. Bevara osäker ortläsning.
- Skriv aktuell kunskap i sammanfattningen. Ett senare fynd ska föras in
  även i tidslinje, relevant tematabell, relationer och profilens frågor.
  Orden ”obelagt”, ”oläst”, ”återstår” och ”okänt” ska alltid prövas mot
  sparade belägg. Oklart, inte undersökt och undersökt utan träff skiljs åt.
- Håll prosa proportionerlig mot materialet. Skilj personfaktum,
  källuppgift, inferens, familjeminne och allmän historisk kontext.
  Syntes får inte göra en osäker uppgift säker eller ge en nolla större
  räckvidd än den granskade källpassagen.

## Belägg, konflikter och historik

Varje sakrad har A-/C-hänvisning enligt evidensmodellen; varje id ska gå
att slå upp. Relationer länkar rätt P-id och har belägg, relevant tid/plats
och oförvanskad status. En person i hushållet är inte automatiskt syskon.
Bevara assertion-id:n och deras spårbarhet vid omstrukturering.

Aktuella slutsatser anger vilka belägg som bär dem och hur motstridiga
uppgifter vägs. En rättad äldre uppgift märks tydligt med hänvisning till
rättelsen; den får inte stå kvar som en parallell aktuell sanning.
Evidensledgern skrivs inte om. Nya källtolkningar och sakrättelser följer
projektets rättelsemodell; redaktionell avstämning länkar befintlig rättelse.

Historik och rättelser bevarar relevanta tidigare bedömningar med datum,
orsak och länk till ersättande belägg/batch/beslut. Flytta historiska
arbetslägen dit och märk dem som historiska. Dubblera inte aktiva
maskinlästa statusfält. Historiska beslut ligger kvar i Project Control.

Konkurrerande identiteter förblir separata. Ägarbekräftade uppgifter och
integritetsavgränsningar består. Nya konflikter med OWNER_CONFIRMED lyfts
för ägarprövning; ingen normalisering får upphäva dem.

### Tabellförda källor: redovisa uppslagets tryckta kolumner

En citation som återger en post ur en tabellförd källa — husförhörslängd,
församlingsbok, ministerialbok, folkräkningsblad — ska lista uppslagets
**tryckta** kolumnrubriker och för varje kolumn ange om den är **avskriven**,
**tom** eller **oläst**.

Skälet är att en cell som inte nämns i dag inte går att skilja från en cell
som är läst och tom. Personaktsprogrammet har funnit fyra fall där en tryckt
kolumn aldrig lästs av någon avskrift: kolumnen `Wigd` bar en vigseldag som
söktes i sju vigselårgångar, kolumnen `Död.` bar en dödsdag på en rad vars
akt sade att personens senare öde inte var fastställt, en annan `Död.`-kolumn
påstods ligga utanför bilden fast den var synlig och tom, och två tryckta
smalkolumner lästes som ett marginaltal.

Läs rubrikraden i **samma utsnitt** som datacellen. En kolumns innebörd
avgörs av dess position, och positionen kan inte fastställas ur en cell
enbart. `—` i en avskrift betyder saknad uppgift, aldrig en oläst kolumn.

Kravet gäller nya och omarbetade citationer. Befintliga citationer skrivs
inte om retroaktivt; se PCD-2026-09-09-027.

## Tre granskningsresultat

Granskningsutfall dokumenteras per person i kohortens dev-log med datum,
standardversion, granskat underlag, rättelser och kvarstående luckor:

| Resultat | Vad som måste visas |
|---|---|
| Format | Rubriker, tabeller, länkar, datumbruk och fält följer standarden |
| Konsolidering | Akt och profil är sakligt avstämda mot allt befintligt relevant underlag; gamla motsägelser är rättade eller tydligt bevarade som konflikter |
| Kontraktsuppfyllelse | Varje PK-01–12 har individuell beläggsmotivering i profilen, med identitetsnivå och livsbildsnivå var för sig |

Alla tio livsteman bedöms individuellt i genomgången. `EJ RELEVANT` eller
integritetsminimering kräver ett personbundet skäl. En ofullständig
utvinning eller okontrollerad källa får inte kallas styrkt. Granskning av
livsbildens brister medför inte att ny livsbildsforskning startas för en
person som ännu inte passerat identitetsgrinden.

GODKÄND och BÄRANDE följer enbart personkontraktet. Bevara redan tillräcklig
forskning och ange konkret grund vid ändrat omdöme. Uppgiftsavslut kan vara
giltigt med dokumenterade forskningsluckor, men betyder inte att personen
eller north star är färdig.

## Införande och fortsatt användning

T-0113 prövar standarden på ett varierat urval. T-0114 fördelar samtliga
akter till fasta Wotan-kohorter och räknar in pilotens redan utförda arbete.
T-0115 verifierar full täckning och inför maskinellt regressionsskydd.
Under införandet visar formatavvikelser återstående arbete; de får inte
maskeras genom att ändra godkända sakbedömningar.

Efter ett materiellt fynd ska berörda aktuella texter, Q-/KP-frågor,
söknycklar, anhöriguppgifter och bedömningar stämmas av före uppgiftens DONE.
Dokumentera en uttrycklig avgränsning och Wotan-ägare för följdarbete utanför
uppgiften. Maskinkontroller kompletterar denna sakgranskning.

### Pilotpreciseringar 2026-09-07

- Huvudtabellens rader ska vara sammanhängande. En blankrad mitt i tabellen
  bryter CommonMark-tabellen och får inte användas för tids-/batchgruppering.
- PK-10 kan vara styrkt när den aktuella berättelsen är källkritisk och
  korrekt även om materiella livsluckor under PK-03/08 består. Bedöm
  varje krav för sig; brist i ett krav ska inte automatiskt kopieras till alla.
- PK-05-brist namnger den relevanta outvunna kolumnen/fortsättningen.
  Dokumenterat prövad oläslighet är en källgräns, inte automatiskt brist.
- Märk upphävda historiska slutsatser i assertionens saktext, inte bara i
  kommentaren. Ursprunglig observation och rättelsereferens ska bestå.

`node scripts/person-format.mjs P-NNNN ...` kontrollerar en angiven kohort;
`--all` visar hela införandets formatbrister. Kontrollen är read-only och
intygar inte saklig konsolidering eller kontraktsuppfyllelse.
