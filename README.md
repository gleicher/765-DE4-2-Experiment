# 43 — DE4-2 one-shot experiment (2025 assignment, 2026 agents)

*Built 2026-10-21. Supersedes the prompt draft in `../42-de4-2-oneshot-prompt.md`.
Context: `../40-ai-resilience.md`, `../41-de2-ai-corpus.md`.*

## Question

What does a student get if they hand the 2025 DE4-2 assignment to a current agent, and how
does that differ from what 2025 students actually turned in? 2025 students worked before
agents were usable design partners, so their DE4-2 submissions (already in the grading tool,
`Assignments/2025/2025-DE4-2`) are a human baseline on the identical prompt and data.

What we want out of it:

1. An **agent-vs-student failure taxonomy** — agents seem to fail "upward" (ambitious designs
   seen in published work, e.g. connected scatterplots; longer text), students with defaults.
2. Whether the **rubric and codebook separate** one-shot agent work from strong student work,
   and what grade a one-shot earns (this sizes the "agent's share" in `40-`).
3. How much **student prompt style** matters (hurried vs careful vs concealing vs show-off).
4. **Cost and effort** of a one-shot, including a quality-vs-time curve from snapshots.
5. What agents write in the **AI-disclosure** answer (Canvas Q20) when they believe they're
   helping a student.

## Design

- **Prompts:** five student-voiced requests (`PROMPTS.md`), none mentioning an experiment.
  SHOWOFF is a separate arm, not part of the human-vs-agent comparison.
- **Models:** Claude Opus and Sonnet (Claude Code), plus Codex (model set in `plan.csv`).
  One rep per cell to start (15 runs); add reps where a cell looks interesting.
- **Context:** the assignment and its linked pages as markdown in `reference/`, the 2025 data
  in `data/`. Web access stays on (students can see past years too); runs are asked to list
  pages they open, and logs are checked.
- **No diversity or quality instructions.** Convergence across runs is part of what's measured.
- **Isolation:** each run is a fresh headless session whose working folder contains only
  `reference/`, `data/`, `answers/`. Run folders live outside this directory.
- **Effort cap:** 60 minutes wall-clock, enforced from outside and not told to the agent.
  `answers/` is snapshotted at 10, 20, 40, 60 minutes.
- **Freeze, then debrief:** after Turn 1 ends, `answers/` is copied (that copy is the
  submission); then the same session gets the debrief turn, which reveals the experiment.
- **Cost:** from harness output (Claude Code's JSON result; Codex's JSON event stream),
  converted to API-equivalent dollars. Self-reports in the debrief are secondary.

## Files

| File | What |
|---|---|
| `RUNBOOK.md` | The operating instructions — "read RUNBOOK.md and go" |
| `PROMPTS.md` | Verbatim prompts; `scripts/get_prompt.py` reads them from here |
| `plan.csv` | One row per run (id, harness, model, prompt, rep) |
| `runs.csv` | Results, one row per run, filled by `scripts/collect.py` |
| `reference/` | What each run gets; `MANIFEST.md` documents sources and exclusions |
| `scripts/` | `setup_runs.sh`, `run_one.sh`, `snapshot.sh`, `get_prompt.py`, `collect.py` |

## Known limits

- The `reference/` pages are the current 765-25 site, not reconstructed to the deadline.
- Three external pages linked from the assignment (the 2024 rubric and codes, a 2021 variant)
  are not mirrored; a browsing run can open them.
- The post-grading codes page (`765-25/posts/de4-codes/`) is reachable online.
- Agents can see sibling run folders if they wander; check logs for reads outside the run folder.
- Comparing to 2025 students requires pseudonymizing the 2025 submissions first (`40-` §Privacy).
