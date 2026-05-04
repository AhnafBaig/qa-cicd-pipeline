#!/usr/bin/env bash
# ============================================================================
# run_pipeline_local.sh
# Simulates the full CI pipeline locally so you can catch issues before push.
# Usage: bash scripts/run_pipeline_local.sh [smoke|regression|all]
# ============================================================================

set -euo pipefail

SCOPE="${1:-smoke}"
REPORTS_DIR="reports"
PASS=0
FAIL=0

mkdir -p "$REPORTS_DIR"

green()  { echo -e "\033[0;32m$*\033[0m"; }
red()    { echo -e "\033[0;31m$*\033[0m"; }
yellow() { echo -e "\033[0;33m$*\033[0m"; }
header() { echo -e "\n\033[1;34m══════════════════════════════════════\033[0m"; \
           echo -e "\033[1;34m  $*\033[0m"; \
           echo -e "\033[1;34m══════════════════════════════════════\033[0m\n"; }

run_stage() {
  local name="$1"
  shift
  header "Stage: $name"
  if "$@"; then
    green "✅  $name PASSED"
    PASS=$((PASS + 1))
  else
    red "❌  $name FAILED"
    FAIL=$((FAIL + 1))
    # Don't abort — run all stages so you see the full picture
  fi
}

header "QA Pipeline — local simulation (scope: $SCOPE)"

case "$SCOPE" in
  smoke)
    run_stage "Smoke — API"  pytest tests/smoke/ -m "smoke and api" -v \
      --html="$REPORTS_DIR/local-smoke-api.html" --self-contained-html
    run_stage "Smoke — UI"   pytest tests/smoke/ -m "smoke and ui"  -v \
      --html="$REPORTS_DIR/local-smoke-ui.html"  --self-contained-html
    ;;

  regression)
    run_stage "API Regression" pytest tests/api/ -v -n auto \
      --html="$REPORTS_DIR/local-api.html" --self-contained-html
    run_stage "UI Regression"  pytest tests/ui/ -v \
      --html="$REPORTS_DIR/local-ui.html"  --self-contained-html
    ;;

  all)
    run_stage "Smoke"          pytest tests/smoke/ -v \
      --html="$REPORTS_DIR/local-smoke.html" --self-contained-html
    run_stage "API Regression" pytest tests/api/   -v -n auto \
      --html="$REPORTS_DIR/local-api.html"   --self-contained-html
    run_stage "UI Regression"  pytest tests/ui/    -v \
      --html="$REPORTS_DIR/local-ui.html"    --self-contained-html
    ;;

  *)
    red "Unknown scope '$SCOPE'. Use: smoke | regression | all"
    exit 1
    ;;
esac

header "Pipeline Complete"
green "Passed stages: $PASS"
[ "$FAIL" -gt 0 ] && red "Failed stages: $FAIL" || green "Failed stages: 0"
echo ""
yellow "Reports saved to ./$REPORTS_DIR/"
[ "$FAIL" -gt 0 ] && exit 1 || exit 0
