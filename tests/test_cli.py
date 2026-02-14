import json
import subprocess
import sys


def test_cli_evaluate_json_output(tmp_path):
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    baseline_path.write_text(json.dumps({"output": "hello", "cost_usd": 1.0}), encoding="utf-8")
    candidate_path.write_text(json.dumps({"output": "hello world", "cost_usd": 1.25}), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "breakpoint.cli.main",
            "evaluate",
            str(baseline_path),
            str(candidate_path),
            "--json",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "WARN"
    assert "COST_WARN_INCREASE" in payload["codes"]


def test_cli_strict_blocks(tmp_path):
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    baseline_path.write_text(json.dumps({"output": "hello", "cost_usd": 1.0}), encoding="utf-8")
    candidate_path.write_text(json.dumps({"output": "hello world", "cost_usd": 1.25}), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "breakpoint.cli.main",
            "evaluate",
            str(baseline_path),
            str(candidate_path),
            "--strict",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "STATUS: BLOCK" in result.stdout
