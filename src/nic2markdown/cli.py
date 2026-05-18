"""CLI entry point for nic2markdown."""

import argparse
import sys

from .fetcher import fetch, FetchError
from .validator import validate, ValidationError
from .extractor import extract_article, ExtractionError
from .converter import convert
from .writer import write_markdown


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="nic2markdown",
        description="Convert MkDocs Material HTML pages to GitHub-compatible Markdown.",
    )
    parser.add_argument(
        "url",
        help="URL of the MkDocs Material page to convert",
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=".",
        help="Directory to write the output Markdown file (default: current directory)",
    )
    args = parser.parse_args()

    url = args.url
    output_dir = args.output_dir

    try:
        # Step 1: Fetch
        print(f"Fetching {url} ...")
        html, final_url = fetch(url)
        if final_url != url:
            print(f"  (redirected to {final_url})")

        # Step 2: Validate
        version = validate(html)
        print(f"  Detected: {version}")

        # Step 3: Extract article
        article_html = extract_article(html, base_url=final_url)
        word_count = len(article_html.split())
        print(f"  Article extracted ({word_count} words)")

        # Step 4: Convert
        print("Converting to Markdown ...")
        markdown = convert(article_html, base_url=final_url)

        # Step 5: Write
        out_path = write_markdown(markdown, url=final_url, output_dir=output_dir)
        print(f"\n[OK] Written to: {out_path}")

    except ValidationError as e:
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
