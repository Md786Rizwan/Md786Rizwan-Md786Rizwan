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
- `.github/workflows/profile-dashboard.yml` (daily auto-update)

## First actions for you
1. Copy `profile_dashboard/README.generated.md` into your GitHub profile repo (`Md786Rizwan/Md786Rizwan`) as `README.md`.
2. Push `.github/workflows/profile-dashboard.yml` into the profile repo.
3. Ensure Actions are enabled and run workflow manually once.
4. Add your LinkedIn URL in README.
5. Update `projects.json` weekly with `last_updated` + `next_action`.

## Correct Directory Structure (Important)
GitHub Actions only detects workflow files from this exact folder in the **repo root**:
`.github/workflows/`

Use this structure:

```text
Md786Rizwan/                <- profile repo root
├─ .github/
│  └─ workflows/
│     └─ profile-dashboard.yml
├─ README.md                <- your profile README
└─ profile_dashboard/
   ├─ projects.json
   ├─ generated/metrics.json
   └─ scripts/
      ├─ metrics.py
      └─ render_readme.py
```

## Local run
```bash
python profile_dashboard/scripts/metrics.py
python profile_dashboard/scripts/render_readme.py
```

Then open `profile_dashboard/README.generated.md`.

## ✅ Next (Do this now)
Since your commit is already pushed, continue in this order:

1. Open your **profile repository** (`Md786Rizwan/Md786Rizwan`).
2. Create folder: `.github/workflows/`.
3. Copy workflow file from this starter to profile repo:
   - source: `.github/workflows/profile-dashboard.yml`
   - destination: `.github/workflows/profile-dashboard.yml`
4. Copy `profile_dashboard/README.generated.md` content into profile repo `README.md`.
5. Commit and push.
6. Go to **GitHub → Actions → Update Profile Dashboard → Run workflow**.
7. Confirm the README updates after workflow run.

## 🧪 Quick Validation Checklist
- Actions tab shows `Update Profile Dashboard` workflow.
- Workflow status is green.
- README dashboard contains:
  - KPI badges
  - project command table
  - top 3 next actions
- Last auto-update date changes after each run.

## ❗ If you get `403 Permission denied to github-actions[bot]`
This is the most common first-time setup issue.

### Fix in GitHub Settings
1. Open your profile repo: `Md786Rizwan/Md786Rizwan`.
2. Go to **Settings → Actions → General**.
3. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
4. Save.
5. Re-run workflow from **Actions** tab.

### Why this happens
- Your workflow can generate files successfully.
- But `git push` fails if `GITHUB_TOKEN` is read-only.
- Error looks like: `Permission denied to github-actions[bot]` + `403`.

## 🔁 Weekly Maintenance (10 minutes)
- Update `profile_dashboard/projects.json` with fresh `last_updated` and `next_action`.
- Re-run workflow manually (or wait for daily cron).
- Share one LinkedIn weekly update from top project progress.

## 🌌 3D/Unique Dashboard Style (What is possible on GitHub)
GitHub README does not allow JavaScript, so true browser real-time 3D is not possible directly.

What we implemented instead:
- A generated **3D-style HUD SVG**: `profile_dashboard/generated/kpi_hud.svg`
- README embeds the SVG so it looks futuristic.
- Workflow refreshes every 3 hours (`cron: 0 */3 * * *`) to feel near-real-time.

For top 1% profile tuning (pinning strategy, KPI upgrades, recruiter positioning), see:
`docs/top1-profile-recommendations.md`
