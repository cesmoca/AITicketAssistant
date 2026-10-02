# AI parser evaluations

This runner calls the existing `OpenAITicketAI` parser directly, using the model
and instructions in `backend/constants.py`. It does not run the ticket processor
or write to the application database.

## Dataset contract

Supply a UTF-8 JSONL file with one JSON object per line. Each object must have:

- `input`: the text to parse, as a string.
- `expected`: the expected output, preserved as supplied.

An optional `id` is copied to the result. When omitted, the runner assigns IDs
such as `case_001` using the case's position in the dataset.

Blank lines are ignored. No dataset is included in this skeleton.

## Run

From the repository root, with the backend dependencies installed and
`OPENAI_API_KEY` set:

```powershell
backend\.venv\Scripts\python.exe -m evals.runner <dataset.jsonl> --dataset-version ticket_eval_v1 --run-id 2026-10-02_baseline --output evals/results/2026-10-02_baseline.json
```

Replace `<dataset.jsonl>` with the path to your dataset. The output is a JSON
object with `metadata`, `metrics`, `by_tag`, and a `cases` array. Each case contains
`id`, `input`, `expected`, `actual`, `passed`, and `errors`. `actual` is the parsed
`TicketAction`, serialized to JSON.

No comparisons or metrics are calculated yet: `metrics` and `by_tag` are empty
objects, `passed` is `null`, and `errors` is an empty list. These placeholders do
not mean the case passed or was checked for errors.

## Versions

- `SYSTEM_VERSION` and `PROMPT_VERSION` are defined in the root `version.py`.
  Update the system version when releasing application changes, and the prompt
  version when changing the extraction instructions in `backend/constants.py`.
- Dataset versions belong to each dataset, rather than one global constant.
  Organize future datasets as `evals/datasets/<name>/<version>/dataset.jsonl`
  and pass that version explicitly with `--dataset-version`. The runner does
  not infer it from the filename or directory. Use a new directory/version
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

The output file is overwritten when rerunning the command. An invalid dataset
or parser failure stops the run; results are written after all cases finish.
