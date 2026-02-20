import re

from breakpoint.engine.policies.base import PolicyResult


def evaluate_red_team_policy(candidate: dict, config: dict) -> PolicyResult:
    if not bool(config.get("enabled", True)):
        return PolicyResult(policy="red_team", status="ALLOW")

    text = candidate.get("output", "")
    if not isinstance(text, str):
        text = str(text)

    blocked_type_counts: dict[str, int] = {}
    categories = config.get("categories", {})
    
    for category_name, patterns in categories.items():
        if not isinstance(patterns, list):
            continue
            
        count = 0
        for pattern in patterns:
            try:
                # Use case-insensitive matching by default for red team patterns
                regex = re.compile(pattern, re.IGNORECASE)
                matches = list(regex.finditer(text))
                count += len(matches)
            except re.error:
                continue
                
        if count > 0:
            blocked_type_counts[category_name.upper()] = count

    if blocked_type_counts:
        blocked_categories = sorted(blocked_type_counts.keys())
        total = sum(blocked_type_counts.values())
        parts = [f"{name}({blocked_type_counts[name]})" for name in blocked_categories]
        return PolicyResult(
            policy="red_team",
            status="BLOCK",
            reasons=[f"Red Team policy violation: {', '.join(parts)}. Total matches: {total}."],
            codes=[f"RED_TEAM_BLOCK_{name}" for name in blocked_categories],
            details={
                "blocked_categories": blocked_categories,
                "blocked_category_counts": blocked_type_counts,
                "blocked_total": total,
            },
        )
    return PolicyResult(policy="red_team", status="ALLOW")
