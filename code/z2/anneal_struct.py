"""Structured simulated annealing for the involution branch (move space suggested 2026-09-21).
State: D = perfect matching on the 42 orbits (Q=2 entries), G = 10-regular graph on the 42 orbits, edge-disjoint from D (Q=1 entries),
sign[U,V] in {0,1} for each G-edge (0: u~v i.e. (a,b)=(1,0); 1: u~sv i.e. (a,b)=(0,1)). (R) and (D) hold by construction.
Moves: 2-switch on G (degree-preserving, avoiding D and duplicates), D-switch (two D-edges re-paired, avoiding G), sign flip.
Energy = violations of (I) + (P) only. Energy 0 => Conway 99-graph with an involution (lifted and verified exactly).
Usage: python anneal_struct.py --seed 1 --minutes 10
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
sUV = np.array([[len(rep[U] & rep[V]) for V in range(N)] for U in range(N)])
sUtV = np.array([[len(rep[U] & trep[V]) for V in range(N)] for U in range(N)])
Itgt = np.array([[1 if (c in rep[U] or (c[0], 1 - c[1]) in rep[U]) else 2 for c in inner] for U in range(N)])
Ia = np.array([[1 if c in rep[V] else 0 for c in inner] for V in range(N)])
Ib = np.array([[1 if c in trep[V] else 0 for c in inner] for V in range(N)])
offd = ~np.eye(N, dtype=bool)

def energy(A, B):
    cnt = A @ Ia + B @ Ib
    eI = np.abs(cnt - Itgt).sum()
    same = A @ A + B @ B; cross = A @ B + B @ A
    eP = np.abs((same + A - (2 - sUV))[offd]).sum() + np.abs((cross + B - (2 - sUtV))[offd]).sum()
    return int(eI + eP), (int(eI), int(eP))

def random_state(rng, shuffles=20000):
    """Perfect matching D and 10-regular G disjoint from D: start from a circulant (U ~ U±1..±5 mod 42, D pairs U with U+21),
    relabel randomly, then randomise G by many random 2-switches that avoid D and duplicates."""
    perm = list(range(N)); rng.shuffle(perm)
    D = {}
    for U in range(21): D[perm[U]] = perm[U + 21]; D[perm[U + 21]] = perm[U]
    G = set()
    for U in range(N):
        for d in range(1, 6):
            V = (U + d) % N; G.add((min(perm[U], perm[V]), max(perm[U], perm[V])))
    assert len(G) == 210
    edges = list(G)
    for _ in range(shuffles):
        e1, e2 = rng.sample(edges, 2); (U, V), (W, X) = e1, e2
        if rng.random() < 0.5: W, X = X, W
        n1, n2 = (min(U, W), max(U, W)), (min(V, X), max(V, X))
        if U == W or V == X or n1 in G or n2 in G or D[U] == W or D[V] == X: continue
        G.remove(e1); G.remove(e2); G.add(n1); G.add(n2)
        edges = list(G)
    return D, G

def matrices(D, G, sign):
    A = np.zeros((N, N), dtype=int); B = np.zeros((N, N), dtype=int)
    for U, V in D.items(): A[U, V] = B[U, V] = 1
    for (U, V) in G:
        if sign[(U, V)]: B[U, V] = B[V, U] = 1
        else: A[U, V] = A[V, U] = 1
    return A, B

def run(seed, minutes, T0=1.5, T1=0.1):
    rng = random.Random(seed)
    D, G = random_state(rng); sign = {e: rng.randint(0, 1) for e in G}
    A, B = matrices(D, G, sign); E, comp = energy(A, B); best = E
    t0 = time.time(); total = minutes * 60; it = 0; acc = 0
    def propose():
        r = rng.random()
        if r < 0.45:   # 2-switch on G
            e1, e2 = rng.sample(sorted(G), 2); (U, V), (W, X) = e1, e2
            if rng.random() < 0.5: W, X = X, W
            new1, new2 = (min(U, W), max(U, W)), (min(V, X), max(V, X))
            if U == W or V == X or new1 in G or new2 in G or D[U] == W or D[V] == X: return None
            s1, s2 = sign[e1], sign[e2]
            def do():
                G.remove(e1); G.remove(e2); del sign[e1]; del sign[e2]
                G.add(new1); G.add(new2); sign[new1] = s1; sign[new2] = s2
            def undo():
                G.remove(new1); G.remove(new2); del sign[new1]; del sign[new2]
                G.add(e1); G.add(e2); sign[e1] = s1; sign[e2] = s2
            return do, undo
        elif r < 0.6:  # D-switch
            U, W = rng.sample(range(N), 2); V, X = D[U], D[W]
            if V == W: return None
            if rng.random() < 0.5: W, X = X, W
            if (min(U, W), max(U, W)) in G or (min(V, X), max(V, X)) in G: return None
            old = dict(D)
            def do(): D[U] = W; D[W] = U; D[V] = X; D[X] = V
            def undo(): D.update(old)
            return do, undo
        else:          # sign flip
            e = rng.choice(sorted(G))
            def do(): sign[e] ^= 1
            return do, do
    Gsorted_cache = None
    while time.time() - t0 < total:
        it += 1
        mv = propose()
        if mv is None: continue
        do, undo = mv; do()
        A, B = matrices(D, G, sign); E2, comp2 = energy(A, B)
        frac = (time.time() - t0) / total; T = T0 * (T1 / T0) ** frac
        if E2 <= E or rng.random() < math.exp(-(E2 - E) / T):
            E, comp = E2, comp2; acc += 1
            if E < best:
                best = E; print("seed %d it %d t=%.0fs E=%d (I=%d,P=%d)" % (seed, it, time.time() - t0, E, *comp), flush=True)
                if E == 0: break
        else:
            undo()
    out = {"seed": seed, "iterations": it, "accepted": acc, "best_energy": best, "final_energy": E, "components": comp, "wall": time.time() - t0}
    if E == 0:
        A, B = matrices(D, G, sign)
        _, _, outer_, rep_, trep_, Av, Bv = build(7, "none"); model = []
        for U in range(N):
            for V in range(U + 1, N):
                model.append(Av[U, V] if A[U, V] else -Av[U, V]); model.append(Bv[U, V] if B[U, V] else -Bv[U, V])
        Mx, ok = lift(7, outer_, rep_, trep_, Av, Bv, model); out["lift_verified"] = bool(ok)
        np.savetxt("STRUCT_SOLUTION_seed%d.txt" % seed, Mx, fmt="%d")
    json.dump(out, open("anneal_struct_seed%d.json" % seed, "w")); print(json.dumps(out))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int, default=1); ap.add_argument("--minutes", type=float, default=10)
    ap.add_argument("--T0", type=float, default=1.5); ap.add_argument("--T1", type=float, default=0.1)
    a = ap.parse_args(); run(a.seed, a.minutes, a.T0, a.T1)
