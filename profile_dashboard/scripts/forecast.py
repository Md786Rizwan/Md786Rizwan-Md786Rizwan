from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS_FILE = ROOT / "generated" / "metrics.json"
OUTPUT_FILE = ROOT / "generated" / "forecast.json"


def forecast_days(stage: str, risk: str) -> int:
    base = {"idea": 45, "poc": 30, "mvp": 18, "prod": 7}.get(stage.lower(), 30)
    risk_factor = {"low": -4, "medium": 0, "high": 7}.get(risk.lower(), 0)
    return max(3, base + risk_factor)


def main() -> None:
    metrics = json.loads(METRICS_FILE.read_text())
    items = []
    for p in metrics.get("projects", []):
        days = forecast_days(p.get("stage", "poc"), p.get("risk", "medium"))
        eta = (dt.date.today() + dt.timedelta(days=days)).isoformat()
        items.append(
            {
                "name": p.get("name"),
                "risk": p.get("risk", "medium"),
                "eta_days": days,
                "eta_date": eta,
            }
        )

    payload = {"generated_at": dt.date.today().isoformat(), "forecast": items}
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2))
    print(f"Forecast generated at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
