param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$ArgsToPass
)

$ErrorActionPreference = "Stop"

[Console]::InputEncoding = [System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$OutputEncoding = [System.Text.UTF8Encoding]::new()

function Test-PythonExe($Path) {
    if ([string]::IsNullOrWhiteSpace($Path)) { return $false }
    try {
        if (-not (Test-Path -LiteralPath $Path)) { return $false }
        & $Path --version *> $null
        return ($LASTEXITCODE -eq 0)
    } catch { return $false }
}

function Invoke-Python($FilePath, $Arguments) {
    # & 연산자로 직접 실행 — PowerShell 유니코드 컨텍스트를 그대로 유지해 한글 인수 보존
    $env:PYTHONIOENCODING = "utf-8"
    if ($Arguments.Count -ge 2 -and $Arguments[0] -eq "-c") {
        # -c "code" 형태 지원: run_py.ps1 -c "print('hello')"
        $code = $Arguments[1]
        $remaining = @()
        if ($Arguments.Count -gt 2) {
            $remaining = $Arguments[2..($Arguments.Count - 1)]
        }
        & $FilePath -c $code @remaining
    } else {
        & $FilePath @Arguments
    }
    exit $LASTEXITCODE
}

$candidates = New-Object System.Collections.Generic.List[string]

if ($env:CODEX_PYTHON) { $candidates.Add($env:CODEX_PYTHON) }

$codexBundledPython = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (Test-Path -LiteralPath $codexBundledPython) { $candidates.Add($codexBundledPython) }

# Fast PATH-based lookup. Avoid recursive disk scans because those can hang on Windows.
foreach ($cmd in @("python.exe", "py.exe", "python3.exe")) {
    try {
        $found = Get-Command $cmd -ErrorAction SilentlyContinue
        if ($found -and $found.Source) { $candidates.Add($found.Source) }
    } catch {}
}

# Common Windows install paths only. No broad recursive search.
$commonRoots = @(
    "$env:LOCALAPPDATA\Programs\Python",
    "$env:ProgramFiles\Python*",
    "${env:ProgramFiles(x86)}\Python*",
    "$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps"
)
foreach ($root in $commonRoots) {
    try {
        Get-ChildItem -Path $root -Filter python.exe -Recurse -ErrorAction SilentlyContinue -Depth 3 | ForEach-Object { $candidates.Add($_.FullName) }
    } catch {}
}

# De-duplicate.
$unique = $candidates | Where-Object { $_ -and $_.Trim() -ne "" } | Select-Object -Unique
foreach ($py in $unique) {
    if (Test-PythonExe $py) {
        Invoke-Python -FilePath $py -Arguments $ArgsToPass
    }
}

Write-Host "ERROR: Python executable was not found." -ForegroundColor Red
Write-Host "Install Python 3.10+ and check 'Add python.exe to PATH', or set CODEX_PYTHON manually:" -ForegroundColor Yellow
Write-Host '$env:CODEX_PYTHON="C:\full\path\to\python.exe"' -ForegroundColor Yellow
Write-Host '[Environment]::SetEnvironmentVariable("CODEX_PYTHON", "C:\full\path\to\python.exe", "User")' -ForegroundColor Yellow
exit 1
