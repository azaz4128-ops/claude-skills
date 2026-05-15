# 실전 워크플로우

모든 명령은 프로젝트 루트 폴더에서 실행합니다.

현재 작업 폴더 예시:

```powershell
cd C:\claude-skills\nq-scenario-replay-db
```

---

## 1단계: 장 전 — 시나리오 작성

`templates/scenario_template.md`를 참고해 시나리오를 작성합니다.

Codex / Claude에서 작성할 때:
1. `prompts/codex_start_prompt.md` 내용을 붙여넣어 컨텍스트 세팅
2. 1시간 방향 → 15분 구조 → 5분 트리거 순서로 시나리오 작성
3. 메인 / 보조 / 실패 후 전환 시나리오 3개 준비

차트 이미지는 `data/screenshots/before/` 에 저장합니다.
파일명 규칙: `YYYY-MM-DD_케이스ID_before.png`

---

## 2단계: 장 후 — 복기 케이스 등록

### 케이스 파일 생성

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 scripts\add_case.py `
  --title "케이스 제목" `
  --date 2026-05-15 `
  --session "RTH Open" `
  --main-pattern "패턴명" `
  --result "전환 성공" `
  --tags "태그1,태그2,태그3"
```

출력된 경로의 md 파일을 열어 아래 섹션을 채웁니다:
- **2. 사전 시나리오** — 장 전 예상 내용
- **3. 실제 진행** — 실제 흐름
- **4. MTF 구조** — 1h / 15min / 5min 각각
- **6. 좋은 진입 포인트** — 공격형 / 중립형 / 보수형
- **7. 손절 / 무효화** — 실패 조건
- **8. 실전 교훈** — 다음에 바로 쓸 수 있는 규칙
- **9. 다음 실전 적용 규칙**

차트 이미지는 `data/screenshots/after/` 에 저장합니다.
선차트 시나리오 이미지는 `data/screenshots/scenario_maps/` 에 저장합니다.

### 태그 작성 원칙
- 공백 없이 붙여서 작성: `하단이탈실패` (O) / `하단 이탈 실패` (X)
- 핵심 가격은 언더스코어로: `29_500회복`
- 검색에 쓸 키워드 위주로 5~10개

---

## 3단계: 다음 장 전 — 유사 케이스 검색

```powershell
# 유사 케이스 검색 (상위 5개)
powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 scripts\search_similar_cases.py --query "검색어"

# 전체 패턴 통계
powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 scripts\summarize_patterns.py
```

검색어는 태그와 같은 형식으로 입력할수록 매칭이 잘 됩니다.
예: `"정규장오픈 하단이탈실패 CVD급반전"`

---

## 환경 점검

프로젝트가 처음이거나 파일 변경 후 이상이 느껴지면 실행합니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

---

## 빠른 참고

| 목적 | 파일 |
|---|---|
| 매매 최우선 기준 | `rules/trading_manual_v4.md` |
| 더블볼린저 지침 | `rules/trading_skill_double_bollinger_1h_v1.md` |
| 패턴 필터 | `rules/trading_skill_pattern_filter_mtf_v1.md` |
| 거래량 필터 | `rules/trading_skill_volume_filter_nq_v1.md` |
| 선차트 출력 지침 | `rules/line_chart_scenario_output_guide.md` |
| 시나리오 템플릿 | `templates/scenario_template.md` |
| 복기 템플릿 | `templates/review_template.md` |
| 케이스 DB | `data/pattern_index.csv` |
