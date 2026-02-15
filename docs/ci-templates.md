# CI Templates (P1)

BreakPoint includes two starter CI templates for pipeline gating:

- GitHub Actions: `examples/ci/github-actions-breakpoint.yml`
- Generic shell runner: `examples/ci/run-breakpoint-gate.sh`

## GitHub Actions

Copy `examples/ci/github-actions-breakpoint.yml` into:

`/.github/workflows/breakpoint-gate.yml`

Behavior:

- Installs BreakPoint
- Runs evaluation with `--json --fail-on warn`
- Uploads `breakpoint-decision.json` as a build artifact

Adjust paths and threshold as needed:

- Baseline/candidate input paths in the `breakpoint evaluate` step
- Gate policy with `--fail-on warn|block`

## Generic CI Shell

Use the script in any CI provider that can run shell commands:

```bash
./examples/ci/run-breakpoint-gate.sh
```

Optional environment variables:

- `BREAKPOINT_BASELINE` (default: `examples/quickstart/baseline.json`)
- `BREAKPOINT_CANDIDATE` (default: `examples/quickstart/candidate_warn.json`)
- `BREAKPOINT_FAIL_ON` (default: `warn`)
- `BREAKPOINT_OUTPUT` (default: `breakpoint-decision.json`)

Example with stricter policy:

```bash
BREAKPOINT_CANDIDATE=examples/quickstart/candidate_block.json \
BREAKPOINT_FAIL_ON=block \
./examples/ci/run-breakpoint-gate.sh
```

## Notes

- Exit behavior follows existing contract:
  - `ALLOW` => `0`
  - `WARN` => `1`
  - `BLOCK` => `2`
- If your pipeline requires explicit artifact retention, archive `breakpoint-decision.json`.
