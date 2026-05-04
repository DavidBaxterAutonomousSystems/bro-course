#!/usr/bin/env python3
"""Generate docs/bom.md from CSV source data."""

from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.request import urlopen

CANONICAL_FIELDNAMES = [
    "category",
    "item",
    "required",
    "selected",
    "qty",
    "unit_cost",
    "buy_link",
    "notes",
]

REQUIRED_FIELDNAMES = [
    "category",
    "item",
    "required",
    "selected",
    "qty",
    "buy_link",
    "notes",
]

HEADER_ALIASES = {
    "quantity": "qty",
    "unit_price": "unit_cost",
    "price": "unit_cost",
    "cost": "unit_cost",
    "unit_cost_sek": "unit_cost",
    "unit_cost_kr": "unit_cost",
    "buy_url": "buy_link",
    "url": "buy_link",
    "link": "buy_link",
}


@dataclass
class BomRow:
    category: str
    item: str
    required: bool
    selected: bool
    qty: float | None
    unit_cost: float | None
    buy_link: str
    notes: str

    @property
    def est_total(self) -> float | None:
        if self.qty is None or self.unit_cost is None:
            return None
        return self.qty * self.unit_cost


def normalize_header(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", (value or "").strip().lower()).strip("_")
    return HEADER_ALIASES.get(normalized, normalized)


def normalize_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    normalized_rows: list[dict[str, str]] = []
    for row in rows:
        normalized_row: dict[str, str] = {}
        for key, value in row.items():
            normalized_key = normalize_header(key)
            if not normalized_key:
                continue

            normalized_value = (value or "").strip()
            existing_value = normalized_row.get(normalized_key, "")
            if existing_value and not normalized_value:
                continue
            normalized_row[normalized_key] = normalized_value
        normalized_rows.append(normalized_row)
    return normalized_rows


def validate_rows(rows: list[dict[str, str]], source_hint: str) -> None:
    if not rows:
        raise ValueError(f"No rows found in CSV source: {source_hint}")

    discovered_fields: set[str] = set()
    for row in rows:
        discovered_fields.update(row.keys())

    missing = [name for name in REQUIRED_FIELDNAMES if name not in discovered_fields]
    if missing:
        missing_text = ", ".join(missing)
        raise ValueError(f"Missing required CSV columns in {source_hint}: {missing_text}")

    if "unit_cost" not in discovered_fields and "unit_cost_usd" not in discovered_fields:
        raise ValueError(
            f"Missing cost column in {source_hint}: expected `unit_cost` (or legacy `unit_cost_usd`)."
        )


def write_rows_to_local_csv(rows: list[dict[str, str]], csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CANONICAL_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            output_row = {name: (row.get(name, "") or "").strip() for name in CANONICAL_FIELDNAMES}
            if not output_row["unit_cost"]:
                output_row["unit_cost"] = (row.get("unit_cost_usd", "") or "").strip()
            writer.writerow(output_row)


def parse_bool(value: str, *, default: bool = False) -> bool:
    raw = (value or "").strip().lower()
    if not raw:
        return default
    return raw in {"1", "y", "yes", "true", "required", "optional:no"}


def parse_number(value: str) -> float | None:
    raw = (value or "").strip()
    if not raw or raw.upper() == "TBD":
        return None
    return float(raw)


def parse_rows(rows: list[dict[str, str]]) -> list[BomRow]:
    parsed: list[BomRow] = []
    for idx, raw_row in enumerate(rows, start=2):
        required = parse_bool(raw_row.get("required", ""), default=False)
        selected = parse_bool(raw_row.get("selected", ""), default=required)
        try:
            qty = parse_number(raw_row.get("qty", ""))
            unit_cost = parse_number(raw_row.get("unit_cost", ""))
            if unit_cost is None:
                unit_cost = parse_number(raw_row.get("unit_cost_usd", ""))
        except ValueError as exc:
            raise ValueError(f"Invalid number at CSV line {idx}: {exc}") from exc

        parsed.append(
            BomRow(
                category=(raw_row.get("category", "") or "").strip(),
                item=(raw_row.get("item", "") or "").strip(),
                required=required,
                selected=selected,
                qty=qty,
                unit_cost=unit_cost,
                buy_link=(raw_row.get("buy_link", "") or "").strip(),
                notes=(raw_row.get("notes", "") or "").strip(),
            )
        )
    return parsed


def read_rows_from_local_csv(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return normalize_rows(rows)


def read_rows_from_url(csv_url: str) -> list[dict[str, str]]:
    with urlopen(csv_url) as response:  # nosec B310 - explicit user-provided CSV URL.
        text = response.read().decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(text)))
    return normalize_rows(rows)


def fmt_qty(value: float | None) -> str:
    if value is None:
        return "TBD"
    if value.is_integer():
        return str(int(value))
    return f"{value:g}"


def fmt_money(value: float | None) -> str:
    if value is None:
        return "TBD"
    return f"{value:.2f}"


def fmt_link(value: str) -> str:
    raw = value.strip()
    if not raw or raw.upper() == "TBD":
        return "TBD"
    if raw.startswith("http://") or raw.startswith("https://"):
        return f"[Link]({raw})"
    return raw


def md_cell(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ")


def render_markdown(rows: list[BomRow], source_hint: str) -> str:
    lines: list[str] = []
    lines.append("# Bill of Materials")
    lines.append("")
    lines.append(
        "This page currently reflects an initial parts plan and is not yet fully updated to match final purchased parts."
    )
    lines.append("")
    lines.append("## Bill of Materials")
    lines.append("")
    lines.append(
        "| Category | Item | Est Total (SEK) | Link | Notes |"
    )
    lines.append("| --- | --- | --- | --- | --- |")

    for row in rows:
        est_total = row.est_total
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(row.category),
                    md_cell(row.item),
                    fmt_money(est_total),
                    md_cell(fmt_link(row.buy_link)),
                    md_cell(row.notes or "-"),
                ]
            )
            + " |"
        )

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate docs/bom.md from CSV data.")
    parser.add_argument(
        "--csv",
        default="data/bom.csv",
        help="Local CSV source path (default: data/bom.csv).",
    )
    parser.add_argument(
        "--csv-url",
        default="",
        help="Optional published CSV URL (for example a Google Sheet export URL).",
    )
    parser.add_argument(
        "--csv-url-file",
        default="",
        help="Optional file containing a published CSV URL (for example .bom-sheet-url).",
    )
    parser.add_argument(
        "--write-csv",
        default="",
        help="Optional local CSV output path to save normalized source rows.",
    )
    parser.add_argument(
        "--out",
        default="docs/bom.md",
        help="Output Markdown path (default: docs/bom.md).",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    out_path = Path(args.out)
    source_hint = args.csv
    csv_url = args.csv_url.strip()

    if args.csv_url and args.csv_url_file:
        raise ValueError("Use either --csv-url or --csv-url-file, not both.")

    if args.csv_url_file:
        csv_url_path = Path(args.csv_url_file)
        if not csv_url_path.exists():
            raise FileNotFoundError(
                f"CSV URL file not found: {csv_url_path}. Create it with one Google Sheet CSV export URL."
            )
        csv_url = csv_url_path.read_text(encoding="utf-8").strip()
        if not csv_url:
            raise ValueError(f"CSV URL file is empty: {csv_url_path}")

    if csv_url:
        rows = read_rows_from_url(csv_url)
        source_hint = csv_url
        validate_rows(rows, source_hint)
        if args.write_csv:
            write_rows_to_local_csv(rows, Path(args.write_csv))
    else:
        rows = read_rows_from_local_csv(Path(args.csv))
        validate_rows(rows, source_hint)

    parsed_rows = parse_rows(rows)
    markdown = render_markdown(parsed_rows, source_hint)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(2)
