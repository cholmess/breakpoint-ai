from dataclasses import dataclass, field


@dataclass(frozen=True)
class Decision:
    schema_version: str = "1.0.0"
    status: str = "ALLOW"
    reasons: list[str] = field(default_factory=list)
    reason_codes: list[str] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    details: dict = field(default_factory=dict)

    @property
    def codes(self) -> list[str]:
        return self.reason_codes

    def to_dict(self) -> dict:
        payload = {
            "schema_version": self.schema_version,
            "status": self.status,
            "reasons": self.reasons,
            "reason_codes": self.reason_codes,
        }
        if self.metrics:
            payload["metrics"] = self.metrics
        if self.metadata:
            payload["metadata"] = self.metadata
        return payload
