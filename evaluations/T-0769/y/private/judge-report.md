# Blind sakgranskning Y, T-0769

Alla 20 anonymiserade svar har lästs individuellt i sin helhet: 16 beslut med action, rationale, replacement, evidence och resolve, samt followups och canonical_changes. Underlag: public/TASK.md, public/input.json, rubric.private.json och respektive autoresultat. Inga runs, modellnamn, schedule, measurements eller blind-map har lästs. Detta är agentfamiljens granskning, inte mänskligt facit.

Fem svar godkänns: B001, B004, B010, B018, B048 (16/16). Fjorton får 15/16 och B040 får 14/16. Poängen räknar godtagbara sakbeslut; request-/canonicalfel är separata globala grindar.

Alla femton övriga svar tappar F5:s opåverkade uppgift att familjen bodde i Östra Husby. De rättar hemort/dödsort men ersätter hela texten med gravkortets begränsade utsaga. Avsaknad av ny boendeevidens motiverar inte att stryka den befintliga saken. Enbart formuleringen ”ingen ny uppgift” återställer inte bostadsuppgiften i replacement.

B006 avslutar inte q2–q9 på respektive objekt och sätter dessutom q1 på Q1 trots att Q1 saknar request. B020, B031, B040, B049 och B059 har icke-tom canonical_changes.persons. Automatiken markerar dessa som avvikelse från fryst rubrics krav på tom canonical. Roots blinda efterprövning finner dock att B020, B031, B049 och B059 bevarar exakt 1901-03-05 och annoterar konflikt, vilket offentlig input.policy inte uttryckligen förbjuder. Dessa fyra registreras därför som automatisk schemaavvikelse, inte kritiskt kanoniskt sakfel. B040 behåller dessutom inte uttryckligen 1901-03-05 som kanoniskt datum, utan ersätter P2 med konfliktalternativen.

Samtliga svar rättar 23 oktober, återger osäkerheten 31/5, tar bort oberoende dubbelräkning och livslång friskhetsslutsats, samt bevarar OWNER_CONFIRMED, Ebbas personkärna och den opåverkade identitetsgrinden. Inga nya personer, relationer, livsbildsgodkännanden eller fabricerade arkivfynd identifierades.

## Invändning mot automatiken för roots efterprövning

Alla svar har P2.action=revise. För B001, B004, B006, B007, B010, B012, B013, B018, B020, B021, B031, B033, B042, B046, B048, B049, B050, B056 och B059 godtas själva sakbeslutet som semantiskt likvärdigt med facit retain: texten bevarar uttryckligen 1901-03-05 under konflikt och lämnar egen födelsepost oprövad. Det reviderar stöd-/konfliktbeskrivningen, inte datumvärdet. B040 har inte tillräckligt tydligt bevarande. Icke-tom canonical bedöms separat; datumbevarande konfliktannotering är efter roots blinda efterprövning en automatisk schemaavvikelse, inte i sig ett kritiskt kanoniskt sakfel.

Root ombeds efterpröva dispositionstolkningen innan resultatet används. Stickprova även F5-gränsdragningen: befintlig bostadssak måste faktiskt bevaras i ersättande text. Frysta instruktioner, facit och råsvar är oförändrade.

Mindre tolererade skillnader: tom evidence för uppenbart opåverkade objekt är inte fel eftersom instruktionen kräver relevans, inte icke-tom lista. B012:s F3 är kort men tar bort både oberoende dubbelräkning och säkert datumanspråk; osäkerheten utvecklas i angränsande beslut. B001:s followup talar om en födelsebok som befintlig källkedja hänvisar till; sådan hänvisning är inte stipulerad men läses som sökanvisning och inte påstått källfynd.

## Blind efterprövning och känslighetsanalys

Root har före unblind läst alla 20 P2/F5 och canonical_changes, instämmer i dispositionstolkningen och skiljer nu datumbevarande konfliktannotering från otillåten kanonisk sakändring. Huvudresultatet är oförändrat: de fyra berörda svaren underkänns fortfarande på F5.

F5-underlaget har en begränsning: det enda uttryckliga stödet för hela ursprungsobjektet är G1, och något separat belägg för familjens boende lämnas inte. Huvudbedömningen följer fryst rubrics krav att bostadsuppgiften ska bestå, men detta motiverar en särredovisad känslighetsanalys.

Varje finalfil har sensitivity_pass_without_F5: alla övriga sakvillkor och individuella requests måste vara uppfyllda, medan datumbevarande konfliktannotering tillåts. Här godkänns 18/20. B006 underkänns fortfarande för requesthanteringen och B040 för otydligt bevarande av befintligt kanoniskt 1901-03-05. Känslighetsresultatet ersätter varken huvudbedömningen, objektscores eller de frysta automatresultaten. Inga råsvar, frysta filer eller modellnycklar har ändrats eller lästs utanför tidigare tillåten blindgranskning.
