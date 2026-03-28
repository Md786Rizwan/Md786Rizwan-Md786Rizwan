# Real-Time AI Portfolio Setup Guide (Start → Production)

## 1) Folder structure
```text
.github/workflows/profile-dashboard.yml
profile_dashboard/
  projects.json
  weekly_focus.json
  README.template.md
  README.generated.md
  scripts/
    activity_fetch.py
    news_fetch.py
    metrics.py
    ai_insights.py
    render_readme.py
  generated/
    activity.json
    news.json
    metrics.json
    ai_insights.json
    metrics_history.json
    kpi_hud.svg
    performance_trend.svg
    weekly_focus.svg
```

## 2) Required GitHub settings
1. Repo → Settings → Actions → General
2. Workflow permissions: **Read and write permissions**
3. Save

## 3) Optional secrets
- `NEWS_API_KEY` (for NewsAPI live feed)

## 4) Local run
```bash
python profile_dashboard/scripts/activity_fetch.py
python profile_dashboard/scripts/metrics.py
python profile_dashboard/scripts/news_fetch.py
python profile_dashboard/scripts/ai_insights.py
python profile_dashboard/scripts/render_readme.py
```

## 5) CI automation
Workflow runs every 30 minutes and on manual dispatch.
It updates `README.md` automatically from generated dashboard output.

## 6) What to edit weekly
- `profile_dashboard/projects.json`: project stage, metrics, next action
- `profile_dashboard/weekly_focus.json`: sprint objective and milestone
