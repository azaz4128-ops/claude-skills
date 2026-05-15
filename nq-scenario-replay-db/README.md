# NQ Scenario Replay DB

나스닥 100 / NQ 차트의 **실시간 예상 시나리오 → 장중 변화 → 사후 복기 → 패턴 DB 누적**을 위한 프로젝트입니다.

## 목적

- 1시간 방향 → 15분 구조 → 5분 트리거 기준으로 시나리오 작성
- 실제 진행 후 예상과 결과를 매칭해 복기
- 반복 패턴을 태그로 저장
- 다음 실전 분석 때 유사 케이스를 검색해 시나리오 품질 개선

## 폴더 구조

```text
nq-scenario-replay-db/
├─ data/
│  ├─ cases/                 # 복기 케이스 md 파일
│  ├─ screenshots/            # 차트 이미지 저장
│  │  ├─ before/              # 분석 전 차트
│  │  ├─ after/               # 결과 차트
│  │  └─ scenario_maps/       # 선차트 시나리오 이미지
│  └─ pattern_index.csv       # 케이스 요약 인덱스
├─ templates/                 # 케이스 / 시나리오 / 복기 템플릿
├─ rules/                     # 현재 프로젝트 매매 지침
├─ scripts/                   # 케이스 추가 / 검색 / 요약 스크립트
├─ prompts/                   # Codex에 바로 붙여넣을 프롬프트
└─ .codex/skills/nq_replay/   # Codex Skill 초안
```

## 빠른 시작

### macOS / Linux

```bash
cd nq-scenario-replay-db
bash install.sh
python3 scripts/add_case.py --title "정규장 오픈 하단 이탈 실패 후 숏커버 롱" --date 2026-05-14 --tags "정규장오픈,하단이탈실패,숏커버,CVD급반전,박스복귀"
python3 scripts/search_similar_cases.py --query "정규장오픈 하단이탈실패 CVD급반전"
python3 scripts/summarize_patterns.py
```

### Windows PowerShell

```powershell
cd C:\claude-skills\nq-scenario-replay-db
powershell -ExecutionPolicy Bypass -File .\install.ps1
powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 scripts\add_case.py --title "정규장 오픈 하단 이탈 실패 후 숏커버 롱" --date 2026-05-14 --tags "정규장오픈,하단이탈실패,숏커버,CVD급반전,박스복귀"
powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 scripts\search_similar_cases.py --query "정규장오픈 하단이탈실패 CVD급반전"
powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 scripts\summarize_patterns.py
```

PowerShell에서 `Get-Content`로 한글이 깨져 보이면 파일이 깨진 것이 아니라 콘솔 인코딩 문제일 수 있습니다. 확인은 아래처럼 Python 래퍼의 `-c` 옵션으로 읽으면 안전합니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 -c "from pathlib import Path; print(Path('README.md').read_text(encoding='utf-8'))"
```

## Codex 앱에서 쓰는 방법

1. Codex 앱을 실행합니다.
2. 이 폴더 `nq-scenario-replay-db`를 프로젝트 폴더로 선택합니다.
3. `prompts/codex_start_prompt.md` 내용을 Codex에 붙여넣습니다.
4. 앞으로 복기할 때는 `data/cases/`에 케이스를 추가하고, 차트 이미지는 `data/screenshots/`에 저장합니다.

## 스크린샷 관리

차트 이미지는 `data/screenshots/` 아래 세 폴더로 구분해 저장합니다.

| 폴더 | 저장 시점 | 내용 |
|---|---|---|
| `before/` | 시나리오 작성 시 | 분석 전 차트 |
| `after/` | 복기 시 | 실제 결과 차트 |
| `scenario_maps/` | 시나리오 작성 시 | 선차트 시나리오 이미지 |

파일명 규칙: `YYYY-MM-DD_케이스ID_설명.png`  
예: `2026-05-14_open_sweep_reversal_long_before.png`

## 운영 원칙

- 실시간 분석은 반드시 `rules/trading_manual_v4.md`를 최우선 기준으로 사용합니다.
- 보조 지침은 더블비 → 패턴 필터 → 거래량 필터 순서로만 적용합니다.
- 복기 케이스는 결과를 과장하지 않고, 예상이 틀린 부분도 명확히 기록합니다.
- “진입 성공”보다 “전환 조건을 얼마나 빨리 인식했는가”를 핵심 평가 항목으로 둡니다.
