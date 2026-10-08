# T-0805 primary normative review v1

Reviewed the exact working-tree diffs in AGENTS.md, person-contract.md, source-strategy.md and working.md, plus the complete proposed PCD2026-10-07-002v1. This is a bounded follow-up to primary-specification-review-v1; no new original/source research, canonical write, task amendment or implementation approval.

## Individual dispositions

- AGENTS.md / Beständigt sökminne: APPROVE. Global scope, exact material/source revision, supplier distinction, reuse, access versus null and historical preservation are correct. “Historiska kvitton ändras inte” means immutable historical versions, consistent with the controlled revision rule; it does not forbid an explicitly documented corrective new revision.
- docs/research/person-contract.md / Negativa resultat och oberoende added paragraph: APPROVE. It correctly requires all future searches to retain individual scope and keeps the existing distinction between search result and justified negative evidence.
- docs/research/source-strategy.md / Återbruk av resultatlösa sökningar: APPROVE. Exact representation limits and pre-search reuse are appropriate. “En nyckel eller ny materialversion öppnar en motiverad ny passage” is a reason to reconsider within Wotan and an actual mandate, never an independent execution authorization; the PCD and working.md preserve that boundary.
- genealogy2/docs/working.md / new standard: APPROVE core text; REQUEST two precise additions below before final normative approval. Structure/references versus source judgement, unknown version/copy, exact null, replay and explicit subject binding are correctly distinguished. No claim that a schema certifies actual exhaustive historical research.
- proposed-PCD-2026-10-07-002-v1.md: APPROVE complete draft as written. It preserves the exact owner authorization, the three-person pilot versus global future standard, prior decisions, no new research, no global task migration and no automatic further commit/push. This review relies on root's actual push verification rather than claiming an independent remote check.

## Required bounded additions in working.md

1. After the paragraph distinguishing identifiers/snapshot, add:

> Om samma sökkvitto omfattar flera materialenheter ska varje enhet identifieras och knytas till sina faktiska söknycklar, gränser och resultat. Ange vad en bevarad kopia faktiskt återger: till exempel ett indexsvar, en katalogpost eller en originalsida. En delkopia eller ett gemensamt material-ID får inte beskrivas som fullständig kopia av flera undersökta enheter.

This prevents one mandatory singular material/snapshot field from creating false precision for several independently searched units. It is documentation/source scope, not a schema expansion mandate.

2. After the final paragraph concerning older searches, add:

> En dokumentär rättelse av ett äldre sökkvitto skiljs från en ny utförd sökning: bevara ursprungligt genomförandedatum och känt omfång, ange rättelsens belägg och ändra inte okända äldre uppgifter till nyutförda kontroller. Identiska redan accepterade operationsomförsök återger sitt ursprungliga kvitto även om källobjektet senare fått en ny revision. Historisk replaykompatibilitet är inte en tillåten väg att kringgå den nya standarden vid ny forskning.

This does not approve any specific bypass or documentary correction implementation. The implementation review must verify that the actual API behavior matches the stated historical/non-downgrade distinctions.

## Result

PCD and three shorter normative additions approved unchanged. Working.md requires only the two bounded additions above. No policy or canonical edits performed by this reviewer. Actual code/view/search writes and database immutability remain for separate final implementation review.
