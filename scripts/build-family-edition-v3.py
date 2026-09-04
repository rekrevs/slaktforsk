#!/usr/bin/env python
"""Build the compact, monochrome Adam-and-Axel depth-5 family edition."""

from __future__ import annotations

import argparse
import html
import importlib.util
import json
import math
import subprocess
from copy import deepcopy
from pathlib import Path

from PIL import Image, ImageOps
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
EDITION_PATH = ROOT / "genealogy/editions/adam-axel-depth5-v3.json"
CONTENT_PATH = ROOT / "genealogy/editions/adam-axel-depth5-v2.json"
V1_MANIFEST_PATH = ROOT / "genealogy/editions/adam-axel-depth4-v1.json"
PROJECT_DATA_PATH = ROOT / "dashboard/public/data/project.json"
SWEDEN_PATH = ROOT / "genealogy/editions/assets/sweden-outline-natural-earth-5.1.1.geojson"
DEFAULT_PDF = ROOT / "output/pdf/adam-och-axel-janson-fem-generationer-v3.pdf"
TMP_DIR = ROOT / "tmp/pdfs/family-edition-v3"

PORTRAIT = A4
LANDSCAPE = landscape(A4)
INK = colors.HexColor("#111111")
MID = colors.HexColor("#555555")
LIGHT = colors.HexColor("#A8A8A8")
PALE = colors.HexColor("#D6D6D6")
WHITE = colors.white
MARGIN_X = 15 * mm
FOOTER_Y = 9 * mm

STATUS_LABELS = {
    "CORROBORATED": "SAMSTÄMMIGA BELÄGG",
    "TRANSCRIBED": "AVLÄST I KÄLLA",
    "OWNER_CONFIRMED": "SÄKER FAMILJEKUNSKAP",
    "CONFLICT": "ÖPPEN KÄLLKONFLIKT",
    "FRONT": "DOKUMENTERAD ARKIVFRONT",
}

TREE_NAMES = {
    "Sverker": [
        ["Sverker Adam Janson"],
        ["Jan-Christer Janson", "Hillevi Zingmark"],
        ["Arne Godvig Jansson", "Maj Amalia Ekholm", "Oskar Alfred Zingmark", "Ebba Alfrida Andersson"],
        ["Bernhard Eliasson", "Ada Jansson", "Axel Edvard Eriksson", "Hulda Ålund", "Johan Oskar Zingmark", "Ida Andersdotter", "Anders Alfred Andersson", "Anna Fredrika Jakobsdotter"],
    ],
    "Kristina": [
        ["Kristina Elisabeth Petronella Höök"],
        ["Gunnar Höök", "Evy Höök"],
        ["Anders Ivar Höök", "Anna Elisabeth Carlman", "Axel Edvin Henriksson", "Emma Petronella Eugenia Larsson"],
        ["Johannes Ivar Fredberg", "Anna Matilda Hök", "Johan Fredrik Villehad Carlman", "Elin Andersson", "Erik Jonas Henriksson", "Gertrud Jonsson", "Anders Niklas Larsson", "Ingrid Höglund"],
    ],
}


def load_v2_module():
    spec = importlib.util.spec_from_file_location("family_edition_v2", ROOT / "scripts/build-family-edition-v2.py")
    if not spec or not spec.loader:
        raise RuntimeError("Could not load version-2 edition helpers")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V2 = load_v2_module()


