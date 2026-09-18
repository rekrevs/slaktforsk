# T-0673 A-operation: oberoende förhandsgranskning

Read-only granskning av `T-0673/a-pilot-v1`: 53 ändringar, 62 individuella
resolutions och två nya medier. Ingen apply utförd; datum-/bildläsningens
sakbedömning är redan rootgranskad och upprepas inte här.

## Exakta kontroller

- Alla expectedVersion matchar aktuella objekt.
- Policy 2 är explicit. Dess rekursiva beroendeurval reproducerades med
  read-only SQL för varje tidigare revision; objekt som får ny revision i
  samma operation undantogs. Hashen `op:affected:after` gav exakt **62**
  requests, identiska med operationens lista, utan saknade eller extra id.
- Alla fyra reviderade postobjekts gamla importerade assetlänkar är bevarade.
- Den först upptäckta bristen med tom evidence på nya sakliga rättelsenoter
  rapporterades. Root har därefter lagt till avgränsade supports till rätt
  postversion 2 på de 16 tidigare olänkade objekten, inklusive händelser och
  source_assessment-fakta. Den bristen är därmed åtgärdad i förslaget.

## Kvar att justera före apply

Generisk P02-not ersätter hela body i flera objekt, och tappar därmed sakligt
relevant aktuell information trots att gammal revision finns i historiken:

1. `CONTRACT-P-0414-PK-05`: behåll den befintliga avgränsade bedömningen av
   fyra posters utvinning. Byt den felaktiga uppgiften om olästa vigselfält
   mot nu läst omfång/reservationer; pilotnoten ersätter inte hela PK-05.
2. `THEME-P-0414-SAM`: behåll Q-01/KP-01/C-0600-kopplingar och aktuell
   avgränsning av livshändelsen; ersätt endast oläst-premissen och tillför
   pilotresultatets reservationer.
3. `KEY-P-0414-f4ca37315156`: behåll nyckeln vigsel1874-12-12, Skön E I/2,
   Rökland och C-0600. En generell brudgumsårs-/kolumnnot är inte ensam en
   användbar söknyckel. Föräldrakolumnförväntan ska förstås tas bort/rättas.
4. `PATH-P-0414-KP-01`: bevara namnnycklarna Anna Lovisa Andersdotter och
   Johan August Fredberg, hänvisningen C-0600 och leverantör/åtkomst för den
   exakt redan lästa posten. Nya textens återaktiveringsgräns och T-0616 som
   utförandeägare är bra och ska kvarstå.

`P-0414/Q-01` behåller huvudfråga, födelsetid/Fågelvik, osäkert ursprung och
alternativen rätt socken/fel ortnamn. Ingen motsvarande blockerande sakförlust
identifierades där. Gamla generella påståendet att vigselböcker normalt
namnger brudens far ska inte återinföras som aktuell säker väg.

Efter dessa fyra lokala bodyjusteringar behöver versions- och request-id-listan
normalt inte ändras, eftersom samma objekt/evidensversioner revideras. Root bör
ändå köra sitt avsedda scratchprov innan huvuddatabasens apply. Den här
kontrollen bevisar formatförutsättningar och bevarat omfång, inte att varje
osäker historisk bokstav är rätt avläst.

## Slutlig disposition 2026-09-18

De fyra bodyförlusterna rättades före apply: tidigare relevanta avgränsningar, C/Q/KP-hänvisningar och namnnycklar bevarades tillsammans med den nya avläsningen. De16 noter som behövde belägg är länkade. T-0673/a-pilot-v1 är applicerad med53 revisioner, två medier och62 individuella resolutions. Slutliga verify/verify-assets/verify-source passerar.
