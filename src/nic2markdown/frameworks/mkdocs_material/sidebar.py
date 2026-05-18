"""Extract sidebar navigation links from MkDocs Material pages.

Parses <nav class="md-nav--primary"> to build a structured list of
navigation links with hierarchy information.
"""

from urllib.parse import urljoin

from bs4 import BeautifulSoup

from ..base import SidebarLink


def extract_sidebar_links(html: str, base_url: str = "") -> list[SidebarLink]:
    """Extract all navigation links from the left sidebar.

    Parses the primary navigation tree and returns links with their
    nesting level derived from the data-md-level attribute.

    Args:
        html: Full page HTML.
        base_url: Base URL for resolving relative hrefs.

    Returns:
        List of SidebarLink objects with href, text, and level.
    """
    soup = BeautifulSoup(html, "lxml")

    nav = soup.find("nav", class_="md-nav--primary")
    if nav is None:
        return []

    links: list[SidebarLink] = []

    for a in nav.find_all("a", class_="md-nav__link", href=True):
        href = a.get("href", "")
        text = a.get_text(strip=True)

        if not text or not href:
            continue

        # Resolve relative URLs
        if base_url and not href.startswith(("http://", "https://", "#", "mailto:")):
            href = urljoin(base_url, href)

        # Determine nesting level from parent <nav data-md-level="N">
        level = 0
        parent_nav = a.find_parent("nav", class_="md-nav")
        if parent_nav:
            raw_level = parent_nav.get("data-md-level", "0")
            try:
                level = int(raw_level)
            except (ValueError, TypeError):
                level = 0

        links.append(SidebarLink(href=href, text=text, level=level))

    return links


def format_sidebar_markdown(links: list[SidebarLink]) -> str:
    """Format sidebar links as an indented Markdown list.

    Example output:
        ## Sidebar Links

        - [Home](...)
          - [Section](...)
            - [Page](...)
    """
    if not links:
        return ""

    lines = ["## Sidebar Links", ""]

    for link in links:
        indent = "  " * link.level
        lines.append(f"{indent}- [{link.text}]({link.href})")

    return "\n".join(lines) + "\n"
