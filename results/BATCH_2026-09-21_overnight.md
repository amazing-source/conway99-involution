# Overnight exact batch, 2026-09-21 18:50 → 2026-09-22 02:58 (all UNKNOWN)

Native Linux solvers in Docker (image `satbox`: kissat 4.0.4, cadical), 1 CPU each, wall limit 8 h, instances from `orbit_sat.py --m 7`
(666 183 vars / 1.51 M clauses; sound case split on the double orbit of U0, plus the dis00/dis10 sub-split).

| instance | solver | result | wall |
|---|---|---|---|
| k14_sib | cadical | c UNKNOWN (alarm, exit 142) | 8 h |
| k14_one | cadical | c UNKNOWN (alarm) | 8 h |
| k14_dis | cadical | c UNKNOWN (alarm) | 8 h |
| k14_sib | kissat | s UNKNOWN | 8 h |
| k14_one | kissat | s UNKNOWN | 8 h |
| k14_dis00 | kissat | s UNKNOWN | 8 h |
| k14_dis10 | kissat | s UNKNOWN | 8 h |

Heuristics (bit-flip annealing, 3 seeds, up to 1 h; structured-move annealing, 3 seeds, 10 min): plateau at energy ≈ 1550–1650
(P-constraint violations dominate); no solution. A timeout is not evidence; the involution branch remains open.
Lesson for the next campaign: run solvers with statistics on (no `-q`), add symmetry breaking (BreakID / lex-leader under 2^7⋊S_7),
or move to an orderly generator with spectral interlacing (see report §5).
