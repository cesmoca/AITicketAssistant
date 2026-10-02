import copy
import json
from unittest.mock import Mock

import pytest

from backend.domain.task_info import TaskInfo
from backend.domain.ticket_action import TicketAction, TicketActionType
from evals import run_eval
from evals.assertions import compare_case
from evals.loader import load_cases, validate_case


@pytest.fixture(autouse=True)
def isolated_configuration(monkeypatch):
    # Infrastructure tests do not load or modify the production prompts.
    from evals import runner

    monkeypatch.setattr(runner, "get_configuration", lambda: ("test-model", "test-instructions"))
    monkeypatch.setattr(run_eval, "get_configuration", lambda: ("test-model", "test-instructions"))


@pytest.fixture
def case():
    # Synthetic infrastructure fixture, not an AI evaluation dataset.
    return {
        "id": "infrastructure_check", "setup": {"tickets": []}, "input": "test input",
        "expected": {
            "response": {"status": "ok", "data": "Ticket added"},
            "database": {
                "ticket_count": 1,
                "tickets": [{"match": {"name": "Test"}, "assert": {"state": "ACTIVE"}}],
            },
        },
    }


@pytest.fixture
def parser_factory():
    parser = Mock()
    parser.request_ai.return_value = TicketAction(
        action_type=TicketActionType.NEW,
        info=TaskInfo(name="Test", appliance=None, address=None, failure=None, other_details=None),
    )
    return Mock(return_value=parser)


def test_loader_accepts_optional_fields_and_utf8_bom(tmp_path, case):
    path = tmp_path / "fixture.jsonl"
    path.write_text("\n" + json.dumps(case) + "\n", encoding="utf-8-sig")
    loaded = load_cases(path)
    assert loaded == [{**case, "source": str(path)}]


@pytest.mark.parametrize("field", ["id", "setup", "expected", "input"])
def test_loader_rejects_missing_fields(case, field):
    del case[field]
    with pytest.raises(ValueError):
        validate_case(case)


