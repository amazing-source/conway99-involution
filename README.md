# Conway's 99-graph — the involution branch (research log)

Private research repository on one branch of the existence problem for srg(99,14,1,2): **a putative Conway 99-graph Γ with an automorphism
of order 2**. Everything here is either cited to a primary source or proved/computed in the repository.
**Nothing here resolves the existence of srg(99,14,1,2), and no case of the involution branch has been eliminated.**

**Where to start**
- Running computations (lab machine): **`LAB_INSTRUCTIONS.md`**.
- What was checked, and what was wrong: `notes/AUDIT_2026-09-22.md`.
- The mathematics: `report/dossier_chercheurs_fr.pdf` (French, full state, revision 2) or `report/conway99_involution_report.pdf` (English, short).

## 0. Summary
|Aut(Γ)| ∈ {1, 2, 3} (Makhnev–Minakova 2004; Behbahani 2009 / Behbahani–Lam 2011; Crnković–Maksimović 2020; Cesarz–Woldar 2025). To our knowledge
the involution case has never been computed (Behbahani's table starts at p = 3). An involution t fixes exactly one vertex x and flips every matched
pair of N(x) (essentially Makhnev's lemma). This repository adds the **perfect matching D** on the 42 outer σ-orbits (N(u) ∩ N(σu) is always a full orbit),
an **exact 42-orbit model** (1722 bits, constraints (R),(D),(I),(P)), which splits exactly into an ordinary-quotient stage Q and a sign stage S, and invariants
usable as filters (Spec(Q_out) = {12, (−2)^6, 3^20, (−4)^15}; rank_F2(Γ̄ + Nb Nbᵀ) = 20; mod-3 ranks). These invariants are consequences of the model,
not independent obstructions. Generic SAT/CP-SAT runs (up to 8 h per case) are all undecided. Separately: an audit of Reimbayev's order-seven census
(arXiv:2608.19410): four typos, after which it adds no constraint on n₃.

## 1. Status
| Item | Status |
|---|---|
| Rigidity (t = flip, u ≁ σu, a₁(t) = 14) | Proved; flip lemma essentially Makhnev (Bielefeld notes). |
| Matching D, exact orbit model (R),(D),(I),(P) | Proved; code reviewed line by line; **validated on srg(243,22,1,2)** (m = 11, 0 violations). |
| CNF encoding at m = 11 (`control_bvls.py --cnf`) | **Passed** on the lab machine, 2026-09-22 (planted BvLS SAT + lift, 4/4 flips UNSAT; `results/lab_2026-09-22/control4_bvls_cnf.log`). |
| Case split sib / one / dis on D(U0) | Proved exhaustive (Stab(U0) of order 15 360 has 3 orbits). |
| Spec(Q_out), F₂ rank 20, F₃ ranks | Proved; general-k analogues checked on srg(243,22,1,2). Filters, not obstructions. |
| SAT/CP-SAT on the full model | 7 × 8 h UNKNOWN; CP-SAT 15–25 min UNKNOWN. A timeout is not evidence. |
| `results/batch_kissat_one10.log` (UNSAT) | **Do not cite.** Undocumented sub-case, empty by construction (see `notes/ONE10_PROVENANCE.md`). |
| Order-7 census audit | Four typos; re-verified offline from the archived JSONs. No new constraint. |
| **Next task** | Enumerate the Q_out orbit matrices (Stage Q) — `LAB_INSTRUCTIONS.md` §4. In progress: Stage Q 2 h UNKNOWN (kissat, CP-SAT); 1 326 symmetry cubes; see `results/HANDOFF_2026-09-22.md`. |

## 2. Corrections made on 2026-09-22 (details in `notes/AUDIT_2026-09-22.md`)
- The dossier's "new congruence" (#induced C4 odd) was empty: c4 = 2079 in every srg(99,14,1,2). Removed.
- The k = 4 / k = 6 controls were too weak to catch a model error; the strong control `code/z2/control_bvls.py` was added.
- "Rank 20 is genuinely additional information" was wrong (it follows from the model); fixed in all reports.
- The "signed-only relaxation" (`cpsat_model.py`, `dfs_backup.py`) omits Cᵀ S_out = 0; documented.
- The k = 4 probe finds 1 labelled solution, not 3; the Q − 3I part of the dossier's Prop. F3(iv) was unproved; credits and bibliography fixed.
- The order-3 third-party notes (`notes/third_party/`) were removed as off-topic (recoverable at commit `9eb634d`).

## 3. Layout
- `LAB_INSTRUCTIONS.md` — what the lab session runs, in which order, and the rules for reporting.
- `report/` — `dossier_chercheurs_fr` (full state, French), `conway99_involution_report` (English), `involution_notes_fr` (French, pedagogical); `Dockerfile.tex`.
- `notes/` — `AUDIT_2026-09-22.md`, `NOTE_involution_case.md`, `ONE10_PROVENANCE.md`, `AUDIT_reimbayev_order7.md`, `WHAT_WOULD_HELP.md`, `SOURCES.md`, `RESEARCH_MEMORY.md` (historical).
- `code/z2/` — `orbit_sat.py` (exact CNF model + lift), `cpsat_orbit.py`, `run_orbit.py`, `row_fix.py`, `rows.py`, `joint_dfs.py`, `sout_dfs.py`,
  `anneal_orbit.py`, `anneal_struct.py`, `control_bvls.py` (strong control), `probe99/` (generic 99-vertex model), `Dockerfile` (satbox), `run_batch.sh`;
  `common.py` / `cpsat_model.py` / `dfs_backup.py` (weaker signed relaxation, see above).
- `code/r7_check/` — order-7 audit scripts (need the arXiv TeX and the public repo) and their JSON outputs.
- `results/` — solver logs and the overnight batch summary.

## 4. Reproduce (Python 3.12: `sympy numpy python-sat ortools`; generate CNFs under Docker/WSL, the repo checks out CRLF on Windows)
```
python code/z2/orbit_sat.py --m 2 --solve      # weak control: SAT, lift verified as srg(9,4,1,2)
python code/z2/orbit_sat.py --m 3 --solve      # weak control: UNSAT (srg(19,6,1,2) does not exist)
python code/z2/control_bvls.py                 # strong control on srg(243,22,1,2), light (< 2 min)
python code/z2/control_bvls.py --cnf           # CNF-encoding check, ~20 GB RAM: lab machine only
python code/z2/orbit_sat.py --m 7 --case one --out k14_one.cnf
docker build -t satbox code/z2 && sh code/z2/run_batch.sh 28800 "$PWD"
```

## 5. Principal sources
Makhnev–Minakova, Diskr. Mat. 16:1 (2004), DOI 10.4213/dm144; Makhnev, Bielefeld notes; Behbahani, thesis (2009) and Behbahani–Lam, Discrete Math. 311 (2011);
Crnković–Maksimović, Contrib. Discrete Math. 15 (2020); Cesarz–Woldar, Algebraic Combinatorics 8 (2025); Keramatipour, arXiv:2604.23037;
Thakkar–Severini, arXiv:2608.11211; Ishida, arXiv:2606.29183; Reimbayev, arXiv:2608.19410; YesterdaysLemon/conway-99-research. Links: `notes/SOURCES.md`.
