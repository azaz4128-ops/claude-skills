#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "data" / "cases"
INDEX = ROOT / "data" / "pattern_index.csv"
TEMPLATE = ROOT / "templates" / "case_template.md"
INDEX_FIELDS = ["case_id", "date", "title", "session", "main_pattern", "result", "tags", "case_file"]


def slugify(text: str) -> str:
    text = re.sub(r"[^0-9A-Za-z가-힣]+", "_", text.strip()).strip("_")
    return text[:60] or "case"


def parse_tags(text: str) -> list[str]:
    tags = []
    seen = set()
    for tag in re.split(r"[,，|/]+", text):
        tag = tag.strip()
        if tag and tag not in seen:
            tags.append(tag)
            seen.add(tag)
    return tags


def ensure_index() -> None:
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    if not INDEX.exists():
        INDEX.write_text("case_id,date,title,session,main_pattern,result,tags,case_file\n", encoding="utf-8-sig")


def case_exists(case_id: str) -> bool:
    if not INDEX.exists():
        return False
    with INDEX.open("r", encoding="utf-8-sig", newline="") as f:
        return any(row.get("case_id") == case_id for row in csv.DictReader(f))


def append_index(row: dict[str, str]) -> None:
    ensure_index()
    with INDEX.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=INDEX_FIELDS)
        writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="복기 케이스 md 파일과 pattern_index.csv를 생성합니다.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--session", default="")
    parser.add_argument("--main-pattern", default="")
    parser.add_argument("--result", default="")
    parser.add_argument("--tags", default="")
    parser.add_argument("--no-open", action="store_true", help="호환용 옵션입니다. 현재는 항상 생성 경로만 출력합니다.")
    args = parser.parse_args()

    CASES.mkdir(parents=True, exist_ok=True)
    case_id = f"{args.date}_{slugify(args.title)}"
    file_path = CASES / f"{case_id}.md"

    tags = parse_tags(args.tags)
    tags_list = "\n".join(f"- {tag}" for tag in tags) or "-"

    if not file_path.exists():
        template = TEMPLATE.read_text(encoding="utf-8")
        content = (
            template.replace("{{title}}", args.title)
            .replace("{{case_id}}", case_id)
            .replace("{{date}}", args.date)
            .replace("{{session}}", args.session)
            .replace("{{main_pattern}}", args.main_pattern)
            .replace("{{result}}", args.result)
            .replace("{{tags_list}}", tags_list)
        )
        file_path.write_text(content, encoding="utf-8-sig")

    ensure_index()
    if not case_exists(case_id):
        append_index({
            "case_id": case_id,
            "date": args.date,
            "title": args.title,
            "session": args.session,
            "main_pattern": args.main_pattern,
            "result": args.result,
            "tags": "|".join(tags),
            "case_file": str(file_path.relative_to(ROOT)),
        })

    print(file_path)


if __name__ == "__main__":
    main()
