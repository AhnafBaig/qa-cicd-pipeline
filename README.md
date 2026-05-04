# ⚙️ QA CI/CD Pipeline

A production-grade, multi-stage CI/CD test automation pipeline demonstrating smoke testing, full regression, PR gate enforcement, and parallel execution — configured for both **GitHub Actions** and **Azure DevOps Pipelines**.

[![Smoke Tests](https://github.com/YOUR_USERNAME/qa-cicd-pipeline/actions/workflows/smoke.yml/badge.svg)](https://github.com/YOUR_USERNAME/qa-cicd-pipeline/actions/workflows/smoke.yml)
[![Regression Suite](https://github.com/YOUR_USERNAME/qa-cicd-pipeline/actions/workflows/regression.yml/badge.svg)](https://github.com/YOUR_USERNAME/qa-cicd-pipeline/actions/workflows/regression.yml)
[![PR Gate](https://github.com/YOUR_USERNAME/qa-cicd-pipeline/actions/workflows/pr-gate.yml/badge.svg)](https://github.com/YOUR_USERNAME/qa-cicd-pipeline/actions/workflows/pr-gate.yml)

---

## 🏗️ Project Structure

```
qa-cicd-pipeline/
│
├── .github/workflows/
│   ├── smoke.yml           # Runs on every push — cross-platform (Ubuntu + Windows)
│   ├── regression.yml      # Nightly full suite — staged: API → UI → summary
│   └── pr-gate.yml         # Blocks PRs merging unless @critical tests pass
│
├── azure-pipelines.yml     # Azure DevOps equivalent — Smoke → API → UI stages
│
├── features/               # Gherkin BDD feature files
│   ├── login.feature       # @smoke + @regression + @critical tags
│   ├── cart.feature        # @smoke + @regression tags
│   └── api/
│       └── posts_api.feature
│
├── pages/                  # Page Object Model (POM) classes
├── steps/                  # BDD step definitions (ui/ and api/)
│
├── tests/
│   ├── smoke/              # Fast smoke suite — run on every push (~30s)
│   ├── ui/                 # Full UI regression
│   └── api/                # Full API regression
│
├── utils/
│   ├── config.py           # Centralised config + env vars
│   ├── api_client.py       # Reusable HTTP client with logging
│   └── logger.py           # Coloured console logger
│
├── scripts/
│   └── run_pipeline_local.sh  # Simulate full CI pipeline locally
│
├── Dockerfile              # Self-contained test runner image
├── Makefile                # Developer shortcuts (make smoke, make regression...)
├── conftest.py             # Playwright fixtures + step registration
├── pytest.ini              # pytest config with custom markers
└── requirements.txt
```

---

## 🔁 Pipeline Architecture

### GitHub Actions — 3 workflows

```
Every Push / PR
      │
      ▼
┌─────────────────────────────────────┐
│  🚦 smoke.yml                       │
│  Ubuntu + Windows (parallel matrix) │
│  ~30 seconds                        │
└──────────────┬──────────────────────┘
               │ (smoke passes)
               ▼
┌─────────────────────────────────────┐
│  🔒 pr-gate.yml (PRs to main only)  │
│  Runs @critical tests only          │
│  Blocks merge if any fail           │
└─────────────────────────────────────┘

Every Night (2 AM UTC) / Manual dispatch
      │
      ▼
┌─────────────────────────────────────┐
│  🔁 regression.yml                  │
│  Stage 1: 🌐 API (parallel, fast)  │
│  Stage 2: 🖥️ UI (depends on API)   │
│  Stage 3: 📊 Summary to job log     │
└─────────────────────────────────────┘
```

### Azure DevOps — azure-pipelines.yml

```
Trigger: push + PR + nightly cron
      │
      ▼
  🚦 Smoke  →  🌐 API Regression  →  🖥️ UI Regression
```

Each stage publishes an HTML report as a build artifact.

---

## ⚙️ Tech Stack

| Concern         | Tool                     |
|-----------------|--------------------------|
| Language        | Python 3.12              |
| UI Automation   | Playwright               |
| BDD Framework   | pytest-bdd + Gherkin     |
| API Testing     | Requests + custom client |
| Test Runner     | pytest + pytest-xdist    |
| Reports         | pytest-html              |
| CI/CD #1        | GitHub Actions           |
| CI/CD #2        | Azure DevOps Pipelines   |
| Containerisation| Docker                   |
| Dev shortcuts   | Makefile                 |

---

## 🚀 Quick Start (Local)

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/qa-cicd-pipeline.git
cd qa-cicd-pipeline

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# 3. Install
make install
make browsers

# 4. Run
make smoke            # Fast smoke tests
make regression       # Full API + UI regression
make critical         # PR gate tests only
```

---

## 🐳 Docker

```bash
# Build the image
make docker-build

# Run smoke tests in container (no local Python needed)
make docker-smoke

# Run full regression in container
make docker-regression
```

---

## 🏷️ Test Markers

Tests are tagged so each pipeline stage runs only what it needs:

| Marker       | What it means                              | Used by               |
|--------------|--------------------------------------------|-----------------------|
| `@smoke`     | Fast, must-pass check the system is alive  | smoke.yml, every push |
| `@critical`  | Core flows that block a PR merge           | pr-gate.yml           |
| `@regression`| Extended coverage, runs nightly            | regression.yml        |
| `@ui`        | Requires a browser / Playwright            | UI stage only         |
| `@api`       | HTTP-only, no browser needed               | API stage (fast)      |

Run any marker locally:
```bash
pytest -m "smoke and ui" -v
pytest -m "critical" -v
pytest -m "regression and api" -v
```

---

## 📊 Reports & Artifacts

Every pipeline stage uploads an HTML report as a build artifact:

| Artifact name          | Retention | Contents                    |
|------------------------|-----------|-----------------------------|
| `smoke-report-ubuntu`  | 7 days    | Smoke run on Ubuntu         |
| `smoke-report-windows` | 7 days    | Smoke run on Windows        |
| `api-regression-report`| 30 days   | Full API test results       |
| `ui-regression-report` | 30 days   | Full UI test results        |
| `pr-gate-report`       | 14 days   | Critical test gate results  |
| `failure-screenshots`  | 7 days    | Screenshots on UI failure   |

---

## 🔐 Setting Up Secrets

**GitHub:**
`Repo → Settings → Secrets and variables → Actions → New repository secret`
- `STANDARD_USER` = `standard_user`
- `PASSWORD` = `secret_sauce`

**Azure DevOps:**
`Pipelines → Library → Variable Groups → Create group "qa-credentials"`
- Add `STANDARD_USER` and `PASSWORD` as secret variables
- Link the group to your pipeline under Variables tab

---

## 🔒 Enforcing the PR Gate (GitHub)

To make the PR gate mandatory:
1. Go to `Repo → Settings → Branches → Add rule`
2. Branch name pattern: `main`
3. Check **"Require status checks to pass before merging"**
4. Select `critical-gate` from the list

Now no PR can merge to `main` unless all `@critical` tests pass.

---

## 🌐 Azure DevOps Setup

1. Push this repo to an Azure DevOps project
2. Go to `Pipelines → New Pipeline`
3. Choose your repo → select **"Existing Azure Pipelines YAML file"**
4. Point to `/azure-pipelines.yml`
5. Add secret variables: `STANDARD_USER`, `PASSWORD`
6. Save and run
