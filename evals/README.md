# Evaluation infrastructure

Two runners are available:

- `run_eval.py` executes the production ticket processor with a clean SQLite
  database for each case and checks the response and final database assertions.
- `runner.py` keeps the earlier parser-only mode, which records `TicketAction`
  outputs without executing repository operations.

Both reuse `OpenAITicketAI` and the configuration in
`backend/constants/constants.py`. Neither imports `backend.main` or touches the
application database. The first workflow dataset contains 56 behavior targets at
`evals/datasets/tickets/ticket_eval_v1/dataset.jsonl`. It includes future features
and is expected to report failures against the current implementation.
The dataset uses the production state name `SUSPENDED` for paused tickets.

## Parser-only dataset contract

Supply a UTF-8 JSONL file with one JSON object per line. Each object must have:

- `input`: the text to parse, as a string.
- `expected`: the expected output, preserved as supplied.

An optional `id` is copied to the result. When omitted, the runner assigns IDs
such as `case_001` using the case's position in the dataset.

Blank lines are ignored. The included dataset targets the full workflow runner.

## Run the parser-only mode

From the repository root, with the backend dependencies installed and
`OPENAI_API_KEY` set:

```powershell
backend\.venv\Scripts\python.exe -m evals.runner <dataset.jsonl> --dataset-version ticket_eval_v1 --run-id 2026-10-02_baseline --output evals/results/2026-10-02_baseline.json
```

Replace `<dataset.jsonl>` with the path to your dataset. The output is a JSON
object with `metadata`, `metrics`, `by_tag`, and a `cases` array. Each case contains
`id`, `input`, `expected`, `actual`, `passed`, and `errors`. `actual` is the parsed
`TicketAction`, serialized to JSON.

In parser-only mode, no comparisons or metrics are calculated: `metrics` and `by_tag` are empty
objects, `passed` is `null`, and `errors` is an empty list. These placeholders do
not mean the case passed or was checked for errors.

## Versions

- `SYSTEM_VERSION` and `PROMPT_VERSION` are defined in the root `version.py`.
  Update the system version when releasing application changes, and the prompt
  version when changing the active extraction instructions in `backend/constants/prompts/`.
- Dataset versions belong to each dataset, rather than one global constant.
  Organize future datasets as `evals/datasets/<name>/<version>/dataset.jsonl`
  and pass that version explicitly with `--dataset-version`. The runner does
  not infer it from the filename or directory in parser-only mode. Use a new directory/version
  when changing cases or expected outputs, preserving earlier versions.
- `git_commit` records the full Git HEAD hash at the start of the run, or `null`
  if unavailable. HEAD does not include uncommitted changes.
- `model` records the configured parser model. `timestamp` records the start of
  the run in UTC using an ISO 8601 string ending in `Z`.
- `run_id` comes from `--run-id`, or is generated from the UTC start time when
  omitted.

Metadata is stored once per run and applies to every case in the cases array.
No datasets or dataset versions are created by the runner.

Datasets and result JSON files are intended to be committed to Git. Store each
run in a separate file named after its `run_id`, so previous results remain
available for comparison alongside the dataset and code versions.

The output file is overwritten when rerunning the command. In parser-only mode,
an invalid dataset or parser failure stops the run; results are written after all cases finish.

## Full workflow runner

`evals/run_eval.py` implements the following workflow case schema and CLI.
It records per-case pass/fail assertions; aggregate metrics remain unimplemented.

### Case schema

The workflow dataset uses one object per JSONL line. This example documents
the schema only; it is not an included dataset case:

```json
{
  "id": "update_ambiguous_same_name_001",
  "setup": {
    "tickets": [
      {
        "name": "Pedro",
        "appliance": "lavadora",
        "failure": "no centrifuga",
        "address": "Calle Agua 4",
        "state": "ACTIVE"
      }
    ]
  },
  "input": "Soy Pedro, cambia lo de la lavadora para el jueves",
  "expected": {
    "response": {
      "status": "ok",
      "data": "resolution_required"
    },
    "database": {
      "ticket_count": 1,
      "tickets": [
        {
          "match": {
            "name": "Pedro",
            "appliance": "lavadora"
          },
          "assert": {
            "failure": "no centrifuga",
            "address": "Calle Agua 4",
            "state": "ACTIVE"
          }
        }
      ],
      "absent": []
    }
  },
  "notes": "Optional human-readable explanation."
}
```

`expected.database.absent` and `notes` are optional. The loader validates the
minimum required structure, field types, state names, and unique case IDs before execution. Flat information fields are translated into `Ticket.info` at the evaluation
boundary. `state` uses uppercase enum names such as `ACTIVE`, translated to
`Ticket.status`. Setup tickets require `state`; omitted information fields become
`null`, and IDs are assigned by the production repository. The example's response values are expected assertions, not
a guarantee of the application's current behavior.

### Execution and database isolation

For every case, the workflow runner:

