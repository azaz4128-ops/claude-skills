#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "data" / "reviews.csv"


def read_reviews() -> list[dict[str, str]]:
    if not REVIEWS.exists():
        return []

    for encoding in ("utf-8-sig", "utf-8"):
        try:
            with REVIEWS.open("r", encoding=encoding, newline="") as f:
                return list(csv.DictReader(f))
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("utf-8", b"", 0, 1, "Could not decode reviews.csv")


def tokenize(text: str) -> set[str]:
    return {
        token.lower()
        for token in re.split(r"[\s,|/_:\-]+", text)
        if token.strip()
    }


def haystack(row: dict[str, str]) -> str:
    fields = [
        "review_id",
        "instrument",
        "timeframe",
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
        "review_note",
    ]
    return " ".join(row.get(field, "") or "" for field in fields)


def score(query_tokens: set[str], text: str) -> int:
    lowered = text.lower()
    text_tokens = tokenize(text)
    exact = len(query_tokens & text_tokens) * 3
    partial = sum(1 for token in query_tokens - text_tokens if token in lowered)
    return exact + partial


def contains_filter(row: dict[str, str], field: str, value: str | None) -> bool:
    if not value:
        return True
    return value.lower() in (row.get(field, "") or "").lower()


def print_row(row: dict[str, str], rank_score: int | None = None) -> None:
    prefix = f"[{rank_score}] " if rank_score is not None else ""
    print(f"{prefix}{row.get('review_datetime_kst', '')} | {row.get('instrument', '')} {row.get('timeframe', '')} | {row.get('trade_action', '')}")
    print(f"  결과: {row.get('result', '')}")
    print(f"  확인: {row.get('entry_confirmation', '')}")
    print(f"  핵심 레벨: {row.get('key_levels', '')}")
    print(f"  다음 규칙: {row.get('next_rule', '')}")
    print(f"  태그: {row.get('tags', '')}")
    print(f"  ID: {row.get('review_id', '')}")


def main() -> None:
    parser = argparse.ArgumentParser(description="reviews.csv에서 유사 복기 데이터를 검색합니다.")
    parser.add_argument("--query", default="", help="검색어. 예: '돌파실패 되돌림저항 CVD약화'")
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--tag", default="", help="태그 필터")
    parser.add_argument("--result", default="", help="결과 필터")
    parser.add_argument("--action", default="", help="매매 액션 필터. 예: 숏")
    parser.add_argument("--instrument", default="", help="종목 필터. 예: NQ")
    args = parser.parse_args()

    rows = read_reviews()
    if not rows:
        print("data/reviews.csv 없음")
        return

    filtered = [
        row
        for row in rows
        if contains_filter(row, "tags", args.tag)
        and contains_filter(row, "result", args.result)
        and contains_filter(row, "trade_action", args.action)
        and contains_filter(row, "instrument", args.instrument)
    ]

    query_tokens = tokenize(args.query)
    if query_tokens:
        ranked = []
        for row in filtered:
            text = haystack(row)
            row_score = score(query_tokens, text)
            if row_score:
                ranked.append((row_score, row))
        ranked.sort(key=lambda item: item[0], reverse=True)
        results = ranked[: args.top]
        if not results:
            print("검색 결과 없음")
            return
        for row_score, row in results:
            print_row(row, row_score)
        return

    for row in filtered[-args.top :]:
        print_row(row)


if __name__ == "__main__":
    main()
