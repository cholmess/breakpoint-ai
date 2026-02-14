import argparse
import json

from breakpoint.engine.evaluator import evaluate


def main() -> int:
    parser = argparse.ArgumentParser(prog="breakpoint")
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate_parser = subparsers.add_parser("evaluate", help="Compare baseline and candidate.")
    evaluate_parser.add_argument("baseline_path", help="Path to baseline JSON input.")
    evaluate_parser.add_argument("candidate_path", help="Path to candidate JSON input.")
    evaluate_parser.add_argument("--strict", action="store_true", help="Promote WARN to BLOCK.")
    evaluate_parser.add_argument("--config", help="Path to custom JSON config.")
    evaluate_parser.add_argument("--json", action="store_true", help="Emit JSON decision output.")

    args = parser.parse_args()
    if args.command == "evaluate":
        return _run_evaluate(args)
    return 1


def _run_evaluate(args: argparse.Namespace) -> int:
    baseline_data = _read_json(args.baseline_path)
    candidate_data = _read_json(args.candidate_path)

    decision = evaluate(
        baseline=baseline_data,
        candidate=candidate_data,
        strict=args.strict,
        config_path=args.config,
    )

    if args.json:
        print(
            json.dumps(
                {
                    "status": decision.status,
                    "reasons": decision.reasons,
                    "codes": decision.codes,
                    "details": decision.details,
                },
                indent=2,
            )
        )
        return 0

    print(f"STATUS: {decision.status}")
    for reason in decision.reasons:
        print(f"- {reason}")
    return 0


def _read_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    raise SystemExit(main())
