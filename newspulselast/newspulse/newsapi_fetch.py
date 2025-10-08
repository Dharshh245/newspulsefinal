import sys
from typing import List, Dict

import requests


# Replace this with your actual NewsAPI key
API_KEY = "your_api_key_here"


def fetch_latest_articles(api_key: str, keyword: str, max_results: int = 10) -> List[Dict]:
    """Fetch the latest news articles matching the keyword from NewsAPI.

    Args:
        api_key: NewsAPI API key string.
        keyword: Search term provided by the user.
        max_results: Maximum number of articles to fetch (default 10).

    Returns:
        A list of article dictionaries (possibly empty if no results).

    Raises:
        RuntimeError: For API-level errors (e.g., invalid key, rate limit).
    """
    endpoint = "https://newsapi.org/v2/everything"
    params = {
        "q": keyword,
        "sortBy": "publishedAt",
        "pageSize": max_results,
        "language": "en",
    }
    headers = {"X-Api-Key": api_key}

    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=15)
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Network error while contacting NewsAPI: {exc}") from exc

    # Parse response
    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError("Failed to parse NewsAPI response as JSON") from exc

    # Handle API-level errors according to NewsAPI spec
    status = payload.get("status")
    if status != "ok":
        message = payload.get("message", "Unknown error from NewsAPI")
        code = payload.get("code", "")
        # Provide friendlier messages for common cases
        if code in {"apiKeyMissing", "apiKeyInvalid", "apiKeyDisabled"}:
            raise RuntimeError("API key error: " + message)
        if code in {"rateLimited", "maximumResultsReached"}:
            raise RuntimeError("Rate limit error: " + message)
        raise RuntimeError(f"NewsAPI error: {message}")

    articles = payload.get("articles", [])
    if not isinstance(articles, list):
        raise RuntimeError("Unexpected response format from NewsAPI: 'articles' is not a list")

    return articles


def print_articles(articles: List[Dict]) -> None:
    """Print articles in a clean format: title, source, URL."""
    if not articles:
        print("No articles found for the given keyword.")
        return

    for idx, article in enumerate(articles, start=1):
        title = article.get("title") or "(No title)"
        source = (article.get("source") or {}).get("name") or "(Unknown source)"
        url = article.get("url") or "(No URL)"
        print(f"{idx}. {title}\n   Source: {source}\n   URL: {url}\n")


def main() -> None:
    if not API_KEY or API_KEY == "your_api_key_here":
        print("Error: Please set your NewsAPI key in the API_KEY variable.")
        sys.exit(1)

    try:
        keyword = input("Enter a search keyword for news: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
        sys.exit(1)

    if not keyword:
        print("Error: Keyword cannot be empty.")
        sys.exit(1)

    try:
        articles = fetch_latest_articles(API_KEY, keyword, max_results=10)
    except RuntimeError as err:
        print(f"Failed to fetch articles: {err}")
        sys.exit(1)

    print_articles(articles)


if __name__ == "__main__":
    main()


