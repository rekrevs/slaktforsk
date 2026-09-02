# S-0463: Riksarkivet — Stöde A I/8–9, Hullsjö 1833–1850

## Målvolym

- Arkiv: Stöde kyrkoarkiv, `SE/HLA/1010189`
- Volym: husförhörslängd A I/8, 1833–1842
- Referenskod: `SE/HLA/1010189/A I/8`
- Riksarkivet-id: `WLbpWnDgeK67prw9qLW5I0`
- Reproduktionsserie: `C0033554`
- Fortsättningsvolym: A I/9, 1843–1850, `SE/HLA/1010189/A I/9`
- Riksarkivet-id A I/9: `w0CC9P9MYaAxxOq9fRyZW5`
- Reproduktionsserie A I/9: `C0033555`
- Mål: lokalisera Abraham Jönssons föräldrahushåll i Hullsjö omkring hans
  födelse 1840-02-22 och pröva om hushållet står kvar i nästa längd
- Läst och hämtad: 2026-08-29

## API-först-resultat

Ett URL-kodat sök-API-anrop identifierade A I/8 exakt men saknade
`_links.image`. JSON-LD svarade `200` och visade analog och bildmässig
instansiering utan bild-URI. OAI-EAD svarade `200` och bekräftade signum och
datering utan reproduktionslänk.

Den seriemässigt härledda batchen `C0033554` prövades därefter direkt.
Manifest och `info.json` på den äldre IIIF-vägen gav `403`; även den senare
`/v2/arkis!C0033554_00002/info.json` gav `403` utanför visarsessionen.
Svarshuvuden och svarskroppar är bevarade.

Först efter dessa API-/IIIF-resultat användes Riksarkivets vanliga katalog i
den inbyggda reservwebbläsaren. Katalogen visade en `Bild`-länk utan
inloggning och utan CAPTCHA:

- katalog: <https://sok.riksarkivet.se/arkiv/WLbpWnDgeK67prw9qLW5I0>
- reproduktionsingång:
  <https://sok.riksarkivet.se/bildvisning/83735981-6a13-41a1-87cf-5e89d1580548>
- visaren löste ingången till `C0033554_00001`
- volymen har 262 bilder; bild 14 motsvarar sida 1 och bild 261 sida 243

Visaren laddade IIIF v2-resurser inom sin session trots att samma direkta
anrop gav `403`. Efter pausen lästes bilderna 3–13: de innehåller
slate-/titel-/försätts- och instruktionsblad men inget ortsregister. Det är
ett routingresultat, inte ett personnoll. En systematisk läsning av de
paginerade ortsrubrikerna lokaliserade i stället **Hullsjön till sidorna
88–97**, bilderna `C0033554_00102`–`_00111`; sida 98,
`C0033554_00112`, har en annan ortsrubrik och bevarar gränsen.

På sida 88 står `Jöns Abramsson`, född 1805-08-22, med hustrun Brita
Jonsdotter, född 1812-07-28. I barnraderna står den säkert lästa Brita,
född 1834-03-12, Magdalena, född 1837-05-02, och sonen Abraham, född
1840-02-22. En äldre överstruken barnrad, född 1831-07-10, har inte fått en
personakt eftersom namnet inte kan läsas säkert. Abrahams egen födelsenotis
C-0333 ger samma föräldrapar och datum.

A I/9 identifierades i samma bevarade seriefråga. JSON-LD svarade `200`
utan bild-URI och direkt manifest gav åter `403`; först därefter användes
reservvisaren. Bilderna 2–12 saknar ortsregister. Den systematiska
ortsrubriksläsningen lokaliserade hela Hullsjöavsnittet till sidorna 92–93,
bilderna `C0033555_00105`–`_00106`; sida 94, bild `_00107`, börjar Högsjö.
De båda Hullsjösidorna saknar en säker rad för Jöns Abrahamsson, Brita
Jonsdotter eller Abraham född 1840. Det är ett strikt orts- och
volymintervallsnoll, inte belägg för vart familjen flyttade.

## Bevarade metadata- och hindersvar

- `S-0463-riksarkivet-stode-AI-api-records.json`
- `S-0463-riksarkivet-stode-AI8.jsonld`
- `S-0463-riksarkivet-stode-AI8-oai-ead.xml`
- `S-0463-riksarkivet-stode-AI8-IIIF-manifest.headers.txt`
- `S-0463-riksarkivet-stode-AI8-IIIF-manifest-response.bin`
- `S-0463-riksarkivet-stode-AI8-IIIF-info.headers.txt`
- `S-0463-riksarkivet-stode-AI8-IIIF-info-response.bin`
- `S-0463-riksarkivet-stode-AI8-IIIF-v2-info.headers.txt`
- `S-0463-riksarkivet-stode-AI8-IIIF-v2-info.json`

Manifest- och äldre `info.json`-svaren är avsiktligt bitidentiska `403`-
svar för två skilda URL:er. Exakta byteantal och SHA-256 finns i
`genealogy/media-manifest.json`.

## Bevarade fulloriginal

- C-0590 bevarar samtliga Hullsjösidor 88–97 i A I/8 samt den första
  efterföljande ortssidan 98, alla i full upplösning.
- C-0591 bevarar A I/9:s båda Hullsjösidor 92–93 och den efterföljande
  Högsjösidan 94, alla i full upplösning.
- Dimensioner och SHA-256 redovisas per fil i citationsakterna och i
  `genealogy/media-manifest.json`.

## Exakt återaktivering

1. Följ Jöns och Brita bakåt från A I/8 sida 88 till föregående
   husförhörslängd och till deras egna födelsenotiser 1805-08-22 respektive
   1812-07-28; välj inte namnlikheter utan sammanhängande hushållslänk.
2. Följ familjen framåt utanför Hullsjö efter 1842 via flyttningslängd eller
   en positiv hänvisning. A I/9 sidor 92–93 ska inte läsas om utan ny
   ortsledtråd.
3. Vid ny bildhämtning: pröva sök-API → JSON-LD → IIIF först och använd
   reservvisaren endast efter dokumenterat direktfel. Ingen CAPTCHA visades
   i den genomförda läsningen.

Tillfälliga beskärningar och skärmbilder i `/private/tmp` var endast
läshjälpmedel. De är inte evidens och ingår inte i projektets beständiga
material.