def clean(value: object) -> str:
    return (
        str(value or "")
        .replace("\u2010", "-")
        .replace("\u2011", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
    )


def esc(value: object) -> str:
    return html.escape(clean(value), quote=False).replace("\n", "<br/>")


def register_fonts() -> None:
    font_dir = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("Georgia", str(font_dir / "Georgia.ttf")))
    pdfmetrics.registerFont(TTFont("Georgia-Bold", str(font_dir / "Georgia Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Georgia-Italic", str(font_dir / "Georgia Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Arial", str(font_dir / "Arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(font_dir / "Arial Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Italic", str(font_dir / "Arial Italic.ttf")))


def pstyle(name: str, font="Arial", size=8.3, leading=None, color=INK, align=TA_LEFT) -> ParagraphStyle:
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        leading=leading or size * 1.25,
        textColor=color,
        alignment=align,
        allowWidows=0,
        allowOrphans=0,
    )


def paragraph(c: canvas.Canvas, value: str, x: float, top: float, width: float, style: ParagraphStyle) -> float:
    item = Paragraph(value, style)
    _, height = item.wrap(width, 1000)
    item.drawOn(c, x, top - height)
    return top - height


def fit_paragraph(
    c: canvas.Canvas,
    value: str,
    x: float,
    top: float,
    width: float,
    max_height: float,
    font="Arial",
    start=8.0,
    minimum=6.0,
    leading_factor=1.24,
    color=INK,
    align=TA_LEFT,
) -> float:
    size = start
    while size >= minimum:
        current = pstyle(f"fit-{x}-{top}-{size}", font=font, size=size, leading=size * leading_factor, color=color, align=align)
        item = Paragraph(value, current)
        _, height = item.wrap(width, max_height)
        if height <= max_height:
            item.drawOn(c, x, top - height)
            return height
        size -= 0.25
    raise ValueError(f"Text does not fit allotted area at {x}, {top}: {clean(value)[:80]}")


def rule(c: canvas.Canvas, x1: float, y: float, x2: float, width=0.45, shade=LIGHT) -> None:
    c.setStrokeColor(shade)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)


def footer(c: canvas.Canvas, page_no: int, section: str, size) -> None:
    width, _ = size
    rule(c, MARGIN_X, 13 * mm, width - MARGIN_X, 0.35, PALE)
    c.setFillColor(MID)
    c.setFont("Arial", 6.1)
    c.drawString(MARGIN_X, FOOTER_Y, "ADAM & AXEL JANSON  |  PRIVAT FAMILJEUTGÅVA  |  VERSION 3")
    c.drawCentredString(width / 2, FOOTER_Y, clean(section).upper())
    c.setFont("Arial-Bold", 6.5)
    c.drawRightString(width - MARGIN_X, FOOTER_Y, str(page_no))


def begin_page(c: canvas.Canvas, page_no: int, section: str, title: str, intro: str = "", size=PORTRAIT) -> float:
    c.setPageSize(size)
    width, height = size
    c.setFillColor(WHITE)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setFillColor(MID)
    c.setFont("Arial-Bold", 6.5)
    c.drawString(MARGIN_X, height - 16 * mm, clean(section).upper())
    y = paragraph(c, esc(title), MARGIN_X, height - 21 * mm, width - 2 * MARGIN_X,
                  pstyle(f"title-{page_no}", font="Georgia-Bold", size=19.5, leading=22.0))
    rule(c, MARGIN_X, y - 6, width - MARGIN_X, 0.65, INK)
    y -= 14
    if intro:
        y = paragraph(c, esc(intro), MARGIN_X, y, width - 2 * MARGIN_X,
                      pstyle(f"intro-{page_no}", font="Georgia", size=8.5, leading=11.2, color=MID)) - 8
    footer(c, page_no, section, size)
    return y


def end_page(c: canvas.Canvas) -> None:
    c.showPage()


def draw_cover(c: canvas.Canvas, content: dict) -> None:
    c.setPageSize(PORTRAIT)
    width, height = PORTRAIT
    c.setFillColor(WHITE)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setFillColor(MID)
    c.setFont("Arial-Bold", 7)
    c.drawString(MARGIN_X, height - 18 * mm, "EN KÄLLSTYRD FAMILJEBERÄTTELSE")
    c.setFillColor(INK)
    c.setFont("Georgia-Bold", 31)
    c.drawString(MARGIN_X, height - 42 * mm, "Adam & Axel Janson")
    c.setFont("Georgia", 17)
    c.drawString(MARGIN_X, height - 55 * mm, "fem generationer bakåt")
    rule(c, MARGIN_X, height - 66 * mm, width - MARGIN_X, 0.9, INK)

    y = height - 79 * mm
    y = paragraph(c, "<b>32 av 32</b> personer på djup 5 är kända, granskade och källbreddsklara. "
                  "Utgåvan skiljer arkivbelägg, säker familjekunskap, konflikter och dokumenterade arkivfronter.",
                  MARGIN_X, y, width - 2 * MARGIN_X, pstyle("cover-lead", font="Georgia", size=11.2, leading=15)) - 17
    c.setFont("Arial-Bold", 7)
    c.drawString(MARGIN_X, y, "INNEHÅLL")
    y -= 13
    items = [
        ("2", "Läsnyckel, ändringar och metod"),
        ("3-4", "Två sammanhängande släktträd"),
        ("5-8", "32 personporträtt"),
        ("9-10", "Fyra familjeberättelser"),
        ("11-12", "Platser, tidslinje, konflikter och fronter"),
        ("13-14", "Två källor i närbild"),
        ("15-16", "Exakta hänvisningar"),
    ]
    for page, label in items:
        c.setFont("Arial-Bold", 8)
        c.drawString(MARGIN_X, y, page)
        c.setFont("Arial", 8)
        c.drawString(MARGIN_X + 32, y, clean(label))
        y -= 17
    rule(c, MARGIN_X, y - 4, width - MARGIN_X, 0.35, PALE)
    y -= 24
    paragraph(c, "<b>Utgåveprotokoll.</b> Version 3 är en avskalad bruksversion av samma verifierade "
              "kunskapsläge som version 2. Version 1 och 2 är bevarade oförändrade. "
              "2 672 validerade påståenden, 642 källakter, 827 citationsakter och 4 346 bevarade mediefiler "
              "ligger bakom ögonblicksbilden.", MARGIN_X, y, width - 2 * MARGIN_X,
              pstyle("cover-protocol", size=8.1, leading=11.2))
    c.setFillColor(MID)
    c.setFont("Arial", 6.5)
    c.drawString(MARGIN_X, 18 * mm, "VERSION 3  |  4 SEPTEMBER 2026  |  PRIVAT FAMILJEBRUK")
    c.drawRightString(width - MARGIN_X, 18 * mm, "PCD-2026-09-04-004")


def draw_orientation(c: canvas.Canvas, content: dict) -> None:
    y = begin_page(c, 2, "Orientering", "Läsnyckel, ändringar och metod",
                   "En tätare utgåva behöver fortfarande visa vad som är känt, hur det är känt och var kunskapen tar slut.")
    page_w, _ = PORTRAIT
    gap = 18
    col_w = (page_w - 2 * MARGIN_X - gap) / 2
    left_x, right_x = MARGIN_X, MARGIN_X + col_w + gap

    c.setFont("Georgia-Bold", 11.5)
    c.drawString(left_x, y, "Ändrat sedan version 1")
    y_left = y - 16
    for idx, item in enumerate(content["changes_since_v1"], 1):
        text = f"<b>{idx}.</b> {esc(item)}"
        used = fit_paragraph(c, text, left_x, y_left, col_w, 76, start=7.55, minimum=7.0, leading_factor=1.28)
        y_left -= used + 8
    y_left -= 3
    rule(c, left_x, y_left, left_x + col_w, 0.35, PALE)
    y_left -= 12
    fit_paragraph(c, "<b>Redaktionellt beslut.</b> " + esc(content["editorial_decision"]) +
                  ". Version 3 ändrar formen, inte den genealogiska slutsatsen.",
                  left_x, y_left, col_w, 105, start=7.4, minimum=6.8)

    c.setFont("Georgia-Bold", 11.5)
    c.drawString(right_x, y, "Fyra sorters visshet")
    y_right = y - 17
    evidence = [
        ("SAMSTÄMMIGA BELÄGG", "Två självständiga eller kompletterande källor stöder uppgiften."),
        ("AVLÄST I KÄLLA", "Uppgiften är avläst i en identifierad original- eller registerkälla."),
        ("SÄKER FAMILJEKUNSKAP", "Ägaren har fastställt relationen; den visas inte som ett arkivfynd."),
        ("ÖPPEN KÄLLKONFLIKT", "Källorna skiljer sig åt. Skillnaden bevaras och förklaras."),
        ("DOKUMENTERAD ARKIVFRONT", "Förväntad källa, sökt omfång och återstartvillkor är dokumenterade."),
    ]
    for label, body in evidence:
        c.setFont("Arial-Bold", 6.6)
        c.drawString(right_x, y_right, label)
        y_right = paragraph(c, esc(body), right_x, y_right - 9, col_w,
                            pstyle(f"ev-{label}", size=7.35, leading=9.4, color=MID)) - 9
    rule(c, right_x, y_right, right_x + col_w, 0.35, PALE)
    y_right -= 18
    c.setFont("Georgia-Bold", 11.5)
    c.drawString(right_x, y_right, "Från arkivbild till berättelse")
    y_right -= 17
    steps = [
        ("1. Lokalisera", "Volym, sida, bild-id och sökväg sparas."),
        ("2. Läs", "Källans ord avskrivs före normalisering."),
        ("3. Pröva identitet", "Kronologi, geografi, hushåll, relationer och yrke vägs samman."),
        ("4. Väg belägg", "Samstämmighet, konflikt, familjekunskap och nollresultat hålls isär."),
        ("5. Berätta", "PDF:en sammanfattar; akterna behåller full proveniens."),
    ]
    for label, body in steps:
        y_right = paragraph(c, f"<b>{esc(label)}</b>  {esc(body)}", right_x, y_right, col_w,
                            pstyle(f"step-{label}", size=7.25, leading=9.4)) - 6
    y_right -= 3
    fit_paragraph(c, "<b>Källfamiljer.</b> Födelse-, vigsel- och dödböcker; husförhör och församlingsböcker; "
                  "folkräkningar och SCB-utdrag; flyttlängder; rotemansarkiv; press och missionshistoria; "
                  "barnhusrulla; boupptecknings-, skatt/mantal- och yrkesvägar; namngivna familjeuppgifter.",
                  right_x, y_right, col_w, 115, start=7.15, minimum=6.7)


def tree_centres(depth: int, top=438.0, bottom=57.0) -> list[float]:
    leaves = [top - i * ((top - bottom) / 15) for i in range(16)]
    span = 2 ** (5 - depth)
    return [sum(leaves[i * span:(i + 1) * span]) / span for i in range(2 ** (depth - 1))]


def draw_tree_node(c: canvas.Canvas, name: str, meta: str, x: float, centre: float, w: float, h: float, leaf=False) -> None:
    c.setFillColor(WHITE)
    c.setStrokeColor(MID if not leaf else LIGHT)
    c.setLineWidth(0.55 if not leaf else 0.4)
    c.rect(x, centre - h / 2, w, h, fill=1, stroke=1)
    top = centre + h / 2 - 3.2
    max_name_h = h - (8 if meta else 5)
    fit_paragraph(c, esc(name), x + 3, top, w - 6, max_name_h,
                  font="Arial-Bold" if not leaf else "Arial", start=6.5 if not leaf else 5.8,
                  minimum=5.1, leading_factor=1.05, align=TA_CENTER)
    if meta:
        c.setFillColor(MID)
        c.setFont("Arial", 4.5)
        c.drawCentredString(x + w / 2, centre - h / 2 + 2.3, clean(meta))


def draw_tree(c: canvas.Canvas, page_no: int, side: str, positions: list[dict]) -> None:
    title = f"Adam och Axel via {side}"
    intro = ("Fem generationer bakåt. Läs från vänster till höger: varje person förgrenas till far överst och mor underst. "
             "Tunna linjer visar relationen; statusen på djup 5 står med positionskoden.")
    begin_page(c, page_no, "Sammanhängande släktträd", title, intro, LANDSCAPE)
    xs = [36, 187, 338, 489, 640]
    widths = [123, 123, 123, 123, 166]
    heights = [30, 27, 25, 23, 23]
    generations = deepcopy(TREE_NAMES[side])
    generations.append([entry["name"] for entry in positions])

    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.45)
    for depth in range(1, 5):
        child_centres = tree_centres(depth)
        parent_centres = tree_centres(depth + 1)
        x1 = xs[depth - 1] + widths[depth - 1]
        x2 = xs[depth]
        mid_x = (x1 + x2) / 2
        for index, child_y in enumerate(child_centres):
            upper, lower = parent_centres[index * 2:index * 2 + 2]
            c.line(x1, child_y, mid_x, child_y)
            c.line(mid_x, upper, mid_x, lower)
            c.line(mid_x, upper, x2, upper)
            c.line(mid_x, lower, x2, lower)

    for depth, names in enumerate(generations, 1):
        centres = tree_centres(depth)
        for index, (name, centre) in enumerate(zip(names, centres)):
            meta = ""
            if depth == 5:
                entry = positions[index]
                meta = f"{entry['code']}  |  {STATUS_LABELS[entry['status']]}"
            draw_tree_node(c, name, meta, xs[depth - 1], centre, widths[depth - 1], heights[depth - 1], depth == 5)

    c.setFillColor(MID)
    c.setFont("Arial", 5.7)
    for depth, x in enumerate(xs, 1):
        c.drawCentredString(x + widths[depth - 1] / 2, 460, f"DJUP {depth}")


def draw_portrait_entry(c: canvas.Canvas, entry: dict, person: dict, x: float, top: float, w: float, h: float) -> None:
    summary, citations = V2.select_portrait_text(person, entry)
    c.setFillColor(MID)
    c.setFont("Arial-Bold", 5.8)
    c.drawString(x, top - 7, clean(entry["code"]))
    c.drawRightString(x + w, top - 7, STATUS_LABELS[entry["status"]])
    name_top = top - 14
    used = fit_paragraph(c, esc(entry["name"]), x, name_top, w, 26, font="Georgia-Bold", start=9.4, minimum=8.1, leading_factor=1.08)
    info_top = name_top - used - 2
    info_used = fit_paragraph(c, esc(entry["life"] + " | " + entry["place"]), x, info_top, w, 18,
                              font="Arial-Bold", start=6.3, minimum=5.8, leading_factor=1.1, color=MID)
    body_top = info_top - info_used - 6
    fit_paragraph(c, esc(summary), x, body_top, w, h - (top - body_top) - 25,
                  start=7.2, minimum=6.5, leading_factor=1.25)
    c.setFillColor(MID)
    c.setFont("Arial", 5.2)
    c.drawString(x, top - h + 9, clean("Källor: " + ", ".join(citations[:4])))
    rule(c, x, top - h, x + w, 0.35, PALE)


def draw_portraits(c: canvas.Canvas, page_no: int, entries: list[dict], people: dict, title: str) -> None:
    y = begin_page(c, page_no, "32 personporträtt", title,
                   "Korta ingångar till de konsoliderade personakterna; fullständiga påståenden, konflikter och proveniens ligger kvar i projektarkivet.")
    page_w, _ = PORTRAIT
    gap = 16
    col_w = (page_w - 2 * MARGIN_X - gap) / 2
    row_h = 166
    rule(c, page_w / 2, 45, page_w / 2, 0.35, PALE)
    for idx, entry in enumerate(entries):
        row, col = divmod(idx, 2)
        x = MARGIN_X + col * (col_w + gap)
        top = y - row * row_h
        draw_portrait_entry(c, entry, people[entry["person_id"]], x, top, col_w, row_h - 7)


def draw_story_block(c: canvas.Canvas, story: dict, x: float, top: float, w: float, h: float, index: int) -> None:
    c.setFillColor(MID)
    c.setFont("Arial-Bold", 6.2)
    c.drawString(x, top, clean(story["side"].upper() + "S SIDA"))
    title_h = fit_paragraph(c, esc(story["title"]), x, top - 10, w, 36, font="Georgia-Bold", start=12.3, minimum=10.8, leading_factor=1.1)
    y = top - 14 - title_h
    lead_h = fit_paragraph(c, esc(story["lead"]), x, y, w, 70, font="Georgia", start=8.2, minimum=7.3, leading_factor=1.28, color=MID)
    y -= lead_h + 10
    for number, point in enumerate(story["points"], 1):
        used = fit_paragraph(c, f"<b>{number}.</b> {esc(point)}", x, y, w, 45,
                             start=7.45, minimum=6.8, leading_factor=1.22)
        y -= used + 5
    c.setFillColor(MID)
    c.setFont("Arial", 5.5)
    c.drawString(x, top - h + 10, clean("Verifieringsankare: " + ", ".join(story["citations"])))
    rule(c, x, top - h, x + w, 0.45, LIGHT)


def draw_stories(c: canvas.Canvas, page_no: int, stories: list[dict], title: str) -> None:
    y = begin_page(c, page_no, "Fördjupning", title,
                   "Fyra berättelser visar hur yrken, hushåll, flyttningar och konflikter formar släktlinjerna.")
    page_w, _ = PORTRAIT
    block_h = 342
    draw_story_block(c, stories[0], MARGIN_X, y, page_w - 2 * MARGIN_X, block_h, 0)
    draw_story_block(c, stories[1], MARGIN_X, y - block_h - 12, page_w - 2 * MARGIN_X, block_h, 1)


def geojson_rings(geometry: dict):
    if geometry["type"] == "Polygon":
        return geometry["coordinates"]
    if geometry["type"] == "MultiPolygon":
        return [ring for polygon in geometry["coordinates"] for ring in polygon]
    return []


def all_places(content: dict) -> list[dict]:
    base = json.loads(V1_MANIFEST_PATH.read_text())["map"]["places"]
    extra = deepcopy(content["extra_places"])
    return base + extra


def draw_map_page(c: canvas.Canvas, content: dict) -> None:
    y = begin_page(c, 11, "Plats", "Orterna bakom släktlinjerna",
                   "Punkterna är moderna orienteringspunkter för källstödda livsplatser, inte exakta historiska gårdskoordinater. Kontur: Natural Earth 1:10m v5.1.1. Basorter: OpenStreetMap Nominatim 2026-08-22.", LANDSCAPE)
    width, _ = LANDSCAPE
    places = all_places(content)
    map_x, map_y, map_w, map_h = 35, 52, 345, 438
    list_x, list_w = 408, width - 408 - MARGIN_X

    outline = json.loads(SWEDEN_PATH.read_text())
    points = []
    for feature in outline["features"]:
        for ring in geojson_rings(feature["geometry"]):
            for lon, lat, *_ in ring:
                points.append((lon * math.cos(math.radians(62)), lat))
    min_x = min(p[0] for p in points); max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points); max_y = max(p[1] for p in points)
    scale = min(map_w / (max_x - min_x), map_h / (max_y - min_y))

    def project(lon: float, lat: float) -> tuple[float, float]:
        px = lon * math.cos(math.radians(62))
        x = map_x + (px - min_x) * scale + (map_w - (max_x - min_x) * scale) / 2
        yy = map_y + (lat - min_y) * scale + (map_h - (max_y - min_y) * scale) / 2
        return x, yy

    c.setStrokeColor(MID)
    c.setLineWidth(0.45)
    for feature in outline["features"]:
        for ring in geojson_rings(feature["geometry"]):
            path = c.beginPath()
            for idx, coord in enumerate(ring):
                px, py = project(coord[0], coord[1])
                if idx == 0:
                    path.moveTo(px, py)
                else:
                    path.lineTo(px, py)
            c.drawPath(path, fill=0, stroke=1)

    for idx, place in enumerate(places, 1):
        px, py = project(float(place["lon"]), float(place["lat"]))
        c.setFillColor(INK)
        c.circle(px, py, 2.2, fill=1, stroke=0)
        c.setFont("Arial-Bold", 4.8)
        c.drawString(px + 3.2, py + 1, str(idx))

    c.setFont("Georgia-Bold", 10.5)
    c.drawString(list_x, y, "Platsindex")
    gap = 14
    col_w = (list_w - gap) / 2
    row_h = 38
    for idx, place in enumerate(places, 1):
        col = 0 if idx <= 11 else 1
        row = idx - 1 if col == 0 else idx - 12
        x = list_x + col * (col_w + gap)
        top = y - 16 - row * row_h
        c.setFillColor(INK)
        c.setFont("Arial-Bold", 6.3)
        c.drawString(x, top, f"{idx}. {clean(place['label'])}")
        fit_paragraph(c, esc(clean(place.get("region", "")) + " | " + clean(place.get("period", "")) +
                             " | " + ", ".join(place.get("citations", [])[:3])),
                      x, top - 8, col_w, 25, start=5.3, minimum=4.8, leading_factor=1.13, color=MID)


def draw_timeline_and_fronts(c: canvas.Canvas, content: dict) -> None:
    y = begin_page(c, 12, "Tid och forskningsfront", "Tidslinje, konflikter och återstartvägar",
                   "En behandlad generation är inte en perfekt berättelse. Den är en berättelse där även osäkerheten har en exakt plats.")
    page_w, _ = PORTRAIT
    gap = 18
    col_w = (page_w - 2 * MARGIN_X - gap) / 2
    c.setFont("Georgia-Bold", 11.5)
    c.drawString(MARGIN_X, y, "Tidslinje")
    timeline_top = y - 18
    for idx, event in enumerate(content["timeline"]):
        col = 0 if idx < 4 else 1
        row = idx if col == 0 else idx - 4
        x = MARGIN_X + col * (col_w + gap)
        top = timeline_top - row * 55
        c.setFont("Arial-Bold", 6.7)
        c.setFillColor(INK)
        c.drawString(x, top, clean(event["date"]))
        fit_paragraph(c, esc(event["text"]), x + 48, top + 1, col_w - 48, 38,
                      start=6.4, minimum=5.8, leading_factor=1.2)
        c.setFillColor(MID)
        c.setFont("Arial", 4.9)
        c.drawString(x + 48, top - 34, clean(", ".join(event["citations"])))

    split_y = y - 238
    rule(c, MARGIN_X, split_y, page_w - MARGIN_X, 0.65, INK)
    c.setFillColor(INK)
    c.setFont("Georgia-Bold", 11.5)
    c.drawString(MARGIN_X, split_y - 22, "Konflikter och arkivfronter")
    front_top = split_y - 43
    for idx, item in enumerate(content["fronts_and_conflicts"]):
        col = idx % 2
        row = idx // 2
        x = MARGIN_X + col * (col_w + gap)
        top = front_top - row * 112
        label = "ÖPPEN KÄLLKONFLIKT" if idx < 5 else "DOKUMENTERAD ARKIVFRONT"
        c.setFillColor(MID)
        c.setFont("Arial-Bold", 5.8)
        c.drawString(x, top, label)
        fit_paragraph(c, esc(item), x, top - 10, col_w, 84, start=7.15, minimum=6.4, leading_factor=1.24)
        rule(c, x, top - 98, x + col_w, 0.35, PALE)


def grayscale_source(path: Path) -> Path:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    source = path
    if path.suffix.lower() == ".pdf":
        prefix = TMP_DIR / path.stem
        subprocess.run(["pdftoppm", "-png", "-singlefile", "-r", "180", str(path), str(prefix)],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        source = prefix.with_suffix(".png")
    out = TMP_DIR / (source.stem + "-gray.png")
    with Image.open(source) as image:
        ImageOps.grayscale(image).save(out)
    return out


def draw_fitted_image(c: canvas.Canvas, path: Path, x: float, y: float, w: float, h: float) -> None:
    with Image.open(path) as image:
        iw, ih = image.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(str(path), x + (w - dw) / 2, y + (h - dh) / 2, width=dw, height=dh, mask="auto")


def draw_close_reading(c: canvas.Canvas, page_no: int, item: dict) -> None:
    y = begin_page(c, page_no, "Källan i närbild", item["title"],
                   "Avskrift, belägg och icke-belägg står bredvid bilden så att källans gräns förblir synlig.")
    page_w, _ = PORTRAIT
    image_y, image_h = 365, y - 375
    source = grayscale_source(ROOT / item["image"])
    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.45)
    c.rect(MARGIN_X, image_y, page_w - 2 * MARGIN_X, image_h, fill=0, stroke=1)
    draw_fitted_image(c, source, MARGIN_X + 5, image_y + 5, page_w - 2 * MARGIN_X - 10, image_h - 10)

    top = image_y - 16
    c.setFont("Georgia-Bold", 10.2)
    c.drawString(MARGIN_X, top, "Varsam avskrift")
    top = paragraph(c, esc(item["transcription"]), MARGIN_X, top - 13, page_w - 2 * MARGIN_X,
                    pstyle(f"trans-{page_no}", font="Georgia", size=7.8, leading=10.2)) - 16
    gap = 18
    col_w = (page_w - 2 * MARGIN_X - gap) / 2
    for idx, (label, value) in enumerate((("Detta visar raden", item["proves"]), ("Detta visar den inte", item["does_not_prove"]))):
        x = MARGIN_X + idx * (col_w + gap)
        c.setFont("Georgia-Bold", 9.2)
        c.drawString(x, top, label)
        fit_paragraph(c, esc(value), x, top - 13, col_w, 96, start=7.45, minimum=6.7, leading_factor=1.25)
    c.setFillColor(MID)
    c.setFont("Arial-Bold", 6)
    c.drawRightString(page_w - MARGIN_X, 41, clean(item["citation"]))


def citation_record(citation_id: str) -> tuple[str, str]:
    title, location = V2.citation_record(citation_id)
    return clean(title), clean(location)


def draw_references(c: canvas.Canvas, page_no: int, ids: list[str], part: int, final=False) -> None:
    y = begin_page(c, page_no, "Verifiera själv", f"Exakta hänvisningar - {part}",
                   "Varje C-nummer leder till en full citationsakt med källställe, avskrift, identitetsbedömning och lokalt material där det finns.")
    page_w, _ = PORTRAIT
    gap = 18
    col_w = (page_w - 2 * MARGIN_X - gap) / 2
    per_col = math.ceil(len(ids) / 2)
    item_h = 78
    for idx, citation_id in enumerate(ids):
        col = idx // per_col
        row = idx % per_col
        x = MARGIN_X + col * (col_w + gap)
        top = y - row * item_h
        title, location = citation_record(citation_id)
        title_h = fit_paragraph(c, "<b>" + esc(title) + "</b>", x, top, col_w, 25,
                                start=6.4, minimum=5.7, leading_factor=1.15)
        fit_paragraph(c, esc(location), x, top - title_h - 4, col_w, 44,
                      start=5.5, minimum=4.8, leading_factor=1.17, color=MID)
        rule(c, x, top - 70, x + col_w, 0.3, PALE)
    if final:
        c.setFillColor(MID)
        c.setFont("Arial", 5.4)
        c.drawString(MARGIN_X, 38, "Manifest: genealogy/editions/adam-axel-depth5-v3.json  |  Kunskapsläge: 2026-09-04")
        c.drawRightString(page_w - MARGIN_X, 38, "Full proveniens och återstartvillkor finns i projektarkivet.")


def build(pdf_path: Path) -> None:
    register_fonts()
    edition = json.loads(EDITION_PATH.read_text())
    content = json.loads(CONTENT_PATH.read_text())
    project = json.loads(PROJECT_DATA_PATH.read_text())
    people = {person["id"]: person for person in project["people"]}
    positions = content["depth5_positions"]
    if len(positions) != 32 or any(entry["person_id"] not in people for entry in positions):
        raise ValueError("Version-3 content does not resolve to exactly 32 depth-5 people")

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(pdf_path), pagesize=PORTRAIT, pageCompression=1)
    c.setTitle(clean(edition["edition"]["title"]))
    c.setAuthor("Sverker Janson | källstyrt familjearkiv")
    c.setSubject("Avskalad privat djup-5-utgåva för Adam och Axel Janson")
    c.setKeywords("släktforskning, Janson, Höök, familjehistoria, antavla, djup 5")

    draw_cover(c, content); end_page(c)
    draw_orientation(c, content); end_page(c)
    draw_tree(c, 3, "Sverker", positions[:16]); end_page(c)
    draw_tree(c, 4, "Kristina", positions[16:]); end_page(c)
    portrait_titles = [
        "Sverkers sida - söder", "Sverkers sida - norr",
        "Kristinas sida - Fredberg och Carlman", "Kristinas sida - Medelpad",
    ]
    for offset, title in enumerate(portrait_titles):
        draw_portraits(c, 5 + offset, positions[offset * 8:(offset + 1) * 8], people, title); end_page(c)
    draw_stories(c, 9, content["feature_stories"][:2], "Jord, torp och Västerbottens hushåll"); end_page(c)
    draw_stories(c, 10, content["feature_stories"][2:], "Järnvägen och Lagfors"); end_page(c)
    draw_map_page(c, content); end_page(c)
    draw_timeline_and_fronts(c, content); end_page(c)
    for page_no, item in enumerate(content["source_close_readings"], 13):
        draw_close_reading(c, page_no, item); end_page(c)
    refs = content["reference_citations"]
    draw_references(c, 15, refs[:16], 1); end_page(c)
    draw_references(c, 16, refs[16:], 2, final=True)
    c.save()
    print(pdf_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_PDF)
    args = parser.parse_args()
    build(args.output.resolve())


if __name__ == "__main__":
    main()
