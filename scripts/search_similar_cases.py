#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "pattern_index.csv"
CASES = ROOT / "data" / "cases"


def tokenize(text: str) -> set[str]:
    return {t.lower() for t in re.split(r"[\s,，|/_\-]+", text) if t.strip()}


def score_match(q_tokens: set[str], haystack_lower: str, h_tokens: set[str]) -> int:
    exact = len(q_tokens & h_tokens)
    # 쿼리 토큰이 haystack 안에 부분 문자열로 포함되면 추가 점수 (예: "이탈실패" → "하단이탈실패" 매칭)
    partial = sum(1 for q in q_tokens - h_tokens if q and q in haystack_lower)
    return exact + partial


def main() -> None:
    parser = argparse.ArgumentParser(description="태그/본문 기반으로 유사 복기 케이스를 검색합니다.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args()

    q_tokens = tokenize(args.query)
    if not q_tokens:
        print("검색어를 입력하세요.")
        return

    results = []

    if not INDEX.exists():
        print("data/pattern_index.csv 없음")
        return

    with INDEX.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            case_file_value = row.get("case_file", "")
            case_file = ROOT / case_file_value if case_file_value else Path()
            body = case_file.read_text(encoding="utf-8-sig", errors="ignore") if case_file.is_file() else ""
            haystack = " ".join([row.get("title", ""), row.get("tags", ""), row.get("main_pattern", ""), body])
            h_tokens = tokenize(haystack)
            score = score_match(q_tokens, haystack.lower(), h_tokens)
            if score:
                results.append((score, row, case_file))

    results.sort(key=lambda x: x[0], reverse=True)

    if not results:
        print("유사 케이스 없음")
        return

    for score, row, case_file in results[: args.top]:
        print(f"[{score}] {row.get('date','')} | {row.get('title','')} | {row.get('tags','')}")
        print(f"    {case_file.relative_to(ROOT) if case_file.exists() else row.get('case_file','')}")


if __name__ == "__main__":
    main()
