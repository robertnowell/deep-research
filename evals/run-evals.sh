#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/results"
VALIDATOR="${SCRIPT_DIR}/validate.py"
TEST_CASES="${SCRIPT_DIR}/test-cases.json"
FIXTURES_DIR="${SCRIPT_DIR}/fixtures"

mkdir -p "${RESULTS_DIR}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

pass_count=0
fail_count=0
skip_count=0

print_result() {
    local status="$1" name="$2" detail="${3:-}"
    case "$status" in
        PASS) echo -e "  ${GREEN}PASS${NC}  ${name} ${detail}" ; pass_count=$((pass_count + 1)) ;;
        FAIL) echo -e "  ${RED}FAIL${NC}  ${name} ${detail}" ; fail_count=$((fail_count + 1)) ;;
        SKIP) echo -e "  ${YELLOW}SKIP${NC}  ${name} ${detail}" ; skip_count=$((skip_count + 1)) ;;
    esac
}

# --- Fixtures-only mode ---
run_fixtures() {
    echo "=== Fixture Validation ==="
    echo ""

    # Valid fixtures — should all pass
    for scope in quick standard thorough; do
        fixture="${FIXTURES_DIR}/valid-${scope}.md"
        if [ -f "$fixture" ]; then
            if python3 "$VALIDATOR" "$fixture" --scope "$scope" > /dev/null 2>&1; then
                print_result "PASS" "valid-${scope}.md"
            else
                print_result "FAIL" "valid-${scope}.md" "— expected all checks to pass"
            fi
        fi
    done

    # Invalid fixtures — should fail specific checks
    check_fixture_fails() {
        local fixture_name="$1" expected="$2" scope="${3:-standard}"
        local fixture="${FIXTURES_DIR}/${fixture_name}"
        if [ -f "$fixture" ]; then
            local output
            output=$(python3 "$VALIDATOR" "$fixture" --scope "$scope" --json 2>/dev/null || true)
            if echo "$output" | python3 -c "
import sys, json
data = json.load(sys.stdin)
failed = [r['name'] for r in data['results'] if r['status'] == 'FAIL']
sys.exit(0 if '${expected}' in failed else 1)
" 2>/dev/null; then
                print_result "PASS" "${fixture_name}" "— correctly detected ${expected} failure"
            else
                print_result "FAIL" "${fixture_name}" "— expected ${expected} to fail"
            fi
        fi
    }

    check_fixture_fails "missing-tiers.md" "tier_annotations" "quick"
    check_fixture_fails "missing-answer.md" "answer_status" "quick"
    check_fixture_fails "low-quality.md" "source_quality_caveat" "standard"

    echo ""
}

# --- Live test mode ---
run_live_test() {
    local name="$1" query="$2" scope="$3" assertions="$4"
    local output_file="${RESULTS_DIR}/${name}.md"

    echo "  Running: ${name} ..."
    echo "  Query: ${query}"

    # Run claude in prompt mode and capture output
    if ! claude -p "${query}" > "${output_file}" 2>/dev/null; then
        print_result "FAIL" "${name}" "— claude command failed"
        return
    fi

    # Structural validation
    local wants_structural
    wants_structural=$(echo "$assertions" | python3 -c "import sys,json; print(json.load(sys.stdin).get('structural', True))")

    if [ "$wants_structural" = "True" ]; then
        if python3 "$VALIDATOR" "$output_file" --scope "$scope" > /dev/null 2>&1; then
            print_result "PASS" "${name}/structural"
        else
            print_result "FAIL" "${name}/structural"
            python3 "$VALIDATOR" "$output_file" --scope "$scope" 2>/dev/null || true
        fi
    else
        print_result "SKIP" "${name}/structural" "— not required for this test"
    fi

    # Content assertions
    local contains
    contains=$(echo "$assertions" | python3 -c "
import sys, json
a = json.load(sys.stdin)
for item in a.get('contains', []):
    print(item)
" 2>/dev/null)

    if [ -n "$contains" ]; then
        while IFS= read -r expected; do
            if grep -qi "$expected" "$output_file" 2>/dev/null; then
                print_result "PASS" "${name}/contains '${expected}'"
            else
                print_result "FAIL" "${name}/contains '${expected}'"
            fi
        done <<< "$contains"
    fi

    # Min findings
    local min_findings
    min_findings=$(echo "$assertions" | python3 -c "import sys,json; print(json.load(sys.stdin).get('min_findings', 0))" 2>/dev/null)
    if [ "$min_findings" -gt 0 ] 2>/dev/null; then
        local actual_findings
        actual_findings=$(grep -cE '^\d+\.\s+\*\*' "$output_file" 2>/dev/null || echo 0)
        if [ "$actual_findings" -ge "$min_findings" ]; then
            print_result "PASS" "${name}/min_findings (${actual_findings} >= ${min_findings})"
        else
            print_result "FAIL" "${name}/min_findings (${actual_findings} < ${min_findings})"
        fi
    fi

    echo ""
}

run_live_tests() {
    local filter="${1:-}"

    echo "=== Live Tests ==="
    echo ""

    python3 -c "
import json, sys
with open('${TEST_CASES}') as f:
    cases = json.load(f)
for c in cases:
    if not '${filter}' or c['name'] == '${filter}':
        print(c['name'])
        print(c['query'])
        print(c['scope'])
        print(json.dumps(c['assertions']))
        print('---')
" 2>/dev/null | while IFS= read -r name; do
        IFS= read -r query
        IFS= read -r scope
        IFS= read -r assertions
        IFS= read -r _separator
        run_live_test "$name" "$query" "$scope" "$assertions"
    done
}

# --- Main ---
usage() {
    echo "Usage: $0 [--fixtures-only | --live [test-name]]"
    echo ""
    echo "  --fixtures-only    Run validator against fixtures only (no API calls)"
    echo "  --live [name]      Run live tests via claude -p (expensive)"
    echo "  (no args)          Run fixtures only"
}

case "${1:-}" in
    --fixtures-only|"")
        run_fixtures
        ;;
    --live)
        run_fixtures
        run_live_tests "${2:-}"
        ;;
    --help|-h)
        usage
        ;;
    *)
        # Assume it's a test name
        run_live_tests "$1"
        ;;
esac

echo "=== Summary ==="
echo -e "  ${GREEN}${pass_count} passed${NC}, ${RED}${fail_count} failed${NC}, ${YELLOW}${skip_count} skipped${NC}"

[ "$fail_count" -eq 0 ]
