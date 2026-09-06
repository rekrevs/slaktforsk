# S-0746: Rotemansarkivet, Stockholms stadsarkiv

- Leverantör: Stockholms stadsarkiv,
  <https://sok.stadsarkivet.stockholm.se/Rotemannen2012/Search.aspx>
- Omfattning: **4 312 746 poster** ur roteregistren för Stockholms stad
  **1878–1926**. Rotemännen förde ett löpande register över stadens
  befolkning vid sidan av kyrkobokföringen; varje post motsvarar en person
  under en sammanhängande period i ett hushåll på en adress.
- Källkaraktär: **strukturerad databas, avskrift av original**. Posterna
  återger roteregistrens fält men visar ingen bild. Databasen ska därför
  behandlas som en andrahandskälla med hög tillförlitlighet och namnger
  själv sitt original genom häftesnummer, sida och rad, vilket gör
  originalbladet återsökbart i stadsarkivets serie.
- Fält i den enkla sökningen: `tbBirthday` (fullt datum `ÅÅÅÅ-MM-DD`; ett
  partiellt årtal ger `NoResult`), `tbLastname`, `tbFirstname`,
  `tbBirthplace`, `ddlBirthcounty`, `ddlRote`, `ddlInyear`, `rblSex`.
  Kryssrutorna `cbLastname`, `cbFirstname` och `cbBirthplace` betyder
  **"Exakt fras"** och ska lämnas otippade vid vanlig namnsökning.
- Knappen `btnSearchType` (**Avancerad sökning**) lägger till bland annat
  `tbTitle` (yrke), `tbInplace`/`ddlIncounty`, `tbOutplace`/`ddlOutcounty`,
  `tbStreet`, `tbEstate`, `tbLittera`, `ddlCivilstate`, `tbPostID`,
  `tbLedger`, `tbPage` och `tbRow`. **`tbTitle` matchar hela titeln**, inte
  en delsträng: `Lokeldare` ger träff, `Rör` ger `NoResult`.
- Resultatvyn: `SearchResult.aspx`. Träffraderna öppnas med
  `__doPostBack('gridPeople:_ctlN:_ctl0','')`; menyraden ger
  `menu$lbSamePerson` (**Samma individ**), `menu$lbSameHousehold`,
  `menu$lbSamePage` och `menu$lbSameLedger`. Detaljpanelen har ett eget
  post-id och kan även nås som `SearchResult.aspx?id=<postid>`.
- Träfflistan är alfabetisk och **avkortas vid 200 rader**; en sökning som
  kan ge fler måste därför avgränsas med fler fält innan ett nollresultat
  får tolkas som negativt.
- Åtkomst 2026-09-06: fri, ingen inloggning och ingen captcha. Ingen lokal
  kopia av sidorna sparas; posterna citeras med sitt post-id.
