# install-gitee.ps1 — Windows PowerShell installer for nic2markdown (via Gitee mirror)
# Usage: iwr -useb https://gitee.com/frankshi2024/nic2markdown/raw/main/install-gitee.ps1 | iex

$ErrorActionPreference = "Stop"

$Repo = "https://gitee.com/frankshi2024/nic2markdown.git"
$SkillDir = "$env:USERPROFILE\.config\agents\skills\nic2markdown"
$SkillUrl = "https://gitee.com/frankshi2024/nic2markdown/raw/main/skill/SKILL.md"

Write-Host "====================================="
Write-Host "  nic2markdown installer (Windows)"
Write-Host "====================================="
Write-Host ""

# Check prerequisites
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] uv is required but not installed."
    Write-Host "  Install it: https://docs.astral.sh/uv/#installation"
    exit 1
}

Write-Host "[1/2] Installing nic2markdown CLI (via uv tool install)..."
uv tool install "git+$Repo" --force

Write-Host ""
Write-Host "[2/2] Installing agent skill..."
New-Item -ItemType Directory -Force -Path $SkillDir | Out-Null
Invoke-WebRequest -Uri $SkillUrl -OutFile "$SkillDir\SKILL.md"

Write-Host ""
Write-Host "====================================="
Write-Host "  Installation complete!"
Write-Host "====================================="
Write-Host ""
Write-Host "Try it out:"
Write-Host "  nic2markdown --help"
Write-Host "  nic2markdown https://soc.ustc.edu.cn/COD/lab5/"
