import re

from breakpoint.engine.policies.base import PolicyResult


def evaluate_drift_policy(baseline: dict, candidate: dict, thresholds: dict) -> PolicyResult:
    baseline_text = _as_text(baseline.get("output", ""))
    candidate_text = _as_text(candidate.get("output", ""))

    if not candidate_text.strip():
        return PolicyResult(
            status="BLOCK",
            reasons=["Candidate output is empty."],
            codes=["DRIFT_BLOCK_EMPTY"],
        )

    reasons = []
    codes = []
    details = {}

    baseline_len = max(1, len(baseline_text))
    candidate_len = len(candidate_text)
    delta_pct = abs(candidate_len - baseline_len) / baseline_len * 100
    short_ratio = candidate_len / baseline_len

    warn_delta = float(thresholds.get("warn_length_delta_pct", 60))
    warn_short_ratio = float(thresholds.get("warn_short_ratio", 0.35))
    min_similarity = float(thresholds.get("warn_min_similarity", 0.15))
    semantic_enabled = bool(thresholds.get("semantic_check_enabled", True))

    if delta_pct > warn_delta:
        reasons.append(f"Output drift detected: length delta {delta_pct:.1f}% (>{warn_delta:.0f}%).")
        codes.append("DRIFT_WARN_LENGTH_DELTA")
        details["length_delta_pct"] = delta_pct

    if short_ratio < warn_short_ratio:
        reasons.append(
            f"Output drift detected: candidate length ratio {short_ratio:.2f} (<{warn_short_ratio:.2f})."
        )
        codes.append("DRIFT_WARN_SHORT_OUTPUT")
        details["short_ratio"] = short_ratio

    if semantic_enabled:
        similarity = _token_overlap_similarity(baseline_text, candidate_text)
        details["similarity"] = similarity
        if similarity < min_similarity:
            reasons.append(
                f"Output drift detected: lexical similarity {similarity:.2f} (<{min_similarity:.2f})."
            )
            codes.append("DRIFT_WARN_LOW_SIMILARITY")

    if reasons:
        return PolicyResult(status="WARN", reasons=reasons, codes=codes, details=details)
    return PolicyResult(status="ALLOW", details=details)


def _token_overlap_similarity(left: str, right: str) -> float:
    left_tokens = set(_tokenize(left))
    right_tokens = set(_tokenize(right))
    union = left_tokens | right_tokens
    if not union:
        return 1.0
    intersection = left_tokens & right_tokens
    return len(intersection) / len(union)


def _tokenize(value: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+", value.lower())


def _as_text(value: object) -> str:
    if isinstance(value, str):
        return value
    return str(value)
