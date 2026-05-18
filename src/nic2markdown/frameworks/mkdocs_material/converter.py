"""HTML → GFM Markdown converter for MkDocs Material pages.

Uses markdownify for the base conversion, with pre- and post-processing
to handle MkDocs-specific structures like admonitions, code blocks, tabs,
math, task-lists, and footnotes.
"""

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag
from markdownify import MarkdownConverter

from ..base import BaseConverter, SidebarLink


# ── Admonition type → GFM alert type mapping ──────────────────────────
ADMONITION_MAP: dict[str, str] = {
    "note": "NOTE",
    "info": "NOTE",
    "tip": "TIP",
    "question": "IMPORTANT",
    "warning": "WARNING",
    "danger": "CAUTION",
    "success": "TIP",
    "example": "NOTE",
    "failure": "CAUTION",
    "bug": "CAUTION",
    "abstract": "NOTE",
    "quote": "NOTE",
}


class _ArticleMdConverter(MarkdownConverter):
    """Custom markdownify converter tailored for MkDocs Material articles."""

    def __init__(self, base_url: str = "", **kwargs):
        super().__init__(**kwargs)
        self.base_url = base_url

    def convert_a(self, el: Tag, text: str, parent_tags: list[str]) -> str:
        classes = el.attrs.get("class", [])
        if "headerlink" in classes:
            return ""
        return super().convert_a(el, text, parent_tags)

    def convert_sup(self, el: Tag, text: str, parent_tags: list[str]) -> str:
        return f"[^{text}]" if text.strip() else ""

    def convert_img(self, el: Tag, text: str, parent_tags: list[str]) -> str:
        src = el.attrs.get("src", "")
        if src and self.base_url and not src.startswith(("http://", "https://", "data:")):
            src = urljoin(self.base_url, src)
        alt = el.attrs.get("alt", "")
        return f"![{alt}]({src})"


# ── Preprocessing ──────────────────────────────────────────────────────

def _preprocess_admonitions(soup: BeautifulSoup) -> None:
    for div in soup.find_all("div", class_="admonition"):
        classes = div.get("class", [])
        ad_type = "note"
        for cls in classes:
            if cls != "admonition" and cls in ADMONITION_MAP:
                ad_type = cls
                break
        gfm_type = ADMONITION_MAP.get(ad_type, "NOTE")

        title_p = div.find("p", class_="admonition-title")
        if title_p:
            title_text = title_p.get_text(strip=True)
            title_p.extract()
            if title_text:
                strong_tag = soup.new_tag("strong")
                strong_tag.string = title_text
                p_tag = soup.new_tag("p")
                p_tag.append(strong_tag)
                div.insert(0, p_tag)

        inner = div.decode_contents()
        new_tag = soup.new_tag("admon")
        new_tag["data-type"] = gfm_type
        marker_start = soup.new_string(f"<!--admon:{gfm_type}-->")
        marker_end = soup.new_string("<!--/admon-->")
        new_tag.append(marker_start)
        new_tag.append(BeautifulSoup(inner, "html.parser"))
        new_tag.append(marker_end)
        div.replace_with(new_tag)


def _preprocess_arithmatex(soup: BeautifulSoup) -> None:
    for span in soup.find_all("span", class_="arithmatex"):
        text = span.get_text(strip=True)
        if text.startswith("\\(") and text.endswith("\\)"):
            span.replace_with(f"${text[2:-2]}$")
        elif text.startswith("$") and text.endswith("$"):
            span.replace_with(text)
        else:
            span.replace_with(f"${text}$")

    for div in soup.find_all("div", class_="arithmatex"):
        text = div.get_text(strip=True)
        if text.startswith("\\[") and text.endswith("\\]"):
            div.replace_with(f"\n\n$$\n{text[2:-2].strip()}\n$$\n\n")
        elif text.startswith("$$") and text.endswith("$$"):
            div.replace_with(f"\n\n{text}\n\n")
        else:
            div.replace_with(f"\n\n$$\n{text.strip()}\n$$\n\n")


def _preprocess_tabbed_sets(soup: BeautifulSoup) -> None:
    for tabbed in soup.find_all("div", class_="tabbed-set"):
        labels_div = tabbed.find("div", class_="tabbed-labels")
        content_div = tabbed.find("div", class_="tabbed-content")
        if not labels_div or not content_div:
            continue

        labels = [lb.get_text(strip=True) for lb in labels_div.find_all("label")]
        blocks = content_div.find_all("div", class_="tabbed-block")

        parts = []
        for label, block in zip(labels, blocks):
            code = block.find("pre") or block.find("code")
            code_text = ""
            lang = ""
            if code:
                code_el = code.find("code") if code.name == "pre" else code
                if code_el:
                    for c in code_el.get("class", []):
                        if c.startswith("language-"):
                            lang = c[len("language-"):]
                        elif c.startswith("lang-"):
                            lang = c[len("lang-"):]
                    code_text = code_el.get_text()
            parts.append(f"<!--tab:{label}-->\n```{lang}\n{code_text}\n```")

        replacement = BeautifulSoup("\n\n".join(parts), "lxml")
        tabbed.replace_with(replacement)


