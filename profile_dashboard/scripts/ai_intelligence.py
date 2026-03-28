from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS_FILE = ROOT / "generated" / "metrics.json"
OUTPUT_FILE = ROOT / "generated" / "ai_intelligence.json"


def maturity(stage: str) -> str:
    mapping = {"idea": "Concept", "poc": "Validation", "mvp": "Execution", "prod": "Scale"}
    return mapping.get(stage.lower(), "Unknown")


def default_missing(stage: str) -> list[str]:
    stage = stage.lower()
    if stage == "poc":
        return ["robust evaluation", "deployment pipeline", "monitoring"]
    if stage == "mvp":
        return ["model monitoring", "error analysis", "automated retraining"]
    if stage == "prod":
        return ["cost optimization", "A/B experiments"]
    return ["baseline model", "dataset quality checks"]


def main() -> None:
    data = json.loads(METRICS_FILE.read_text())
    projects = data.get("projects", [])

    intelligence = []
    for p in projects:
        stage = p.get("stage", "idea")
        missing = p.get("missing_parts", default_missing(stage))
        suggestion = f"Improve {p.get('name')} by focusing on {missing[0]} this sprint."
        intelligence.append(
            {
                "name": p.get("name"),
                "maturity_level": maturity(stage),
                "missing_parts": missing,
                "improvement_suggestion": suggestion,
            }
        )

    payload = {
        "generated_at": dt.datetime.utcnow().isoformat() + "Z",
        "intelligence": intelligence,
    }
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2))
    print(f"AI intelligence generated at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
