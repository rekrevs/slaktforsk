# X – Avgränsad källäsning

Läs de medföljande originalbilderna. Uppgiften är råutvinning ur två bestämda
utsnitt, inte identitetsprövning eller ändring av släktdatabasen. Använd endast
filerna i detta paket. Öppna bilderna med bildverktyg; gissa inte från filnamn.
Fullbilderna ger rad- och kolumnkontext, detaljbilderna är oförändrade utsnitt.
Du får göra egna lokala förstoringar/utsnitt om det hjälper.

Fall A: `A-full.jpg`, folio 658, tryckta rader 2 och 3. `A-detail.jpg` visar
vänstersidan med kolumnrubriker. Utvinn exakt fem fält per rad:
- `name`: hela egna namn-/familjeställningstexten, kolumn 1.
- `occupation`: egen yrkestext, kolumn 2.
- `birth`: år samt dag/månad, kolumner 3–4 tillsammans.
- `birthplace`: egen födelseortscell, kolumn 5.
- `marriage`: egen giftcell, kolumn 7.

Fall B: `B-full.jpg`, folio 1064, tryckta rader 8, 9, 10, 11 och 12.
`B-left-detail.jpg` och `B-right-detail.jpg` visar berörda celler.
Utvinn exakt tre fält per rad:
- `name`: hela egna namn-/familjeställningstexten, kolumn 1.
- `birth`: år samt dag/månad, kolumner 3–4 tillsammans.
- `husforhor`: egen cell för bevistat husförhör, kolumn 13.

Bevara förkortningar och källans årtal; fyll inte ut sekler eller efternamn.
Skilj tomma celler från ditto och oläslighet. Kopiera inte in innehåll från en
annan rad eller en förmodad familjeuppgift. Notera överstrykningar och verklig
osäkerhet. Du får ange alternativa läsningar men ska inte lista godtyckliga
alternativ för tydlig text. Alla efterfrågade celler ska vara visuellt prövade.
Andra synliga kolumner/personer är utanför uppgiften.

Leverera ett enda JSON-objekt (ingen Markdown runt JSON), med exakt 25 element
under `fields`. Varje element har:

    {"id":"A.r2.name","raw":"...","state":"read","alternatives":[],"note":""}

ID-format: A.r2.name, A.r2.occupation, A.r2.birth, A.r2.birthplace,
A.r2.marriage; samma fem för A.r3. Därefter B.r8.name, B.r8.birth,
B.r8.husforhor; samma tre för B.r9, B.r10, B.r11, B.r12.

`state` är exakt `read`, `blank` eller `uncertain`. För `blank` är `raw` tom
sträng och `alternatives` tom lista. För `uncertain` återger `raw` den bästa
läsningen (eller `[oläsligt]`) och `alternatives` innehåller eventuella
konkreta alternativ. `note` anger kort vad som är osäkert eller överstruket.
Gör inga påståenden om personernas verkliga födelsedatum, död eller släktskap
utöver avskriften av dessa celler. Skriv inte i projektets kunskapsmodell.
