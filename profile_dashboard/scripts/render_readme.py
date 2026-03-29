from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "README.template.md"
OUTPUT = ROOT / "README.generated.md"
METRICS = ROOT / "generated" / "metrics.json"
INTEL = ROOT / "generated" / "ai_intelligence.json"
FORECAST = ROOT / "generated" / "forecast.json"
LEARNING = ROOT / "generated" / "learning.json"
EXPERIMENTS = ROOT / "generated" / "experiments.json"
CONSISTENCY = ROOT / "generated" / "consistency.json"

START = "<!-- DASHBOARD_START -->"
END = "<!-- DASHBOARD_END -->"


def badge(label: str, value: str, color: str = "00f5ff") -> str:
    return f"![{label}](https://img.shields.io/badge/{quote(str(label), safe='')}-{quote(str(value), safe='')}-{color}?style=for-the-badge)"


def section_projects_table(projects: list[dict]) -> list[str]:
    lines = ["### 🛰️ Engineering Dashboard", "| Project | Stage | Health | Risk | Next Action |", "|---|---|---:|---|---|"]
    for p in projects:
        lines.append(f"| [{p['name']}]({p['url']}) | {p['stage']} | {p['health_score']}/10 | {p['risk']} | {p['next_action']} |")
    return lines


def render_block(metrics: dict, intel: dict, forecast: dict, learning: dict, experiments: dict, consistency: dict) -> str:
    k = metrics["kpis"]
    lines = [
        "### 📊 GitHub Stats",
        badge("Active Projects", k["active_projects"]),
        badge("Completion Ratio", k["completion_ratio"], "7cfc00"),
        badge("Accuracy Score", k["accuracy_score"], "3da5ff"),
        badge("Activity Score", k["activity_score"], "ffa500"),
        badge("Consistency", f"{k['consistency_score']} ({k['consistency_label']})", "9b59b6"),
        badge("Last Updated", k["last_updated"], "2ecc71"),
        "",
        "### 🧩 Featured Projects",
        "- Laptop Price Predictor (ML)",
        "- Phishing Site Classifier (ML + Cybersecurity)",
        "- Kidney Disease Classification (Healthcare AI)",
        "- Exploratory Data Analysis",
        "- Educational Chatbot (NLP)",
        "",
    ]

    lines.extend(section_projects_table(metrics.get("projects", [])))

    lines.extend(["", "### 🧠 AI Project Intelligence"])
    for item in intel.get("intelligence", [])[:5]:
        lines.append(f"- **{item['name']}** → maturity: `{item['maturity_level']}` | missing: `{', '.join(item['missing_parts'][:2])}`")

    lines.extend(["", "### 🤖 Smart Next Actions"])
    for i, action in enumerate(metrics.get("smart_next_actions", [])[:5], start=1):
        lines.append(f"{i}. **{action['name']}** ({action['priority']}) — {action['action']}")

    lines.extend(["", "### 📈 Progress Forecast", "| Project | Risk | ETA (days) | Target Date |", "|---|---|---:|---|"])
    for row in forecast.get("forecast", [])[:5]:
        lines.append(f"| {row['name']} | {row['risk']} | {row['eta_days']} | {row['eta_date']} |")

    lines.extend(["", "### 📚 Learning Recommendations"])
    for rec in learning.get("recommendations", [])[:6]:
        lines.append(f"- {rec}")

    lines.extend(["", "### 🧪 Experiment Tracker", "| Project | Version | Metric | Value | Last Change |", "|---|---|---|---:|---|"])
    for ex in experiments.get("experiments", [])[:5]:
        lines.append(f"| {ex['project']} | {ex['model_version']} | {ex['metric_name']} | {ex['metric_value']} | {ex['last_change']} |")

    lines.extend(["", "### 🔄 Consistency Tracker"])
    lines.append(f"- Weekly Momentum: **{consistency.get('momentum', 'Unknown')}**")
    lines.append(f"- Weekly Score: **{consistency.get('weekly_score', 0)} / 100**")

    lines.extend(["", "### 📅 Build Timeline"])
    for point in consistency.get("history", [])[-6:]:
        lines.append(f"- {point['date']} → completion `{point['completion_ratio']}`, activity `{point['activity_score']}`")

    lines.extend(["", "### 📈 Activity Graph"])
    owner = metrics.get("owner", "Md786Rizwan")
    lines.append(f"![activity graph](https://github-readme-activity-graph.vercel.app/graph?username={owner}&theme=tokyo-night&hide_border=true)")

    lines.append("")
    lines.append(f"_Last auto-update: {metrics['generated_at']}_")
    return "\n".join(lines)


def replace_section(text: str, new_block: str) -> str:
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    return f"{before}{START}\n{new_block}\n{END}{after}"


def main() -> None:
    template = TEMPLATE.read_text()
    metrics = json.loads(METRICS.read_text())
    intel = json.loads(INTEL.read_text()) if INTEL.exists() else {"intelligence": []}
    forecast = json.loads(FORECAST.read_text()) if FORECAST.exists() else {"forecast": []}
    learning = json.loads(LEARNING.read_text()) if LEARNING.exists() else {"recommendations": []}
    experiments = json.loads(EXPERIMENTS.read_text()) if EXPERIMENTS.exists() else {"experiments": []}
    consistency = json.loads(CONSISTENCY.read_text()) if CONSISTENCY.exists() else {"history": []}

    block = render_block(metrics, intel, forecast, learning, experiments, consistency)
    OUTPUT.write_text(replace_section(template, block))
    print(f"Generated README at {OUTPUT}")


if __name__ == "__main__":
    main()
