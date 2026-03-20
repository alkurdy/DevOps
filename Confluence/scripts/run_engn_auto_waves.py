#!/usr/bin/env python3
"""Run ENGN Confluence waves end-to-end without per-wave manual invocation.

This script automates the operational gate sequence per wave:
1) import
2) redaction
3) frontmatter validation
4) duplicate detection (pre)
5) duplicate disposition
6) duplicate detection (post)
7) markdown wave report

It can run a single wave or multiple waves in sequence.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any


def run_cmd(cmd: list[str], cwd: Path) -> None:
    result = subprocess.run(cmd, cwd=str(cwd), check=False)
    if result.returncode != 0:
        joined = " ".join(cmd)
        raise RuntimeError(f"Command failed ({result.returncode}): {joined}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def count_value(value: Any) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        return len(value)
    return 0


def newest_engn_zip(repo_root: Path) -> Path:
    roots = sorted((repo_root / "Texts" / "Originals" / "Confluence" / "ENGN").glob("*/Confluence-export-space-engn.zip"))
    if not roots:
        raise FileNotFoundError("No ENGN source ZIP found under Texts/Originals/Confluence/ENGN")
    return roots[-1]


def build_wave_report(
    report_path: Path,
    wave: int,
    date_str: str,
    pilot: dict[str, Any],
    redaction: dict[str, Any],
    frontmatter: dict[str, Any],
    pre: dict[str, Any],
    post: dict[str, Any],
) -> None:
    redaction_types = redaction.get("replacements_by_type", {})
    content = f"""# ENGN Controlled Wave {wave} ({date_str})

## Scope
- Space: ENGN
- Mode: cumulative expansion
- Requested limit: {pilot.get('limit_requested', 0)} pages
- Eligible pages: {pilot.get('pages_eligible', 0)}
- Processed pages: {pilot.get('pages_processed', 0)}
- Import failures: {len(pilot.get('failures', []))}
- Chunks created: {pilot.get('chunks_created', 0)}

## Pipeline Results
- Pilot import report: Confluence/pilot_reports/pilot_engn_{date_str}-w{wave}.json
- Redaction report: Confluence/pilot_reports/redaction_engn_wave{wave}_{date_str}.json
- Frontmatter validation report: Confluence/pilot_reports/frontmatter_validation_engn_wave{wave}_{date_str}.json
- Duplicate detection report: Confluence/pilot_reports/duplicate_detection_engn_wave{wave}_{date_str}.json
- Disposition report: Confluence/pilot_reports/disposition_engn_wave{wave}_{date_str}.json
- Post-disposition duplicate report: Confluence/pilot_reports/duplicate_detection_engn_wave{wave}_post_disposition_{date_str}.json

## Quality Checks
- Redaction replacements: {redaction.get('replacements_total', 0)} ({redaction_types.get('email', 0)} email, {redaction_types.get('secret_assignment', 0)} secret_assignment, {redaction_types.get('internal_ip', 0)} internal_ip)
- Frontmatter validity: {frontmatter.get('files_valid', 0)}/{frontmatter.get('files_scanned', 0)} valid
- Actionable exact duplicate groups pre-disposition: {len(pre.get('actionable_exact_duplicate_groups', []))}
- Actionable exact duplicate groups post-disposition: {len(post.get('actionable_exact_duplicate_groups', []))}
- Near-duplicate pairs post-disposition: {count_value(post.get('near_duplicate_pairs', 0))}
- Topics with multiple pages post-disposition: {count_value(post.get('topics_with_multiple_pages', 0))}

