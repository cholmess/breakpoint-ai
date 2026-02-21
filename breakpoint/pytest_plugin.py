import pytest
import json
import os
from pathlib import Path
from breakpoint import evaluate as breakpoint_evaluate

class BreakpointAssertor:
    def __init__(self, request):
        self.request = request
        self.test_name = request.node.name
        self.test_dir = Path(request.node.fspath).parent
        
        # Directory to store baselines alongside tests
        self.baseline_dir = self.test_dir / "baselines"
        
    def assert_stable(self, candidate_output: str | dict, candidate_metadata: dict = None, name: str = None, fail_on: str = "warn"):
        """
        Asserts that the candidate output is stable compared to the baseline.
        
        Args:
            candidate_output: The text or JSON output from your agent/LLM.
            candidate_metadata: Optional dictionary of tokens, cost, etc.
            name: Optional specific name for the baseline. Defaults to test function name.
            fail_on: Level at which the test should fail ("warn" or "block"). Default "warn".
        """
        if isinstance(candidate_output, dict):
            candidate_text = json.dumps(candidate_output)
        else:
            candidate_text = str(candidate_output)
            
        baseline_name = f"{name or self.test_name}.json"
        
        baseline_path = self.baseline_dir / baseline_name
        
        if not candidate_metadata:
            candidate_metadata = {}
            
        # If no baseline exists, we either fail (strict) or create one (lenient)
        # For this plugin, let's explicitly require the user to use an environment variable to update/create
        update_baselines = os.environ.get("BREAKPOINT_UPDATE_BASELINES", "0") == "1"
        
        if not baseline_path.exists() or update_baselines:
            if not update_baselines and not baseline_path.exists():
                pytest.fail(
                    f"Baseline file missing at {baseline_path} and BREAKPOINT_UPDATE_BASELINES=1 is not set. "
                    f"Set the environment variable to generate the baseline."
                )
            
            # Create baseline
            self.baseline_dir.mkdir(parents=True, exist_ok=True)
            baseline_data = {
                "output": candidate_text,
                **candidate_metadata
            }
            with open(baseline_path, "w") as f:
                json.dump(baseline_data, f, indent=2)
            
            # If updating/creating, we don't evaluate, we just pass
            return True
            
        # Read baseline
        with open(baseline_path, "r") as f:
            baseline_json = json.load(f)
            
        baseline_text = baseline_json.get("output", "")
        # Extract baseline metrics (cost, latency, tokens...)
        baseline_meta = {k: v for k, v in baseline_json.items() if k != "output"}
        
        # Merge metadata for evaluation
        combined_meta = {}
        for k, v in baseline_meta.items():
            combined_meta[f"baseline_{k}"] = v
        for k, v in candidate_metadata.items():
            combined_meta[f"candidate_{k}"] = v
            
        decision = breakpoint_evaluate(
            baseline_output=baseline_text,
            candidate_output=candidate_text,
            metadata=combined_meta
        )
        
        # Check fail thresholds
        should_fail = False
        if fail_on.lower() == "block" and decision.status == "BLOCK":
            should_fail = True
        elif fail_on.lower() == "warn" and decision.status in ("WARN", "BLOCK"):
            should_fail = True
            
        if should_fail:
            reasons_str = "\n  - ".join(decision.reasons)
            raise AssertionError(f"Breakpoint Policy Violation: {decision.status}\nReasons:\n  - {reasons_str}")
            
        return True


@pytest.fixture
def breakpoint(request):
    """
    Breakpoint fixture to perform policy assertions on LLM outputs in pytest.
    """
    return BreakpointAssertor(request)
