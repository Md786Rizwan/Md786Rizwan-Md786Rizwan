from __future__ import annotations

import datetime as dt
import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote_plus
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT / "generated" / "news.json"

RSS_FALLBACK = "https://hnrss.org/frontpage"


def fetch_newsapi(query: str, api_key: str, limit: int = 5) -> list[dict]:
    url = (
        "https://newsapi.org/v2/everything?"
        f"q={quote_plus(query)}&sortBy=publishedAt&pageSize={limit}&language=en&apiKey={api_key}"
    )
    with urlopen(url, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))
    articles = []
    for item in data.get("articles", [])[:limit]:
        articles.append(
            {
                "title": item.get("title", "Untitled"),
                "url": item.get("url", ""),
                "source": (item.get("source") or {}).get("name", "NewsAPI"),
                "published_at": item.get("publishedAt", ""),
            }
        )
    return articles


def fetch_rss(limit: int = 5) -> list[dict]:
    with urlopen(RSS_FALLBACK, timeout=20) as response:
        raw = response.read().decode("utf-8", errors="replace")
    root = ET.fromstring(raw)
    items = root.findall(".//item")[:limit]
    news = []
    for item in items:
        news.append(
            {
                "title": (item.findtext("title") or "Untitled").strip(),
                "url": (item.findtext("link") or "").strip(),
                "source": "Hacker News",
                "published_at": (item.findtext("pubDate") or "").strip(),
            }
        )
    return news


def main() -> None:
    query = os.getenv("NEWS_QUERY", "artificial intelligence machine learning")
    api_key = os.getenv("NEWS_API_KEY", "")

    articles = []
    mode = "rss_fallback"
    if api_key:
        try:
            articles = fetch_newsapi(query, api_key)
            mode = "newsapi"
        except Exception:
            try:
                articles = fetch_rss()
            except Exception:
                articles = []
    else:
        try:
            articles = fetch_rss()
        except Exception:
            articles = []

    if not articles:
        articles = [
            {
                "title": "Set NEWS_API_KEY secret to enable live AI/Tech news feed.",
                "url": "https://newsapi.org/",
                "source": "system",
                "published_at": "",
            }
        ]
        mode = "fallback_placeholder"

    payload = {
        "generated_at": dt.datetime.utcnow().isoformat() + "Z",
        "source_mode": mode,
        "query": query,
        "articles": articles,
    }
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2))
    print(f"News generated at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
