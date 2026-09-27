# Opus 5.5 i slaktforsks modelltest – T-0772

Genomfört 2026-09-27: **30 försök** med Claude Opus 5.5 (`claude-opus-5-5`)
på exakt samma frysta X/Y/Z-paket och wrapper som [T-0769](../T-0769/report.md),
fem nya sessioner per uppgift och resonemangsnivå: `medium` (som T-0769) och
`xhigh` (som ägarens interaktiva körning). Inga omförsök, tips eller
rättningsrundor. Blind sakbedömning av separata Astra-kontexter
(`gpt-6-astra`/`medium`, samma som T-0769) med 11 inblandade T-0769-svar som
kalibrering: **11/11 fick samma utfall och samma poäng som i T-0769.**

## Resultat i korthet

| Uppgift | Astra | Sol | Terra | Luna | Opus 5.5 medium | Opus 5.5 xhigh |
|---|---:|---:|---:|---:|---:|---:|
| X: originalutvinning | 5/5 | 0/5 | 0/5 | 0/5 | **0/5** | **0/5** |
| Y: följdprövning | 5/5 | 0/5 | 0/5 | 0/5 | **0/5** | **0/5** |
| Z: ändringspaket, strikt | 5/5 | 5/5 | 0/5 | 3/5 | **5/5** | **5/5** |

Genomsnittlig poäng: X 100/88/78/81 % för OpenAI-modellerna mot 92 % (medium)
och 96 % (xhigh) för Opus; Y 100/94/93/94 % mot 94 %/94 %; Z 100 % för Opus.
På de strikta helhetsgrindarna har Opus 5.5 samma profil som Sol. Felen är
dock mycket enhetliga och skiljer sig kvalitativt från OpenAI-modellernas.

**X – ett enda, systematiskt fel.** Alla tio Opus-svar har rätt innehåll i
24 av 25 celler, inklusive radplaceringen av husförhörstalen: 16 i r10 och
r11, tomma r9 och r12, 12,14 i r8. Det var radförskjutning som fällde alla
15 underkända Sol/Terra/Luna-svar i T-0769, och den förekommer inte hos
Opus. Samtliga tio läser däremot B r9:s födelsedag som `1901 5/3` med
`read` och utan alternativ. Den frysta rubriken föredrar 31/3 och godtar
5/3 bara med uttrycklig reservation. Projektets eget underlag säger att 31
föredras men att 5 inte kan uteslutas, och det äldre indexet har
1901-03-05. En säker läsning utan reservation är därför ett kritiskt fel,
oavsett vilken siffra som till sist är rätt. Fyra svar noterade ett extra
drag eller en punkt vid siffrorna utan att reservera läsningen. Felet är
identiskt i 10/10 och påverkas inte av xhigh. xhigh gav något högre poäng
(72 mot 69–70) därför att medium oftare markerade osäker radtillhörighet
för tal som tydligt står i egen rad.

**Y – samma F5-mönster som Sol och Luna.** Alla tio Opus-svar har rätt i
15 av 16 objekt, alla nio requests exakta, 1901-03-05 bevarat under konflikt
och tom `canonical_changes`. Alla tio tappar den befintliga uppgiften att
familjen bodde i Östra Husby när dödsortsslutsatsen rättas, flera med
uttrycklig motivering att boendet saknar stöd när G1 inte belägger det.
Det är en evidensminimalistisk hållning som strider mot projektets
bevarandeprincip i huvudbedömningen. Utan F5-kravet klarar Opus 10/10.

**Z – felfritt.** 10/10 paket gick igenom verklig införsel med 15/15 och
individuella resolve-skäl, utan titelpunkt eller fel objekt.

## Känslighetsanalyser

| Alternativ avgränsning | Astra | Sol | Terra | Luna | Opus medium | Opus xhigh |
|---|---:|---:|---:|---:|---:|---:|
| Y utan enbart F5:s bevarandekrav | 5/5 | 5/5 | 3/5 | 5/5 | 5/5 | 5/5 |
| Z om enbart titelns slutpunkt tolereras | 5/5 | 5/5 | 5/5 | 3/5 | 5/5 | 5/5 |
| X om säker 5/3 bara ger cellavdrag (post hoc) | 5/5 | 0/5 | 0/5 | 0/5 | 5/5 | 5/5 |

Y- och Z-analyserna är T-0769:s förhandslåsta fält. X-raden är **post hoc**:
den definierades efter att det blinda mönstret syntes och ska inte läsas som
ett likvärdigt resultat. Den visar bara att hela Opus X-utfallet hänger på en
enda omstridd siffra, medan T-0769:s underkännanden alla hade radfel och
därför inte ändras. Nyckeln 31/3 är AI-härledd och inte mänskligt
certifierad; ägarens egen blick på B r9:s födelsecell skulle avgöra vilken
läsning som är rätt, men inte om reservationen behövdes.

