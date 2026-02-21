#!/usr/bin/env bash
set -e

BASELINE="${INPUT_BASELINE:?baseline input required}"
CANDIDATE="${INPUT_CANDIDATE:?candidate input required}"
FAIL_ON="${INPUT_FAIL_ON:-warn}"
MODE="${INPUT_MODE:-lite}"
EXTRA_ARGS="${INPUT_EXTRA_ARGS:-}"

ARGS=("$BASELINE" "$CANDIDATE" "--mode" "$MODE" "--json")
if [[ "$FAIL_ON" != "allow" ]]; then
  ARGS+=("--fail-on" "$FAIL_ON")
fi
if [[ -n "$EXTRA_ARGS" ]]; then
  for w in $EXTRA_ARGS; do ARGS+=("$w"); done
fi

echo "::group::BreakPoint Evaluate"
echo "breakpoint evaluate ${ARGS[*]}"
echo "::endgroup::"

exec breakpoint evaluate "${ARGS[@]}"
