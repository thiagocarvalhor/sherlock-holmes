"""Generate PNCP API seed manifests from the manually curated Excel file."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_WORKBOOK = ROOT_DIR / "documentation" / "source" / "exemplo_1.xlsx"
DEFAULT_MANIFEST = ROOT_DIR / "data" / "interim" / "pncp" / "manual_manifest.csv"
DEFAULT_SMOKE_SAMPLE = ROOT_DIR / "documentation" / "plans" / "pncp-api-smoke-sample.csv"

TARGET_SHEET_NAME = "CONSOLIDADO"
DATA_START_ROW = 6
SMOKE_SAMPLE_SIZE = 5

NS_MAIN = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
NS_REL = {"rel": "http://schemas.openxmlformats.org/package/2006/relationships"}
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

FIELDNAMES = [
    "source_row",
    "municipio",
    "uf",
    "regiao",
    "populacao",
    "faixa_populacional",
    "objeto_contrato",
    "nome_empresa",
    "revisao_empresas",
    "cnpj",
    "vigencia_inicio",
    "vigencia_inicio_raw",
    "vigencia_fim",
    "vigencia_fim_raw",
    "valor_contrato",
    "numero_contrato",
    "fonte_texto",
    "fonte_url",
    "is_pncp_source",
]

COLUMN_MAP = {
    "B": "municipio",
    "C": "uf",
    "D": "regiao",
    "E": "populacao",
    "F": "faixa_populacional",
    "G": "objeto_contrato",
    "H": "nome_empresa",
    "I": "revisao_empresas",
    "J": "cnpj",
    "K": "vigencia_inicio_raw",
    "L": "vigencia_fim_raw",
    "M": "valor_contrato",
    "N": "numero_contrato",
    "O": "fonte_texto",
}


@dataclass(frozen=True)
class WorkbookSheet:
    name: str
    target: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate PNCP manifests from exemplo_1.xlsx.")
    parser.add_argument("--workbook", type=Path, default=DEFAULT_WORKBOOK)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--smoke-sample", type=Path, default=DEFAULT_SMOKE_SAMPLE)
    parser.add_argument("--smoke-size", type=int, default=SMOKE_SAMPLE_SIZE)
    return parser.parse_args()


def read_xml(zip_file: ZipFile, path: str) -> ET.Element:
    with zip_file.open(path) as file:
        return ET.parse(file).getroot()


def load_shared_strings(zip_file: ZipFile) -> list[str]:
    try:
        root = read_xml(zip_file, "xl/sharedStrings.xml")
    except KeyError:
        return []

    strings: list[str] = []
    for item in root.findall("main:si", NS_MAIN):
        text_parts = [node.text or "" for node in item.findall(".//main:t", NS_MAIN)]
        strings.append("".join(text_parts))
    return strings


def load_sheets(zip_file: ZipFile) -> list[WorkbookSheet]:
    workbook = read_xml(zip_file, "xl/workbook.xml")
    rels = read_xml(zip_file, "xl/_rels/workbook.xml.rels")
    rel_targets = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall("rel:Relationship", NS_REL)
    }

    sheets: list[WorkbookSheet] = []
    for sheet in workbook.findall("main:sheets/main:sheet", NS_MAIN):
        rel_id = sheet.attrib[f"{{{OFFICE_REL_NS}}}id"]
        target = rel_targets[rel_id]
        if not target.startswith("xl/"):
            target = f"xl/{target}"
        sheets.append(WorkbookSheet(name=sheet.attrib["name"], target=target))
    return sheets


def find_sheet(zip_file: ZipFile, sheet_name: str) -> WorkbookSheet:
    for sheet in load_sheets(zip_file):
        if sheet.name.casefold() == sheet_name.casefold():
            return sheet
    raise ValueError(f"Sheet not found: {sheet_name}")


def load_sheet_hyperlinks(zip_file: ZipFile, sheet_path: str) -> dict[str, str]:
    rel_path = sheet_path.replace("xl/worksheets/", "xl/worksheets/_rels/") + ".rels"
    try:
        rels = read_xml(zip_file, rel_path)
    except KeyError:
        return {}

    rel_targets = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall("rel:Relationship", NS_REL)
    }
    sheet = read_xml(zip_file, sheet_path)

    hyperlinks: dict[str, str] = {}
    for hyperlink in sheet.findall("main:hyperlinks/main:hyperlink", NS_MAIN):
        rel_id = hyperlink.attrib.get(f"{{{OFFICE_REL_NS}}}id")
        cell_ref = hyperlink.attrib.get("ref")
        if rel_id and cell_ref and rel_id in rel_targets:
            hyperlinks[cell_ref] = rel_targets[rel_id]
    return hyperlinks


def column_name(cell_ref: str) -> str:
    match = re.match(r"([A-Z]+)", cell_ref)
    if not match:
        raise ValueError(f"Invalid cell reference: {cell_ref}")
    return match.group(1)


def cell_text(cell: ET.Element, shared_strings: list[str]) -> str:
    value = cell.find("main:v", NS_MAIN)
    if value is None or value.text is None:
        inline = cell.find("main:is/main:t", NS_MAIN)
        return inline.text.strip() if inline is not None and inline.text else ""

    raw_value = value.text
    if cell.attrib.get("t") == "s":
        return shared_strings[int(raw_value)].strip()
    return raw_value.strip()


def excel_serial_to_iso(value: str) -> str:
    if not value:
        return ""
    try:
        serial = float(value)
    except ValueError:
        return value

    if serial <= 0:
        return value

    converted = datetime(1899, 12, 30) + timedelta(days=serial)
    return converted.date().isoformat()


def normalize_cnpj(value: str) -> str:
    digits = re.sub(r"\D", "", value)
    if len(digits) == 14:
        return digits
    return value.strip()


def normalize_value(value: str) -> str:
    if not value:
        return ""
    try:
        numeric = float(value)
    except ValueError:
        return value.strip()
    return f"{numeric:.2f}"


def is_meaningful_row(row: dict[str, str]) -> bool:
    return any(row.get(field, "") for field in ("municipio", "nome_empresa", "cnpj", "numero_contrato"))


def build_rows(workbook_path: Path) -> list[dict[str, str]]:
    with ZipFile(workbook_path) as zip_file:
        shared_strings = load_shared_strings(zip_file)
        sheet_info = find_sheet(zip_file, TARGET_SHEET_NAME)
        sheet = read_xml(zip_file, sheet_info.target)
        hyperlinks = load_sheet_hyperlinks(zip_file, sheet_info.target)

        rows: list[dict[str, str]] = []
        for row_element in sheet.findall("main:sheetData/main:row", NS_MAIN):
            row_number = int(row_element.attrib["r"])
            if row_number < DATA_START_ROW:
                continue

            row: dict[str, str] = {field: "" for field in FIELDNAMES}
            row["source_row"] = str(row_number)

            for cell in row_element.findall("main:c", NS_MAIN):
                cell_ref = cell.attrib["r"]
                column = column_name(cell_ref)
                target_field = COLUMN_MAP.get(column)
                if target_field is not None:
                    row[target_field] = cell_text(cell, shared_strings)

            row["cnpj"] = normalize_cnpj(row["cnpj"])
            row["vigencia_inicio"] = excel_serial_to_iso(row["vigencia_inicio_raw"])
            row["vigencia_fim"] = excel_serial_to_iso(row["vigencia_fim_raw"])
            row["valor_contrato"] = normalize_value(row["valor_contrato"])
            row["fonte_url"] = hyperlinks.get(f"O{row_number}", "") or hyperlinks.get(f"N{row_number}", "")
            row["is_pncp_source"] = str(
                "pncp" in row["fonte_texto"].casefold()
                or "pncp" in row["fonte_url"].casefold()
                or "pncp" in row["numero_contrato"].casefold()
            ).lower()

            if is_meaningful_row(row):
                rows.append(row)

    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    rows = build_rows(args.workbook)
    pncp_rows = [row for row in rows if row["is_pncp_source"] == "true"]
    smoke_rows = pncp_rows[: args.smoke_size]

    write_csv(args.manifest, rows)
    write_csv(args.smoke_sample, smoke_rows)

    print(f"Workbook: {args.workbook.relative_to(ROOT_DIR).as_posix()}")
    print(f"Manifest rows: {len(rows)}")
    print(f"PNCP source rows: {len(pncp_rows)}")
    print(f"Smoke sample rows: {len(smoke_rows)}")
    print(f"Manifest: {args.manifest.relative_to(ROOT_DIR).as_posix()}")
    print(f"Smoke sample: {args.smoke_sample.relative_to(ROOT_DIR).as_posix()}")


if __name__ == "__main__":
    main()
