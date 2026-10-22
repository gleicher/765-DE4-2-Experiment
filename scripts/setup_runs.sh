#!/usr/bin/env bash
# Build one fresh run folder per row of plan.csv.
# Usage: scripts/setup_runs.sh [RUNS_ROOT] [HARNESS]   (default: ./runs, all rows)
# Must be run from the experiment directory. This helper does not launch agents.
set -euo pipefail
EXP="$(pwd)"
ROOT="${1:-$EXP/runs}"
SELECT="${2:-}"
case "$SELECT" in ""|codex|claude) ;; *) echo "unknown harness: $SELECT"; exit 1;; esac
[[ -f plan.csv && -d reference ]] || { echo "run this from the experiment directory"; exit 1; }
DATA_REPO=https://github.com/uwgraphics/765Data
DATA_COMMIT=06b17de   # 2025-09-21; the 2025 data. Later commits (2026-09) are 2026 updates
mkdir -p "$ROOT"
ROOT="$(cd "$ROOT" && pwd)"
[[ "$ROOT" != "$EXP" ]] || { echo "RUNS_ROOT must be a separate folder"; exit 1; }
CACHE="$ROOT/.data-cache"
if [ ! -d "$CACHE" ]; then
  git clone -q "$DATA_REPO" "$CACHE.git"
  git -C "$CACHE.git" checkout -q "$DATA_COMMIT"
  mkdir -p "$CACHE" && (cd "$CACHE.git" && git archive HEAD) | tar -x -C "$CACHE"
  rm -rf "$CACHE.git"
fi
tail -n +2 plan.csv | while IFS=, read -r RUN_ID HARNESS MODEL PROMPT REP; do
  [ -z "$RUN_ID" ] && continue
  [ -n "$SELECT" ] && [ "$HARNESS" != "$SELECT" ] && continue
  [[ "$RUN_ID" =~ ^[A-Za-z0-9][A-Za-z0-9_-]*$ ]] || { echo "invalid run ID: $RUN_ID"; exit 1; }
  R="$ROOT/$RUN_ID"
  if [ -e "$R" ]; then echo "exists, skipping: $R"; continue; fi
  mkdir -p "$R/answers/figures" "$R/work"
  rsync -a --exclude '_to_delete' --exclude 'MANIFEST.md' reference/ "$R/reference/"
  cp -R "$CACHE" "$R/data"
  cat > "$R/AGENTS.md" <<'EOF'
# Tools and working files

Choose the tools appropriate to the task. Python is not required or preferred; R is also
installed. If you use Python, use /opt/anaconda3/envs/p314/bin/python. Do not create a virtual
environment or use another interpreter. Propose needed packages and wait for approval
before installing anything.

Node is managed by mise; do not change managers, versions, or shims. R is installed via
Homebrew with per-project packages in .Rlib/; do not relocate R or manage or modify .Rlib/.

Keep your scripts, notebooks, source files, and intermediate files in work/. Include a short
work/README.md describing the tools and how to regenerate the figures, including manual
steps. Follow the output locations in the task request.
EOF
  cp "$R/AGENTS.md" "$R/CLAUDE.md"
  echo "made $R"
done
