"""Tests for the MkDocs Material sidebar link extraction."""

from nic2markdown.frameworks.mkdocs_material.sidebar import (
    extract_sidebar_links,
    format_sidebar_markdown,
)
from nic2markdown.frameworks.base import SidebarLink


MKDOCS_WITH_SIDEBAR = """<!DOCTYPE html>
<html>
<head>
    <meta name="generator" content="mkdocs-1.6.1, mkdocs-material-9.7.6">
</head>
<body>
    <div class="md-sidebar">
        <nav class="md-nav md-nav--primary" aria-label="导航栏" data-md-level="0">
            <ul class="md-nav__list">
                <li class="md-nav__item">
                    <a href="../" class="md-nav__link">首页</a>
                </li>
                <li class="md-nav__item md-nav__item--nested">
                    <nav class="md-nav" data-md-level="1">
                        <ul class="md-nav__list">
                            <li class="md-nav__item">
                                <a href="../lab1/" class="md-nav__link">实验一</a>
                            </li>
                            <li class="md-nav__item md-nav__item--nested">
                                <nav class="md-nav" data-md-level="2">
                                    <ul class="md-nav__list">
                                        <li class="md-nav__item">
                                            <a href="../lab1/rars/" class="md-nav__link">RARS</a>
                                        </li>
                                    </ul>
                                </nav>
                            </li>
                        </ul>
                    </nav>
                </li>
            </ul>
        </nav>
    </div>
    <div class="md-content">
        <article class="md-content__inner md-typeset">
            <h1>Test Page</h1>
        </article>
    </div>
</body>
</html>"""


class TestExtractSidebarLinks:
    def test_extracts_top_level_links(self):
        links = extract_sidebar_links(MKDOCS_WITH_SIDEBAR)
        texts = {l.text for l in links}
        assert "首页" in texts

    def test_extracts_hierarchy_levels(self):
        links = extract_sidebar_links(MKDOCS_WITH_SIDEBAR)
        # 首页: level 0, 实验一: level 1, RARS: level 2
        levels = {l.text: l.level for l in links}
        assert levels.get("首页") == 0
        assert levels.get("实验一") == 1
        assert levels.get("RARS") == 2

    def test_resolves_relative_urls(self):
        links = extract_sidebar_links(
            MKDOCS_WITH_SIDEBAR,
            base_url="https://example.com/docs/"
        )
        for link in links:
            if link.text == "首页":
                assert link.href == "https://example.com/"
            elif link.text == "实验一":
                assert link.href == "https://example.com/lab1/"

    def test_no_sidebar_returns_empty(self):
        html = "<html><body>No sidebar</body></html>"
        links = extract_sidebar_links(html)
        assert links == []


class TestFormatSidebarMarkdown:
    def test_format_basic(self):
        links = [
            SidebarLink(href="https://example.com/", text="首页", level=0),
            SidebarLink(href="https://example.com/lab1/", text="实验一", level=1),
        ]
        md = format_sidebar_markdown(links)
        assert "## Sidebar Links" in md
        assert "- [首页](https://example.com/)" in md
        assert "  - [实验一](https://example.com/lab1/)" in md

    def test_format_empty(self):
        assert format_sidebar_markdown([]) == ""
