# Repair Pack v2

이 패치팩은 다음 3개 문제를 수정합니다.

1. `install.ps1` 41번째 줄 따옴표 오류 수정
2. `tools/run_py.ps1` Python 탐색 강화
   - `CODEX_PYTHON` 환경변수
   - PATH의 `python`, `py`, `python3`
   - `codex` 실행 파일 주변 경로
   - 일반 Codex/OpenAI 앱 설치 경로
   - 일반 Python 설치 경로
3. `data/pattern_index.csv`의 `case_file`을 실제 파일명인 `data/cases/2026-05-14_open_sweep_reversal_long.md`로 수정

## 적용 방법

기존 프로젝트 폴더에 이 패치팩 내용을 병합/덮어쓰기 하세요.

그 다음 PowerShell에서:

```powershell
cd C:\claude-skills\nq-scenario-replay-db
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

## Python을 그래도 못 찾는 경우

Codex 앱 내부 Python 경로를 알고 있다면:

```powershell
$env:CODEX_PYTHON="C:\full\path\to\python.exe"
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

경로를 영구 저장하려면:

```powershell
[Environment]::SetEnvironmentVariable("CODEX_PYTHON", "C:\full\path\to\python.exe", "User")
```

## 검색 테스트

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 scripts\search_similar_cases.py --query "정규장오픈 하단이탈실패 CVD급반전"
```
