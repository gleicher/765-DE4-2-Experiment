# RUNBOOK — read this and go

You are the orchestrator for a batch of agent runs. Your job is mechanical: set up folders, run
the scripts, check outputs, collect results. **Do not do the assignment yourself, and do not
read or edit the run agents' answers beyond the checks below.** Read `README.md` for why.

All commands run from this directory (`43-de4-2-experiment/`).

## 0. Preflight (once)

1. **Check the CLI flags the scripts assume.** Run `claude --help` and `codex exec --help`
   (and `codex exec resume --help`). `scripts/run_one.sh` assumes:
   - claude: `-p`, `--model`, `--output-format json`, `--permission-mode bypassPermissions`, `--resume <session_id>`; the JSON result has `session_id`, `usage`, `total_cost_usd`, `num_turns`, and possibly `modelUsage`.
   - codex: `exec`, `--model`, `--json`, `--full-auto`, `exec resume <id>`; network access enabled for the sandbox.
   If anything differs, fix the two harness blocks in `run_one.sh` and note the change at the
   bottom of this file. Don't change the prompts.
2. **Set the Codex model** in `plan.csv` (replace `CODEX_MODEL`). Ask Mike if unsure.
3. **Check for leaks into the run sessions:**
   - User-level instruction files (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, or similar)
     must not mention this course, grading, or this experiment. If they do, stop and tell Mike.
   - Turn off any persistent memory feature the harness has, if possible, or tell Mike it's on.
   - Built-in skills: leave the harness default, and record what it is below.
4. **Check the runs root is outside this directory** (default `~/de4-2-runs`; results go to
   `~/de4-2-results`).
5. **Dry run:** `python3 scripts/get_prompt.py PLAIN` and `python3 scripts/get_prompt.py DEBRIEF` should print the prompts.

## 1. Set up

```
scripts/setup_runs.sh            # makes ~/de4-2-runs/<run_id>/{reference,data,answers}
```

Spot-check one run folder: `reference/` has 6 `.md` files and `images/`; there's no
`MANIFEST.md`; `data/` has the CSVs and readmes.

## 2. Run

Run the rows **one at a time** (cleaner timing and cost; avoids rate-limit interference):

```
for id in $(tail -n +2 plan.csv | cut -d, -f1); do scripts/run_one.sh "$id"; done
```

Each run takes up to 60 minutes plus the debrief. After each, check `~/de4-2-results/<id>/`:
`frozen/answer.md` exists, `turn1.exit` is 0 (142 means it hit the 60-minute cap — that's a valid result,
not a failure), `session_id.txt` is non-empty, `debrief/ABOUT.md` exists. If a run errors out
before producing anything (auth failure, bad flag), fix the cause, delete that run's folder in
both roots, re-run `setup_runs.sh`, and re-run it. **Do not re-run because the output looks bad.**

If an agent refuses or pushes back (asks whether AI is allowed, etc.), don't re-prompt. Record
it in the notes column.

## 3. Collect

```
python3 scripts/collect.py
```

Then fill in by hand, in `runs.csv` → `notes`: refusals or pushback; any reads outside the run
folder you can see in the logs; whether the run opened `posts/de4-codes` or other post-deadline
pages (check `frozen/sources.txt` and the logs); anything odd. For Codex runs, turn the usage
event in `notes` into token counts.

Convert tokens to API-equivalent dollars using the providers' published prices **on the run
date**; write the price table you used at the bottom of this file. Where a run spawned
sub-agents on other models, count each model at its own price.

## 4. Report

Write `RESULTS.md` here: a table of runs (wall-clock, cost, figures, words, cap hit?), plus a
short paragraph of anything Mike should know (failures, leaks, flag changes). No evaluation of
the submissions' quality — that's a separate step.

Hand back: `runs.csv`, `RESULTS.md`, and the path to `~/de4-2-results/`.

---

## Operator notes (fill in during the run)

- Harness versions:
- Flag changes made to `run_one.sh`:
- Skills / memory settings:
- Price table used:
