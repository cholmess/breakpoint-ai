import re

from breakpoint.engine.policies.base import PolicyResult


def evaluate_pii_policy(candidate: dict, patterns: dict, allowlist: list[str]) -> PolicyResult:
    text = candidate.get("output", "")
    if not isinstance(text, str):
        text = str(text)

    blocked_patterns = []
    compiled_allowlist = [re.compile(item) for item in allowlist]
    for label, pattern in patterns.items():
        regex = re.compile(pattern)
        if not regex.search(text):
            continue
        if _is_allowlisted(text, regex, compiled_allowlist):
            continue
        blocked_patterns.append(label.upper())

    if blocked_patterns:
        return PolicyResult(
            status="BLOCK",
            reasons=[f"PII detected: {', '.join(blocked_patterns)}."],
            codes=[f"PII_BLOCK_{name}" for name in blocked_patterns],
        )
    return PolicyResult(status="ALLOW")


def _is_allowlisted(text: str, regex: re.Pattern, allowlist: list[re.Pattern]) -> bool:
    for match in regex.finditer(text):
        value = match.group(0)
        for allowed in allowlist:
            if allowed.search(value):
                return True
    return False
