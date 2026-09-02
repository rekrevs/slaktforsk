# S-0568: Riksarkivet — Piteå A I/3b–e och A I/4a–e, Olaus-screening

## Källbeskrivning

- Institution: Riksarkivet i Härnösand
- Arkivbildare: Piteå landsförsamlings kyrkoarkiv, `SE/HLA/1010154`
- Serie: A I, husförhörslängder
- Målperiod: A I/3b–e 1789–1806 och A I/4a–e 1807–1817
- Kontrollerat och hämtat: 2026-09-01

## Digital routing

JSON-LD anger både fysisk och bildmässig instansiering för alla nio volymer
men saknar direkt bild-URI. Den exakta A I/3b-posten öppnades därför i ägarens
inloggade Chrome utanför sandboxen. Riksarkivet omdirigerade även där till
ALTCHA; checkboxen lämnades orörd och ingen kontroll löstes.

Den exponerade äldre Arkis-UUID:n räckte tillsammans med Riksarkivets publika
arkivträd för att identifiera reproduktionen. Samma publika väg gav därefter
hela serien utan sessionsdata:

| Volym | Permanent id | Arkis-UUID | Reproduktion | Bildytor |
|---|---|---|---|---:|
| A I/3b | `EUudzbk3IgB63NzdcAbO7E` | `fc27ee39-06b7-4595-8c1a-ff9e62a5607e` | `C0035001` | 198 |
| A I/3c | `4WU1hwFpU4IVpYisyAXma4` | `af810712-f3a3-4478-9fce-2b36f150e124` | `C0035002` | 198 |
| A I/3d | `bGX1oa5QZ4IB54Vxi8jva3` | `ca410895-5a41-448c-8b14-47fbb08b7993` | `C0035003` | 200 |
| A I/3e | `50yo8ef9DoV1f8Ra04Gtw1` | `45640f14-9214-4f6e-8349-0dc800886fd1` | `C0035004` | 196 |
| A I/4a | `iuksR0EIuazBzqWCfHcdRD` | `6cb68bb3-9203-4fe2-97fd-203294669dbd` | `C0035005` | 226 |
| A I/4b | `hktyHBXvM2VDfRxb6k4X65` | `89fcedae-f270-4fb0-9b4b-7dca35c24235` | `C0035006` | 98 |
| A I/4c | `FEqewULjVaYYflmSSoi291` | `e928ed3c-6de5-487e-a2a6-fc1c732b0225` | `C0035007` | 257 |
| A I/4d | `9HuLQ3ikMa2PXQ6p4Iw520` | `68151e25-2e3b-405a-9985-a1b3112e8508` | `C0035008` | 245 |
| A I/4e | `hznaaVViJgF3jSJkhrsl03` | `23c9f8af-d8ef-479d-876b-89dd5ebb5e03` | `C0035009` | 249 |

De nio officiella IIIF-manifesten omfattar tillsammans 1 867 bildytor.

## Kandidatscreening

Reducerade arbetskopior av alla 1 867 bildytor screenades lokalt i två
Apple Vision-OCR-pass: hela sidan och ett vänsterutsnitt med personkolumnerna.
OCR användes enbart för att nominera namnfragment och födelseår, aldrig som
avskrift eller personbelägg.

Nio faktiska Olaus-rader i A I/3b–e och en konkret Olof-rad med födelseåret
1784 lästes därefter visuellt i maximala Riksarkivet-original. Olaus-raderna
har födelseår 1779, 1788, 1794, 1795, 1798 eller 1799 och motsvarar därför
inte Överklintenkandidaten född 1784-02-07. Den starkaste namn-/årskandidaten,
Olof född 1784 på `C0035001_00118`, står som son i Anders Pehrssons hushåll.
Han är därmed patronymiskt Andersson, inte den sökte Olaus Pehrsson, och
avvisas utan sammanslagning. A I/4a–e gav ingen nominerad målrad.

## Slutsatsgräns och återstart

Detta är ett maskinnominerat **kandidatscreeningsresultat**, inte ett
fullständigt person-, vistelse-, by-, församlings- eller helvolymsnoll.
Handskrifts-OCR kan missa namn, och volymerna saknar manifeststrukturer som
avgränsar byarna. Resultatet belägger därför inte att Olaus saknas i Piteå
eller att han inte var Barbros far. Ingen biologisk relation skapas.

De nio volymerna ska inte OCR-screenas på nytt utan en ny by-, sida-,
familje- eller flyttnyckel. En sådan nyckel ska routas direkt till de nu
bevarade IIIF-manifesten och läsas i original.

Metadataoriginal, manifest och de tio visuellt prövade kandidatbilderna
redovisas med individuella SHA-256 i
[C-0735](../citations/C-0735-pitea-AI3-AI4-olaus-kandidatscreening.md).

