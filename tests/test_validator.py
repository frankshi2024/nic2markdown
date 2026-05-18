"""Tests for the validator module."""

import pytest
from nic2markdown.validator import is_mkdocs_material, get_generator_version, validate, ValidationError

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


class TestIsMkdocsMaterial:
    def test_mkdocs_material(self):
        assert is_mkdocs_material(MKDOCS_HTML) is True

    def test_mkdocs_material_alt_version(self):
        assert is_mkdocs_material(MKDOCS_HTML_ALT) is True

    def test_non_mkdocs(self):
        assert is_mkdocs_material(NON_MKDOCS_HTML) is False

    def test_no_generator(self):
        assert is_mkdocs_material(NO_GENERATOR_HTML) is False


class TestGetGeneratorVersion:
    def test_extracts_version(self):
        version = get_generator_version(MKDOCS_HTML)
        assert version == "mkdocs-1.6.1, mkdocs-material-9.7.6"

    def test_returns_none_for_no_generator(self):
        version = get_generator_version(NO_GENERATOR_HTML)
        assert version is None


class TestValidate:
    def test_valid_page(self):
        version = validate(MKDOCS_HTML)
        assert "mkdocs" in version

    def test_invalid_page_raises(self):
        with pytest.raises(ValidationError, match="Not a MkDocs Material page"):
            validate(NON_MKDOCS_HTML)

    def test_no_generator_raises(self):
        with pytest.raises(ValidationError, match="Not a MkDocs Material page"):
            validate(NO_GENERATOR_HTML)
