from breakpoint.engine.policies.base import PolicyResult

_EPSILON = 1e-9


def evaluate_cost_policy(
    baseline: dict, candidate: dict, thresholds: dict, pricing: dict
) -> PolicyResult:
    baseline_cost = _resolve_cost(baseline, pricing)
    candidate_cost = _resolve_cost(candidate, pricing)

    if baseline_cost is None or candidate_cost is None:
        return PolicyResult(
            policy="cost",
            status="WARN",
            reasons=["Insufficient cost data; unable to compute full cost delta."],
            codes=["COST_WARN_MISSING_DATA"],
        )

    min_baseline_cost = float(thresholds.get("min_baseline_cost_usd", 0.01))
    if baseline_cost < min_baseline_cost:
        return PolicyResult(
            policy="cost",
            status="WARN",
            reasons=[
                f"Baseline cost ${baseline_cost:.4f} is below minimum ${min_baseline_cost:.4f}; percent delta is unreliable."
            ],
            codes=["COST_WARN_LOW_BASELINE"],
            details={"baseline_cost_usd": baseline_cost, "min_baseline_cost_usd": min_baseline_cost},
        )

    delta_usd = candidate_cost - baseline_cost
    increase_pct = ((candidate_cost - baseline_cost) / baseline_cost) * 100
    block_threshold = float(thresholds.get("block_increase_pct", 35))
    warn_threshold = float(thresholds.get("warn_increase_pct", 20))
    warn_delta_usd = float(thresholds.get("warn_delta_usd", 0.0))
    block_delta_usd = float(thresholds.get("block_delta_usd", 0.0))

    if (block_delta_usd > 0 and _meets_or_exceeds(delta_usd, block_delta_usd)) or _meets_or_exceeds(
        increase_pct, block_threshold
    ):
        reason = _format_cost_reason(
            increase_pct, baseline_cost, candidate_cost, baseline, candidate, block_threshold, "block"
        )
        return PolicyResult(
            policy="cost",
            status="BLOCK",
            reasons=[reason],
            codes=["COST_BLOCK_INCREASE"],
            details={"increase_pct": increase_pct, "delta_usd": delta_usd},
        )
    if (warn_delta_usd > 0 and _meets_or_exceeds(delta_usd, warn_delta_usd)) or _meets_or_exceeds(
        increase_pct, warn_threshold
    ):
        reason = _format_cost_reason(
            increase_pct, baseline_cost, candidate_cost, baseline, candidate, warn_threshold, "warn"
        )
        return PolicyResult(
            policy="cost",
            status="WARN",
            reasons=[reason],
            codes=["COST_WARN_INCREASE"],
            details={"increase_pct": increase_pct, "delta_usd": delta_usd},
        )
    return PolicyResult(policy="cost", status="ALLOW")


def _resolve_cost(record: dict, pricing: dict) -> float | None:
    direct_cost = record.get("cost_usd")
    if isinstance(direct_cost, (int, float)):
        return float(direct_cost)

    model_name = record.get("model")
    model_pricing = pricing.get(model_name, {}) if isinstance(model_name, str) else {}

    tokens_in = record.get("tokens_in")
    tokens_out = record.get("tokens_out")
    tokens_total = record.get("tokens_total")

    if isinstance(tokens_in, (int, float)) and isinstance(tokens_out, (int, float)):
        input_per_1k = model_pricing.get("input_per_1k")
        output_per_1k = model_pricing.get("output_per_1k")
        if isinstance(input_per_1k, (int, float)) and isinstance(output_per_1k, (int, float)):
            return (float(tokens_in) / 1000 * float(input_per_1k)) + (
                float(tokens_out) / 1000 * float(output_per_1k)
            )

    if isinstance(tokens_total, (int, float)):
        per_1k = model_pricing.get("per_1k")
        if isinstance(per_1k, (int, float)):
            return (float(tokens_total) / 1000) * float(per_1k)

    return None


def _meets_or_exceeds(value: float, threshold: float) -> bool:
    return value + _EPSILON >= threshold


def _format_cost_reason(
    increase_pct: float,
    baseline_cost: float,
    candidate_cost: float,
    baseline: dict,
    candidate: dict,
    threshold: float,
    severity: str,
) -> str:
    """Explicit reason: numbers and threshold."""
    cost_part = f"${baseline_cost:.4f} → ${candidate_cost:.4f}"
    token_part = _token_comparison(baseline, candidate)
    suffix = f"exceeding {threshold:.0f}% {severity} threshold"
    # Prefer tokens when they differ; otherwise use cost
    if token_part and _tokens_differ(baseline, candidate):
        return f"Cost increased by {increase_pct:.1f}% ({token_part}), {suffix}."
    return f"Cost increased by {increase_pct:.1f}% ({cost_part}), {suffix}."


def _tokens_differ(baseline: dict, candidate: dict) -> bool:
    """True when tokens_out or tokens_total differ between baseline and candidate."""
    b_out, c_out = baseline.get("tokens_out"), candidate.get("tokens_out")
    if isinstance(b_out, (int, float)) and isinstance(c_out, (int, float)):
        return int(b_out) != int(c_out)
    b_total, c_total = baseline.get("tokens_total"), candidate.get("tokens_total")
    if isinstance(b_total, (int, float)) and isinstance(c_total, (int, float)):
        return int(b_total) != int(c_total)
    return False


def _token_comparison(baseline: dict, candidate: dict) -> str:
    """Return '1,000 → 1,380 tokens' when tokens_out or tokens_total available."""
    b_out = baseline.get("tokens_out")
    c_out = candidate.get("tokens_out")
    if isinstance(b_out, (int, float)) and isinstance(c_out, (int, float)):
        return f"{int(b_out):,} → {int(c_out):,} tokens"
    b_total = baseline.get("tokens_total")
    c_total = candidate.get("tokens_total")
    if isinstance(b_total, (int, float)) and isinstance(c_total, (int, float)):
        return f"{int(b_total):,} → {int(c_total):,} tokens"
    return ""
