# S-0585: Riksarkivet — inloggad återaktivering av spärrade specialsökningar

## Källbeskrivning

- Institution: Riksarkivet
- Tjänster: Folkräkningar, Bouppteckningar och Indelningsverket (Grill)
- Kontrollerat: 2026-09-01
- Klient: användarens egen, redan inloggade Chrome-session
- Bevarad observation:
  [strukturerad transkription](../media/S-0585-riksarkivet-inloggad-reaktivering-observation.json)

## Åtkomstproveniens

Användaren meddelade att inloggningen var aktiv och att den tidigare
CAPTCHA-utmaningen redan var besvarad. Återaktiveringen navigerade därefter
direkt till Riksarkivets egna sök- och postvyer. Ingen ny CAPTCHA eller
ALTCHA löstes eller klickades av agenten. Inga kakor, tokens, kontouppgifter,
local storage- eller session storage-värden lästes eller bevarades.

Den lokala JSON-filen är en deterministisk arbetsavskrift av synliga
sökparametrar, träffantal och postfält. Den är inte ett exporterat API-svar.
Originalbilder och officiell IIIF-/arkivmetadata bevaras separat där en
positiv träff ledde till digitalt material.

## Resultatfamiljer

- Folkräkningarna gav positiva poster för Carl Fredrik Grill 1880 och 1890
  under indexnamnet `Drill`, och för Johan Petter Zingmark 1900. De
  underliggande originalen behandlas i C-0750 respektive C-0751.
- Erik Grill 1860 och Stina Kajsa/Cajsa Nordlund 1870 gav noll träffar, men
  Riksarkivets registreringsstatus visar att deras län inte ingår i de
  aktuella indexårens redovisade täckning. De är därför täckningsuteslutna,
  inte person- eller folkräkningsnoll.
- Margareta Charlotta, född 1825 i Stockholm, gav noll 1910. Resultatet är
  frågebundet och endast förenligt med den separat källbelagda dödsnotisen
  1901; det är inte ett självständigt dödsbelägg.
- Bouppteckningsfrågorna för Abraham Jönsson, Sara Sophia Pehrsdotter och
  Henrik Henriksson gav noll träffar. Registerfullständighet eller frånvaro
  av akter har inte därigenom bevisats.
- Indelningsverket gav en positiv post för Glippsta nummer 36 i Bettna:
  Livkompaniet, Södermanlands regemente. Registret är en auktoritativ
  ort-/roterouting men namnger inte Carl Fredrik Grill i denna post.

## Källkritik

Träfflistor och normaliserade poster är sökregister, inte originalhandlingar.
Stavningsvarianter, indexfel och ofullständig år-/länstäckning gör att ett
träningssäkert frågenoll alltid måste avgränsas till exakt fråga och
registrerad täckning. Positiva personuppgifter används först efter jämförelse
med länkad originalbild eller annan central källrygg.

