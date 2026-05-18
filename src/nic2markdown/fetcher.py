"""Download HTML content from a URL."""

import httpx

USER_AGENT = "nic2markdown/0.1 (MkDocs to Markdown converter)"
DEFAULT_TIMEOUT = 30.0


class FetchError(Exception):
    """Raised when the page cannot be fetched."""


def fetch(url: str, timeout: float = DEFAULT_TIMEOUT) -> tuple[str, str]:
    """Fetch a URL and return (html_content, final_url).

    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.

    Returns:
        Tuple of (html_text, final_url_after_redirects).

    Raises:
        FetchError: If the request fails or returns a non-2xx status.
    """
    try:
        response = httpx.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=timeout,
            follow_redirects=True,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise FetchError(f"HTTP error: {e.response.status_code} for {url}") from e
    except httpx.RequestError as e:
        raise FetchError(f"Request failed: {e}") from e

    return response.text, str(response.url)
