# Runbook

Open this folder in Codex or Claude Code and say **“go”**. The session coordinates fresh
assignment-solving subagents using the harness's native tools. It does not solve the
assignment itself. No shell script launches model sessions.

## 0. Ground rules for the coordinating session

This folder coordinates an informal instructional-design exploration. Carry out this workflow
using native assignment-solving subagents with fresh contexts. Do not solve the assignment in
the coordinating session. Launch only planned models your native tools support; do not
substitute models or shell out to another model harness. Editing this procedure is not a
request to launch runs. These rules apply to the coordinating session only; solvers get
nothing but their task (§3). Keep this context out of `AGENTS.md`/`CLAUDE.md` at the top of
this folder: solver subagents load those automatically.

## 1. Choose the runs

You MUST read `plan.csv` and check which planned models your native subagent tools can
actually launch. The initial plan is one PLAIN attempt each for Codex, Opus, and Sonnet.
Run the available rows; report the unavailable ones without substituting another model.
For example, Codex can run its Codex row, and a Claude Code session can run its Claude rows.
Mike may also name a specific row or prompt.

You MUST skip runs that already have results. Do not overwrite a previous attempt. If Mike
requests another attempt, add a new row with a new run ID and repetition number.

## 2. Prepare assignment folders

You MUST run `scripts/setup_runs.sh "$PWD/runs" HARNESS`, replacing HARNESS with `codex` or
`claude` for the rows you can launch. This helper only copies instructions, references, and
the 2025 data; it does not start agents. Check that the selected run folders contain
`reference/`, `data/`, `answers/figures/`, `work/`, and a short `AGENTS.md` / `CLAUDE.md`.
If data retrieval fails, report the problem and keep any existing work.

The folders live in `runs/` for convenience. Separate folders and fresh contexts are enough
for this informal exploration; they are not filesystem isolation.

## 3. Delegate the assignment

You MUST launch one fresh native subagent per selected row, with the row's requested model.
Run sequentially so it is easy to follow progress. Do not reuse a solver from another row.

You MUST give the solver only:

- The absolute path of its run folder and an instruction to use it as its working directory and read
  its `CLAUDE.md`/`AGENTS.md` (these hold only neutral task instructions).
- The student prompt and common tail, obtained with
  `/opt/anaconda3/envs/p314/bin/python scripts/get_prompt.py PROMPT_ID`.

Use an agent type that can write files and run tools. If the tool supports excluding parent
history, select that option. In this Codex environment, use `collaboration.spawn_agent` with
`fork_turns="none"` and the planned `model`; this runbook authorizes those model selections.
In Claude Code, use the Agent tool with `subagent_type: "general-purpose"` and `model` set to
`opus` or `sonnet` — never `fork`, which inherits the coordinator's conversation. Its final
report comes back to you; for the optional debrief, continue the same agent with
`SendMessage` to its ID. Package-approval requests from a solver come back to you as its
result: relay them to Mike.
Do not attach the runbook, experiment discussion, other submissions, or comparison criteria:
the solver only needs the assignment request. If the runtime cannot provide a fresh context,
report that limitation instead of silently sending the parent conversation.

You MUST record the start time, requested model, harness/interface, and returned agent ID in
`results/RUN_ID/run.json`. Record the actual model if the runtime reports it; otherwise leave
`actual_model` blank. Tell Mike which row is running and provide brief progress updates.

Let the solver finish normally. There is no automatic time cap or intermediate snapshotting.
If it gets stuck, record what happened and interrupt it if necessary. Do not improve its
answer or send corrective assignment advice, because the first attempt is what we want to
see. Save refusals, incomplete answers, and questions as outcomes too.
If a new package is needed, propose it to Mike for approval under the environment policy.
Do not install packages automatically or replace `p314` with another Python environment.

## 4. Keep the result

You MUST save the solver's final message in `results/RUN_ID/final.md`, record its end time and
status in `run.json`, and copy `answers/` to `results/RUN_ID/frozen/` and `work/` to
`results/RUN_ID/work/`. Keep the original run folder too. Save a transcript or session
reference when readily available. Telemetry is optional: missing logs, token counts, or cost
estimates MUST NOT block completion or make a run unsuccessful. Do not rerun an assignment
just to obtain telemetry. In Claude Code, when available, copy the
solver's `agent-<id>.jsonl` and `.meta.json` from
`~/.claude/projects/<this-folder>/<session>/subagents/` into `results/RUN_ID/`, and take
`actual_model` from the `message.model` field of its assistant entries. In Codex, when available, copy the session log
(`~/.codex/sessions/.../rollout-*.jsonl` for the solver's thread) into `results/RUN_ID/`.
`collect.py` reads token counts and estimates cost from these copies when present. Otherwise,
leave unavailable fields blank and briefly note the reporting limitation.
These logs stay local (git-ignored): they contain the user-level harness configuration.

**Keep employer and infrastructure details out of git.** Before committing, scan everything
that will be committed and redact what you find — debriefs and final messages often name the
harness, cloud provider, or plugins. The terms to look for are in `.private-terms` (local,
git-ignored):

```
git add -A -n | cut -c6- | tr -d "'" | xargs grep -liE -f .private-terms
```

Ignore false positives (e.g. a country name or a substring of an ordinary word). Don't write
these details into `run.json`, `RESULTS.md`, or `journal.md` either.

Check whether `answer.md` and the six requested figure files exist. Record missing pieces,
tooling problems, refusals, and anything conspicuous in `run.json`'s `notes`. Do not repair
the submission or repeat an attempt just because it looks poor. Infrastructure failures
before any assignment work can be retried in a new run folder, with the reason recorded.

An optional debrief is in `PROMPTS.md`. Use it only if Mike asks or a particular result makes
it useful. If the runtime supports resuming the same solver, send it there after saving the
result, then copy `debrief/` into the results folder. If it cannot resume, omit the debrief.
Treat self-reports as commentary, not verified measurements.

## 5. Report and pause for inspection

You MUST run `/opt/anaconda3/envs/p314/bin/python scripts/collect.py` and write or update
`RESULTS.md` with a small table and brief observations: completeness, design choices,
obvious failures, disclosure, and anything worth Mike's attention. Mike does the grading.
The collector uses `run.json`; a minimal record looks like:

```json
{
  "harness": "codex",
  "interface": "Codex session with native subagents",
  "requested_model": "openai.gpt-6.1-sol",
  "actual_model": "",
  "agent_id": "returned agent ID",
  "start": "2026-10-22T09:00:00-05:00",
  "end": "2026-10-22T09:12:00-05:00",
  "status": "completed",
  "notes": ""
}
```

Append one short session summary to `journal.md`: rows attempted, outcomes, important
decisions, and problems. Do not log every command.

After the initial available PLAIN runs, stop for Mike to inspect the results. The remaining
prompts are options for later exploration, not a batch to launch automatically.
