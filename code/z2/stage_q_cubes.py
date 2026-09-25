"""Cubes for Stage Q: one cube per Stab(U0, D(U0))-orbit of U0-rows (representatives from u0_rows.py).

A cube fixes the whole row of U0 = (1,2,0): the 2 at D(U0), the ten 1s, zeros elsewhere, as unit literals on the primary
variables of stage_q (same numbering as the Stage-Q CNF: x = [Q>=1], y = [Q=2]). Exhaustive within a case: every Stage-Q
solution of the case has a U0-row in one of the orbits, and relabelling by an element of Stab(U0, D(U0)) maps it to a solution
whose U0-row is the representative (the case clause and all Stage-Q constraints are invariant under the relabelling group).
Usage: python stage_q_cubes.py --case sib --rows u0_rows_sib.json --out cubes_sib.txt   (one cube per line: literals, 0-terminated)
"""
import argparse, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from stage_q import primaries, CASES


def cube(row_ones, case, m=7):
    outer, X, Y, top = primaries(m)
    U0 = outer.index((1, 2, 0)); D0 = outer.index(CASES[case])
    ones = set(outer.index(tuple(o)) for o in row_ones)
    assert len(ones) == 2 * m - 4 and D0 not in ones and U0 not in ones
    lits = []
    for V in range(len(outer)):
        if V == U0: continue
        q = 2 if V == D0 else (1 if V in ones else 0)
        lits.append(X[U0, V] if q >= 1 else -X[U0, V]); lits.append(Y[U0, V] if q == 2 else -Y[U0, V])
    return lits


def decode_row(lits, m=7):
    outer, X, Y, top = primaries(m); U0 = outer.index((1, 2, 0)); pos = set(l for l in lits if l > 0); row = {}
    for V in range(len(outer)):
        if V != U0: row[outer[V]] = (X[U0, V] in pos) + (Y[U0, V] in pos)
    return row


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--case", required=True); ap.add_argument("--rows", required=True)
    ap.add_argument("--out", required=True); a = ap.parse_args()
    reps = json.load(open(a.rows)); n = 0
    with open(a.out, "w", newline="\n") as f:
        for r in reps:
            lits = cube(r["row_ones"], a.case); row = decode_row(lits)
            assert sorted(k for k, v in row.items() if v == 1) == sorted(tuple(o) for o in r["row_ones"])
            assert [k for k, v in row.items() if v == 2] == [CASES[a.case]]
            f.write(" ".join(map(str, lits)) + " 0\n"); n += 1
    print("case %s: %d cubes written to %s (each fixes %d primary literals; decode check passed)" % (a.case, n, a.out, len(lits)))
