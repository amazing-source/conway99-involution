# Test of the C3-style "two specializations" invariant at p = 2 for an involution sigma fixing one vertex x.
# F = E_theta Z_2^n is free over Z_2[C_2]; R = det(Lambda^+)/det(Lambda^-) (invariant / anti-invariant eigen-sublattices).
# Local prediction (derived by hand): R/2-adic unit ratio  == 1 + 2 t  (mod 4), with t = (E_theta)_xx / 2 (a 2-adic number; t mod 2).
import sys, itertools
from fractions import Fraction
import numpy as np
sys.path.insert(0, ".")
def int_kernel(M):
    # integer kernel basis of integer matrix M (rows x n) via column Euclid with transformation (exact Python ints)
    M = [list(map(int, r)) for r in M]; m, n = len(M), len(M[0])
    U = [[int(i == j) for j in range(n)] for i in range(n)]   # columns transform
    col = 0
    for r in range(m):
        while True:
            nz = [c for c in range(col, n) if M[r][c] != 0]
            if len(nz) <= 1: break
            p = min(nz, key=lambda c: abs(M[r][c]))
            for c in nz:
                if c != p:
                    q = M[r][c] // M[r][p]
                    for i in range(m): M[i][c] -= q * M[i][p]
                    for i in range(n): U[i][c] -= q * U[i][p]
        nz = [c for c in range(col, n) if M[r][c] != 0]
        if nz:
            p = nz[0]
            for i in range(m): M[i][col], M[i][p] = M[i][p], M[i][col]
            for i in range(n): U[i][col], U[i][p] = U[i][p], U[i][col]
            col += 1
    return [[U[i][c] for i in range(n)] for c in range(col, n)]
def det_int(G):
    return int(round(float(np.linalg.det(np.array(G, dtype=float))))) if len(G) < 12 else None
def det_frac(G):
    G = [[Fraction(x) for x in r] for r in G]; n = len(G); d = Fraction(1)
    for i in range(n):
        p = next(k for k in range(i, n) if G[k][i] != 0)
        if p != i: G[i], G[p] = G[p], G[i]; d = -d
        d *= G[i][i]
        for k in range(i + 1, n):
            f = G[k][i] / G[i][i]
            if f: G[k] = [a - f * b for a, b in zip(G[k], G[i])]
    return d
def v2(z):
    z = abs(int(z)); c = 0
    while z % 2 == 0: z //= 2; c += 1
    return c
def test(name, A, sig, x, theta):
    n = len(A); orbs = []; seen = set()
    for u in range(n):
        if u in seen or u == x: continue
        seen |= {u, sig[u]}; orbs.append((u, sig[u]))
    # invariant lattice basis f_x, f_U ; anti-invariant g_U
    def quot(sign):
        basis = ([[1 if i == x else 0 for i in range(n)]] if sign > 0 else []) + \
                [[(1 if i == u else (sign if i == w else 0)) for i in range(n)] for (u, w) in orbs]
        B = np.array(basis, dtype=np.int64).T          # n x d
        AB = A @ B                                       # express A*B in basis: coordinates = entries at representative
        reps = ([x] if sign > 0 else []) + [u for (u, w) in orbs]
        Qm = AB[reps, :]                                 # coordinate of A f_j on f_i is (A f_j)[rep_i]
        return B, Qm
    out = {}
    for sign in (+1, -1):
        B, Qm = quot(sign)
        d = Qm.shape[0]
        K = int_kernel((Qm - theta * np.eye(d, dtype=np.int64)).tolist())   # integer kernel in f/g coordinates
        V = np.array(K, dtype=object).T                  # d x rk
        Gf = np.diag([1 if (sign > 0 and i == 0) else 2 for i in range(d)]).astype(object)
        G = (V.T.dot(Gf)).dot(V)
        out[sign] = (len(K), det_frac(G.tolist()))
    (rp, Dp), (rm, Dm) = out[1], out[-1]
    Exx = None
    ev = np.linalg.eigvalsh(A.astype(float)); mult = int(sum(abs(ev - theta) < 1e-6))
    Exx = Fraction(mult, n)
    up, um = int(Dp) // 2**v2(int(Dp)), int(Dm) // 2**v2(int(Dm))
    t = Fraction(Exx, 2)
    print(f"{name} theta={theta}: rank+={rp} rank-={rm}  det+={int(Dp)} (2^{v2(int(Dp))}*{up})  det-={int(Dm)} (2^{v2(int(Dm))}*{um})")
    print(f"   odd ratio u+/u- mod 8 = {(up * pow(um, -1, 8)) % 8};  (E_theta)_xx/2 = {t}  -> t mod 2 = {t.numerator % 2};  predicted mod 4: {(1 + 2 * (t.numerator % 2)) % 4}")
# Paley 9 = rook graph K3xK3 on F_3^2, sigma: v -> -v, x = 0
P = list(itertools.product(range(3), repeat=2)); idx = {p: i for i, p in enumerate(P)}
A9 = np.array([[int(p != q and (p[0] == q[0] or p[1] == q[1])) for q in P] for p in P], dtype=np.int64)
s9 = [idx[((-p[0]) % 3, (-p[1]) % 3)] for p in P]
for th in (1, -2): test("Paley9", A9, s9, idx[(0, 0)], th)
from control_bvls import bvls
A, V, ix, cols, neg = bvls(); A = A.astype(np.int64)
sB = [ix[neg(v)] for v in V]
for th in (4, -5): test("BvLS", A, sB, ix[(0,) * 5], th)
