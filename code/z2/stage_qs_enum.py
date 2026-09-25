"""Stage Q -> Stage S pipeline for the involution branch (m = 7, one case of the D(U0) split).

Loop: find a Stage-Q orbit matrix with an incremental SAT solver; check every Q-equation exactly (integers) and the
F2-rank filter; solve Stage S for that Q; if S exists, lift (a,b) = ((Q+S)/2, (Q-S)/2) and test A^2 + A - 12I = 2J;
then block this labelled Q and continue. Every Q found is appended to <prefix>_Q.jsonl, one JSON line per Q, flushed.
A found graph (lift verified) is written to <prefix>_GRAPH_<n>.txt and the run stops.
Note: blocking is per labelled matrix (no isomorph rejection); counts are therefore labelled counts within the case.
Usage: python stage_qs_enum.py --case sib --max-q 100000 --prefix runs/enum_sib
"""
import argparse, json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from stage_q import build_q, decode_q, check_q, solve_s, check_s, lift_qs
from pysat.solvers import Solver


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--m", type=int, default=7); ap.add_argument("--case", required=True)
    ap.add_argument("--max-q", type=int, default=10 ** 9); ap.add_argument("--prefix", required=True)
    ap.add_argument("--solver", default="cadical195")
    a = ap.parse_args(); m = a.m
    t0 = time.time(); cnf, pool, outer, X, Y = build_q(m, a.case); N = len(outer)
    prim = sorted(set(X.values()) | set(Y.values()))
    print("Stage Q m=%d case=%s vars=%d clauses=%d build=%.1fs" % (m, a.case, pool.top, len(cnf.clauses), time.time() - t0), flush=True)
    stats = {"q": 0, "q_eq_ok": 0, "f2_ok": 0, "s_sat": 0, "lift_ok": 0}
    with Solver(name=a.solver, bootstrap_with=cnf.clauses) as sv, open(a.prefix + "_Q.jsonl", "a") as out:
        del cnf
        while stats["q"] < a.max_q:
            t1 = time.time(); res = sv.solve(); dt = time.time() - t1
            if not res:
                print("Stage Q: no more solutions (UNSAT after %d blocked) t=%.0fs" % (stats["q"], time.time() - t0), flush=True)
                break
            model = sv.get_model(); Qm = decode_q(model, N, X, Y); stats["q"] += 1
            cq = check_q(m, Qm); stats["q_eq_ok"] += cq["all_equations"]; stats["f2_ok"] += cq["f2_ok"]
            rec = {"n": stats["q"], "t_solve": round(dt, 2), "t": round(time.time() - t0, 1), "eq": cq["all_equations"],
                   "f2": cq["f2_rank"], "Q": Qm.tolist()}
            if not cq["all_equations"]:
                rec["ERROR"] = "decoded Q violates Stage-Q equations: encoding bug"; out.write(json.dumps(rec) + "\n"); out.flush()
                print("ENCODING ERROR: decoded Q fails the exact equations", cq, flush=True); sys.exit(2)
            if cq["f2_ok"]:
                t2 = time.time(); Sm = solve_s(m, Qm); rec["t_S"] = round(time.time() - t2, 2); rec["S"] = Sm is not None
                if Sm is not None:
                    stats["s_sat"] += 1; assert check_s(m, Qm, Sm)
                    M, ok = lift_qs(m, Qm, Sm); rec["lift"] = bool(ok)
                    if ok:
                        stats["lift_ok"] += 1; fn = "%s_GRAPH_%d.txt" % (a.prefix, stats["q"]); np.savetxt(fn, M, fmt="%d")
                        out.write(json.dumps(rec) + "\n"); out.flush()
                        print("!!! LIFT VERIFIED: srg(99,14,1,2) candidate written to", fn, flush=True); break
            out.write(json.dumps(rec) + "\n"); out.flush()
            pos = set(l for l in model if l > 0)
            sv.add_clause([-v if v in pos else v for v in prim])
            if stats["q"] <= 20 or stats["q"] % 100 == 0:
                print("Q#%d solve %.1fs t=%.0fs %s" % (stats["q"], dt, time.time() - t0, stats), flush=True)
    print("FINAL", json.dumps(stats), "t=%.0fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
