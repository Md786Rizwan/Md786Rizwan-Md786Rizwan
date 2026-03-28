from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_FILE = ROOT / "projects.json"
OUTPUT_FILE = ROOT / "generated" / "activity.json"


def get_json(url: str, token: str = "") -> list | dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-dashboard-bot"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers)
    with urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    token = os.getenv("GH_TOKEN", "")
    owner = json.loads(PROJECTS_FILE.read_text()).get("owner", "Md786Rizwan")
    repos = [p["name"] for p in json.loads(PROJECTS_FILE.read_text()).get("projects", [])]

    try:
        events = get_json(f"https://api.github.com/users/{owner}/events/public", token)
    except Exception:
        events = []
    push_events = [e for e in events if e.get("type") == "PushEvent"]

    recent_commits = []
    for event in push_events[:8]:
        repo_name = (event.get("repo") or {}).get("name", "")
        for c in (event.get("payload") or {}).get("commits", [])[:2]:
            recent_commits.append(
                {
                    "repo": repo_name,
                    "message": c.get("message", ""),
                    "url": c.get("url", ""),
                }
            )

    active_repo_count = len({(event.get("repo") or {}).get("name", "") for event in push_events[:20] if (event.get("repo") or {}).get("name", "")})

    payload = {
        "generated_at": dt.datetime.utcnow().isoformat() + "Z",
        "owner": owner,
        "tracked_repos": repos,
        "recent_push_events": len(push_events[:20]),
        "active_repo_count": active_repo_count,
        "recent_commits": recent_commits[:8],
    }
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2))
    print(f"Activity generated at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
