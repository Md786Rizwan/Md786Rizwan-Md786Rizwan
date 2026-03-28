from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS_FILE = ROOT / "generated" / "metrics.json"
NEWS_FILE = ROOT / "generated" / "news.json"
ACTIVITY_FILE = ROOT / "generated" / "activity.json"
OUTPUT_FILE = ROOT / "generated" / "ai_insights.json"


def summarize_headline(title: str) -> str:
    words = title.split()
    return " ".join(words[:12]) + ("..." if len(words) > 12 else "")


def main() -> None:
    metrics = json.loads(METRICS_FILE.read_text())
    news = json.loads(NEWS_FILE.read_text()) if NEWS_FILE.exists() else {"articles": []}
    activity = json.loads(ACTIVITY_FILE.read_text()) if ACTIVITY_FILE.exists() else {"recent_push_events": 0}

    projects = metrics.get("projects", [])
    stalled = [p for p in projects if p.get("is_stalled")]
    top_actions = metrics.get("top_next_actions", [])

    learning = []
    for article in news.get("articles", [])[:3]:
        learning.append(f"Read: {summarize_headline(article.get('title', ''))}")

    if metrics["kpis"]["completion_ratio"] < 0.7:
        learning.append("Improve project closure by moving at least one POC to MVP this week.")
    if activity.get("recent_push_events", 0) < 3:
        learning.append("Increase commit cadence: target 1 meaningful push every 2 days.")

    payload = {
        "generated_at": dt.datetime.utcnow().isoformat() + "Z",
        "news_summaries": [
            {
                "title": a.get("title", ""),
                "summary": summarize_headline(a.get("title", "")),
                "url": a.get("url", ""),
            }
            for a in news.get("articles", [])[:5]
        ],
        "project_recommendations": [
            f"Prioritize {item['name']}: {item['next_action']}" for item in top_actions
        ],
        "risk_alerts": [f"Stalled: {p['name']}" for p in stalled],
        "learning_recommendations": learning[:5],
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2))
    print(f"AI insights generated at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
