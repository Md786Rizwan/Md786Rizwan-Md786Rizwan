from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_FILE = ROOT / "projects.json"
OUTPUT_FILE = ROOT / "generated" / "metrics.json"
HISTORY_FILE = ROOT / "generated" / "metrics_history.json"
CONSISTENCY_FILE = ROOT / "generated" / "consistency.json"

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


def consistency_score(projects: list[dict], today: dt.date) -> tuple[int, str]:
    recent = 0
    for p in projects:
        days = (today - parse_date(p.get("last_updated", str(today)))).days
        if days <= 7:
            recent += 1
    ratio = recent / max(len(projects), 1)
    score = int(ratio * 100)
    label = "High" if score >= 70 else ("Medium" if score >= 40 else "Low")
    return score, label


def update_history(today: dt.date, kpis: dict) -> list[dict]:
    history = load_json_list(HISTORY_FILE)
    key = today.isoformat()
    history = [h for h in history if h.get("date") != key]
    history.append(
        {
            "date": key,
            "completion_ratio": kpis["completion_ratio"],
            "consistency_score": kpis["consistency_score"],
            "activity_score": kpis["activity_score"],
        }
    )
    history = sorted(history, key=lambda x: x["date"])[-20:]
    HISTORY_FILE.write_text(json.dumps(history, indent=2))
    return history


def load_json_list(path: Path) -> list[dict]:
    if not path.exists():
        return []
    raw = path.read_text().strip()
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return []
    return parsed if isinstance(parsed, list) else []


def main() -> None:
    today = dt.date.today()
    raw = json.loads(PROJECTS_FILE.read_text())
    projects = raw.get("projects", [])

    enriched = []
    stalled = 0
    for p in projects:
        score = health_score(p, today)
        stale_days = (today - parse_date(p.get("last_updated", str(today)))).days
        risk = "high" if stale_days > 21 else ("medium" if stale_days > 10 else "low")
        is_stalled = stale_days > 14
        stalled += 1 if is_stalled else 0
        enriched.append({**p, "health_score": score, "risk": risk, "is_stalled": is_stalled})

    ranked = sorted(
        enriched,
        key=lambda p: (PRIORITY_WEIGHT.get(str(p.get("priority", "low")).lower(), 1), p["health_score"]),
        reverse=True,
    )

    completion_ratio = round(
        sum(1 for p in enriched if str(p.get("stage", "")).lower() in {"mvp", "prod"}) / max(len(enriched), 1),
        2,
    )
    avg_accuracy = round(sum(float(p.get("metric_value", 0.0)) for p in enriched) / max(len(enriched), 1), 2)
    activity_score = int(sum(max(0, 10 - (today - parse_date(p.get("last_updated", str(today)))).days // 3) for p in enriched) / max(len(enriched), 1) * 10)
    cons_score, cons_label = consistency_score(enriched, today)

    kpis = {
        "active_projects": len(enriched),
        "stalled_projects": stalled,
        "completion_ratio": completion_ratio,
        "accuracy_score": avg_accuracy,
        "activity_score": activity_score,
        "consistency_score": cons_score,
        "consistency_label": cons_label,
        "last_updated": today.isoformat(),
    }

    payload = {
        "generated_at": today.isoformat(),
        "owner": raw.get("owner", "Md786Rizwan"),
        "profile_repo": raw.get("profile_repo", "Md786Rizwan/Md786Rizwan"),
        "kpis": kpis,
        "projects": enriched,
        "smart_next_actions": [
            {"name": p["name"], "action": p.get("next_action", "Define next milestone"), "priority": p.get("priority", "medium")}
            for p in ranked[:5]
        ],
    }

    history = update_history(today, kpis)
    consistency_payload = {
        "generated_at": today.isoformat(),
        "weekly_score": cons_score,
        "momentum": cons_label,
        "history": history[-8:],
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2))
    CONSISTENCY_FILE.write_text(json.dumps(consistency_payload, indent=2))
    print(f"Metrics generated at {OUTPUT_FILE}")
    print(f"Consistency generated at {CONSISTENCY_FILE}")


if __name__ == "__main__":
    main()
