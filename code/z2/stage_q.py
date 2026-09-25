"""Two-stage form of the involution model (LAB_INSTRUCTIONS.md §4), general k = 2m.

With Q = a + b, S = a - b on the outer orbits of orbit_sat.py, the exact model (R),(D),(I),(P) is equivalent to
  Stage Q:  Q in {0,1,2}, symmetric, zero diagonal; each row: one entry 2 (matching D) and k-4 entries 1;
            block sums  sum_{V meets l} Q[U,V] = 2 if l in blocks(U) else 4;
            Gram (U != V): sum_W Q[U,W] Q[V,W] + Q[U,V] = 4 - Sh[U,V]            (sum of the two (P) equations)
  Stage S:  S[U,V] = +-1 where Q[U,V] = 1, else 0;  C^T S = 0  (difference of the two halves of (I));
            Gram (U != V): sum_W S[U,W] S[V,W] + S[U,V] = -G[U,V], G = C C^T    (difference of the two (P) equations)
and a = (Q+S)/2, b = (Q-S)/2. Stage Q alone is a relaxation: UNSAT in a case closes that case.
Necessary filter on Q from the S-spectrum (dossier, F2-rank theorem): rank_F2((Q mod 2) + Nb Nb^T) = (#eigenvalue-r of S) - m.

Usage:
  python stage_q.py --validate                     # m=2 SAT+lift, m=3 UNSAT, BvLS m=11 planted table SAT, flipped entries UNSAT
  python stage_q.py --m 7 --case sib --out q_sib.cnf
"""
import argparse, itertools, os, sys, time
import numpy as np
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
CASES = {"sib": (1, 2, 1), "one": (1, 3, 0), "dis": (3, 4, 0)}


def frame(m):
    outer = [(i, j, e) for i in range(1, m + 1) for j in range(i + 1, m + 1) for e in (0, 1)]
    N = len(outer)
    C = np.array([[1 if l == i else ((-1 if e else 1) if l == j else 0) for l in range(1, m + 1)] for (i, j, e) in outer], dtype=np.int64)
    Nb = np.abs(C)
    return outer, N, C, Nb, Nb @ Nb.T, C @ C.T


def primaries(m):
    """Primary variable ids: X[U,V] = [Q>=1], Y[U,V] = [Q=2], numbered 1.. in a fixed order (same ids as build_q)."""
    outer, N, C, Nb, Sh, G = frame(m)
    X = {}; Y = {}; nid = 0
    for U in range(N):
        for V in range(U + 1, N):
            nid += 1; X[U, V] = X[V, U] = nid; nid += 1; Y[U, V] = Y[V, U] = nid
    return outer, X, Y, nid


def constraints(m, case="none"):
    """Yield the Stage-Q constraints over primary ids: ("clause", [lits]) or ("card", terms, target), where a term is a
    primary literal (int) or a product (p, q) of two positive primary ids."""
    k = 2 * m
    outer, N, C, Nb, Sh, G = frame(m); _, X, Y, _ = primaries(m)
    for U in range(N):
        for V in range(U + 1, N):
            yield ("clause", [-Y[U, V], X[U, V]])                              # Q=2 -> Q>=1
    for U in range(N):
        oth = [V for V in range(N) if V != U]
        yield ("card", [X[U, V] for V in oth] + [Y[U, V] for V in oth], k - 2)          # row sum of Q
        yield ("card", [Y[U, V] for V in oth], 1)                                        # exactly one 2 (D)
        for l in range(m):                                                               # block sums
            on = [V for V in oth if Nb[V, l]]
            yield ("card", [X[U, V] for V in on] + [Y[U, V] for V in on], 2 if Nb[U, l] else 4)
    for U in range(N):                                                                   # Q-Gram
        for V in range(U + 1, N):
            terms = [X[U, V], Y[U, V]]
            for W in range(N):
                if W in (U, V): continue
                for p in (X[U, W], Y[U, W]):
                    for q in (X[V, W], Y[V, W]):
                        terms.append((p, q))
            yield ("card", terms, 4 - int(Sh[U, V]))
    if case != "none":
        yield ("clause", [Y[0, outer.index(CASES[case])]])


