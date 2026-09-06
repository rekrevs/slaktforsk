# C-0963: Stockholms mantalslängd 1877 är digitaliserad — källvägen till Olaus mantalsuppgift öppnas

## Källa

[S-0752](../sources/S-0752-stockholm-mantalslangder-1877.md)

## Exakt lokalisering

Manifestetiketter för bildbatcherna `A0057715`–`A0057760`, hämtade
2026-09-06 i T-0082, samt tre lästa uppslag:

- `A0057718_00006` (`G 1 BA:76/1`) — `Qvarteret Träskbacken`
- `A0057721_00006` (`G 1 BA:76/4`) — `Qvarteret Sperlingens backe`
- `A0057735_00006` (`G 1 BA:76/20`) — `Qvart. Öfra Jerngrafven`

## Utfall

**Den tidigare slutsatsen att 1877 års mantalsmaterial kräver läsesal är
delvis överspelad.** [C-0649](C-0649-kungsholm-15-kungsholmsgatan-och-mantalsvag.md)
byggde på Stadsarkivets instruktion för **mantalsuppgiften**, alltså serien
`G 1 BB`. Den serien har fortfarande ingen bildlänk. Men **mantalslängden**,
serien `G 1 BA`, är en annan handling, och **hela årgången 1877 är
digitaliserad**: fyrtiotvå volymer, `G 1 BA:76/1`–`76/42`, i batcherna
`A0057718`–`A0057757`, drygt elva tusen bildytor, alla åtkomliga över det
öppna IIIF-API:et.

Mantalslängdens formulär har dessutom **en egen kolumn `Nummer å
Mantalsuppgiften`**. Det är exakt det nummer som Stockholms stadsarkivs
Mantalsregister 1800–1884 gav för Olaus:
**Kungsholmen 1877, nummer 1217** ([C-0648](C-0648-stockholms-mantalsregister-1876-negativ-1877-kontroll.md)).
Numret är alltså läsbart i en digitaliserad källa.

**Vad som återstår är en lokaliseringsfråga, inte ett åtkomsthinder.**
Volymerna är ordnade **efter kvarter**, och kolumnens numrering börjar om
lågt i varje volym — stickprovet i `76/20` visar `2` på första raden. Numret
1217 kan därför inte användas som direkt ingång. Vägen går i stället över
adressen: [C-0649](C-0649-kungsholm-15-kungsholmsgatan-och-mantalsvag.md) rättade den
till **15 Kungsholmsgatan**, så det gäller att finna den eller de volymer i
`76/1`–`76/42` som upptar Kungsholmens kvarter och därefter fastigheten.

De tre lästa kvartersrubrikerna visar att ordningen varken är alfabetisk
eller församlingsvis i någon uppenbar följd: `Träskbacken` i volym 1,
`Sperlingens backe` i volym 4 och `Öfra Jerngrafven` i volym 20. Ingen av
dem ligger på Kungsholmen. Volymidentifieringen är alltså **påbörjad men
inte avslutad**.

**Åtkomstnot.** Under passagen låg **hela Riksarkivets katalog- och
specialsöksgränssnitt bakom ALTCHA** — `/arkiv/<id>`, `/nad`,
`/bouppteckningar`, `/dodregister` och `mantalslangder-stockholms-stad` med
frågeparametrar omdirigerades alla till `/captcha`, medan samma sessions
IIIF-anrop svarade `200`. Volymgruppen kunde därför kartläggas bara genom
Riksarkivets MCP-metadatasökning och genom att hämta manifestetiketter
batch för batch. Agenten löste ingen captcha.

## Stödda påståenden

A-3615 (P-0336).
