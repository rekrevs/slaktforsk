#!/usr/bin/env python
"""Structural and text QA for the Adam-and-Axel family PDF."""

from __future__ import annotations

import argparse
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / "output/pdf/adam-och-axel-janson-fyra-generationer-v1.pdf"


def verify(path: Path) -> None:
    errors: list[str] = []
    reader = PdfReader(str(path))
    if len(reader.pages) != 20:
        errors.append(f"expected 20 pages, got {len(reader.pages)}")
    metadata = reader.metadata or {}
    if metadata.get("/Title") != "Adam och Axel Janson – fyra generationer bakåt":
        errors.append(f"unexpected title metadata: {metadata.get('/Title')!r}")

    page_texts = [(page.extract_text() or "") for page in reader.pages]
    all_text = "\n".join(page_texts)
    required = [
        "ADAM JAN GUNNAR JANSON",
        "AXEL IVAR MALTE JANSON",
        "Helsyskonen Marianne",
        "Alla fyra var barn till Elisabeth och Ivar.",
        "Ivars far · okänd",
        "Johannes Ivar Fredberg",
        "Källorna bakom berättelsen",
        "Källbilden är inte dekoration",
        "Vad raden inte bevisar",
        "Källan namnger ingen far",
        "Natural Earth",
        "OpenStreetMap Nominatim",
        "Folk_131974316",
        "B0001195_00465",
        "Forskningsfront – det vi ännu inte vet",
    ]
    for phrase in required:
        if phrase not in all_text:
            errors.append(f"missing required text: {phrase}")
    forbidden = [
        "Ivars far källbelagd",
        "Adam Jan Gunnar Jansson",
        "Axel Ivar Malte Jansson",
        "Johannes Ivar Fredberg var far",
        "Johannes Ivar Fredberg – far",
        "�",
    ]
    for phrase in forbidden:
        if phrase in all_text:
            errors.append(f"forbidden or damaged text present: {phrase}")

    for index, text in enumerate(page_texts, start=1):
        if len(text.strip()) < (80 if index == 1 else 180):
            errors.append(f"page {index} has suspiciously little extractable text ({len(text.strip())})")
        if index > 1 and "PRIVAT FAMILJEUTGÅVA" not in text:
            errors.append(f"page {index} footer label not extractable")

    with pdfplumber.open(str(path)) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            width, height = page.width, page.height
            for char in page.chars:
                if char["x0"] < -0.2 or char["x1"] > width + 0.2:
                    errors.append(f"page {index}: character outside horizontal page bounds")
                    break
                if char["top"] < -0.2 or char["bottom"] > height + 0.2:
                    errors.append(f"page {index}: character outside vertical page bounds")
                    break
            if abs(width - 595.276) > 0.2 or abs(height - 841.89) > 0.2:
                errors.append(f"page {index}: not A4 ({width} x {height})")

    if errors:
        print(f"Family edition invalid: {path}")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"OK: {path.name}; 20 A4 pages; required text present; bounds and metadata valid.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", nargs="?", type=Path, default=DEFAULT_PDF)
    args = parser.parse_args()
    verify(args.pdf.resolve())


if __name__ == "__main__":
    main()
