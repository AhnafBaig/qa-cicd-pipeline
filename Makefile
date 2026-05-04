# ============================================================================
# QA CI/CD Pipeline — Makefile
# Mirrors what the CI pipelines do so devs get identical results locally.
# ============================================================================

.PHONY: help install browsers smoke regression-api regression-ui regression \
        critical clean report docker-build docker-smoke docker-regression

# Default target
help:
	@echo ""
	@echo "  QA CI/CD Pipeline — available commands"
	@echo "  ───────────────────────────────────────"
	@echo "  make install          Install Python dependencies"
	@echo "  make browsers         Install Playwright browsers"
	@echo "  make smoke            Run smoke tests (fast, ~30s)"
	@echo "  make regression-api   Run full API regression"
	@echo "  make regression-ui    Run full UI regression"
	@echo "  make regression       Run complete regression suite"
	@echo "  make critical         Run only @critical tests (PR gate)"
	@echo "  make report           Open the last HTML report in browser"
	@echo "  make clean            Delete generated reports and cache"
	@echo "  make docker-build     Build the Docker test image"
	@echo "  make docker-smoke     Run smoke tests in Docker"
	@echo "  make docker-regression Run full regression in Docker"
	@echo ""

# ── Setup ────────────────────────────────────────────────────────────────────
install:
	pip install -r requirements.txt

browsers:
	playwright install chromium

# ── Test targets ─────────────────────────────────────────────────────────────
smoke:
	pytest tests/smoke/ -v -m smoke \
		--html=reports/smoke.html --self-contained-html

regression-api:
	pytest tests/api/ -v \
		--html=reports/api-regression.html --self-contained-html \
		-n auto

regression-ui:
	pytest tests/ui/ -v \
		--html=reports/ui-regression.html --self-contained-html

regression:
	$(MAKE) regression-api
	$(MAKE) regression-ui

critical:
	pytest tests/ -v -m critical \
		--html=reports/pr-gate.html --self-contained-html

# ── Utilities ────────────────────────────────────────────────────────────────
report:
	@python -m webbrowser reports/smoke.html 2>/dev/null || \
	 python -m webbrowser reports/api-regression.html 2>/dev/null || \
	 echo "No report found. Run 'make smoke' or 'make regression' first."

clean:
	rm -rf reports/ screenshots/ .pytest_cache/ __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete

# ── Docker ───────────────────────────────────────────────────────────────────
docker-build:
	docker build -t qa-cicd-pipeline:latest .

docker-smoke:
	docker run --rm \
		-e HEADLESS=true \
		-e STANDARD_USER=standard_user \
		-e PASSWORD=secret_sauce \
		-v $(PWD)/reports:/app/reports \
		qa-cicd-pipeline:latest \
		pytest tests/smoke/ -v -m smoke \
			--html=reports/smoke-docker.html --self-contained-html

docker-regression:
	docker run --rm \
		-e HEADLESS=true \
		-e STANDARD_USER=standard_user \
		-e PASSWORD=secret_sauce \
		-v $(PWD)/reports:/app/reports \
		qa-cicd-pipeline:latest \
		pytest tests/ -v \
			--html=reports/regression-docker.html --self-contained-html
