from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS_FILE = ROOT / "generated" / "metrics.json"
INTEL_FILE = ROOT / "generated" / "ai_intelligence.json"
OUTPUT_FILE = ROOT / "generated" / "learning.json"


def main() -> None:
    metrics = json.loads(METRICS_FILE.read_text())
    intel = json.loads(INTEL_FILE.read_text()) if INTEL_FILE.exists() else {"intelligence": []}

    recs = []
    for item in intel.get("intelligence", [])[:5]:
        mp = item.get("missing_parts", [])
        if mp:
            recs.append(f"Learn {mp[0]} for {item['name']}.")

    if metrics.get("kpis", {}).get("consistency_score", 0) < 60:
        recs.append("Practice consistency: commit to 3 focused coding sessions this week.")
    if metrics.get("kpis", {}).get("accuracy_score", 0) < 0.9:
        recs.append("Study model calibration, cross-validation, and hyperparameter tuning.")

    payload = {
        "generated_at": dt.date.today().isoformat(),
        "recommendations": recs[:8],
    }
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2))
    print(f"Learning recommendations generated at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
