# Granskningsunderlag för personkohorter

Detta beskriver en tillfällig, fryst migrationsleverans, inte en andra
redigerbar personmodell. Native-operationen och databasen äger resultatet.
Läs hela akten och profilen inklusive senare rättelser. Återanvänd det som
redan är tillräckligt undersökt; gör ingen ny arkivläsning.

Varje del är en JSON-lista med ett objekt per P-id:

```
{
  "person": "P-NNNN",
  "documents": [{"path": "genealogy/people/…", "sha256": "…"},
                {"path": "genealogy/research-profiles/…", "sha256": "…"}],
  "readingNote": "Vad genomläsningen visade, rättelser och aktuella gränser.",
  "changes": [ … ],
  "reuse": [{"object": "befintligt id", "origins": [ … ], "rationale": "…"}],
  "assertions": [{"id": "A-NNNN", "state": "mapped_complete|preserved_text|preserved_history|pending_interpretation",
                  "targets": ["mål-id"], "rationale": "…", "question": "…"}],
  "relations": [{"unit": "exakt befintligt unit.id", "state": "…", "targets": ["mål-id"], "rationale": "…", "question": "…"}],
  "pending": [{"origin": …, "question": "…"}]
}
```

`changes` använder den befintliga native-modellen: `id`, `kind`, `data`,
`disposition`, `evidenceStatus`, `rationale`, `caveat`, `origins`, `evidence`.
Importören sätter `expectedVersion` och bindningar. En avsiktlig revision av ett befintligt objekt kräver även `revises` med dess aktuella version; annars ska objektet återbrukas. Ursprungsreferenser är
antingen en sträng med exakt A-id/unit-id, eller
`{entity:"P-/C-id",kind:"person|profile|citation",startLine:1,endLine:2}`.
Belägg använder `{object:"R-/O-/ID-/…",role:"supports|contradicts|context|derived_from",note:"…"}`;
importören binder den faktiskt aktuella revisionen. Ett C-id är ingen R-post.
Välj de faktiskt relevanta posterna; koppla inte alla kontrollrader i en
citation till målpersonen. Ursprung i redan bedömd personkunskap får vara
primär migrationsgrund där finare källbindning ännu inte kan avgöras.

Varje aktuell A-rad och varje innehållsbärande relationsrad ska ha eget
utfall. Sammansatta rader kan ge flera typade objekt. `mapped_complete`
kräver att hela den sakliga innebörden inklusive förbehåll är representerad.
Bevarad text är tillåten för resonemang, historik och osäkra postgränser;
använd inte detta för att hoppa över klara viktiga personfakta. En kvarvarande
tolkningsfråga ska säga vad som inte är tolkat, inte bara "behöver granskas".
Förankra `pending.origin` i den granskade personens egen akt eller profil.
Om motuppgiften står i en citation, ange dess exakta hänvisning i frågan
och i sakobjektets `origins`. Personkohorten får inte tyst lämna bort ett
tolkningsbeslut därför att dess ankare ligger utanför dess dokumentomfång.

Typa uttryckliga personfakta, relevanta livshändelser och relationer med
rätt subjekt/riktning. Skilj källrapport från accepterad personslutsats,
osäker identitet från säker person men osäker födelse, och avvisad hypotes
från fortfarande giltigt avgränsat söknoll. En far får inte automatiskt
biologisk art. Kön kräver explicit uppgift, aldrig rollord/namn. Skapa inga
extra personer för kontrollrader. Behåll ägarkunskap och minimerade uppgifter.

Gemensamma relationer: förälder → barn, övriga symmetriska par sorteras.
Återbruka befintlig relation med samma par/typ när den redan finns. Annars
id `REL-parent-P-NNNN-P-NNNN`, `REL-spouse-P-NNNN-P-NNNN` eller
`REL-sibling-P-NNNN-P-NNNN`. Relationstyp sibling införs uttryckligen i
valideraren; den blir inte en föräldralänk. Andra typer rapporteras först.
Återanvänd pilotens id:n och skriv inte över dess kvalificerade innehåll.

Händelseid vid nya enkla livshändelser: `E-birth-P-NNNN`,
`E-baptism-P-NNNN`, `E-death-P-NNNN`, `E-burial-P-NNNN`.
Vigsel: `E-marriage-P-NNNN-P-NNNN-YYYY` med sorterat par. Namnge andra
händelser stabilt efter person och dokumenterat sammanhang. Deltagande har
`EP-<eventid>-<personid>-<role>`. Dopvittne är en deltagarroll vid ett bestämt
dop, inte en släktrelation. Om dopbarnet inte kan avgöras, bevara konkret fråga.
Ingen datering/plats/foliorad får fyllas ut genom gissning.

Nya vittnesdeltaganden använder `role: "witness"`; typen av händelse
anger om det gäller dop eller något annat. Inför inte ytterligare
synonymer som `baptism_witness`. Detta gäller den typade deltagarrollen;
omnämnandets ordagranna `role_literal` bevaras separat och normaliseras inte.

Övriga fakta har `F-<P-id>-<property>-<scope>` och explicit `value_type`.
Använd beskrivande gemensamma egenskaper som name_form, occupation,
education, residence, civil_status, military_registration, property_holding,
source_reference eller household_membership. Påståenden om källans
uttryck snarare än personens liv ska vara observationer när rätt R kan
avgränsas; annars en tydligt benämnd bevarad bedömning. Samma metadata
ska inte mekaniskt upprepas som flera oberoende fakta.

