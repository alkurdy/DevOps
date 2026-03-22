#!/usr/bin/env python3
"""Convert and chunk books from a books index into AI-readable markdown/chunks.

Default flow:
- read books_index.json
- convert pending sources to markdown in ConvertedAI
- chunk markdown into ChunkedAI
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from markitdown import MarkItDown

SUPPORTED_EXTS = {".pdf", ".epub", ".mobi", ".docx", ".html", ".htm", ".txt", ".pptx", ".xlsx", ".md"}


EUC_EXTRACTOR = Path(r"C:\Users\alkur\OneDrive\Documents\EUC\PDF\tools\extract_text.py")
CALIBRE_CANDIDATES = [
    r"C:\Program Files\Calibre2\ebook-convert.exe",
    r"C:\Program Files (x86)\Calibre2\ebook-convert.exe",
]


def find_ebook_convert() -> str | None:
    """Locate Calibre ebook-convert executable if available."""
    exe = shutil.which("ebook-convert.exe") or shutil.which("ebook-convert")
    if exe:
        return exe
    for p in CALIBRE_CANDIDATES:
        if Path(p).exists():
            return p
    return None


def safe_name(s: str) -> str:
    s = re.sub(r'[\\/*?:"<>|]', "", s)
    s = re.sub(r"\s+", "_", s.strip())
    return s[:60] or "section"


def chunk_markdown(src_md: Path, chunk_dir: Path, min_lines: int) -> int:
    chunk_dir.mkdir(parents=True, exist_ok=True)
    lines = src_md.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)

    chunks: list[tuple[str, list[str]]] = []
    buf: list[str] = []
    title = "FrontMatter"

    for line in lines:
        heading = re.match(r"^#{1,3} ", line)
        if heading and len(buf) >= min_lines:
            chunks.append((title, buf))
            buf = []
            title = safe_name(re.sub(r"^#+\s*", "", line))
        buf.append(line)

    if buf:
        chunks.append((title, buf))

    for idx, (name, content) in enumerate(chunks):
        out = chunk_dir / f"{idx:03d}_{name}.md"
        out.write_text("".join(content), encoding="utf-8")

    return len(chunks)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default=str(Path(__file__).resolve().parent / "books_index.json"))
    parser.add_argument("--books-root", default=r"D:\\Books")
    parser.add_argument("--converted-root", default=r"D:\\Books\\ConvertedAI")
    parser.add_argument("--chunked-root", default=r"D:\\Books\\ChunkedAI")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--min-chunk-lines", type=int, default=50)
    parser.add_argument("--status", choices=["pending", "converted", "all"], default="pending")
    parser.add_argument("--contains", default="")
    args = parser.parse_args()

    idx_path = Path(args.index)
    data = json.loads(idx_path.read_text(encoding="utf-8"))
    entries = data.get("entries", [])

    books_root = Path(args.books_root)
    converted_root = Path(args.converted_root)
    chunked_root = Path(args.chunked_root)
    converted_root.mkdir(parents=True, exist_ok=True)
    chunked_root.mkdir(parents=True, exist_ok=True)

    md = MarkItDown()

    selected = []
    for e in entries:
        if args.status != "all" and e.get("status") != args.status:
            continue
        rel = e.get("relative_path", "")
        if args.contains and args.contains.lower() not in rel.lower():
            continue
        selected.append(e)
        if len(selected) >= args.limit:
            break

    converted_ok = 0
    chunked_ok = 0
    failed = 0

    for e in selected:
        rel = Path(e["relative_path"])
        src = books_root / rel
        ext = src.suffix.lower()
        if ext not in SUPPORTED_EXTS:
            continue

        out_md = (converted_root / rel).with_suffix(".md")
        out_md.parent.mkdir(parents=True, exist_ok=True)

        try:
            if ext in {".md", ".txt"}:
                out_md.write_text(src.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
            else:
                try:
                    result = md.convert(str(src))
                    out_md.write_text(result.text_content, encoding="utf-8")
                except Exception as ex:
                    if ext == ".pdf" and EUC_EXTRACTOR.exists():
                        r = subprocess.run(
                            [sys.executable, str(EUC_EXTRACTOR), "--input", str(src), "--output", str(out_md)],
                            check=False,
                            capture_output=True,
                            text=True,
                        )
                        if r.returncode != 0:
                            raise RuntimeError(r.stderr.strip() or str(ex))
                    elif ext == ".mobi":
                        ebook_convert = find_ebook_convert()
                        if not ebook_convert:
                            raise RuntimeError(
                                "MOBI conversion requires Calibre 'ebook-convert'. Install Calibre or add ebook-convert.exe to PATH."
                            )

                        temp_epub = out_md.with_suffix(".tmp.epub")
                        r = subprocess.run(
                            [ebook_convert, str(src), str(temp_epub)],
                            check=False,
                            capture_output=True,
                            text=True,
                        )
                        if r.returncode != 0 or not temp_epub.exists():
                            raise RuntimeError(r.stderr.strip() or r.stdout.strip() or str(ex))

                        try:
                            result = md.convert(str(temp_epub))
                            out_md.write_text(result.text_content, encoding="utf-8")
                        finally:
                            if temp_epub.exists():
                                temp_epub.unlink()
                    else:
                        raise

            converted_ok += 1

            chunk_dir = chunked_root / rel.with_suffix("")
            count = chunk_markdown(out_md, chunk_dir, args.min_chunk_lines)
            if count > 0:
                chunked_ok += 1

        except Exception:
            failed += 1

    print(json.dumps({
        "selected": len(selected),
        "converted_ok": converted_ok,
        "chunked_ok": chunked_ok,
        "failed": failed,
        "converted_root": str(converted_root),
        "chunked_root": str(chunked_root),
    }, indent=2))


if __name__ == "__main__":
    main()
