# Repair Pack 적용 안내

이 패치는 Windows/Codex 앱 환경에서 누락되기 쉬운 항목을 보강합니다.

## 추가/수정 내용

- `tools/run_py.ps1`: Windows에서 `python` 명령이 없어도 Python 실행 파일을 탐색하는 래퍼.
- `install.ps1`: `tools/run_py.ps1` 기반으로 수정.
- `rules/line_chart_scenario_output_guide.md`: 한글 파일명 인식 문제 대비용 영문 파일명 복사본.
- `data/cases/2026-05-14_open_sweep_reversal_long.md`: 한글 파일명 인식 문제 대비용 영문 파일명 샘플 케이스.

## 적용 후 확인 명령

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Python이 PATH에 없으면 다음 둘 중 하나가 필요합니다.

1. Python 3.10+ 설치 후 `Add python.exe to PATH` 체크.
2. 이미 쓸 수 있는 Python 경로를 알고 있으면:

```powershell
$env:CODEX_PYTHON="C:\Path\To\python.exe"
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

## 실행 예시

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 scripts\summarize_patterns.py
powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 scripts\search_similar_cases.py --query "정규장오픈 하단이탈실패 CVD급반전"
```
