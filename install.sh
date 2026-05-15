#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

mkdir -p data/cases data/screenshots/before data/screenshots/after data/screenshots/scenario_maps templates rules scripts prompts .codex/skills/nq_replay

if [ ! -f data/pattern_index.csv ]; then
  cat > data/pattern_index.csv <<CSV
case_id,date,title,session,main_pattern,result,tags,case_file
CSV
fi

python3 --version >/dev/null 2>&1 || { echo "Python3가 필요합니다. Python3 설치 후 다시 실행하세요."; exit 1; }

echo "설치 완료: $PROJECT_DIR"
echo "검색 테스트: python3 scripts/search_similar_cases.py --query '정규장오픈 하단이탈실패 CVD급반전'"
echo "새 케이스 추가: python3 scripts/add_case.py --title '케이스 제목' --date YYYY-MM-DD --tags '태그1,태그2'"
