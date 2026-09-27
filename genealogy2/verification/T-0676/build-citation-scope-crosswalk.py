"""Read-only crosswalk of G024 frozen citation scope and its 50 native records."""

import glob
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
scope = json.loads((HERE / "scope.json").read_text())
citations = scope["members"]["citations"]
assert len(citations) == 13 and len(scope["records"]) == 50

notes = {
    "C-0904": {
        "covered_subscope": "En egen SvenskaGravar-post för Ivar Gunnar Emanuel Höök i Floby, FLP330 (R40).",
        "outside_or_other_primary": "C-0903:s Lidingöbok och äldre gravar.se-täckningsbedömning är refererade jämförelser, inte egna original inom denna citation. Posten har ingen medgravsatt i den frysta texten; senare daterade kortfångster är separata evidenslager.",
        "disposition": "En registerpost i G024; jämförelse- och åtkomsthistorik hålls separat.",
    },
    "C-0907": {
        "covered_subscope": "Ytterhiske nr2, Umeå landsförsamling AIIa/23 uppslag2284 r12–23, hela egna hushållsposten på 00206295_00175 (R10), inklusive senare append-only läsrättelser.",
        "outside_or_other_primary": "Nollpåståenden för föregående volym AIIa/15 bild00206287_00164 samt omkringliggande uppslag2280–2283/2285–2328 är inte egna R i de50. Degerfors födelsebok1888, uppslag2088 och Örebro-/Lommakällor är framtida eller andra källors primärposter; citationen refererar dem utan att täcka dem här.",
        "disposition": "Egen uppslag2284-post täckt; historiska noll-/källvägspåståenden och andra originals omfång särskiljs.",
    },
    "C-0908": {
        "covered_subscope": "Sex separata inflyttningsposter nr208–213 på Umeå landsförsamling BI/11 s53, en R per post (R1,2,11,16,34,43), samma bild00206349_00056.",
        "outside_or_other_primary": "Degerfors reciproka utflyttning C-0890, Umeå hushållsuppslag2284 C-0907 och döttrarnas tidigare separata ankomster är andra primära postomfång. Räkningen 2M/3K på post208 är en postuppgift, inte sex oberoende källor.",
        "disposition": "Alla sex av citationens egna registerposter täckta; korshänvisningar separata.",
    },
    "C-0909": {
        "covered_subscope": "Floda AIIa/11 Ökna fol608, Ada r9 (R17) och Ada/Arne r15–16 (R15), samma bild00154078_00201; fulla54 fält och rättad personbunden flyttgräns genom j177–178.",
        "outside_or_other_primary": "Flen914 är C-0910:s egen primärpost. Frysta citationens påstående att båda utflyttade 1918-10-28 och r16:s gamla flyttditton är historiskt överspelat: bara Adas egen Floda-rad anger utflyttning; Arnes egen Flen-ankomst består. Familjeminnets faktiska omsorg är annan röst.",
        "disposition": "Båda egna Flodaposter täckta; den gamla gemensamma utflyttningsslutsatsen får inte ärvas.",
    },
    "C-0910": {
        "covered_subscope": "AIIa/4b ortregisterbild00153993_00004 (R3) och AIIa/4c fol914 övre r1–8 (R45), Torvald r9–12 (R49), Ture r15–17 (R26), Johan/Astrid r24–26 (R25). Fyra hushålls-R delar bild00153994_00100.",
        "outside_or_other_primary": "C-0911:s tidigare hushåll, lysningsbok30/1918, fol601 och andra uppslag är andra original. Grannrader utanför avgränsade grupper normaliseras inte. Den äldre avskriftens r5 födelsedag, r4 yrke, r8 namn/datum, r9 m.fl. och slutsatser om faktisk omsorg/vigsel är historiska lager, inte nuvarande källstatus.",
        "disposition": "Båda egna bilder och alla i citationen senare utpekade familjerader har avgränsade R; källkedjor och äldre felslut särskiljs.",
    },
    "C-0912": {
        "covered_subscope": "Floda AIIa/11 Ökna fol592 på bild00154078_00185: r1–2 (R47), r5 (R12), r11 (R4), r12 Bernhard (R28); fyra avgränsade R på samma bild.",
        "outside_or_other_primary": "Rad14–18 sägs uttryckligen vara annat hushåll och normaliseras inte. Värsås C-0917, Oskarshamn C-0915, tidigare bok C-0913, fotot/familjekrönikan och födelseoriginal är andra källors omfång. Ökna1914 eller faktisk vistelse före bokförd ankomst 1916 bevisas inte av denna rad.",
        "disposition": "Citerade egna rader täckta; övriga personer, kedjor och familjeminne separat.",
    },
    "C-0914": {
        "covered_subscope": "Oskarshamn EI/4 s231 inskrivning35 för Eliasson–Nilsson (R8), bild00001074_00234, samtliga13 tryckta kolumner inklusive senare rättade förrättar-/bevisfält.",
        "outside_or_other_primary": "Församlingsboksuppslag1208/115 hör till andra poster (C-0915 respektive ej denna R). Växiö i förrättaruppgift är inte verifierad fysisk vigselort, och äldre kyrkoformulering var inte egen råkolumn. Sidans andra inskrivningar omfattas inte.",
        "disposition": "En egen inskrivning täckt; plats-/formslutsatser behåller godkända reservationer.",
    },
    "C-0915": {
        "covered_subscope": "Oskarshamn AIIa/6 uppslag1208 Bernhards egen rad1 (R38), bild00001019_00062, med följdprövade yrkes-, militär-, attest- och flyttfält.",
        "outside_or_other_primary": "Rader2–11 sägs vara andra hushåll och normaliseras inte. Vigselbokens post35 C-0914 och Floda-bokens egen avresa C-0912 är separata primärposter; samma datum gör dem inte automatiskt oberoende vittnen för varje detalj.",
        "disposition": "Bernhards egen rad täckt; andra rader och reciprok kedja avgränsas.",
    },
    "C-0916": {
        "covered_subscope": "Umeå stad AIIa/5e fol1839 bild00206417_00013: huvudfamilj r1–8 (R33), Anders r9 (R5), Petrus/Anna r10–11 (R41), Johan/Sigrid r13–14 (R21), Johan Holger r23 (R30), Gustav r24 (R46), Sixten r25 (R6). Sju R delar samma bild och omfattar senare append-only läsrättelser, inklusive r1:s 1258-råform.",
        "outside_or_other_primary": "Barnrader12 och15–18 är uttryckligen utelämnade i citationen; övriga grannrader ingår inte i de sju egna R. Fastighetsregister AIIb/14 s11–12 bild00178898_00302 hör till C-0981/G026, inte till R33. Uppslag1704/1840, dödbok och externa vigsel-/lagfartsakter är källvägar, inte lästa genom fol1839.",
        "disposition": "Fol1839:s citerade rader täckta; fastighetsregister och övriga original inte absorberade av R33.",
    },
    "C-0917": {
        "covered_subscope": "Värsås AIIa/2 Djursätra fol134 bild00073285_00141: familjer1–9 (R22), Karl Adolf r23 (R24), Anna Vilhelmina r24 (R31). Senare rättelser för föräldradatum, värnpliktsradbindning och Bernhards flyttdag hör till dessa egna rader.",
        "outside_or_other_primary": "Ortregisterbild00073285_00003 användes som lokalisering och är media-proveniens i G012, inte en av de tre R. Fol132–135 utanför fol134, Agnes senare fol162, egen födelse-/vigselbok och Floda592 är skilda primärposter. Rader10–22 anges tomma.",
        "disposition": "Alla positiva egna fol134-rader i fryst citation täckta; ortregister och senare poster separat.",
    },
    "C-0918": {
        "covered_subscope": "Flen B/6b s20 post106 för Ada, betyg/utflyttning29 oktober1918 (R44), bild00154039_00023.",
        "outside_or_other_primary": "Grannpost105 anges uttryckligen gälla Lundqvist. Flen914 C-0910, Norges senare källor och födelseuppgift1922 är separata. Postens 1921-anteckning är reserverad och daterar inte Maj-Britts födelse eller specifikt ärende; bokföringsdag är inte fysisk resdag.",
        "disposition": "En egen utflyttningspost täckt; grannpost och senare familje-/Norgekedja separata.",
    },
    "C-0923": {
        "covered_subscope": "Fyra namngivna SvenskaGravar-kort: Arne (R19), Maj (R20), Axel (R42), Hulda (R13), var sitt register-R utan äldre lokalt kort-URL/hash.",
        "outside_or_other_primary": "Tre daterade nollsökningar för Ada (två namnformer) och Bernhard är inte dessa fyra gravposter och ingår inte i någon av de50 R. Senare kortfångster är nya bevarade kopior, inte den saknade exakta 2026-09-06-kopian. Hemort/gravplats anger inte dödsort, obrutet boende eller civilstånd.",
        "disposition": "Fyra positiva registerposter täckta; historiska nollsökningar och kopieproveniens separata.",
    },
    "C-0981": {
        "covered_subscope": "Endast C-0916:s fol1839 r1-råform och rättelsehistorik 1258/1268 korsbinder till G024 R33. Denna R täcker samma C-0916-bild00206417_00013, inte fastighetsregistret.",
        "outside_or_other_primary": "C-0981:s HUVUDORIGINAL är AIIb/14 stadsägeregister s11–12 bild00178898_00302: två befintliga native R-e445f96b83125c478c8b1af8 (1269) och R-fa685dc0f1a3a1defbd354ae (sex nummer), primärt G026/T-0701 READY, utanför de50 och utan lokal media. C-0971/C-0980:s serie-/nollpåståenden samt C-0981:s äldre slutsats att fastighetsblad saknas/serien är uttömd är historiska bedömningar, inte verifierade av R33 eller av ny G024-kontroll. T-0154 återtar påståendet att femman var en sexa: råtexten i C-0916 är 1258, registerträff1268 en möjlig saklig koppling, inte säker avskriftsrättelse.",
        "disposition": "SPLIT_REQUIRED: endast fol1839-delen inom G024; registerhuvudposterna ägs G026/T-0701 och nollslutsatserna kräver egen prövning. Får inte märkas helgranskad av R33.",
    },
}
assert set(notes) == set(citations)
rows = []
mapped = set()
for cid in citations:
    matches = glob.glob(str(ROOT / "genealogy/citations" / f"{cid}-*.md"))
    assert len(matches) == 1
    file = Path(matches[0])
    body = file.read_text()
    linked = [record for record in scope["records"] if any(cid in origin["document_path"] for origin in record["origins"])]
    mapped.update(r["record"] for r in linked)
    rows.append({"citation": cid, "frozenText": str(file.relative_to(ROOT)), "frozenTextSha256": hashlib.sha256(file.read_bytes()).hexdigest(),
                 "readLines": len(body.splitlines()),
                 "G024RecordNumbers": [r["number"] for r in linked], "G024RecordIds": [r["record"] for r in linked],
                 **notes[cid]})
