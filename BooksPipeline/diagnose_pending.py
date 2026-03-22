#!/usr/bin/env python3
"""Diagnose pending books by attempting conversion and recording failure reasons."""

from __future__ import annotations

import argparse
import json
import traceback
from pathlib import Path

from markitdown import MarkItDown

SUPPORTED_EXTS = {".pdf", ".epub", ".mobi", ".docx", ".html", ".htm", ".txt", ".pptx", ".xlsx", ".md"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default=str(Path(__file__).resolve().parent / "books_index.json"))
    parser.add_argument("--books-root", default=r"D:\\Books")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--out-json", default=str(Path(__file__).resolve().parent / "pending_diagnostics.json"))
    parser.add_argument("--out-md", default=str(Path(__file__).resolve().parent / "pending_diagnostics.md"))
    args = parser.parse_args()

    index_path = Path(args.index)
    books_root = Path(args.books_root)
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)

    payload = json.loads(index_path.read_text(encoding="utf-8"))
    entries = [e for e in payload.get("entries", []) if e.get("status") == "pending"][: args.limit]

    md = MarkItDown()
    diagnostics: list[dict[str, str]] = []

    for e in entries:
        rel = e.get("relative_path", "")
        src = books_root / Path(rel)
        ext = src.suffix.lower()

        result = {
            "relative_path": rel,
            "extension": ext,
            "exists": str(src.exists()),
            "supported": str(ext in SUPPORTED_EXTS),
            "status": "unknown",
            "reason": "",
        }

        if not src.exists():
            result["status"] = "error"
            result["reason"] = "source_missing"
            diagnostics.append(result)
            continue

        if ext not in SUPPORTED_EXTS:
            result["status"] = "error"
            result["reason"] = "unsupported_extension"
            diagnostics.append(result)
            continue

        try:
            if ext == ".md":
                _ = src.read_text(encoding="utf-8", errors="replace")
            else:
                _ = md.convert(str(src))
            result["status"] = "ok"
            result["reason"] = "convertible"
        except KeyboardInterrupt:
            raise
        except Exception as ex:
            result["status"] = "error"
            reason = str(ex).strip() or ex.__class__.__name__
            short_trace = traceback.format_exc(limit=1).strip().replace("\n", " | ")
            result["reason"] = f"{reason} || {short_trace}"

        diagnostics.append(result)

    out_json.write_text(json.dumps({"count": len(diagnostics), "items": diagnostics}, indent=2), encoding="utf-8")

    md_lines = [
        "# Pending Diagnostics",
        "",
        f"- Total analyzed: {len(diagnostics)}",
        "",
        "| Status | Extension | Relative Path | Reason |",
        "|---|---|---|---|",
    ]

    for d in diagnostics:
        reason = d["reason"].replace("|", "\\|")
        md_lines.append(f"| {d['status']} | {d['extension']} | {d['relative_path']} | {reason} |")

    out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    ok_count = sum(1 for d in diagnostics if d["status"] == "ok")
    err_count = sum(1 for d in diagnostics if d["status"] == "error")

    print(
        json.dumps(
            {
                "analyzed": len(diagnostics),
                "convertible": ok_count,
                "errors": err_count,
                "out_json": str(out_json),
                "out_md": str(out_md),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
