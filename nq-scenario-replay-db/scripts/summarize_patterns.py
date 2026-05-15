#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "pattern_index.csv"


def main() -> None:
    if not INDEX.exists():
        print("data/pattern_index.csv 없음")
        return

    tag_counter = Counter()
    result_counter = Counter()
    session_counter = Counter()
    pattern_counter = Counter()
    total = 0

    with INDEX.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            total += 1
            result_counter[row.get("result", "미기록") or "미기록"] += 1
            session_counter[row.get("session", "미기록") or "미기록"] += 1
            pattern_counter[row.get("main_pattern", "미기록") or "미기록"] += 1
            for tag in (row.get("tags", "") or "").split("|"):
                tag = tag.strip()
                if tag:
                    tag_counter[tag] += 1

    print(f"총 케이스: {total}")
    print("\n결과 분포")
    for k, v in result_counter.most_common():
        print(f"- {k}: {v}")

    print("\n세션 분포")
    for k, v in session_counter.most_common():
        print(f"- {k}: {v}")

    print("\n메인 패턴 분포")
    for k, v in pattern_counter.most_common():
        print(f"- {k}: {v}")

    print("\n상위 태그")
    for k, v in tag_counter.most_common(20):
        print(f"- {k}: {v}")


if __name__ == "__main__":
    main()
