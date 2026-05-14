# Codex 시작 프롬프트

이 프로젝트는 NQ / NASDAQ 100 차트 복기 DB입니다. 아래 원칙대로 작업하세요.

## 최우선 기준
1. `rules/trading_manual_v4.md`를 최우선 기준으로 사용한다.
2. 보조 지침은 아래 순서로만 사용한다.
   - `rules/trading_skill_double_bollinger_1h_v1.md`
   - `rules/trading_skill_pattern_filter_mtf_v1.md`
   - `rules/trading_skill_volume_filter_nq_v1.md`
3. 선차트 이미지/시나리오 맵 요청은 `rules/line_chart_scenario_output_guide.md` 형식을 따른다.

## 프로젝트 목적
- 실시간 예상 시나리오를 md로 정리한다.
- 장 진행 후 실제 차트와 매칭해서 복기한다.
- 성공/실패/전환 조건을 패턴 DB로 누적한다.
- 다음 실전 시나리오 작성 시 유사 케이스를 검색해 반영한다.

## 작업 규칙
- 새 복기 케이스는 `data/cases/`에 저장한다.
- 케이스 요약은 `data/pattern_index.csv`에도 반영한다.
- 차트 이미지는 `data/screenshots/before`, `data/screenshots/after`, `data/screenshots/scenario_maps`에 구분 저장한다.
- 결과를 과장하지 않는다. 예상이 틀린 부분과 전환이 늦었던 부분도 기록한다.
- 실전 교훈은 다음에 바로 적용 가능한 규칙으로 작성한다.

## 자주 쓰는 명령
```bash
python3 scripts/add_case.py --title "케이스 제목" --date YYYY-MM-DD --session "RTH Open" --tags "태그1,태그2,태그3"
python3 scripts/search_similar_cases.py --query "정규장오픈 하단이탈실패 CVD급반전"
python3 scripts/summarize_patterns.py
```

## 첫 번째 할 일
`data/cases/2026-05-14_open_sweep_reversal_long.md` 케이스를 열어서 내용을 보강하고, 이후 유사 패턴 검색이 잘 되도록 태그와 실전 적용 규칙을 정리한다.
