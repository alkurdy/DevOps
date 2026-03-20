#!/usr/bin/env python3
"""Search chunked AI-readable book data by keyword and return best matches."""

from __future__ import annotations

import argparse
from pathlib import Path


def score_text(text: str, terms: list[str]) -> int:
    lower = text.lower()
    return sum(lower.count(t) for t in terms)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Keyword phrase to search")
    parser.add_argument("--chunked-root", default=r"D:\\Books\\ChunkedAI")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--preview-lines", type=int, default=8)
    args = parser.parse_args()

    chunked_root = Path(args.chunked_root)
    if not chunked_root.exists():
        raise FileNotFoundError(f"Chunked root not found: {chunked_root}")

    terms = [t.lower() for t in args.query.split() if t.strip()]
    if not terms:
        print("No query terms provided.")
        return

    hits: list[tuple[int, Path, str]] = []
    for md in chunked_root.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        score = score_text(text, terms)
        if score <= 0:
            continue
        hits.append((score, md, text))

    hits.sort(key=lambda x: x[0], reverse=True)
    top = hits[: args.limit]

    for rank, (score, path, text) in enumerate(top, start=1):
        preview = "\n".join(text.splitlines()[: args.preview_lines])
        print(f"[{rank}] score={score} path={path}")
        print(preview)
        print("-" * 60)

    print(f"Hits returned: {len(top)}")


if __name__ == "__main__":
    main()
