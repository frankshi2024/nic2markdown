"""Tests for the extractor module."""

import pytest
from nic2markdown.frameworks.mkdocs_material.extractor import MkdocsMaterialExtractor, ExtractionError

extractor = MkdocsMaterialExtractor()

MKDOCS_FULL_PAGE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="generator" content="mkdocs-1.6.1, mkdocs-material-9.7.6">
    <link rel="stylesheet" href="assets/main.css">
</head>
<body>
    <header class="md-header">
        <nav>Site Navigation</nav>
    </header>
    <main>
        <div class="md-sidebar">
            <ul><li><a href="../page1/">Page 1</a></li></ul>
        </div>
        <div class="md-content">
            <article class="md-content__inner md-typeset">
                <h1 id="hello">Hello World<a class="headerlink" href="#hello">&para;</a></h1>
                <p>This is the <strong>main</strong> content.</p>
                <a href="next.html">Next page</a>
                <img src="img/photo.png" alt="Photo">
            </article>
        </div>
    </main>
</body>
</html>"""

MKDOCS_PAGE_NO_ARTICLE = """<!DOCTYPE html>
<html>
<head>
    <meta name="generator" content="mkdocs-1.6.1, mkdocs-material-9.7.6">
</head>
<body>
    <main>
        <div class="md-content">
            <p>No article here</p>
        </div>
    </main>
</body>
</html>"""


class TestExtractArticle:
    def test_extracts_article_content(self):
        result = extractor.extract(MKDOCS_FULL_PAGE)
        assert "Hello World" in result
        assert "main" in result
        assert "content" in result

    def test_removes_headerlink(self):
        result = extractor.extract(MKDOCS_FULL_PAGE)
        assert "headerlink" not in result
        assert "&para;" not in result

    def test_fixes_relative_links(self):
        result = extractor.extract(
            MKDOCS_FULL_PAGE,
            base_url="https://example.com/docs/page/"
        )
        # Relative href should become absolute
        assert 'href="https://example.com/docs/page/next.html"' in result or \
               "href=\"https://example.com/docs/page/next.html\"" in result

    def test_fixes_relative_images(self):
        result = extractor.extract(
            MKDOCS_FULL_PAGE,
            base_url="https://example.com/docs/page/"
        )
        assert 'src="https://example.com/docs/page/img/photo.png"' in result or \
               "src=\"https://example.com/docs/page/img/photo.png\"" in result

    def test_raises_when_no_article(self):
        with pytest.raises(ExtractionError, match="Could not find article"):
            extractor.extract(MKDOCS_PAGE_NO_ARTICLE)

    def test_keeps_content_structure(self):
        result = extractor.extract(MKDOCS_FULL_PAGE)
        assert "<h1" in result
        assert "<p>" in result
        assert "<strong>" in result
