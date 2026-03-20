#!/usr/bin/env python3
"""Detect duplicate and near-duplicate Confluence pages in converted markdown."""

from __future__ import annotations

import argparse
import difflib
import itertools
import json
import re
from collections import defaultdict
from pathlib import Path


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
        result[key.strip()] = value.strip().strip('"')
    return result


def extract_content(text: str) -> str:
    marker = "\n## Content\n"
    idx = text.find(marker)
    if idx == -1:
        return text
    return text[idx + len(marker) :]


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base",
        default="Texts/Converted/Confluence/JAVA",
        help="Directory containing converted markdown files.",
    )
    parser.add_argument(
        "--report",
        default="Confluence/pilot_reports/duplicate_detection_java_2026-03-20.json",
        help="Output JSON report path.",
    )
    parser.add_argument(
        "--near-threshold",
        type=float,
        default=0.90,
        help="Similarity threshold for near-duplicates when fingerprints differ.",
    )
    args = parser.parse_args()

    base = Path(args.base)
    report_path = Path(args.report)

    rows = []
    for file_path in sorted(base.glob("*.md")):
        text = file_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if not fm:
            continue
        rows.append(
            {
                "file": str(file_path),
                "title": fm.get("title", ""),
                "page_id": fm.get("page_id", ""),
                "canonical_topic_id": fm.get("canonical_topic_id", ""),
                "content_fingerprint": fm.get("content_fingerprint", ""),
                "normalized_content": normalize(extract_content(text)),
            }
        )

    by_topic: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_topic[row["canonical_topic_id"]].append(row)

    exact_duplicates = []
    near_duplicates = []

    for topic, members in by_topic.items():
        if len(members) < 2:
            continue

        by_fp: dict[str, list[dict]] = defaultdict(list)
        for m in members:
            by_fp[m["content_fingerprint"]].append(m)

        for fp, fp_members in by_fp.items():
            if fp and len(fp_members) > 1:
                exact_duplicates.append(
                    {
                        "canonical_topic_id": topic,
                        "content_fingerprint": fp,
                        "members": [
                            {"file": m["file"], "page_id": m["page_id"], "title": m["title"]}
                            for m in fp_members
                        ],
                    }
                )

        for a, b in itertools.combinations(members, 2):
            if a["content_fingerprint"] and a["content_fingerprint"] == b["content_fingerprint"]:
                continue
            ratio = difflib.SequenceMatcher(None, a["normalized_content"], b["normalized_content"]).ratio()
            if ratio >= args.near_threshold:
                near_duplicates.append(
                    {
                        "canonical_topic_id": topic,
                        "similarity": round(ratio, 4),
                        "a": {"file": a["file"], "page_id": a["page_id"], "title": a["title"]},
                        "b": {"file": b["file"], "page_id": b["page_id"], "title": b["title"]},
                    }
                )

    report = {
        "base": str(base),
        "files_scanned": len(rows),
        "topics_with_multiple_pages": sum(1 for v in by_topic.values() if len(v) > 1),
        "exact_duplicate_groups": exact_duplicates,
        "near_duplicates": near_duplicates,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
