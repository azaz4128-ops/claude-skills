#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "data" / "reviews.csv"

FIELDS = [
    "review_id",
    "review_datetime_kst",
    "instrument",
    "timeframe",
    "scenario_time_kst",
    "current_chart_time_kst",
    "scenario_bias",
    "main_plan",
    "actual_flow",
    "entry_confirmation",
    "trade_action",
    "result",
    "targets",
    "key_levels",
    "cvd_read",
    "good_decision",
    "risk_check",
    "next_rule",
    "tags",
    "scenario_image",
    "current_image",
    "review_note",
]


def slugify(text: str) -> str:
    value = re.sub(r"[^0-9A-Za-z가-힣]+", "_", text.strip()).strip("_")
    return value[:80] or "review"


def normalize_tags(value: str) -> str:
    tags: list[str] = []
    seen: set[str] = set()
    for tag in re.split(r"[,|/]+", value or ""):
        clean = tag.strip().replace(" ", "")
        if clean and clean not in seen:
            tags.append(clean)
            seen.add(clean)
    return "|".join(tags)


def read_existing_ids() -> set[str]:
    if not REVIEWS.exists():
        return set()
    with REVIEWS.open("r", encoding="utf-8-sig", newline="") as f:
        return {row.get("review_id", "") for row in csv.DictReader(f)}


def ensure_file() -> None:
    REVIEWS.parent.mkdir(parents=True, exist_ok=True)
    if REVIEWS.exists():
        return
    with REVIEWS.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()


def build_review_id(args: argparse.Namespace) -> str:
    if args.review_id:
        return args.review_id
    dt = args.review_datetime_kst or datetime.now().strftime("%Y-%m-%d %H:%M KST")
    base = f"{dt}_{args.instrument}_{args.timeframe}_{args.trade_action}"
    return slugify(base)


def main() -> None:
    parser = argparse.ArgumentParser(description="reviews.csv에 복기 데이터를 안전하게 추가합니다.")
    parser.add_argument("--review-id", default="")
    parser.add_argument("--review-datetime-kst", required=True)
    parser.add_argument("--instrument", required=True)
    parser.add_argument("--timeframe", required=True)
    parser.add_argument("--scenario-time-kst", default="")
    parser.add_argument("--current-chart-time-kst", default="")
    parser.add_argument("--scenario-bias", default="")
    parser.add_argument("--main-plan", default="")
    parser.add_argument("--actual-flow", default="")
    parser.add_argument("--entry-confirmation", default="")
    parser.add_argument("--trade-action", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--targets", default="")
    parser.add_argument("--key-levels", default="")
    parser.add_argument("--cvd-read", default="")
    parser.add_argument("--good-decision", default="")
    parser.add_argument("--risk-check", default="")
    parser.add_argument("--next-rule", default="")
    parser.add_argument("--tags", default="")
    parser.add_argument("--scenario-image", default="")
    parser.add_argument("--current-image", default="")
    parser.add_argument("--review-note", default="")
    parser.add_argument("--allow-duplicate", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    row = {
        "review_id": build_review_id(args),
        "review_datetime_kst": args.review_datetime_kst,
        "instrument": args.instrument,
        "timeframe": args.timeframe,
        "scenario_time_kst": args.scenario_time_kst,
        "current_chart_time_kst": args.current_chart_time_kst,
        "scenario_bias": args.scenario_bias,
        "main_plan": args.main_plan,
        "actual_flow": args.actual_flow,
        "entry_confirmation": args.entry_confirmation,
        "trade_action": args.trade_action,
        "result": args.result,
        "targets": args.targets,
        "key_levels": args.key_levels,
        "cvd_read": args.cvd_read,
        "good_decision": args.good_decision,
        "risk_check": args.risk_check,
        "next_rule": args.next_rule,
        "tags": normalize_tags(args.tags),
        "scenario_image": args.scenario_image,
        "current_image": args.current_image,
        "review_note": args.review_note,
    }

    if args.dry_run:
        writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerow(row)
        return

    ensure_file()
    existing_ids = read_existing_ids()
    if row["review_id"] in existing_ids and not args.allow_duplicate:
        raise SystemExit(f"이미 존재하는 review_id입니다: {row['review_id']}")

    with REVIEWS.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(row)

    print(row["review_id"])


if __name__ == "__main__":
    main()
