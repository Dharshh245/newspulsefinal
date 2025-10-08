from __future__ import annotations

import os
import time
from typing import List, Literal, Dict, Tuple

import requests


Category = Literal[
    "entertainment",
    "finance",
    "business",
    "technology",
    "sports",
    "science",
    "health",
    "world",
    "nation",
]


class NewsApiError(Exception):
    pass


def _map_category_for_gnews(category: Category) -> str:
    # GNews categories: general, world, nation, business, technology, entertainment, sports, science, health
    if category == "finance":
        return "business"
    if category in {"business", "technology", "entertainment", "sports", "science", "health", "world", "nation"}:
        return category
    # default fallback
    return "entertainment"


def _request_with_retry(url: str, params: Dict, max_attempts: int = 4, base_delay: float = 1.0) -> requests.Response:
    attempt = 0
    last_exc: Exception | None = None
    while attempt < max_attempts:
        try:
            resp = requests.get(url, params=params, timeout=15)
            # Handle explicit 429 with Retry-After if present
            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After")
                delay = float(retry_after) if retry_after and retry_after.isdigit() else base_delay * (2 ** attempt)
                time.sleep(min(delay, 10.0))
                attempt += 1
                continue
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            last_exc = e
            # Backoff on network or 5xx errors
            status = getattr(getattr(e, 'response', None), 'status_code', None)
            if status and status < 500:
                break
            time.sleep(min(base_delay * (2 ** attempt), 10.0))
            attempt += 1
    if last_exc:
        raise last_exc
    raise requests.RequestException("Request failed without exception")


def fetch_gnews(category: Category, limit: int = 20, api_key: str | None = None) -> List[str]:
    key = api_key or os.getenv("GNEWS_API_KEY", "").strip()
    if not key:
        raise NewsApiError("GNEWS_API_KEY is not configured")

    mapped_category = _map_category_for_gnews(category)
    url = "https://gnews.io/api/v4/top-headlines"
    params = {
        "token": key,
        "lang": "en",
        "category": mapped_category,
        "max": max(1, min(100, int(limit))),
    }

    try:
        resp = _request_with_retry(url, params)
        data = resp.json() or {}
        articles = data.get("articles", []) or []
        texts: List[str] = []
        for a in articles:
            title = (a.get("title") or "").strip()
            desc = (a.get("description") or "").strip()
            content = f"{title}. {desc}".strip(". ")
            if content:
                texts.append(content)
        if not texts:
            raise NewsApiError("No articles returned from GNews")
        return texts
    except requests.RequestException as e:
        raise NewsApiError(f"GNews request failed: {e}")
    except ValueError:
        raise NewsApiError("GNews returned invalid JSON")


# GDELT support removed per app requirements


def fetch_live_news(provider: Literal["gnews", "gdelt"], category: Category, limit: int = 20) -> List[str]:
    # Backwards compatibility for existing code paths; now only GNews is supported
    return fetch_gnews(category, limit)


def fetch_gnews_articles(category: Category, limit: int = 20, api_key: str | None = None) -> List[Dict]:
    key = api_key or os.getenv("GNEWS_API_KEY", "").strip()
    if not key:
        raise NewsApiError("GNEWS_API_KEY is not configured")

    mapped_category = _map_category_for_gnews(category)
    url = "https://gnews.io/api/v4/top-headlines"
    params = {
        "token": key,
        "lang": "en",
        "category": mapped_category,
        "max": max(1, min(100, int(limit))),
    }

    try:
        resp = _request_with_retry(url, params)
        data = resp.json() or {}
        articles = data.get("articles", []) or []
        items: List[Dict] = []
        for a in articles:
            title = (a.get("title") or "").strip()
            description = (a.get("description") or "").strip()
            url_ = (a.get("url") or "").strip()
            image = (a.get("image") or "").strip()
            source = ((a.get("source") or {}).get("name") or "").strip()
            content = ". ".join([p for p in [title, description] if p]).strip(". ")
            if title or description:
                items.append({
                    "id": url_ or title,
                    "title": title,
                    "description": description,
                    "image": image,
                    "url": url_,
                    "source": source,
                    "content": content,
                })
        if not items:
            raise NewsApiError("No articles returned from GNews")
        return items
    except requests.RequestException as e:
        # Provide a friendlier message for rate limiting
        status = getattr(getattr(e, 'response', None), 'status_code', None)
        if status == 429:
            raise NewsApiError("GNews rate limit reached. Please try again in a moment.")
        raise NewsApiError(f"GNews request failed: {e}")
    except ValueError:
        raise NewsApiError("GNews returned invalid JSON")


# GDELT article support removed


def fetch_live_news_articles(provider: Literal["gnews", "gdelt"], category: Category, limit: int = 20) -> List[Dict]:
    # Backwards-compatible signature; provider ignored, only GNews used
    return fetch_gnews_articles(category, limit)

def fetch_news_category(category: Category, limit: int = 20) -> List[Dict]:
    return fetch_gnews_articles(category, limit)


def search_gnews(query: str, limit: int = 20, api_key: str | None = None) -> List[Dict]:
    key = api_key or os.getenv("GNEWS_API_KEY", "").strip()
    if not key:
        raise NewsApiError("GNEWS_API_KEY is not configured")

    url = "https://gnews.io/api/v4/search"
    params = {
        "token": key,
        "lang": "en",
        "q": query.strip(),
        "max": max(1, min(100, int(limit))),
    }

    try:
        resp = _request_with_retry(url, params)
        data = resp.json() or {}
        articles = data.get("articles", []) or []
        items: List[Dict] = []
        for a in articles:
            title = (a.get("title") or "").strip()
            description = (a.get("description") or "").strip()
            url_ = (a.get("url") or "").strip()
            image = (a.get("image") or "").strip()
            source = ((a.get("source") or {}).get("name") or "").strip()
            content = ". ".join([p for p in [title, description] if p]).strip(". ")
            if title or description:
                items.append({
                    "id": url_ or title,
                    "title": title,
                    "description": description,
                    "image": image,
                    "url": url_,
                    "source": source,
                    "content": content,
                })
        if not items:
            raise NewsApiError("No results returned from GNews search")
        return items
    except requests.RequestException as e:
        status = getattr(getattr(e, 'response', None), 'status_code', None)
        if status == 429:
            raise NewsApiError("GNews rate limit reached. Please try again in a moment.")
        raise NewsApiError(f"GNews search failed: {e}")
    except ValueError:
        raise NewsApiError("GNews returned invalid JSON")
