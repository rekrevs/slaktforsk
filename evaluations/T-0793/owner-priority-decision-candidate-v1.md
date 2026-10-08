## PCR-2026-10-07-001 — Verkställ anlinjeprioritet efter nodpiloten

- Record type: review
- Date: 2026-10-07
- Mode: checkpoint
- Trigger: Ägaren frågar om kärnprioriteringen faktiskt sätter säkert fastställande av anlinjer före livsbildsarbete.
- Control judgement: redirect, operate, preserve
- Current gate: Kärnkön efter T-0805 innehåller tio READY (nio CORE_LIFE, en CORE_SUPPORT) och en blockerad CORE_LIFE men ingen återstående CORE_IDENTITY. Nästa selectorval T-0217 är livsbildsrouting. T-0793:s närfrontsprövning är ännu inte utförd.
- Recommendation: Genomför T-0793 före T-0217; pröva aktuella närmaste anled och identitets-/föräldrafrågor balanserat på båda sidor, återbruka accepterat och OWNER_CONFIRMED, omsätt verkliga frågor i bounded CORE_IDENTITY först i Wotan och börja därefter första sakligt motiverade uppgiften. Bevara livsbild och sidoarbete med fullscope och senare aktivt ansvar.
- Owner decision required: none; ägaren har godkänt rekommendationen.
- Evidence: wotan/backlog.json; wotan/dev-log/T-0793.md; wotan/dev-log/T-0805.md; faktisk wotan-priority efter T-0805; ägarens frågor och ”då kör vi så”.
- Uncertainty: Maskinella grindstopp är inte automatiskt materiell identitetsosäkerhet; nästa person-/source-scope väljs först efter currentfullread, stronger/OWNER och accepted kvitton.
- Revisit when: T-0793:s individuella närfrontsprövning är klar, den första anlinjeuppgiften avslutas eller ett faktiskt hinder kräver annan genomförbar anlinjepassage.

## PCD-2026-10-07-003 — Faktisk anlinjekö före livsbildskön

- Record type: decision
- Date: 2026-10-07
- Decides review: PCR-2026-10-07-001
- Owner: Sverker Adam Janson
- Decision: Ägaren godkänner med ”då kör vi så” rekommendationen att genomföra T-0793 före T-0217, bygga konkreta anlinjeuppgifter före livsbildsuppgifterna och därefter börja den första sakligt motiverade anlinjeuppgiften. Närmast otillräckligt fastställda anled på Sverkers och Kristinas sida prioriteras balanserat; redan tillräckligt accepterade uppgifter granskas inte om enbart för nya formatfält.
- Disposition: approved
- Scope: T-0793:s fasta14nära+16djup4 och160persons planägarskap. Ny sourceexekvering sker endast inom därefter individuellt sakprövad, verifierbar och aktiv bounded Wotanuppgift. Beställningen ger mandat att börja första sådan uppgift, ingen obegränsad kökörning eller allmaterialrevision.
- Preserved rules: CORE_IDENTITY-frågor går före fristående CORE_LIFE i faktisk körordning; nödvändigt bounded CORE_SUPPORT för närfronten kan föregå dem. Livsbildernas krav och alla uppskjutna scopes kvarstår med namngiven aktiv senare checkpoint och konkreta villkor, aldrig som föräldraledets extra arkivbeviskrav. Full relevant originalutvinning inom öppnade poster, oberoende sakgranskning, individuell följdprövning, OWNER_CONFIRMED och sökminnesstandarden består.
- Supersedes decision: PCD-2026-10-05-002:s operativa ordning i den del där livsbildsrouting annars föregår oprövad närmaste anfront; tidigare utfört arbete, uppgiftsscopes och deras historik bevaras. PCD-2026-10-05-001:s hårda kärnprioritet förstärks.
- Resulting Wotan tasks: T-0793 samt dess sakprövade bounded efterföljare, namngivna i slutloggen före DONE.
- Related records: PCD-2026-10-05-001; PCD-2026-10-05-002; PCD-2026-10-07-001; PCD-2026-10-07-002; wotan/dev-log/T-0793.md.
- Portfolio signal: Aktivt projekt styrs mot direkt anlinjeprogress; ingen ytterligare metodutbyggnad är beslutad.
- Revisit when: Aktuellt anlinjepass är utfört, en balanserad generationsvåg nått sin checkpoint eller ett materiellt hinder behöver ny bounded lösning.
