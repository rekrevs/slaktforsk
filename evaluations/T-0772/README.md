# T-0772 – Opus 5.5 på T-0769:s modelltest

Ägarbeställt 2026-09-27. Utförande och återstart ägs av
[wotan/dev-log/T-0772.md](../../wotan/dev-log/T-0772.md).
Resultat: [report.md](report.md).

- `PROTOCOL.md`, `frozen-manifest.json`, `schedule.json` (seed 772),
  `WRAPPER.txt` (byte-identisk med T-0769).
- `runs/<id>/`: indata (T-0769:s publika paket), `RUN.md`, `answer.json` och
  försökets egna bildutsnitt.
- `logs/`: kommandorad (`*.start.json`), råström (`*.stream.jsonl`),
  avslut; `runs-telemetry/`: härledd telemetry med verktygsanrop.
- `blind/`, `blind-map.private.json` (30 försök + 11 T-0769-ankare),
  `judge/` (standarder, prompter, granskarnas utfiler och händelser),
  `scores/` (auto och final), `grade-lock.json`.
- `prices.json`: Anthropic listpris som proxy, inte faktisk debitering.

Kör inte om försöken eller granskarna; `run_trials.py` och `run_judges.py`
vägrar starta om något som redan startat. Reproducerbara kontroller från
denna katalog:

```sh
python3 collect.py && python3 audit.py
python3 prepare_blind.py && python3 score_automatic.py
python3 summarize.py
python3 verify_benchmark.py
```

`collect_aux.py` förutsätter att granskarnas händelser finns och kan ges
rootsessionens Claude Code-transkript som argument.
