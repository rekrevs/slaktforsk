# S-0457: Riksarkivet — register-API och åtkomst, Flen/Björkvik 2026-08-29

## Prövade API-vägar

- Riksarkivets OpenAPI-schema anger parametrarna `grooms_name` och
  `brides_name` för vigselregistret. En exakt Erik Karlsson–Matilda
  Charlotta Sjöberg-fråga för 1895 gav noll träffar.
- Födelseregistret gav noll för Matilda Charlotta/Matilda i Björkvik 1860.
  Registertäckningen omfattar inte Södermanlands födelseböcker, så detta är
  ett täckningsnoll och inte ett personnoll.
- Det generiska sök-API:et identifierade Björkvik C/7 och A I/17 a–b som
  digitaliserade men utelämnade bildlänkarna. Exakta JSON-LD-omprov för alla
  tre poster gav `403` den 2026-08-29 och deras svarskroppar bevaras; ingen
  bild-URI kan därför beläggas därifrån.
- Två endast sekvensmässigt härledda kandidatmanifest för A I/17 a–b gav
  `403`; de används inte som säkra reproduktions-id:n.
- Flens A I/25 identifierades exakt i API/JSON-LD/OAI. JSON-LD:s bildrepresentation
  finns men utan URI; en direkt kataloghämtning nådde CAPTCHA före
  innehåll. CAPTCHA lämnades orörd.

## Resultat och återaktivering

Register-API:ets noll fick inte avsluta sökningen. SCB:s årsutdrag löste både
Matildas födelsefamilj och vigseln genom S-0453–S-0454. Björkvik C/9 och Flen
A I/26 var samtidigt publika via API/IIIF och gav C-0579–C-0580.

En ny fullständig fondinventering i S-0535 visar att Flens E I/1 slutar
1861 och E I/2 börjar 1905; någon katalogiserad E I-volym för vigselåret
1895 finns inte. H V/1 börjar 1919. Den tidigare formuleringen att den
bundna 1895-boken återstod som bildmål är därför supersederad. P I/1,
Pålysningsböcker 1849–1926, är i stället en exakt analog beställningsroute.

För nästa hushållslänk: pröva först på nytt sök-API → JSON-LD → IIIF för
Björkvik A I/17 a–b och Flen A I/25. För 1895 års lysning ska P I/1
beställas; sök inte en påhittad E I-volym. Om bild-URI fortfarande saknas eller
IIIF ger dokumenterat `401`/`403`, använd därefter en inloggad katalogsession
utan att röra CAPTCHA, eller annan laglig bildleverantör.

OpenAPI-schema, exakta registerfrågor, API-svar, JSON-LD/OAI, båda `403`-
svaren och CAPTCHA-originalet är bevarade lokalt med SHA-256 i
mediamanifestet.
