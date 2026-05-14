$ErrorActionPreference = "Stop"

function Fail($msg) {
    Write-Host "ERROR: $msg" -ForegroundColor Red
    exit 1
}

Write-Host "[1/4] Checking project folders..."
$folders = @("data", "data/cases", "templates", "rules", "scripts", "tools", "prompts")
foreach ($f in $folders) {
    if (!(Test-Path $f)) { Fail "Missing folder: $f" }
}

Write-Host "[2/4] Checking required files..."
$files = @(
    "rules/trading_manual_v4.md",
    "rules/trading_skill_double_bollinger_1h_v1.md",
    "rules/trading_skill_pattern_filter_mtf_v1.md",
    "rules/trading_skill_volume_filter_nq_v1.md",
    "rules/line_chart_scenario_output_guide.md",
    "data/cases/2026-05-14_open_sweep_reversal_long.md",
    "data/pattern_index.csv",
    "scripts/search_similar_cases.py",
    "scripts/summarize_patterns.py",
    "scripts/add_case.py",
    "tools/run_py.ps1"
)
foreach ($file in $files) {
    if (!(Test-Path $file)) { Fail "Missing file: $file" }
    Write-Host "  OK: $file"
}

Write-Host "[3/4] Checking Python through tools/run_py.ps1..."
& powershell -NoProfile -ExecutionPolicy Bypass -File ".\tools\run_py.ps1" "--version"
if ($LASTEXITCODE -ne 0) {
    Fail "Python check failed. Install Python 3.10+ or set CODEX_PYTHON. See README/repair notes."
}

Write-Host "[4/4] Running script smoke tests..."
& powershell -NoProfile -ExecutionPolicy Bypass -File ".\tools\run_py.ps1" "scripts\summarize_patterns.py"
if ($LASTEXITCODE -ne 0) { Fail "summarize_patterns.py failed" }

& powershell -NoProfile -ExecutionPolicy Bypass -File ".\tools\run_py.ps1" "scripts\search_similar_cases.py" "--query" "정규장오픈 하단이탈실패 CVD급반전"
if ($LASTEXITCODE -ne 0) { Fail "search_similar_cases.py failed" }

Write-Host ""
Write-Host "Install/check completed successfully." -ForegroundColor Green
Write-Host "Try:"
Write-Host 'powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 scripts\search_similar_cases.py --query "정규장오픈 하단이탈실패 CVD급반전"'
