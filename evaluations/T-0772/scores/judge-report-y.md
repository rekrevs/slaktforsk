# Blind sakgranskning Y – T-0772

Detta är AI-granskning, inte mänskligt certifierat facit. Ingen modellidentitet har efterforskats. Inga nätverk eller subagenter användes.

## Lästa underlag

- `evaluations/T-0769/y/public/TASK.md`
- `evaluations/T-0769/y/public/input.json`
- `evaluations/T-0769/y/rubric.private.json`
- `evaluations/T-0772/judge/STANDARD-Y.md`
- Hela svaren i `evaluations/T-0772/blind/y/` och motsvarande hela `evaluations/T-0772/scores/Cnnn.auto.json` för följande 14 ID: C001, C005, C007, C008, C009, C018, C022, C023, C028, C031, C033, C036, C037, C040.

Inga andra källfiler lästes. Endast arbetskatalogens out/ har använts för utdata. Varje svar bedömdes i sin helhet, inklusive samtliga motiveringar, ersättningstexter, evidence, resolve, followups och canonical_changes. Automatiken behandlades som förkontroll, inte facit.

## Resultat och gemensamma mönster

Alla svar har 16 objekt och exakt rätt nio requestkopplingar samt null för övriga sju. Alla rättar Ebbas utflyttning och söknyckel till 23 oktober, bevarar historik och OWNER_CONFIRMED, skiljer Ludvig från Ebba, tar bort oberoenderäkningen av I2 och begränsar hälsoobservationen. Identitetsgrinden bevaras utan nytt livsbildsgodkännande. Evidenslistorna är relevanta; tomma listor för opåverkade objekt är tillåtna.

Två svar, C033 och C037, godkänns med 16/16. Elva svar får 15/16 på grund av förlorad bostadsuppgift i F5. C028 får 14/16 eftersom även P2 saknar tydligt bevarande av det befintliga kanoniska datumet. Totalt 211 av 224 objektbeslut godtas. Utan F5:s bevarandekrav klarar 13 av 14 svar grinden.

## Gränsfall

Alla svar använder revise för P2. Det är inte i sig fel: tretton behåller uttryckligen 1901-03-05 som kanoniskt värde under konflikt och lämnar egen födelsepost oläst. Automatikens P2.action-flagga åsidosätts sakligt för dessa. C028 anger i stället att det kanoniska datumet är under konflikt och räknar upp alternativen. Även dess persons-post säger bara att 31 föredras och 5 inte kan uteslutas. Det räcker inte för standardens krav på uttryckligt bibehållet 1901-03-05. C028 får därför både automatisk schemaavvikelse och underkänt kanoniskt skydd, utan att en ny person eller ett säkert 31-marsdatum påstås ha skapats.

F5:s korrigering av dödsort räcker inte när hela bostadsuppgiften försvinner. Formuleringar om vad G1 inte belägger och nya förslag att söka familjens boende återställer inte det gamla opåverkade faktumet. C033 och C037 har däremot kvar den uttryckliga meningen att familjen bodde i Östra Husby. Alla svar klarar den separata delen att hemort inte fastställer fysisk dödsort.

C018:s korta F3 godtas: dess ersättning tar bort både dubbelräkningen och det säkra datumanspråket. O1 behöver inte nämna betyg 20 uttryckligen när det korrekta datumet anges utan sammanblandning. C018:s O2 läses i sin helhet med den omedelbara reservationen för dag 5. Q1:s motkontroll i C008 och C040 återöppnar inte den besvarade dagsfrågan inom R1.

C031:s ord folkbokföring i F5:s motivering är en överprecis tolkning av hemort, inte ett rapporterat nytt arkivfynd; ersättningstexten stannar vid hemort. Den noteras men ger inte en ytterligare fristående underkännandegrund i känslighetsprövningen. Födelseböcker, församlingar och dödböcker i följdstegen läses som föreslagna sökvägar, inte som redan öppnade eller säkert framgångsrika fynd. Hälsotäckning och uttryck som ett enda primärt belägg läses inom det givna mikrofalets underlag.

Poängen räknar enbart godtagbara objektbeslut. Requests och kanoniskt skydd är separata grindar. En rent annoterande persons-post med uttryckligt bevarat värde skulle enligt standarden inte ensam underkänna sakgrinden; något sådant godtagbart icke-tomt fall finns inte här. Känslighetsprövningen undantar endast F5:s bostadsbevarande och behåller övriga krav.

| Cnnn | poäng/16 | godkänd | utan F5-krav |
|---|---:|:---:|:---:|
| C001 | 15/16 | nej | ja |
| C005 | 15/16 | nej | ja |
| C007 | 15/16 | nej | ja |
| C008 | 15/16 | nej | ja |
| C009 | 15/16 | nej | ja |
| C018 | 15/16 | nej | ja |
| C022 | 15/16 | nej | ja |
| C023 | 15/16 | nej | ja |
| C028 | 14/16 | nej | nej |
| C031 | 15/16 | nej | ja |
| C033 | 16/16 | ja | ja |
| C036 | 15/16 | nej | ja |
| C037 | 16/16 | ja | ja |
| C040 | 15/16 | nej | ja |

## Slutkontroll

Utfilerna kontrolleras programmatiskt mot alla 14 tillåtna svars-ID: giltig JSON, exakt 16 unika objekt per fil, sammanlagt 224 poster, poäng lika med antal godtagna objekt, korrekta requestkopplingar, automatiska avvikelselistor samt konsekvent huvudgrind och känslighetsgrind.
