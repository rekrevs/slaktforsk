# S-0452: Riksarkivet — Degerfors API- och folkräkningsåtkomst 2026-08-29

## Prövade vägar

1. Ett generiskt records-API-anrop på `Johan Peter Zingmark` gav
   `totalHits: 0`. API:et söker arkivbeskrivningar, inte folkräkningens
   personposter; resultatet är därför bara ett routingnoll.
2. Exakt specialfråga i folkräkning 1900 — Johan Peter Zingmark, född 1825 i
   Sävar och hemförsamling Degerfors — nådde Riksarkivets ALTCHA-sida innan
   någon resultatlista visades. ALTCHA lämnades orörd.
3. Sök-API för Degerfors A II a och OAI för A II a/1 stoppades först av ett
   WAF-svar. URL-kodning, `Accept` och vanlig `User-Agent` löste hindret; den
   exakta serien och A II a/3 kunde sedan hämtas i S-0451.

Ingen Chrome användes. Det lösta WAF-hindret får inte återrapporteras som
aktiv spärr. Folkräkningsfrågan är däremot fortfarande ett åtkomsthinder och
varken positivt eller negativt personresultat.

## Återaktivering

1. Pröva först ett person-API för folkräkningar om Riksarkivet publicerar
   ett sådant; det generiska records-API:et är inte rätt sökyta.
2. Använd annars den publika IIIF-volymen `folk!024008` när en källburen sida
   eller ort ger ett avgränsat mål.
3. Använd specialregistrets ALTCHA endast efter uttrycklig ägarbekräftelse,
   eller sök via annan laglig leverantör.
4. För församlingsböcker: fortsätt API → JSON-LD → IIIF med URL-kodade
   parametrar och innehållsförhandling; gå inte till Chrome så länge dessa
   lager fungerar.

Originalen och deras SHA-256 är bundna i C-0575 och mediamanifestet.
