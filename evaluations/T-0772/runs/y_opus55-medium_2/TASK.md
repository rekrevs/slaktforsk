# Y – individuell följdprövning
Läs input.json. Gör ett enda självständigt försök. Bedöm samtliga 16 objekt
mot den givna nya evidensen, inga externa källor behövs. Ändra ingen databas.
Returnera JSON i answer.json med exakt denna struktur:
{"decisions":[{"id":"O1","action":"revise|retain|historical|irrelevant","rationale":"egen saklig motivering","replacement":"ny saktext eller null","evidence":["R1@2"],"resolve":"q1 eller null"}],"followups":["avgränsat nästa källsteg"],"canonical_changes":{"persons":[],"relations":[],"owner_confirmed":[]}}.
Välj en action, inte strängen med alternativen. revise behöver replacement.
retain gäller aktuella sakligt bestående objekt; historical gäller uttrycklig
historik; irrelevant gäller en orelaterad träff. Evidence listar bara relevant
underlag för beslutet, inte alla förekommande identifierare.
Inga nya statusgodkännanden eller datumfastställanden utöver underlaget.
