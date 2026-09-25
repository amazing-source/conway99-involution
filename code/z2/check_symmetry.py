"""Audit checks for the symmetry arguments used by the Stage-Q cubes (2026-09-22).
1. Case split: Stab(U0) (in the relabelling group 2^6 x| S_7 acting on the 42 orbits) has exactly three orbits on the other 41 orbits,
   {(1,2,1)}, the 20 orbits sharing one block with U0, the 20 orbits on blocks 3..7. This is what makes sib/one/dis exhaustive.
2. Cube orbits: the 12 stabiliser elements used by u0_rows.py (same seed) generate the whole Stab(U0, D(U0)), so the 13/149/1164
   orbit counts are exact, not upper bounds.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from u0_rows import outer, idx, N, CASES, stabilizer, act
import itertools

U0 = idx[(1, 2, 0)]
# 1. orbits of Stab(U0) on the other orbits
stab = []
for perm in itertools.permutations(range(1, 8)):
    pi = dict(zip(range(1, 8), perm))
    for r in range(64):
        F = {l for l in range(1, 7) if r >> (l - 1) & 1}
        p = act(pi, F)
        if p[U0] == U0: stab.append(p)
print("|Stab(U0)| =", len(stab))
seen = set(); orbs = []
for V in range(N):
    if V == U0 or V in seen: continue
    orb = set(int(p[V]) for p in stab); seen |= orb; orbs.append(sorted(outer[w] for w in orb))
print("orbits of Stab(U0) on the other 41 orbits: sizes", sorted(len(o) for o in orbs))
for o in orbs: print("  size %2d, contains %s" % (len(o), [t for t in o if t in CASES.values()]))
# 2. closure of the generators used by u0_rows.py
for case in ("sib", "one", "dis"):
    G = stabilizer(U0, idx[CASES[case]])
    rng = np.random.default_rng(0); gens = [G[i] for i in rng.choice(len(G), size=min(12, len(G)), replace=False)]
    ident = tuple(range(N)); H = {ident}; frontier = [ident]
    while frontier:
        nxt = []
        for h in frontier:
            for g in gens:
                c = tuple(int(g[x]) for x in h)
                if c not in H: H.add(c); nxt.append(c)
        frontier = nxt
    print("case %s: |Stab(U0,D0)| = %d, |<12 generators>| = %d -> %s" % (case, len(G), len(H), "EQUAL (orbit counts exact)" if len(H) == len(G) else "PROPER SUBGROUP"))
