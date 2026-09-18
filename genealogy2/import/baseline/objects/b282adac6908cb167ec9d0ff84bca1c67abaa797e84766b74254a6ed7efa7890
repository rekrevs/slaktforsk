#!/usr/bin/env python
"""Build the private Adam-and-Axel depth-4 family edition from its manifest."""

from __future__ import annotations

import argparse
import html
import json
import math
import re
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from shapely.geometry import LineString


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "genealogy/editions/adam-axel-depth4-v1.json"
OUT_DIR = ROOT / "output/pdf"
ASSET_DIR = ROOT / "output/family-edition-assets"
DEFAULT_PDF = OUT_DIR / "adam-och-axel-janson-fyra-generationer-v1.pdf"
SWEDEN = ROOT / "genealogy/editions/assets/sweden-outline-natural-earth-5.1.1.geojson"

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

PAPER = colors.HexColor("#F6F0E5")
PAPER_2 = colors.HexColor("#EFE4D3")
INK = colors.HexColor("#24313A")
MUTED = colors.HexColor("#65727A")
LINE = colors.HexColor("#CFC3B1")
WHITE = colors.HexColor("#FFFDFC")
RUST = colors.HexColor("#A14D35")
BLUE = colors.HexColor("#376F8E")
SAGE = colors.HexColor("#78866B")
GOLD = colors.HexColor("#C39149")
BURGUNDY = colors.HexColor("#7B4553")
SOFT_RED = colors.HexColor("#E9D3CB")
SOFT_BLUE = colors.HexColor("#DCE8ED")
SOFT_GREEN = colors.HexColor("#E1E7DB")
SOFT_GOLD = colors.HexColor("#F0E1C5")

STATUS_COLORS = {
    "CORROBORATED": SAGE,
    "TRANSCRIBED": BLUE,
    "LEAD": GOLD,
    "CONFLICT": RUST,
    "UNKNOWN": MUTED,
}
STATUS_LABELS = {
    "CORROBORATED": "SAMSTÄMMIGA BELÄGG",
    "TRANSCRIBED": "AVLÄST / FAMILJEUPPGIFT",
    "LEAD": "LEDTRÅD",
    "CONFLICT": "KÄLLKONFLIKT",
    "UNKNOWN": "DOKUMENTERAT OKÄND",
}


