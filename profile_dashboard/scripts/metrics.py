from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_FILE = ROOT / "projects.json"
OUTPUT_FILE = ROOT / "generated" / "metrics.json"
HUD_FILE = ROOT / "generated" / "kpi_hud.svg"

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
    HUD_FILE.write_text(build_hud_svg(metrics))
    print(f"Metrics generated at {OUTPUT_FILE}")
    print(f"HUD SVG generated at {HUD_FILE}")


def build_hud_svg(metrics: dict) -> str:
    kpis = metrics["kpis"]
    date = metrics["generated_at"]
    active = kpis["active_projects"]
    stalled = kpis["stalled_projects"]
    completion = kpis["completion_ratio"]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="260" viewBox="0 0 1100 260" role="img" aria-label="KPI HUD">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#07101F"/>
      <stop offset="100%" stop-color="#0E1B2F"/>
    </linearGradient>
    <linearGradient id="cyan" x1="0" x2="1">
      <stop offset="0%" stop-color="#00E5FF"/>
      <stop offset="100%" stop-color="#00FFC6"/>
    </linearGradient>
    <linearGradient id="pink" x1="0" x2="1">
      <stop offset="0%" stop-color="#FF4D94"/>
      <stop offset="100%" stop-color="#FF7AD9"/>
    </linearGradient>
    <linearGradient id="green" x1="0" x2="1">
      <stop offset="0%" stop-color="#9BFF00"/>
      <stop offset="100%" stop-color="#59FF9C"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1100" height="260" fill="url(#bg)" rx="20"/>
  <rect x="22" y="20" width="1056" height="220" fill="none" stroke="#1B355A" stroke-width="2" rx="14"/>

  <text x="40" y="58" fill="#EAF3FF" font-size="28" font-family="Segoe UI, Arial" font-weight="700">🚀 Md786Rizwan KPI HUD</text>
  <text x="40" y="84" fill="#8FB7FF" font-size="14" font-family="Segoe UI, Arial">Auto-updated: {date}</text>

  <rect x="40" y="108" width="320" height="110" rx="14" fill="#0A1628" stroke="#0DEBFF" stroke-width="2" filter="url(#glow)"/>
  <text x="62" y="140" fill="#9ADFFF" font-size="15" font-family="Segoe UI, Arial">ACTIVE PROJECTS</text>
  <text x="62" y="192" fill="url(#cyan)" font-size="46" font-family="Consolas, monospace" font-weight="700">{active}</text>

  <rect x="390" y="108" width="320" height="110" rx="14" fill="#0A1628" stroke="#FF6AB3" stroke-width="2" filter="url(#glow)"/>
  <text x="412" y="140" fill="#FFB8DB" font-size="15" font-family="Segoe UI, Arial">STALLED PROJECTS</text>
  <text x="412" y="192" fill="url(#pink)" font-size="46" font-family="Consolas, monospace" font-weight="700">{stalled}</text>

  <rect x="740" y="108" width="320" height="110" rx="14" fill="#0A1628" stroke="#A5FF3E" stroke-width="2" filter="url(#glow)"/>
  <text x="762" y="140" fill="#D8FFB2" font-size="15" font-family="Segoe UI, Arial">COMPLETION RATIO</text>
  <text x="762" y="192" fill="url(#green)" font-size="46" font-family="Consolas, monospace" font-weight="700">{completion}</text>
</svg>
"""


if __name__ == "__main__":
    main()
