#!/usr/bin/env python3
"""Build a searchable index for D:\\Books content.

Outputs:
- books_index.json
- books_index.csv
- books_index_summary.md

The index is designed to support staged conversion/chunking to AI-readable data.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from collections import Counter
from pathlib import Path
from typing import Any

SUPPORTED_EXTS = {
    ".pdf",
    ".epub",
    ".mobi",
    ".docx",
    ".html",
    ".htm",
    ".txt",
    ".pptx",
    ".xlsx",
    ".md",
}

DEFAULT_EXCLUDES = {"Converted", "ConvertedAI", "Chunked", "ChunkedAI", "Temp", "$RECYCLE.BIN", "System Volume Information"}


def fmt_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)
    for u in units:
        if value < 1024 or u == units[-1]:
            return f"{value:.1f} {u}"
        value /= 1024
    return f"{size} B"


def should_skip(path: Path, root: Path, excludes: set[str]) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return True
    return any(part in excludes for part in rel.parts)


def detect_status(src: Path, root: Path, converted_root: Path, chunked_root: Path) -> tuple[bool, bool]:
    rel = src.relative_to(root)
    converted = (converted_root / rel).with_suffix(".md")
    chunk_dir = chunked_root / rel.with_suffix("")
    converted_exists = converted.exists()
    chunked_exists = chunk_dir.exists() and any(chunk_dir.glob("*.md"))
    return converted_exists, chunked_exists


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--books-root", default=r"D:\\Books")
    parser.add_argument("--converted-root", default=r"D:\\Books\\ConvertedAI")
    parser.add_argument("--chunked-root", default=r"D:\\Books\\ChunkedAI")
    parser.add_argument("--out-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--include-all-extensions", action="store_true")
    args = parser.parse_args()

    books_root = Path(args.books_root)
    converted_root = Path(args.converted_root)
    chunked_root = Path(args.chunked_root)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not books_root.exists():
        raise FileNotFoundError(f"Books root not found: {books_root}")

    excludes = set(DEFAULT_EXCLUDES)

    entries: list[dict[str, Any]] = []
    ext_counter: Counter[str] = Counter()
    category_counter: Counter[str] = Counter()
    size_total = 0

    file_id = 0
    for p in books_root.rglob("*"):
        if not p.is_file():
            continue
        if should_skip(p, books_root, excludes):
            continue
        ext = p.suffix.lower()
        if (not args.include_all_extensions) and ext not in SUPPORTED_EXTS:
            continue

        file_id += 1
        rel = p.relative_to(books_root)
        category = rel.parts[0] if rel.parts else "ROOT"
        size = p.stat().st_size
        converted_exists, chunked_exists = detect_status(p, books_root, converted_root, chunked_root)

        entry = {
            "id": file_id,
            "category": category,
            "relative_path": str(rel).replace("\\", "/"),
            "source_path": str(p),
            "extension": ext,
            "size_bytes": size,
            "size_human": fmt_size(size),
            "converted_exists": converted_exists,
            "chunked_exists": chunked_exists,
            "status": "chunked" if chunked_exists else ("converted" if converted_exists else "pending"),
            "indexed_at": dt.datetime.now().isoformat(timespec="seconds"),
        }
        entries.append(entry)
        ext_counter[ext or "<none>"] += 1
        category_counter[category] += 1
        size_total += size

    entries.sort(key=lambda e: (e["category"], e["relative_path"]))

    out_json = out_dir / "books_index.json"
    out_csv = out_dir / "books_index.csv"
    out_summary = out_dir / "books_index_summary.md"

    payload = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "books_root": str(books_root),
        "converted_root": str(converted_root),
        "chunked_root": str(chunked_root),
        "file_count": len(entries),
        "total_size_bytes": size_total,
        "total_size_human": fmt_size(size_total),
        "by_extension": dict(sorted(ext_counter.items(), key=lambda kv: kv[0])),
        "by_category": dict(sorted(category_counter.items(), key=lambda kv: kv[0])),
        "entries": entries,
    }
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "category",
                "relative_path",
                "source_path",
                "extension",
                "size_bytes",
                "size_human",
                "converted_exists",
                "chunked_exists",
                "status",
                "indexed_at",
            ],
        )
        w.writeheader()
        w.writerows(entries)

    summary_lines = [
        "# Books Index Summary",
        "",
        f"- Generated: {payload['generated_at']}",
        f"- Books root: {books_root}",
        f"- Converted root: {converted_root}",
        f"- Chunked root: {chunked_root}",
        f"- Indexed files: {len(entries)}",
        f"- Total size: {fmt_size(size_total)}",
        "",
        "## By Category",
    ]
    for k, v in sorted(category_counter.items()):
        summary_lines.append(f"- {k}: {v}")

    summary_lines.append("")
    summary_lines.append("## By Extension")
    for k, v in sorted(ext_counter.items()):
        summary_lines.append(f"- {k}: {v}")

    pending = sum(1 for e in entries if e["status"] == "pending")
    converted = sum(1 for e in entries if e["status"] == "converted")
    chunked = sum(1 for e in entries if e["status"] == "chunked")
    summary_lines.extend(
        [
            "",
            "## Processing Status",
            f"- pending: {pending}",
            f"- converted: {converted}",
            f"- chunked: {chunked}",
            "",
            "## Outputs",
            "- books_index.json",
            "- books_index.csv",
            "- books_index_summary.md",
        ]
    )

    out_summary.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "file_count": len(entries),
        "total_size": fmt_size(size_total),
        "out_json": str(out_json),
        "out_csv": str(out_csv),
        "out_summary": str(out_summary),
    }, indent=2))


if __name__ == "__main__":
    main()
