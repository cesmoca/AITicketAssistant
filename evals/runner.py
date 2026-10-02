import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from backend.constants import MODEL, SYSTEM_PROMPT
from backend.processors.ticket_processor import ProcessTicketRequest
from backend.remote.openai_ticket_ai import OpenAITicketAI
from backend.remote.ticket_ai import TicketAI
from version import PROMPT_VERSION, SYSTEM_VERSION


def load_dataset(path: Path) -> list[dict]:
    cases = []
    with path.open(encoding="utf-8-sig") as dataset:
        for line_number, line in enumerate(dataset, start=1):
            if not line.strip():
                continue

            try:
                case = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"{path}:{line_number}: invalid JSON") from error

            if not isinstance(case, dict) or not isinstance(case.get("input"), str):
                raise ValueError(f"{path}:{line_number}: input must be a string")
            if "expected" not in case:
                raise ValueError(f"{path}:{line_number}: expected is required")

            cases.append(case)
    return cases


def run_cases(cases: list[dict], parser: TicketAI) -> list[dict]:
    results = []
    for index, case in enumerate(cases, start=1):
        action = parser.request_ai(ProcessTicketRequest(text=case["input"]))
        if action is None:
            raise RuntimeError("The AI parser returned no parsed action")

        results.append({
            "id": case.get("id", f"case_{index:03d}"),
            "input": case["input"],
            "expected": case["expected"],
            "actual": action.model_dump(mode="json"),
            "passed": None,
            "errors": [],
        })
    return results


def build_metadata(dataset_version: str, run_id: str | None = None) -> dict:
    started_at = datetime.now(timezone.utc)
    repository_root = Path(__file__).resolve().parents[1]
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repository_root,
            check=True, capture_output=True, text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        commit = None

    return {
        "run_id": run_id if run_id is not None else started_at.strftime("%Y-%m-%d_%H%M%S%f"),
        "system_version": SYSTEM_VERSION,
        "dataset_version": dataset_version,
        "prompt_version": PROMPT_VERSION,
        "model": MODEL,
        "git_commit": commit,
        "timestamp": started_at.isoformat().replace("+00:00", "Z"),
    }


def save_results(results: list[dict], metadata: dict, path: Path) -> None:
    document = {
        "metadata": metadata,
        "metrics": {},
        "by_tag": {},
        "cases": results,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    cli = argparse.ArgumentParser(description="Run the existing AI parser on a JSONL dataset.")
    cli.add_argument("dataset", type=Path, help="Path to the input JSONL dataset")
    cli.add_argument("--dataset-version", required=True, help="Version of the supplied dataset")
    cli.add_argument("--run-id", help="Run identifier; defaults to a UTC timestamp")
    cli.add_argument("--output", type=Path, required=True, help="Path to the results JSON")
    args = cli.parse_args()

    cases = load_dataset(args.dataset)
    metadata = build_metadata(args.dataset_version, args.run_id)
    parser = OpenAITicketAI(instructions=SYSTEM_PROMPT, model=MODEL)
    results = run_cases(cases, parser)
    save_results(results, metadata, args.output)
    print(f"Saved {len(results)} results to {args.output}")


if __name__ == "__main__":
    main()
