from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_FILE = ROOT / "projects.json"
OUTPUT_FILE = ROOT / "generated" / "experiments.json"


def main() -> None:
    projects = json.loads(PROJECTS_FILE.read_text()).get("projects", [])
    experiments = []
    for p in projects:
        experiments.append(
            {
                "project": p.get("name"),
                "model_version": p.get("model_version", "v1.0"),
                "metric_name": p.get("impact_metric", "primary metric"),
                "metric_value": p.get("metric_value", 0.0),
                "last_change": p.get("last_updated"),
            }
        )

    payload = {
        "generated_at": dt.date.today().isoformat(),
        "experiments": experiments,
    }
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2))
    print(f"Experiments generated at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
