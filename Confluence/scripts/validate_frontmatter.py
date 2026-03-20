#!/usr/bin/env python3
"""Validate required Confluence frontmatter fields in Markdown files.

Phase 2 skeleton only. No import logic included.
"""

from pathlib import Path

REQUIRED_KEYS = {
    "source_system",
    "space_key",
    "page_id",
    "title",
    "exported_at",
    "source_repo",
}


def main() -> None:
    base = Path("Texts/Converted/Confluence")
    print(f"[INFO] Placeholder validator. Target base: {base}")
    print(f"[INFO] Required keys: {sorted(REQUIRED_KEYS)}")
    print("[TODO] Implement YAML frontmatter parse and validation report.")


if __name__ == "__main__":
    main()
