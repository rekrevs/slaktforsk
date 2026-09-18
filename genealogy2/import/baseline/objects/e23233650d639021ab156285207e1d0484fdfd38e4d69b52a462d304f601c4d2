#!/usr/bin/env python
"""Verify version 4's complete trees, complete catalogue and preserved editions."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "output/pdf/adam-och-axel-janson-fem-generationer-v4.pdf"
EDITION_PATH = ROOT / "genealogy/editions/adam-axel-depth5-v4.json"
CONTENT_PATH = ROOT / "genealogy/editions/adam-axel-depth5-v2.json"
PROJECT_DATA_PATH = ROOT / "dashboard/public/data/project.json"
A4_PORTRAIT = (595.276, 841.89)
A4_LANDSCAPE = (841.89, 595.276)


def load_builder():
    path = ROOT / "scripts/build-family-edition-v4.py"
    spec = importlib.util.spec_from_file_location("family_edition_v4_verify", path)
    if not spec or not spec.loader:
        raise RuntimeError("Could not load version-4 edition builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V4 = load_builder()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean(value: object) -> str:
    return " ".join(
        str(value or "")
        .replace("\u2010", "-")
        .replace("\u2011", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .split()
    )


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
    people = {person["id"]: person for person in project["people"]}

    if edition.get("schema") != "slaktforsk.family-edition.v4":
        errors.append("unexpected version-4 manifest schema")
    if edition.get("content_manifest") != "genealogy/editions/adam-axel-depth5-v2.json":
        errors.append("version 4 is not pinned to the frozen version-2 content manifest")
    if edition.get("base_layout_manifest") != "genealogy/editions/adam-axel-depth5-v3.json":
        errors.append("version 4 is not linked to the version-3 layout manifest")
    if edition.get("editorial_decision") != "PCD-2026-09-04-005":
        errors.append("version 4 is not linked to the owner decision")
    if edition.get("layout_contract", {}).get("target_pages") != 43:
        errors.append("version-4 layout contract does not promise 43 pages")
    for preserved in edition.get("preserved_editions", []):
        preserved_path = ROOT / preserved["path"]
        if not preserved_path.is_file():
            errors.append(f"missing preserved edition: {preserved['path']}")
        elif sha256(preserved_path) != preserved["sha256"]:
            errors.append(f"preserved edition checksum changed: {preserved['path']}")

    sides = {
        side: V4.tree_positions(edition, content, side)
        for side in ("Sverker", "Kristina")
    }
    catalogue = sides["Sverker"] + sides["Kristina"]
    if len(catalogue) != 62:
        errors.append(f"expected 62 tree positions, got {len(catalogue)}")
    if len({item["person_id"] for item in catalogue}) != 62:
        errors.append("tree positions do not contain 62 unique people")
    if {item["person_id"] for item in catalogue} - set(people):
        errors.append("tree contains people missing from canonical project data")
    for side, positions in sides.items():
        counts = [sum(item["depth"] == depth for item in positions) for depth in range(1, 6)]
        if counts != [1, 2, 4, 8, 16]:
            errors.append(f"{side} tree shape is {counts}, expected [1, 2, 4, 8, 16]")

    reader = PdfReader(str(path))
    if len(reader.pages) != 43:
        errors.append(f"expected 43 pages, got {len(reader.pages)}")
    metadata = reader.metadata or {}
    if metadata.get("/Title") != "Adam och Axel Janson - fem generationer bakåt":
        errors.append(f"unexpected title metadata: {metadata.get('/Title')!r}")
    if metadata.get("/Subject") != "Komplett privat djup-5-utgåva för Adam och Axel Janson":
        errors.append(f"unexpected subject metadata: {metadata.get('/Subject')!r}")

    page_texts = [(page.extract_text() or "") for page in reader.pages]
    all_text = "\n".join(page_texts)
    normalized_pages = [clean(text) for text in page_texts]
    normalized_all = clean(all_text)

    required = [
        "62 personer i två sammanhängande släktträd",
        "Komplett personkatalog",
        "PCD-2026-09-04-005",
        "Adam och Axel via Sverker",
        "Adam och Axel via Kristina",
        "Orterna bakom släktlinjerna",
        "Tidslinje, konflikter och återstartvägar",
        "Ivar i folkräkningen 1930",
        "Barnhusrulla 2532",
    ]
    required.extend(story["title"] for story in content["feature_stories"])
    required.extend(event["text"] for event in content["timeline"])
    required.extend(content["fronts_and_conflicts"])
    required.extend(content["reference_citations"])
    for phrase in required:
        if clean(phrase) not in normalized_all:
            errors.append(f"missing required content: {clean(phrase)[:90]}")

    for side, page_number in (("Sverker", 3), ("Kristina", 4)):
        tree_text = normalized_pages[page_number - 1]
        for item in sides[side]:
            for field in ("name", "life", "place"):
                if clean(item[field]) not in tree_text:
                    errors.append(f"tree page {page_number} missing {item['person_id']} {field}: {item[field]}")
        if re.search(r"\b(?:D5-|P-\d{4})", tree_text):
            errors.append(f"tree page {page_number} contains a cryptic person or position id")
        for status in V4.V3.STATUS_LABELS.values():
            if clean(status) in tree_text:
                errors.append(f"tree page {page_number} contains evidence-status prose: {status}")

    for index, item in enumerate(catalogue):
        page_number = 5 + index // 2
        text = normalized_pages[page_number - 1]
        person = people[item["person_id"]]
        expected = [
            item["person_id"], item["name"], item["life"], item["place"],
            f"{item['branch']}s sida | djup {item['depth']}", "Känd information", "Citationsakter",
        ]
        for phrase in expected:
            if clean(phrase) not in text:
                errors.append(f"catalogue page {page_number} missing {item['person_id']} field: {phrase}")
        relations = V4.known_relations(people, item["person_id"])
        for relation_people in relations.values():
            for related in relation_people:
                if clean(V4.named_ref(related)) not in text:
                    errors.append(
                        f"catalogue page {page_number} missing known relation for {item['person_id']}: {related['id']}"
                    )
        selected = V4.selected_claims(person)
        selected_citations = {
            citation
            for claim in selected
            for citation in claim.get("citations", [])
            if citation
        }
        if not selected:
            errors.append(f"catalogue entry {item['person_id']} has no selected known information")
        if selected_citations and not any(citation in text for citation in selected_citations):
            errors.append(f"catalogue entry {item['person_id']} lacks readable selected C-reference")

    forbidden = ["�", "\u2011", "\u2013", "\u2014"]
    for phrase in forbidden:
        if phrase in all_text:
            errors.append(f"forbidden or damaged text present: {phrase!r}")
    for index, text in enumerate(page_texts, 1):
        minimum = 150 if index == 1 else 260
        if len(text.strip()) < minimum:
            errors.append(f"page {index} has suspiciously little extractable text ({len(text.strip())})")
        if index > 1 and "PRIVAT FAMILJEUTGÅVA" not in text:
            errors.append(f"page {index} footer is not extractable")

    landscape_pages = {3, 4, 38}
    with pdfplumber.open(str(path)) as pdf:
        for index, page in enumerate(pdf.pages, 1):
            expected = A4_LANDSCAPE if index in landscape_pages else A4_PORTRAIT
            if not near((page.width, page.height), expected):
                errors.append(
                    f"page {index}: expected A4 {'landscape' if index in landscape_pages else 'portrait'}, "
                    f"got {(page.width, page.height)}"
                )
            for char in page.chars:
                if char["x0"] < -0.2 or char["x1"] > page.width + 0.2 or char["top"] < -0.2 or char["bottom"] > page.height + 0.2:
                    errors.append(f"page {index}: character outside page bounds")
                    break
            for kind in ("chars", "lines", "rects", "curves"):
                for obj in getattr(page, kind):
                    if any(not is_gray(obj.get(key)) for key in ("stroking_color", "non_stroking_color")):
                        errors.append(f"page {index}: non-grayscale {kind[:-1]}")
                        break
            for rect in page.rects:
                colour = rect.get("non_stroking_color")
                if rect.get("fill") and colour not in (None, 1, 1.0, (1,), [1]):
                    if not (isinstance(colour, (tuple, list)) and min(colour[:3]) > 0.995):
                        errors.append(f"page {index}: filled panel is not white")
            if index in {3, 4}:
                if len(page.rects) < 31:
                    errors.append(f"page {index}: pedigree has fewer than 31 visible person nodes")
                if len(page.lines) < 55:
                    errors.append(f"page {index}: pedigree has too few connector lines")

    if errors:
        print(f"Family edition v4 invalid: {path}")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(
        f"OK: {path.name}; 43 A4 pages (40 portrait, 3 landscape); two complete 31-node pedigrees; "
        "62 unique catalogue entries with named relations and sourced life summaries; grayscale, bounds, "
        "metadata, frozen content and preserved-edition checksums valid."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", nargs="?", type=Path, default=PDF_PATH)
    args = parser.parse_args()
    verify(args.pdf.resolve())


if __name__ == "__main__":
    main()
