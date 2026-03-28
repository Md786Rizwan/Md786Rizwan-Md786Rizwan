from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_FILE = ROOT / "projects.json"
OUTPUT_FILE = ROOT / "generated" / "metrics.json"

PRIORITY_WEIGHT = {"high": 3, "medium": 2, "low": 1}
STAGE_WEIGHT = {"prod": 4, "mvp": 3, "poc": 2, "idea": 1}


def parse_date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def health_score(project: dict, today: dt.date) -> int:
    priority = PRIORITY_WEIGHT.get(str(project.get("priority", "low")).lower(), 1)
    stage = STAGE_WEIGHT.get(str(project.get("stage", "idea")).lower(), 1)
    last_updated = parse_date(project.get("last_updated", str(today)))
    stale_days = (today - last_updated).days
    freshness_bonus = 3 if stale_days <= 7 else (1 if stale_days <= 14 else -2)
    return max(1, min(10, priority + stage + freshness_bonus))


def main() -> None:
    today = dt.date.today()
    raw = json.loads(PROJECTS_FILE.read_text())
    projects = raw.get("projects", [])

    enriched = []
    stalled = 0

    for project in projects:
        score = health_score(project, today)
        last_updated = parse_date(project["last_updated"])
        is_stalled = (today - last_updated).days > 14
        stalled += 1 if is_stalled else 0

        enriched_project = {
            **project,
            "health_score": score,
            "is_stalled": is_stalled,
        }
        enriched.append(enriched_project)

    ranked_actions = sorted(
        enriched,
        key=lambda p: (
            PRIORITY_WEIGHT.get(str(p.get("priority", "low")).lower(), 1),
            p["health_score"],
        ),
        reverse=True,
    )

    completion_ratio = round(
        sum(1 for p in enriched if str(p.get("stage", "")).lower() in {"mvp", "prod"})
        / max(len(enriched), 1),
        2,
    )

    metrics = {
        "generated_at": today.isoformat(),
        "owner": raw.get("owner", "unknown"),
        "kpis": {
            "active_projects": len(enriched),
            "stalled_projects": stalled,
            "completion_ratio": completion_ratio,
        },
        "top_next_actions": [
            {
                "name": p["name"],
                "next_action": p.get("next_action", "No action specified"),
            }
            for p in ranked_actions[:3]
        ],
        "projects": enriched,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(metrics, indent=2))
    print(f"Metrics generated at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
