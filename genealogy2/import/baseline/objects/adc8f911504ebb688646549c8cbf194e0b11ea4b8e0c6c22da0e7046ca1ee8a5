#!/usr/bin/env python
"""Verify structure, content, grayscale design and preserved editions for v3."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / "output/pdf/adam-och-axel-janson-fem-generationer-v3.pdf"
EDITION_PATH = ROOT / "genealogy/editions/adam-axel-depth5-v3.json"
CONTENT_PATH = ROOT / "genealogy/editions/adam-axel-depth5-v2.json"
PROJECT_DATA_PATH = ROOT / "dashboard/public/data/project.json"
A4_PORTRAIT = (595.276, 841.89)
A4_LANDSCAPE = (841.89, 595.276)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_gray(value) -> bool:
    if value is None or isinstance(value, (int, float)):
        return True
    if isinstance(value, (list, tuple)):
        if len(value) == 1:
            return True
        if len(value) in {3, 4}:
            return max(value[:3]) - min(value[:3]) < 0.002
    return False


def near(actual: tuple[float, float], expected: tuple[float, float]) -> bool:
    return abs(actual[0] - expected[0]) < 0.25 and abs(actual[1] - expected[1]) < 0.25


def verify(path: Path) -> None:
    errors: list[str] = []
    edition = json.loads(EDITION_PATH.read_text())
    content = json.loads(CONTENT_PATH.read_text())
    project = json.loads(PROJECT_DATA_PATH.read_text())
    project_people = {person["id"] for person in project["people"]}
    positions = content.get("depth5_positions", [])

    if edition.get("schema") != "slaktforsk.family-edition.v3":
        errors.append("unexpected version-3 manifest schema")
    if edition.get("content_manifest") != "genealogy/editions/adam-axel-depth5-v2.json":
        errors.append("version 3 is not pinned to the frozen version-2 content manifest")
    if edition.get("editorial_decision") != "PCD-2026-09-04-004":
        errors.append("version 3 is not linked to the owner design decision")
    if edition.get("layout_contract", {}).get("target_pages") != 16:
        errors.append("version-3 layout contract does not promise 16 pages")
    for preserved in edition.get("preserved_editions", []):
        preserved_path = ROOT / preserved["path"]
        if not preserved_path.is_file():
            errors.append(f"missing preserved edition: {preserved['path']}")
        elif sha256(preserved_path) != preserved["sha256"]:
            errors.append(f"preserved edition checksum changed: {preserved['path']}")

    if len(positions) != 32:
        errors.append(f"expected 32 depth-5 positions, got {len(positions)}")
    if len({entry.get("code") for entry in positions}) != 32:
        errors.append("depth-5 position codes are not unique")
    if len({entry.get("person_id") for entry in positions}) != 32:
        errors.append("depth-5 person ids are not unique")
    if {entry.get("person_id") for entry in positions} - project_people:
        errors.append("version-3 content contains people missing from project data")
    if sum(entry.get("branch") == "Sverker" for entry in positions) != 16:
        errors.append("version-3 content is not 16 positions on Sverker's side")
    if sum(entry.get("branch") == "Kristina" for entry in positions) != 16:
        errors.append("version-3 content is not 16 positions on Kristina's side")

    goal_state = json.loads(subprocess.run(
        ["node", "scripts/goal-state.mjs", "--json"], cwd=ROOT, check=True,
        text=True, stdout=subprocess.PIPE,
    ).stdout)
    depth5 = [person for person in goal_state["persons"] if person["depth"] == 5]
    if {entry["person_id"] for entry in positions} != {person["id"] for person in depth5}:
        errors.append("version-3 person set does not match current goal-state depth 5")
    if goal_state.get("sharedDepth", 0) < 5 or not all(p.get("reviewed") and p.get("coverageReady") for p in depth5):
        errors.append("goal-state depth 5 is not fully reviewed and coverage-ready")

    for item in content.get("source_close_readings", []):
        if not (ROOT / item["image"]).is_file():
            errors.append(f"missing close-reading source: {item['image']}")
    for citation_id in content.get("reference_citations", []):
        if not list((ROOT / "genealogy/citations").glob(f"{citation_id}-*.md")):
            errors.append(f"missing reference citation file: {citation_id}")

    reader = PdfReader(str(path))
    if len(reader.pages) != 16:
        errors.append(f"expected 16 pages, got {len(reader.pages)}")
    metadata = reader.metadata or {}
    if metadata.get("/Title") != "Adam och Axel Janson - fem generationer bakåt":
        errors.append(f"unexpected title metadata: {metadata.get('/Title')!r}")
    if metadata.get("/Subject") != "Avskalad privat djup-5-utgåva för Adam och Axel Janson":
        errors.append(f"unexpected subject metadata: {metadata.get('/Subject')!r}")

    page_texts = [(page.extract_text() or "") for page in reader.pages]
    all_text = "\n".join(page_texts)
    required = [
        "Adam & Axel Janson", "32 av 32", "Läsnyckel, ändringar och metod",
        "SAMSTÄMMIGA BELÄGG", "SÄKER FAMILJEKUNSKAP", "ÖPPEN KÄLLKONFLIKT",
        "Adam och Axel via Sverker", "Adam och Axel via Kristina",
        "Orterna bakom släktlinjerna", "Natural Earth", "OpenStreetMap Nominatim",
        "Tidslinje, konflikter och återstartvägar", "Ivar i folkräkningen 1930",
        "Barnhusrulla 2532", "PCD-2026-08-29-001", "PCD-2026-09-03-003",
        "2 672", "642", "827", "4 346", "PCD-2026-09-04-004",
    ]
    required.extend(story["title"] for story in content["feature_stories"])
    required.extend(event["text"] for event in content["timeline"])
    required.extend(content["fronts_and_conflicts"])
    required.extend(content["reference_citations"])
    for phrase in required:
        if clean_for_match(phrase) not in clean_for_match(all_text):
            errors.append(f"missing required content: {clean_for_match(phrase)[:90]}")
    for entry in positions:
        if entry["code"] not in all_text:
            errors.append(f"missing depth-5 code: {entry['code']}")
        if entry["name"] not in all_text:
            errors.append(f"missing depth-5 name: {entry['name']}")
    for story in content["feature_stories"]:
        for point in story["points"]:
            if clean_for_match(point) not in clean_for_match(all_text):
                errors.append(f"missing story point: {clean_for_match(point)[:90]}")
    for item in content["source_close_readings"]:
        for field in ("transcription", "proves", "does_not_prove"):
            if clean_for_match(item[field]) not in clean_for_match(all_text):
                errors.append(f"missing close-reading {field}: {clean_for_match(item[field])[:90]}")

    forbidden = ["�", "\u2011", "\u2013", "\u2014"]
    for phrase in forbidden:
        if phrase in all_text:
            errors.append(f"forbidden or damaged text present: {phrase!r}")
    for index, text in enumerate(page_texts, 1):
        minimum = 180 if index == 1 else 300
        if len(text.strip()) < minimum:
            errors.append(f"page {index} has suspiciously little extractable text ({len(text.strip())})")
        if index > 1 and "PRIVAT FAMILJEUTGÅVA" not in text:
            errors.append(f"page {index} footer is not extractable")

    landscape_pages = {3, 4, 11}
    with pdfplumber.open(str(path)) as pdf:
        for index, page in enumerate(pdf.pages, 1):
            actual = (page.width, page.height)
            expected = A4_LANDSCAPE if index in landscape_pages else A4_PORTRAIT
            if not near(actual, expected):
                errors.append(f"page {index}: expected A4 {'landscape' if index in landscape_pages else 'portrait'}, got {actual}")
            for char in page.chars:
                if char["x0"] < -0.2 or char["x1"] > page.width + 0.2 or char["top"] < -0.2 or char["bottom"] > page.height + 0.2:
                    errors.append(f"page {index}: character outside page bounds")
                    break
            for kind in ("chars", "lines", "rects", "curves"):
                for obj in getattr(page, kind):
                    for key in ("stroking_color", "non_stroking_color"):
                        if not is_gray(obj.get(key)):
                            errors.append(f"page {index}: non-grayscale {kind[:-1]} {key}: {obj.get(key)}")
                            break
            for rect in page.rects:
                if rect.get("fill") and rect.get("non_stroking_color") not in (None, 1, 1.0, (1,), [1]):
                    if not (isinstance(rect.get("non_stroking_color"), (tuple, list)) and min(rect["non_stroking_color"][:3]) > 0.995):
                        errors.append(f"page {index}: filled panel is not white")
            if index in {3, 4}:
                if len(page.rects) < 31:
                    errors.append(f"page {index}: pedigree has fewer than 31 visible person nodes")
                if len(page.lines) < 55:
                    errors.append(f"page {index}: pedigree has too few connector lines")

    if errors:
        print(f"Family edition v3 invalid: {path}")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(
        f"OK: {path.name}; 16 A4 pages (13 portrait, 3 landscape); 32 unique depth-5 positions (16/16); "
        "connected pedigree geometry, complete frozen-v2 content, grayscale graphics, bounds, metadata and preserved-edition checksums valid."
    )


def clean_for_match(value: object) -> str:
    return " ".join(str(value or "").replace("\u2010", "-").replace("\u2011", "-").replace("\u2013", "-").replace("\u2014", "-").split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", nargs="?", type=Path, default=DEFAULT_PDF)
    args = parser.parse_args()
    verify(args.pdf.resolve())


if __name__ == "__main__":
    main()
