# DE4-2 one-shot exploration (2025 assignment, 2026 agents)

*Started 2026-10-21. An informal look to inform instructional design, not a research study.*

What happens when an agent is asked to complete last year's visualization assignment?
Inspect the resulting stories, six charts, rationales, critique, and AI disclosure.
The 2025 submissions in `Assignments/2025/2025-DE4-2` provide a useful human comparison.
Mike can judge the work with the assignment rubric and decide what it implies for teaching.

## Running it

Open this folder in Codex or Claude Code and say **“go”**. `RUNBOOK.md` tells the session to
prepare fresh folders and launch assignment-solving subagents with fresh contexts using
its native tools. There is no external process launcher or configuration cleanup.
Start with one PLAIN run each for Codex, Opus, and Sonnet. Each session runs only models its
native tools support; use a Claude Code session for Claude rows and Codex for Codex rows.
Existing results are skipped. Inspect these outputs before adding prompt variants.

Agents choose their own tools: Python, R, or other installed software. **If they use Python,
they must use `p314`.** There is no preference for Python. Package additions require Mike's
approval; agents must not create alternative Python environments or change toolchains.
Each agent is asked to retain its code and working files in `work/`, alongside the final
answers and images in `answers/`.

Keep a saved submission, working files, final agent message, approximate duration, and short
notes. Save transcripts when available. Debriefs are optional; token accounting, cost
estimates, intermediate snapshots, and exhaustive command journals are not required.

## Files

| File | Purpose |
|---|---|
| `AGENTS.md`, `CLAUDE.md` | Session entry instructions and environment policy |
| `RUNBOOK.md` | The “go” workflow |
| `PROMPTS.md` | Student requests, common instructions, optional debrief |
| `plan.csv` | Initial three PLAIN runs; add rows for later attempts |
| `runs/` | Assignment folders, original answers, and working files |
| `results/` | Saved submissions, code, final messages, and brief run records |
| `runs.csv`, `RESULTS.md` | Counts and instructor-facing observations |
| `journal.md` | Short session summaries; previous history is retained |
| `reference/` | Assignment and related pages; `MANIFEST.md` lists sources |
| `scripts/` | Helpers to copy inputs, assemble prompts, and collect results |

## Accepted limits

- The references come from the current 765-25 site, not a reconstruction of the deadline.
- Some external links are not mirrored; agents may browse. Later grading material is
  reachable online.
- Fresh subagents share the runtime's tools and filesystem. This is context separation,
  not a sealed environment or a controlled comparison of models.
- Agents receive prepared files and available local tooling; that is useful context when
  comparing their outputs with student work.
- Prompt variants mix intentions. Use them to discover interesting behavior rather than
  isolate the effect of individual phrases.
