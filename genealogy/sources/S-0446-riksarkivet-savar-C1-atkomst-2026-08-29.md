# S-0446: Riksarkivet — Sävar C/1, åtkomstförsök 2026-08-29

> Historisk åtkomstpost. Hindret supersederades 2026-08-30 av
> [S-0520](S-0520-riksarkivet-savar-C1-AI1-zingmark.md), där volymens
> reproduktion och målbild är lösta och lästa.

## Målvolym

- Arkiv: Sävar kyrkoarkiv, `SE/HLA/1010199`
- Volym: C/1, födelse- och dopbok 1823–1837
- Referenskod: `SE/HLA/1010199/C/1`
- Målpost: Johan Peter Zingmark, uppgiven född 1825-02-01 i Sävar

## API-först-försök och hinder

Den tidigare API-inventeringen hade identifierat volymen men ingen bildlänk.
Vid återaktiveringen 2026-08-29 prövades först en exakt sök-API-fråga på
referenskoden. Direktanropet gav `403` med WAF/HTML-svar; försök att öppna
samma API-URL i de tillgängliga nätkontexterna stoppades med
`ERR_BLOCKED_BY_CLIENT`. Detta är ett åtkomsthinder, inte ett söknoll.

Först därefter prövades den inloggade NAD-katalogen. Sökning på
`Sävars kyrkoarkiv` utlöste en ALTCHA-dialog (`Verifiera att du är människa`,
`Jag är inte en robot`). Ingen CAPTCHA-kontroll aktiverades. Ingen
katalogpost eller källbild lästes i detta försök.

## Återaktiveringsväg

1. Försök åter med sök-API och JSON-LD när WAF-/klientspärren har lättat.
2. Om bildlänk fortsatt saknas: låt ägaren uttryckligen godkänna/manuellt
   hantera ALTCHA i den inloggade katalogen och lös reproduktions-id:t.
3. Pröva därefter IIIF före bildvisaren. Om IIIF svarar `401`/`403`, använd
   den inloggade bildvisaren och bevara fulloriginalet.
4. En lagligt åtkomlig parallell leverantör kan användas, men ska få egen
   källpost och full provenans.

## API-omprov 2026-08-29

Ett senare URL-kodat omprov med korrekt `Accept` och vanlig `User-Agent`
lyckades. Sök-API:t identifierade C/1 som id
`jhPzyZGRDb8aSLomDTa2u0`; JSON-LD svarade `200` och visar att en
bildrepresentation finns. Representationen saknar dock URI, manifest och
batch-id. Den tidigare WAF-spärren är alltså löst, men bildåtkomsten är
fortsatt spärrad på metadata→reproduktion. API-originalen och den nya
återstarten finns i C-0587. Chrome användes inte.

## Källkritik

Ingen negativ slutsats om Johan Peters födelse eller föräldrar får dras av
denna post. Den dokumenterar endast att den redan identifierade volymen inte
kunde öppnas i denna körning.
