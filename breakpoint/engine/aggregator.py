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

    return Decision(status=status, reasons=reasons, codes=codes, details=details)