def _preprocess_task_lists(soup: BeautifulSoup) -> None:
    for li in soup.find_all("li", class_="task-list-item"):
        checkbox = li.find("input", type="checkbox")
        if checkbox:
            is_checked = checkbox.has_attr("checked")
            checkbox.extract()
            indicator = li.find("span", class_="task-list-indicator")
            if indicator:
                indicator.extract()
            marker = "[x]" if is_checked else "[ ]"
            if li.string:
                li.string.replace_with(f"{marker} {li.string}")
            else:
                li.insert(0, f"{marker} ")

    for ul in soup.find_all("ul", class_="task-list"):
        ul["class"] = [c for c in ul.get("class", []) if c != "task-list"]


def _preprocess_footnotes(soup: BeautifulSoup) -> None:
    footnotes: dict[str, str] = {}
    footnote_section = soup.find("div", class_="footnote")
    if footnote_section:
        for li in footnote_section.find_all("li", id=lambda x: x and x.startswith("fn:")):
            fn_id = li.get("id", "").replace("fn:", "")
            backref = li.find("a", class_="footnote-backref")
            if backref:
                backref.extract()
            text = li.get_text(strip=True)
            footnotes[fn_id] = text
        footnote_section.extract()

    for sup in soup.find_all("sup", class_="footnote-ref"):
        a = sup.find("a")
        if a:
            fn_id = a.get("href", "").lstrip("#fn:").replace("fn:", "")
            sup.replace_with(f"[^{fn_id}]")

    if footnotes:
        lines = ["\n"]
        for fn_id, text in sorted(footnotes.items()):
            lines.append(f"[^{fn_id}]: {text}")
        soup.append(BeautifulSoup("\n".join(lines), "lxml"))


def _preprocess_headings(soup: BeautifulSoup) -> None:
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        for bold in tag.find_all(["strong", "b", "em", "i"]):
            bold.unwrap()


def _preprocess(soup: BeautifulSoup) -> None:
    _preprocess_headings(soup)
    _preprocess_admonitions(soup)
    _preprocess_arithmatex(soup)
    _preprocess_tabbed_sets(soup)
    _preprocess_task_lists(soup)
    _preprocess_footnotes(soup)


# ── Postprocessing ─────────────────────────────────────────────────────

def _postprocess_admonitions(text: str) -> str:
    def _replace(m: re.Match) -> str:
        gfm_type = m.group(1)
        content = m.group(2).strip()
        lines = content.split("\n")
        result = [f"> [!{gfm_type}]"]
        for line in lines:
            if line.strip():
                result.append(f"> {line}")
            else:
                result.append(">")
        return "\n".join(result)

    return re.sub(
        r"<!--admon:(\w+)-->\n?(.*?)\n?<!--/admon-->",
        _replace, text, flags=re.DOTALL,
    )


def _postprocess_tab_labels(text: str) -> str:
    return re.sub(r"<!--tab:(.*?)-->", r"*\\{\1\\}*\n", text)


def _postprocess_whitespace(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text)


def _postprocess_relative_links(text: str, base_url: str) -> str:
    if not base_url:
        return text

    def _fix_link(m: re.Match) -> str:
        link_text = m.group(1)
        url = m.group(2)
        if url.startswith(("http://", "https://", "#", "mailto:", "data:")):
            return m.group(0)
        full = urljoin(base_url, url)
        return f"[{link_text}]({full})"

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _fix_link, text)


def _postprocess(text: str, base_url: str = "") -> str:
    text = _postprocess_admonitions(text)
    text = _postprocess_tab_labels(text)
    text = _postprocess_whitespace(text)
    if base_url:
        text = _postprocess_relative_links(text, base_url)
    return text.strip() + "\n"


# ── Main Converter Class ───────────────────────────────────────────────

class MkdocsMaterialConverter(BaseConverter):
    """Converter for MkDocs Material documentation pages."""

    @staticmethod
    def detect(html: str) -> bool:
        from .validator import detect as _detect
        return _detect(html)

    def extract_article(self, html: str, base_url: str) -> str:
        from .extractor import MkdocsMaterialExtractor
        extractor = MkdocsMaterialExtractor()
        return extractor.extract(html, base_url)

    def convert(self, article_html: str, base_url: str = "") -> str:
        soup = BeautifulSoup(article_html, "lxml")
        _preprocess(soup)
        md_converter = _ArticleMdConverter(base_url=base_url, heading_style="ATX")
        md = md_converter.convert_soup(soup)
        return _postprocess(md, base_url=base_url)

    def extract_sidebar_links(self, html: str, base_url: str) -> list[SidebarLink]:
        from .sidebar import extract_sidebar_links as _extract
        return _extract(html, base_url)