assert len(mapped) == 36
other = [r for r in scope["records"] if r["record"] not in mapped]
assert len(other) == 14
assert {Path(o["document_path"]).name[:6] for r in other for o in r["origins"]} == {"C-0944", "C-0945"}
report = {"task": "T-0676", "mode": "READ_ONLY_CITATION_SCOPE_CROSSWALK", "date": "2026-09-24",
          "scopeManifest": str((HERE / "scope.json").relative_to(ROOT)), "scopeManifestSha256": hashlib.sha256((HERE / "scope.json").read_bytes()).hexdigest(),
          "frozenCitationCount": 13, "totalG024Records": 50, "uniqueG024RecordsLinkedFrom13C": 36,
          "citationToRecordLinks": sum(len(r["G024RecordIds"]) for r in rows),
          "duplicateCrossCitationRecord": "R-ac9bd9bbd4cf62fd811703f3 appears under both C-0916 and C-0981 for the same fol1839 source line, not two independent originals",
          "otherFourteenG024Records": [{"number": r["number"], "record": r["record"], "originCitationIds": sorted({Path(o["document_path"]).name[:6] for o in r["origins"]})} for r in other],
          "otherFourteenPrimaryCitationOwner": "C-0944/C-0945 belong to G023 whole-citation scope; G024 contains fourteen crossed grave records but not these citations as whole members",
          "citations": rows,
          "decisionBoundary": "This crosswalk does not mark any whole citation DONE or infer source review from record presence. Root Astra decides dispositions, especially C-0981 and historical zero claims.",
          "canonicalApply": False, "wotanChange": False, "newOriginalOpened": False}
out = HERE / "citation-scope-crosswalk-20260924.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"file": str(out.relative_to(ROOT)), "sha256": hashlib.sha256(out.read_bytes()).hexdigest(), "citations": len(rows), "G024Records": len(mapped), "crossG023Records": len(other)}, ensure_ascii=False))