Fyra X-försök (medium 2, 3, 4 och xhigh 5) skrev egna bildutsnitt i `/tmp`
i stället för RUN_DIR; T-0769 hade två sådana. Ingen läsning av repo,
instruktioner, facit, andra försök eller loggar observerades. Utan dessa
fyra: X 0/2 (medium) och 0/4 (xhigh), Y 0/5 och 0/5, Z 5/5 och 5/5.

## Tid och kostnad

Kostnad är **beräknad standard-API-kostnad**, inte faktisk
abonnemangsdebitering: Anthropic listpris för Opus 5.5, $4 per miljon
input, $20 output, $0,20 cacheläsning och $8 1h-cacheskrivning. Beräkningen
reproducerar Claude Codes egen listkostnad exakt. OpenAI-siffrorna är
T-0769:s oförändrade proxy.

| Uppgift | Astra s / $ | Sol s / $ | Opus medium s / $ | Opus xhigh s / $ |
|---|---:|---:|---:|---:|
| X | 108 / 0,606 | 124 / 0,395 | 45 / 0,399 | 150 / 0,805 |
| Y | 80 / 0,292 | 87 / 0,174 | 45 / 0,292 | 84 / 0,429 |
| Z | 38 / 0,207 | 55 / 0,137 | 18 / 0,210 | 22 / 0,251 |

Tider är medianer och kostnader medelvärden per försök. Opus medium var 1,8–2,4
gånger snabbare än Astra i alla tre uppgifterna. xhigh ökade tid och kostnad
(X 3,3× tid och 2× kostnad) utan att ändra något godkännande.

50–77 % av Opus-proxyn är 1h-cacheskrivning av 20 000–59 000 tokens per ny
session: Claude Codes systeminstruktion, CLAUDE.md, verktygs- och
skillförteckningar samt bilderna. OpenAI-proxyn har ingen skrivpremie.
Prissatt som vanlig input blir Opus-medelkostnaden X 0,265/0,602, Y
0,203/0,321 och Z 0,128/0,159 (medium/xhigh). Den fasta startkostnaden per
fristående session är alltså betydande för små uppdrag.

De 30 försöken kostade cirka $11,93 enligt proxyn. De tre Astra-granskarna
kostade cirka $3,82. Rootsessionens planering, pilot, orkestrering och
kontroll kostade $7,61 fram till uttaget; rapportarbetet tillkommer.

## Vad detta betyder för arbetsfördelningen

- **Källtolkning (X):** Opus 5.5 ersätter inte Astra i detta prov. Felet är
  dock ett annat än de billigare OpenAI-modellernas: Opus håller rad- och
  kolumngränser och läser tydlig text rätt, men markerar inte osäkerhet i
  en genuint tvetydig siffra. Om Opus används för utvinning bör uppdraget
  kräva uttryckliga alternativ för dag/månad och svaga siffror, följt av en
  riktad andra läsning. Högre effort löste inte detta.
- **Följdprövning (Y):** samma helhetsutfall som Sol och Luna. Slutlig
  bedömning av hur en rättelse påverkar befintlig kunskap bör fortsatt ligga
  hos Astra, med samma förbehåll som i T-0769: Y vilar på ett enda fall.
- **Fastställda ändringspaket (Z):** Opus är lika säker som Astra och Sol,
  och snabbast. Beräknad kostnad per fristående session ligger i nivå med
  Astra och över Sol. Där Claude Code redan är orkestrerare är Opus
  `medium` en rimlig utförare med automatisk införselkontroll.
- **Resonemangsnivå:** `medium` räckte för allt som Opus klarade. `xhigh`
  gav inga fler godkända svar i dessa moment.

Detta är rekommendationer för uppmätta moment. AGENTS.md:s modellregel och
agentkonfigurationer är oförändrade; en ändring kräver ägarbeslut.

## Vad slutsatserna håller för

Fem upprepningar av samma lilla material mäter körstabilitet, inte fem
oberoende genealogiska fall. 5/5 är ingen felfrihetsgaranti (95 %
Wilsonintervall ungefär 57–100 %) och 0/5 bevisar inte att modellen aldrig
klarar momentet. Opus kördes genom Claude Code och OpenAI-modellerna genom
Codex; verktygsskal, systeminstruktion och cacheprissättning ingår i det som
mäts. Nätverk, MCP och subagenter var tekniskt avstängda för Opus men bara
förbjudna i T-0769, vilket inte påverkade uppgifter som inte behöver dem.

Granskarna tillhör konkurrerande modellfamilj. Kalibreringen visar att de
återger T-0769:s bedömningar exakt, inte att de saknar bias. De avgörande
Opus-felen är dock regelstyrda: säker 5/3 utan reservation och borttappad
bostadsuppgift. De är kontrollerade i råsvaren. Rooten är samma modell som
prövas och gjorde bara formell kontroll ([ROOT-REVIEW](ROOT-REVIEW.md)).
X-granskarens egna förstoringar misslyckades eftersom PIL saknades, så
bildbedömningen byggde på hel- och detaljbilderna; ankarsvaren fick ändå
identiska cellpoäng. Effort ekas inte av API:et och är verifierad genom
kommandoraden.