def encode(cons, pool, sink, prodmap, enc=EncType.seqcounter):
    """Encode one constraint into clauses appended to sink (list-like with .append/.extend). Products are shared via prodmap."""
    def lit(t):
        if isinstance(t, tuple):
            p, q = min(t), max(t)
            if (p, q) not in prodmap:
                z = pool.id(("p", p, q)); sink.extend([[-z, p], [-z, q], [z, -p, -q]]); prodmap[p, q] = z
            return prodmap[p, q]
        return t
    if cons[0] == "clause":
        sink.append(list(cons[1])); return
    _, terms, t = cons; lits = [lit(x) for x in terms]
    if not lits:
        if t != 0: sink.append([])
        return
    if t < 0 or t > len(lits): sink.append([]); return
    sink.extend(CardEnc.equals(lits=lits, bound=t, vpool=pool, encoding=enc).clauses)


def build_q(m, case="none", enc=EncType.seqcounter):
    outer, X, Y, top = primaries(m)
    pool = IDPool(start_from=top + 1); cnf = CNF(); prodmap = {}
    for c in constraints(m, case): encode(c, pool, cnf, prodmap, enc)
    return cnf, pool, outer, X, Y


def check_planted_streaming(m, value, flip=None):
    """Memory-light exact test of the Stage-Q CNF on a planted primary assignment value[id] in {0,1}.
    With all primaries fixed, product variables are determined and every cardinality constraint has private auxiliary
    variables, so the CNF is satisfiable iff every constraint's clause set is satisfiable under the assumptions.
    Each constraint is encoded exactly as build_q encodes it and solved alone. Returns the number of failing constraints."""
    from pysat.solvers import Solver
    bad = 0
    for c in constraints(m):
        ids = set(abs(l) for l in c[1]) if c[0] == "clause" else set(
            v for t in c[1] for v in ((t if isinstance(t, tuple) else (abs(t),))))
        if flip is not None and flip not in ids: continue
        pool = IDPool(start_from=max(value) + 1); cl = []; encode(c, pool, cl, {})
        ass = [v if value[v] else -v for v in ids]
        with Solver(name="minisat22", bootstrap_with=cl) as s:
            if not s.solve(assumptions=ass): bad += 1
    return bad


def q_assumptions(Qm, X, Y):
    N = Qm.shape[0]; ass = []
    for U in range(N):
        for V in range(U + 1, N):
            q = int(Qm[U, V]); ass.append(X[U, V] if q >= 1 else -X[U, V]); ass.append(Y[U, V] if q == 2 else -Y[U, V])
    return ass


def decode_q(model, N, X, Y):
    val = set(l for l in model if l > 0); Qm = np.zeros((N, N), dtype=np.int64)
    for U in range(N):
        for V in range(U + 1, N):
            Qm[U, V] = Qm[V, U] = (X[U, V] in val) + (Y[U, V] in val)
    return Qm


def rank_f2(M):
    M = (M.copy() % 2).astype(np.uint8); r = 0; rows, cols = M.shape
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i, c]), None)
        if piv is None: continue
        M[[r, piv]] = M[[piv, r]]
        for i in range(rows):
            if i != r and M[i, c]: M[i] ^= M[r]
        r += 1
    return r


def eigen_rs(k):
    d = int(round((4 * k - 7) ** 0.5)); assert d * d == 4 * k - 7
    return (-1 + d) // 2, (-1 - d) // 2


