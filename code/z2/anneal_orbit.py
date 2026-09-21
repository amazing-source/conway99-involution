"""Incomplete (heuristic) search in the involution branch: simulated annealing on the orbit-level model.
State: bits a[U,V], b[U,V] for U<V (1722 bits). Energy = total violation of (R),(D),(I),(P) (see orbit_sat.py).
Energy 0 <=> a Conway 99-graph with an involution (then lifted and verified exactly).
Usage: python anneal_orbit.py --seed 1 --hours 8
"""
import argparse, json, math, random, time
import numpy as np
from orbit_sat import build, lift

m = 7; k = 14
outer = [(i, j, e) for i in range(1, m + 1) for j in range(i + 1, m + 1) for e in (0, 1)]
N = len(outer)
rep = [frozenset([(i, 0), (j, e)]) for (i, j, e) in outer]
trep = [frozenset([(i, 1), (j, 1 - e)]) for (i, j, e) in outer]
inner = [(i, s) for i in range(1, m + 1) for s in (0, 1)]
# targets
sUV = np.array([[len(rep[U] & rep[V]) for V in range(N)] for U in range(N)])      # |u ∩ v|
sUtV = np.array([[len(rep[U] & trep[V]) for V in range(N)] for U in range(N)])   # |u ∩ tv|
Itgt = np.zeros((N, 14), dtype=int); Ia = np.zeros((N, 14), dtype=int); Ib = np.zeros((N, 14), dtype=int)
for U in range(N):
    for ci, c in enumerate(inner):
        Itgt[U, ci] = 1 if (c in rep[U] or (c[0], 1 - c[1]) in rep[U]) else 2
for V in range(N):
    for ci, c in enumerate(inner):
        Ia[V, ci] = 1 if c in rep[V] else 0; Ib[V, ci] = 1 if c in trep[V] else 0

def energy(A, B):
    """A,B symmetric 0/1 (N x N) with zero diagonal. Returns total violation and components."""
    Q = A + B
    eR = np.abs(Q.sum(1) - (k - 2)).sum()
    eD = np.abs((A * B).sum(1) - 1).sum()
    cnt = A @ Ia + B @ Ib                       # neighbours of u containing c
    eI = np.abs(cnt - Itgt).sum()
    same = A @ A + B @ B; cross = A @ B + B @ A  # (P): same[U,V] + A[U,V] = 2 - s ; cross + B = 2 - s'
    offd = ~np.eye(N, dtype=bool)
    eP = np.abs((same + A - (2 - sUV))[offd]).sum() + np.abs((cross + B - (2 - sUtV))[offd]).sum()
    return int(eR + eD + eI + eP), (int(eR), int(eD), int(eI), int(eP))

def run(seed, hours, T0=2.0, T1=0.15):
    rng = random.Random(seed)
    A = np.zeros((N, N), dtype=int); B = np.zeros((N, N), dtype=int)
    # random start: for each U pick 12 (a or b) entries
    pairs = [(U, V) for U in range(N) for V in range(U + 1, N)]
    for (U, V) in rng.sample(pairs, 250):
        if rng.random() < 0.5: A[U, V] = A[V, U] = 1
        else: B[U, V] = B[V, U] = 1
    E, comp = energy(A, B); best = E; t0 = time.time(); it = 0; T = T0
    total = hours * 3600
    while time.time() - t0 < total:
        it += 1
        U, V = rng.choice(pairs); M = A if rng.random() < 0.5 else B
        M[U, V] ^= 1; M[V, U] ^= 1
        E2, comp2 = energy(A, B)
        frac = (time.time() - t0) / total; T = T0 * (T1 / T0) ** frac
        if E2 <= E or rng.random() < math.exp(-(E2 - E) / T):
            E, comp = E2, comp2
            if E < best:
                best = E; print("seed %d it %d t=%.0fs E=%d %s" % (seed, it, time.time() - t0, E, comp), flush=True)
                if E == 0: break
        else:
            M[U, V] ^= 1; M[V, U] ^= 1
    out = {"seed": seed, "iterations": it, "best_energy": best, "final_energy": E, "components": comp, "wall": time.time() - t0}
    if E == 0:
        # lift and verify exactly
        _, _, outer_, rep_, trep_, Av, Bv = build(7, "none")
        model = []
        for U in range(N):
            for V in range(U + 1, N):
                model.append(Av[U, V] if A[U, V] else -Av[U, V]); model.append(Bv[U, V] if B[U, V] else -Bv[U, V])
        Mx, ok = lift(7, outer_, rep_, trep_, Av, Bv, model); out["lift_verified"] = bool(ok)
        np.savetxt("ANNEAL_SOLUTION_seed%d.txt" % seed, Mx, fmt="%d")
    json.dump(out, open("anneal_seed%d.json" % seed, "w")); print(json.dumps(out))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int, default=1); ap.add_argument("--hours", type=float, default=8)
    a = ap.parse_args(); run(a.seed, a.hours)
