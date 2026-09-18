# S-0578: Riksarkivet — Piteå stad A I/1a–2a, Olaus-registerroute

## Källbeskrivning

Källpaketet prövar den positiva `Piteå`-nyckeln på Olaus Pehrssons rad i
Bygdeå A I/6 mot Piteå stadsförsamlings första två husförhörslängder. Endast
Riksarkivet användes. Den tidigare bevarade facetterade API-responsen
[S-0552](../media/S-0552-riksarkivet-pitea-stad-faceted-api.json) innehåller
volymposterna.

| Volym | Datering | Permanent id | Äldre Arkis-UUID | Reproduktion | Omfattning |
|---|---|---|---|---|---|
| Piteå stad `SE/HLA/1010155/A I/1a` | 1812–1822 | `qOTXwDefsKUH5DToYdVu91` | `e86187d1-29da-47d9-9114-d7728a77f825` | `C0035078` | 190 bildytor |
| Piteå stad `SE/HLA/1010155/A I/1b` | 1812–1822 | `63e75yOoznFfp7Wb9RLhL4` | `17073a18-65cc-4ffc-a731-e09496d5ad54` | — | separat, enligt katalogen ofullständigt personregister |
| Piteå stad `SE/HLA/1010155/A I/2a` | 1823–1831 | `kzTuAkyl8H8jAnfGny8zLr` | `55f0eebb-bcde-4884-b4ac-69431f11f575` | `C0035079` | 424 bildytor |
| Piteå stad `SE/HLA/1010155/A I/2b` | 1823–1831 | `KW5IjBubTq6RM54FPxojp2` | `b4520152-25be-4177-9b58-510f67bcadce` | — | separat personregister utan publik reproduktionsroute |

Kontrollerat och hämtat: 2026-09-01.

## Åtkomst och reproduktionsrouting

De fyra permanenta kataloglänkarna prövades i ansluten Chrome utanför
filsystemsandboxen. De omdirigerade fortfarande till Riksarkivets
CAPTCHA-sida; `returnUrl` exponerade respektive äldre Arkis-UUID. Ingen
kontroll aktiverades och inga sessionsdata lästes eller sparades.

De publika `Tree/SubTree`-svaren för A I/1a och A I/2a gav däremot
reproduktionerna `C0035078` och `C0035079`. Deras officiella IIIF-manifest
och maxbilder kunde hämtas utan CAPTCHA eller sessionsdata. De separata
personregistren A I/1b och A I/2b gav tomma publika arkivträd och ingen
reproduktion. Direkta JSON-LD-omprov utanför nätverkssandboxen gav WAF-HTML
i stället för JSON; de felmärkta temporära svaren har inte bevarats som
källoriginal.

## Inbundna register i huvudvolymerna

Trots de separata registerposternas åtkomstläge innehåller huvudvolymernas
inledande bildytor fotograferade personregister. Manifesten saknar
strukturer, så de relevanta alfabetbladen identifierades visuellt:

- A I/1a bild `C0035078_00028` täcker P–R. Ingen registerrad läses Olaus eller
  Olof Pehrsson/Persson. Katalogen kallar A I/1b uttryckligen
  `Ofullständigt`; resultatet är därför bara ett noll på det exakta
  fotograferade registerbladet, aldrig ett helvolyms- eller personnoll.
- A I/2a bild `C0035079_00033` täcker P–R och har raden `Persson, Olof` med
  hänvisning till sida 192.

## Den avvisade sidan 192-kandidaten

A I/2a bild `C0035079_00250`, sida 192, visar den registerhänvisade mannen
som `Drängen Olof Pehrsson`, född 1804-04-21. Han är därför inte Olaus
Pehrsson från Överklinten, född 1784-02-07. Den konkreta namnkandidaten
avvisas utan sammanslagning och utan relation till Barbro Olofsdotter.

Resultatet säger inte att Olaus saknades i Piteå stad eller land under hela
perioden. Det visar bara vad de två P–R-registerbladen innehåller och att den
enda hänvisade Olof Persson/Pehrsson på det senare bladet har fel
födelsedatum.

## Återaktivering

1. Upprepa inte P–R-registerbladen eller sida 192 utan en ny
   namn-, sida-, hushålls- eller flyttnyckel.
2. A I/1a:s register är uttryckligen ofullständigt; skapa inget personnoll
   från den tomma Olaus/Olof-kontrollen.
3. A I/2a-kandidaten född 1804-04-21 är avvisad. Följ honom inte som
   Överklintenmannen.
4. Olaus Pehrsson förblir endast en faderskandidat till Barbro. Skapa ingen
   far- eller farbrorsrelation utan uttrycklig handling.
5. Återta Piteåspåret först med en ny ort-, hushålls-, flytt- eller
   relationsnyckel; de tidigare landsförsamlingsscreeningarna ska inte
   upprepas blint.

## Lokalt bevarade metadata- och processoriginal

| Fil | Byte | SHA-256 |
|---|---:|---|
| [A I/1a IIIF-manifest](../media/S-0578-riksarkivet-pitea-stad-AI1a-C0035078-IIIF-manifest.json) | 552961 | `1944905e2f7787172446a8af79f95cce544a3f280d96b5d63665af42c2e99080` |
| [A I/2a IIIF-manifest](../media/S-0578-riksarkivet-pitea-stad-AI2a-C0035079-IIIF-manifest.json) | 1232200 | `92ef6b2cf457a3ba0e88f15842ccb788a302e8a94d116bec1be73bfe97d675c2` |
| [Rensade route- och registerobservationer](../media/S-0578-riksarkivet-pitea-stad-register-route-observations.json) | 3993 | `96232cb0d3ae7fc1c7cc461e70e829db06d9131cf0c017e9f804e738a1629f91` |

Fulloriginalen redovisas med mått, byte och checksummor i
[C-0745](../citations/C-0745-pitea-stad-register-olaus-pehrsson.md).

## Stödda påståenden

A-2899–A-2902.