def test_loader_rejects_duplicate_ids(tmp_path, case):
    path = tmp_path / "fixture.jsonl"
    path.write_text(json.dumps(case) + "\n" + json.dumps(case), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate case ID"):
        load_cases(path)


def test_loader_rejects_unknown_fields_and_bad_state(case):
    case["setup"]["tickets"] = [{"state": ["ACTIVE"]}]
    with pytest.raises(ValueError, match="state"):
        validate_case(case)
    case["setup"]["tickets"] = [{"state": "ACTIVE", "failura": "test"}]
    with pytest.raises(ValueError, match="unknown"):
        validate_case(case)


def test_real_processor_and_repository_with_case_isolation(case, parser_factory):
    first = run_eval.execute_case(case, parser_factory=parser_factory)
    second = run_eval.execute_case(case, parser_factory=parser_factory)
    assert first["passed"] and second["passed"]
    assert first["initial_database"] == second["initial_database"] == {"ticket_count": 0, "tickets": []}
    assert first["actual"]["database"]["tickets"][0]["id"] == 1
    assert second["actual"]["database"]["tickets"][0]["id"] == 1
    assert parser_factory.call_count == 2
    assert parser_factory.return_value.request_ai.call_args.args[0].text == case["input"]


def test_setup_tickets_use_production_repository(case, parser_factory):
    case["setup"]["tickets"] = [{"name": "Existing", "state": "SUSPENDED"}]
    case["expected"]["database"]["ticket_count"] = 2
    result = run_eval.execute_case(case, parser_factory=parser_factory)
    assert result["passed"]
    initial = result["initial_database"]["tickets"][0]
    assert initial["name"] == "Existing" and initial["state"] == "SUSPENDED"
    assert initial["failure"] is None


@pytest.mark.parametrize("action_type", [TicketActionType.UPDATE, TicketActionType.CANCEL])
def test_existing_ticket_workflow(case, parser_factory, action_type):
    case["setup"]["tickets"] = [{
        "name": "Test", "state": "SUSPENDED", "appliance": "Washer", "failure": "Old failure",
    }]
    parser_factory.return_value.request_ai.return_value = TicketAction(
        action_type=action_type,
        info=TaskInfo(name="Test", appliance=None, address=None, failure="New failure", other_details=None),
    )
    case["expected"]["response"] = {"status": "error", "data": "resolution_required"}
    if action_type == TicketActionType.UPDATE:
        case["expected"]["database"]["tickets"][0]["assert"] = {
            "id": 1, "state": "SUSPENDED", "appliance": "Washer", "failure": "New failure",
        }
    else:
        case["expected"]["database"] = {
            "ticket_count": 0, "tickets": [], "absent": [{"name": "Test"}],
        }
    result = run_eval.execute_case(case, parser_factory=parser_factory)
    assert result["passed"], result["errors"]
    parser_factory.assert_called_once_with(model="test-model", instructions="test-instructions")


@pytest.mark.parametrize("count", [0, 2])
def test_matching_requires_exactly_one_ticket(case, count):
    actual = {"response": case["expected"]["response"], "database": {
        "ticket_count": 1, "tickets": [{"name": "Test", "state": "ACTIVE"}] * count,
    }}
    errors = compare_case(case["expected"], actual)
    assert errors == [f"ticket match={{'name': 'Test'}}: expected exactly 1 match; actual {count}"]


def test_only_declared_fields_are_checked(case):
    actual = {"response": {**case["expected"]["response"], "result": None}, "database": {
        "ticket_count": 1, "tickets": [{"name": "Test", "state": "ACTIVE", "failure": "Unasserted value"}],
    }}
    assert compare_case(case["expected"], actual) == []
    case["expected"]["database"]["tickets"][0]["assert"]["failure"] = "Expected failure"
    assert "failure" in compare_case(case["expected"], actual)[0]


def test_response_count_absent_and_missing_field_differences(case):
    case["expected"]["database"]["absent"] = [{"name": "Test"}]
    actual = {"response": {"status": "error"}, "database": {
        "ticket_count": 2, "tickets": [{"name": "Test", "state": "ACTIVE"}],
    }}
    errors = compare_case(case["expected"], actual)
    assert len(errors) == 4
    assert any("response.status" in error for error in errors)
    assert any("response.data: missing" in error for error in errors)
    assert any("ticket_count" in error for error in errors)
    assert any("absent" in error for error in errors)


def test_single_case_exception_propagates_with_diagnostics(case, parser_factory, capsys):
    parser_factory.return_value.request_ai.side_effect = RuntimeError("parser error")
    with pytest.raises(RuntimeError, match="parser error"):
        run_eval.execute_case(case, parser_factory=parser_factory)
    output = capsys.readouterr().out
    assert "FAIL: infrastructure_check" in output
    assert "INITIAL DATABASE" in output and "ACTUAL FINAL DATABASE" in output


def test_full_run_exception_is_recorded_with_traceback(case, parser_factory, capsys):
    parser_factory.return_value.request_ai.side_effect = RuntimeError("parser error")
    result = run_eval.execute_case(case, catch_exceptions=True, parser_factory=parser_factory)
    assert result["passed"] is False
    assert result["errors"] == ["RuntimeError: parser error"]
    assert result["actual"]["database"]["ticket_count"] == 0
    assert "Traceback" in capsys.readouterr().err


def test_cli_list_does_not_execute(case, monkeypatch, capsys):
    monkeypatch.setattr(run_eval, "load_cases", lambda source: [case])
    execute = Mock()
    monkeypatch.setattr(run_eval, "execute_case", execute)
    assert run_eval.main(["--list"]) == 0
    execute.assert_not_called()
    assert capsys.readouterr().out.strip() == case["id"]


def test_cli_selects_case_and_preserves_result_structure(case, parser_factory, monkeypatch, tmp_path):
    other = {**copy.deepcopy(case), "id": "other", "source": "datasets/1.0/fixture.jsonl"}
    case["source"] = other["source"]
    monkeypatch.setattr(run_eval, "load_cases", lambda source: [case, other])
    monkeypatch.setattr(run_eval, "OpenAITicketAI", parser_factory)
    output = tmp_path / "result.json"
    assert run_eval.main(["--case", case["id"], "--verbose", "--output", str(output)]) == 0
    document = json.loads(output.read_text(encoding="utf-8"))
    assert [row["id"] for row in document["cases"]] == [case["id"]]
    assert document["metrics"] == document["by_tag"] == {}
    assert document["metadata"]["dataset_version"] == "1.0"


def test_cli_full_run_continues_and_exits_nonzero(case, parser_factory, monkeypatch, tmp_path):
    second = {**copy.deepcopy(case), "id": "second"}
    case["source"] = second["source"] = "datasets/1.0/fixture.jsonl"
    monkeypatch.setattr(run_eval, "load_cases", lambda source: [case, second])
    parser_factory.return_value.request_ai.side_effect = [RuntimeError("first failed"), parser_factory.return_value.request_ai.return_value]
    monkeypatch.setattr(run_eval, "OpenAITicketAI", parser_factory)
    output = tmp_path / "result.json"
    assert run_eval.main(["--output", str(output)]) == 1
    document = json.loads(output.read_text(encoding="utf-8"))
    assert [row["passed"] for row in document["cases"]] == [False, True]
