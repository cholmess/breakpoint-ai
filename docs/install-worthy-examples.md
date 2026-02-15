# Install-Worthy Demo Scenarios

These examples are designed to make BreakPoint value obvious quickly.
All files live in `examples/install_worthy/`.

Baseline:

```bash
examples/install_worthy/baseline.json
```

Run all scenarios in one command:

```bash
make demo
```

## Scenario A: Cost regression from model swap

Command:

```bash
breakpoint evaluate examples/install_worthy/baseline.json examples/install_worthy/candidate_cost_model_swap.json
```

Expected status: `BLOCK`

Why this matters:
- Candidate output looks equivalent, but cost jumps enough to violate release policy.

## Scenario B: Structured-output format regression

Command:

```bash
breakpoint evaluate examples/install_worthy/baseline.json examples/install_worthy/candidate_format_regression.json
```

Expected status: `BLOCK`

Why this matters:
- Candidate output drops expected structure and shrinks too far from baseline behavior.

## Scenario C: PII + verbosity drift

Command:

```bash
breakpoint evaluate examples/install_worthy/baseline.json examples/install_worthy/candidate_pii_verbosity.json
```

Expected status: `BLOCK`

Why this matters:
- Candidate introduces direct PII (email/phone) while also drifting longer and noisier.

## Scenario D: Small prompt change -> big cost blowup

Command:

```bash
breakpoint evaluate examples/install_worthy/baseline.json examples/install_worthy/candidate_killer_tradeoff.json
```

Expected status: `BLOCK`

Why this matters:
- Candidate still looks acceptable to a quick reviewer, but a prompt-detail tweak plus model upgrade drives major cost/latency growth and output-contract drift.

## JSON mode for deterministic checks

```bash
breakpoint evaluate examples/install_worthy/baseline.json examples/install_worthy/candidate_killer_tradeoff.json --json
```

This exposes `status`, `reason_codes`, and `metrics` for CI or snapshot testing.
