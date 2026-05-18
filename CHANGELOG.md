# Changelog

## [0.2.0] — 2026-05-18

### Added
- **Sidebar navigation link extraction** (`-s` / `--sidebar` flag)
  - Parses `<nav class="md-nav--primary">` for MkDocs Material
  - Preserves hierarchy via `data-md-level` attribute
  - Outputs as nested Markdown list under `## Sidebar Links`
- **Framework-based architecture** with gateway routing
  - `gateway.py`: framework detection → dispatch to appropriate converter
  - `frameworks/base.py`: `BaseConverter` abstract interface (`detect`, `extract_article`, `convert`, `extract_sidebar_links`)
  - `frameworks/mkdocs_material/`: all MkDocs Material logic isolated in one package
  - Extensible registry: add new frameworks by implementing `BaseConverter`
- New test suites: `test_gateway.py` (6 tests), `test_sidebar.py` (6 tests)

### Changed
- **Default output directory** changed from `.` to `output/`
- CLI rewritten to use gateway-based dispatch
- `__init__.py` updated to re-export gateway and `MkdocsMaterialConverter`
- Old top-level `validator.py` removed (migrated to `frameworks/mkdocs_material/validator.py`)
- Old top-level `extractor.py` removed (migrated to `frameworks/mkdocs_material/extractor.py`)
- Old top-level `converter.py` removed (migrated to `frameworks/mkdocs_material/converter.py`)
- `MkdocsMaterialConverter.convert()` now a class method; old free function `convert()` deprecated

### Fixed
- `base_url` parameter now defaults to `""` in `BaseConverter.convert()` and `MkdocsMaterialConverter.convert()`

---

## [0.1.0] — 2026-05-18

### Added

- **Initial release** — core MkDocs Material → GFM Markdown conversion pipeline
- `validator.py`: Detect MkDocs Material pages via `<meta name="generator">`
- `fetcher.py`: Download HTML via httpx with redirect handling
- `extractor.py`: Extract `<article class="md-content__inner md-typeset">` from full page; fix relative URLs; remove headerlink anchors and code-copy buttons
- `converter.py`: HTML → Markdown via `markdownify` with custom pre/post-processing:
  - **Admonitions**: 11-type mapping to GFM alerts (`> [!NOTE]`, `> [!WARNING]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!CAUTION]`)
  - **Headings**: `<strong>` / `<em>` unwrapping inside `<h1>`-`<h6>`
  - **Task lists**: `<li class="task-list-item">` → `- [ ]` / `- [x]`
  - **Code blocks**: `<div class="highlight"><pre><code>` → fenced ` ``` `
  - **MathJax**: arithmatex `<span>`/`<div>` → `$`/`$$` delimiters
  - **Tabbed sets**: multi-code-block with label annotations
  - **Footnotes**: `[^n]` / `[^n]:` format
  - **Relative links**: resolved to absolute URLs
- `writer.py`: Timestamped naming (`<stem>.<yyyymmddhhmmss>.md`)
- `cli.py`: argparse-based CLI
- 37 unit tests covering validator, extractor, and converter logic
- Project scaffolding: uv-managed dependencies, git-init
