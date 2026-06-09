param(
    [string]$Python = "py -3.12",
    [string]$VenvName = ".venv-crewai"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Venv = Join-Path $Root $VenvName
$PythonExe = Join-Path $Venv "Scripts\python.exe"

if (!(Test-Path $Venv)) {
    $parts = $Python.Split(" ", [System.StringSplitOptions]::RemoveEmptyEntries)
    $exe = $parts[0]
    $args = @()
    if ($parts.Count -gt 1) {
        $args = $parts[1..($parts.Count - 1)]
    }
    & $exe @args -m venv $Venv
}

& $PythonExe -m pip install --upgrade pip
& $PythonExe -m pip install -r (Join-Path $Root "requirements.txt")

Write-Host ""
Write-Host "CrewAI environment ready."
Write-Host "Activate with:"
Write-Host "  .\.venv-crewai\Scripts\Activate.ps1"
Write-Host ""
Write-Host "Next:"
Write-Host "  Copy .env.example to .env and set GEMINI_API_KEY or OPENAI_API_KEY."
Write-Host "  python scripts/generate_online.py"
