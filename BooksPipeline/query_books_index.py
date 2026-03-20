#!/usr/bin/env python3
"""Query books_index.json for quick lookup of source/converted/chunk targets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Substring to search in relative_path")
    parser.add_argument("--index", default=str(Path(__file__).resolve().parent / "books_index.json"))
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    data = json.loads(Path(args.index).read_text(encoding="utf-8"))
    rows = data.get("entries", [])
    q = args.query.lower()

    hits = [r for r in rows if q in r.get("relative_path", "").lower()]
    hits = hits[: args.limit]

    for h in hits:
        print(f"[{h['id']}] {h['relative_path']} | {h['status']} | {h['size_human']}")

    print(f"\nHits: {len(hits)}")


if __name__ == "__main__":
    main()
