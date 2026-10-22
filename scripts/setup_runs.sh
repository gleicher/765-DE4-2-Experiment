#!/usr/bin/env bash
# Build one fresh run folder per row of plan.csv.
# Usage: scripts/setup_runs.sh [RUNS_ROOT]   (default: ~/de4-2-runs)
# Must be run from the experiment directory. RUNS_ROOT must NOT be inside it.
set -euo pipefail
EXP="$(pwd)"
ROOT="${1:-$HOME/de4-2-runs}"
DATA_REPO=https://github.com/uwgraphics/765Data
DATA_COMMIT=06b17de   # last commit before the 2025 DE4-2 deadline (2025-09-21); later commits are 2026 updates
case "$ROOT" in "$EXP"*) echo "RUNS_ROOT is inside the experiment dir; refusing"; exit 1;; esac
mkdir -p "$ROOT"
CACHE="$ROOT/.data-cache"
if [ ! -d "$CACHE" ]; then
  git clone -q "$DATA_REPO" "$CACHE.git"
  git -C "$CACHE.git" checkout -q "$DATA_COMMIT"
  mkdir -p "$CACHE" && (cd "$CACHE.git" && git archive HEAD) | tar -x -C "$CACHE"
  rm -rf "$CACHE.git"
fi
tail -n +2 plan.csv | while IFS=, read -r RUN_ID HARNESS MODEL PROMPT REP; do
  [ -z "$RUN_ID" ] && continue
  R="$ROOT/$RUN_ID"
  if [ -e "$R" ]; then echo "exists, skipping: $R"; continue; fi
  mkdir -p "$R/answers/figures"
  rsync -a --exclude '_to_delete' --exclude 'MANIFEST.md' reference/ "$R/reference/"
  cp -R "$CACHE" "$R/data"
  echo "made $R"
done
