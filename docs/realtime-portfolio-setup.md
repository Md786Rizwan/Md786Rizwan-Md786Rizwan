# Real-Time AI Portfolio Setup Guide

## 1) Required files
- `README.md`
- `.github/workflows/dashboard.yml`
- `requirements.txt`
- `profile_dashboard/projects.json`
- `profile_dashboard/scripts/metrics.py`
- `profile_dashboard/scripts/ai_intelligence.py`
- `profile_dashboard/scripts/forecast.py`
- `profile_dashboard/scripts/learning.py`
- `profile_dashboard/scripts/experiments.py`
- `profile_dashboard/scripts/render_readme.py`

## 2) GitHub settings
1. Repository → Settings → Actions → General
2. Workflow permissions → **Read and write permissions**
3. Save

## 3) Optional customization
- Edit `profile_dashboard/projects.json` weekly
- Edit `profile_dashboard/weekly_focus.json` for sprint objective

## 4) Local run (same as CI)
```bash
pip install -r requirements.txt
python profile_dashboard/scripts/metrics.py
python profile_dashboard/scripts/ai_intelligence.py
python profile_dashboard/scripts/forecast.py
python profile_dashboard/scripts/learning.py
python profile_dashboard/scripts/experiments.py
python profile_dashboard/scripts/render_readme.py
cp profile_dashboard/README.generated.md README.md
```

## 5) Automation behavior
- Workflow runs every **30 minutes** and on manual trigger.
- `README.md` is updated automatically with latest dashboard state.
