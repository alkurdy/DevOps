#!/usr/bin/env python3
"""Apply duplicate disposition updates to converted markdown frontmatter.

Rules:
- For exact duplicate groups, keep one primary (highest page_id).
- Mark remaining members as redundancy_status: duplicate, lifecycle_state: legacy.
- For near-duplicates, mark both as near-duplicate if still unique.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str], list[str]]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}, [], lines

    fm_lines = []
    body_start = 0
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            body_start = i + 1
            break
        fm_lines.append(line)

    fm = {}
    for line in fm_lines:
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()

    return fm, fm_lines, lines[body_start:]


def upsert_fm_line(lines: list[str], key: str, value: str) -> list[str]:
    pattern = re.compile(rf"^{re.escape(key)}\s*:")
    replaced = False
    out = []
    for line in lines:
        if pattern.match(line):
            out.append(f"{key}: {value}")
            replaced = True
        else:
            out.append(line)
    if not replaced:
        out.append(f"{key}: {value}")
    return out


def write_file(path: Path, fm_lines: list[str], body_lines: list[str]) -> None:
    text = "---\n" + "\n".join(fm_lines) + "\n---\n\n" + "\n".join(body_lines).lstrip("\n")
    path.write_text(text, encoding="utf-8")


def page_id_from_file(path_str: str) -> int:
    m = re.search(r"-(\d+)\.md$", path_str)
    return int(m.group(1)) if m else 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--duplicates-report",
        default="Confluence/pilot_reports/duplicate_detection_java_2026-03-20.json",
    )
    parser.add_argument(
        "--out-report",
        default="Confluence/pilot_reports/disposition_java_2026-03-20.json",
    )
    args = parser.parse_args()

    dup = json.loads(Path(args.duplicates_report).read_text(encoding="utf-8"))

    changed = []

    for group in dup.get("exact_duplicate_groups", []):
        members = group.get("members", [])
        if len(members) < 2:
            continue

        # Keep highest page_id as primary.
        sorted_members = sorted(members, key=lambda m: page_id_from_file(m["file"]), reverse=True)
        primary = sorted_members[0]

        # Ensure primary remains unique/active.
        ppath = Path(primary["file"])
        ptxt = ppath.read_text(encoding="utf-8")
        pfm, pfm_lines, pbody = parse_frontmatter(ptxt)
        pfm_lines = upsert_fm_line(pfm_lines, "redundancy_status", "unique")
        pfm_lines = upsert_fm_line(pfm_lines, "lifecycle_state", "active")
        write_file(ppath, pfm_lines, pbody)
        changed.append({"file": str(ppath), "action": "set_primary"})

        for member in sorted_members[1:]:
            path = Path(member["file"])
            text = path.read_text(encoding="utf-8")
            fm, fm_lines, body = parse_frontmatter(text)
            fm_lines = upsert_fm_line(fm_lines, "redundancy_status", "duplicate")
            fm_lines = upsert_fm_line(fm_lines, "lifecycle_state", "legacy")
            write_file(path, fm_lines, body)
            changed.append({"file": str(path), "action": "set_duplicate"})

    for pair in dup.get("near_duplicates", []):
        for side in ("a", "b"):
            path = Path(pair[side]["file"])
            text = path.read_text(encoding="utf-8")
            fm, fm_lines, body = parse_frontmatter(text)
            if fm.get("redundancy_status", "").strip() == "unique":
                fm_lines = upsert_fm_line(fm_lines, "redundancy_status", "near-duplicate")
                write_file(path, fm_lines, body)
                changed.append({"file": str(path), "action": "set_near_duplicate"})

    out = {
        "changed_files": len(changed),
        "changes": changed,
    }
    Path(args.out_report).write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
