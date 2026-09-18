#!/usr/bin/env python
"""Build the complete-tree and complete-catalogue version-4 family edition."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
EDITION_PATH = ROOT / "genealogy/editions/adam-axel-depth5-v4.json"
CONTENT_PATH = ROOT / "genealogy/editions/adam-axel-depth5-v2.json"
PROJECT_DATA_PATH = ROOT / "dashboard/public/data/project.json"
DEFAULT_PDF = ROOT / "output/pdf/adam-och-axel-janson-fem-generationer-v4.pdf"
TMP_DIR = ROOT / "tmp/pdfs/family-edition-v4"


def load_v3_module():
    path = ROOT / "scripts/build-family-edition-v3.py"
    spec = importlib.util.spec_from_file_location("family_edition_v3_for_v4", path)
    if not spec or not spec.loader:
        raise RuntimeError("Could not load version-3 edition helpers")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V3 = load_v3_module()
BASE_BEGIN_PAGE = V3.begin_page

KNOWN_RELATION_STATUSES = {
    "CORROBORATED", "TRANSCRIBED", "OWNER_CONFIRMED", "CONFIRMED", "VERIFIED"
}


def clean(value: object) -> str:
    return V3.clean(value)


def esc(value: object) -> str:
    return V3.esc(value)


def footer(c: canvas.Canvas, page_no: int, section: str, size) -> None:
    width, _ = size
    V3.rule(c, V3.MARGIN_X, 13 * mm, width - V3.MARGIN_X, 0.35, V3.PALE)
    c.setFillColor(V3.MID)
    c.setFont("Arial", 6.1)
    c.drawString(V3.MARGIN_X, V3.FOOTER_Y, "ADAM & AXEL JANSON  |  PRIVAT FAMILJEUTGÅVA  |  VERSION 4")
    c.drawCentredString(width / 2, V3.FOOTER_Y, clean(section).upper())
    c.setFont("Arial-Bold", 6.5)
    c.drawRightString(width - V3.MARGIN_X, V3.FOOTER_Y, str(page_no))


def begin_page(c: canvas.Canvas, page_no: int, section: str, title: str, intro: str = "", size=A4) -> float:
    if section == "Plats" and page_no == 11:
        page_no = 38
    elif section == "Tid och forskningsfront" and page_no == 12:
        page_no = 39
    return BASE_BEGIN_PAGE(c, page_no, section, title, intro, size)


def tree_positions(edition: dict, content: dict, side: str) -> list[dict]:
    near = [dict(item, branch=side) for item in edition["near_tree_positions"][side]]
    depth_five = [
        {
            "person_id": item["person_id"],
            "depth": 5,
            "name": item["name"],
            "life": item["life"],
            "place": item["place"],
            "branch": side,
        }
        for item in content["depth5_positions"]
        if item["branch"] == side
    ]
    result = near + depth_five
    expected = [1, 2, 4, 8, 16]
    counts = [sum(item["depth"] == depth for item in result) for depth in range(1, 6)]
    if counts != expected:
        raise ValueError(f"Unexpected {side} tree shape: {counts}")
    if len({item["person_id"] for item in result}) != 31:
        raise ValueError(f"Duplicate person in {side} tree")
    return result


def draw_cover(c: canvas.Canvas, content: dict) -> None:
    width, height = A4
    c.setPageSize(A4)
    c.setFillColor(V3.WHITE)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setFillColor(V3.MID)
    c.setFont("Arial-Bold", 7)
    c.drawString(V3.MARGIN_X, height - 18 * mm, "EN KÄLLSTYRD FAMILJEBERÄTTELSE")
    c.setFillColor(V3.INK)
    c.setFont("Georgia-Bold", 31)
    c.drawString(V3.MARGIN_X, height - 42 * mm, "Adam & Axel Janson")
    c.setFont("Georgia", 17)
    c.drawString(V3.MARGIN_X, height - 55 * mm, "fem generationer bakåt")
    V3.rule(c, V3.MARGIN_X, height - 66 * mm, width - V3.MARGIN_X, 0.9, V3.INK)

    y = height - 79 * mm
    y = V3.paragraph(
        c,
        "<b>62 personer i två sammanhängande släktträd.</b> Varje trädruta visar namn, "
        "kända levnadsår och en relevant ort. Samtliga personer får därefter en egen "
        "post i den kompletta personkatalogen.",
        V3.MARGIN_X,
        y,
        width - 2 * V3.MARGIN_X,
        V3.pstyle("v4-cover-lead", font="Georgia", size=11.2, leading=15),
    ) - 17
    c.setFont("Arial-Bold", 7)
    c.drawString(V3.MARGIN_X, y, "INNEHÅLL")
    y -= 13
    items = [
        ("2", "Läsnyckel och redaktionell princip"),
        ("3-4", "Två kompletta femgenerations-träd"),
        ("5-35", "Komplett personkatalog, två personer per sida"),
        ("36-37", "Fyra familjeberättelser"),
        ("38-39", "Platser, tidslinje, konflikter och fronter"),
        ("40-41", "Två källor i närbild"),
        ("42-43", "Exakta hänvisningar"),
    ]
    for pages, label in items:
        c.setFont("Arial-Bold", 8)
        c.drawString(V3.MARGIN_X, y, pages)
        c.setFont("Arial", 8)
        c.drawString(V3.MARGIN_X + 38, y, clean(label))
        y -= 17
    V3.rule(c, V3.MARGIN_X, y - 4, width - V3.MARGIN_X, 0.35, V3.PALE)
    y -= 24
    V3.paragraph(
        c,
        "<b>Version 4.</b> Person-ID och namngivna familjerelationer finns i katalogen, "
        "där de kan läsas i sitt sammanhang. Träden reserverar den knappa ytan för namn, "
        "år och ort. Version 1-3 är bevarade oförändrade.",
        V3.MARGIN_X,
        y,
        width - 2 * V3.MARGIN_X,
        V3.pstyle("v4-cover-protocol", size=8.1, leading=11.2),
    )
    c.setFillColor(V3.MID)
    c.setFont("Arial", 6.5)
    c.drawString(V3.MARGIN_X, 18 * mm, "VERSION 4  |  4 SEPTEMBER 2026  |  PRIVAT FAMILJEBRUK")
    c.drawRightString(width - V3.MARGIN_X, 18 * mm, "PCD-2026-09-04-005")


def draw_orientation(c: canvas.Canvas) -> None:
    y = begin_page(
        c,
        2,
        "Orientering",
        "Så läses träd och personkatalog",
        "Version 4 gör översikten mänskligare i träden och flyttar den detaljerade spårbarheten till en komplett katalog.",
    )
    page_w, _ = A4
    gap = 18
    col_w = (page_w - 2 * V3.MARGIN_X - gap) / 2
    left_x, right_x = V3.MARGIN_X, V3.MARGIN_X + col_w + gap

    c.setFont("Georgia-Bold", 11.5)
    c.drawString(left_x, y, "I träden")
    left_items = [
        ("Namn", "är alltid den största och första uppgiften i rutan."),
        ("År", "visar födelse- och dödsår när de är tillräckligt kända; ett öppet slutstreck betyder att säkert dödsår saknas."),
        ("Ort", "är en relevant livs-, födelse- eller familjeort, inte alltid en exakt adress."),
        ("Linjer", "leder från barn till far överst och mor underst."),
    ]
    yy = y - 20
    for label, body in left_items:
        yy = V3.paragraph(c, f"<b>{esc(label)}.</b> {esc(body)}", left_x, yy, col_w,
                          V3.pstyle(f"v4-left-{label}", size=7.6, leading=10.0)) - 10
    V3.rule(c, left_x, yy, left_x + col_w, 0.35, V3.PALE)
    yy -= 18
    c.setFont("Georgia-Bold", 11.5)
    c.drawString(left_x, yy, "I katalogen")
    yy -= 18
    V3.fit_paragraph(
        c,
        "Varje person får person-ID, trädposition, år, ort, kända föräldrar, partner och barn "
        "med både namn och ID. Därefter följer en redaktionellt sammanställd uppsättning "
        "källstödda livsuppgifter. C-numren leder till projektets fullständiga citationsakter.",
        left_x,
        yy,
        col_w,
        125,
        start=7.6,
        minimum=7.0,
        leading_factor=1.3,
    )

    c.setFont("Georgia-Bold", 11.5)
    c.drawString(right_x, y, "Vad komplett betyder här")
    right_items = [
        ("62 av 62", "Alla personer som är egna rutor i de två träden har en katalogpost."),
        ("Kända relationer", "Osäkra LEAD-, CONFLICT-, REJECTED- och UNKNOWN-relationer visas inte som familjefakta."),
        ("Känd information", "Identitet, tid, geografi, familj och de mest relevanta livsuppgifterna sammanställs; full akttext ligger kvar i projektarkivet."),
        ("Okänt förblir okänt", "Saknat dödsår, förälder eller ort fylls inte ut genom gissning."),
        ("Privat familjebruk", "För nu levande personer begränsas texten till den familjehistoriskt nödvändiga nivån."),
    ]
    yy = y - 20
    for label, body in right_items:
        yy = V3.paragraph(c, f"<b>{esc(label)}.</b> {esc(body)}", right_x, yy, col_w,
                          V3.pstyle(f"v4-right-{label}", size=7.5, leading=9.8)) - 9
    V3.rule(c, right_x, yy, right_x + col_w, 0.35, V3.PALE)
    yy -= 18
    V3.fit_paragraph(
        c,
        "<b>Redaktionellt beslut.</b> PCD-2026-09-04-005. Version 4 ändrar presentationen "
        "och katalogens täckning, inte vilka osäkra relationer som får ingå i släktträdet.",
        right_x,
        yy,
        col_w,
        90,
        start=7.4,
        minimum=6.9,
        leading_factor=1.28,
    )


def draw_tree_node(c: canvas.Canvas, item: dict, x: float, centre: float, w: float, h: float, leaf: bool) -> None:
    c.setFillColor(V3.WHITE)
    c.setStrokeColor(V3.LIGHT if leaf else V3.MID)
    c.setLineWidth(0.4 if leaf else 0.55)
    c.rect(x, centre - h / 2, w, h, fill=1, stroke=1)
    bottom = centre - h / 2
    top = centre + h / 2 - 2.3
    name_size = 5.4 if leaf else 6.25
    name_min = 4.5 if leaf else 5.0
    V3.fit_paragraph(
        c,
        esc(item["name"]),
        x + 3,
        top,
        w - 6,
        h - 12.2,
        font="Arial-Bold",
        start=name_size,
        minimum=name_min,
        leading_factor=1.02,
        align=TA_CENTER,
    )
    c.setFillColor(V3.MID)
    c.setFont("Arial-Bold", 4.35 if leaf else 4.6)
    c.drawCentredString(x + w / 2, bottom + 6.4, clean(item["life"]))
    c.setFont("Arial", 3.95 if leaf else 4.25)
    c.drawCentredString(x + w / 2, bottom + 2.0, clean(item["place"]))


def draw_tree(c: canvas.Canvas, page_no: int, side: str, positions: list[dict]) -> None:
    title = f"Adam och Axel via {side}"
    intro = (
        "Fem generationer bakåt. Läs från vänster till höger: varje person förgrenas till far överst och mor underst. "
        "Varje ruta prioriterar namn, kända levnadsår och en relevant ort; person-ID och källor finns i katalogen."
    )
    begin_page(c, page_no, "Sammanhängande släktträd", title, intro, V3.LANDSCAPE)
    xs = [36, 187, 338, 489, 640]
    widths = [123, 123, 123, 123, 166]
    heights = [40, 36, 32, 28, 23.5]
    generations = [[item for item in positions if item["depth"] == depth] for depth in range(1, 6)]

    c.setStrokeColor(V3.LIGHT)
    c.setLineWidth(0.45)
    for depth in range(1, 5):
        child_centres = V3.tree_centres(depth)
        parent_centres = V3.tree_centres(depth + 1)
        x1 = xs[depth - 1] + widths[depth - 1]
        x2 = xs[depth]
        mid_x = (x1 + x2) / 2
        for index, child_y in enumerate(child_centres):
            upper, lower = parent_centres[index * 2:index * 2 + 2]
            c.line(x1, child_y, mid_x, child_y)
            c.line(mid_x, upper, mid_x, lower)
            c.line(mid_x, upper, x2, upper)
            c.line(mid_x, lower, x2, lower)

    for depth, items in enumerate(generations, 1):
        for item, centre in zip(items, V3.tree_centres(depth)):
            draw_tree_node(c, item, xs[depth - 1], centre, widths[depth - 1], heights[depth - 1], depth == 5)

    c.setFillColor(V3.MID)
    c.setFont("Arial", 5.7)
    for depth, x in enumerate(xs, 1):
        c.drawCentredString(x + widths[depth - 1] / 2, 460, f"DJUP {depth}")


def relation_kind(relation: str) -> str | None:
    value = clean(relation).lower().strip()
    if re.match(r"^(far|mor)(?:\b|\s)", value):
        return "parent"
    if re.match(r"^(son|dotter)(?:\b|\s)", value):
        return "child"
    if re.match(r"^(make|maka|hustru|partner)(?:\b|\s)", value) or value.startswith("gift"):
        return "partner"
    return None


def display_name(person: dict) -> str:
    return re.sub(r"\s+\(\d{4}[^)]*\)$", "", clean(person["name"])).strip()


def named_ref(person: dict) -> str:
    return f"{display_name(person)} ({person['id']})"


def known_relations(people: dict[str, dict], person_id: str) -> dict[str, list[dict]]:
    result: dict[str, dict[str, dict]] = {"parent": {}, "partner": {}, "child": {}}

    def add(kind: str, target_id: str) -> None:
        if target_id in people and target_id != person_id:
            result[kind][target_id] = people[target_id]

    for source_id, source in people.items():
        for relation in source.get("relations", []):
            if relation.get("status") not in KNOWN_RELATION_STATUSES:
                continue
            target_id = relation.get("target")
            kind = relation_kind(relation.get("relation", ""))
            if not kind or target_id not in people:
                continue
            if source_id == person_id:
                add(kind, target_id)
            elif target_id == person_id and kind != "partner":
                inverse = {"parent": "child", "child": "parent"}[kind]
                add(inverse, source_id)
    return {kind: list(items.values()) for kind, items in result.items()}


def claim_category(statement: str) -> str:
    value = clean(statement).lower()
    if any(word in value for word in ("föräldrar", "far till", "mor till", "dotter till", "son till")):
        return "relation"
    if "född" in value or "födelse" in value:
        return "birth"
    if any(word in value for word in ("dog", "avled", "död", "begrav")):
        return "death"
    if any(word in value for word in ("arbet", "yrke", "bonde", "torpare", "hemmans", "dräng", "smed", "lärare", "missionär", "järnväg")):
        return "work"
    if any(word in value for word in ("flytt", "bodde", "bosatt", "hushåll", "hemvist")):
        return "place"
    if any(word in value for word in ("gift", "vigdes", "hustru", "make")):
        return "family"
    return "other"


def claim_score(claim: dict) -> tuple[int, str]:
    statement = clean(claim.get("statement", "")).lower()
    score = {"birth": 12, "death": 11, "work": 9, "place": 8, "family": 7, "other": 4, "relation": 2}[claim_category(statement)]
    if claim.get("status") == "CORROBORATED":
        score += 4
    elif claim.get("status") == "OWNER_CONFIRMED":
        score += 3
    elif claim.get("status") == "CONFLICT":
        score -= 1
    if claim.get("citations"):
        score += 2
    return score, claim.get("id", "")


def safe_private_statement(statement: str) -> str:
    return re.sub(r"\b(\d{4})-\d{2}-\d{2}\b", r"\1", clean(statement))


def selected_claims(person: dict) -> list[dict]:
    allowed = {"CORROBORATED", "TRANSCRIBED", "OWNER_CONFIRMED", "CONFLICT"}
    claims = [claim for claim in person.get("claims", []) if claim.get("status") in allowed]
    ordered = sorted(claims, key=claim_score, reverse=True)
    selected: list[dict] = []
    used_categories: set[str] = set()
    limit = 3 if person.get("private") else 5

    for claim in ordered:
        category = claim_category(claim.get("statement", ""))
        if category == "relation":
            continue
        if category not in used_categories:
            selected.append(claim)
            used_categories.add(category)
        if len(selected) >= limit:
            break

    if len(selected) < limit:
        for claim in ordered:
            if claim not in selected and claim_category(claim.get("statement", "")) != "relation":
                selected.append(claim)
            if len(selected) >= limit:
                break

    if not selected and claims:
        selected = claims[:limit]
    return selected


def first_sentence(value: str) -> str:
    return V3.V2.first_sentence(value)


def relationship_line(label: str, people: list[dict]) -> str:
    if not people:
        value = "inte säkert identifierade i projektet"
    else:
        value = "; ".join(named_ref(person) for person in people)
    return f"<b>{esc(label)}:</b> {esc(value)}"


def draw_catalogue_entry(c: canvas.Canvas, item: dict, person: dict, people: dict[str, dict], top: float, height: float) -> None:
    page_w, _ = A4
    x = V3.MARGIN_X
    width = page_w - 2 * V3.MARGIN_X
    bottom = top - height
    relations = known_relations(people, item["person_id"])

    c.setFillColor(V3.MID)
    c.setFont("Arial-Bold", 6.0)
    c.drawString(x, top - 7, clean(item["person_id"]))
    c.drawRightString(x + width, top - 7, clean(f"{item['branch']}s sida | djup {item['depth']}"))
    name_top = top - 18
    name_h = V3.fit_paragraph(c, esc(item["name"]), x, name_top, width, 28,
                              font="Georgia-Bold", start=12.2, minimum=10.5, leading_factor=1.08)
    meta_top = name_top - name_h - 3
    meta_h = V3.fit_paragraph(c, esc(f"{item['life']} | {item['place']}"), x, meta_top, width, 18,
                              font="Arial-Bold", start=7.0, minimum=6.4, leading_factor=1.1, color=V3.MID)
    yy = meta_top - meta_h - 8

    relation_texts = [
        relationship_line("Föräldrar", relations["parent"]),
        relationship_line("Partner", relations["partner"]),
        relationship_line("Barn", relations["child"]),
    ]
    for index, relation_text in enumerate(relation_texts):
        used = V3.fit_paragraph(c, relation_text, x, yy, width, 34,
                                start=6.45, minimum=5.7, leading_factor=1.18)
        yy -= used + 3

    yy -= 10
    c.setFillColor(V3.INK)
    c.setFont("Georgia-Bold", 8.6)
    c.drawString(x, yy, "Känd information")
    yy -= 12
    citations: list[str] = []
    for claim in selected_claims(person):
        statement = first_sentence(claim.get("statement", ""))
        if person.get("private"):
            statement = safe_private_statement(statement)
        claim_citations = [cid for cid in claim.get("citations", []) if cid]
        for cid in claim_citations:
            if cid not in citations:
                citations.append(cid)
        suffix = f" [{', '.join(claim_citations[:3])}]" if claim_citations else ""
        prefix = "Källkonflikt: " if claim.get("status") == "CONFLICT" else ""
        fact = f"• {prefix}{statement}{suffix}"
        used = V3.fit_paragraph(c, esc(fact), x + 3, yy, width - 6, 43,
                                start=6.55, minimum=5.8, leading_factor=1.2)
        yy -= used + 3

    c.setFillColor(V3.MID)
    c.setFont("Arial", 5.35)
    source_text = "Citationsakter: " + (", ".join(citations) if citations else "inga separata C-referenser i de valda kataloguppgifterna")
    V3.fit_paragraph(c, esc(source_text), x, bottom + 14, width, 18,
                     start=5.35, minimum=4.9, leading_factor=1.1, color=V3.MID)
    V3.rule(c, x, bottom + 4, x + width, 0.45, V3.LIGHT)
    if yy < bottom + 34:
        raise ValueError(f"Catalogue entry overflow for {item['person_id']}: {yy:.1f} < {bottom + 34:.1f}")


def draw_catalogue_page(c: canvas.Canvas, page_no: int, items: list[dict], people: dict[str, dict], part: int, total: int) -> None:
    y = begin_page(
        c,
        page_no,
        "Komplett personkatalog",
        f"Personkatalog {part} av {total}",
        "Alla personer följer trädordningen. Namngivna relationer visar både person och projektets stabila person-ID; C-numren leder till den fulla källredovisningen.",
    )
    available_bottom = 48
    gap = 10
    entry_h = (y - available_bottom - gap) / 2
    for index, item in enumerate(items):
        top = y - index * (entry_h + gap)
        draw_catalogue_entry(c, item, people[item["person_id"]], people, top, entry_h)


def draw_references(c: canvas.Canvas, page_no: int, ids: list[str], part: int, final: bool = False) -> None:
    y = begin_page(
        c,
        page_no,
        "Verifiera själv",
        f"Exakta hänvisningar - {part}",
        "Varje C-nummer leder till en full citationsakt med källställe, avskrift, identitetsbedömning och lokalt material där det finns.",
    )
    page_w, _ = A4
    gap = 18
    col_w = (page_w - 2 * V3.MARGIN_X - gap) / 2
    per_col = (len(ids) + 1) // 2
    item_h = 78
    for index, citation_id in enumerate(ids):
        col = index // per_col
        row = index % per_col
        x = V3.MARGIN_X + col * (col_w + gap)
        top = y - row * item_h
        title, location = V3.citation_record(citation_id)
        title_h = V3.fit_paragraph(c, "<b>" + esc(title) + "</b>", x, top, col_w, 25,
                                   start=6.4, minimum=5.7, leading_factor=1.15)
        V3.fit_paragraph(c, esc(location), x, top - title_h - 4, col_w, 44,
                         start=5.5, minimum=4.8, leading_factor=1.17, color=V3.MID)
        V3.rule(c, x, top - 70, x + col_w, 0.3, V3.PALE)
    if final:
        c.setFillColor(V3.MID)
        c.setFont("Arial", 5.4)
        c.drawString(V3.MARGIN_X, 38, "Manifest: genealogy/editions/adam-axel-depth5-v4.json | Kunskapsläge: 2026-09-04")
        c.drawRightString(page_w - V3.MARGIN_X, 38, "Full proveniens och återstartvillkor finns i projektarkivet.")


def build(pdf_path: Path) -> None:
    V3.register_fonts()
    edition = json.loads(EDITION_PATH.read_text())
    content = json.loads(CONTENT_PATH.read_text())
    project = json.loads(PROJECT_DATA_PATH.read_text())
    people = {person["id"]: person for person in project["people"]}
    side_positions = {side: tree_positions(edition, content, side) for side in ("Sverker", "Kristina")}
    catalogue = side_positions["Sverker"] + side_positions["Kristina"]
    if len(catalogue) != 62 or len({item["person_id"] for item in catalogue}) != 62:
        raise ValueError("Version-4 catalogue does not resolve to 62 unique tree people")
    missing = [item["person_id"] for item in catalogue if item["person_id"] not in people]
    if missing:
        raise ValueError(f"Tree people missing from project data: {missing}")

    V3.EDITION_PATH = EDITION_PATH
    V3.CONTENT_PATH = CONTENT_PATH
    V3.PROJECT_DATA_PATH = PROJECT_DATA_PATH
    V3.TMP_DIR = TMP_DIR
    V3.footer = footer
    V3.begin_page = begin_page

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(pdf_path), pagesize=A4, pageCompression=1)
    c.setTitle(clean(edition["edition"]["title"]))
    c.setAuthor("Sverker Janson | källstyrt familjearkiv")
    c.setSubject("Komplett privat djup-5-utgåva för Adam och Axel Janson")
    c.setKeywords("släktforskning, Janson, Höök, familjehistoria, släktträd, personkatalog, djup 5")

    draw_cover(c, content); V3.end_page(c)
    draw_orientation(c); V3.end_page(c)
    draw_tree(c, 3, "Sverker", side_positions["Sverker"]); V3.end_page(c)
    draw_tree(c, 4, "Kristina", side_positions["Kristina"]); V3.end_page(c)

    catalogue_pages = (len(catalogue) + 1) // 2
    for part, start in enumerate(range(0, len(catalogue), 2), 1):
        draw_catalogue_page(c, 4 + part, catalogue[start:start + 2], people, part, catalogue_pages)
        V3.end_page(c)

    V3.draw_stories(c, 36, content["feature_stories"][:2], "Jord, torp och Västerbottens hushåll"); V3.end_page(c)
    V3.draw_stories(c, 37, content["feature_stories"][2:], "Järnvägen och Lagfors"); V3.end_page(c)
    V3.draw_map_page(c, content); V3.end_page(c)
    V3.draw_timeline_and_fronts(c, content); V3.end_page(c)
    for page_no, item in enumerate(content["source_close_readings"], 40):
        V3.draw_close_reading(c, page_no, item); V3.end_page(c)
    refs = content["reference_citations"]
    draw_references(c, 42, refs[:16], 1); V3.end_page(c)
    draw_references(c, 43, refs[16:], 2, final=True)
    c.save()
    print(pdf_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_PDF)
    args = parser.parse_args()
    build(args.output.resolve())


if __name__ == "__main__":
    main()
