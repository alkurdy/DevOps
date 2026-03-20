#!/usr/bin/env python3
"""Controlled Phase 3 pilot import for Confluence JAVA space.

Behavior:
- Copies source ZIP into private Originals staging
- Extracts a limited number of pages from entities.xml
- Writes normalized markdown pages to Converted
- Writes heading-based chunks to Chunked
- Emits a pilot report JSON for manual gate review

No broad import logic is included.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import xml.etree.ElementTree as ET


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "untitled"


def prop(obj: ET.Element, name: str) -> Optional[ET.Element]:
    return obj.find(f"property[@name='{name}']")


def prop_text(obj: ET.Element, name: str) -> str:
    p = prop(obj, name)
    if p is None:
        return ""
    return (p.text or "").strip()


def prop_body_content(obj: ET.Element) -> str:
    """Return robust body property content, including nested XML when needed."""
    p = prop(obj, "body")
    if p is None:
        return ""

    text_parts: List[str] = []
    if p.text:
        text_parts.append(p.text)

    # Some exports store body payload as nested XML nodes rather than plain text.
    for child in list(p):
        text_parts.append(ET.tostring(child, encoding="unicode", method="xml"))
        if child.tail:
            text_parts.append(child.tail)

    return "".join(text_parts).strip()


def prop_ref_id(obj: ET.Element, name: str) -> str:
    p = prop(obj, name)
    if p is None:
        return ""
    id_el = p.find("id")
    return (id_el.text or "").strip() if id_el is not None else ""


def normalize_for_fingerprint(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def htmlish_to_markdown(value: str) -> str:
    value = html.unescape(value)

    hrefs = re.findall(r'href="([^"]+)"', value, flags=re.IGNORECASE)
    srcs = re.findall(r'src="([^"]+)"', value, flags=re.IGNORECASE)
    attachments = re.findall(r'ri:filename="([^"]+)"', value, flags=re.IGNORECASE)

    # Basic structural conversions to preserve readable chunks.
    value = re.sub(r"<\s*br\s*/?>", "\n", value, flags=re.IGNORECASE)
    for level in range(1, 7):
        value = re.sub(
            rf"<\s*h{level}[^>]*>(.*?)<\s*/\s*h{level}\s*>",
            lambda m: f"\n{'#' * level} {strip_tags(m.group(1)).strip()}\n",
            value,
            flags=re.IGNORECASE | re.DOTALL,
        )

    value = re.sub(r"<\s*li[^>]*>", "\n- ", value, flags=re.IGNORECASE)
    value = re.sub(r"<\s*/\s*li\s*>", "", value, flags=re.IGNORECASE)
    value = re.sub(r"<\s*/\s*p\s*>", "\n\n", value, flags=re.IGNORECASE)

    value = strip_tags(value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    cleaned = value.strip()

    resources: List[str] = []
    for link in hrefs + srcs:
        link = link.strip()
        if link and link not in resources:
            resources.append(link)

    for name in attachments:
        name = name.strip()
        if name and name not in resources:
            resources.append(f"attachment:{name}")

    if resources:
        resource_block = "\n".join(f"- {r}" for r in resources)
        if cleaned:
            cleaned = f"{cleaned}\n\n## Embedded Resources\n{resource_block}"
        else:
            cleaned = f"## Embedded Resources\n{resource_block}"

    return cleaned.strip()


def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def canonical_topic_id(title: str) -> str:
    parts = [p for p in slugify(title).split("-") if p]
    return "topic." + ".".join(parts[:6]) if parts else "topic.untitled"


def parse_entities(entities_xml: str) -> Tuple[Dict[str, dict], Dict[str, str]]:
    root = ET.fromstring(entities_xml)

    pages: Dict[str, dict] = {}
    bodies: Dict[str, str] = {}

    for obj in root.findall("object"):
        cls = obj.get("class", "")

        if cls == "Page":
            page_id_el = obj.find("id[@name='id']")
            if page_id_el is None or not (page_id_el.text or "").strip():
                continue
            page_id = (page_id_el.text or "").strip()
            title = prop_text(obj, "title")
            version = prop_text(obj, "version") or "1"
            creation_date = prop_text(obj, "creationDate")
            modified_date = prop_text(obj, "lastModificationDate")
            status = prop_text(obj, "contentStatus") or "current"
            parent_id = prop_ref_id(obj, "parent")
            space_id = prop_ref_id(obj, "space")

            pages[page_id] = {
                "page_id": page_id,
                "title": title,
                "version": version,
                "creation_date": creation_date,
                "modified_date": modified_date,
                "status": status,
                "parent_page_id": parent_id,
                "space_id": space_id,
            }

        elif cls == "BodyContent":
            page_id = prop_ref_id(obj, "content")
            body = prop_body_content(obj)
            if not page_id or not body:
                continue

            # Keep the richest body if duplicates exist.
            existing = bodies.get(page_id, "")
            if len(body) > len(existing):
                bodies[page_id] = body

    return pages, bodies


def sort_key(page: dict) -> Tuple[int, str]:
    # Prefer recently modified pages first for pilot relevance.
    stamp = page.get("modified_date") or page.get("creation_date") or ""
    try:
        d = dt.datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S.%f")
        return (int(d.timestamp()), page.get("page_id", "0"))
    except ValueError:
        return (0, page.get("page_id", "0"))


def write_chunks(md_text: str, out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)

    lines = md_text.splitlines()
    boundaries = [i for i, line in enumerate(lines) if re.match(r"^#{1,3}\s", line)]

    chunks: List[Tuple[str, List[str]]] = []
    if not boundaries:
        chunks.append(("full-content", lines))
    else:
        for idx, start in enumerate(boundaries):
            end = boundaries[idx + 1] if idx + 1 < len(boundaries) else len(lines)
            title = lines[start].lstrip("#").strip().lower()
            title = slugify(title) or "section"
            section = lines[start:end]
            if section:
                chunks.append((title, section))

    for i, (name, chunk_lines) in enumerate(chunks):
        out_file = out_dir / f"{i:03d}_{name}.md"
        out_file.write_text("\n".join(chunk_lines).strip() + "\n", encoding="utf-8")

    return len(chunks)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-zip", required=True)
    parser.add_argument("--space-key", default="JAVA")
    parser.add_argument("--space-name", default="JAVA")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--export-date", default=dt.date.today().isoformat())
    parser.add_argument(
        "--page-ids",
        default="",
        help="Optional comma-separated page IDs for targeted rerun.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]

    originals_dir = repo_root / "Texts" / "Originals" / "Confluence" / args.space_key / args.export_date
    converted_dir = repo_root / "Texts" / "Converted" / "Confluence" / args.space_key
    chunked_base = repo_root / "Texts" / "Chunked" / "Confluence" / args.space_key
    report_dir = repo_root / "Confluence" / "pilot_reports"

    originals_dir.mkdir(parents=True, exist_ok=True)
    converted_dir.mkdir(parents=True, exist_ok=True)
    chunked_base.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    src_zip = Path(args.source_zip)
    staged_zip = originals_dir / src_zip.name
    shutil.copy2(src_zip, staged_zip)

    with zipfile.ZipFile(src_zip, "r") as zf:
        entities_xml = zf.read("entities.xml").decode("utf-8", errors="replace")

    pages, bodies = parse_entities(entities_xml)

    eligible = []
    for page_id, page in pages.items():
        if page.get("status", "current") != "current":
            continue
        body = bodies.get(page_id, "")
        if not body.strip():
            continue
        if not page.get("title", "").strip():
            continue
        eligible.append((page_id, page, body))

    eligible.sort(key=lambda row: sort_key(row[1]), reverse=True)

    selected = eligible[: args.limit]
    target_ids = {x.strip() for x in args.page_ids.split(",") if x.strip()}
    if target_ids:
        selected = [row for row in eligible if row[0] in target_ids]

    processed = 0
    total_chunks = 0
    failures = []

    for page_id, page, body_html in selected:
        try:
            title = page["title"].strip()
            slug = slugify(title)
            page_slug = f"{slug}-{page_id}"

            body_md = htmlish_to_markdown(body_html)
            body_norm = normalize_for_fingerprint(body_md)
            fp = hashlib.sha256(body_norm.encode("utf-8")).hexdigest()

            md = (
                "---\n"
                "source_system: confluence\n"
                "source_format: xml\n"
                f"space_key: {args.space_key}\n"
                f"space_name: \"{args.space_name}\"\n"
                f"page_id: \"{page_id}\"\n"
                f"parent_page_id: \"{page.get('parent_page_id', '')}\"\n"
                f"title: \"{title.replace('\\\"', '\"')}\"\n"
                "labels: []\n"
                f"version: {page.get('version', '1')}\n"
                f"exported_at: \"{args.export_date}\"\n"
                "source_repo: DevOps\n"
                f"source_path: Texts/Originals/Confluence/{args.space_key}/{args.export_date}/\n"
                "systems_domains: [Software Development, DevOps Automation]\n"
                "systems_concepts: [Feedback Loops, Delays, Resilience]\n"
                "confidence: medium\n"
                f"canonical_topic_id: \"{canonical_topic_id(title)}\"\n"
                f"content_fingerprint: \"{fp}\"\n"
                "redundancy_status: unique\n"
                "signal_strength: medium\n"
                "lifecycle_state: active\n"
                "curation_tags: [domain:software, domain:devops, artifact:standard, lifecycle:active, confidence:medium, sensitivity:internal]\n"
                "sensitivity: internal\n"
                "---\n\n"
                f"# {title}\n\n"
                "## Source Metadata\n"
                f"- page_id: {page_id}\n"
                f"- parent_page_id: {page.get('parent_page_id', '')}\n"
                f"- created: {page.get('creation_date', '')}\n"
                f"- modified: {page.get('modified_date', '')}\n\n"
                "## Content\n\n"
                f"{body_md}\n"
            )

            out_md = converted_dir / f"{page_slug}.md"
            out_md.write_text(md, encoding="utf-8")

            chunk_count = write_chunks(md, chunked_base / page_slug)
            total_chunks += chunk_count
            processed += 1

        except Exception as exc:  # noqa: BLE001
            failures.append({"page_id": page_id, "title": page.get("title", ""), "error": str(exc)})

    report = {
        "run_at": dt.datetime.now().isoformat(timespec="seconds"),
        "phase": "phase3-controlled-pilot",
        "space_key": args.space_key,
        "limit_requested": args.limit,
        "pages_eligible": len(eligible),
        "pages_processed": processed,
        "chunks_created": total_chunks,
        "failures": failures,
        "staged_zip": str(staged_zip),
        "converted_dir": str(converted_dir),
        "chunked_dir": str(chunked_base),
        "manual_gate_required": True,
    }

    report_file = report_dir / f"pilot_{args.space_key.lower()}_{args.export_date}.json"
    report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
