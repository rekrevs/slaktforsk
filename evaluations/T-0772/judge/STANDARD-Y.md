# Bedömningsstandard Y (fastställd i T-0769, tillämpas oförändrad)

Destillerad ur T-0769:s blinda Y-granskning och rootens prövning före
avblindning. AI-härledd, inte mänskligt facit. Läs varje svar i sin helhet.

## Grind
`passed` kräver: alla 16 sakbeslut godtagbara, alla 9 requests exakt enligt
rubriken (objekt utan request ska ha null), kanonisk kunskap sakligt skyddad,
alla manuella sakkontroller uppfyllda, inga fabricerade fakta. `score` är
antalet godtagbara objektbeslut 0–16; request- och kanonfel är separata
globala grindar som underkänner utan att sänka objektpoängen.

## Redan prövade gränsfall
- **P2:** `revise` är sakligt likvärdigt med facit `retain` när texten
  uttryckligen behåller 1901-03-05 som kanoniskt datum under konflikt och
  lämnar egen födelsepost oprövad. Ersätts datumet av konfliktalternativ
  eller är bevarandet otydligt underkänns P2.
- **canonical_changes:** en icke-tom `persons`-post som bara annoterar
  konflikt och uttryckligen bevarar 1901-03-05 är en automatisk
  schemaavvikelse, inte ett kritiskt kanoniskt sakfel. Faktisk ändring av
  kanoniskt värde, ny person/relation eller ändrad OWNER_CONFIRMED är kritiskt.
- **F5:** hemort är inte dödsort och ska rättas, men den opåverkade
  befintliga uppgiften att familjen bodde i Östra Husby ska finnas kvar i
  ersättningstexten. Att ersätta hela texten med gravkortets begränsade
  utsaga tappar den uppgiften och är ett kritiskt fel i huvudbedömningen.
  Formuleringen ”ingen ny uppgift” återställer inte bostadsuppgiften.
- **sensitivity_pass_without_F5:** samma krav som `passed`, inklusive exakta
  requests och tydligt bevarat 1901-03-05, men utan kravet att F5 bevarar
  bostadsuppgiften. Ersätter inte huvudbedömningen.
- Tom evidence för uppenbart opåverkade objekt är inte fel (relevans krävs,
  inte icke-tom lista). Ett kort F3-beslut godtas om det tar bort oberoende
  dubbelräkning och säkert datumanspråk. En followup som nämner en
  födelsebok läses som sökanvisning, inte som påstått fynd.
- Manuella kontroller per objekt finns i rubriken (`manual_checks`); O1 ska
  vara 23 oktober och inte betygsnumret 20; O2 ska återge 31/5-osäkerheten
  utan säkert nytt datum; F4 ska inte behålla livslång friskhet; Q2 ska
  återöppna frågan om egen födelsepost.
