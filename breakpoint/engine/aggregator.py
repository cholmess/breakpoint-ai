from breakpoint.engine.policies.base import PolicyResult
from breakpoint.models.decision import Decision


def aggregate_policy_results(results: list[PolicyResult], strict: bool = False) -> Decision:
    reasons = []
    codes = []
    details = {}

    has_block = False
    has_warn = False
    for result in results:
        reasons.extend(result.reasons)
        codes.extend(result.codes)
        if result.status == "BLOCK":
            has_block = True
        elif result.status == "WARN":
            has_warn = True
        details[result.policy] = result.details or {}

    if has_block:
        status = "BLOCK"
    elif has_warn:
        status = "WARN"
    else:
        status = "ALLOW"

    if strict and status == "WARN":
        status = "BLOCK"
        reasons.append("Strict mode promoted WARN to BLOCK.")
        codes.append("STRICT_PROMOTED_WARN")

    reason_codes = [_to_reason_code(code) for code in codes]
    metrics = _extract_metrics(details)
    return Decision(status=status, reasons=reasons, reason_codes=reason_codes, metrics=metrics, details=details)


def _to_reason_code(code: str) -> str:
    mapping = {
        "COST_WARN_INCREASE": "COST_INCREASE_WARN",
        "COST_BLOCK_INCREASE": "COST_INCREASE_BLOCK",
        "LATENCY_WARN_INCREASE": "LATENCY_INCREASE_WARN",
        "LATENCY_BLOCK_INCREASE": "LATENCY_INCREASE_BLOCK",
        "PII_BLOCK_EMAIL": "PII_EMAIL_BLOCK",
        "PII_BLOCK_PHONE": "PII_PHONE_BLOCK",
        "PII_BLOCK_CREDIT_CARD": "PII_CREDIT_CARD_BLOCK",
        "PII_BLOCK_SSN": "PII_SSN_BLOCK",
        "DRIFT_BLOCK_EMPTY": "DRIFT_EMPTY_OUTPUT_WARN",
        "DRIFT_WARN_SHORT_OUTPUT": "DRIFT_TOO_SHORT_WARN",
        "DRIFT_WARN_LENGTH_DELTA": "DRIFT_LENGTH_WARN",
        "DRIFT_WARN_LOW_SIMILARITY": "DRIFT_SIMILARITY_WARN",
        "STRICT_PROMOTED_WARN": "STRICT_MODE_PROMOTION_BLOCK",
    }
    return mapping.get(code, code)


def _extract_metrics(details: dict) -> dict:
    metrics = {}

    cost = details.get("cost", {})
    if isinstance(cost.get("increase_pct"), (int, float)):
        metrics["cost_delta_pct"] = round(float(cost["increase_pct"]), 4)
    if isinstance(cost.get("delta_usd"), (int, float)):
        metrics["cost_delta_usd"] = round(float(cost["delta_usd"]), 6)

    latency = details.get("latency", {})
    if isinstance(latency.get("increase_pct"), (int, float)):
        metrics["latency_delta_pct"] = round(float(latency["increase_pct"]), 4)
    if isinstance(latency.get("delta_ms"), (int, float)):
        metrics["latency_delta_ms"] = round(float(latency["delta_ms"]), 4)

    drift = details.get("drift", {})
    if isinstance(drift.get("length_delta_pct"), (int, float)):
        metrics["length_delta_pct"] = round(float(drift["length_delta_pct"]), 4)
    if isinstance(drift.get("short_ratio"), (int, float)):
        metrics["short_ratio"] = round(float(drift["short_ratio"]), 6)
    if isinstance(drift.get("similarity"), (int, float)):
        metrics["similarity"] = round(float(drift["similarity"]), 6)

    return metrics
