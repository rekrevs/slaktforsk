# C-0722: Göta livgarde 194/198 — åtkomst och Olaus-kandidater

## Källa

- [S-0550](../sources/S-0550-riksarkivet-svea-aib8-livgardesrullor.md)

## Extern Chrome-kontroll av namnregister 198

Den exakta permanenta Riksarkivet-routen för Göta livgardes namnregister
`SE/KrA/0102/A/001:Ö/0/198`, 1874–1927, öppnades i den verkliga,
inloggade Chrome-sessionen utanför sandboxen. Riksarkivet omdirigerade ändå
till ALTCHA. Kontrollens `returnUrl` exponerade den äldre Arkis-
identifieraren `ee04c964-05da-4b86-8727-b5c0ccd5d2f7`. Ingen checkbox
aktiverades och ingen CAPTCHA/ALTCHA löstes.

På ägarens förslag upprepades kontrollen 2026-09-01 i samma typ av verklig,
inloggad Chrome-session utanför sandboxen. Routen omdirigerade åter till
Riksarkivets ALTCHA-sida. Kryssrutan lämnades även denna gång orörd.

Identifieraren prövades därefter mot Riksarkivets publika batch-endpoint.
Svaret var Riksarkivets generiska felsida, inte batchmetadata,
reproduktionskod eller bildlänk. Detta är ett exakt åtkomstresultat för den
prövade katalogposten. Det visar inte att namnregistret saknar en Olaus-rad.

## Maskinassisterad kandidatkontroll i digitala volym 194

Riksarkivets publika IIIF-manifest och bilder för reproduktion `K0000725`
fungerade utan session och CAPTCHA. De kompanivisa rullbilderna 4–435
screenades maskinellt efter namnformer och periodnära årtal. OCR användes
endast för att nominera möjliga sidor; tre starkaste kandidater
kontrollerades därefter i fulla Riksarkivet-original:

- Livkompaniet nr 93 är **Per Alexander Svensson**, född 1852-03-07 och
  värvad 1876-06-03. Namn och födelsedatum avviker från Olaus.
- Fjärde kompaniet nr 47 är **Carl Olaus Carlsson**, född 1859-07-01 och
  värvad 1877-07-11. Efternamn, födelsedatum och värvningsår avviker.
- Sjunde kompaniet nr 85 är **Johan Olsson Fredberg**, född 1877-09-26 och
  värvad 1895-03-19. Förnamn, födelsedatum och period avviker.

De tre posterna avvisas därför som Olaus Fredberg. Screeningen kan missa
handskrivna namn och är varken en verifierad fullvolymsläsning eller ett
person-, förbands- eller tjänstgöringsnoll. Namnregister 198 förblir den
säkraste routen; journalerna 240 och 241 återstår därefter.

## Fulloriginal

| Bild | Storlek | SHA-256 |
|---|---:|---|
| [Livkompaniet nr 93, Per Alexander Svensson](../media/C-0722-riksarkivet-gota-194-K0000725_00015-per-alexander-svensson.jpg) | 4 703 × 5 296 px | `847aa1d1642fe27d58cc436267c5c780f181b57e33bc208c1b5eec5ccf7e2320` |
| [Fjärde kompaniet nr 47, Carl Olaus Carlsson](../media/C-0722-riksarkivet-gota-194-K0000725_00189-carl-olaus-carlsson.jpg) | 4 907 × 5 296 px | `8055163c8dd0a0e8a9c50094d5b88ae78b2261dfe459636440ce4f36acbc73d8` |
| [Sjunde kompaniet nr 85, Johan Olsson Fredberg](../media/C-0722-riksarkivet-gota-194-K0000725_00370-johan-olsson-fredberg.jpg) | 5 077 × 5 296 px | `c9c42b0d65e4ee0a3ef731359d30021396f830e5d497a0848f2f7c4a958c0b58` |

## Exakt filproveniens

- Fil: [Livkompaniet nr 93, Per Alexander Svensson](../media/C-0722-riksarkivet-gota-194-K0000725_00015-per-alexander-svensson.jpg)
- SHA-256: `847aa1d1642fe27d58cc436267c5c780f181b57e33bc208c1b5eec5ccf7e2320`
- Fil: [Fjärde kompaniet nr 47, Carl Olaus Carlsson](../media/C-0722-riksarkivet-gota-194-K0000725_00189-carl-olaus-carlsson.jpg)
- SHA-256: `8055163c8dd0a0e8a9c50094d5b88ae78b2261dfe459636440ce4f36acbc73d8`
- Fil: [Sjunde kompaniet nr 85, Johan Olsson Fredberg](../media/C-0722-riksarkivet-gota-194-K0000725_00370-johan-olsson-fredberg.jpg)
- SHA-256: `c9c42b0d65e4ee0a3ef731359d30021396f830e5d497a0848f2f7c4a958c0b58`
- Fil: [Publikt batchfel för volym 198:s Arkis-identifierare](../media/S-0550-riksarkivet-gota-198-public-batch-error.html)
- SHA-256: `b10052f622ec12275831b0ad7b32cae85f837e2fd9b5de46adb1a6e131024511`

Alla fyra filer redovisas även i `genealogy/media-manifest.json`.

## Slutsatsens gräns

Kontrollen bekräftar att även extern, inloggad Chrome kan möta ALTCHA på
den exakta analoga katalogrouten, medan volym 194:s offentliga IIIF-bilder
fungerar utan session. Den avvisar tre namnlika rullposter men varken Olaus
Fredberg, Göta livgarde eller något annat förband i stort. Ingen identitet,
tjänstgöring eller relation skapas.

## Stödda påståenden

A-2813–A-2814.
