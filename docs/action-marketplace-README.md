# BreakPoint Evaluate

**AI output evaluation & LLM baseline comparison.** Compare candidate vs baseline model outputs, detect cost spikes, PII leaks, and format drift—then block bad AI releases in CI before production.

## Description

BreakPoint evaluates AI/LLM outputs against a baseline and returns `ALLOW`, `WARN`, or `BLOCK`. Use this action to gate pull requests: fail the workflow when your candidate output violates cost, PII, drift, or output-contract policies.

**Use cases:**
- Pre-merge quality gate for model or prompt changes
- Detect cost regression when swapping models
- Block PII (email, phone, credit card, SSN) in candidate output
- Enforce output format/schema consistency (Full mode)
- Catch latency increases (Full mode)

**Lite mode (default):** Cost, PII, and drift—zero config.  
**Full mode:** Output contract, latency, red team, presets, custom config.

## Usage

```yaml
- name: Checkout
  uses: actions/checkout@v4

- name: BreakPoint Evaluate
  uses: cholmess/breakpoint-ai@v1
  with:
    baseline: baseline.json
    candidate: candidate.json
    fail_on: warn
    mode: lite
```

### Pre-merge gate

```yaml
name: BreakPoint Gate

on:
  pull_request:
    branches: [main]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build candidate
        run: # ... generate candidate.json from your model

      - name: BreakPoint Evaluate
        uses: cholmess/breakpoint-ai@v1
        with:
          baseline: baseline.json
          candidate: candidate.json
          fail_on: warn
```

## Inputs

| Input       | Required | Default | Description |
|-------------|----------|---------|-------------|
| `baseline`  | Yes      | —       | Path to baseline JSON file |
| `candidate` | Yes      | —       | Path to candidate JSON file |
| `fail_on`   | No       | `warn`  | When to fail the workflow: `allow` (never), `warn` (on WARN or BLOCK), `block` (on BLOCK only) |
| `mode`      | No       | `lite`  | Evaluation mode: `lite` (cost, PII, drift) or `full` (adds output contract, latency, red team) |
| `extra_args`| No       | `''`    | Optional extra CLI args (e.g. `--strict --config policy.json`) |

## Output

The action runs `breakpoint evaluate` with `--json` and prints the decision to the job log. The workflow fails (non-zero exit) when the result matches `fail_on`.

## Requirements

- `ubuntu-latest` runner
- Python 3.11 (set by the action)
- `breakpoint-ai` installed via pip (done by the action)

---

*Keywords: AI evaluation, LLM evaluation, baseline comparison, AI quality gate, cost regression, PII detection, output drift, CI gate*
