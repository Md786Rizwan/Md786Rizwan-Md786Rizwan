# Md786Rizwan — GitHub Enhancement Starter (Futuristic + Auto-Updating)

This package is customized for your profile and five flagship repositories.

## Repositories wired in this starter
1. Laptop_Price_Predictor_Using_ML
2. Phising_Site
3. Kidney_Disease_Classification_Project
4. Exploratory-data-Analysis
5. Educational-chatbot

## What was prepared
- `profile_dashboard/README.template.md` (futuristic profile layout)
- `profile_dashboard/projects.json` (your project registry)
- `profile_dashboard/scripts/metrics.py` (KPI and scoring)
- `profile_dashboard/scripts/render_readme.py` (dashboard generator)
- `profile_dashboard/.github/workflows/dashboard.yml` (daily auto-update)

## First actions for you
1. Copy `profile_dashboard/README.generated.md` into your GitHub profile repo (`Md786Rizwan/Md786Rizwan`) as `README.md`.
2. Push `.github/workflows/dashboard.yml` into the profile repo.
3. Ensure Actions are enabled and run workflow manually once.
4. Add your LinkedIn URL in README.
5. Update `projects.json` weekly with `last_updated` + `next_action`.

## Local run
```bash
python profile_dashboard/scripts/metrics.py
python profile_dashboard/scripts/render_readme.py
```

Then open `profile_dashboard/README.generated.md`.
