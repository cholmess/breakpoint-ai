#!/usr/bin/env sh
set -eu

# Inputs:
#  - BREAKPOINT_BASELINE (default: examples/quickstart/baseline.json)
#  - BREAKPOINT_CANDIDATE (default: examples/quickstart/candidate_warn.json)
#  - BREAKPOINT_FAIL_ON (default: warn)
BASELINE_PATH="${BREAKPOINT_BASELINE:-examples/quickstart/baseline.json}"
CANDIDATE_PATH="${BREAKPOINT_CANDIDATE:-examples/quickstart/candidate_warn.json}"
FAIL_ON="${BREAKPOINT_FAIL_ON:-warn}"
OUTPUT_PATH="${BREAKPOINT_OUTPUT:-breakpoint-decision.json}"

pip install . >/dev/null
breakpoint evaluate "$BASELINE_PATH" "$CANDIDATE_PATH" --json --fail-on "$FAIL_ON" > "$OUTPUT_PATH"

echo "Decision written to $OUTPUT_PATH"
