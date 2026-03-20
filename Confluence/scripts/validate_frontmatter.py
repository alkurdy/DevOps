#!/usr/bin/env python3
"""Validate required Confluence frontmatter fields in Markdown files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_KEYS = {
    "source_system",
    "space_key",
    "page_id",
    "title",
    "exported_at",
    "source_repo",
    "canonical_topic_id",
    "content_fingerprint",
    "redundancy_status",
    "lifecycle_state",
    "curation_tags",
    "sensitivity",
}


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}

    result: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base",
        default="Texts/Converted/Confluence/JAVA",
        help="Directory containing converted markdown files.",
    )
    parser.add_argument(
        "--report",
        default="Confluence/pilot_reports/frontmatter_validation_java_2026-03-20.json",
        help="Output JSON report path.",
    )
    args = parser.parse_args()

    base = Path(args.base)
    report_path = Path(args.report)

    files = sorted(base.glob("*.md"))
    issues = []
    valid_count = 0

    for file_path in files:
        text = file_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        file_issues = []

        if not fm:
            file_issues.append("missing-frontmatter")
        else:
            missing = sorted(k for k in REQUIRED_KEYS if k not in fm)
            if missing:
                file_issues.append({"missing_keys": missing})

            empty_required = sorted(k for k in REQUIRED_KEYS if k in fm and not fm[k].strip())
            if empty_required:
                file_issues.append({"empty_required_keys": empty_required})

        if file_issues:
            issues.append({"file": str(file_path), "issues": file_issues})
        else:
            valid_count += 1

    report = {
        "base": str(base),
        "files_scanned": len(files),
        "files_valid": valid_count,
        "files_with_issues": len(issues),
        "required_keys": sorted(REQUIRED_KEYS),
        "issues": issues,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
