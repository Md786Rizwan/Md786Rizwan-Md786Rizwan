from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "README.template.md"
OUTPUT = ROOT / "README.generated.md"
METRICS = ROOT / "generated" / "metrics.json"

START = "<!-- DASHBOARD_START -->"
END = "<!-- DASHBOARD_END -->"


def badge(label: str, value: str, color: str = "00f5ff") -> str:
    safe_label = label.replace(" ", "%20")
    safe_value = str(value).replace(" ", "%20")
    return f"![{label}](https://img.shields.io/badge/{safe_label}-{safe_value}-{color}?style=for-the-badge)"


def dashboard_block(data: dict) -> str:
    kpis = data["kpis"]
    lines = [
        "### ⚡ Live KPI Snapshot",
        "![3D KPI HUD](profile_dashboard/generated/kpi_hud.svg)",
        "",
        "_3D-style HUD card is auto-generated every workflow run._",
        "",
        badge("Active Projects", kpis["active_projects"]),
        badge("Stalled Projects", kpis["stalled_projects"], "ff5c8a"),
        badge("Completion Ratio", kpis["completion_ratio"], "7cfc00"),
        "",
        "### 📊 Project Command Center",
        "| Project | Stage | Priority | Health | Next Action |",
        "|---|---|---|---:|---|",
    ]

    for p in data["projects"]:
        lines.append(
            f"| [{p['name']}]({p['url']}) | {p['stage']} | {p['priority']} | {p['health_score']}/10 | {p['next_action']} |"
        )

    lines.extend([
        "",
        "### 🤖 Top 3 Next Actions",
    ])

    for idx, item in enumerate(data["top_next_actions"], start=1):
        lines.append(f"{idx}. **{item['name']}** — {item['next_action']}")

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
    block = dashboard_block(metrics)
    rendered = replace_section(template_text, block)
    OUTPUT.write_text(rendered)
    print(f"Generated README at {OUTPUT}")

if __name__ == "__main__":
    main()


