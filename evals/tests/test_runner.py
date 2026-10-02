import json
from datetime import datetime
from unittest.mock import Mock

import pytest

from backend.constants import MODEL, SYSTEM_PROMPT
from backend.constants.prompts.system_prompt_v1 import SYSTEM_PROMPT_V1
from backend.domain.task_info import TaskInfo
from backend.domain.ticket_action import TicketAction, TicketActionType
from evals import runner
from version import PROMPT_VERSION, SYSTEM_VERSION


def test_production_configuration_can_be_loaded():
    assert runner.get_configuration() == (MODEL, SYSTEM_PROMPT)
    assert SYSTEM_PROMPT == SYSTEM_PROMPT_V1
    assert isinstance(SYSTEM_PROMPT, str) and SYSTEM_PROMPT


def test_metadata_and_result_json(tmp_path):
    metadata = runner.build_metadata("ticket_eval_v1", "test_run")
    assert set(metadata) == {
        "run_id", "system_version", "dataset_version", "prompt_version",
        "model", "git_commit", "timestamp",
    }
    assert metadata["run_id"] == "test_run"
    assert metadata["system_version"] == SYSTEM_VERSION
    assert metadata["dataset_version"] == "ticket_eval_v1"
    assert metadata["prompt_version"] == PROMPT_VERSION
    assert metadata["model"] == MODEL
    assert datetime.fromisoformat(metadata["timestamp"]).utcoffset().total_seconds() == 0
    path = tmp_path / "results" / "run.json"
    cases = [{"input": "Avería", "expected": None, "actual": None}]
    runner.save_results(cases, metadata, path)
    assert json.loads(path.read_text(encoding="utf-8")) == {
        "metadata": metadata, "metrics": {}, "by_tag": {}, "cases": cases,
    }


def test_metadata_without_git(monkeypatch):
    monkeypatch.setattr(runner.subprocess, "run", Mock(side_effect=OSError("git unavailable")))
    metadata = runner.build_metadata("v1")
    assert metadata["git_commit"] is None
    assert metadata["run_id"]


def test_parser_only_runner_preserves_inputs_and_expected(tmp_path):
    path = tmp_path / "fixture.jsonl"
    cases = [{"input": "Avería", "expected": {"name": None}},
             {"id": "explicit", "input": "Otro aviso", "expected": {}}]
    path.write_text("\n".join(json.dumps(case) for case in cases), encoding="utf-8-sig")
    action = TicketAction(
        action_type=TicketActionType.NEW,
        info=TaskInfo(name=None, appliance=None, address=None, failure=None, other_details=None),
    )
    parser = Mock()
    parser.request_ai.return_value = action
    results = runner.run_cases(runner.load_dataset(path), parser)
    assert [call.args[0].text for call in parser.request_ai.call_args_list] == [case["input"] for case in cases]
    assert [row["id"] for row in results] == ["case_001", "explicit"]
    for case, result in zip(cases, results):
        assert result["input"] == case["input"]
        assert result["expected"] == case["expected"]
        assert result["actual"] == action.model_dump(mode="json")
        assert result["actual"]["info"]["name"] is None
        assert result["passed"] is None
        assert result["errors"] == []


def test_parser_only_runner_rejects_missing_action():
    parser = Mock()
    parser.request_ai.return_value = None
    with pytest.raises(RuntimeError, match="no parsed action"):
        runner.run_cases([{"input": "test", "expected": {}}], parser)
