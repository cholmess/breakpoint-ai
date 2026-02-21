import pytest
import functools
from io import StringIO
import tempfile
import json

# This test file uses the `breakpoint` fixture provided by our new plugin.

def agent_mock(prompt):
    """A mock LLM that generates a fixed output based on the prompt."""
    if prompt == "hello":
        return "Hello world!"
    if prompt == "secret":
        return "My password is mypassword123 and phone is 555-010-9999"
    return "Generic response."

def test_stable_output(breakpoint):
    # First run will fail because baseline doesn't exist, OR we can mock the existence.
    # The simplest way to test is to just provide candidate metadata and evaluate
    # But since the plugin writes/reads to the filesystem based on the test name,
    # let's write to it using the fixture internals for the test.
    
    # Setup baseline (include cost_usd so cost policy has data)
    breakpoint.baseline_dir.mkdir(parents=True, exist_ok=True)
    baseline_path = breakpoint.baseline_dir / "test_stable_output.json"
    with open(baseline_path, "w") as f:
        json.dump({"output": "Hello world!", "cost_usd": 0.01}, f)
        
    output = agent_mock("hello")
    # This should pass without raising because "Hello world!" matches "Hello world!"
    breakpoint.assert_stable(
        candidate_output=output,
        candidate_metadata={"cost_usd": 0.01},
        name="test_stable_output",
    )


def test_unstable_output_blocks(breakpoint):
    breakpoint.baseline_dir.mkdir(parents=True, exist_ok=True)
    baseline_path = breakpoint.baseline_dir / "test_unstable_output_blocks.json"
    
    # Baseline was clean (include cost_usd for cost policy)
    with open(baseline_path, "w") as f:
        json.dump({"output": "Hello world!", "cost_usd": 0.01}, f)
        
    # Candidate outputs PII (phone number)
    output = agent_mock("secret")
    
    # This should block (fail) because PII is blocked by default in lite mode
    with pytest.raises(Exception, match="BLOCK"):
        breakpoint.assert_stable(
            candidate_output=output,
            candidate_metadata={"cost_usd": 0.01},
            name="test_unstable_output_blocks",
        )


def test_unstable_output_warns(breakpoint):
    breakpoint.baseline_dir.mkdir(parents=True, exist_ok=True)
    baseline_path = breakpoint.baseline_dir / "test_unstable_output_warns.json"
    
    # Baseline was a short sentence (include cost_usd for cost policy)
    with open(baseline_path, "w") as f:
        json.dump({
            "output": "Short response.",
            "cost_usd": 0.01,
            "tokens_total": 10,
        }, f)
        
    # Drift: WARN at +35%, BLOCK at +70%. Baseline 15 chars.
    # Candidate 21 chars = 40% expansion -> WARN (not BLOCK)
    output = "This is a longer reply"
    
    metadata = {"cost_usd": 0.01, "tokens_total": 13}
    
    # By default, assert_stable fails on "warn".
    with pytest.raises(Exception, match="WARN"):
        breakpoint.assert_stable(candidate_output=output, candidate_metadata=metadata, name="test_unstable_output_warns")

