from dataclasses import dataclass, field


@dataclass(frozen=True)
class Decision:
    status: str
    reasons: list[str] = field(default_factory=list)
    codes: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)
