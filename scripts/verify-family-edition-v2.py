#!/usr/bin/env python
"""Structural, content and provenance QA for the depth-5 family edition."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / "output/pdf/adam-och-axel-janson-fem-generationer-v2.pdf"
MANIFEST_PATH = ROOT / "genealogy/editions/adam-axel-depth5-v2.json"
PROJECT_DATA_PATH = ROOT / "dashboard/public/data/project.json"
V1_PDF = ROOT / "output/pdf/adam-och-axel-janson-fyra-generationer-v1.pdf"
V1_SHA256 = "fbb9e906ae2a20093e502e38bf5dcb2d8f0b9d3651536c64e1d6de5336870803"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(path: Path) -> None:
    errors: list[str] = []
    manifest = json.loads(MANIFEST_PATH.read_text())
    project = json.loads(PROJECT_DATA_PATH.read_text())
    people = {person["id"] for person in project["people"]}
    positions = manifest.get("depth5_positions", [])
    goal_state = json.loads(
        subprocess.run(
            ["node", "scripts/goal-state.mjs", "--json"],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout
    )
    goal_depth5 = [person for person in goal_state["persons"] if person["depth"] == 5]

    if manifest.get("schema") != "slaktforsk.family-edition.v2":
        errors.append("unexpected or missing edition manifest schema")
    if len(positions) != 32:
        errors.append(f"expected 32 depth-5 positions, got {len(positions)}")
    codes = [position.get("code") for position in positions]
    person_ids = [position.get("person_id") for position in positions]
    if len(set(codes)) != 32 or len(set(person_ids)) != 32:
        errors.append("depth-5 position codes or person ids are not unique")
    if sum(position.get("branch") == "Sverker" for position in positions) != 16:
        errors.append("depth-5 manifest is not 16 positions on Sverker's side")
    if sum(position.get("branch") == "Kristina" for position in positions) != 16:
        errors.append("depth-5 manifest is not 16 positions on Kristina's side")
    missing_people = sorted(set(person_ids) - people)
    if missing_people:
        errors.append(f"manifest people missing from project data: {missing_people}")
    if set(person_ids) != {person["id"] for person in goal_depth5}:
        errors.append("manifest person set does not exactly match goal-state depth 5")
    if goal_state.get("sharedDepth") < 5:
        errors.append(f"goal-state shared depth is below 5: {goal_state.get('sharedDepth')}")
    if not all(person.get("reviewed") and person.get("coverageReady") for person in goal_depth5):
        errors.append("goal-state depth 5 is not fully reviewed and coverage-ready")
    for close_reading in manifest.get("source_close_readings", []):
        source = ROOT / close_reading["image"]
        if not source.is_file():
            errors.append(f"missing close-reading source: {source.relative_to(ROOT)}")
    for citation_id in manifest.get("reference_citations", []):
        if not list((ROOT / "genealogy/citations").glob(f"{citation_id}-*.md")):
            errors.append(f"missing reference citation file: {citation_id}")
    if sha256(V1_PDF) != V1_SHA256:
        errors.append("historical version-1 PDF checksum changed")

    reader = PdfReader(str(path))
    if len(reader.pages) != 31:
        errors.append(f"expected 31 pages, got {len(reader.pages)}")
    metadata = reader.metadata or {}
    if metadata.get("/Title") != "Adam och Axel Janson - fem generationer bakåt":
        errors.append(f"unexpected title metadata: {metadata.get('/Title')!r}")
    if metadata.get("/Subject") != "Privat djup-5-utgåva för Adam och Axel Janson":
        errors.append(f"unexpected subject metadata: {metadata.get('/Subject')!r}")

    page_texts = [(page.extract_text() or "") for page in reader.pages]
    all_text = "\n".join(page_texts)
    required = [
        "ADAM & AXEL",
        "Vad som ändrats sedan version 1",
        "32 av 32",
        "SÄKER FAMILJEKUNSKAP",
        "PCD-2026-08-29-001",
        "PCD-2026-09-03-003",
        "Johannes Ivar Fredberg",
        "Henrik Henriksson",
        "Margareta Charlotta Sjödin/Sjölin",
        "Barnhusrulla 2532",
        "Ivar i folkräkningen 1930",
        "Från arkivbild till familjeberättelse",
        "Konflikter och arkivfronter",
        "Natural Earth",
        "OpenStreetMap Nominatim",
        "C-0258",
        "C-0606",
        "2 672",
        "642",
        "827",
        "4 346",
    ]
    for phrase in required:
        if phrase not in all_text:
            errors.append(f"missing required text: {phrase}")
    for position in positions:
        if position["code"] not in all_text:
            errors.append(f"missing depth-5 position code: {position['code']}")
        if position["name"] not in all_text:
            errors.append(f"missing depth-5 name: {position['name']}")
    forbidden = [
        "Ivars far är fortfarande okänd",
        "Erik Jonas är en olöst identitet",
        "Hillevis koppling till Oskar Alfred och Ebba Alfrida behöver primärbelägg",
        "Johannes Ivar Fredberg nämns bara som en fortsatt ledtråd",
        "�",
        "\u2011",
        "\u2013",
        "\u2014",
    ]
    for phrase in forbidden:
        if phrase in all_text:
            errors.append(f"forbidden, obsolete or damaged text present: {phrase!r}")

    for index, text in enumerate(page_texts, start=1):
        minimum = 70 if index == 1 else 180
        if len(text.strip()) < minimum:
            errors.append(f"page {index} has suspiciously little extractable text ({len(text.strip())})")
        if index > 1 and "PRIVAT FAMILJEUTGÅVA" not in text:
            errors.append(f"page {index} footer label not extractable")
        if index > 1 and str(index) not in text:
            errors.append(f"page {index} number not extractable")

    with pdfplumber.open(str(path)) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            width, height = page.width, page.height
            if abs(width - 595.276) > 0.2 or abs(height - 841.89) > 0.2:
                errors.append(f"page {index}: not A4 ({width} x {height})")
            for char in page.chars:
                if char["x0"] < -0.2 or char["x1"] > width + 0.2:
                    errors.append(f"page {index}: character outside horizontal page bounds")
                    break
                if char["top"] < -0.2 or char["bottom"] > height + 0.2:
                    errors.append(f"page {index}: character outside vertical page bounds")
                    break

    if errors:
        print(f"Family edition invalid: {path}")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(
        f"OK: {path.name}; 31 A4 pages; 32 unique depth-5 positions (16/16); "
        "required text, sources, bounds, metadata and preserved-v1 checksum valid."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", nargs="?", type=Path, default=DEFAULT_PDF)
    args = parser.parse_args()
    verify(args.pdf.resolve())


if __name__ == "__main__":
    main()
