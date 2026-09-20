# T-0769 modelljämförelse

Ägarbeställt 2026-09-19. Utförande och återstart ägs av
[wotan/dev-log/T-0769.md](../../wotan/dev-log/T-0769.md).
Ordinarie forskning förblir pausad.

- `PROTOCOL.md`: försöksdesign och begränsningar.
- `schedule.json`: förutbestämd körordning, tre samtidiga som mest.
- `frozen-manifest.json`: kontrollsummor före försöken.
- `x/public`, `y/public`, `z/public`: testpaket; varje försök har egen kopia.
- `runs/`: råa svar och telemetry med verkliga modell-/effortfält,
  tokenposter, tider och verktygsanrop.
- `blind/`: byte-identiska svar med slump-ID utan modellnamn.
- `scores/`: automatisk förkontroll och blind sakbedömning, hålls isär.
- `prices.json`: verifierade standard-API-priser som jämförelsegrund,
  inte faktisk debitering i Codex.

Kör inte om försöken rutinmässigt. Nya repetitioner är nya försök och ska
inte ersätta misslyckade svar. Ingen evaluator skriver ordinarie databas.

Reproducerbara kontroller från repositoryroten:

```sh
python evaluations/T-0769/collect.py
python evaluations/T-0769/prepare_blind.py
python evaluations/T-0769/score_automatic.py
python evaluations/T-0769/audit.py
node evaluations/T-0769/z/private/self-test.mjs
python evaluations/T-0769/summarize.py
```

`collect.py` förutsätter att lokala Codex-loggar finns kvar. Härledda
telemetryfiler är bevarade utan kompletta miljö-/kontouppgifter. Tokenantal
summerar varje responss användning en gång; cached input är en del av input,
reasoning output en del av output. `tool_calls` räknar yttre verktygsanrop;
ett `functions.exec` kan i sin tur utföra flera lokala verktygsoperationer.

Startmeddelandet och RUN.md är lika efter normalisering av den egna
körkatalogen. Katalognamnet avslöjar modell/upprepningsnummer för försöket;
resultatbedömaren får endast ett slump-ID. Alla modeller får samma frysta
uppgift per X/Y/Z. Isoleringen är en instruktion och nya kontexter, inte en
separat OS-sandbox. Granskningen måste därför kontrollera faktisk läsning.

Två verkliga bildutsnitt samt syntetiserade Y/Z-mikrofall kan vägleda
arbetsfördelning för dessa moment. De mäter inte fri källsökning,
webbnavigering, lång kontext, hela personakter eller generell genealogisk
bevisförmåga. Fem upprepningar av samma paket är inte fem olika källfall.
