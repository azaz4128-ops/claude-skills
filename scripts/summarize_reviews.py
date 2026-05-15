#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter
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


def split_tags(value: str) -> list[str]:
    return [tag.strip() for tag in (value or "").split("|") if tag.strip()]


def print_counter(title: str, counter: Counter[str], limit: int = 20) -> None:
    print(f"\n{title}")
    if not counter:
        print("- 없음")
        return
    for key, count in counter.most_common(limit):
        print(f"- {key}: {count}")


def is_win(result: str) -> bool:
    return any(word in result for word in ("수익", "성공", "익절"))


def is_loss(result: str) -> bool:
    if is_win(result):
        return False
    return any(word in result for word in ("손실", "실패", "손절"))


def main() -> None:
    rows = read_reviews()
    if not rows:
        print("data/reviews.csv 없음")
        return

    result_counter = Counter(row.get("result", "미기록") or "미기록" for row in rows)
    action_counter = Counter(row.get("trade_action", "미기록") or "미기록" for row in rows)
    instrument_counter = Counter(row.get("instrument", "미기록") or "미기록" for row in rows)
    timeframe_counter = Counter(row.get("timeframe", "미기록") or "미기록" for row in rows)
    tag_counter: Counter[str] = Counter()
    rule_counter: Counter[str] = Counter()

    for row in rows:
        tag_counter.update(split_tags(row.get("tags", "")))
        rule = (row.get("next_rule", "") or "").strip()
        if rule:
            rule_counter[rule] += 1

    wins = sum(1 for row in rows if is_win(row.get("result", "") or ""))
    losses = sum(1 for row in rows if is_loss(row.get("result", "") or ""))

    print(f"총 복기 수: {len(rows)}")
    print(f"수익/성공 기록: {wins}")
    print(f"손실/실패 기록: {losses}")

    print_counter("종목 분포", instrument_counter)
    print_counter("타임프레임 분포", timeframe_counter)
    print_counter("매매 액션 분포", action_counter)
    print_counter("결과 분포", result_counter)
    print_counter("상위 태그", tag_counter)
    print_counter("반복 학습 규칙", rule_counter, limit=10)

    print("\n최근 복기")
    for row in rows[-5:]:
        print(f"- {row.get('review_datetime_kst', '')} | {row.get('trade_action', '')} | {row.get('result', '')} | {row.get('review_id', '')}")


if __name__ == "__main__":
    main()
