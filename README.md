# BreakPoint Library

Local-first policy engine to compare baseline vs candidate LLM outputs and return `ALLOW`, `WARN`, or `BLOCK`.

## Quickstart

```bash
pip install -e .
breakpoint evaluate baseline.json candidate.json
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
