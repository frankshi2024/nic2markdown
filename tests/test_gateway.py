"""Tests for the gateway module (framework detection and routing)."""

import pytest
from nic2markdown.gateway import (
    detect_framework,
    get_converter,
    get_framework_name,
    UnsupportedFrameworkError,
)
from nic2markdown.frameworks.mkdocs_material.converter import MkdocsMaterialConverter


MKDOCS_HTML = """<!DOCTYPE html>
<html>
<head>
    <meta name="generator" content="mkdocs-1.6.1, mkdocs-material-9.7.6">
    <title>Test</title>
</head>
<body><article class="md-content__inner md-typeset"><p>Content</p></article></body>
</html>"""

HUGO_HTML = """<!DOCTYPE html>
<html>
<head>
    <meta name="generator" content="Hugo 0.120.0">
    <title>Test</title>
</head>
<body><p>Content</p></body>
</html>"""


class TestDetectFramework:
    def test_detects_mkdocs(self):
        converter = detect_framework(MKDOCS_HTML)
        assert converter is not None
        assert isinstance(converter, MkdocsMaterialConverter)

    def test_returns_none_for_unknown(self):
        converter = detect_framework(HUGO_HTML)
        assert converter is None


class TestGetConverter:
    def test_returns_converter_for_mkdocs(self):
        converter = get_converter(MKDOCS_HTML)
        assert isinstance(converter, MkdocsMaterialConverter)

    def test_raises_for_unknown(self):
        with pytest.raises(UnsupportedFrameworkError, match="Unsupported framework"):
            get_converter(HUGO_HTML)


class TestGetFrameworkName:
    def test_mkdocs_name(self):
        name = get_framework_name(MKDOCS_HTML)
        assert "mkdocs" in name
        assert "9.7.6" in name

    def test_unknown_name(self):
        name = get_framework_name(HUGO_HTML)
        assert name == "unknown"
