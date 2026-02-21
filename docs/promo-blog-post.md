# How We Gate LLM Changes in CI

You change an LLM model. Or tweak a prompt. The output looks fine. Then you ship it—and cost jumps 38%, a phone number slips into the response, or the JSON breaks your downstream parser. No unit test caught it. Manual review didn't scale. You're left firefighting in production.

This is the gap BreakPoint fills.

## The Problem

Unit tests assume deterministic behavior. LLM output is not. When you swap models or adjust prompts, subtle regressions slip through: cost spikes, PII leaks, format drift. Traditional CI doesn't know how to gate "is this candidate output acceptable compared to the baseline?"

You need a deterministic decision: compare the candidate output to a known-good baseline, evaluate cost, PII, and semantic drift, and block risky changes before merge.

## Introducing BreakPoint

BreakPoint is a local-first decision engine that compares baseline vs. candidate LLM output and returns one of three outcomes: **ALLOW**, **WARN**, or **BLOCK**. It runs entirely locally—no SaaS, no API keys. Policy evaluation is deterministic from your saved artifacts.

**Lite mode** (default) is zero-config. Out of the box it checks:

- **Cost:** WARN at +20%, BLOCK at +40%
- **PII:** BLOCK on first detection (email, phone, credit card, SSN)
- **Drift:** WARN at +35%, BLOCK at +70% (semantic similarity)
- **Empty output:** Always BLOCK

Stable exit codes make it CI-friendly: `0` = ALLOW, `1` = WARN, `2` = BLOCK.

## Quick Example

```bash
pip install breakpoint-ai
breakpoint evaluate baseline.json candidate.json
```

Example output:

```
STATUS: BLOCK

Reasons:
- Cost increased by 38% (baseline: 1,000 tokens -> candidate: 1,380)
- Detected US phone number pattern
```

That's it. One command, one clear decision.

## CI Integration

Add BreakPoint to your PR workflow with the GitHub Action:

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

      - name: Generate candidate
        run: # ... produce candidate.json from your model

      - name: BreakPoint Evaluate
        uses: cholmess/breakpoint-ai@v1
        with:
          baseline: baseline.json
          candidate: candidate.json
          fail_on: warn
```

With `fail_on: warn`, any WARN or BLOCK fails the workflow. Your PR is blocked until you fix the regression or explicitly adjust the baseline.

## Real-World Scenarios

BreakPoint catches cases that slip through the cracks:

1. **Cost regression after model swap** — Output looks equivalent, but token count spikes. Policy blocks before deploy.

2. **Structured output format regression** — The candidate drops expected JSON structure or drifts too far from baseline behavior. Blocked.

3. **PII in candidate output** — Email, phone, or credit card appears. Immediate BLOCK.

4. **Small prompt change → big cost blowup** — A tweak plus a model upgrade creates large cost and latency increases with output-contract drift. Caught before merge.

## Ship with Confidence

BreakPoint is open source, MIT licensed, and runs locally. No telemetry. No cloud dependency. Your baselines stay in your repo. The decision is deterministic and auditable.

Try it in 60 seconds:

```bash
pip install breakpoint-ai
make demo
```

Or explore the examples in the [repo](https://github.com/cholmess/breakpoint-ai).

---

**Links**

- [GitHub](https://github.com/cholmess/breakpoint-ai)
- [PyPI](https://pypi.org/project/breakpoint-ai/)
- [GitHub Action](https://github.com/marketplace/actions/breakpoint-evaluate)