## Recommendation
- Go for ENGN wave-{wave} synthesis/audit/promotion checkpoint.
- No-go for ENGN bulk import.
"""
    report_path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--space-key", default="ENGN")
    parser.add_argument("--space-name", default="ENGN")
    parser.add_argument("--start-wave", type=int, required=True)
    parser.add_argument("--start-limit", type=int, required=True)
    parser.add_argument("--end-limit", type=int, required=True)
    parser.add_argument("--step", type=int, default=25)
    parser.add_argument("--source-zip", default="")
    args = parser.parse_args()

    if args.end_limit < args.start_limit:
        raise ValueError("end-limit must be >= start-limit")
    if args.step <= 0:
        raise ValueError("step must be > 0")

    repo_root = Path(__file__).resolve().parents[2]
    py = sys.executable
    scripts_dir = repo_root / "Confluence" / "scripts"
    reports_dir = repo_root / "Confluence" / "pilot_reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    source_zip = Path(args.source_zip) if args.source_zip else newest_engn_zip(repo_root)
    if not source_zip.exists():
        raise FileNotFoundError(f"Source ZIP not found: {source_zip}")

    limits = list(range(args.start_limit, args.end_limit + 1, args.step))
    waves = list(range(args.start_wave, args.start_wave + len(limits)))

    summary: list[dict[str, Any]] = []

    for wave, limit in zip(waves, limits):
        export_tag = f"{args.date}-w{wave}"

        run_cmd(
            [
                py,
                str(scripts_dir / "run_java_pilot_import.py"),
                "--source-zip",
                str(source_zip),
                "--space-key",
                args.space_key,
                "--space-name",
                args.space_name,
                "--limit",
                str(limit),
                "--export-date",
                export_tag,
            ],
            repo_root,
        )

        run_cmd(
            [
                py,
                str(scripts_dir / "redact_converted.py"),
                "--base",
                "Texts/Converted/Confluence/ENGN",
                "--report",
                f"Confluence/pilot_reports/redaction_engn_wave{wave}_{args.date}.json",
            ],
            repo_root,
        )
        run_cmd(
            [
                py,
                str(scripts_dir / "validate_frontmatter.py"),
                "--base",
                "Texts/Converted/Confluence/ENGN",
                "--report",
                f"Confluence/pilot_reports/frontmatter_validation_engn_wave{wave}_{args.date}.json",
            ],
            repo_root,
        )
        run_cmd(
            [
                py,
                str(scripts_dir / "detect_duplicates.py"),
                "--base",
                "Texts/Converted/Confluence/ENGN",
                "--report",
                f"Confluence/pilot_reports/duplicate_detection_engn_wave{wave}_{args.date}.json",
            ],
            repo_root,
        )
        run_cmd(
            [
                py,
                str(scripts_dir / "apply_duplicate_disposition.py"),
                "--duplicates-report",
                f"Confluence/pilot_reports/duplicate_detection_engn_wave{wave}_{args.date}.json",
                "--out-report",
                f"Confluence/pilot_reports/disposition_engn_wave{wave}_{args.date}.json",
            ],
            repo_root,
        )
        run_cmd(
            [
                py,
                str(scripts_dir / "detect_duplicates.py"),
                "--base",
                "Texts/Converted/Confluence/ENGN",
                "--report",
                f"Confluence/pilot_reports/duplicate_detection_engn_wave{wave}_post_disposition_{args.date}.json",
            ],
            repo_root,
        )

        pilot = load_json(reports_dir / f"pilot_engn_{args.date}-w{wave}.json")
        redaction = load_json(reports_dir / f"redaction_engn_wave{wave}_{args.date}.json")
        frontmatter = load_json(reports_dir / f"frontmatter_validation_engn_wave{wave}_{args.date}.json")
        pre = load_json(reports_dir / f"duplicate_detection_engn_wave{wave}_{args.date}.json")
        post = load_json(reports_dir / f"duplicate_detection_engn_wave{wave}_post_disposition_{args.date}.json")

        build_wave_report(
            reports_dir / f"engn_wave{wave}_{args.date}.md",
            wave,
            args.date,
            pilot,
            redaction,
            frontmatter,
            pre,
            post,
        )

        summary.append(
            {
                "wave": wave,
                "limit": limit,
                "pages_eligible": pilot.get("pages_eligible", 0),
                "pages_processed": pilot.get("pages_processed", 0),
                "chunks_created": pilot.get("chunks_created", 0),
                "failures": len(pilot.get("failures", [])),
                "redaction_total": redaction.get("replacements_total", 0),
                "frontmatter_valid": frontmatter.get("files_valid", 0),
                "frontmatter_scanned": frontmatter.get("files_scanned", 0),
                "pre_actionable_exact": len(pre.get("actionable_exact_duplicate_groups", [])),
                "post_actionable_exact": len(post.get("actionable_exact_duplicate_groups", [])),
                "near_duplicates_post": count_value(post.get("near_duplicate_pairs", 0)),
                "topics_with_multiple_pages": count_value(post.get("topics_with_multiple_pages", 0)),
            }
        )

    out = {
        "run_at": dt.datetime.now().isoformat(timespec="seconds"),
        "space": args.space_key,
        "date": args.date,
        "start_wave": args.start_wave,
        "start_limit": args.start_limit,
        "end_limit": args.end_limit,
        "step": args.step,
        "waves_run": len(summary),
        "summary": summary,
    }
    (reports_dir / f"engn_auto_waves_{args.date}_w{args.start_wave}_to_w{waves[-1]}.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