En annan session arbetade samtidigt med T-0677 i genealogy2. Skyddet av
forskningsdata är därför verifierat genom verktygsloggarna och inte genom
en kontrollsumma över hela databasen: filverktygen var begränsade till
RUN_DIR, och inga Bash-skrivningar skedde utanför RUN_DIR förutom de
redovisade `/tmp`-utsnitten, som har tagits bort.

## Tillägg: ägarens bedömning av B r9 (efter låsning)

Ägaren bedömde 2026-09-27, efter rapporten, att cellen troligen lyder 5/3
men är så svårläst att ett korrekt svar ska kommentera att den är tvetydig.
Det är en bedömning, inte en OWNER_CONFIRMED-uppgift. Den stämmer med
kunskapsmodellens registrerade 1901-03-05 för P-0035 och C-0907:s 5/3; där
står T-0675:s reserverade 31/3[5/3?] redan kvar som öppen konflikt.

Ingen av de 30 X-svaren i de två studierna markerade tvetydigheten. Alla
fem Astra-svar läste säker `1901 31/3`, och Opus-svaren läste lika säkert
`1901 5/3`. Den frysta nyckeln för cellen byggdes i T-0769 av en
Astra-kontext och föredrog 31/3. Med ägarens standard skiljer den inte
längre mellan modellerna ([omräkning](owner-ambiguity-rescore.json),
[skript](rescore_owner_ambiguity.py); låsta betyg är oförändrade):

| X-avgränsning | Astra | Sol | Terra | Luna | Opus medium | Opus xhigh |
|---|---:|---:|---:|---:|---:|---:|
| Fryst nyckel (huvudresultat) | 5/5 | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 |
| Båda läsningarna godtas, saknad tvetydighetskommentar kostar statuspoäng | 5/5 | 0/5 | 0/5 | 0/5 | 5/5 | 5/5 |
| Säker läsning utan tvetydighetskommentar är kritiskt fel | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 |

Det som faktiskt skiljer modellerna i X är radplaceringen. Astra och Opus
placerade alla husförhörstal rätt, medan alla 15 Sol/Terra/Luna-svar hade
radfel. I övrigt är Astra och Opus likvärdiga i X. Ingen av dem klarar den
kalibrering ägaren efterfrågar, och varken Astra eller Opus xhigh bör
ensamma lita på en säker läsning av en svårläst siffra. T-0769:s slutsats
att Astra var ensam om att klara bildpaketet vilar för denna cell på en
nyckel som Astra själv satt. Modellregeln i AGENTS.md hänvisar till T-0769
och är inte ändrad; en omprövning är ägarens beslut.

## Ägarbeslut och diskuterad tillämpning

Ägarbeslut 2026-09-27: **ingen policyändring.** AGENTS.md:s modellregel
består; resultaten bevaras här för att kunna återbesökas vid behov. Ägaren
bekräftade också att projektet ännu inte har andra fakta om Ludvigs
födelsedag än arkivdokumenten, så konflikten i P-0035 förblir öppen.

Diskuterat men inte antaget, som underlag vid ett senare återbesök:

- Y-typ, alltså följder av rättelser, revise/retain och ersättningstexter:
  bara Astra, även utan Opus-utkast. Opus tolkade ”ingen ny uppgift” som
  ”inget stöd” och tog bort opåverkad befintlig kunskap i 10/10 försök.
- X-typ, alltså svåra originalceller som matar kanoniska datum och namn:
  oberoende läsning av Astra och Opus. Oenighet registreras som
  tvetydighet eller konflikt och avgörs inte av någon modell. Upprepning med
  samma modell gav ingen andra åsikt (Astra 5/5 säker 31/3, Opus 10/10
  säker 5/3), men två modellfamiljer tillsammans hade fångat cellen.
- Z-typ, alltså fastställda ändringspaket med automatisk kontroll: Opus
  `medium` kunde ta Sols roll i Claude Code; Sol är billigare i Codex.
- Framtida modellprov: nycklar för svåra celler ska inte komma från en enda
  modellfamilj, och Y behöver fler fall än F5 innan Opus prövas för sådant
  arbete.

## Bevarande och verifiering

Allt finns bevarat: [protokoll](PROTOCOL.md), körordning, 30 råsvar,
råströmmar i `logs/`, telemetry per försök, blindkopior, automatiska och
blinda betyg med granskarrapporter (`scores/judge-report-*.md`),
[låsning](grade-lock.json), [resultat](results.csv),
[sammanställning och kalibrering](summary.json),
[paketgranskning](protocol-review.json) och [audit](audit.json).
`verify_benchmark.py` godkänd: T-0769:s 24 och T-0772:s 134 frysta filer
oförändrade, 30/30 försök kompletta med rätt modell och effort, 41
byte-identiska blindkopior och betyg oförändrade sedan låsning. T-0769:s
automatiska kontroller gav identiskt resultat för alla 11 ankare på dagens
kod, inklusive verklig Z-införsel.

Lokalt commit på main efter ägarens persistensbesked; ingen push, ingen
dashboarduppdatering, ingen live-apply och
ingen ändring av T-0769 eller forskningsdata.