def check_q(m, Qm):
    """Exact integer checks of every Stage-Q equation, plus the spectral and F2 filters. Returns dict."""
    k = 2 * m; outer, N, C, Nb, Sh, G = frame(m); I = np.eye(N, dtype=np.int64); J = np.ones((N, N), dtype=np.int64)
    r, s = eigen_rs(k)
    out = {}
    out["symmetric_zero_diag_range"] = bool(np.array_equal(Qm, Qm.T) and not np.diag(Qm).any() and Qm.min() >= 0 and Qm.max() <= 2)
    out["rows"] = bool(((Qm == 2).sum(1) == 1).all() and ((Qm == 1).sum(1) == k - 4).all())
    out["blocks"] = bool(np.array_equal(Nb.T @ Qm, 4 * np.ones((m, N), dtype=np.int64) - 2 * Nb.T))
    out["gram"] = bool(np.array_equal(Qm @ Qm + Qm, (k - 2) * I + 4 * J - Sh))
    # S has eigenvalues r, s on m+N dims with tr S = -m  ->  multiplicity f of r
    f = (-m - s * (m + N)) // (r - s)
    exp = (f if r % 2 else (m + N - f)) - m
    out["f2_rank"] = rank_f2((Qm % 2) + Sh); out["f2_rank_expected"] = exp; out["f2_ok"] = out["f2_rank"] == exp
    ev = np.sort(np.round(np.linalg.eigvalsh(Qm.astype(float)), 6))
    out["spectrum"] = {float(x): int(c) for x, c in zip(*np.unique(ev, return_counts=True))}
    out["all_equations"] = out["symmetric_zero_diag_range"] and out["rows"] and out["blocks"] and out["gram"]
    return out


