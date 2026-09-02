# S-0577: Riksarkivet — Lycksele A I/7 och C/2, Petter Reinholds route

## Källbeskrivning

Källpaketet återtar den Lycksele-route som Degerfors A I/2 sida 179 anger
för Petter Reinhold Pehrsson. Endast Riksarkivet användes.

| Volym | Datering | Permanent id | Äldre Arkis-UUID | Reproduktion | Omfattning/använt ställe |
|---|---|---|---|---|---|
| Lycksele `SE/HLA/1010118/A I/6` | 1810–1817 | `OKR8b0QODaE0oFa01Bzma4` | `94c84661-9806-4336-80c8-f90004bfe124` | `C0034136` | 187 bildytor; endast digital route säkrad |
| Lycksele `SE/HLA/1010118/A I/7` | 1817–1828 | `fia6FyUUuQPH3Kjsac2Wk2` | `3f06c9a6-3dcf-4cc3-a21a-96ed24c14172` | `C0034137` | bild 164, sida 126, Åskilje |
| Lycksele `SE/HLA/1010118/C/2` | 1778–1813 | `gN6FEww6hKYywO7yuLaSa8` | `3b8f71a9-86ae-48ad-bdd3-03fb85647248` | `C0034150` | hela födelseåret 1798 på bilderna 111–112; bild 113 börjar 1799 |
| Lycksele `SE/HLA/1010118/B I/1` | 1834–1842 | `Exfq5YVySYTEkV27UGdfw0` | — | — | första katalogiserade inbundna flyttningsvolymen börjar efter målperioden |

Kontrollerat och hämtat: 2026-09-01. De tidigare records-API-, JSON-LD-
och OAI-originalen för A I/6, A I/7 och C/2 bevaras i
[S-0567](S-0567-riksarkivet-lycksele-och-degerfors-kallgap.md).

## Bruten bildspärr

De tre permanenta kataloglänkarna prövades i ansluten Chrome utanför
filsystemsandboxen. Var och en omdirigerade fortfarande till Riksarkivets
CAPTCHA-sida, men `returnUrl` exponerade den äldre Arkis-UUID:n. Ingen
kontroll aktiverades och inga sessionsdata lästes eller sparades.

Riksarkivets publika `Tree/SubTree`-svar för UUID:erna angav därefter
reproduktionerna `C0034136`, `C0034137` och `C0034150`. De tre officiella
IIIF-manifesten och de använda maxbilderna fungerade utan CAPTCHA; maxbilderna
hämtades med Riksarkivets bildvisare som `Referer`.

## Positiv rad i Åskilje

Lycksele A I/7 bild `C0034137_00164`, sida 126, har ortsrubriken Åskilje.
En separat rad läses försiktigt `Rein[hold] Pehrsson`, född 1798. Förnamnet
är kontraherat i originalet och `Petter` skrivs inte ut på denna rad.

Identiteten stöds i kombination med Degerfors A I/2 sida 179: där står det
ovanliga fulla namnet Petter Reinhold Pehrsson, samma födelseår 1798 och den
uttryckliga uppgiften att han flyttat till Lycksele med attest. Namnprofil,
år och riktad flyttanteckning gör Åskiljeraden till samme man med hög
tillförlitlighet. Raden namnger däremot inga föräldrar, ingen födelseort och
ingen exakt födelsedag. Den ska inte användas för släktskap med de omgivande
hushållen.

För att lokalisera raden screenades A I/7:s 226 sakliga bildytor efter
register/frontmatter med två lokala Apple Vision-OCR-pass på observerad
Apple M4 Max (`arm64`): hela reducerade bildytan och ett förstorat vänsterfält
med personkolumnerna. OCR användes endast för kandidatnavigation. Den positiva
bilden och varje här återgiven uppgift lästes därefter visuellt i maximalt
Riksarkivet-original. Screeningen är inte ett helvolyms- eller personnoll,
och A I/6 personscreenades inte.

## Komplett Lycksele C/2-årgång 1798

