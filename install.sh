#!/usr/bin/env bash
# install.sh — one-liner installer for nic2markdown
# Usage: curl -fsSL https://raw.githubusercontent.com/frankshi2024/nic2markdown/main/install.sh | bash

set -euo pipefail

REPO="https://github.com/frankshi2024/nic2markdown.git"
SKILL_DIR="${HOME}/.config/agents/skills/nic2markdown"
SKILL_URL="https://raw.githubusercontent.com/frankshi2024/nic2markdown/main/skill/SKILL.md"

echo "====================================="
echo "  nic2markdown installer"
echo "====================================="
echo ""

# Check prerequisites
if ! command -v uv &>/dev/null; then
    echo "[ERROR] uv is required but not installed."
    echo "  Install it: https://docs.astral.sh/uv/#installation"
    exit 1
fi

echo "[1/2] Installing nic2markdown CLI (via uv tool install)..."
uv tool install "git+${REPO}" --force

echo ""
echo "[2/2] Installing agent skill..."
mkdir -p "${SKILL_DIR}"
curl -fsSL "${SKILL_URL}" -o "${SKILL_DIR}/SKILL.md"

echo ""
echo "====================================="
echo "  Installation complete!"
echo "====================================="
echo ""
echo "Try it out:"
echo "  nic2markdown --help"
echo "  nic2markdown https://soc.ustc.edu.cn/COD/lab5/"
