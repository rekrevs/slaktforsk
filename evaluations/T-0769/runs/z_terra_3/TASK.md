# Z — Bygg ett versionsbundet ändringspaket

Du får ett syntetiskt, fryst genealogy2-underlag i `input.json`. Skapa `answer.json` med **en** JSON-operation som genomför det fastställda sakbeslutet. Läs bara denna instruktion och input.json; sök inte i repositoryt, privata bedömningsfiler eller andra körningars svar. Använd gärna lokal kod för att forma JSON. Kör inte apply och ändra inga projektdata. Inga nya källundersökningar eller sakbeslut behövs.

## Format och regler

`input.currentChanges` visar varje aktuellt objekt i skrivformat. `expectedVersion` anger objektets nuvarande version. Kopiera hela objektet för en ändring, behåll fälten som inte omfattas av beslutet och ändra motiveringen. En ändring skapar nästa version. Omodifierade objekt ska inte tas med. `changes` måste vara i beroendeordning, så att en rättad källpost kommer före observationen och observationen före slutsatsen.

Operationens format:

```json
{
  "id": "T-0769-Z-answer",
  "actor": "benchmark",
  "reason": "T-0769: konkret sammanfattning av beslutet",
  "dependencyReviewVersion": 2,
  "media": [],
  "changes": [],
  "resolve": []
}
```

Varje ändring använder fälten `id`, `kind`, `expectedVersion`, `disposition`, `rationale`, `data` samt befintliga `origins`, `evidence`, `media`, `evidenceStatus` och `caveat` där sådana finns. Motiveringar får vara korta men ska vara meningsfulla. Bevara dispositioner, befintliga ursprung, medielänkar, evidensroller, förbehåll och övriga sakfält.

Ett versionsbundet underlag har formatet `{"object":"R-exempel","version":2,"role":"supports"}`. När underlaget ändras i operationen måste beroende ändringar peka på dess **nya** version. Versionsnumret avser underlagets version, inte det ändrade objektets egen version. Observationens `data.record_id` ändras inte. Inga extra `bindings` behövs när rätt referens finns i `evidence`.

`input.newMedia` är ett redan förberett registreringsobjekt. Lägg det oförändrat i operationens översta `media`-lista. Källpostens egen `media` innehåller däremot bara länkar av formen `{"id":"MED-exempel","region":"helbild"}`. Båda nivåerna behövs för ett nytt medium. Befintligt medium ska behålla sin länk och region men inte registreras på nytt överst.

`input.pendingReviews` innehåller de två väntande individuella prövningarna. Varje prövning stängs med `{"request":"exakt id från input","rationale":"sakskäl för just detta berörda objekt"}` i `resolve`. En ny objektrevision stänger inte automatiskt en prövning. Eftersom alla ändrade beroenden uppdateras i samma operation utlöses inga ytterligare prövningar i detta avgränsade material.

## Fastställt beslut

Genomför båda fallen i `input.decision`: en enkel titelrättelse och en källposts-/datumrättelse med nya medier och följder. Totalt ska fyra befintliga objekt ändras: S-A, R-B, O-B, F-B. Personkärnan P-A, S-B och F-OWNER ska förbli exakt oförändrade. Inga objekt ska skapas eller tas bort. Bedömningen kontrollerar schema, faktisk införsel i en engångsdatabas, sakvärden, versioner, bevarande och individuell stängning. Svaret ska vara ren JSON i `answer.json`.
