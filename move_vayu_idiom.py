#!/usr/bin/env python3
"""Move records mentioning "成语" in desc out of vayu_desc.csv."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


MATCH_TEXT = "成语"


def move_idiom_rows(source: Path, destination: Path) -> tuple[int, int]:
    """Move matching rows to destination and return (moved, remaining)."""

    with source.open("r", newline="", encoding="utf-8-sig") as source_file:
        reader = csv.DictReader(source_file)
        if reader.fieldnames is None or "desc" not in reader.fieldnames:
            raise ValueError("输入 CSV 必须包含 desc 字段")
        fieldnames = reader.fieldnames
        rows = list(reader)

    moved = [row for row in rows if MATCH_TEXT in row.get("desc", "")]
    remaining = [row for row in rows if MATCH_TEXT not in row.get("desc", "")]

    with destination.open("w", newline="", encoding="utf-8-sig") as destination_file:
        writer = csv.DictWriter(destination_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(moved)

    # Rewrite the source with only the remaining rows: matched rows are moved,
    # not duplicated in both files.
    with source.open("w", newline="", encoding="utf-8-sig") as source_file:
        writer = csv.DictWriter(source_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(remaining)

    return len(moved), len(remaining)


def main() -> None:
    parser = argparse.ArgumentParser(description="从 vayu_desc.csv 移出含‘成语’的记录")
    parser.add_argument("source", nargs="?", type=Path, default=Path("vayu_desc.csv"))
    parser.add_argument("--output", type=Path, default=Path("vayu_idiom.csv"))
    args = parser.parse_args()

    moved, remaining = move_idiom_rows(args.source, args.output)
    print(f"已移动到 {args.output}: {moved} 行")
    print(f"{args.source} 剩余: {remaining} 行")


if __name__ == "__main__":
    main()