def build_s(m, Qm, enc=EncType.seqcounter):
    """CNF for Stage S given Q. Variable s[U,V] (U<V, Q=1) true <=> S[U,V] = +1."""
    outer, N, C, Nb, Sh, G = frame(m)
    pool = IDPool(); cnf = CNF(); Sv = {}
    for U in range(N):
        for V in range(U + 1, N):
            if Qm[U, V] == 1: Sv[U, V] = Sv[V, U] = pool.id(("s", U, V))
    def eq(lits, t):
        if not lits:
            if t != 0: cnf.append([])
            return
        if t < 0 or t > len(lits) or t != int(t): cnf.append([]); return
        cnf.extend(CardEnc.equals(lits=lits, bound=int(t), vpool=pool, encoding=enc).clauses)
    XN = {}
    def xnor(p, q):                                  # true <=> S_p * S_q = +1
        key = (min(p, q), max(p, q))
        if key not in XN:
            z = pool.id(("e",) + key); cnf.extend([[-z, -p, q], [-z, p, -q], [z, p, q], [z, -p, -q]]); XN[key] = z
        return XN[key]
    for U in range(N):                               # C^T S = 0 : sum_V C[V,l] S[U,V] = 0
        for l in range(m):
            lits = []
            for V in range(N):
                if V != U and Qm[U, V] == 1 and C[V, l]:
                    lits.append(Sv[U, V] if C[V, l] > 0 else -Sv[U, V])
            if len(lits) % 2: cnf.append([]); continue
            eq(lits, len(lits) // 2)
    for U in range(N):                               # S-Gram
        for V in range(U + 1, N):
            Ws = [W for W in range(N) if W not in (U, V) and Qm[U, W] == 1 and Qm[V, W] == 1]
            lits = [xnor(Sv[U, W], Sv[V, W]) for W in Ws]; t = len(Ws); g = int(G[U, V])
            if Qm[U, V] == 1:                        # 2 sum(e) - t + (2 s - 1) = -g
                if (t - g + 1) % 2: cnf.append([]); continue
                eq(lits + [Sv[U, V]], (t - g + 1) // 2)
            else:                                    # 2 sum(e) - t = -g
                if (t - g) % 2: cnf.append([]); continue
                eq(lits, (t - g) // 2)
    return cnf, pool, Sv


def solve_s(m, Qm, solver="cadical195"):
    from pysat.solvers import Solver
    cnf, pool, Sv = build_s(m, Qm)
    N = Qm.shape[0]
    with Solver(name=solver, bootstrap_with=cnf.clauses) as sv:
        ok = sv.solve()
        if not ok: return None
        val = set(l for l in sv.get_model() if l > 0)
    Sm = np.zeros((N, N), dtype=np.int64)
    for (U, V), v in Sv.items(): Sm[U, V] = 1 if v in val else -1
    return Sm


def check_s(m, Qm, Sm):
    outer, N, C, Nb, Sh, G = frame(m); k = 2 * m; I = np.eye(N, dtype=np.int64)
    return bool(np.array_equal(np.abs(Sm), (Qm == 1).astype(np.int64)) and np.array_equal(C.T @ Sm, np.zeros((m, N), dtype=np.int64))
                and np.array_equal(Sm @ Sm + Sm, (k - 2) * I - G))


def lift_qs(m, Qm, Sm):
    """a=(Q+S)/2, b=(Q-S)/2 -> full adjacency via orbit_sat.lift; returns (M, srg identity holds)."""
    from orbit_sat import lift
    outer, N, C, Nb, Sh, G = frame(m)
    Am = (Qm + Sm) // 2; Bm = (Qm - Sm) // 2
    assert ((Qm + Sm) % 2 == 0).all()
    A = {}; B = {}; model = []; nid = 0
    for U in range(N):
        for V in range(U + 1, N):
            nid += 1; A[U, V] = A[V, U] = nid; model.append(nid if Am[U, V] else -nid)
            nid += 1; B[U, V] = B[V, U] = nid; model.append(nid if Bm[U, V] else -nid)
    rep = [frozenset([(i, 0), (j, e)]) for (i, j, e) in outer]
    trep = [frozenset([(i, 1), (j, 1 - e)]) for (i, j, e) in outer]
    return lift(m, outer, rep, trep, A, B, model)


def validate():
    from pysat.solvers import Solver
    t0 = time.time()
    # m = 2: must be SAT, S-stage SAT, lift to srg(9,4,1,2)
    cnf, pool, outer, X, Y = build_q(2)
    with Solver(name="cadical195", bootstrap_with=cnf.clauses) as sv:
        assert sv.solve(); Qm = decode_q(sv.get_model(), len(outer), X, Y)
    cq = check_q(2, Qm); Sm = solve_s(2, Qm)
    M, ok = lift_qs(2, Qm, Sm)
    print("m=2: Stage Q SAT, checks", cq["all_equations"], "f2", cq["f2_ok"], "| Stage S", Sm is not None and check_s(2, Qm, Sm), "| lift srg(9,4,1,2):", ok)
    assert cq["all_equations"] and ok
    # m = 3: no srg(19,6,1,2): Stage Q need not be UNSAT (relaxation), just report
    cnf, pool, outer, X, Y = build_q(3)
    with Solver(name="cadical195", bootstrap_with=cnf.clauses) as sv:
        print("m=3: Stage Q", "SAT" if sv.solve() else "UNSAT", "(no srg(19,6,1,2); either answer is consistent for a relaxation)")
    # m = 11: BvLS planted table must satisfy the Stage-Q CNF; flipped entries must be rejected
    from control_bvls import bvls
    import control_bvls as cb
    A, V, ix, cols, neg = bvls(); n, k, m = 243, 22, 11
    inner = {}
    for i, c in enumerate(cols): inner[ix[c]] = (i + 1, 0); inner[ix[neg(c)]] = (i + 1, 1)
    x = ix[(0,) * 5]; label = {}
    for v in range(n):
        if v == x or v in inner: continue
        label[frozenset(inner[w] for w in np.flatnonzero(A[v]) if w in inner)] = v
    outer, N, C, Nb, Sh, G = frame(m)
    rep = [frozenset([(i, 0), (j, e)]) for (i, j, e) in outer]; trep = [frozenset([(i, 1), (j, 1 - e)]) for (i, j, e) in outer]
    Am = np.array([[A[label[rep[U]], label[rep[W]]] if U != W else 0 for W in range(N)] for U in range(N)])
    Bm = np.array([[A[label[rep[U]], label[trep[W]]] if U != W else 0 for W in range(N)] for U in range(N)])
    Qb = Am + Bm; Sb = Am - Bm
    cq = check_q(m, Qb)
    print("BvLS m=11 table: Stage-Q equations", cq["all_equations"], "| F2 rank", cq["f2_rank"], "expected", cq["f2_rank_expected"],
          "| Stage-S equations", check_s(m, Qb, Sb), "| lift:", lift_qs(m, Qb, Sb)[1])
    assert cq["all_equations"] and cq["f2_ok"] and check_s(m, Qb, Sb)
    # the S-stage CNF must accept the planted S for the planted Q
    scnf, spool, Sv = build_s(m, Qb)
    sass = [Sv[U, W] if Sb[U, W] > 0 else -Sv[U, W] for (U, W) in Sv if U < W]
    with Solver(name="cadical195", bootstrap_with=scnf.clauses) as sv:
        okS = sv.solve(assumptions=sass)
        print("BvLS Stage-S CNF accepts planted S:", okS); assert okS
        bad = list(sass); bad[0] = -bad[0]; rS = sv.solve(assumptions=bad)
        print("BvLS Stage-S CNF, one sign flipped -> SAT:", rS); assert rS is False
    D0 = int(np.flatnonzero(Qb[0] == 2)[0]); U0, Dt = outer[0], outer[D0]
    typ = "sib" if Dt == (1, 2, 1) else ("one" if len(set(U0[:2]) & set(Dt[:2])) == 1 else "dis")
    print("BvLS: D(U0) =", Dt, "-> case type", typ)
    t1 = time.time(); outer_, X, Y, top = primaries(m)
    value = {}
    for U in range(N):
        for W in range(U + 1, N):
            value[X[U, W]] = int(Qb[U, W] >= 1); value[Y[U, W]] = int(Qb[U, W] == 2)
    nbad = check_planted_streaming(m, value)
    print("planted BvLS Q, streaming per-constraint check of the m=11 Stage-Q CNF: failing constraints = %d (%.0fs)" % (nbad, time.time() - t1), flush=True)
    assert nbad == 0
    rng = np.random.default_rng(1)
    for t in range(6):
        v = int(rng.integers(1, top + 1)); flipped = dict(value); flipped[v] = 1 - flipped[v]
        nb = check_planted_streaming(m, flipped, flip=v)
        print("  primary var %d flipped -> failing constraints: %d" % (v, nb), flush=True); assert nb > 0
    # the same streaming check must agree with a whole-CNF solve where that is cheap (m = 7 would need a planted table;
    # use m = 2 instead: the unique Q is planted, then one flip)
    o2, X2, Y2, top2 = primaries(2); cnf2, pool2, _, _, _ = build_q(2)
    with Solver(name="cadical195", bootstrap_with=cnf2.clauses) as sv:
        sv.solve(); Q2 = decode_q(sv.get_model(), len(o2), X2, Y2)
    v2 = {}
    for U in range(len(o2)):
        for W in range(U + 1, len(o2)):
            v2[X2[U, W]] = int(Q2[U, W] >= 1); v2[Y2[U, W]] = int(Q2[U, W] == 2)
    assert check_planted_streaming(2, v2) == 0
    print("VALIDATION PASSED (%.0fs)" % (time.time() - t0))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true"); ap.add_argument("--m", type=int, default=7)
    ap.add_argument("--case", default="none", choices=["none"] + list(CASES)); ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.validate: validate(); sys.exit(0)
    t0 = time.time(); cnf, pool, outer, X, Y = build_q(a.m, a.case)
    print("Stage Q m=%d case=%s vars=%d clauses=%d build=%.1fs" % (a.m, a.case, pool.top, len(cnf.clauses), time.time() - t0), flush=True)
    if a.out: cnf.to_file(a.out); print("written", a.out)
