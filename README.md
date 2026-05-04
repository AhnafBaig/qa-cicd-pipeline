# QA CI/CD Pipeline

A multi-stage CI/CD test automation pipeline configured for both **GitHub Actions** and **Azure DevOps**, with smoke testing, full regression, PR merge gating, and Docker support.

[![Smoke Tests](https://github.com/AhnafBaig/qa-cicd-pipeline/actions/workflows/smoke.yml/badge.svg)](https://github.com/AhnafBaig/qa-cicd-pipeline/actions/workflows/smoke.yml)
[![Regression Suite](https://github.com/AhnafBaig/qa-cicd-pipeline/actions/workflows/regression.yml/badge.svg)](https://github.com/AhnafBaig/qa-cicd-pipeline/actions/workflows/regression.yml)

---

## Structure

```
qa-cicd-pipeline/
├── .github/workflows/
│   ├── smoke.yml          # Runs on every push (Ubuntu + Windows)
│   ├── regression.yml     # Nightly full suite (API → UI → summary)
│   └── pr-gate.yml        # Blocks PRs unless @critical tests pass
├── azure-pipelines.yml    # Azure DevOps equivalent
├── features/              # Gherkin BDD feature files
├── pages/                 # Page Object Model classes
├── steps/                 # BDD step definitions
├── tests/
│   ├── smoke/             # Fast checks (~30s)
│   ├── ui/                # Full UI regression
│   └── api/               # Full API regression
├── Dockerfile             # Containerised test runner
└── Makefile               # Developer shortcuts
```

---

## Tech Stack

| Layer    | Tool                          |
|----------|-------------------------------|
| Language | Python 3.12                   |
| UI       | Playwright                    |
| BDD      | pytest-bdd + Gherkin          |
| API      | Requests                      |
| CI/CD    | GitHub Actions + Azure DevOps |
| Docker   | Containerised test runner     |

---

## Quick Start

```bash
git clone https://github.com/AhnafBaig/qa-cicd-pipeline.git
cd qa-cicd-pipeline

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

make install
make browsers
```

---

## ▶Running Tests

```bash
make smoke         # Fast smoke tests (~30s)
make regression    # Full API + UI suite
make critical      # PR gate tests only
make docker-smoke  # Run in Docker container
```

---

## Pipeline Triggers

| Trigger             | What runs                          |
|---------------------|------------------------------------|
| Every push          | Smoke (Ubuntu + Windows parallel)  |
| PR to main          | @critical tests gate merge         |
| Nightly (2 AM UTC)  | Full regression (API → UI)         |
| Manual dispatch     | Choose: all, ui, api, or smoke     |

Add secrets under **Repo → Settings → Secrets → Actions**: `STANDARD_USER`, `PASSWORD`

---

## Targets

| Layer | App |
|-------|-----|
| UI    | [SauceDemo](https://www.saucedemo.com) |
| API   | [JSONPlaceholder](https://jsonplaceholder.typicode.com) |
