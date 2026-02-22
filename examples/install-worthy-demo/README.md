# BreakPoint 30-Second Demo

This demo simulates a prompt/model change that introduces:

- **50% cost increase**
- A **leaked phone number**

## Run

```bash
pip install breakpoint-ai
cd examples/install-worthy-demo
./run.sh
```

## Expected result

BreakPoint returns **BLOCK** with:

- Cost exceeded threshold
- PII detected

## Note

This demo uses static artifacts to simulate model output. In production, these artifacts would be generated from your LLM calls in CI.