def register_fonts() -> None:
    font_dir = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("Georgia", str(font_dir / "Georgia.ttf")))
    pdfmetrics.registerFont(TTFont("Georgia-Bold", str(font_dir / "Georgia Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Georgia-Italic", str(font_dir / "Georgia Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Arial", str(font_dir / "Arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(font_dir / "Arial Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Italic", str(font_dir / "Arial Italic.ttf")))


def pstyle(
    name: str,
    font: str = "Arial",
    size: float = 9,
    leading: float | None = None,
    color=INK,
    align=TA_LEFT,
    space_after: float = 0,
) -> ParagraphStyle:
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        leading=leading or size * 1.32,
        textColor=color,
        alignment=align,
        spaceAfter=space_after,
        allowWidows=0,
        allowOrphans=0,
    )


BODY = pstyle("body", size=9.1, leading=12.2)
BODY_SMALL = pstyle("body-small", size=7.7, leading=10.2)
BODY_TINY = pstyle("body-tiny", size=6.5, leading=8.2)
CAPTION = pstyle("caption", font="Arial-Italic", size=7, leading=9, color=MUTED)
CARD_TITLE = pstyle("card-title", font="Georgia-Bold", size=11.5, leading=13.2)
CARD_LIFE = pstyle("card-life", font="Arial-Bold", size=7.5, leading=9, color=MUTED)
CARD_BODY = pstyle("card-body", size=8.15, leading=10.6)
CARD_SIB = pstyle("card-sib", size=7.4, leading=9.4, color=MUTED)


def para(c: canvas.Canvas, text: str, x: float, y_top: float, width: float, style=BODY) -> float:
    paragraph = Paragraph(text, style)
    _, height = paragraph.wrap(width, PAGE_H)
    paragraph.drawOn(c, x, y_top - height)
    return y_top - height


def safe(text: str) -> str:
    return html.escape(text, quote=False).replace("\n", "<br/>")


def citations_line(ids: list[str], limit: int = 6) -> str:
    if not ids:
        return ""
    shown = ids[:limit]
    suffix = " …" if len(ids) > limit else ""
    return "Källor: " + ", ".join(shown) + suffix


def status_chip(c: canvas.Canvas, status: str, x: float, y: float, compact: bool = False) -> float:
    label = STATUS_LABELS.get(status, status)
    size = 5.6 if compact else 6.1
    pad_x = 5
    width = pdfmetrics.stringWidth(label, "Arial-Bold", size) + 2 * pad_x
    c.setFillColor(STATUS_COLORS.get(status, MUTED))
    c.roundRect(x, y, width, 13 if not compact else 11.5, 5, fill=1, stroke=0)
    c.setFont("Arial-Bold", size)
    c.setFillColor(WHITE)
    c.drawString(x + pad_x, y + (4 if not compact else 3.5), label)
    return width


def page_background(c: canvas.Canvas, page_no: int, section: str = "") -> None:
    c.setPageSize(A4)
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(MARGIN, 13 * mm, PAGE_W - MARGIN, 13 * mm)
    c.setFillColor(MUTED)
    c.setFont("Arial", 6.5)
    c.drawString(MARGIN, 8.5 * mm, "ADAM & AXEL JANSON · PRIVAT FAMILJEUTGÅVA · 2026-08-22")
    if section:
        c.drawCentredString(PAGE_W / 2, 8.5 * mm, section.upper())
    c.setFont("Arial-Bold", 7)
    c.drawRightString(PAGE_W - MARGIN, 8.5 * mm, str(page_no))


def page_title(
    c: canvas.Canvas,
    page_no: int,
    kicker: str,
    title: str,
    intro: str | None = None,
    accent=RUST,
    section: str = "",
) -> float:
    page_background(c, page_no, section)
    c.setFillColor(accent)
    c.roundRect(MARGIN, PAGE_H - 29 * mm, 28 * mm, 4 * mm, 2 * mm, fill=1, stroke=0)
    c.setFont("Arial-Bold", 7.2)
    c.drawString(MARGIN, PAGE_H - 19 * mm, kicker.upper())
    c.setFillColor(INK)
    c.setFont("Georgia-Bold", 23)
    c.drawString(MARGIN, PAGE_H - 38 * mm, title)
    y = PAGE_H - 45 * mm
    if intro:
        y = para(c, safe(intro), MARGIN, y, PAGE_W - 2 * MARGIN, pstyle("intro", font="Georgia", size=9.5, leading=12.6, color=MUTED))
    return y - 5 * mm


def rounded_card(c, x, y, w, h, fill=WHITE, stroke=LINE, radius=8) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.6)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def draw_portrait_card(c, portrait: dict, x: float, y: float, w: float, h: float, accent, compact=False) -> None:
    rounded_card(c, x, y, w, h)
    c.setFillColor(accent)
    c.roundRect(x, y + h - 5, w, 5, 3, fill=1, stroke=0)
    pad = 10
    top = y + h - 15
    title_style = pstyle("card-title-local", font="Georgia-Bold", size=10.5 if compact else 12, leading=12 if compact else 14)
    top = para(c, safe(portrait["display_name"]), x + pad, top, w - 2 * pad, title_style)
    if portrait.get("life"):
        top = para(c, safe(portrait["life"]), x + pad, top - 2, w - 2 * pad, CARD_LIFE)
    top = para(c, safe(portrait["summary"]), x + pad, top - 7, w - 2 * pad, BODY_SMALL if compact else CARD_BODY)
    sibling = portrait.get("siblings", {})
    if sibling.get("text"):
        sibling_top = y + (76 if h >= 170 else 48)
        c.setStrokeColor(LINE)
        c.line(x + pad, sibling_top + 7, x + w - pad, sibling_top + 7)
        para(
            c,
            "<b>Syskon och uppväxtfamilj.</b> " + safe(sibling["text"]),
            x + pad,
            sibling_top,
            w - 2 * pad,
            pstyle("card-sib-local", size=6.8 if h < 210 else 7.2, leading=8.2 if h < 210 else 9.1, color=MUTED),
        )
    status = sibling.get("status", "TRANSCRIBED")
    status_chip(c, status, x + pad, y + 10, compact=True)
    c.setFillColor(MUTED)
    c.setFont("Arial", 5.8)
    c.drawRightString(x + w - pad, y + 13, citations_line(portrait.get("citations", []), 4))


def draw_generation4_card(c, profile: dict, x: float, y: float, w: float, h: float, accent) -> None:
    fill = SOFT_GOLD if profile["status"] in {"LEAD", "CONFLICT"} else (SOFT_BLUE if profile["status"] == "UNKNOWN" else WHITE)
    rounded_card(c, x, y, w, h, fill=fill)
    c.setFillColor(accent)
    c.rect(x, y, 4, h, fill=1, stroke=0)
    top = y + h - 13
    top = para(c, safe(profile["display_name"]), x + 12, top, w - 24, pstyle("g4-title", font="Georgia-Bold", size=11, leading=12.5))
    top = para(c, safe(profile["life"]), x + 12, top - 1, w - 24, CARD_LIFE)
    para(c, safe(profile["text"]), x + 12, top - 6, w - 24, pstyle("g4-body", size=8.2, leading=10.6))
    rounded_card(c, x + 11, y + 48, w - 22, 82, fill=PAPER, stroke=LINE, radius=5)
    para(c, "<b>Familjekontext.</b> " + safe(profile["context"]), x + 20, y + 118, w - 40, pstyle("g4-context", size=7.2, leading=9.1, color=MUTED))
    status_chip(c, profile["status"], x + 12, y + 10, compact=True)
    c.setFillColor(MUTED)
    c.setFont("Arial", 5.6)
    c.drawRightString(x + w - 10, y + 13, citations_line(profile["citations"], 5))


def branch_group(branch: str) -> str:
    if any(token in branch for token in ["Janson", "Ekholm", "Eliasson"]):
        return "Janson / Ekholm / Eliasson"
    if any(token in branch for token in ["Zingmark", "Andersson"]):
        return "Zingmark / Andersson"
    if any(token in branch for token in ["Henriksson", "Larsson", "Höglund"]):
        return "Henriksson / Larsson / Höglund"
    return "Höök / Carlman"


MAP_COLORS = {
    "Janson / Ekholm / Eliasson": "#A14D35",
    "Zingmark / Andersson": "#376F8E",
    "Henriksson / Larsson / Höglund": "#78866B",
    "Höök / Carlman": "#7B4553",
}


def generate_map(manifest: dict, path: Path) -> None:
    sweden = gpd.read_file(SWEDEN).to_crs(3006)
    places = manifest["map"]["places"]
    points = gpd.GeoDataFrame(
        places,
        geometry=gpd.points_from_xy([p["lon"] for p in places], [p["lat"] for p in places]),
        crs=4326,
    ).to_crs(3006)
    place_by_id = {row["id"]: row for _, row in points.iterrows()}

    fig, ax = plt.subplots(figsize=(6.2, 9.4), dpi=260)
    fig.patch.set_facecolor("#F6F0E5")
    ax.set_facecolor("#F6F0E5")
    sweden.plot(ax=ax, color="#EEE2D0", edgecolor="#59676F", linewidth=0.8, zorder=1)

    for movement in manifest["map"]["movements"]:
        a = place_by_id[movement["from"]].geometry
        b = place_by_id[movement["to"]].geometry
        group = branch_group(place_by_id[movement["from"]]["branch"])
        line = gpd.GeoSeries([LineString([(a.x, a.y), (b.x, b.y)])], crs=3006)
        line.plot(
            ax=ax,
            color=MAP_COLORS[group],
            linewidth=1.0,
            alpha=0.54,
            linestyle=(0, (4, 3)) if movement["status"] == "TRANSCRIBED" else "solid",
            zorder=2,
        )

    for index, (_, row) in enumerate(points.iterrows(), start=1):
        group = branch_group(row["branch"])
        ax.scatter(
            [row.geometry.x],
            [row.geometry.y],
            s=84,
            color=MAP_COLORS[group],
            edgecolor="#FFFDFC",
            linewidth=1.2,
            zorder=4,
        )
        ax.text(
            row.geometry.x,
            row.geometry.y,
            str(index),
            ha="center",
            va="center",
            fontsize=5.4,
            weight="bold",
            color="white",
            zorder=5,
        )

    minx, miny, maxx, maxy = sweden.total_bounds
    ax.set_xlim(minx - 70_000, maxx + 80_000)
    ax.set_ylim(miny - 50_000, maxy + 40_000)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout(pad=0.2)
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def generate_source_crops(manifest: dict, context_path: Path, detail_path: Path) -> None:
    source = ROOT / manifest["close_reading"]["image"]
    image = Image.open(source)
    image.crop((40, 2920, 3600, 3670)).save(context_path, quality=96, subsampling=0, dpi=(300, 300))
    image.crop((210, 3070, 2460, 3570)).save(detail_path, quality=96, subsampling=0, dpi=(300, 300))


def position_life(manifest: dict, person_id: str | None) -> str:
    if not person_id:
        return "okänd"
    for collection in (manifest["portraits"], manifest["generation4_profiles"]):
        for item in collection:
            if item.get("person_id") == person_id:
                return item.get("life", "")
    for root in manifest["roots"]:
        if root["person_id"] == person_id:
            return "född " + root["birth_date"]
    return ""


def position_status(manifest: dict, position: dict) -> str:
    if not position.get("person_id"):
        return "UNKNOWN"
    if position["depth"] == 4:
        for profile in manifest["generation4_profiles"]:
            if profile.get("person_id") == position["person_id"]:
                return profile["status"]
    statuses = [
        link["status"]
        for link in manifest["pedigree"]["parent_links"]
        if link.get("parent") == position.get("person_id")
    ]
    if "LEAD" in statuses:
        return "LEAD"
    return statuses[0] if statuses else "TRANSCRIBED"


def short_name(label: str, max_len: int = 33) -> str:
    label = label.replace(", senare Henriksson", "").replace(", gift Höök", "")
    if len(label) <= max_len:
        return label
    parts = label.split()
    if len(parts) > 3:
        label = " ".join(parts[:2] + [parts[-1]])
    return label if len(label) <= max_len else label[: max_len - 1] + "…"


def draw_tree_box(c, manifest, position, x, center_y, w, h, accent) -> None:
    status = position_status(manifest, position)
    fill = WHITE
    if status == "LEAD":
        fill = SOFT_GOLD
    elif status in {"UNKNOWN", "CONFLICT"}:
        fill = SOFT_RED if status == "CONFLICT" else SOFT_BLUE
    rounded_card(c, x, center_y - h / 2, w, h, fill=fill, radius=5)
    c.setFillColor(accent)
    c.rect(x, center_y - h / 2, 3, h, fill=1, stroke=0)
    if not position.get("person_id") and position.get("terminal_status"):
        name = "Ivars far · okänd"
    else:
        name = short_name(position["label"], 36 if position["depth"] < 4 else 29)
    title = pstyle("tree-name", font="Georgia-Bold", size=7.7 if position["depth"] < 4 else 6.8, leading=8.5 if position["depth"] < 4 else 7.5)
    para(c, safe(name), x + 7, center_y + h / 2 - 8, w - 13, title)
    life = position_life(manifest, position.get("person_id"))
    if life:
        c.setFillColor(MUTED)
        c.setFont("Arial", 5.6)
        c.drawString(x + 7, center_y - h / 2 + 7, life)
    c.setFillColor(STATUS_COLORS.get(status, MUTED))
    c.circle(x + w - 7, center_y - h / 2 + 8, 2.5, fill=1, stroke=0)


def draw_pedigree_page(c, manifest: dict, page_no: int, branch_code: str, accent, title: str, intro: str) -> None:
    page_title(c, page_no, "Antavlan", title, intro, accent=accent, section="Antavla")
    positions = manifest["pedigree"]["positions"]
    levels = []
    for depth in range(1, 5):
        prefix = f"D{depth}-{branch_code}"
        levels.append([p for p in positions if p["code"].startswith(prefix)])
    x_positions = [MARGIN, 157, 289, 431]
    widths = [92, 103, 113, 112]
    heights = [58, 50, 46, 43]
    top, bottom = PAGE_H - 64 * mm, 28 * mm
    centers: dict[str, tuple[float, float, float, float]] = {}
    for level, items in enumerate(levels):
        count = len(items)
        for index, position in enumerate(items):
            center_y = top - (index + 0.5) * (top - bottom) / count
            centers[position["code"]] = (x_positions[level], center_y, widths[level], heights[level])

    c.setStrokeColor(colors.HexColor("#A9A095"))
    c.setLineWidth(0.7)
    for depth in range(1, 4):
        for child in levels[depth - 1]:
            child_x, child_y, child_w, _ = centers[child["code"]]
            for suffix in ("F", "M"):
                parent_code = f"D{depth + 1}-{child['code'].split('-', 1)[1]}{suffix}"
                parent_x, parent_y, _, _ = centers[parent_code]
                mid_x = (child_x + child_w + parent_x) / 2
                c.line(child_x + child_w, child_y, mid_x, child_y)
                c.line(mid_x, child_y, mid_x, parent_y)
                c.line(mid_x, parent_y, parent_x, parent_y)

    for level in levels:
        for position in level:
            x, center_y, w, h = centers[position["code"]]
            draw_tree_box(c, manifest, position, x, center_y, w, h, accent)

    c.setFont("Arial", 6.3)
    c.setFillColor(MUTED)
    for x, label in zip(x_positions, ["FÖRÄLDER", "MOR-/FARFÖRÄLDRAR", "DERAS FÖRÄLDRAR", "DJUP 4"]):
        c.drawString(x, top + 11, label)
    legend_y = 20 * mm
    x = MARGIN
    for status in ["CORROBORATED", "TRANSCRIBED", "LEAD", "CONFLICT", "UNKNOWN"]:
        c.setFillColor(STATUS_COLORS[status])
        c.circle(x + 3, legend_y, 3, fill=1, stroke=0)
        c.setFillColor(MUTED)
        c.setFont("Arial", 5.8)
        label = STATUS_LABELS[status].lower()
        c.drawString(x + 9, legend_y - 2, label)
        x += pdfmetrics.stringWidth(label, "Arial", 5.8) + 24


def draw_cover(c, manifest: dict) -> None:
    c.setPageSize(A4)
    c.setFillColor(INK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor("#55636B"))
    c.setLineWidth(0.8)
    for x in [85, 170, 280, 390, 505]:
        c.line(PAGE_W / 2, 167, x, 310)
        c.circle(x, 310, 4.5, fill=0, stroke=1)
    c.setFillColor(GOLD)
    c.roundRect(MARGIN, PAGE_H - 44 * mm, 32 * mm, 4 * mm, 2 * mm, fill=1, stroke=0)
    c.setFont("Arial-Bold", 8)
    c.drawString(MARGIN, PAGE_H - 31 * mm, "PRIVAT FAMILJEUTGÅVA · VERSION 1")
    c.setFillColor(WHITE)
    c.setFont("Georgia-Bold", 39)
    c.drawString(MARGIN, PAGE_H - 68 * mm, "Adam & Axel")
    c.setFont("Georgia", 24)
    c.drawString(MARGIN, PAGE_H - 84 * mm, "Janson")
    c.setFont("Georgia-Italic", 14)
    c.setFillColor(colors.HexColor("#D9D4CB"))
    c.drawString(MARGIN, PAGE_H - 107 * mm, "Fyra generationer bakåt – och människorna mellan årtalen")

    y = 127 * mm
    c.setStrokeColor(colors.HexColor("#6C787E"))
    c.line(MARGIN, y, PAGE_W - MARGIN, y)
    c.setFont("Arial-Bold", 9)
    c.setFillColor(WHITE)
    c.drawString(MARGIN, y - 12 * mm, "ADAM JAN GUNNAR JANSON")
    c.drawRightString(PAGE_W - MARGIN, y - 12 * mm, "AXEL IVAR MALTE JANSON")
    c.setFont("Arial", 8)
    c.setFillColor(colors.HexColor("#B8C0C3"))
    c.drawString(MARGIN, y - 18 * mm, "född 8 mars 1989")
    c.drawRightString(PAGE_W - MARGIN, y - 18 * mm, "född 26 augusti 1993")

    c.setFillColor(colors.HexColor("#E8E1D7"))
    c.setFont("Georgia", 10)
    c.drawCentredString(PAGE_W / 2, 41 * mm, "En balanserad, källstyrd antavla för två bröder")
    c.setFillColor(colors.HexColor("#9FAAAF"))
    c.setFont("Arial", 7)
    c.drawCentredString(PAGE_W / 2, 28 * mm, "Riksarkivets källor · familjeminnen · karta · tidslinje · källkritiska gränser")
    c.drawCentredString(PAGE_W / 2, 17 * mm, manifest["edition"]["as_of"])


def draw_scope_page(c, manifest: dict, page_no: int) -> None:
    page_title(
        c,
        page_no,
        "Utgåvans ram",
        "En gemensam antavla",
        "Bröderna delar samma antavla. Djup 4 betyder deras 16 teoretiska anpositioner fyra led bakåt – inte att varje vidare gren redan är färdigforskad.",
        accent=GOLD,
        section="Läsanvisning",
    )
    left, gap = MARGIN, 12 * mm
    col = (PAGE_W - 2 * MARGIN - gap) / 2
    y = PAGE_H - 68 * mm
    rounded_card(c, left, y - 92, col, 92, fill=SOFT_RED)
    para(c, "<b>Adam Jan Gunnar Janson</b><br/><font color='#65727A'>född 1989-03-08</font>", left + 12, y - 15, col - 24, pstyle("root-a", font="Georgia-Bold", size=12, leading=15))
    para(c, "Söner till Sverker Adam Janson och Kristina Elisabeth Petronella Janson, född Höök.", left + 12, y - 52, col - 24, BODY_SMALL)
    rounded_card(c, left + col + gap, y - 92, col, 92, fill=SOFT_BLUE)
    para(c, "<b>Axel Ivar Malte Janson</b><br/><font color='#65727A'>född 1993-08-26</font>", left + col + gap + 12, y - 15, col - 24, pstyle("root-x", font="Georgia-Bold", size=12, leading=15))
    para(c, "Efternamnet är <b>Janson</b> med ett s. Det gäller båda bröderna och utgåvans titel.", left + col + gap + 12, y - 52, col - 24, BODY_SMALL)

    y2 = y - 118
    c.setFont("Georgia-Bold", 14)
    c.setFillColor(INK)
    c.drawString(left, y2, "Så läses beläggen")
    yy = y2 - 22
    for entry in manifest["evidence_policy"]["labels"]:
        status_chip(c, entry["status"], left, yy - 4, compact=True)
        para(c, safe(entry["meaning"]), left + 104, yy + 6, col - 104, BODY_TINY)
        yy -= 35

    toc_x = left + col + gap
    c.setFont("Georgia-Bold", 14)
    c.drawString(toc_x, y2, "I den här utgåvan")
    toc = [
        ("Antavlan", "3"),
        ("Personporträtt och syskon", "5"),
        ("Kartan", "12"),
        ("Tidslinjen", "14"),
        ("En handskriven källa i närbild", "16"),
        ("Källorna bakom berättelsen", "17"),
        ("Hänvisningar och forskningsfront", "19"),
    ]
    yy = y2 - 25
    for label, page in toc:
        c.setFont("Arial", 9)
        c.setFillColor(INK)
        c.drawString(toc_x, yy, label)
        c.setStrokeColor(LINE)
        c.setDash(1, 2)
        c.line(toc_x + 125, yy + 2, toc_x + col - 20, yy + 2)
        c.setDash()
        c.setFont("Arial-Bold", 9)
        c.drawRightString(toc_x + col, yy, page)
        yy -= 27

    rounded_card(c, toc_x, 55, col, 100, fill=PAPER_2)
    para(c, "<b>Det viktiga undantaget</b>", toc_x + 12, 140, col - 24, CARD_TITLE)
    para(c, "Ivars far är fortfarande okänd i de lästa originalkällorna. Johannes Ivar Fredberg nämns bara som en fortsatt ledtråd – aldrig som en ruta i antavlan.", toc_x + 12, 112, col - 24, BODY_SMALL)


def draw_nearest_page(c, manifest: dict, page_no: int) -> None:
    page_title(c, page_no, "Personerna", "De närmaste släktleden", "Här hålls nu levande personer avsiktligt korta. Syskonraderna är en del av familjekontexten men utvidgar inte antavlans djup.", accent=GOLD, section="Porträtt")
    portraits = {p["person_id"]: p for p in manifest["portraits"]}
    parents = [portraits["P-0004"], portraits["P-0210"]]
    grandparents = [portraits[i] for i in ["P-0005", "P-0006", "P-0212", "P-0211"]]
    gap = 10
    col = (PAGE_W - 2 * MARGIN - gap) / 2
    y_top = PAGE_H - 68 * mm
    for index, portrait in enumerate(parents):
        draw_portrait_card(c, portrait, MARGIN + index * (col + gap), y_top - 126, col, 126, RUST if index == 0 else BLUE, compact=True)
    y_top -= 145
    card_h = 191
    for index, portrait in enumerate(grandparents):
        row, column = divmod(index, 2)
        draw_portrait_card(c, portrait, MARGIN + column * (col + gap), y_top - (row + 1) * card_h - row * gap, col, card_h, RUST if index < 2 else BLUE, compact=True)


def draw_four_portraits_page(c, manifest, page_no, ids, title, intro, accent) -> None:
    page_title(c, page_no, "Personerna", title, intro, accent=accent, section="Porträtt")
    portraits = {p["person_id"]: p for p in manifest["portraits"]}
    gap = 10
    col = (PAGE_W - 2 * MARGIN - gap) / 2
    top = PAGE_H - 68 * mm
    card_h = 285
    for index, person_id in enumerate(ids):
        row, column = divmod(index, 2)
        y = top - (row + 1) * card_h - row * gap
        draw_portrait_card(c, portraits[person_id], MARGIN + column * (col + gap), y, col, card_h, accent)


def draw_four_generation4(c, manifest, page_no, profiles, title, intro, accent) -> None:
    page_title(c, page_no, "Djup 4", title, intro, accent=accent, section="Fjärde generationen")
    gap = 10
    col = (PAGE_W - 2 * MARGIN - gap) / 2
    top = PAGE_H - 68 * mm
    card_h = 278
    for index, profile in enumerate(profiles):
        row, column = divmod(index, 2)
        y = top - (row + 1) * card_h - row * gap
        draw_generation4_card(c, profile, MARGIN + column * (col + gap), y, col, card_h, accent)


def draw_map_page(c, manifest, page_no, map_path) -> None:
    page_title(c, page_no, "Geografin", "Var livsspåren finns", manifest["map"]["scope_note"], accent=SAGE, section="Karta")
    c.drawImage(str(map_path), MARGIN, 39 * mm, width=365, height=542, preserveAspectRatio=True, anchor="sw", mask="auto")
    x = 440
    y = PAGE_H - 76 * mm
    y = para(c, "<b>Fyra färgade vägstråk</b>", x, y, 105, pstyle("map-side", font="Georgia-Bold", size=11, leading=13)) - 14
    for group, color in MAP_COLORS.items():
        c.setFillColor(colors.HexColor(color))
        c.circle(x + 5, y + 3, 4, fill=1, stroke=0)
        y = para(c, safe(group), x + 16, y + 9, 92, BODY_TINY) - 13
    y -= 7
    para(c, "<b>Linjer</b><br/>Heldragen: samstämmiga belägg.<br/>Streckad: avläst uppgift eller familjeminne.<br/><br/><b>Punkter</b><br/>Numret leder till ortslistan på nästa sida.", x, y, 105, BODY_TINY)
    rounded_card(c, x - 5, 58, 115, 135, fill=PAPER_2)
    para(c, "<b>Ingen falsk precision</b>", x + 6, 180, 93, pstyle("map-note", font="Georgia-Bold", size=9.5, leading=11))
    para(c, "Kartans koordinater är moderna orts- eller kyrkcentrumpunkter från Nominatim. De visar ungefär var i Sverige källhändelsen hör hemma – inte exakt hus eller äga.", x + 6, 150, 93, BODY_TINY)
    c.setFillColor(MUTED)
    c.setFont("Arial", 5.8)
    c.drawString(MARGIN, 26 * mm, "Sverigekontur: Natural Earth 1:10m, Admin 0, version 5.1.1. Ortsdata: OpenStreetMap Nominatim, hämtad 2026-08-22.")


def display_person_names(manifest: dict, ids: list[str]) -> str:
    labels = {p["person_id"]: p["label"] for p in manifest["pedigree"]["positions"] if p.get("person_id")}
    names = [short_name(labels.get(pid, pid), 23) for pid in ids]
    return ", ".join(names[:3]) + (" m.fl." if len(names) > 3 else "")


def draw_places_page(c, manifest, page_no) -> None:
    page_title(c, page_no, "Geografin", "Orterna bakom numren", "Varje punkt har en källbunden person eller händelse, en tidsangivelse och en uttrycklig ungefärlighetsflagga i utgåvemanifestet.", accent=SAGE, section="Karta")
    places = manifest["map"]["places"]
    gap = 15
    col = (PAGE_W - 2 * MARGIN - gap) / 2
    top = PAGE_H - 67 * mm
    item_h = 58
    for index, place in enumerate(places, start=1):
        column = 0 if index <= 9 else 1
        row = (index - 1) % 9
        x = MARGIN + column * (col + gap)
        y = top - row * item_h
        group = branch_group(place["branch"])
        c.setFillColor(colors.HexColor(MAP_COLORS[group]))
        c.circle(x + 9, y - 9, 9, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Arial-Bold", 6.5)
        c.drawCentredString(x + 9, y - 11.5, str(index))
        para(c, safe(place["label"]) + f" <font color='#65727A'>· {safe(place['period'])}</font>", x + 25, y, col - 25, pstyle("place-title", font="Arial-Bold", size=8.2, leading=9.5))
        details = f"{display_person_names(manifest, place['people'])}. {', '.join(place['events'])}."
        para(c, safe(details), x + 25, y - 14, col - 25, BODY_TINY)
        c.setFillColor(MUTED)
        c.setFont("Arial", 5.5)
        c.drawString(x + 25, y - 43, citations_line(place["citations"], 5))


def draw_timeline_page(c, manifest, page_no, events, title, intro) -> None:
    page_title(c, page_no, "Tidslinjen", title, intro, accent=BURGUNDY, section="Tidslinje")
    x_line = 112
    top = PAGE_H - 67 * mm
    bottom = 28 * mm
    step = (top - bottom) / len(events)
    c.setStrokeColor(LINE)
    c.setLineWidth(1.5)
    c.line(x_line, bottom, x_line, top)
    for index, event in enumerate(events):
        y = top - (index + 0.5) * step
        color = STATUS_COLORS[event["status"]]
        c.setFillColor(color)
        c.circle(x_line, y, 5, fill=1, stroke=0)
        c.setFont("Arial-Bold", 8)
        c.setFillColor(INK)
        c.drawRightString(x_line - 15, y - 3, event["date"])
        c.setFillColor(WHITE)
        c.setStrokeColor(LINE)
        c.roundRect(x_line + 18, y - step * 0.35, PAGE_W - MARGIN - x_line - 18, step * 0.72, 6, fill=1, stroke=1)
        para(c, safe(event["text"]), x_line + 30, y + step * 0.26, PAGE_W - MARGIN - x_line - 42, pstyle("timeline-text", size=8.4, leading=10.5))
        c.setFont("Arial", 5.7)
        c.setFillColor(MUTED)
        c.drawRightString(PAGE_W - MARGIN - 8, y - step * 0.24, f"{event['precision']} · {citations_line(event['citations'], 5)}")


def draw_close_reading(c, manifest, page_no, context_path, detail_path) -> None:
    close = manifest["close_reading"]
    page_title(c, page_no, "Så här vet vi", "En rad som löser en identitet", "Källbilden är inte dekoration: kombinationen av tre generationer, familjeställningen och yrket ‘missionär’ binder pojken i Hudiksvall till den vuxne Ivar Höök.", accent=BLUE, section="Källa i närbild")
    c.drawImage(str(context_path), MARGIN, 520, width=PAGE_W - 2 * MARGIN, height=112, preserveAspectRatio=True, anchor="sw")
    para(c, "Originalutsnitt med hushållet på församlingsbokssida 593. Bilden är endast beskuren; ingen handskrift har retuscherats.", MARGIN, 512, PAGE_W - 2 * MARGIN, CAPTION)
    c.drawImage(str(detail_path), MARGIN, 353, width=PAGE_W - 2 * MARGIN, height=138, preserveAspectRatio=True, anchor="sw")
    para(c, "Förstoring av namnen och kolumnerna för familjeställning/yrke.", MARGIN, 344, PAGE_W - 2 * MARGIN, CAPTION)

    gap = 10
    col = (PAGE_W - 2 * MARGIN - 2 * gap) / 3
    boxes = [
        ("Diplomatisk kärnavskrift", close["diplomatic_transcription"], SOFT_BLUE),
        ("Läshjälp", close["reading_help"], PAPER_2),
        ("Vad raden bevisar", close["proves"], SOFT_GREEN),
    ]
    for index, (heading, text, fill) in enumerate(boxes):
        x = MARGIN + index * (col + gap)
        rounded_card(c, x, 154, col, 150, fill=fill)
        para(c, safe(heading), x + 10, 288, col - 20, pstyle(f"close-{index}", font="Georgia-Bold", size=10, leading=12))
        para(c, safe(text), x + 10, 258, col - 20, BODY_SMALL)
    rounded_card(c, MARGIN, 73, PAGE_W - 2 * MARGIN, 65, fill=SOFT_RED)
    para(c, "<b>Vad raden inte bevisar.</b> " + safe(close["does_not_prove"]), MARGIN + 12, 123, PAGE_W - 2 * MARGIN - 24, BODY_SMALL)
    para(c, safe(close["reference"]), MARGIN + 12, 96, PAGE_W - 2 * MARGIN - 24, BODY_TINY)


def draw_sources_page(c, manifest, page_no, sections, title, intro) -> None:
    page_title(c, page_no, "Källorna bakom berättelsen", title, intro, accent=GOLD, section="Källor")
    gap = 12
    col = (PAGE_W - 2 * MARGIN - gap) / 2
    top = PAGE_H - 68 * mm
    card_h = 205
    for index, section in enumerate(sections):
        row, column = divmod(index, 2)
        x = MARGIN + column * (col + gap)
        y = top - (row + 1) * card_h - row * gap
        rounded_card(c, x, y, col, card_h, fill=WHITE)
        para(c, safe(section["heading"]), x + 12, y + card_h - 16, col - 24, pstyle(f"src-title-{index}", font="Georgia-Bold", size=12, leading=14))
        para(c, safe(section["explanation"]), x + 12, y + card_h - 58, col - 24, pstyle(f"src-body-{index}", size=8.5, leading=11.1))
        c.setFillColor(MUTED)
        c.setFont("Arial", 5.7)
        c.drawString(x + 12, y + 12, citations_line(section["used_citations"], 8))


def draw_source_method(c, manifest) -> None:
    method = manifest["source_method"]
    rounded_card(c, MARGIN, 73, PAGE_W - 2 * MARGIN, 330, fill=PAPER_2)
    para(c, safe(method["heading"]), MARGIN + 15, 387, PAGE_W - 2 * MARGIN - 30, pstyle("method-title", font="Georgia-Bold", size=14, leading=16))
    left = MARGIN + 15
    y = 348
    for index, step in enumerate(method["steps"], start=1):
        c.setFillColor(GOLD)
        c.circle(left + 9, y - 2, 9, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Arial-Bold", 7.5)
        c.drawCentredString(left + 9, y - 4.5, str(index))
        para(c, safe(step), left + 28, y + 5, 290, BODY_SMALL)
        y -= 46
    x = 385
    para(c, "Tre frågor för läsaren", x, 348, 145, pstyle("questions-title", font="Georgia-Bold", size=11.5, leading=13.5))
    y = 311
    for question in method["reader_questions"]:
        rounded_card(c, x, y - 47, 145, 47, fill=WHITE, radius=5)
        para(c, safe(question), x + 10, y - 10, 125, pstyle("question", font="Arial-Bold", size=7.8, leading=9.5))
        y -= 62
    para(c, "Den sista frågan – vad posten inte visar – är avgörande för att Fredberg-ledtråden inte ska bli en påhittad far i trädet.", x, 116, 145, BODY_TINY)


def citation_record(citation_id: str) -> tuple[str, str]:
    paths = list((ROOT / "genealogy/citations").glob(f"{citation_id}-*.md"))
    if not paths:
        return citation_id, ""
    text = paths[0].read_text()
    title = text.splitlines()[0].removeprefix("# ").strip()
    if citation_id == "C-0050":
        title = "C-0050: Johan August (senare Johan Oskar Zingmark), född 1861"
    location = ""
    for heading in ["Exakt lokalisering", "Lokalisering", "Hänvisning", "Källställe"]:
        match = re.search(rf"## {re.escape(heading)}\n\n(.*?)(?=\n## |\Z)", text, re.S)
        if match:
            location = re.sub(r"\s+", " ", match.group(1)).strip()
            location = re.sub(r"\[([^]]+)]\([^)]+\)", r"\1", location)
            location = location.replace("`", "")
            break
    if not location:
        location = "Se full citationsakt i det källstyrda projektarkivet."
    return title, location


def draw_references_page(c, manifest, page_no, citation_ids, title, intro, include_front=False) -> None:
    page_title(c, page_no, "Verifiera själv", title, intro, accent=RUST, section="Hänvisningar")
    gap = 13
    col = (PAGE_W - 2 * MARGIN - gap) / 2
    top = PAGE_H - 67 * mm
    per_col = math.ceil(len(citation_ids) / 2)
    item_h = 72 if not include_front else 67
    for index, citation_id in enumerate(citation_ids):
        column = 0 if index < per_col else 1
        row = index if column == 0 else index - per_col
        x = MARGIN + column * (col + gap)
        y = top - row * item_h
        title_text, location = citation_record(citation_id)
        para(c, safe(title_text), x, y, col, pstyle(f"ref-{citation_id}", font="Arial-Bold", size=7.5, leading=9))
        para(c, safe(location[:360] + ("…" if len(location) > 360 else "")), x, y - 15, col, BODY_TINY)
    if include_front:
        rounded_card(c, MARGIN, 58, PAGE_W - 2 * MARGIN, 130, fill=PAPER_2)
        para(c, "Forskningsfront – det vi ännu inte vet", MARGIN + 12, 172, PAGE_W - 2 * MARGIN - 24, pstyle("front-title", font="Georgia-Bold", size=12, leading=14))
        y = 143
        for item in manifest["research_front"]:
            y = para(c, "• " + safe(item), MARGIN + 12, y, PAGE_W - 2 * MARGIN - 24, BODY_SMALL) - 5


def build(pdf_path: Path) -> None:
    register_fonts()
    manifest = json.loads(MANIFEST.read_text())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    map_path = ASSET_DIR / "adam-axel-sweden-map.png"
    context_path = ASSET_DIR / "C-0258-context-crop.jpg"
    detail_path = ASSET_DIR / "C-0258-detail-crop.jpg"
    generate_map(manifest, map_path)
    generate_source_crops(manifest, context_path, detail_path)

    c = canvas.Canvas(str(pdf_path), pagesize=A4, pageCompression=1)
    c.setTitle(manifest["edition"]["title"])
    c.setAuthor("Sverker Janson · källstyrt familjearkiv")
    c.setSubject("Privat familjeutgåva för Adam och Axel Janson")
    c.setKeywords("släktforskning, Janson, Höök, Riksarkivet, familjehistoria")

    draw_cover(c, manifest)
    c.showPage()
    draw_scope_page(c, manifest, 2)
    c.showPage()
    draw_pedigree_page(c, manifest, 3, "F", RUST, "Sverkers gren", "Från Sverker genom Janson, Ekholm, Zingmark och Andersson till åtta positioner på djup 4.")
    c.showPage()
    draw_pedigree_page(c, manifest, 4, "M", BLUE, "Kristinas gren", "Från Kristina genom Höök, Carlman, Henriksson och Larsson. En okänd far visas öppet; inga ledtrådar fyller hans plats.")
    c.showPage()
    draw_nearest_page(c, manifest, 5)
    c.showPage()
    draw_four_portraits_page(c, manifest, 6, ["P-0003", "P-0007", "P-0001", "P-0002"], "Fyra liv på Sverkers sida", "Samma utrymme för fyra olika livsbågar: hantverk, kontorsarbete, vägbygge och skola.", RUST)
    c.showPage()
    draw_four_portraits_page(c, manifest, 7, ["P-0239", "P-0240", "P-0241", "P-0246"], "Fyra liv på Kristinas sida", "Mission, sjukvård och familjeliv binds här till Hudiksvall, Danderyd och Storbränna.", BLUE)
    c.showPage()

    g4 = manifest["generation4_profiles"]
    draw_four_generation4(c, manifest, 8, g4[0:4], "Sörmländska rötter", "Bernhard, Ada, Axel Edvard och Hulda Amalia – fyra föräldrar bakom Arne och Maj.", RUST)
    c.showPage()
    draw_four_generation4(c, manifest, 9, g4[4:8], "Västerbottniska rötter", "Sågverk, jordbruk och långa hushållsspår bakom Oskar Alfred och Ebba Alfrida.", RUST)
    c.showPage()
    draw_four_generation4(c, manifest, 10, g4[8:12], "Hälsingland, Öland och Östergötland", "En dokumenterat okänd far står sida vid sida med tre källidentifierade personer.", BLUE)
    c.showPage()
    draw_four_generation4(c, manifest, 11, g4[12:16], "Medelpadsrötter", "Erik Jonas är en olöst identitet bakåt; Gertrud, Anders Niklas och Ingrid har starkare föräldra- och platskedjor.", BLUE)
    c.showPage()

    draw_map_page(c, manifest, 12, map_path)
    c.showPage()
    draw_places_page(c, manifest, 13)
    c.showPage()
    timeline = manifest["timeline"]
    draw_timeline_page(c, manifest, 14, timeline[:10], "Från 1861 till 1930", "Tidslinjen blandar inte precisioner: exakt dag, årskluster och längre perioder behåller sina källors upplösning.")
    c.showPage()
    draw_timeline_page(c, manifest, 15, timeline[10:], "Från mission till minnets namnbruk", "Arbete, vigslar, flyttning och död ger släktträdet en gemensam historisk rytm.")
    c.showPage()
    draw_close_reading(c, manifest, 16, context_path, detail_path)
    c.showPage()
    source_sections = manifest["source_explanations"]
    draw_sources_page(c, manifest, 17, source_sections[:4], "Källor är skapade för olika syften", "En födelsebok, en folkräkning och ett familjeminne svarar på olika frågor. Därför behöver berättelsen flera källfamiljer.")
    c.showPage()
    draw_sources_page(c, manifest, 18, source_sections[4:], "När arkivet behöver andra röster", "Missionshistoria och familjeminnen ger verksamhet och personlighet – men deras uppgifter märks tydligt och kontrolleras där det går.")
    draw_source_method(c, manifest)
    c.showPage()

    refs_1 = ["C-0008", "C-0020", "C-0040", "C-0043", "C-0050", "C-0067", "C-0232", "C-0240"]
    refs_2 = ["C-0244", "C-0246", "C-0253", "C-0258", "C-0260", "C-0269", "C-0270", "C-0271", "C-0274"]
    draw_references_page(c, manifest, 19, refs_1, "Ett urval exakta hänvisningar · 1", "Varje C-nummer motsvarar en full citationsakt i projektarkivet. Här återges de viktigaste verifieringsankarna i läsbar kortform.")
    c.showPage()
    draw_references_page(c, manifest, 20, refs_2, "Ett urval exakta hänvisningar · 2", "De senaste källfynden stänger flera djup-4-positioner men bevarar också de frågor som ännu är öppna.", include_front=True)
    c.save()

    print(pdf_path)
    print(map_path)
    print(context_path)
    print(detail_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_PDF)
    args = parser.parse_args()
    build(args.output.resolve())


if __name__ == "__main__":
    main()
