#!/usr/bin/env bash
# Run one row of plan.csv: Turn 1 (student prompt) with a 60-minute cap, freeze, Turn 2 (debrief).
# Usage: scripts/run_one.sh RUN_ID [RUNS_ROOT] [RESULTS_ROOT]
#
# ASSUMPTIONS TO CHECK BEFORE THE FIRST RUN (run `claude --help`, `codex exec --help`):
#   claude: -p, --model, --output-format json, --permission-mode, --resume <session_id>
#   codex:  exec, --model, --json, sandbox/approval flags, network access, `exec resume`
# Fix the two harness blocks below if any flag differs. Everything else is harness-neutral.
set -euo pipefail
EXP="$(pwd)"
RUN_ID="$1"; ROOT="${2:-$HOME/de4-2-runs}"; RES="${3:-$HOME/de4-2-results}"
LINE=$(grep "^$RUN_ID," plan.csv) || { echo "no such run"; exit 1; }
IFS=, read -r _ HARNESS MODEL PROMPT REP <<< "$LINE"
R="$ROOT/$RUN_ID"; O="$RES/$RUN_ID"; mkdir -p "$O"
STUDENT=$(python3 scripts/get_prompt.py "$PROMPT")
DEBRIEF=$(python3 scripts/get_prompt.py DEBRIEF)
CAP=3600
# Portable timestamp and timeout (macOS has no GNU `timeout` or `date -I`). Cap exit code: 142.
now() { python3 -c "import datetime;print(datetime.datetime.now().astimezone().isoformat())"; }
capped() { perl -e 'alarm shift; exec @ARGV' "$@"; }

cd "$R"
now > "$O/start.txt"
"$EXP/scripts/snapshot.sh" "$R" "$O/snapshots" & SNAP_PID=$!

case "$HARNESS" in
  claude)
    set +e
    capped $CAP claude -p "$STUDENT" --model "$MODEL" --output-format json \
      --permission-mode bypassPermissions > "$O/turn1.json" 2> "$O/turn1.err"
    echo $? > "$O/turn1.exit"; set -e
    SESSION=$(python3 -c "import json;print(json.load(open('$O/turn1.json')).get('session_id',''))" 2>/dev/null || true)
    ;;
  codex)
    set +e
    capped $CAP codex exec --model "$MODEL" --json --full-auto "$STUDENT" > "$O/turn1.jsonl" 2> "$O/turn1.err"
    echo $? > "$O/turn1.exit"; set -e
    SESSION=$(python3 -c "
import json
for l in open('$O/turn1.jsonl'):
    try: e=json.loads(l)
    except: continue
    s=e.get('session_id') or e.get('thread_id') or (e.get('msg') or {}).get('session_id')
    if s: print(s); break" 2>/dev/null || true)
    ;;
esac
now > "$O/end.txt"
kill $SNAP_PID 2>/dev/null || true

# Freeze: this copy is the submission.
cp -R "$R/answers" "$O/frozen"

# Debrief (Turn 2) in the same session.
if [ -n "${SESSION:-}" ]; then
  case "$HARNESS" in
    claude) claude -p "$DEBRIEF" --resume "$SESSION" --model "$MODEL" --output-format json \
              --permission-mode bypassPermissions > "$O/turn2.json" 2> "$O/turn2.err" || true ;;
    codex)  codex exec resume "$SESSION" --json --full-auto "$DEBRIEF" > "$O/turn2.jsonl" 2> "$O/turn2.err" || true ;;
  esac
  cp -R "$R/debrief" "$O/debrief" 2>/dev/null || true
else
  echo "no session id captured; debrief skipped" > "$O/turn2.skipped"
fi
echo "$SESSION" > "$O/session_id.txt"
echo "done: $RUN_ID -> $O"
