"""CP-SAT form of Stage Q, built from the SAME constraint generator as the CNF (stage_q.constraints), so the two
models cannot drift apart. A returned Q is re-checked exactly with stage_q.check_q; if it passes the F2 filter,
Stage S is solved and the lift is tested. An INFEASIBLE answer here is NOT a certificate (no proof): it would have to be
re-proved by kissat with a DRAT proof checked by drat-trim.
Usage: python stage_q_cpsat.py --m 7 --case sib --time 7200 --workers 8 --out result.json
"""
import argparse, json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from stage_q import primaries, constraints, check_q, solve_s, check_s, lift_qs
from ortools.sat.python import cp_model


def build(m, case):
    outer, X, Y, top = primaries(m)
    mdl = cp_model.CpModel(); b = {v: mdl.NewBoolVar("v%d" % v) for v in range(1, top + 1)}; P = {}
    def lit(t):
        if isinstance(t, tuple):
            p, q = min(t), max(t)
            if (p, q) not in P:
                z = mdl.NewBoolVar("p%d_%d" % (p, q))
                mdl.AddBoolAnd([b[p], b[q]]).OnlyEnforceIf(z); mdl.AddBoolOr([b[p].Not(), b[q].Not()]).OnlyEnforceIf(z.Not())
                P[p, q] = z
            return P[p, q]
        return b[t] if t > 0 else b[-t].Not()
    for c in constraints(m, case):
        if c[0] == "clause": mdl.AddBoolOr([lit(l) for l in c[1]])
        else: mdl.Add(sum(lit(t) for t in c[1]) == c[2])
    return mdl, b, outer, X, Y


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--m", type=int, default=7); ap.add_argument("--case", default="none")
    ap.add_argument("--time", type=float, default=600); ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0); ap.add_argument("--out", default=None)
    a = ap.parse_args(); t0 = time.time()
    mdl, b, outer, X, Y = build(a.m, a.case); N = len(outer)
    print("CP-SAT Stage Q m=%d case=%s built in %.1fs" % (a.m, a.case, time.time() - t0), flush=True)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = a.time; s.parameters.num_workers = a.workers
    s.parameters.random_seed = a.seed; s.parameters.log_search_progress = True; s.log_callback = lambda msg: print(msg, flush=True)
    st = s.Solve(mdl); name = s.StatusName(st)
    res = {"m": a.m, "case": a.case, "status": name, "wall": s.WallTime(), "conflicts": s.NumConflicts(), "branches": s.NumBranches()}
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        Qm = np.zeros((N, N), dtype=np.int64)
        for U in range(N):
            for V in range(U + 1, N):
                Qm[U, V] = Qm[V, U] = s.Value(b[X[U, V]]) + s.Value(b[Y[U, V]])
        cq = check_q(a.m, Qm); res.update({"eq": cq["all_equations"], "f2": cq["f2_rank"], "f2_ok": cq["f2_ok"], "Q": Qm.tolist()})
        if cq["all_equations"] and cq["f2_ok"]:
            Sm = solve_s(a.m, Qm); res["S"] = Sm is not None
            if Sm is not None:
                assert check_s(a.m, Qm, Sm); M, ok = lift_qs(a.m, Qm, Sm); res["lift"] = bool(ok)
    print("RESULT", json.dumps({k: v for k, v in res.items() if k != "Q"}), flush=True)
    if a.out: json.dump(res, open(a.out, "w"))


if __name__ == "__main__":
    main()
