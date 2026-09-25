"""Rows of U0 = (1,2,0) in Stage Q, per case of D(U0), and their orbits under Stab(U0, D(U0)).

Orbits of labels are (pair {i,j}, e) with e = s_i xor s_j; the relabelling group acts by block permutations (e kept) and block
flips (flip of block l toggles e on every pair containing l; flipping all 7 blocks = sigma acts trivially), order 7! * 2^6 = 322 560.
A U0-row = Q[U0, .] with one entry 2 at D(U0), k-4 = 10 entries 1, block sums 2 on blocks of U0 and 4 elsewhere (row constraints only).
Prints the number of rows and of Stab(U0,D0)-orbits; writes one representative per orbit to u0_rows_<case>.json.
"""
import itertools, json, os, sys
import numpy as np
from collections import deque

m = 7
outer = [(i, j, e) for i in range(1, m + 1) for j in range(i + 1, m + 1) for e in (0, 1)]
idx = {o: t for t, o in enumerate(outer)}; N = len(outer)
CASES = {"sib": (1, 2, 1), "one": (1, 3, 0), "dis": (3, 4, 0)}


def act(pi, F):
    """Permutation of orbit indices for block permutation pi (dict 1..m -> 1..m) then flip set F (set of blocks)."""
    p = np.empty(N, dtype=np.int64)
    for t, (i, j, e) in enumerate(outer):
        a, b = sorted((pi[i], pi[j])); e2 = e ^ (a in F) ^ (b in F)
        p[t] = idx[(a, b, e2)]
    return p


def stabilizer(U, D):
    els = []
    for perm in itertools.permutations(range(1, m + 1)):
        pi = dict(zip(range(1, m + 1), perm))
        for r in range(0, 2 ** (m - 1)):                          # flip sets modulo the all-flip: those not containing block 7
            F = {l for l in range(1, m) if r >> (l - 1) & 1}
            p = act(pi, F)
            if p[U] == U and p[D] == D: els.append(p)
    return els


def rows(case):
    U0 = idx[(1, 2, 0)]; D0 = idx[CASES[case]]
    need = {l: (2 if l in (1, 2) else 4) for l in range(1, m + 1)}
    for l in outer[D0][:2]: need[l] -= 2
    cand = [V for V in range(N) if V not in (U0, D0) and all(need[l] > 0 for l in outer[V][:2])]
    out = []
    def rec(start, chosen, need):
        if len(chosen) == 10:
            if all(v == 0 for v in need.values()): out.append(tuple(chosen))
            return
        if sum(need.values()) != 2 * (10 - len(chosen)): return
        for t in range(start, len(cand)):
            V = cand[t]; i, j, _ = outer[V]
            if need[i] > 0 and need[j] > 0:
                need[i] -= 1; need[j] -= 1; chosen.append(V)
                rec(t + 1, chosen, need)
                chosen.pop(); need[i] += 1; need[j] += 1
    rec(0, [], dict(need))
    return U0, D0, out


def main():
    res = {}
    for case in ("sib", "one", "dis"):
        U0, D0, R = rows(case)
        G = stabilizer(U0, D0)
        key = {r: t for t, r in enumerate(R)}; seen = [False] * len(R); reps = []
        rng = np.random.default_rng(0); gens = [G[i] for i in rng.choice(len(G), size=min(12, len(G)), replace=False)]
        for t0, r0 in enumerate(R):
            if seen[t0]: continue
            seen[t0] = True; orb = 1; q = deque([r0])
            while q:
                r = q.popleft()
                for g in gens:
                    s = tuple(sorted(int(g[v]) for v in r)); u = key[s]
                    if not seen[u]: seen[u] = True; orb += 1; q.append(s)
            reps.append({"row_ones": [outer[v] for v in r0], "orbit_size": orb})
        tot = sum(x["orbit_size"] for x in reps)
        print("case %s: D0=%s |Stab(U0,D0)|=%d rows=%d orbits=%d (orbit sizes sum %d; sizes %s)" % (
            case, CASES[case], len(G), len(R), len(reps), tot, sorted(x["orbit_size"] for x in reps)), flush=True)
        res[case] = reps
        json.dump(reps, open("u0_rows_%s.json" % case, "w"))
    return res


if __name__ == "__main__":
    main()
