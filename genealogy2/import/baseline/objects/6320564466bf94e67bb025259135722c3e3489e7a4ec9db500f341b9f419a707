#!/usr/bin/env python
"""Build the private Adam-and-Axel depth-5 family edition."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import re
import subprocess
from copy import deepcopy
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "genealogy/editions/adam-axel-depth5-v2.json"
V1_MANIFEST_PATH = ROOT / "genealogy/editions/adam-axel-depth4-v1.json"
PROJECT_DATA_PATH = ROOT / "dashboard/public/data/project.json"
DEFAULT_PDF = ROOT / "output/pdf/adam-och-axel-janson-fem-generationer-v2.pdf"
TMP_DIR = ROOT / "tmp/pdfs/family-edition-v2"

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
PAPER = colors.HexColor("#F5EFE3")
PAPER_DEEP = colors.HexColor("#EADFCF")
WHITE = colors.HexColor("#FFFDF8")
INK = colors.HexColor("#24313A")
MUTED = colors.HexColor("#64717A")
LINE = colors.HexColor("#CBBEAB")
RUST = colors.HexColor("#9A4A35")
BLUE = colors.HexColor("#356F8E")
SAGE = colors.HexColor("#718168")
GOLD = colors.HexColor("#B7873F")
BURGUNDY = colors.HexColor("#754252")
SOFT_RUST = colors.HexColor("#F1DDD5")
SOFT_BLUE = colors.HexColor("#DDEBF0")
SOFT_GOLD = colors.HexColor("#F2E5CC")
SOFT_GREEN = colors.HexColor("#E4EBDD")

STATUS = {
    "CORROBORATED": (SAGE, "SAMSTÄMMIGA BELÄGG"),
    "TRANSCRIBED": (BLUE, "AVLÄST I KÄLLA"),
    "OWNER_CONFIRMED": (BURGUNDY, "SÄKER FAMILJEKUNSKAP"),
    "CONFLICT": (RUST, "ÖPPEN KÄLLKONFLIKT"),
    "FRONT": (GOLD, "DOKUMENTERAD ARKIVFRONT"),
}


def load_v1_module():
    spec = importlib.util.spec_from_file_location("family_edition_v1", ROOT / "scripts/build-family-edition.py")
    if not spec or not spec.loader:
        raise RuntimeError("Could not load the version-1 family-edition helpers")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V1 = load_v1_module()


def clean(value: object) -> str:
    text = str(value or "")
    return (
        text.replace("\u2011", "-")
        .replace("\u2010", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
    )


def esc(value: object) -> str:
    import html

    return html.escape(clean(value), quote=False).replace("\n", "<br/>")


def register_fonts() -> None:
    font_dir = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("Georgia", str(font_dir / "Georgia.ttf")))
    pdfmetrics.registerFont(TTFont("Georgia-Bold", str(font_dir / "Georgia Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Georgia-Italic", str(font_dir / "Georgia Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Arial", str(font_dir / "Arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(font_dir / "Arial Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Italic", str(font_dir / "Arial Italic.ttf")))


def style(name: str, font="Arial", size=9, leading=None, color=INK, align=TA_LEFT) -> ParagraphStyle:
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        leading=leading or size * 1.3,
        textColor=color,
        alignment=align,
        allowWidows=0,
        allowOrphans=0,
    )


BODY = style("body", size=9.1, leading=12.1)
SMALL = style("small", size=7.6, leading=10.0)
TINY = style("tiny", size=6.4, leading=8.2, color=MUTED)
INTRO = style("intro", font="Georgia", size=10, leading=13.2, color=MUTED)


def para(c: canvas.Canvas, value: object, x: float, top: float, width: float, pstyle=BODY) -> float:
    p = Paragraph(esc(value), pstyle)
    _, height = p.wrap(width, PAGE_H)
    p.drawOn(c, x, top - height)
    return top - height


def rich_para(c: canvas.Canvas, value: str, x: float, top: float, width: float, pstyle=BODY) -> float:
    p = Paragraph(clean(value), pstyle)
    _, height = p.wrap(width, PAGE_H)
    p.drawOn(c, x, top - height)
    return top - height


def card(c, x, y, w, h, fill=WHITE, stroke=LINE, radius=8) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.65)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def chip(c, key: str, x: float, y: float, compact=False) -> float:
    color, label = STATUS.get(key, (MUTED, key))
    font_size = 5.5 if compact else 6.2
    height = 12 if compact else 14
    width = pdfmetrics.stringWidth(label, "Arial-Bold", font_size) + 11
    c.setFillColor(color)
    c.roundRect(x, y, width, height, height / 2, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Arial-Bold", font_size)
    c.drawString(x + 5.5, y + (3.5 if compact else 4.2), label)
    return width


def footer(c: canvas.Canvas, page_no: int, section: str) -> None:
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(MARGIN, 13 * mm, PAGE_W - MARGIN, 13 * mm)
    c.setFillColor(MUTED)
    c.setFont("Arial", 6.3)
    c.drawString(MARGIN, 8.5 * mm, "ADAM & AXEL JANSON  |  PRIVAT FAMILJEUTGÅVA  |  2026-09-04")
    c.drawCentredString(PAGE_W / 2, 8.5 * mm, clean(section).upper())
    c.setFont("Arial-Bold", 7)
    c.drawRightString(PAGE_W - MARGIN, 8.5 * mm, str(page_no))


def background(c: canvas.Canvas, page_no: int, section: str) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    footer(c, page_no, section)


def page_title(c, page_no: int, kicker: str, title: str, intro: str, accent, section: str) -> float:
    background(c, page_no, section)
    c.setFillColor(accent)
    c.roundRect(MARGIN, PAGE_H - 28 * mm, 30 * mm, 4 * mm, 2 * mm, fill=1, stroke=0)
    c.setFont("Arial-Bold", 7.1)
    c.drawString(MARGIN, PAGE_H - 18.5 * mm, clean(kicker).upper())
    y = para(c, title, MARGIN, PAGE_H - 31 * mm, PAGE_W - 2 * MARGIN, style("page-title", font="Georgia-Bold", size=22, leading=24.5))
    y = para(c, intro, MARGIN, y - 9, PAGE_W - 2 * MARGIN, INTRO)
    return y - 10


def page_done(c: canvas.Canvas) -> None:
    c.showPage()


def first_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", clean(text)).strip()
    match = re.match(r"(.+?[.!?])(?:\s|$)", text)
    return match.group(1) if match else text


def select_portrait_text(person: dict, entry: dict) -> tuple[str, list[str]]:
    claims = [c for c in person.get("claims", []) if c.get("status") in {"CORROBORATED", "TRANSCRIBED", "OWNER_CONFIRMED", "CONFLICT"}]
    conflict = [c for c in claims if c.get("status") == "CONFLICT"]

    def score(claim: dict) -> tuple[int, str]:
        s = clean(claim.get("statement", "")).lower()
        points = 0
        for token, weight in [
            ("född", 5), ("födelse", 5), ("dog", 4), ("avled", 4),
            ("yrke", 4), ("arbet", 4), ("bonde", 4), ("torpare", 4),
            ("hemmans", 4), ("föräldrar", 3), ("gifte", 2), ("hustru", 2),
        ]:
            if token in s:
                points += weight
        if claim.get("status") == "CORROBORATED":
            points += 3
        return points, claim.get("id", "")

    def category(claim: dict) -> str:
        statement = clean(claim.get("statement", "")).lower()
        if "född" in statement or "födelse" in statement:
            return "birth"
        if "dog" in statement or "avled" in statement or "död" in statement:
            return "death"
        if any(token in statement for token in ("arbet", "bonde", "torpare", "hemmans", "kronolänsman", "järnväg")):
            return "work"
        if "föräldrar" in statement or "dotter till" in statement or "son till" in statement:
            return "parents"
        if "gift" in statement or "hustru" in statement or "make" in statement:
            return "family"
        return "other"

    picked: list[dict] = []
    if entry["status"] == "CONFLICT" and conflict:
        picked.append(sorted(conflict, key=score, reverse=True)[0])
    ordered = sorted(claims, key=score, reverse=True)
    for claim in ordered:
        if claim not in picked:
            picked.append(claim)
            break
    for claim in ordered:
        if claim not in picked and all(category(claim) != category(other) for other in picked):
            picked.append(claim)
            break
    summary = " ".join(first_sentence(c.get("statement", "")) for c in picked)
    if len(summary) > 360:
        summary = summary[:357].rsplit(" ", 1)[0] + "..."
    citations: list[str] = []
    for claim in picked:
        for citation in claim.get("citations", []):
            if citation not in citations:
                citations.append(citation)
    return summary, citations[:6]


def draw_cover(c: canvas.Canvas, manifest: dict) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(RUST)
    c.rect(0, 0, PAGE_W / 2, PAGE_H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(PAGE_W / 2, 0, PAGE_W / 2, PAGE_H, fill=1, stroke=0)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.09))
    for radius in (95, 155, 215, 275):
        c.circle(PAGE_W / 2, PAGE_H * 0.69, radius, fill=0, stroke=1)
    c.setFillColor(WHITE)
    c.setFont("Arial-Bold", 8)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 41 * mm, "EN KÄLLSTYRD FAMILJEBERÄTTELSE")
    c.setFont("Georgia-Bold", 38)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 75 * mm, "ADAM & AXEL")
    c.setFont("Georgia", 22)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 91 * mm, "JANSON")
    c.setFont("Georgia-Italic", 15)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 116 * mm, "fem generationer bakåt")
    card(c, 54 * mm, 86 * mm, PAGE_W - 108 * mm, 55 * mm, fill=colors.Color(1, 1, 1, alpha=0.93), stroke=WHITE)
    rich_para(c, "<b>32 av 32</b><br/><font size='8'>personer på djup 5 är kända, granskade och källbreddsklara</font>", 65 * mm, 126 * mm, PAGE_W - 130 * mm, style("cover-stat", font="Georgia", size=18, leading=22, align=TA_CENTER))
    c.setFillColor(WHITE)
    c.setFont("Arial", 8)
    c.drawCentredString(PAGE_W / 2, 59 * mm, "VERSION 2  |  4 SEPTEMBER 2026  |  PRIVAT FAMILJEBRUK")
    c.setFont("Arial-Italic", 7)
    c.drawCentredString(PAGE_W / 2, 47 * mm, "Arkivbelägg, familjekunskap, konflikter och öppna fronter hålls synligt isär.")


def draw_changes(c, manifest, page_no: int) -> None:
    y = page_title(c, page_no, "Ny utgåva", "Vad som ändrats sedan version 1", "Version 1 från augusti 2026 bevaras oförändrad. Den här utgåvan är en ny fryst ögonblicksbild av projektets kanoniska kunskapsläge den 4 september 2026.", GOLD, "Orientering")
    for index, item in enumerate(manifest["changes_since_v1"], 1):
        fill = SOFT_RUST if index % 2 else SOFT_BLUE
        card(c, MARGIN, y - 76, PAGE_W - 2 * MARGIN, 64, fill=fill)
        c.setFillColor(RUST if index % 2 else BLUE)
        c.circle(MARGIN + 20, y - 44, 12, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Arial-Bold", 9)
        c.drawCentredString(MARGIN + 20, y - 47, str(index))
        para(c, item, MARGIN + 43, y - 23, PAGE_W - 2 * MARGIN - 58, SMALL)
        y -= 78
    rich_para(c, "<b>Redaktionellt beslut:</b> " + manifest["editorial_decision"] + ". Den nya PDF:en föregår djup-6-forskningen och skriver inte över den första utgåvan.", MARGIN, y - 8, PAGE_W - 2 * MARGIN, SMALL)


def draw_evidence(c, page_no: int) -> None:
    y = page_title(c, page_no, "Så ska den läsas", "Fyra lager - fyra sorters visshet", "Utgåvan berättar sammanhängande, men låter aldrig berättelsens flyt sudda ut varifrån en uppgift kommer eller vad som fortfarande är osäkert.", SAGE, "Orientering")
    items = [
        ("CORROBORATED", "Arkivbelägg", "Två självständiga eller kompletterande källor stödjer den konsoliderade uppgiften."),
        ("OWNER_CONFIRMED", "Säker familjekunskap", "Projektägaren har uttryckligen fastställt relationen. Den är sann i projektet men visas inte som om den kom ur en arkivpost."),
        ("CONFLICT", "Källkonflikt", "Källorna skiljer sig åt i exempelvis datum, ort eller namnform. Skillnaden bevaras och förklaras."),
        ("FRONT", "Arkivfront", "Förväntad källa, prövat omfång och återstartvillkor är dokumenterade. Åtkomsthinder förväxlas inte med att material saknas."),
    ]
    for idx, (status, title, body) in enumerate(items):
        row, col = divmod(idx, 2)
        w = (PAGE_W - 2 * MARGIN - 12) / 2
        h = 205
        x = MARGIN + col * (w + 12)
        yy = y - (row + 1) * h - row * 14
        card(c, x, yy, w, h, fill=WHITE)
        chip(c, status, x + 14, yy + h - 32)
        para(c, title, x + 14, yy + h - 55, w - 28, style(f"ev-title-{idx}", font="Georgia-Bold", size=13, leading=15))
        para(c, body, x + 14, yy + h - 86, w - 28, SMALL)
    rich_para(c, "<b>Måttet bakom utgåvan.</b> Djup 5 är behandlat först när alla kända personer är identitetsgranskade och källbreddsklara och varje närmare anspets har en giltig, exakt klassificerad arkivfront.", MARGIN, 105, PAGE_W - 2 * MARGIN, BODY)


ROOT_LADDERS = {
    "Sverker": [
        ("Djup 1", "Sverker Adam Janson"),
        ("Djup 2", "Jan-Christer Janson  |  Hillevi Zingmark"),
        ("Djup 3", "Arne Godvig Jansson  |  Maj Amalia Ekholm  |  Oskar Alfred Zingmark  |  Ebba Alfrida Andersson"),
        ("Djup 4", "Bernhard Eliasson  |  Ada Jansson  |  Axel Edvard Eriksson  |  Hulda Ålund  |  Johan Oskar Zingmark  |  Ida Andersdotter  |  Anders Alfred Andersson  |  Anna Fredrika Jakobsdotter"),
    ],
    "Kristina": [
        ("Djup 1", "Kristina Elisabeth Petronella Höök"),
        ("Djup 2", "Gunnar Höök  |  Evy Höök"),
        ("Djup 3", "Anders Ivar Höök  |  Anna Elisabeth Carlman  |  Axel Edvin Henriksson  |  Emma Petronella Eugenia Larsson"),
        ("Djup 4", "Johannes Ivar Fredberg  |  Anna Matilda Hök  |  Johan Fredrik Villehad Carlman  |  Elin Andersson  |  Erik Jonas Henriksson  |  Gertrud Jonsson  |  Anders Niklas Larsson  |  Ingrid Höglund"),
    ],
}


def draw_roots(c, page_no: int) -> None:
    y = page_title(c, page_no, "Antavlan", "Från bröderna till djup 4", "Adam och Axel delar samma antavla. Här visas vägen fram till de sexton personer vars föräldrar tillsammans bildar utgåvans 32 positioner på djup 5.", GOLD, "Antavla")
    w = (PAGE_W - 2 * MARGIN - 14) / 2
    for col, (side, accent) in enumerate((("Sverker", RUST), ("Kristina", BLUE))):
        x = MARGIN + col * (w + 14)
        card(c, x, 75, w, y - 85, fill=WHITE)
        c.setFillColor(accent)
        c.rect(x, y - 12, w, 5, fill=1, stroke=0)
        para(c, side + "s sida", x + 14, y - 28, w - 28, style(f"ladder-{side}", font="Georgia-Bold", size=16, leading=19))
        top = y - 65
        for depth, names in ROOT_LADDERS[side]:
            c.setFillColor(accent)
            c.setFont("Arial-Bold", 7)
            c.drawString(x + 14, top, depth.upper())
            top = para(c, names, x + 14, top - 10, w - 28, style(f"names-{side}-{depth}", size=7.3, leading=9.7)) - 22
    c.setFillColor(MUTED)
    c.setFont("Arial-Italic", 6.8)
    c.drawString(MARGIN, 58, "Ordningen i följande antavlesidor är alltid far före mor; positionskoden kan följas tillbaka till respektive gren.")


def draw_depth5(c, entries: list[dict], page_no: int, title: str, intro: str, accent) -> None:
    y = page_title(c, page_no, "Djup 5", title, intro, accent, "Antavla")
    gap_x, gap_y = 10, 9
    cols = 2
    w = (PAGE_W - 2 * MARGIN - gap_x) / cols
    h = 126
    for idx, entry in enumerate(entries):
        row, col = divmod(idx, cols)
        x = MARGIN + col * (w + gap_x)
        yy = y - (row + 1) * h - row * gap_y
        fill = SOFT_GOLD if entry["status"] == "CONFLICT" else WHITE
        card(c, x, yy, w, h, fill=fill)
        c.setFillColor(accent)
        c.rect(x, yy, 4, h, fill=1, stroke=0)
        c.setFont("Arial-Bold", 6.3)
        c.setFillColor(MUTED)
        c.drawString(x + 13, yy + h - 18, entry["code"])
        para(c, entry["name"], x + 13, yy + h - 31, w - 26, style(f"ped-{page_no}-{idx}", font="Georgia-Bold", size=10.4, leading=12))
        para(c, entry["life"] + "  |  " + entry["place"], x + 13, yy + 50, w - 26, style(f"ped-life-{page_no}-{idx}", size=6.8, leading=8.5, color=MUTED))
        chip(c, entry["status"], x + 13, yy + 12, compact=True)


def draw_portraits(c, manifest: dict, people: dict, group: dict, page_no: int) -> None:
    accent = RUST if group["side"] == "Sverker" else BLUE
    y = page_title(c, page_no, "32 kompakta porträtt", group["title"], "Varje kort bygger på den konsoliderade personakten. Kortet är en ingång, inte en ersättning för aktens fulla påståenden, konflikter och provenans.", accent, "Personporträtt")
    by_id = {p["person_id"]: p for p in manifest["depth5_positions"]}
    gap_x, gap_y = 10, 11
    w = (PAGE_W - 2 * MARGIN - gap_x) / 2
    h = 265
    for idx, person_id in enumerate(group["ids"]):
        entry = by_id[person_id]
        person = people[person_id]
        summary, citations = select_portrait_text(person, entry)
        row, col = divmod(idx, 2)
        x = MARGIN + col * (w + gap_x)
        yy = y - (row + 1) * h - row * gap_y
        fill = SOFT_GOLD if entry["status"] == "CONFLICT" else WHITE
        card(c, x, yy, w, h, fill=fill)
        c.setFillColor(accent)
        c.rect(x, yy + h - 5, w, 5, fill=1, stroke=0)
        top = para(c, entry["name"], x + 13, yy + h - 18, w - 26, style(f"portrait-name-{person_id}", font="Georgia-Bold", size=11.2, leading=13))
        top = para(c, entry["life"] + "  |  " + entry["place"], x + 13, top - 3, w - 26, style(f"portrait-life-{person_id}", font="Arial-Bold", size=6.9, leading=8.5, color=MUTED))
        para(c, summary, x + 13, top - 11, w - 26, style(f"portrait-body-{person_id}", size=7.55, leading=10.1))
        chip(c, entry["status"], x + 13, yy + 13, compact=True)
        c.setFillColor(MUTED)
        c.setFont("Arial", 5.7)
        c.drawRightString(x + w - 12, yy + 35, clean("Källor: " + ", ".join(citations[:4])))


def draw_story(c, story: dict, page_no: int) -> None:
    accent = RUST if story["side"] == "Sverker" else BLUE
    y = page_title(c, page_no, story["side"] + "s sida", story["title"], story["lead"], accent, "Fördjupning")
    for idx, point in enumerate(story["points"], 1):
        card(c, MARGIN, y - 97, PAGE_W - 2 * MARGIN, 82, fill=WHITE)
        c.setFillColor(accent)
        c.setFont("Georgia-Bold", 21)
        c.drawString(MARGIN + 17, y - 62, f"{idx:02d}")
        para(c, point, MARGIN + 65, y - 31, PAGE_W - 2 * MARGIN - 82, BODY)
        y -= 100
    card(c, MARGIN, 70, PAGE_W - 2 * MARGIN, 85, fill=SOFT_RUST if story["side"] == "Sverker" else SOFT_BLUE)
    rich_para(c, "<b>Verifieringsankare.</b> " + ", ".join(story["citations"]), MARGIN + 14, 135, PAGE_W - 2 * MARGIN - 28, SMALL)
    para(c, "Längre transkriptioner, negativa kontroller och fullständig identitetsanalys finns i person- och citationsakterna.", MARGIN + 14, 105, PAGE_W - 2 * MARGIN - 28, TINY)


def build_map_assets(manifest: dict) -> tuple[Path, list[dict]]:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    base = json.loads(V1_MANIFEST_PATH.read_text())
    map_data = deepcopy(base["map"])
    for idx, place in enumerate(manifest["extra_places"], 1):
        item = deepcopy(place)
        item["id"] = f"PL-V2-{idx}"
        item["branch"] = "Zingmark" if item["branch"] == "Sverker" else "Henriksson"
        item.setdefault("events", ["livsplats"])
        item.setdefault("approximate", True)
        map_data["places"].append(item)
    map_manifest = {"map": map_data}
    path = TMP_DIR / "sweden-depth5.png"
    V1.generate_map(map_manifest, path)
    return path, map_data["places"]


def draw_map(c, page_no: int, map_path: Path) -> None:
    page_title(c, page_no, "Geografin", "Ett släktträd över nästan hela Sverige", "Punkterna är moderna orienteringspunkter för källstödda livsplatser, inte exakta historiska gårdskoordinater. Linjerna visar några av de rörelser som faktiskt kan följas.", SAGE, "Plats")
    c.drawImage(str(map_path), MARGIN, 48, width=PAGE_W - 2 * MARGIN, height=610, preserveAspectRatio=True, anchor="c", mask="auto")
    card(c, PAGE_W - MARGIN - 150, 72, 150, 91, fill=colors.Color(1, 1, 1, alpha=0.92))
    rich_para(c, "<b>Färgspår</b><br/><font color='#9A4A35'>Sörmland och Västergötland</font><br/><font color='#356F8E'>Västerbotten</font><br/><font color='#718168'>Medelpad</font><br/><font color='#754252'>Höök och Carlman</font>", PAGE_W - MARGIN - 138, 150, 126, TINY)
    c.setFillColor(MUTED)
    c.setFont("Arial", 5.5)
    c.drawString(MARGIN, 50, "Kontur: Natural Earth 1:10m v5.1.1. Basorter: OpenStreetMap Nominatim 2026-08-22; fyra djup-5-tillägg är uttryckligt ungefärliga.")


def draw_places(c, page_no: int, places: list[dict]) -> None:
    y = page_title(c, page_no, "Platsindex", "Orterna bakom kartans punkter", "Perioden anger den del av livskedjan som utgåvans källor knyter till platsen. Samma person kan därför finnas vid flera punkter.", SAGE, "Plats")
    gap = 18
    col_w = (PAGE_W - 2 * MARGIN - gap) / 2
    per_col = math.ceil(len(places) / 2)
    for idx, place in enumerate(places):
        col = idx // per_col
        row = idx % per_col
        x = MARGIN + col * (col_w + gap)
        yy = y - row * 45
        c.setFillColor(SAGE)
        c.circle(x + 8, yy - 4, 8, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Arial-Bold", 5.5)
        c.drawCentredString(x + 8, yy - 6, str(idx + 1))
        rich_para(c, "<b>" + esc(place["label"]) + "</b>  <font color='#64717A'>" + esc(place.get("region", "")) + "</font><br/><font size='6.2'>" + esc(place.get("period", "")) + "  |  " + esc(", ".join(place.get("citations", [])[:3])) + "</font>", x + 22, yy + 5, col_w - 22, TINY)


def draw_timeline(c, manifest: dict, page_no: int, events: list[dict], title: str, intro: str) -> None:
    y = page_title(c, page_no, "Tidslinje", title, intro, GOLD, "Tid")
    x_line = MARGIN + 73
    c.setStrokeColor(LINE)
    c.setLineWidth(2)
    c.line(x_line, 85, x_line, y - 8)
    step = 132 if len(events) <= 4 else 112
    for idx, event in enumerate(events):
        yy = y - 42 - idx * step
        c.setFillColor(GOLD)
        c.circle(x_line, yy, 7, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Georgia-Bold", 13)
        c.drawRightString(x_line - 18, yy - 4, clean(event["date"]))
        card(c, x_line + 20, yy - 50, PAGE_W - MARGIN - x_line - 20, 101, fill=WHITE)
        para(c, event["text"], x_line + 34, yy + 31, PAGE_W - MARGIN - x_line - 48, SMALL)
        para(c, "Källor: " + ", ".join(event["citations"]), x_line + 34, yy - 22, PAGE_W - MARGIN - x_line - 48, TINY)


def rasterize_source_pdf(source: Path) -> Path:
    output_prefix = TMP_DIR / source.stem
    output = output_prefix.with_suffix(".png")
    subprocess.run(
        ["pdftoppm", "-png", "-singlefile", "-r", "180", str(source), str(output_prefix)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return output


def draw_fitted_image(c, path: Path, x: float, y: float, w: float, h: float) -> None:
    image = Image.open(path)
    iw, ih = image.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(image), x + (w - dw) / 2, y + (h - dh) / 2, width=dw, height=dh, mask="auto")


def draw_close_reading(c, page_no: int, item: dict) -> None:
    y = page_title(c, page_no, "Källan i närbild", item["title"], "En källbild blir användbar först när dess exakta ord, sammanhang och gränser redovisas. Därför står avskrift, belägg och icke-belägg bredvid bilden.", BURGUNDY, "Källnärläsning")
    source = ROOT / item["image"]
    if source.suffix.lower() == ".pdf":
        source = rasterize_source_pdf(source)
    image_h = 330
    card(c, MARGIN, y - image_h, PAGE_W - 2 * MARGIN, image_h, fill=PAPER_DEEP)
    draw_fitted_image(c, source, MARGIN + 10, y - image_h + 10, PAGE_W - 2 * MARGIN - 20, image_h - 20)
    top = y - image_h - 18
    card(c, MARGIN, top - 105, PAGE_W - 2 * MARGIN, 95, fill=WHITE)
    rich_para(c, "<b>Varsam avskrift</b><br/>" + esc(item["transcription"]), MARGIN + 13, top - 20, PAGE_W - 2 * MARGIN - 26, SMALL)
    gap = 12
    w = (PAGE_W - 2 * MARGIN - gap) / 2
    for idx, (label, text_value, fill) in enumerate((("Detta visar raden", item["proves"], SOFT_GREEN), ("Detta visar den inte", item["does_not_prove"], SOFT_GOLD))):
        x = MARGIN + idx * (w + gap)
        card(c, x, 67, w, 126, fill=fill)
        para(c, label, x + 13, 174, w - 26, style(f"close-label-{page_no}-{idx}", font="Georgia-Bold", size=10.5, leading=12))
        para(c, text_value, x + 13, 143, w - 26, SMALL)
    c.setFillColor(MUTED)
    c.setFont("Arial-Bold", 6)
    c.drawRightString(PAGE_W - MARGIN, 55, item["citation"])


def draw_source_method(c, page_no: int) -> None:
    y = page_title(c, page_no, "Källkritik", "Från arkivbild till familjeberättelse", "Ingen källa svarar på allt. Metoden kombinerar källor efter deras syfte och bevarar varje steg från observation till konsoliderad slutsats.", SAGE, "Metod")
    steps = [
        ("1", "Lokalisera", "Volym, sida, bild-id och sökväg sparas; en registerträff ersätter inte originalet."),
        ("2", "Läs", "Det som faktiskt står transkriberas innan namn, datum och orter normaliseras."),
        ("3", "Pröva identitet", "Kronologi, geografi, hushåll, relationer och yrke måste bilda en sammanhängande person."),
        ("4", "Väg belägg", "Samstämmighet, konflikt, ägarkunskap och nollresultat får skilda statusar."),
        ("5", "Berätta", "Utgåvan sammanfattar; personakter och citationsakter behåller full provenans och återstartvägar."),
    ]
    for idx, (num, title, body) in enumerate(steps):
        yy = y - idx * 90
        c.setFillColor(SAGE)
        c.circle(MARGIN + 17, yy - 27, 15, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Georgia-Bold", 12)
        c.drawCentredString(MARGIN + 17, yy - 31, num)
        para(c, title, MARGIN + 45, yy - 12, 110, style(f"method-title-{idx}", font="Georgia-Bold", size=11, leading=13))
        para(c, body, MARGIN + 158, yy - 10, PAGE_W - MARGIN - (MARGIN + 158), SMALL)
    card(c, MARGIN, 67, PAGE_W - 2 * MARGIN, 128, fill=SOFT_GREEN)
    rich_para(c, "<b>Källfamiljer i den här utgåvan</b><br/>Födelse-, vigsel- och dödböcker  |  husförhör och församlingsböcker  |  folkräkningar och SCB-utdrag  |  flyttlängder  |  rotemansarkiv  |  press och missionshistoria  |  barnhusrulla  |  boupptecknings-, skatt/mantal- och yrkesvägar  |  namngivna familjeuppgifter", MARGIN + 14, 174, PAGE_W - 2 * MARGIN - 28, SMALL)


def draw_fronts(c, manifest: dict, page_no: int) -> None:
    y = page_title(c, page_no, "Ärlig ofullständighet", "Konflikter och arkivfronter", "En färdigbehandlad generation betyder inte att varje detalj är känd. Det betyder att osäkerheten är avgränsad, klassificerad och möjlig att återuppta med en konkret ny nyckel.", GOLD, "Forskningsfront")
    for idx, text_value in enumerate(manifest["fronts_and_conflicts"]):
        row, col = divmod(idx, 2)
        w = (PAGE_W - 2 * MARGIN - 12) / 2
        h = 172
        x = MARGIN + col * (w + 12)
        yy = y - (row + 1) * h - row * 12
        card(c, x, yy, w, h, fill=SOFT_GOLD if idx < 5 else SOFT_BLUE)
        chip(c, "CONFLICT" if idx < 5 else "FRONT", x + 13, yy + h - 31, compact=True)
        para(c, text_value, x + 13, yy + h - 51, w - 26, SMALL)


def citation_record(citation_id: str) -> tuple[str, str]:
    title, location = V1.citation_record(citation_id)
    return clean(title), clean(location)


def draw_references(c, page_no: int, ids: list[str], part: int) -> None:
    y = page_title(c, page_no, "Verifiera själv", f"Exakta hänvisningar - {part}", "Varje C-nummer leder till en full citationsakt i projektarkivet med källställe, avskrift, identitetsbedömning och lokalt bevarat material när det finns.", RUST, "Hänvisningar")
    gap = 14
    col_w = (PAGE_W - 2 * MARGIN - gap) / 2
    per_col = math.ceil(len(ids) / 2)
    item_h = 73
    for idx, citation_id in enumerate(ids):
        col = idx // per_col
        row = idx % per_col
        x = MARGIN + col * (col_w + gap)
        yy = y - row * item_h
        title, location = citation_record(citation_id)
        if len(location) > 230:
            location = location[:227].rsplit(" ", 1)[0] + "..."
        rich_para(c, "<b>" + esc(title) + "</b>", x, yy, col_w, style(f"ref-title-{page_no}-{idx}", size=6.7, leading=8.0))
        para(c, location, x, yy - 17, col_w, style(f"ref-body-{page_no}-{idx}", size=5.8, leading=7.2, color=MUTED))


def draw_colophon(c, manifest: dict, page_no: int) -> None:
    y = page_title(c, page_no, "Utgåveprotokoll", "En fryst berättelse ur ett levande arkiv", "PDF:en är en läsutgåva. Det underliggande familjearkivet fortsätter att bevara observationer append-only och låter den kanoniska personmodellen revideras när ny evidens tillkommer.", BURGUNDY, "Kolofon")
    stats = [
        ("32", "personer på djup 5"), ("16 + 16", "balans mellan sidorna"),
        ("2 672", "validerade påståenden"), ("642", "källakter"),
        ("827", "citationsakter"), ("4 346", "bevarade mediefiler"),
    ]
    gap = 10
    w = (PAGE_W - 2 * MARGIN - 2 * gap) / 3
    for idx, (value, label) in enumerate(stats):
        row, col = divmod(idx, 3)
        x = MARGIN + col * (w + gap)
        yy = y - (row + 1) * 112 - row * 12
        card(c, x, yy, w, 112, fill=WHITE)
        para(c, value, x + 10, yy + 80, w - 20, style(f"stat-{idx}", font="Georgia-Bold", size=18, leading=21, align=TA_CENTER))
        para(c, label, x + 10, yy + 46, w - 20, style(f"stat-label-{idx}", size=6.8, leading=8.2, color=MUTED, align=TA_CENTER))
    card(c, MARGIN, 121, PAGE_W - 2 * MARGIN, 205, fill=SOFT_BLUE)
    rich_para(c, "<b>Utgåveidentitet</b><br/>Manifest: genealogy/editions/adam-axel-depth5-v2.json<br/>Beslut: PCD-2026-09-04-002<br/>Kunskapsläge: 2026-09-04<br/>Tidigare utgåva: adam-axel-depth4-v1, bevarad med SHA-256 fbb9e906ae2a20093e502e38bf5dcb2d8f0b9d3651536c64e1d6de5336870803<br/><br/><b>Kvalitetsprincip</b><br/>Ingen LEAD-, CONFLICT-, REJECTED- eller UNKNOWN-relation förs vidare som etablerad anlinje. OWNER_CONFIRMED är sann projektinformation med separat beslutsspår. Fullständiga källkedjor och återstartvillkor finns i repositoryts person-, käll- och citationsakter.", MARGIN + 16, 304, PAGE_W - 2 * MARGIN - 32, SMALL)
    c.setFillColor(BURGUNDY)
    c.setFont("Georgia-Italic", 12)
    c.drawCentredString(PAGE_W / 2, 88, "För Adam och Axel - med källorna synliga.")


def build(pdf_path: Path) -> None:
    register_fonts()
    manifest = json.loads(MANIFEST_PATH.read_text())
    project = json.loads(PROJECT_DATA_PATH.read_text())
    people = {p["id"]: p for p in project["people"]}
    missing = [p["person_id"] for p in manifest["depth5_positions"] if p["person_id"] not in people]
    if missing:
        raise ValueError(f"Depth-5 people missing from project data: {missing}")
    if len(manifest["depth5_positions"]) != 32:
        raise ValueError("The depth-5 edition must contain exactly 32 positions")

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    map_path, map_places = build_map_assets(manifest)
    c = canvas.Canvas(str(pdf_path), pagesize=A4, pageCompression=1)
    c.setTitle(clean(manifest["edition"]["title"]))
    c.setAuthor("Sverker Janson | källstyrt familjearkiv")
    c.setSubject("Privat djup-5-utgåva för Adam och Axel Janson")
    c.setKeywords("släktforskning, Janson, Höök, Riksarkivet, familjehistoria, djup 5")

    draw_cover(c, manifest); page_done(c)
    draw_changes(c, manifest, 2); page_done(c)
    draw_evidence(c, 3); page_done(c)
    draw_roots(c, 4); page_done(c)
    positions = manifest["depth5_positions"]
    depth_pages = [
        (positions[0:8], "Sverkers sida - Sörmland och Västergötland", "Föräldrarna bakom Bernhard, Ada, Axel Edvard och Hulda Amalia.", RUST),
        (positions[8:16], "Sverkers sida - Västerbotten", "Föräldrarna bakom Johan Oskar, Ida Sofia, Anders Alfred och Anna Fredrika.", RUST),
        (positions[16:24], "Kristinas sida - Fredberg, Hök och Carlman", "Föräldrarna bakom Johannes Ivar, Anna Matilda, Johan Fredrik Villehad och Elin.", BLUE),
        (positions[24:32], "Kristinas sida - Lagfors och Indal", "Föräldrarna bakom Erik Jonas, Gertrud, Anders Niklas och Ingrid.", BLUE),
    ]
    for offset, (entries, title, intro, accent) in enumerate(depth_pages, 5):
        draw_depth5(c, entries, offset, title, intro, accent); page_done(c)
    for page_no, group in enumerate(manifest["portrait_groups"], 9):
        draw_portraits(c, manifest, people, group, page_no); page_done(c)
    for page_no, story in enumerate(manifest["feature_stories"], 17):
        draw_story(c, story, page_no); page_done(c)
    draw_map(c, 21, map_path); page_done(c)
    draw_places(c, 22, map_places); page_done(c)
    draw_timeline(c, manifest, 23, manifest["timeline"][:4], "Från 1825 till hushållens genombrott", "Djup-5-generationen formas under ett halvsekel av lokala samhällen, flyttningar och nya familjehushåll."); page_done(c)
    draw_timeline(c, manifest, 24, manifest["timeline"][4:], "Från nästa generation till dagens arkiv", "Livslinjer sluts, konflikter avgränsas och ett modernt projekt gör det möjligt att se båda familjesidorna samtidigt."); page_done(c)
    for page_no, item in enumerate(manifest["source_close_readings"], 25):
        draw_close_reading(c, page_no, item); page_done(c)
    draw_source_method(c, 27); page_done(c)
    draw_fronts(c, manifest, 28); page_done(c)
    refs = manifest["reference_citations"]
    draw_references(c, 29, refs[:16], 1); page_done(c)
    draw_references(c, 30, refs[16:], 2); page_done(c)
    draw_colophon(c, manifest, 31)
    c.save()
    print(pdf_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_PDF)
    args = parser.parse_args()
    build(args.output.resolve())


if __name__ == "__main__":
    main()
