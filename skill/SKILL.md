---
name: nic2markdown
description: |
  Convert MkDocs Material and other documentation pages to GitHub-compatible 
  Markdown. Use this skill whenever the user wants to save, read, or process 
  a course experiment / lab documentation page as clean Markdown — especially 
  in computer science and engineering course experiments where browsing raw 
  HTML pages is token-heavy and error-prone for coding agents.
---

# nic2markdown

Convert documentation pages (MkDocs Material, and more frameworks to come)
into clean GitHub-Flavored Markdown — ideal for human reading and agent consumption.

## Usage

```bash
# Basic conversion — output saved to output/<stem>.<yyyymmddhhmmss>.md
nic2markdown <url>

# Also extract sidebar navigation links
nic2markdown <url> -s

# Custom output directory
nic2markdown <url> -o ./my-notes
```

## What it handles

- **Admonitions** (note, warning, tip, danger, question, ...) → GFM alerts (`> [!NOTE]`)
- **Code blocks** with syntax highlighting info preserved
- **Tables**, task lists, footnotes
- **MathJax** → `$` / `$$` delimiters
- **Relative links** → resolved to absolute URLs
- **Sidebar navigation** (optional, with `-s` flag)

## Health check

```bash
nic2markdown --help
```

## Supported frameworks

| Framework | Status |
|-----------|--------|
| MkDocs Material | ✅ Supported |
| More frameworks | 🚧 Planned (open an issue if your course uses a different one) |

## Installation

```bash
# One-liner (Linux / macOS / Git Bash / WSL)
curl -fsSL https://raw.githubusercontent.com/frankshi2024/nic2markdown/main/install.sh | bash

# Windows PowerShell
iwr -useb https://raw.githubusercontent.com/frankshi2024/nic2markdown/main/install.ps1 | iex
```

Requires **uv** (https://docs.astral.sh/uv/).
