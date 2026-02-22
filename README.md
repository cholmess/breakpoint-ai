# BreakPoint AI

[![PyPI version](https://img.shields.io/pypi/v/breakpoint-ai.svg)](https://pypi.org/project/breakpoint-ai/)
[![Tests](https://github.com/cholmess/breakpoint-ai/actions/workflows/test.yml/badge.svg)](https://github.com/cholmess/breakpoint-ai/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**BreakPoint blocks risky LLM changes before they ship.**

**Problem:** You change a prompt or swap a model. Output looks fine. But cost jumps 38%, a phone number slips in, or the format breaks your parser. You ship it. Users and budgets get hurt.

**Who it's for:** Teams shipping LLM features to production, merging prompt or model changes via PR, or running cost-sensitive systems.

**When to use it:** Before every deploy. Gate PRs. Catch regressions before they reach users.

**If you don't:** Cost drift, PII leaks, and format regressions ship unnoticed. Unit tests won't catch these—LLM output isn't deterministic.

---

## 3-Step Mental Model

```
Step 1: Capture baseline   →  Approved output artifact (store in repo)
Step 2: Generate candidate →  New output from your changed prompt/model
Step 3: Gate in CI         →  breakpoint evaluate baseline.json candidate.json
```

```
Baseline  ──→  Candidate  ──→  BreakPoint  ──→  ALLOW / WARN / BLOCK  ──→  CI
```

---

## Lite Mode (Zero Config)

Out of the box, no config needed:

- **Cost:** WARN at +20%, BLOCK at +40%
- **PII:** BLOCK on email, phone, credit card (Luhn), SSN
- **Drift:** WARN at +35% length delta, BLOCK at +70%, BLOCK on empty output

Exit codes: `0` = ALLOW, `1` = WARN, `2` = BLOCK.

Advanced (config, presets, waivers): `--mode full` → `docs/user-guide-full-mode.md`.

---

## 60-Second Quickstart

```bash
pip install breakpoint-ai
breakpoint evaluate baseline.json candidate.json
```

Each JSON needs `output` (string). Optional: `cost_usd`, `tokens_in`, `tokens_out`, `model`, `latency_ms`.

Example BLOCK:

```
  Final Decision: BLOCK

  • Cost increased by 68.9% ($0.0450 → $0.0760), exceeding 40% block threshold.
  • PII: US phone number pattern detected.

  Exit: 2
```

---

## Baseline: Treat LLM Output Like a Code Artifact

Baselines are approved snapshots. You commit them. You diff against them. When a change is **intentional** and you've reviewed it, promote the candidate to baseline:

```bash
breakpoint accept baseline.json candidate.json
```

CI flow: **Fails** → Human reviews → **Accept baseline** (or fix) → Merge.

---

## CI Integration

Run the gate directly—no marketplace action required:

```bash
breakpoint evaluate baseline.json candidate.json --fail-on warn
```

`--fail-on warn` fails CI on WARN or BLOCK. Use `--fail-on block` to fail only on BLOCK.

Minimal GitHub Actions:

```yaml
- uses: actions/checkout@v4
- name: Generate candidate
  run: # ... produce candidate.json
- name: BreakPoint Gate
  run: breakpoint evaluate baseline.json candidate.json --fail-on warn
```

Or use the [BreakPoint Evaluate action](https://github.com/marketplace/actions/breakpoint-evaluate).

---

## Why Not Just Unit Tests?

Unit tests assume deterministic behavior. LLM output is not. BreakPoint catches what tests miss:

- Cost drift (same output, higher token bill)
- Subtle regressions (format change, dropped keys)
- PII leaks (phone, email, credit card)

---

## Real Story

"We swapped GPT-4 to GPT-4.1. Output looked identical. Cost rose 38%. BreakPoint blocked it before deploy."

---

## Try in 60 Seconds – FastAPI Demo

![BreakPoint catching cost regression in FastAPI LLM demo](docs/demo-fastapi.gif)

```bash
git clone https://github.com/cholmess/breakpoint-ai
cd breakpoint-ai/examples/fastapi-llm-demo
make install
make good        # PASS
make bad-tokens  # BLOCK
```

---

## When To Use / When Not

**Use:** Production LLM features, PR merges, cost-sensitive systems.

**Skip:** One-off experiments, hobby scripts, non-production.

---

## Why Local-First?

Most tools send prompts and outputs to SaaS. BreakPoint runs on your machine. Artifacts stay in your repo. No network calls for evaluation.

---

## Four Examples

```bash
breakpoint evaluate examples/install_worthy/baseline.json examples/install_worthy/candidate_cost_model_swap.json
breakpoint evaluate examples/install_worthy/baseline.json examples/install_worthy/candidate_format_regression.json
breakpoint evaluate examples/install_worthy/baseline.json examples/install_worthy/candidate_pii_verbosity.json
breakpoint evaluate examples/install_worthy/baseline.json examples/install_worthy/candidate_killer_tradeoff.json
```

Details: `docs/install-worthy-examples.md`.

---

## CLI

```bash
breakpoint evaluate baseline.json candidate.json
breakpoint evaluate payload.json                    # combined {baseline, candidate}
breakpoint accept baseline.json candidate.json     # promote candidate to baseline
breakpoint evaluate ... --verbose                   # full policy output
breakpoint evaluate ... --json --fail-on warn       # CI-friendly
```

---

## Input Schema

`output` (string) required. Optional: `cost_usd`, `tokens_in`, `tokens_out`, `model`, `latency_ms`. Combined: `{"baseline": {...}, "candidate": {...}}`.

---

## Pytest Plugin

```python
def test_my_agent(breakpoint):
    response = call_my_llm("Hello")
    breakpoint.assert_stable(response, candidate_metadata={"cost_usd": 0.002})
```

Update baselines: `BREAKPOINT_UPDATE_BASELINES=1 pytest`.

---

## Python API

```python
from breakpoint import evaluate

decision = evaluate(
    baseline_output="hello",
    candidate_output="hello there",
    metadata={"baseline_tokens": 100, "candidate_tokens": 140},
)
print(decision.status, decision.reasons)
```

---

## Troubleshooting

- `ModuleNotFoundError: breakpoint` → `pip install breakpoint-ai`
- File not found → Check paths.
- JSON validation → Ensure `output` (string) in each object.

---

## Docs

- `docs/user-guide.md`
- `docs/user-guide-full-mode.md`
- `docs/quickstart-10min.md`
- `docs/install-worthy-examples.md`
- `docs/baseline-lifecycle.md`
- `docs/ci-templates.md`

---

## Maintainer

BreakPoint is maintained by Christopher Holmes Silva.

- X: [https://x.com/cholmess](https://x.com/cholmess)
- LinkedIn: [https://linkedin.com/in/cholmess](https://linkedin.com/in/cholmess)

Feedback and real-world usage stories welcome—[open an issue](https://github.com/cholmess/breakpoint-ai/issues) or [c.holmes.silva@gmail.com](mailto:c.holmes.silva@gmail.com).
