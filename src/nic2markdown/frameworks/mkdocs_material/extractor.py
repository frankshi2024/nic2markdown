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
    for a in soup.find_all("a", class_="headerlink"):
        a.extract()
    for btn in soup.find_all("button", class_="md-clipboard"):
        btn.extract()
    for span in soup.find_all("span", class_="md-ellipsis"):
        span.unwrap()


class MkdocsMaterialExtractor:
    """Extract article content from MkDocs Material pages."""

    def extract(self, html: str, base_url: str = "") -> str:
        """Extract article inner HTML from the full page HTML.

        Looks for <article class="md-content__inner md-typeset">.

        Raises ExtractionError if no article element is found.
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

        return article.decode_contents()
