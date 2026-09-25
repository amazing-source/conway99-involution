#!/bin/bash
# Run Stage-Q cubes with kissat inside the satbox-proof image (kissat 4.0.4 + drat-trim).
# Usage (inside the container, /work = directory with q_<case>.cnf and cubes_<case>.txt):
#   bash cube_run.sh <case> <first_line> <last_line> <time_limit_s> <proof:0|1> <results_file>
# For each cube line: base CNF + unit clauses -> kissat (statistics on). With proof=1 an UNSAT cube writes a binary DRAT proof,
# drat-trim checks it at once, and only the check log and the proof's sha256 are kept (the proof itself is deleted).
# One result line per cube: case idx verdict kissat_exit seconds conflicts [drat=VERIFIED|FAILED sha256]
set -u
case=$1; first=$2; last=$3; T=$4; proof=$5; out=$6
base=/work/q_$case.cnf; cubes=/work/cubes_$case.txt
read -r _ _ V C < <(head -1 "$base")
mkdir -p /work/cubelogs
for i in $(seq "$first" "$last"); do
  line=$(sed -n "${i}p" "$cubes"); [ -z "$line" ] && continue
  k=$(echo "$line" | wc -w); k=$((k - 1))
  cnf=/tmp/cube_${case}_$i.cnf
  { echo "p cnf $V $((C + k))"; tail -n +2 "$base"; for l in $line; do [ "$l" != 0 ] && echo "$l 0"; done; } > "$cnf"
  log=/work/cubelogs/${case}_$i.log; t0=$(date +%s)
  if [ "$proof" = 1 ]; then kissat --time="$T" "$cnf" "/tmp/p_${case}_$i.drat" > "$log" 2>&1; ex=$?
  else kissat --time="$T" "$cnf" > "$log" 2>&1; ex=$?; fi
  t1=$(date +%s); v=$(grep -m1 -E "^s " "$log" | cut -c3-); conf=$(grep -m1 -E "^c conflicts:" "$log" | awk '{print $3}')
  extra=""
  if [ "$proof" = 1 ] && [ "$ex" = 20 ]; then
    h=$(sha256sum "/tmp/p_${case}_$i.drat" | cut -c1-64)
    drat-trim "$cnf" "/tmp/p_${case}_$i.drat" > "/work/cubelogs/${case}_$i.drat-trim.log" 2>&1
    if tr -d '\r' < "/work/cubelogs/${case}_$i.drat-trim.log" | grep -q "^s VERIFIED"; then extra="drat=VERIFIED $h"; else extra="drat=FAILED $h"; fi
  fi
  rm -f "$cnf" "/tmp/p_${case}_$i.drat"
  echo "$case $i ${v:-NONE} $ex $((t1 - t0)) ${conf:-?} $extra" >> "$out"
done
