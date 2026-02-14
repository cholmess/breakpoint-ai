from breakpoint import evaluate


def test_cost_warn_on_increase():
    decision = evaluate(
        baseline={"output": "same", "cost_usd": 1.0},
        candidate={"output": "same", "cost_usd": 1.24},
    )
    assert decision.status == "WARN"
    assert "COST_WARN_INCREASE" in decision.codes


def test_pii_blocks_email():
    decision = evaluate(
        baseline={"output": "hello"},
        candidate={"output": "contact me at hi@example.com", "cost_usd": 1.0},
    )
    assert decision.status == "BLOCK"
    assert "PII_BLOCK_EMAIL" in decision.codes


def test_drift_blocks_empty_candidate():
    decision = evaluate(
        baseline={"output": "long baseline text", "cost_usd": 1.0},
        candidate={"output": "  ", "cost_usd": 1.0},
    )
    assert decision.status == "BLOCK"
    assert "DRIFT_BLOCK_EMPTY" in decision.codes


def test_strict_promotes_warn_to_block():
    decision = evaluate(
        baseline={"output": "abc", "cost_usd": 1.0},
        candidate={"output": "abcdef", "cost_usd": 1.24},
        strict=True,
    )
    assert decision.status == "BLOCK"
    assert "STRICT_PROMOTED_WARN" in decision.codes


def test_missing_cost_data_warns():
    decision = evaluate(
        baseline={"output": "hello"},
        candidate={"output": "hello there"},
    )
    assert decision.status in {"WARN", "BLOCK"}
    assert "COST_WARN_MISSING_DATA" in decision.codes
    assert "cost" in decision.details
