# Repair Pack v3

## What changed

- `tools/run_py.ps1` no longer performs broad recursive searches across Codex/OpenAI app folders. That broad search could make PowerShell appear frozen.
- `install.ps1` now calls the Python wrapper with `--version` only during the Python check.
- Script smoke tests run after Python is found.

## Apply

Copy/merge this folder over `C:\nq-scenario-replay-db`, then run:

```powershell
cd C:\nq-scenario-replay-db
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

## If Python is still not found

Install Python 3.10+ from python.org or Microsoft Store and check **Add python.exe to PATH**.

Or set the path manually:

```powershell
$env:CODEX_PYTHON="C:\full\path\to\python.exe"
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Permanent:

```powershell
[Environment]::SetEnvironmentVariable("CODEX_PYTHON", "C:\full\path\to\python.exe", "User")
```
