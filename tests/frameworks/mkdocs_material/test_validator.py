"""Tests for the validator module."""

from nic2markdown.frameworks.mkdocs_material.validator import detect, get_version

MKDOCS_HTML = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="generator" content="mkdocs-1.6.1, mkdocs-material-9.7.6">
    <title>Test</title>
</head>
<body><p>Hello</p></body>
</html>"""

MKDOCS_HTML_ALT = """<!DOCTYPE html>
<html>
<head>
    <meta name="generator" content="mkdocs-1.5.0, mkdocs-material-9.4.0">
    <title>Test</title>
</head>
<body><p>Hello</p></body>
</html>"""

NON_MKDOCS_HTML = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="generator" content="Hugo 0.120.0">
    <title>Test</title>
</head>
<body><p>Hello</p></body>
</html>"""

NO_GENERATOR_HTML = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Test</title>
</head>
<body><p>Hello</p></body>
</html>"""


class TestDetect:
    def test_mkdocs_material(self):
        assert detect(MKDOCS_HTML) is True

    def test_mkdocs_material_alt_version(self):
        assert detect(MKDOCS_HTML_ALT) is True

    def test_non_mkdocs(self):
        assert detect(NON_MKDOCS_HTML) is False

    def test_no_generator(self):
        assert detect(NO_GENERATOR_HTML) is False


class TestGetVersion:
    def test_extracts_version(self):
        version = get_version(MKDOCS_HTML)
        assert version == "mkdocs-1.6.1, mkdocs-material-9.7.6"

    def test_returns_none_for_no_generator(self):
        version = get_version(NO_GENERATOR_HTML)
        assert version is None
