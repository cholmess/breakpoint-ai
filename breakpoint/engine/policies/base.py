from dataclasses import dataclass, field


@dataclass
class PolicyResult:
    status: str
    reasons: list[str] = field(default_factory=list)
    codes: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)
