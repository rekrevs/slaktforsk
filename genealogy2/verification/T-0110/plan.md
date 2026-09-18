# T-0110: fördefinierat originalprov 2026-09-18

Plan fastställd före dragning och före visuell omläsning. Gamla citationer
är frysta jämförelseunderlag; dagens versionerade slutsatser och redan
införda rättelser avgör vad som ännu åberopas. Urvalsenheten är citation,
inte en person eller en enstaka siffra. Ingen förhandsselektion på bildens
åtkomlighet, lättlästhet eller tidigare kända fel görs.

## Urvalsram

Bygg unionen av citationer som via versionsbundna underlag eller uttryckliga
importerade beläggshänvisningar stöder:

1. aktuella sakpåståenden, händelser och relationer för en person med användbar
   BÄRANDE trädverkan i dagens inventering;
2. en accepterad identitetskoppling eller föräldrarelation med endast en
   identifierbar citation i beläggskedjan, även utanför den bärande gruppen;
3. ett negativt sökresultat som ensamt åberopas av en avslutad/avgränsad fråga.

Följ stöd/härledning, inte rena kontext- eller motbevislänkar. Registrera
vilka objekt och revisions-id:n som motiverar varje inkluderad citation.
Ingen parentpropagering härleds genom fritextens släktord. Kandidat-, avvisade
eller avvecklade slutsatser räknas inte som accepterade. Ägaruppgifter utan
arkivaliskt citat är ingen bildläsning och ingår inte i denna population.
Redovisa tydligt ramens täckningsgränser: den är beroende av faktiskt
registrerade beläggskopplingar och kan inte upptäcka helt oregistrerade sådana.

## Dragning och precision

Dra 30 distinkta citationer med enkel slumpmässig dragning utan återläggning
ur den sorterade, sparade ramen. Använd en ny systemgenererad 256-bitars seed,
spara seed före urvalets innehåll öppnas och sortera på SHA-256(seed + citat-id).
Inga omdragningar eller ersättningar av svåra/saknade original tillåts.

Storleken är ett avgränsat första mått, inte certifiering av hela materialet.
Rapportera felandel per granskad citation och ett tvåsidigt 95-procentigt
Wilsonintervall (binomial approximation, utan ändlighetskorrektion). Med 30
observationer är precisionen begränsad; noll fel skulle inte bevisa felfrihet.
Oprövbara original redovisas separat och med intervallet för möjliga felandelar
om samtliga bortfall är korrekta respektive felaktiga. Ingen procentsiffra för
hela projektets bevisriktighet eller north-star-uppfyllelse får härledas.

## Läsning och utfall

Läs citatets aktuellt åberopade text och rättelsekedja, dess källidentitet,
hela det relevanta originalomfånget samt tryckta kolumnrubriker. Visa bilden
för orientering och läs målpost/styrande fält i originalupplösning; använd
utsnitt vid behov. Bevara full relevant utvinning för varje faktiskt öppnad
målpost, inklusive namn, rådatum, relationer, ort, hänvisningar och övriga
relevanta fält. Ett index eller en miniatyr ersätter inte originalet.

Varje citation får: bekräftat, rättat eller ej fullt prövbart, med exakt
läst omfång och motivering. Jämför sida, år, omfång, söknyckel, namn, ort,
siffror och den bärande slutsatsens räckvidd. Räkna en citation högst en gång
som felaktig; notera feltyper separat. En redan korrekt införd historisk
rättelse är inte ett nytt fel. Ren typografi räknas inte; felläsning,
fel lokalisering, missad relevant uppgift eller övertolkning gör det.
Ett fastställt fel kan räknas som fel även om annan del är oprövbar;
redovisa då båda förhållandena. Läsolösta tecken blir inte säkra rättelser.

Resultaten registreras en gång som versionsbundna forskningsbedömningar i
Genealogy2 med T-0110 och kriterium. Nya rättelser bevarar tidigare revision,
prövar alla utlösta beroenden och ändrar inga personstatusar utan belägg.
Wotan länkar operationerna. Saknad bevarad kopia söks på den redan kända
originalvägen; oförmåga att återläsa är bortfall, aldrig ett bekräftat citat.

## Ramkontroll före dragning

Frågeobjektens importerade belägg kan fortfarande vara textreferenser utan
native dependency-rader. Sju avslutade frågor med en enda C-referens vars
citation också innehåller ett negativt sökobjekt sakgranskades därför före
slumpningen. Fyra innehåller ett avgränsat noll som stängt just den passagen:
P-0082/Q-02 (C-1071), P-0344/Q-01 (C-0858), P-0416/Q-01 (C-1031) och
P-0452/Q-01 (C-0854). Tre positiva hushållsfrågor kvalificerar inte på denna
regel. Detta är ramprövning av texter, inte originalomläsning eller ett
urval av kända fel. Byggskriptet bevarar dessa fyra beslut uttryckligen.

Exakta skäl finns i frame.json; populationsstorleken finns i sample.json.
Plan, ram, seed och det enda dragna urvalet bevaras innan bilder öppnas.
Metodreferens: [NIST, Wilsonintervall](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm),
kontrollerad 2026-09-18. Intervallet avser citationers felandel i ramen.
