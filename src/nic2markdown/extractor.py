"""Extract the main article content from a MkDocs Material HTML page."""

from urllib.parse import urljoin

from bs4 import BeautifulSoup


class ExtractionError(Exception):
    """Raised when the article content cannot be found."""


def _fix_relative_urls(soup: BeautifulSoup, base_url: str) -> None:
    """Convert relative URLs in href/src attributes to absolute."""
    if not base_url:
        return

    for tag in soup.find_all(["a", "img", "link", "script"], href=True):
        href = tag["href"]
        if href and not href.startswith(("http://", "https://", "#", "mailto:", "data:", "javascript:")):
            tag["href"] = urljoin(base_url, href)

    for tag in soup.find_all(["img", "script", "source", "video"], src=True):
        src = tag["src"]
        if src and not src.startswith(("http://", "https://", "data:")):
            tag["src"] = urljoin(base_url, src)


def _remove_noise(soup: BeautifulSoup) -> None:
    """Remove elements that don't translate well to Markdown."""
    # Headerlink anchors (the ¶ permalink)
    for a in soup.find_all("a", class_="headerlink"):
        a.extract()

    # Code copy buttons (mkdocs-material adds these)
    for btn in soup.find_all("button", class_="md-clipboard"):
        btn.extract()

    # Empty spans that mkdocs adds for annotation
    for span in soup.find_all("span", class_="md-ellipsis"):
        span.unwrap()


def extract_article(html: str, base_url: str = "") -> str:
    """Extract the article content from a MkDocs Material HTML page.

    Looks for <article class="md-content__inner md-typeset">.

    Args:
        html: The full page HTML.
        base_url: The base URL for resolving relative links.

    Returns:
        The inner HTML of the article element.

    Raises:
        ExtractionError: If no article element is found.
    """
    soup = BeautifulSoup(html, "lxml")

    article = soup.find("article", class_="md-content__inner")
    if article is None:
        raise ExtractionError(
            "Error: Could not find article content. "
            "The page may not be a standard MkDocs Material page."
        )

    _remove_noise(article)
    _fix_relative_urls(article, base_url)

    # Return the inner HTML of the article
    return article.decode_contents()
