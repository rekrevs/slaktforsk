# Avgränsad källrevision och konsolidering – försöksprotokoll v1

Använd med ett Wotanmandat, fixerad äldre databas, källpost, personurval och acceptanskriterier. Protokollet gäller olika personer och källklasser. Det anger arbetskrav, inga förväntade läsningar eller rättelser. I detta försök används endast gpt-6.1-sol; projektets ordinarie modellregel ändras inte.

## 1. Läs en källpost

Fastställ sidans rubriker, målpostens gränser, datum-/dittoankare och administrativa grupper. Läs hela relevanta målposten. Spara råvärde och status för varje eget logiskt fält: läst, tomt, osäkert eller oläst. Dokumentera strykningar, kantspår och marginaltecken, även utan säker innebörd. Blankbeskrivning får inte dölja otydliga tecken. Återge datum och namn diplomatiskt före normalisering. Skilj tryckt rubrik, egen cell och överförd uppgift. Kön kräver uttryckligt stöd, inte namn eller roll.

Arbeta med en post i taget och bildderivat vid behov. Dela stort hushåll i rader för läsning, men bevara hela hushållsgränsen. Angränsande person används bara där den behövs som kontext. Lås första egna avläsningen före andra läsarens svar. Två avläsningar av samma källa är kvalitetskontroll, inte två historiska vittnen.

## 2. Kartlägg berörd befintlig kunskap

Läs aktuell äldre personvy, forskningsobjekt och källunderlag. Inventera både versionsbundna beroenden och textkopior i fakta, berättelser, frågor, kontraktsbedömningar och källvägar. Sök med de namn-, orts-, tids- och begreppsnycklar som den egna läsningen motiverar. En träff är en kandidat, inte stöd eller fel. Avgränsa bred sökning med person/tid/plats; dölj inte relevanta resultat bakom en godtycklig träffgräns.

Befintliga relevanta påståenden om andra källor ingår när de påverkar dessa personers berörda kunskapsläge. Samma post kan motivera flera personbedömningar; ingen ny generation eller obegränsad livsforskning följer. Redovisa varför en kandidat sakligt hör utanför omfånget. Ett aktuellt berört påstående kan inte lämnas utanför bara därför att det finns i en lång profil eller skapades tidigare.

## 3. Granska små påståendepaket

Högst sex aktuella påståenden åt gången. Ett långt objekt delas i sammanhängande segment med exakta teckenpositioner; alla relevanta segment ska läsas. Verktygstrunkering betyder oläst och måste åtgärdas. Ett paket är underlag, inte en parallell utförandekö; Wotan håller återupptagningsläget.

För varje påstående returnera:

- objekt-id/version, textfält/teckenposition och exakt aktuellt citat;
- relevanta äldre underlag med objekt/version och vad de faktiskt stöder;
- den egna källobservationen eller redan kända uppgiften som kan påverka påståendet;
- individuell bedömning: stärkt, kvalificerat, motsagt, oförändrat, orelaterat eller olöst;
- beslut: behåll, revidera, kvalificera eller lämna sakfrågan uttryckligen öppen;
- konkret skäl kopplat till det citerade påståendet; vid ändring exakt före/efter och målobjekt;
- berörda kopior, datum-/precisionsgränser och kvarstående fråga.

Att behålla är ett positivt sakbeslut, inte standardval. En gemensam förklaring per objekttyp eller källa ersätter inte påståendeprövning. Ett oförändrat sakutfall kan ändå kräva ändrad formulering om precision, underlag eller vad som nu är prövat. Kännedom om en uppgift och utvinning av ett nytt fynd är olika saker; befintlig tillräcklig forskning ska användas. En svagare omläsning upphäver inte automatiskt tidigare starkare belägg.

## 4. Konsolidera innan införsel

Samla resultaten per person och källa. Kontrollera att nya förbehåll, rättelser och relevanta redan kända uppgifter får genomslag i alla faktiskt berörda aktuella påståenden. En ny observation eller granskningsanteckning uppdaterar inte automatiskt gamla fakta eller prosekopior. Kontrollera även formuleringar om oprövad, genomgången, blank, fullständig och uttömd; skilj utförd prövning från en fortfarande olöst innebörd.

Bevara historik, konkurrerande identiteter, OWNER_CONFIRMED, källberoenden och skillnaden mellan identitetsnivå/livsbild. Inga osäkra personer eller relationer förs in i verifierad antavla. Varje berörd person får nativeprofil eller uttrycklig avgränsad adoption, utan falskt fullkontraktsgodkännande.

## 5. Oberoende kontroll och avgränsad implementation

Kontrolläs avgörande och osäkra fält. Granska alla materiella ändringsbeslut och behållandebeslut med risk för dold precisions-/källgräns. Granskaren läser konkreta citat och belägg, inte bara implementerarens sammanfattning. Alla motiverade anmärkningar får eget svar före paketlås; olösta sakfrågor består synligt.

Skapa fullständiga versionsbundna operationer efter besluten. Före/efter, disposition, evidensstatus, ursprung, exakta stöd och metadata ingår. Inaktuellt stöd granskas individuellt mot gammal/aktuell version före eventuell ombindning. Lös bara faktiskt existerande omprövnings-id efter sakprövning. Prova genom kontrollerad apply och faktisk fullobjektsjämförelse. I försöket: endast separat databas och journal, aldrig huvudmodellen.

## 6. Slutgranska kunskapsresultatet

Kontrollera: hela källomfånget utvunnet; inga sakligt relevanta olästa segment; varje relevant påstående har individuellt beslut; alla beslutade kopior faktiskt uppdaterade; kvarstående osäkerhet är rätt uttryckt; nya och äldre formuleringar motsäger inte varandra genom utebliven konsolidering. Kontrollera särskilt behållanden. Inga generiska beslut godtas som täckningsbevis.

Validatorer, noll väntande omprövningar och antal objekt bevisar teknisk giltighet, inte fullföljd sakbedömning. Redovisa olösta frågor och arbetsluckor separat. Frys kandidat och beslut före referensjämförelse. Resultatet får kallas fullföljt inom omfånget först när dessa krav är styrkta; ett färdigt jämförelseförsök kan redovisa en underkänd kandidat.
