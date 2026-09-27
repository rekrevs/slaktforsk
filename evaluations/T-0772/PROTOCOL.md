# T-0772 – fryst protokoll

Replikering av [T-0769](../T-0769/PROTOCOL.md) med Claude Opus 5.5.
Ägarbeställt 2026-09-27. Ägaren valde båda resonemangsnivåerna och blind
Astra-granskning.

30 nya sessioner: 3 uppgifter × 2 armar × 5 upprepningar. Modell
`claude-opus-5-5`. Arm `opus55-medium` motsvarar T-0769:s `medium`; arm
`opus55-xhigh` är den nivå ägaren kör interaktivt. Slumpad startordning
seed 772, högst tre parallella försök, max 15 min per försök. Timeout räknas
som misslyckat försök med kvarvarande artefakt. Inget försök upprepas eller
ersätts, inga tips eller rättningsrundor.

Samma frysta publika paket som T-0769 (kontrollsummor enligt dess
frozen-manifest, oförändrade 2026-09-27), samma `WRAPPER.txt` byte för byte;
endast RUN_DIR skiljer sig. Startmeddelandet är RUN.md utan avslutande
radbrytning.

## Körmiljö

Varje försök är en ny `claude -p`-process (Claude Code 2.1.283) med
arbetskatalog RUN_DIR, exakt kommandorad i `logs/<id>.start.json`:
`--model claude-opus-5-5 --effort <nivå> --permission-mode acceptEdits`,
tillåtna verktyg Read/Write/Edit/Bash/Glob/Grep, WebFetch/WebSearch/Agent
avstängda, inga MCP-servrar (`--strict-mcp-config`) och ingen Chrome.
Användarens och projektets CLAUDE.md laddas som i vanligt arbete, i likhet
med Codex AGENTS.md-laddning i T-0769. Filredigeringsverktygen är begränsade
till RUN_DIR; Bash är tillåten för egna bildutsnitt och JSON-kontroll, så
isoleringen är i övrigt instruktionsbaserad som i T-0769. Skillnad mot
T-0769: nätverks-, MCP- och subagentverktyg är tekniskt avstängda i stället
för endast förbjudna.

Effort sätts med CLI-flagga; API-svaret ekar inte nivån. Kommandoraden per
försök är därför beviset, tillsammans med rapporterad modell i strömmen.

## Mätning

Råström (stream-json) per försök i `logs/`, utanför RUN_DIR: verktygsanrop
med argument, tokenanvändning per svar, `total_cost_usd` (Claude Codes
listprisberäkning), tider. Tid mäts som processens start till slut samt
rapporterad `duration_ms`. Kostnadsproxy: Anthropic listpris för
claude-opus-5-5, $4/M input, $20/M output, $0,20/M cacheläsning, $8/M
1h-cacheskrivning ($5/M 5m); kontrollerat mot Claude Codes egen
listkostnad i pilot 2026-09-27. Inte faktisk abonnemangsdebitering.

## Bedömning

Automatiska kontroller oförändrade från T-0769: `score_x.py`, `score_y.py`,
`z/private/evaluate.mjs` med verklig införsel i engångsdatabas.

Blind sakbedömning: tre separata `codex exec`-kontexter med
`gpt-6-astra`, reasoning `medium` (samma som T-0769:s granskare), en per
uppgift. Svaren får slump-ID `Cnnn` utan modell/arm. Till de 30 nya svaren
blandas 11 kalibreringssvar från T-0769 (seedat urval över godkända och
underkända) under samma slump-ID-serie. Granskaren får fryst rubrik och en
bedömningsstandard destillerad ur T-0769:s granskarrapporter och
rootadjudikation, utan svarsspecifika utfall. Samma grindar: X ≥68/75 och
inga kritiska fel; Y alla 16 beslut, 9 requests, skydd och F5-bevarande med
känslighetsfält; Z 15 automatiska kontroller plus individuella sakskäl, med
`material_pass` för enbart titelpunkt.

Rooten (Opus 5.5, samma modell som prövas) granskar bara formella fel i
granskningen före låsning och får inte ändra sakbedömning utan redovisad
avvikelse. Betyg låses med kontrollsummor innan blindnyckeln används.
Kalibrering redovisas som överensstämmelse mellan nya och låsta T-0769-betyg
för ankarsvaren; avvikelser där visar granskarens drift, inte modellfel.

## Begränsningar

Fem upprepningar på samma material mäter körstabilitet, inte fem oberoende
genealogiska fall. Opus 5.5 körs genom Claude Code och OpenAI-modellerna
genom Codex; verktygsskal och systeminstruktion skiljer sig och ingår i
det som mäts. Cacheprissättning skiljer sig mellan leverantörerna
(Anthropic tar betalt för cacheskrivning). Gemensamt filsystem,
instruktionsbaserad läsisolering; verktygsloggar granskas för otillåten
läsning och rapporteras separat, utan ersättning.
