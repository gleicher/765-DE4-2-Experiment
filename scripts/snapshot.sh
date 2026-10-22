#!/usr/bin/env bash
# Snapshot a run's answers/ at fixed minutes after start. Started in the background by run_one.sh.
# Usage: scripts/snapshot.sh RUN_DIR SNAP_DIR
set -u
RUN="$1"; SNAP="$2"; START=$(date +%s)
for M in 10 20 40 60; do
  while [ $(( $(date +%s) - START )) -lt $(( M * 60 )) ]; do sleep 15; done
  mkdir -p "$SNAP/t$M" && cp -R "$RUN/answers/." "$SNAP/t$M/" 2>/dev/null
done
