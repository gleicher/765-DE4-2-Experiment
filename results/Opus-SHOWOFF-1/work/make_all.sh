#!/bin/sh
# Regenerate every figure in answers/figures/ (run from anywhere).
set -e
cd "$(dirname "$0")"
PY=/opt/anaconda3/envs/p314/bin/python
for s in fig1a_gap_path.py fig1b_gap_heatmap.py fig2a_components_bars.py fig2b_county_quadrants.py fig3_milestones.py fig4_two_recessions.py; do
  $PY "$s"
done