C/2 bild `C0034150_00111` börjar uttryckligen födda och döpta år 1798.
Bild 112 fortsätter årgången till dess sista daterade poster, och bild 113
börjar 1799. Hela namn- och föräldraföljden på bilderna 111–112 lästes
visuellt i maxoriginal utan Petter/Peter/Petrio Reinhold Pehrsson.

Den enda nära förnamnsposten är `Petrio`, född 1798-07-06, på bild 111.
Föräldrarna anges som Olof Ersson i Wargträsk och Elisabeth
Abrahamsdotter. Fadern gör pojken till Olofsson, inte Pehrsson, och inget
Reinhold-namn står i posten; kandidaten avvisas därför.

Resultatet är endast volym-, församlings-, årgångs- och namnformsbundet.
Det bevisar inte att Petter Reinhold föddes någon annanstans eller att
1798-årsuppgiften är exakt.

## Flyttningsseriens lucka

Riksarkivets exakta JSON-LD-post för Lycksele B I/1 daterar den första
katalogiserade inbundna flyttningsvolymen till 1834–1842. Den täcker inte
A I/7-perioden eller återgången till Degerfors före vigseln 1826. Detta är
ett källgap, inte ett flyttnings- eller vistelsenoll.

## Återaktivering

1. Upprepa inte A I/7:s blinda OCR-screening; återgå direkt till Åskilje
   sida 126 och följ en ny positiv sida-, by-, hushålls- eller flyttnyckel.
2. Upprepa inte Lycksele C/2 eller Degerfors C/1 år 1798 utan en ny
   datum-, orts- eller familjenyckel.
3. A I/6 har nu en fungerande reproduktionsroute men inget läst
   personinnehåll. Screenas först om en ny källa placerar Petter i Lycksele
   före 1817.
4. Skapa inga föräldrar från Åskiljehushållets närhet. Exakt födelsedag,
   födelseort och föräldrar är fortsatt öppna.

## Lokalt bevarade metadata- och processoriginal

| Fil | Byte | SHA-256 |
|---|---:|---|
| [A I/6 IIIF-manifest](../media/S-0577-riksarkivet-lycksele-AI6-C0034136-IIIF-manifest.json) | 538439 | `e6ccc62c0afc14e0f649bf7b132f36749330e7e55c3794d5312852ef2aaaf47d` |
| [A I/6 Tree/SubTree](../media/S-0577-riksarkivet-lycksele-AI6-tree.html) | 773 | `6755032b570285d5a4f37cb1c3db85c5aa10bbb2cd5d1431183ecebebae6e799` |
| [A I/7 IIIF-manifest](../media/S-0577-riksarkivet-lycksele-AI7-C0034137-IIIF-manifest.json) | 695462 | `5025658c0334e72aed3fe30f1a9cd720788c3cdd16f879d8208209c89df1b46f` |
| [A I/7 Tree/SubTree](../media/S-0577-riksarkivet-lycksele-AI7-tree.html) | 773 | `739935a4d22fe398bd42bf0f8ae08cf2e72e944aa350c682e5bfa39ba040cc9f` |
| [C/2 IIIF-manifest](../media/S-0577-riksarkivet-lycksele-C2-C0034150-IIIF-manifest.json) | 594116 | `a68ec231e8beef6cb94f5589e30b357dffbe196a6d43ecc8b69af410ecb1554a` |
| [C/2 Tree/SubTree](../media/S-0577-riksarkivet-lycksele-C2-tree.html) | 773 | `f7594aac373e2535a859ddc1ab75a0d0cd5b502d332cf9b854bc1f910cf7a718` |
| [B I/1 JSON-LD](../media/S-0577-riksarkivet-lycksele-BI1-jsonld.json) | 3531 | `82e9ba6a4a5926c08188e735f02e422ee7dcc511c48f744bd30fc8b178dc156b` |
| [Rensade route- och screeningobservationer](../media/S-0577-riksarkivet-lycksele-route-screening-observations.json) | 3854 | `58a528273d2a9b4e98ec1c536468548372b6ceba5a13fe5912a4817f91b9b3b8` |

Fulloriginalen redovisas med individuella mått och checksummor i
[C-0744](../citations/C-0744-lycksele-askilje-petter-reinhold-C2-1798.md).

## Stödda påståenden

A-2896–A-2898.
