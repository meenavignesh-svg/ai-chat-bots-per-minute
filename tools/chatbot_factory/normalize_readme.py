#!/usr/bin/env python3
"""Keep the root catalog stable after generation."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
HEADER = "| S.No | Product | Made On (UTC) | Category | Folder | Value | Demo |"
SEPARATOR = "| ---: | --- | --- | --- | --- | --- | --- |"


def is_catalog_row(line: str) -> bool:
    return bool(re.match(r"^\|\s*\d+\s*\|.*`ai-chatbots/", line))


def renumber(rows: list[str]) -> list[str]:
    output = []
    for index, row in enumerate(rows, 1):
        output.append(re.sub(r"^\|\s*\d+\s*\|", f"| {index} |", row))
    return output


def main() -> None:
    if not README.exists():
        return
    lines = README.read_text(encoding="utf-8").splitlines()
    rows = renumber([line for line in lines if is_catalog_row(line)])
    cleaned = [line for line in lines if not is_catalog_row(line)]

    try:
        header_index = cleaned.index(HEADER)
    except ValueError:
        README.write_text("\n".join(cleaned).rstrip() + "\n", encoding="utf-8")
        return

    insert_at = header_index + 1
    if insert_at < len(cleaned) and cleaned[insert_at] == SEPARATOR:
        insert_at += 1
    cleaned[insert_at:insert_at] = rows
    README.write_text("\n".join(cleaned).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
