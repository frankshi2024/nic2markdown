"""Write converted Markdown to a file with timestamp naming."""

import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


def _stem_from_url(url: str) -> str:
    """Derive a clean filename stem from a URL.

    Examples:
        https://soc.ustc.edu.cn/COD/lab5/  →  lab5
        https://soc.ustc.edu.cn/COD/lab5/flow/  →  flow
        https://example.com/index.html  →  index
    """
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")

    if not path:
        return "index"

    # Get the last segment
    stem = path.rsplit("/", 1)[-1]

    # Remove extension if it's a .html file
    stem = re.sub(r"\.html?$", "", stem)

    return stem or "index"


def _timestamp() -> str:
    """Generate a 14-digit timestamp: yyyymmddhhmmss."""
    return datetime.now().strftime("%Y%m%d%H%M%S")


def write_markdown(content: str, url: str, output_dir: str = ".") -> str:
    """Write markdown content to a file and return the file path.

    File name format: {stem}.{14-digit-timestamp}.md

    Args:
        content: The markdown text.
        url: The source URL (used to derive filename stem).
        output_dir: Directory to write the file to.

    Returns:
        The full path to the written file.
    """
    stem = _stem_from_url(url)
    ts = _timestamp()
    filename = f"{stem}.{ts}.md"

    out_path = Path(output_dir) / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")

    return str(out_path.resolve())
