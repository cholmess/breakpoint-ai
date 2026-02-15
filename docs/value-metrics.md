# Value Metrics (P1-2)

BreakPoint is most useful when you can quantify outcomes, not just usage.

## What to Track

Core pipeline metrics:

- `warn_rate`: WARN / total
- `block_rate`: BLOCK / total
- `top_reason_codes`: which rules fire most often
- `waiver_rate`: waivers applied / total

Outcome metrics (requires human/system feedback):

- `false_positive_rate`: fraction of WARN/BLOCK later judged safe
- `true_positive_rate`: fraction of BLOCK that prevented a bad deploy

## Store Decision Artifacts

In CI, always save the decision JSON artifact (example: `breakpoint-decision.json`).

GitHub Actions template:
- `examples/ci/github-actions-breakpoint.yml`

## Summarize Metrics Locally or In CI

Summarize one file:

```bash
breakpoint metrics summarize breakpoint-decision.json
```

Summarize a directory (recursive scan of `*.json`):

```bash
breakpoint metrics summarize . --json
```

Notes:

- Summary reads BreakPoint decision JSON (contract fields `schema_version`, `status`, `reasons`, `reason_codes`).
- If `metadata.waivers_applied` exists, it is counted as waiver usage.

## Joining To Feedback (Optional)

For outcome metrics like false-positive rate, you need a stable join key.

BreakPoint decisions can be joined by:

- the build/run identifier you store alongside the artifact, or
- a stable hash of the decision JSON (future: first-class feedback format).
