from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "README.template.md"
OUTPUT = ROOT / "README.generated.md"
METRICS = ROOT / "generated" / "metrics.json"
NEWS = ROOT / "generated" / "news.json"
INSIGHTS = ROOT / "generated" / "ai_insights.json"
HISTORY = ROOT / "generated" / "metrics_history.json"

START = "<!-- DASHBOARD_START -->"
END = "<!-- DASHBOARD_END -->"


def badge(label: str, value: str, color: str = "00f5ff") -> str:
    safe_label = label.replace(" ", "%20")
    safe_value = str(value).replace(" ", "%20")
    return f"![{label}](https://img.shields.io/badge/{safe_label}-{safe_value}-{color}?style=for-the-badge)"


def build_timeline(history: list[dict]) -> list[str]:
    lines = ["### 📅 Build Timeline"]
    for item in history[-4:]:
        lines.append(
            f"- **{item.get('date')}** — completion: `{item.get('completion_ratio')}`, avg health: `{item.get('avg_health')}`"
        )
    if len(lines) == 1:
        lines.append("- No history yet.")
    return lines


def dashboard_block(data: dict, news: dict, insights: dict, history: list[dict]) -> str:
    kpis = data["kpis"]
    lines = [
        "### ⚡ Live KPI Snapshot",
        "![3D KPI HUD](profile_dashboard/generated/kpi_hud.svg)",
        "![Completion Trend](profile_dashboard/generated/performance_trend.svg)",
        "![Weekly Focus](profile_dashboard/generated/weekly_focus.svg)",
        "",
        badge("Active Projects", kpis["active_projects"]),
        badge("Stalled Projects", kpis["stalled_projects"], "ff5c8a"),
        badge("Completion Ratio", kpis["completion_ratio"], "7cfc00"),
        badge("Accuracy Score", kpis.get("accuracy_score", "n/a"), "3da5ff"),
        badge("Activity Score", kpis.get("activity_score", "n/a"), "ffa500"),
        badge("Last Updated", kpis.get("last_updated", "n/a"), "9b59b6"),
        "",
        "### 📊 Project Command Center",
        "| Project | Stage | Priority | Health | Impact Metric | Next Action |",
        "|---|---|---|---:|---|---|",
    ]

    for p in data["projects"]:
        lines.append(
            f"| [{p['name']}]({p['url']}) | {p['stage']} | {p['priority']} | {p['health_score']}/10 | {p.get('impact_metric', 'Add KPI')} | {p['next_action']} |"
        )

    lines.extend([
        "",
        "### 🤖 Top 3 Next Actions",
    ])
    for idx, item in enumerate(data["top_next_actions"], start=1):
        lines.append(f"{idx}. **{item['name']}** — {item['next_action']}")

    lines.extend(["", "### 📰 Live AI/Tech News"])
    for item in news.get("articles", [])[:5]:
        lines.append(f"- [{item.get('title','Untitled')}]({item.get('url','#')}) — *{item.get('source','source')}*")

    lines.extend(["", "### 🧠 AI Insights"])
    for rec in insights.get("project_recommendations", [])[:3]:
        lines.append(f"- {rec}")
    for learn in insights.get("learning_recommendations", [])[:3]:
        lines.append(f"- 💡 {learn}")

    lines.extend(["", "### 📈 Activity Graph"])
    owner = data.get("owner", "Md786Rizwan")
    lines.append(
        f"![activity graph](https://github-readme-activity-graph.vercel.app/graph?username={owner}&theme=tokyo-night&hide_border=true)"
    )

    lines.extend([""] + build_timeline(history))

    lines.append("")
    lines.append(f"_Last auto-update: {data['generated_at']}_")
    return "\n".join(lines)


def replace_section(text: str, new_block: str) -> str:
    if START not in text or END not in text:
        raise ValueError("Template must include DASHBOARD_START and DASHBOARD_END markers")

    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    return f"{before}{START}\n{new_block}\n{END}{after}"


def main() -> None:
    template_text = TEMPLATE.read_text()
    metrics = json.loads(METRICS.read_text())
    news = json.loads(NEWS.read_text()) if NEWS.exists() else {"articles": []}
    insights = json.loads(INSIGHTS.read_text()) if INSIGHTS.exists() else {"project_recommendations": [], "learning_recommendations": []}
    history = json.loads(HISTORY.read_text()) if HISTORY.exists() else []

    block = dashboard_block(metrics, news, insights, history)
    rendered = replace_section(template_text, block)
    OUTPUT.write_text(rendered)
    print(f"Generated README at {OUTPUT}")


if __name__ == "__main__":
    main()
