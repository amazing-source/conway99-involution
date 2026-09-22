"""Strong positive control for the involution model (added 2026-09-22 by the audit, see notes/AUDIT_2026-09-22.md).

The k=4 control (m=2) of orbit_sat.py has only 3 primary variables and the k=6 control is a known non-existence,
so neither exercises the model. A real, non-trivial instance of the SAME problem family exists:
the Berlekamp-van Lint-Seidel graph srg(243,22,1,2) (Cayley graph on F_3^5, connection set = +-columns of a
parity-check matrix of the ternary Golay code), with the involution x -> -x, which fixes only 0.
This is exactly the m=11 (k=22) instance of orbit_sat.py.

Default mode (light, < 2 min, ~1 GB RAM): builds the graph, checks the rigidity lemmas, builds the orbit table (a,b)
exactly as orbit_sat.py defines it, checks (R),(D),(I),(P), the Q-only equations, the signed (S) equations, and the
general-k analogues of the dossier's spectral / F2-rank statements.
--cnf mode (HEAVY, lab machine only: m=11 CNF has ~12.6 M variables / 28.3 M clauses, needs ~16-20 GB RAM):
feeds the planted solution to orbit_sat.build(11) as assumptions -> must be SAT and lift; flipping a primary bit -> UNSAT.
Usage: python control_bvls.py            (light)
       python control_bvls.py --cnf      (lab only)
"""
import argparse, itertools, json, os, sys, tempfile, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def nullspace_gf3(G):
    G = G.copy() % 3; r, c = G.shape; piv = []; row = 0
    for col in range(c):
        p = next((i for i in range(row, r) if G[i, col]), None)
        if p is None: continue
        G[[row, p]] = G[[p, row]]; G[row] = (G[row] * G[row, col]) % 3   # 1^-1 = 1, 2^-1 = 2 in F_3
        for i in range(r):
            if i != row and G[i, col]: G[i] = (G[i] - G[i, col] * G[row]) % 3
        piv.append(col); row += 1
        if row == r: break
    free = [j for j in range(c) if j not in piv]; basis = []
    for f in free:
        v = np.zeros(c, dtype=int); v[f] = 1
        for i, p in enumerate(piv): v[p] = (-G[i, f]) % 3
        basis.append(v)
    return np.array(basis)


def bvls():
    g = np.array([2, 0, 1, 2, 1, 1])                 # generator polynomial of the [11,6] ternary Golay (QR) code, low -> high
    G = np.zeros((6, 11), dtype=int)
    for s in range(6): G[s, s:s + 6] = g
    H = nullspace_gf3(G); assert H.shape == (5, 11) and not ((G @ H.T) % 3).any()
    cols = [tuple(H[:, i]) for i in range(11)]
    neg = lambda v: tuple((-np.array(v)) % 3)
    S = set(cols) | set(neg(c) for c in cols); assert len(S) == 22
    V = list(itertools.product(range(3), repeat=5)); ix = {v: t for t, v in enumerate(V)}
    A = np.zeros((243, 243), dtype=np.int64)
    for v in V:
        for s in S: A[ix[v], ix[tuple((np.array(v) + s) % 3)]] = 1
    return A, V, ix, cols, neg


