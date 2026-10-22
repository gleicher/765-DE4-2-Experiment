#!/bin/sh
# Regenerate every figure in answers/figures/ (and the CSVs in work/intermediate/).
set -e
PY=/opt/anaconda3/envs/p314/bin/python
cd "$(dirname "$0")"
$PY q1_data.py > /dev/null
$PY q2_data.py > /dev/null
$PY q4_data.py > /dev/null
for f in fig1a_setback_small_multiples.py fig1b_setback_scatter.py \
         fig2a_components_bars.py fig2b_components_heatmap.py \
         fig3_education_gaps.py fig4_50_to_70.py; do
  echo "$f"; $PY "$f" > /dev/null
done
