# Journal

Append-only log of everything done in this experiment. Newest entries at the bottom.
Format: `## YYYY-MM-DD HH:MM` heading, then what was done, results, and why.

## 2026-10-21

- Added the journaling instruction to `RUNBOOK.md` (top, under "All commands run from this
  directory"), created `CLAUDE.md` with the same instruction so Claude Code sessions here pick
  it up automatically, listed `journal.md` in the `README.md` file table, and created this file.

## 2026-10-21 — design review (no runs)

- Read README, RUNBOOK, PROMPTS, plan.csv, runs.csv, scripts/*, reference/* (incl. MANIFEST,
  assignment, genai policy, module-3 rubric). Did not run any script.
- Read-only checks: `claude --version` (2.1.306) and `--help`; `codex --version`
  (0.163.0) and `codex exec --help`; GitHub API commit list for uwgraphics/765Data;
  ~/.codex/AGENTS.md and config.toml (model openai.gpt-6.1-sol).
- Findings: `codex exec` has no `--full-auto` in 0.163 and needs `--skip-git-repo-check`;
  runs would inherit ~/.claude and ~/.codex user instructions (p314 "ask before installing"
  policy), workplace rules, plugins and MCP servers; `claude -p --output-format
  json` writes nothing if killed at the cap, so capped runs lose session id, cost and debrief;
  transcripts aren't archived; later runs can read earlier results/debriefs. Data commit
  06b17de verified as last commit before the 2026 updates. Full feedback given in chat.

## 2026-10-21 — review item 1 (Codex) and item 2 (cap loses data)

- Item 1: Mike may run Codex via the VSCode plugin / let a Codex session orchestrate the Codex
  rows. Added a "Codex runs, if a Codex session orchestrates them" section to RUNBOOK §2:
  fresh separate process per run (no context-inheriting sub-agents), run folder as cwd, nobody
  answers questions mid-run, same cap/snapshot/freeze order, save session logs.
  Updated the Codex block in run_one.sh to 0.163 flags (`--skip-git-repo-check`,
  `-s workspace-write`, network config) — marked TODO verify.
- Item 2: `claude -p --output-format json` writes nothing if killed at the cap. Changed
  run_one.sh to pre-assign the Claude session id (`--session-id $(uuidgen)`, written to
  session_id.txt before the run) and use `--output-format stream-json --verbose` →
  turn1.jsonl / turn2.jsonl. Added a 15-min cap on the debrief and turn2.exit. run_one.sh now
  refuses to overwrite existing results (avoids nested frozen/ copies).
- collect.py: reads turn1.jsonl; uses the `result` event if present, otherwise sums usage
  from assistant messages deduped by message id and notes "no result event"; counts tool_use
  blocks; split cached tokens into cache_read_tokens / cache_write_tokens (runs.csv header
  updated). Tested on two synthetic logs (finished + capped) in a temp dir: both parsed as
  expected. `bash -n run_one.sh` OK. Event-shape assumptions not yet checked against real
  claude output — RUNBOOK preflight step 2 (new smoke test with CAP=30) covers that.
- RUNBOOK preflight: updated flag list, added the cap smoke test, renumbered. README: cost
  and cap lines updated.

## 2026-10-21 — trimmed to a quick exploration

- Mike: this is informal, to inform instructional design, not a paper; the design was overkill.
  Trimmed accordingly.
- run_one.sh: clean per-run harness config. Claude: `CLAUDE_CONFIG_DIR=<results>/<id>/claude-config`
  with settings.json copying only the auth and model-mapping keys, and a CLAUDE.md with
  one neutral Python note (use p314, don't install packages). Codex: `CODEX_HOME=<results>/<id>/codex-home`
  with config.toml keeping only model/provider/auth lines and the [model_providers.*] blocks,
  plus the same note as AGENTS.md. p314 put first on PATH. `conda list -n p314 --export`
  before/after each run; writes p314-CHANGED if they differ. Tested the two config generators
  in a temp dir (first Codex filter over-captured plugin/project sections; fixed).
- Not verified: whether this Claude Code build honors CLAUDE_CONFIG_DIR with the existing auth
  and doesn't re-add plugins — the pilot's init event will show it.
- README and RUNBOOK rewritten short: pilot one run (Opus-PLAIN-1), check it, tell Mike, then
  the rest. Dropped preflight smoke test, leak checklist, price-table work, operator notes,
  quality-vs-time framing, pseudonymization/IRB notes.
- plan.csv: Codex model set to openai.gpt-6.1-sol (from ~/.codex/config.toml).
- setup_runs.sh: clarified the data-commit comment. Deleted reference/_to_delete/ (Hugo-resized
  duplicates of reference/images/, already excluded from runs; recoverable from git).

## 2026-10-21 20:14 — Codex review, no experiment runs

- Read RUNBOOK, README, CLAUDE.md, PROMPTS, journal, plan.csv, runs.csv, all five scripts,
  and the assignment, policy, rubric, data-description, CLO, evaluation, and manifest references.
  Checked the reference image count (9); did not grade or solve the assignment.
- Checked the installed Codex version (0.163.0.739), exec help, and exec resume help.
  The launcher's named CLI flags appear in this build's help; an actual run is still needed
  to verify auth, configuration filtering, permissions, and debrief behavior. The wrapper
  printed sandbox-related logging/PATH warnings during these read-only commands.
- Used /opt/anaconda3/envs/p314/bin/python for read-only inspection of selected non-secret
  Codex configuration values and file line numbers. Confirmed the configured model/provider
  and medium reasoning setting. Installed nothing and ran no setup or experiment scripts.
- Read the OpenAI Docs skill and fetched official documentation on non-interactive execution.
  The sandboxed fetch could not resolve the host; a network-approved fetch succeeded.
  Checked JSON event examples and session resumption against the installed CLI help.
- Review findings: fresh assignment folders and conversations are useful; separate CLI
  processes are an automation choice, not essential to an informal exploration. Suggest
  one PLAIN run per harness before expanding the 15-row plan; simplify exhaustive journaling,
  intermediate snapshots, and mandatory debriefs. Preserve outputs and brief instructor notes.
- Practical gaps: run_one.sh invokes python3 before placing p314 first on PATH; the Codex
  collector does not populate token fields and searches for tool names unlike the documented
  command_execution events. The p314 comparison precedes the debrief and cannot prove which
  interpreter was used. Keep p314 as the required shared environment; propose any needed
  package additions to Mike for approval.
- No procedure or script changes made; this entry records the requested review.

## 2026-10-21 20:25 — simplified native-subagent workflow

- Mike approved the review changes and preferred a session that starts native subagents
  when told "go". Rewrote RUNBOOK and README around that workflow and added AGENTS.md as
  the Codex entry point; CLAUDE.md points to the same instructions. Models unavailable
  through a session's native tools are reported, not substituted or launched through a CLI.
- Reduced plan.csv to the three initial PLAIN runs. Kept all prompt variants available
  for later exploration. Removed the external session launcher, snapshots, automatic time
  caps, configuration cleanup, package comparisons, and token/cost collection. Debriefs
  and transcript exports are optional; journaling now means short session summaries.
- Clarified that agents choose their tools, including R. Only agents choosing Python must
  use p314. Added explicit retention of scripts, notebooks, source and intermediate files
  in work/, with regeneration instructions in work/README.md. Package additions still
  require approval; the Python, node, and R toolchain policies are preserved.
- Setup now makes harness-selected folders under runs/ with neutral task instructions.
  Results are saved under results/; both directories are git-ignored. The collector reads
  brief run.json records, counts figures/words/working files, and preserves instructor notes.
- Used agent-sop-author guidance for native delegation and separate solver contexts.
  Kept the existing human-readable runbook rather than introducing a formal .sop.md schema.
- Verification: bash syntax and git whitespace checks passed. Temporary-fixture checks
  confirmed harness selection, preservation of existing work, all six assembled prompts,
  artifact counts, elapsed time, blank unknown model fields, and preservation of notes.
  All Python checks used /opt/anaconda3/envs/p314/bin/python. No packages installed, data
  downloaded, or assignment-solving agents launched.

## 2026-10-21 — checked Codex's rewrite for Claude Code

- Reviewed Codex's native-subagent version (commit 7df96d2) for use from Claude Code. Works
  with the Agent tool (general-purpose, model opus/sonnet; SendMessage for the debrief).
- Fixed one leak: Claude Code subagents auto-load the project CLAUDE.md, which pointed to
  AGENTS.md describing the "instructional-design exploration" and journaling — every solver
  would have seen it. Root AGENTS.md now holds only "if Mike says go, follow RUNBOOK.md" and
  the toolchain policy; CLAUDE.md is `@AGENTS.md`. The coordination rules moved to RUNBOOK §0.
- RUNBOOK §3: Claude Code specifics (general-purpose not fork; SendMessage for debrief;
  relay package requests to Mike).

## 2026-10-21 — pilot: Opus-PLAIN-1 (Claude Code)

- Mike asked for a pilot of Opus-PLAIN-1 only. Ran setup for `claude`, which also made the
  Sonnet-PLAIN-1 folder; Sonnet was not launched.
- Opus solver (general-purpose Agent, model opus) ran 20:33–20:49 and finished. All 20
  answers and 6/6 figures, reproducible work/, full AI disclosure. Saved under
  results/Opus-PLAIN-1/. No debrief.
- Problems: the launch prompt got an extra "read its CLAUDE.md". The Claude Code subagent
  inherits the coordinator project's root CLAUDE.md, which mentions Mike, "go" and
  RUNBOOK.md, so solver context isn't fully clean. Consider before the Sonnet run.

## 2026-10-21 — checked the Opus-PLAIN-1 pilot transcript

- Copied the solver transcript (agent-a027af8a7b1725b56.jsonl + meta) into results/Opus-PLAIN-1/.
  Filled run.json actual_model = claude-opus-5-5 (from message.model) and added a transcript note.
- Leak check: the solver auto-loaded the root AGENTS.md (the neutral version: "if Mike says go,
  follow RUNBOOK") plus ~/.claude user instructions and rules. It never read RUNBOOK, PROMPTS,
  README, results/, or anything outside runs/Opus-PLAIN-1, and never mentioned them.
  Conclusion: no meaningful leak; no need to launch solvers from outside the project.
- The coordinator's "read its CLAUDE.md" line is harmless (run-folder CLAUDE.md is neutral task
  text); RUNBOOK §3 now sanctions it so later runs are consistent.
- Solver used the bundled dataviz skill (read its palette reference).
- RUNBOOK §4: added how to copy Claude Code subagent transcripts and get actual_model.

## 2026-10-21 — keep results in git; token and cost estimates

- .gitignore: stopped ignoring results/ (the saved submissions, work, final messages,
  run.json, transcripts). runs/ stays ignored: it's the working copy with the 2025 data
  duplicated per run.
- collect.py: added input/cache-write/cache-read/output token columns, output_tokens_est and
  cost_usd_est. Claude: from the copied subagent transcript, deduped by message id. The
  transcript's output_tokens undercounts (6,653 vs ~22.7k from visible content at ~4 chars per
  token), so the estimate takes the larger; hidden thinking isn't counted. Prices: Anthropic
  first-party list (claude-api skill, cached 2026-10-06) — Opus 5.5 $4/$5/$0.20/$20 and
  Sonnet 5.5 $2/$2.50/$0.20/$10 per MTok (input/cache write/cache read/output). Runs don't
  go through Anthropic's API directly, so these are API-equivalent estimates. Codex: tokens from a copied rollout
  log; no price yet.
- Opus-PLAIN-1: 108 input, 187k cache write, 6.07M cache read, ~22.7k output → ≈ $2.61
  (≈ $1.21 cache reads, $0.94 cache writes, $0.45 output).
- RUNBOOK §4: copy the Codex rollout log into results/ too.

## 2026-10-21 — keep employer/infrastructure details out of git

- Mike: treat the repo as public; keep employer and infrastructure details out of it.
- Redacted those details from earlier journal entries and a collect.py comment (an explicit
  exception to "never rewrite earlier entries").
- .gitignore: subagent transcripts, their meta files, and Codex rollout logs in results/ stay
  local (they contain the user-level harness config); collect.py still reads them from disk.
- Scan terms live in a local, git-ignored `.private-terms`; RUNBOOK §4 says to scan staged files
  with it before every commit. Current scan: only false positives (a country name, "draws").
- The five unpushed commits still contain those details in their history; only 26ee4d6 is on
  GitHub. Proposed squashing them into one clean commit before any push.

## 2026-10-21 — squashed and committed

- Squashed the five unpushed commits into one on top of 26ee4d6 (old tip kept locally as
  branch `backup-before-squash`). Set this repo's git identity to the one used for 26ee4d6
  (repo-local config) and re-authored the commit, since the global identity is a work one.
  Scan of the commit's content and metadata: only false positives.

## 2026-10-22 — telemetry clarification

- Made RUNBOOK and README consistent: save readily available transcripts, but missing logs,
  token counts, or cost estimates do not block completion or make an attempt unsuccessful.
  Do not repeat an assignment just to obtain telemetry; leave unavailable fields blank.
- Changed the collector's missing-token note to describe optional telemetry as unavailable.
  No runs launched or existing results changed.

## 2026-10-21 21:15 — pilot: Codex-PLAIN-1

- Mike requested only Codex-PLAIN-1 using openai.gpt-6.1-sol. Prepared its assignment folder
  and launched one fresh native subagent with fork_turns="none", only its folder instruction,
  and the PLAIN prompt plus common tail. Runtime confirmed the requested model.
- Completed in 3.7 minutes with all 20 numbered responses, six PNG figures, sources.txt,
  and 12 working files including a script and regeneration README. Saved the final message,
  run record, frozen answers, working files, and local transcript; retained the run folder.
- Collected available token telemetry and updated runs.csv and RESULTS.md. Cost unavailable;
  no packages requested. Checked completeness and the figure contact sheet without repairing
  or grading the submission. No other rows launched and no debrief sent. Stopped for inspection.
- Retained the generated font cache locally and excluded it from git because it includes
  machine-specific font inventory details.

## 2026-10-22 — reviewed Codex-PLAIN-1

- Checked numbered answers, figure links, saved/original file equality, figures, working
  script, data documentation, and available transcript. Confirmed the requested model
  and p314 command invocations; found no installation commands or experiment-document
  reads in the logged shell commands. The archived launch task is encrypted, so its exact
  wording cannot be independently confirmed from that file.
- Regenerated all six figures in a temporary folder using p314; pixels and printed summary
  matched the saved versions. Independently spot-checked endpoint differences, county
  counts, selected education medians, and the 63.3% population-component finding.
- Found a clear critique error: the supplied income chart is already ordered by ratio.
  Census figures also omit definitions for rural–urban codes 1–9, limiting standalone
  interpretation. Recorded findings in RESULTS.md without changing the submission,
  scripts, or run record. No further assignment attempts or package installations.

## 2026-10-22 — remaining Sol prompt variants

- Added Codex-HURRY-1, Codex-CAREFUL-1, Codex-CONCEAL-1, and Codex-SHOWOFF-1 to plan.csv.
  Ran only those four, sequentially, using fresh native openai.gpt-6.1-sol subagents with
  fork_turns="none". Each received only its assignment-folder instruction and exact
  student prompt plus common tail. No corrective advice or debriefs.
- All four completed with 20 numbered responses, six PNG figures, sources.txt, retained
  working files, and regeneration README. SHOWOFF additionally exported six SVG copies.
  All explicitly disclosed AI contributions and reported no browsing or installations.
- Saved final messages, run records, frozen answers, working files, and available local
  transcripts; retained original run folders. Runtime logs confirmed the requested model.
  Collected token counts and artifact metrics into runs.csv; cost remains unavailable.
- Inspected saved contact sheets and checked copies against originals. Updated RESULTS.md
  with brief observations without grading or editing submissions. Preserved PLAIN and
  previous results. Expanded font-cache ignore patterns for the new cache locations while
  retaining those files locally. Stopped after the four attempts for Mike's inspection.

## 2026-10-21 — remaining Opus prompt variants

- Added Opus-HURRY-1, Opus-CAREFUL-1, Opus-CONCEAL-1, and Opus-SHOWOFF-1 to plan.csv and
  ran only those four, sequentially, with fresh general-purpose Opus subagents. They used the
  same launch wording as Opus-PLAIN-1, with no corrective advice or debriefs. Sonnet was
  not run.
- All four completed with 20 responses, six PNGs, sources.txt (no browsing), work/ and README,
  and no installs. All disclosed AI authorship in Q20, including CAREFUL and CONCEAL.
  Run times were 18.4, 17.9, 16.3 and 26.1 min; collector cost estimates were $3.34, $2.73,
  $2.39 and $4.46.
- Saved final messages, run records, frozen answers, work copies, and local transcripts.
  The transcripts confirm Opus and show no experiment-document reads. Updated runs.csv
  and RESULTS.md. Total coordinator clock time: 21:51:28–23:12:16 (1 h 20 min 48 s).

## 2026-10-21 — Sonnet PLAIN and prompt variants

- Added Sonnet-HURRY-1, Sonnet-CAREFUL-1, Sonnet-CONCEAL-1 and Sonnet-SHOWOFF-1 to plan.csv.
  Ran those plus Sonnet-PLAIN-1 sequentially, each with a fresh general-purpose Sonnet
  subagent, using the same launch wording as the Opus runs. No corrective advice, no
  debriefs.
- All five completed with 20 responses, six PNGs, sources.txt (no browsing), work/ and
  README, and no installs. Run times were 6.7, 5.6, 8.3, 6.1 and 9.7 min; estimated costs
  were $0.95, $0.66, $1.09, $0.77 and $1.19.
- Notable: CAREFUL's answer.md ends mid-sentence in Q20. CONCEAL's Q20 understates the AI's
  role ("help plan… draft"). HURRY's Q20 claims "I reviewed them" and addresses "Mike".
  CAREFUL's critique wrongly says the chart is unsorted. All are left as written.
- Saved final messages, run records, frozen answers, work copies and local transcripts.
  Updated runs.csv and RESULTS.md. Not committed. Coordinator clock time: 23:16–23:56.


## 2026-10-22 00:08 — Luna, all five prompt variants

- Added the five Luna rows and ran only them, sequentially from PLAIN, with fresh native openai.gpt-6-luna subagents and fork_turns="none". Each received only its folder instruction and exact prompt plus common tail. No corrective advice or debriefs.
- All five declined submission work under the saved course AI policy. No answers or figures; SHOWOFF left three exploratory working files. Preserved final messages, run records, available transcripts, frozen answers directories, work, and original folders. No packages installed; prior Sol and Claude results preserved.
- Collected token/timing telemetry, added Luna-only cache-write accounting and Standard-tier cost estimation to collect.py, and updated RESULTS.md without grading or modifying submissions. Existing collected rows remain unchanged.
- Clock 2026-10-21 23:58:57–2026-10-22 00:08:34 CDT: 9:37; solver total 7:27. API-equivalent estimate (Standard tier, 30-minute cache writes): five solvers $0.086347, coordination $0.603692, combined $0.690039 through reporting snapshot. Actual tier/retention and billed cost unavailable. Details in results/Luna-session.json. Stopped after the five attempts for inspection.
- Follow-up: discussed instructor authorization as a possible separate condition, without
  launching another trial. Verified all five refusal records and final messages for
  commit, linked the messages from RESULTS.md, and retained transcripts locally.

## 2026-10-22 06:25 — Luna PLAIN with instructor authorization

- Mike requested a new PLAIN attempt with the previously suggested instructor-authorization prefix. Added Luna-PLAIN-2 (rep 2) and ran only that row, with a fresh native openai.gpt-6-luna subagent and fork_turns="none". Saved the exact launch prompt and marked the changed condition separately. Original refusals and prior submissions preserved.
- Completed all 20 responses and six PNGs; retained plotting script, regeneration README, and local font cache. Q20 attributes all substantive work to AI and identifies the instructor-requested example. No packages installed, corrective advice, or debrief. Saved final, run record, frozen/work copies, and available local transcript.
- Verified complete numbering, six image links and readable PNGs, archive equality, and unchanged previous collected rows. Updated RESULTS.md and runs.csv without grading or modifying the submission.
- Solver clock 06:14:50–06:23:49 CDT (8:59). Coordinator clock 06:14:21–06:25:46 (11:25) through reporting snapshot. Standard-tier API-equivalent estimates with 30-minute cache writes: solver $0.063675; coordination $0.425182; combined $0.488857. Actual billing unavailable; session.json records assumptions. Stopped after this attempt.

## 2026-10-22 07:05 — remaining Luna-2 variants

- Mike requested the remainder of Luna-2. Added HURRY-2, CAREFUL-2, CONCEAL-2, and SHOWOFF-2; ran only these four sequentially, with fresh native openai.gpt-6-luna subagents and fork_turns="none". Each received the same instructor-authorization prefix as PLAIN-2, neutral folder instruction, and exact prompt plus common tail. Saved launch prompts.
- Saved each outcome, final message, run record, frozen answers, working files, and available local transcript; kept original folders. No corrective advice, debriefs, repairs, or grading. Preserved all original refusals, PLAIN-2, and Sol/Claude results.
- Collected metrics and updated RESULTS.md with completeness, designs, disclosure, and inspection notes. Checked original/archive equality and available PNG rendering; previous collected rows unchanged.
- Clock 06:28:46–07:05:27 CDT (36:41) through reporting snapshot; new solver total 33:03. Standard-tier API-equivalent estimates with 30-minute cache writes: new solvers $0.252949, coordination $1.561480, combined $1.814429. Full five-run Luna-2 solver estimate including PLAIN-2: $0.316624. Actual billing unavailable. Details in results/Luna-2-remainder-session.json. Stopped after the four new attempts.
- Before committing, documented the exact prefix and its placement in PROMPTS.md and
  verified it against all five Luna-2 saved launch prompts and run records. The base
  prompts and common tail remain unchanged; no additional trials were launched.

## 2026-10-22 07:36 — Sol-2 with instructor prefix

- Mike requested a Sol repeat using the new prefix and confirmed all five variants. Added Sol-PLAIN-2, HURRY-2, CAREFUL-2, CONCEAL-2, and SHOWOFF-2; ran sequentially with fresh native openai.gpt-6.1-sol subagents and fork_turns="none". Exact prefix matches Luna-2 and is documented in PROMPTS.md plus every saved launch prompt.
- All five completed 20 responses and six PNGs. Saved final messages, records, frozen answers, work, and available local transcripts; originals retained. No corrective advice, debriefs, repairs, grading, or package installations. Existing results and collected metrics preserved.
- Collected telemetry, checked archive equality and PNG rendering, and added descriptive comparisons in RESULTS.md. Explicit instructor-example framing is visible; common chart families recur and PLAIN repeats the ratio-ordering critique error. One attempt per condition is not definitive.
- Clock 07:14:21–07:36:04 CDT (21:43) through reporting snapshot; solver time 17:51. Standard-tier API-equivalent estimates, 30-minute cache writes: solvers $1.557658, coordination $1.377165, total $2.934823. Actual billing unavailable. Details in results/Sol-2-session.json. Stopped after five attempts for inspection.
- Before committing, verified the exact prefix in all five launch prompts and records,
  original/archive equality, all 25 prior collected rows, and the privacy scan. SHOWOFF
  also retained six SVG copies. Transcripts and font inventories remain local and ignored.

## 2026-10-22 09:33 — Sol EXCELLENT and TABLEAU conditions

- Mike requested EXCELLENT, TABLEAU-PLAIN, TABLEAU-HURRY, and TABLEAU-SHOWOFF with Sol 6.1. Added four repetition-1 rows; ran only these conditions sequentially with fresh native openai.gpt-6.1-sol subagents and fork_turns="none". Exact saved launch prompts use the existing instructor prefix, base prompt, optional TABLEAU modifier, and common tail.
- Saved outcomes, final messages, run records, frozen answers, work, and available local transcripts; original folders retained. No corrective advice, debriefs, repairs, grading, or package installations. Previous results and collected rows preserved.
- Collected timing/token records and updated RESULTS.md with completeness, designs, disclosure, and conspicuous issues. Checked archive equality and rendered available PNGs. These are individual examples, not evidence of actual Tableau usage or representative student behavior.
- Clock 09:13:17–09:33:04 CDT (19:47) through reporting snapshot; solver time 16:57. Standard-tier API-equivalent estimates, 30-minute cache writes: solvers $1.398674, coordination $1.167889, total $2.566563. Actual billing unavailable. Details in results/Sol-EXCELLENT-TABLEAU-session.json. Stopped after four attempts.

## 2026-10-22 10:06 — Luna-2 EXCELLENT and TABLEAU additions

- Mike requested the same four new conditions as additions to Luna-2. Added Luna-EXCELLENT-2, TABLEAU-PLAIN-2, TABLEAU-HURRY-2, and TABLEAU-SHOWOFF-2; ran only these conditions sequentially with fresh native openai.gpt-6-luna subagents and fork_turns="none". Exact saved launch prompts use the existing instructor prefix, base prompt, optional TABLEAU modifier, and common tail.
- Saved outcomes, final messages, run records, frozen answers, work, and available local transcripts; original folders retained. No corrective advice, debriefs, repairs, grading, or package installations. Previous results and collected rows preserved. HURRY has one coordinator transcription typo in its modifier (an otherwise -> anotherwise), saved in the actual launch text and recorded as a protocol deviation; no corrective feedback or replacement attempt.
- Collected timing/token records and updated RESULTS.md with completeness, designs, disclosure, and conspicuous issues. Checked archive equality and rendered available PNGs. These are individual examples, not evidence of actual Tableau usage or representative student behavior.
- Clock 09:35:57–10:06:36 CDT (30:39) through reporting snapshot; solver time 26:22. Standard-tier API-equivalent estimates, 30-minute cache writes: solvers $0.194326, coordination $1.786869, total $1.981195. Actual billing unavailable. Details in results/Luna-EXCELLENT-TABLEAU-session.json. Stopped after four attempts.