1. Create a clean isolated test database.
2. Insert the tickets in `setup.tickets`.
3. Execute the real production flow using `input`.
4. Capture the application response and query the final database state.
5. Compare the expected response, `ticket_count`, matched ticket fields, and
   optional absence assertions.
6. Print a clear PASS or FAIL for the case and return a non-zero process exit
   code if any case fails.

Each case gets a new SQLAlchemy SQLite engine using `sqlite://` and
`StaticPool`. The runner creates tables from `SQLAlchemyBase.metadata`, inserts
setup tickets with `SQLAlchemyTicketRepository.create()`, executes
`AITicketProcessor.process_ticket()`, reads the final state through the same
repository, and disposes the engine. A fresh AI adapter is created for each case.
Cases cannot share database state or write to `backend/tickets.db`. Per-case assertions are separate from aggregate metrics: no accuracy,
precision, recall, F1, or other aggregate metrics are part of this stage.

### Matching and assertions

`match` locates a ticket in the final database and must match exactly one row:

- Zero matches: fail because the expected ticket is missing.
- One match: check only the fields explicitly declared in `assert`.
- Multiple matches: fail and report the ambiguity.

Do not compare the entire Ticket object when only selected fields are asserted.
If `expected.database.absent` is supplied, its selectors must match zero final
tickets. Entries may be direct field selectors or objects containing `match`.
Selectors and assertions support `id`, `state`, and the five information fields.
Matching uses exact field equality. Response comparison checks the fields supplied
in `expected.response`, allowing extra response fields such as `result`.

### Workflow CLI

From the repository root, with the backend virtual environment activated and
`OPENAI_API_KEY` configured:

```powershell
# Run all cases
python evals/run_eval.py

# Run one case
python evals/run_eval.py --case update_ambiguous_same_name_001

# Run one case with detailed diagnostics
python evals/run_eval.py --case update_ambiguous_same_name_001 --verbose

# List case IDs without executing them
python evals/run_eval.py --list
```

The default source is `evals/datasets/`, searched recursively for `*.jsonl` in
sorted order. You may supply a file or directory as a positional argument.
The included `ticket_eval_v1` dataset is loaded by default.
`--list` validates and lists IDs without calling AI or creating a database.

Without activating the virtual environment, use its interpreter directly:

```powershell
backend\.venv\Scripts\python.exe evals/run_eval.py
backend\.venv\Scripts\python.exe evals/run_eval.py --case update_ambiguous_same_name_001
backend\.venv\Scripts\python.exe evals/run_eval.py --case update_ambiguous_same_name_001 --verbose
backend\.venv\Scripts\python.exe evals/run_eval.py --list
```

Additional options are `--dataset-version`, `--run-id`, and `--output`. Results
use the existing metadata/metrics/by_tag/cases structure and default to
`evals/results/<run_id>.json`. When no dataset version is supplied, the runner
uses the selected files' parent directory names (or file stems for files directly
under `evals/datasets/`), joining multiple labels with commas. Supply an explicit
version label when evaluating a dataset collection.

Per-case `actual` contains `response` and `database`, not just the parser action.
The result also records the initial database, optional notes, source path,
`passed`, and descriptive `errors`. `metrics` and `by_tag` remain empty.

### Failure diagnostics and debugging

Every failing case must print its ID, input, optional notes, initial database
state, expected and actual response, expected database assertions, final
database state, and clear field-level differences. An ambiguity report must
identify the selector that matched multiple tickets. Verbose mode may include
additional intermediate information already accessible without changing
production behavior.

Do not hide exceptions. Full-run mode may catch an exception per case to continue
with the remaining cases, but it must print the exception type and traceback.
Single-case mode (`--case`) prints diagnostics and re-raises the original
exception, so a Python debugger or IDE can stop on the original stack frame.
No additional debug flag is needed. Avoid wrapper layers that obscure the production call stack.

### Scope and infrastructure tests

Loading/validation lives in `loader.py`, comparisons in `assertions.py`, and
execution/CLI in `run_eval.py`. Shared result writing and version metadata are
reused from `runner.py`.

Focused tests use synthetic temporary fixtures and mocked AI responses while
executing the real processor and repository. They cover validation, database
isolation, setup, unique matching, partial assertions, absence checks, CLI
selection, JSON results, failure exit codes, continuation, and exception traces.
They make no live AI calls and add no dataset files under `evals/datasets/`.

```powershell
backend\.venv\Scripts\python.exe -m pytest evals/tests -q
```

- Do not change production AI behavior, prompts, or unrelated production code.
- Keep dataset behavior targets intact; aggregate metrics remain unimplemented.
- Do not add dashboards, external eval frameworks, MLflow, pandas, LangSmith,
  or similar dependencies.
- Reuse the production pipeline and keep the diff small and reviewable.
- Add focused automated tests for infrastructure where useful.

Production exceptions remain visible to the runner; this infrastructure does
not fix or change the application behavior being evaluated.