def rank_mod(M, p):
    M = M.copy() % p; r = 0; rows, cols = M.shape
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i, c]), None)
        if piv is None: continue
        M[[r, piv]] = M[[piv, r]]; M[r] = (M[r] * pow(int(M[r, c]), -1, p)) % p
        for i in range(rows):
            if i != r and M[i, c]: M[i] = (M[i] - M[i, c] * M[r]) % p
        r += 1
    return r


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cnf", action="store_true"); a = ap.parse_args()
    A, V, ix, cols, neg = bvls()
    n, k, m = 243, 22, 11
    assert np.array_equal(A @ A + A - (k - 2) * np.eye(n, dtype=np.int64), 2 * np.ones((n, n), dtype=np.int64))
    print("BvLS: srg(243,22,1,2) identity holds")
    P = np.zeros((n, n), dtype=np.int64)
    for v in V: P[ix[v], ix[neg(v)]] = 1
    assert np.array_equal(P @ A, A @ P) and int(np.trace(P)) == 1
    print("x -> -x: automorphism with exactly 1 fixed point")
    x = ix[(0,) * 5]; inner = {}
    for i, c in enumerate(cols): inner[ix[c]] = (i + 1, 0); inner[ix[neg(c)]] = (i + 1, 1)
    assert all(A[ix[c], ix[neg(c)]] == 1 for c in cols)          # blocks {h_i,-h_i} are the edges of N(x) = 11 K2; t = flip
    label = {}
    for v in range(n):
        if v == x or v in inner: continue
        nb = [inner[w] for w in np.flatnonzero(A[v]) if w in inner]
        assert len(nb) == 2 and nb[0][0] != nb[1][0]
        label[frozenset(nb)] = v
    outer = [(i, j, e) for i in range(1, m + 1) for j in range(i + 1, m + 1) for e in (0, 1)]
    rep = [frozenset([(i, 0), (j, e)]) for (i, j, e) in outer]
    trep = [frozenset([(i, 1), (j, 1 - e)]) for (i, j, e) in outer]
    N = len(outer)
    assert all(ix[neg(V[label[rep[U]]])] == label[trep[U]] for U in range(N))
    assert all(A[label[rep[U]], label[trep[U]]] == 0 for U in range(N))
    print("rigidity lemmas: t = flip on N(x); no outer vertex adjacent to its image")
    Am = np.array([[A[label[rep[U]], label[rep[W]]] if U != W else 0 for W in range(N)] for U in range(N)])
    Bm = np.array([[A[label[rep[U]], label[trep[W]]] if U != W else 0 for W in range(N)] for U in range(N)])
    inl = [(i, s) for i in range(1, m + 1) for s in (0, 1)]
    sUV = np.array([[len(rep[U] & rep[W]) for W in range(N)] for U in range(N)])
    sUtV = np.array([[len(rep[U] & trep[W]) for W in range(N)] for U in range(N)])
    Ia = np.array([[1 if c in rep[W] else 0 for c in inl] for W in range(N)])
    Ib = np.array([[1 if c in trep[W] else 0 for c in inl] for W in range(N)])
    Itgt = np.array([[1 if (c in rep[U] or (c[0], 1 - c[1]) in rep[U]) else 2 for c in inl] for U in range(N)])
    offd = ~np.eye(N, dtype=bool)
    eR = int((Am + Bm).sum(1).__ne__(k - 2).sum()); eD = int((Am * Bm).sum(1).__ne__(1).sum())
    eI = int(((Am @ Ia + Bm @ Ib) != Itgt).sum())
    eP = int(((Am @ Am + Bm @ Bm + Am - (2 - sUV)) != 0)[offd].sum() + ((Am @ Bm + Bm @ Am + Bm - (2 - sUtV)) != 0)[offd].sum())
    print("orbit model (R,D,I,P) violations:", eR, eD, eI, eP)
    assert (eR, eD, eI, eP) == (0, 0, 0, 0)
    # quotients
    Q = Am + Bm; Sg = Am - Bm
    C = np.array([[1 if l == i else ((-1 if e else 1) if l == j else 0) for l in range(1, m + 1)] for (i, j, e) in outer])
    Nb = np.abs(C); Sh = Nb @ Nb.T; Gm = C @ C.T; J = np.ones((N, N), dtype=np.int64); I = np.eye(N, dtype=np.int64)
    D = (Q == 2).astype(int)
    assert (D.sum(1) == 1).all() and np.array_equal(D, D.T); print("D is a perfect matching on the", N, "outer orbits")
    assert np.array_equal(Q @ Q + Q, (k - 2) * I + 4 * J - Sh) and np.array_equal(Nb.T @ Q, 4 * np.ones((m, N), dtype=int) - 2 * Nb.T)
    print("Q-only equations hold: Q^2+Q = (k-2)I+4J-Sh ; Nb^T Q = 4J-2Nb^T")
    assert np.array_equal(C.T @ Sg, np.zeros((m, N), dtype=int)) and np.array_equal(Sg @ Sg + Sg, (k - 2) * I - Gm)
    print("signed equations hold: C^T S_out = 0 ; S_out^2+S_out = (k-2)I-G")
    r_, s_ = 4, -5                                      # eigenvalues of srg(243,22,1,2)
    # general-k analogue of the dossier's Spec(Q_out): {k-2, (-2)^(m-1), r^b, s^c}, b,c from tr Q_out = 0
    rest = N - m; b = ((2 * (m - 1) - (k - 2)) - s_ * rest) // (r_ - s_); c = rest - b
    pred = sorted([k - 2] + [-2] * (m - 1) + [r_] * b + [s_] * c)
    got = sorted(np.round(np.linalg.eigvalsh(Q.astype(float))).astype(int).tolist())
    print("Spec(Q_out) = predicted {%d, (-2)^%d, %d^%d, (%d)^%d}:" % (k - 2, m - 1, r_, b, s_, c), got == pred)
    Sfull = np.block([[-np.eye(m, dtype=int), C.T], [C, Sg]])
    assert np.array_equal(Sfull @ Sfull + Sfull, (k - 2) * np.eye(m + N, dtype=int))
    f = (-m - s_ * (m + N)) // (r_ - s_)                # tr S = -m
    rk2 = rank_mod(Sfull, 2); exp2 = f if r_ % 2 else (m + N - f)
    print("rank_F2(S) =", rk2, "(predicted", exp2, ") ; rank_F2(Gamma1 + Nb Nb^T) =", rank_mod((Q % 2) + Sh, 2), "(predicted", exp2 - m, ")")
    nonedges = n * (n - 1 - k) // 2
    print("reminder: in ANY srg(n,k,1,2) the number of induced C4 is the constant non-edges/2 (here %d),"
          " so a parity statement about it carries no information" % (nonedges // 2))
    if not a.cnf:
        print("light control PASSED (run with --cnf on the lab machine for the full CNF check)"); return
    from orbit_sat import build, lift
    from pysat.solvers import Solver
    t0 = time.time(); cnf, pool, outer_, rep_, trep_, Av, Bv = build(m, "none")
    print("m=11 CNF: vars=%d clauses=%d build=%.0fs" % (pool.top, len(cnf.clauses), time.time() - t0), flush=True)
    assum = []
    for U in range(N):
        for W in range(U + 1, N):
            assum.append(int(Av[U, W] if Am[U, W] else -Av[U, W])); assum.append(int(Bv[U, W] if Bm[U, W] else -Bv[U, W]))
    tmp = os.path.join(tempfile.gettempdir(), "k22_control.cnf"); cnf.to_file(tmp); del cnf
    s = Solver(name="cadical195")
    with open(tmp) as fh:
        for line in fh:
            if line[0] in "pc": continue
            s.add_clause([int(t) for t in line.split()[:-1]])
    ok = s.solve(assumptions=assum); print("planted BvLS assignment -> SAT:", ok, "t=%.0fs" % (time.time() - t0), flush=True)
    assert ok
    M, good = lift(m, outer_, rep_, trep_, Av, Bv, s.get_model()); print("lift verifies srg(243,22,1,2):", good); assert good
    for i in (0, 1, 777, 5000):
        bad = list(assum); bad[i] = -bad[i]; r = s.solve(assumptions=bad)
        print("negative control, primary bit %d flipped -> SAT:" % i, r); assert r is False
    os.remove(tmp); print("CNF control PASSED")


if __name__ == "__main__":
    main()
