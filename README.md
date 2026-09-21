# Conway's 99-graph — the involution branch (research log, 2026-09-21)

Private research repository. Everything here is either cited to a primary source or proved/computed in the repository.
**Nothing here resolves the existence of srg(99,14,1,2).**

## 0. One-paragraph summary
|Aut(Γ)| ∈ {1, 2, 3} for a putative Conway 99-graph Γ (Makhnev–Minakova 2004; Behbahani–Lam 2009/2011; Crnković–Maksimović 2020;
Cesarz–Woldar 2025). The one-fixed-point Z7 case, called "open" by Thakkar–Severini (arXiv:2608.11211), was closed at the orbit-matrix
level in 2009/2011. The **involution branch has never been computed**. We show it is completely rigid (Fix(t) = {x}, t = flip of every
matched pair of N(x), no vertex outside N(x) adjacent to its image, the μ-graphs {u,tu} form a perfect matching on the 42 outer orbits),
reduce it to an exact 42-orbit model (validated SAT/CP-SAT encodings), derive a **new necessary condition** from the 2-adic structure
(eigenlattices are free Z₂[C₂]-modules ⇒ rank_F2(Γ̄ + NbNbᵀ) = 20 with Γ̄² + Γ̄ = NbNbᵀ over F₂), and report first computations (all inconclusive).
Separately we audit Reimbayev's order-seven census (arXiv:2608.19410): four typos, after which it is exactly the repository's wave-23 family
and gives no new constraint on n₃.

## 1. Established (with sources) — see `report/conway99_involution_report.tex` §1
- Makhnev–Minakova 2004 (Diskr. Mat. 16:1, DOI 10.4213/dm144, Theorem 1): prime-order automorphism ⇒ Fix = one vertex (order 2 or 7), empty (3 or 11), or a triangle (3).
- Behbahani 2009 thesis (LAC NR63369), Thm 4.14 / Table 21: no orbit matrices for p = 5, 7, 11 (all fixed-point counts) nor p = 3 with fixed points. p = 2 not computed.
- Crnković–Maksimović 2020: orders 6 and 9 excluded. Cesarz–Woldar 2025: 2 | |G| ⇒ |G| | 6; 7 | |G| ⇒ G ≅ Z7 (weaker than B–L for 7).
- Repo `YesterdaysLemon/conway-99-research`: rigorous 708 ≤ n₃ ≤ 4158; full order-7 affine family (wave 23); three-centre compatibility (wave 206, unmerged branch); universal rank_F7(M) ≥ 27.

## 2. New in this work
- Rigidity of the involution and the orbit-level exact model (`NOTE_involution_case.md` §2; report §2).
- Theorem (report §3): free Z₂[C₂]-structure of the eigenlattices ⇒ exact F₂-rank equation for the single-adjacency graph on the 42 orbits.
- Audit of arXiv:2608.19410 (`AUDIT_reimbayev_order7.md`): z₂₁ (drop (k−3)), z₈₀ = z₈₄ ((2k−7) → (2k−17)), z₁₇₆ (1/84 → 1/8).
- Literature correction: Z7 case closed since 2009/2011; repo waves 69/72 on order 11 redundant with Behbahani–Lam.

## 3. Tested (scope) and open
- Tested: S-relaxation CP-SAT 25 min → UNKNOWN; joint model with the row of U₀ fixed → CaDiCaL ≥ 30 min CPU ×4 undecided, CP-SAT 15 min UNKNOWN;
  native CaDiCaL/Kissat batch on 3 cases (+2 subcases), 8 h limit → see `results/`.
- Open: the involution branch itself (a decision either way is certifiable); the order-3 fixed-point-free branch (crowded); the asymmetric case (no known method).

## 4. Layout
- `report/` — `conway99_involution_report.pdf` (English, technical) and **`involution_notes_fr.pdf` (notes en français : ce que j'explore, ce que j'ai trouvé, ce qui tourne)**, with sources.
- `notes/` — `NOTE_involution_case.md`, `AUDIT_reimbayev_order7.md`, `RESEARCH_MEMORY.md`, `SOURCES.md`, **`WHAT_WOULD_HELP.md`** (what is missing / what a researcher could provide).
- `code/z2/` — `orbit_sat.py` (CNF model + lift/verify), `cpsat_orbit.py`, `run_orbit.py`, `row_fix.py`, `anneal_orbit.py` (recuit simulé), `joint_dfs.py`, `sout_dfs.py`, `rows.py`, `Dockerfile`, `run_batch.sh`.
- `code/r7_check/` — `parse_r7.py`, `match705.py`, `corrected.py`, `family_n3.py` (order-7 audit; needs the arXiv TeX source and the public repo).
- `results/` — JSON results and solver logs.

## 5. Reproduce (Python 3.12, `uv pip install sympy numpy python-sat ortools`)
```
python code/z2/orbit_sat.py --m 2 --solve      # control k=4: SAT, lifted matrix verified as srg(9,4,1,2)
python code/z2/orbit_sat.py --m 3 --solve      # control k=6: UNSAT (srg(19,6,1,2) does not exist)
python code/z2/orbit_sat.py --m 7 --case one --out k14_one.cnf
docker build -t satbox code/z2 && sh code/z2/run_batch.sh 28800
```
