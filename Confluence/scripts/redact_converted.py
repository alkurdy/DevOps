#!/usr/bin/env python3
"""Apply conservative redaction patterns to converted markdown files.

This script updates files in place and writes a report of replacements.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PATTERNS = [
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "[EMAIL]"),
    (
        "phone",
        re.compile(r"\b(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b"),
        "[PHONE]",
    ),
    ("ssn", re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[SSN]"),
    (
        "aws_access_key",
        re.compile(r"\b(?:AKIA|ASIA|AROA|ANPA)[A-Z0-9]{16}\b"),
        "[AWS_ACCESS_KEY]",
    ),
    (
        "secret_assignment",
        re.compile(r"(?i)(password|passwd|secret|token|api[_\s-]?key)\s*[:=]\s*\S+"),
        "[REDACTED_CREDENTIAL]",
    ),
    (
        "internal_ip",
        re.compile(r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b"),
        "[INTERNAL_IP]",
    ),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base",
        default="Texts/Converted/Confluence/JAVA",
        help="Directory containing converted markdown files.",
    )
    parser.add_argument(
        "--report",
        default="Confluence/pilot_reports/redaction_java_2026-03-20.json",
        help="Output JSON report path.",
    )
    args = parser.parse_args()

    base = Path(args.base)
    report_path = Path(args.report)

    files = sorted(base.glob("*.md"))
    replaced_by_type: dict[str, int] = {name: 0 for name, _, _ in PATTERNS}
    per_file = []

    for file_path in files:
        text = file_path.read_text(encoding="utf-8")
        total = 0
        file_detail = {"file": str(file_path), "replacements": {}}

        for name, pattern, repl in PATTERNS:
            text, count = pattern.subn(repl, text)
            if count:
                total += count
                replaced_by_type[name] += count
                file_detail["replacements"][name] = count

        if total:
            file_path.write_text(text, encoding="utf-8")
            per_file.append(file_detail)

    report = {
        "base": str(base),
        "files_scanned": len(files),
        "files_modified": len(per_file),
        "replacements_total": sum(replaced_by_type.values()),
        "replacements_by_type": replaced_by_type,
        "files": per_file,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
