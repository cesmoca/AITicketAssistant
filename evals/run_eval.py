import argparse
import json
import sys
import traceback
from pathlib import Path

# Support both python evals/run_eval.py and python -m evals.run_eval.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain.task_info import TaskInfo
from backend.domain.ticket import Ticket, TicketStatus
from backend.persistence.sqlalchemy_base import SQLAlchemyBase
from backend.processors.ai_ticket_processor import AITicketProcessor
from backend.processors.ticket_processor import ProcessTicketRequest
from backend.remote.openai_ticket_ai import OpenAITicketAI
from backend.repositories.sqlalquemy_ticket_repository import SQLAlchemyTicketRepository
from evals.assertions import compare_case
from evals.loader import INFO_FIELDS, load_cases
from evals.runner import build_metadata, get_configuration, save_results

EVALS_ROOT = Path(__file__).resolve().parent


def snapshot(repository: SQLAlchemyTicketRepository) -> dict:
    tickets = [
        {"id": ticket.id, **ticket.info.model_dump(mode="json"), "state": ticket.status.name}
        for ticket in repository.list()
    ]
    return {"ticket_count": len(tickets), "tickets": tickets}


def case_result(case: dict, initial: dict | None, actual: dict, errors: list[str]) -> dict:
    return {
        "id": case["id"], "input": case["input"], "expected": case["expected"],
        "actual": actual, "passed": not errors, "errors": errors,
        "notes": case.get("notes"), "initial_database": initial,
        "source": case.get("source"),
    }


def execute_case(case: dict, *, catch_exceptions: bool = False, parser_factory=None) -> dict:
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    repository = SQLAlchemyTicketRepository(sessionmaker(bind=engine))
    initial = None
    actual = {"response": None, "database": None}
    errors = []
    try:
        SQLAlchemyBase.metadata.create_all(engine)
        for fields in case["setup"]["tickets"]:
            repository.create(Ticket(
                id=None,
                info=TaskInfo(**{field: fields.get(field) for field in INFO_FIELDS}),
                status=TicketStatus[fields["state"]],
            ))
        initial = snapshot(repository)
        model, instructions = get_configuration()
        parser = (parser_factory or OpenAITicketAI)(instructions=instructions, model=model)
        processor = AITicketProcessor(repository=repository, ticket_ai=parser)
        response = processor.process_ticket(ProcessTicketRequest(text=case["input"]))
        actual["response"] = response.model_dump(mode="json")
        actual["database"] = snapshot(repository)
        errors = compare_case(case["expected"], actual)
    except Exception as error:
        errors.append(f"{type(error).__name__}: {error}")
        try:
            actual["database"] = snapshot(repository)
        except Exception as snapshot_error:
            errors.append(f"Database snapshot failed: {type(snapshot_error).__name__}: {snapshot_error}")
            traceback.print_exc()
        if not catch_exceptions:
            print_case(case_result(case, initial, actual, errors))
            raise
        traceback.print_exc()
    finally:
        engine.dispose()

    return case_result(case, initial, actual, errors)


def print_case(result: dict, verbose: bool = False) -> None:
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {result['id']}")
    if result["passed"] and not verbose:
        return
    details = {
        "INPUT": result["input"],
        "NOTES": result["notes"],
        "INITIAL DATABASE": result["initial_database"],
        "EXPECTED RESPONSE": result["expected"]["response"],
        "ACTUAL RESPONSE": result["actual"]["response"],
        "EXPECTED DATABASE ASSERTIONS": result["expected"]["database"],
        "ACTUAL FINAL DATABASE": result["actual"]["database"],
        "DIFFERENCES": result["errors"],
    }
    for label, value in details.items():
        print(f"\n{label}:\n{json.dumps(value, ensure_ascii=False, indent=2)}")


def main(argv: list[str] | None = None) -> int:
    cli = argparse.ArgumentParser(description="Evaluate the production ticket workflow with isolated databases.")
    cli.add_argument("dataset", nargs="?", type=Path, default=EVALS_ROOT / "datasets", help="JSONL file or directory; default: evals/datasets")
    cli.add_argument("--case", dest="case_id", help="Run one case; exceptions propagate for debugging")
    cli.add_argument("--verbose", action="store_true")
    cli.add_argument("--list", action="store_true", help="List case IDs without creating a database or calling AI")
    cli.add_argument("--dataset-version", help="Version label; default: selected dataset directories or file names")
    cli.add_argument("--run-id")
    cli.add_argument("--output", type=Path, help="Default: evals/results/<run_id>.json")
    args = cli.parse_args(argv)
    cases = load_cases(args.dataset)
    if args.case_id:
        cases = [case for case in cases if case["id"] == args.case_id]
        if not cases:
            cli.error(f"Unknown case ID: {args.case_id}")
    if args.list:
        for case in cases:
            print(case["id"])
        return 0

    version = args.dataset_version
    if version is None:
        version = ",".join(sorted({
            Path(case["source"]).stem if Path(case["source"]).parent == EVALS_ROOT / "datasets"
            else Path(case["source"]).parent.name
            for case in cases
        }))
    metadata = build_metadata(version, args.run_id)
    output = args.output or EVALS_ROOT / "results" / f"{metadata['run_id']}.json"
    results = []
    for case in cases:
        result = execute_case(case, catch_exceptions=args.case_id is None)
        print_case(result, args.verbose)
        results.append(result)
    save_results(results, metadata, output)
    print(f"Saved {len(results)} cases to {output}")
    return 1 if any(not result["passed"] for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
