"""CLI entry point for nic2markdown."""

import argparse
import sys

from .fetcher import fetch, FetchError
from .gateway import get_converter, get_framework_name, UnsupportedFrameworkError
from .frameworks.mkdocs_material.extractor import ExtractionError
from .frameworks.mkdocs_material.sidebar import format_sidebar_markdown
from .writer import write_markdown


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="nic2markdown",
        description="Convert MkDocs Material HTML pages to GitHub-compatible Markdown.",
    )
    parser.add_argument(
        "url",
        help="URL of the documentation page to convert",
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="output",
        help="Directory to write the output Markdown file (default: output/)",
    )
    parser.add_argument(
        "-s", "--sidebar",
        action="store_true",
        default=False,
        help="Extract and append sidebar navigation links (default: off)",
    )
    args = parser.parse_args()

    url = args.url
    output_dir = args.output_dir
    include_sidebar = args.sidebar

    try:
        # Step 1: Fetch
        print(f"Fetching {url} ...")
        html, final_url = fetch(url)
        if final_url != url:
            print(f"  (redirected to {final_url})")

        # Step 2: Detect framework & get converter
        print("Detecting framework ...")
        framework_name = get_framework_name(html)
        print(f"  Detected: {framework_name}")

        converter = get_converter(html)

        # Step 3: Extract article
        article_html = converter.extract_article(html, base_url=final_url)
        word_count = len(article_html.split())
        print(f"  Article extracted ({word_count} words)")

        # Step 4: Convert
        print("Converting to Markdown ...")
        markdown = converter.convert(article_html, base_url=final_url)

        # Step 5: Optionally extract sidebar links
        if include_sidebar:
            print("Extracting sidebar links ...")
            sidebar_links = converter.extract_sidebar_links(html, base_url=final_url)
            if sidebar_links:
                sidebar_md = format_sidebar_markdown(sidebar_links)
                markdown += "\n" + sidebar_md
                print(f"  {len(sidebar_links)} sidebar links appended")
            else:
                print("  No sidebar links found")

        # Step 6: Write
        out_path = write_markdown(markdown, url=final_url, output_dir=output_dir)
        print(f"\n[OK] Written to: {out_path}")

    except UnsupportedFrameworkError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except FetchError as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)
    except ExtractionError as e:
        print(str(e), file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(4)


if __name__ == "__main__":
    main()
