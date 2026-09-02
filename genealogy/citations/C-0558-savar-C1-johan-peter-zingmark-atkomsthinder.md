# C-0558: Sävar C/1 för Johan Peter Zingmark stoppad av API/WAF och ALTCHA

## Källa och mål

[S-0446](../sources/S-0446-riksarkivet-savar-C1-atkomst-2026-08-29.md),
Sävar `SE/HLA/1010199/C/1` 1823–1837, målpost 1825-02-01.

## Utfall

Sök-API-frågan på den exakta referenskoden kunde inte levereras i den
aktuella nätmiljön (`403`/WAF respektive `ERR_BLOCKED_BY_CLIENT`). Den
inloggade katalogens reservsökning utlöste ALTCHA; kontrollen lämnades
orörd. Ingen volymsida lästes och ingen källträff eller källnoll fastställdes.

## Tolkning

Detta är en ren åtkomstincident. Johan Peters uppgift 1825-02-01 i Sävar
står kvar från hushållskällan C-0552, men egen födelsenotis och föräldrar är
fortsatt öppna. Exakt återaktiveringsväg finns i S-0446.

## Senare API-omprov

C-0587 dokumenterar att WAF-fasen senare löstes: API och JSON-LD svarar nu
`200`, men bildrepresentationen saknar URI. Hindret har därmed flyttats
från API-leverans till reproduktionsidentifiering; ingen källsida har ännu
lästs.

## Stödda påståenden

A-2454.
