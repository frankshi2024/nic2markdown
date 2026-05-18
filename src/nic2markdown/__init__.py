"""nic2markdown — Convert documentation pages to GitHub-compatible Markdown."""

__version__ = "0.2.0"

from .gateway import get_converter, detect_framework, get_framework_name
from .frameworks.mkdocs_material.converter import MkdocsMaterialConverter