Ett omnämnandes `name_literal` kommer från en faktiskt utvunnen namnform
i den avgränsade posten, aldrig personens kanoniska visningsnamn som
standardvärde. Flera sakuppgifter om samma person på samma källrad delar
omnämnande och identitetslänk. Utan utvunnen namnform kan observationen ha
`mention_id: null` och sina exakta käll-/personursprung. Verkliga olika
anonyma personer, till exempel två vittnens namnlösa hustrur, förblir olika.
Samma person kan förekomma i flera R-poster inom en citation. Dessa får
skilda omnämnanden och observationer; ett id byggt enbart av C-id och namn
räcker då inte. Kontrollera faktisk `record_id` innan ett objekt återbrukas.
`role_literal` innehåller endast utvunnen rå rolltext. Om ingen separat
roll har utvunnits används tom sträng med uttryckligt förbehåll; `null`
är inte tillåtet. Kommentarer som ”utan prefix” hör till observation eller
förbehåll, inte till rårollen.

En observation återger endast den post som dess `record_id` avgränsar.
För inte in senare hushållsböckers datum, släktskapskorrelationer eller
projektets bedömningar i dess råvärden. Jämförelser mellan poster blir
`fact` eller `assessment` med uttryckliga belägg till de berörda posterna
eller observationerna. En hel relationsrad ur en akt är en sammanställning,
inte en avskrift ur den första citerade källan. Kontrollera denna gräns
särskilt när en rad återanvänds för flera familjemedlemmar. Tomt rånamn
för en namnlös källperson förklaras i förbehållet; en redaktionell
platshållare får inte presenteras som källans namn.

En kvalificerande sakuppgift om ett personpar kan ha relationens id som
`subject_id`. Exempelvis bevaras en tvillinginferens en gång som ett fakta
om syskonrelationen, med egen status och motivering. Båda personvyerna
visar den under samma relation utan kopior eller ny föräldraslutsats.

Importören överför dessutom profilens frågor, bedömningar, söknycklar,
teman, krav och källvägar samt aktens biografi som versionsbundna
forskningsobjekt med råtext och kriterier. De blir ingen exekveringskö.
Dessa ska inte handkopieras till `changes`. Rapportera motsägelser eller
senare överordnade rättelser så de inte normaliseras bort. P-id i en annan
grupp får refereras men motpartens hela dossier konverteras inte här.

Den samordnade råformen för nya odaterade relationer är
`{"precision":"unknown","literal":"Ingen säker datering av relationens början/slut."}`.
Använd `recorded_parent` respektive `recorded_sibling` för ospecificerad
källangiven art; exempelvis `paternal_sibling` när endast gemensam far är belagd.
Disposition och evidensstatus är skilda: en befintlig accepterad slutsats
kan ha `TRANSCRIBED` och uttryckliga förbehåll. Ett registerobjekts `recorded`
ska inte automatiskt spärra en sakligt accepterad personidentitet, men ingen
status höjs genom en generell regel. Bind inte kontraktsgodkännande till
personens existens eller till varje separat källidentitet.

Schema006 bevarar samtliga mål i `unit_decision_target`, även när objekten
återbrukas utan revision. En konkret tolkningsfråga får kvarstå samtidigt
som redan representerade deluppgifter fortfarande är nåbara. Personvyn
visar källobservationer i underlaget separat från personslutsatser; detta
kräver inte påhittade omnämnanden/identitetslänkar för att göra dem synliga.

Avvecklad forskning behöver ett uttryckligt `researchState` med
`disposition: "retired"`, `origins` och `rationale`. Då bevaras profilens
frågor, vägar och bedömningar med den dispositionen och ursprungligt
råutfall. Ett tidigare `ÖPPEN` återaktiverar inte frågan; personvyn ger
`active: false`. Personens existens och sakuppgifter avvisas inte därför
att forskning om personen avvecklats.

Native-sökningar använder `outcome: negative|positive|access_problem|inconclusive`.
Varje sökning kräver ett faktiskt `source_id`, en `body` som beskriver
utfallet och dess förbehåll, samt både `scope_json.description` och
`scope_json.query`. Inget obligatoriskt
källfält fylls genom gissning; underlaget måste identifiera källan.
Ett negativt resultat kräver `scope_json.bounds` som ett uttryckligt objekt
med den faktiskt lästa volymen, perioden och/eller postföljden; en fri
textsträng räcker inte. Behåll rå omfångsbeskrivning och förbehåll i övriga
fält. Ett historiserat felaktigt söknoll blir inte ett giltigt negativt
resultat genom formatkonvertering. `identity_resolution.decision` använder
`same_person|different_people|unresolved`; själva argumentet hör till
revisionens motivering och förbehåll, inte ett påhittat payloadfält.

## Gamla akter som inte representerar en egen person

Ett dubblettalias eller ett avvisat läsningsförslag får inte återuppstå som
person. Importen kräver ett redan infört `IMPORT-P-NNNN`-beslut, motsvarande
`same_identity` respektive `archival_reference`-mappning och uttrycklig
`researchState: {disposition: "retired", rationale: …, origins: […]}`.
Profilens automatobjekt och berättelse behåller den gamla aktens egna id:n,
men får importbeslutet som ämne. De blir historiska och läsbara via den gamla
aktens vy. Målpersonens aktuella profil och berättelse skrivs inte över.
Sakuppgifter återbrukas eller förs till sina verkliga ämnen efter individuell
bedömning. En läskontext är aldrig i sig ett identitetsalias.
