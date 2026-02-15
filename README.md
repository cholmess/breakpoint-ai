# BreakPoint Library

You change a model.
Output looks fine at a glance.
Cost is suddenly +38%.
A phone number slips into a response.
BreakPoint catches it before deploy.

BreakPoint is a local-first, deterministic pre-deploy gate for LLM changes with verdicts: `ALLOW`, `WARN`, `BLOCK`.

## CI First (Recommended)

```bash
breakpoint evaluate baseline.json candidate.json --json --fail-on warn
```

Why this is the default integration path:
- Machine-readable decision payload (`schema_version`, `status`, `reason_codes`, metrics).
- Non-zero exit code on risky changes.
- Easy to wire into existing CI without additional services.

## Try In 60 Seconds

```bash
pip install -e .
make demo
```

What you should see:
- Scenario A: `BLOCK` (cost spike)
- Scenario B: `BLOCK` (format/contract regression)
- Scenario C: `BLOCK` (PII + verbosity drift)
- Scenario D: `BLOCK` (cost/latency/verbosity tradeoff)

## Three Realistic Examples

Baseline for all examples:
- `examples/install_worthy/baseline.json`

### 1) Cost regression after model swap

```bash
breakpoint evaluate examples/install_worthy/baseline.json examples/install_worthy/candidate_cost_model_swap.json
```

Expected: `BLOCK`
Why it matters: output appears equivalent, but cost increases enough to violate policy.

### 2) Structured-output behavior regression

```bash
breakpoint evaluate examples/install_worthy/baseline.json examples/install_worthy/candidate_format_regression.json
```

Expected: `BLOCK`
Why it matters: candidate drops expected structure and drifts from baseline behavior.

### 3) PII appears in candidate output

```bash
breakpoint evaluate examples/install_worthy/baseline.json examples/install_worthy/candidate_pii_verbosity.json
```

Expected: `BLOCK`
Why it matters: candidate introduces PII and adds verbosity drift.

More scenario details:
- `docs/install-worthy-examples.md`

## CLI

Evaluate two JSON files:

```bash
breakpoint evaluate baseline.json candidate.json
```

Evaluate a single combined JSON file:

```bash
breakpoint evaluate payload.json
```

JSON output for CI/parsing:

```bash
breakpoint evaluate baseline.json candidate.json --json
```

Exit-code gating options:

```bash
# fail on WARN or BLOCK
breakpoint evaluate baseline.json candidate.json --fail-on warn

# fail only on BLOCK
breakpoint evaluate baseline.json candidate.json --fail-on block
```

Stable exit codes:
- `0` = `ALLOW`
- `1` = `WARN`
- `2` = `BLOCK`

Waivers (suppressions):

```bash
breakpoint evaluate baseline.json candidate.json --config policy.json --now 2026-02-15T00:00:00Z --json
```

Config inspection:

```bash
breakpoint config print
breakpoint config print --config custom_policy.json
breakpoint config print --config custom_policy.json --env dev
```

## Input Schema

Each input JSON is an object with at least:
- `output` (string)

Optional fields used by policies:
- `cost_usd` (number)
- `model` (string)
- `tokens_total` (number)
- `tokens_in` / `tokens_out` (number)
- `latency_ms` (number)

Combined input format:

```json
{
  "baseline": { "output": "..." },
  "candidate": { "output": "..." }
}
```

## Python API

```python
from breakpoint import evaluate

decision = evaluate(
    baseline_output="hello",
    candidate_output="hello there",
    metadata={"baseline_tokens": 100, "candidate_tokens": 140},
)
print(decision.status)
print(decision.reasons)
```

## Additional Docs

- `docs/quickstart-10min.md`
- `docs/install-worthy-examples.md`
- `docs/baseline-lifecycle.md`
- `docs/ci-templates.md`
- `docs/value-metrics.md`
- `docs/policy-presets.md`
- `docs/release-gate-audit.md`
