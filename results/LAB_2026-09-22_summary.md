# Lab session 2026-09-22 (evening), lab machine (Ryzen 7 7800X3D, 32 GB)

Starting point: commit 8b4ba9a (audit). Everything below was run on this machine; raw logs in `results/lab_2026-09-22/`.

## Step 1: preservation of the original session's work
All files of the original session (eeaf2d22: temp scratchpad incl. the 8 `k14_*.cnf`, transcripts, subagent/workflow logs, uploads) and the
58 untracked repo files (`code/z2/phase2/`, `notes/BRIEFING_phase2.md`, `notes/DEEP_THOUGHT_2026-09-22.md`) were copied unchanged to
`C:\Users\RESEARCHER\Desktop\conway99-lab-archive\` with `SHA256SUMS.txt` (11 591 files, every copy re-hashed against its source: all match).

## Step 2: evidence vs. the audit (the evidence wins)
| "Not archived" output | What exists on this machine |
|---|---|
| `result_cpsat_none.json` | Existed only as the **m = 3 control** (UNSAT 0.01 s). The k = 14 CP-SAT "none" run (2 h cap) was killed after ~5 min; no result. `SOLUTION_cpsat_none.txt` is the m = 2 (9×9) solution. |
| `rowfix_seed*.json` | Never written (4 runs printed "row built", killed after ~30 min). |
| `rows_U0.npy` / rows.py count | Never written; `rows.py` printed `Q-patterns: 7164496 t=202.0s`, killed before the sign stage. A phase-2 agent counted 22 176 (sib) / 155 904 (one) valid U0 rows (unverified; dis unfinished). |
| joint_dfs / sout_dfs traces | In the transcript: both hit a node cap after 5–8 s (sout: max 6 rows in 3 M nodes; joint: max 2 rows in 4 M nodes). "Stall at rows 2–6" overstates this. |
| probe99 at k = 14 | Built (886 200 vars, 2.10 M clauses); no result ever written ("no result", not "UNKNOWN"). |
Also: `RESEARCH_MEMORY.md` 36–37 overstate the runs (pysat CaDiCaL ×3 killed after ~1 h; CP-SAT none after ~5 min). All 15 original scripts are
byte-identical (modulo CRLF) to the repo versions, so there is no variant of `cpsat_model.py` with Cᵀ S_out = 0 (audit confirmed).
Phase 2 (8-agent workflow, stopped before any agent finished) is unknown to the audit; it contains a Stage-Q CNF generator (`phase2/encodings/genq.py`),
a Stage-Q CP-SAT model (`phase2/method-transfer/q_only_cpsat.py`) and an independent BvLS table. None of it is validated.

## §2 controls: all pass
`orbit_sat.py --m 2 --solve` SAT + lift; `--m 3` UNSAT; `control_bvls.py` light PASSED; **`control_bvls.py --cnf` PASSED** (first run anywhere):
m = 11 CNF 12 606 825 vars / 28 274 730 clauses, planted BvLS assignment SAT (99 s) and lift verifies srg(243,22,1,2), 4/4 flipped bits UNSAT;
memory sampled every ~20 s: last sample 9.77 GB, 2 s before exit, so the true peak is ≥ 9.8 GB and otherwise unknown (the audit's 16–20 GB
estimate is neither confirmed nor refuted; the run fitted in 32 GB). probe99 `validate_k4.py`: 1 solution per mode (audit confirmed).

## §3 CNF reproducibility and one10: settled
Regenerated in Docker (LF) = the audit's SHA-256 table exactly = the old files after `tr -d '\r'` (old files were CRLF).
Sorted diffs: one10 = one + units `1 0`, `-2 0` (a, b of (U0, (1,2,1))); one00/dis00/dis10 likewise. Unit propagation on k14_one:
(a,b) ∈ {(1,0),(0,1),(1,1)} conflict, (0,0) none, so one10 is empty by propagation and one00 ≡ one. On k14_dis: (1,0),(0,1) consistent (block swap), (1,1) conflict.
Appended to `notes/ONE10_PROVENANCE.md`.

## §4 Stage Q (in progress)
Decomposition re-derived: with Q = a + b, S = a − b, (R),(D) ⇔ Q row constraints; (I) ⇔ Q block sums ∧ Cᵀ S = 0 (the two targets of a block are equal);
(P) ⇔ Q-Gram ∧ S-Gram (sum and difference). So full model = Stage Q ∧ Stage S ∧ supp S = {Q = 1}; Stage Q is a sound relaxation.
New code: `code/z2/stage_q.py` (constraint generator, CNF, exact checks, Stage-S CNF, lift), `stage_qs_enum.py` (Q → F2 filter → S → lift loop),
`stage_q_cpsat.py` (CP-SAT from the same generator), `Dockerfile.py` (Linux Python, pinned).
Validation (`stageq_validate.log`): m = 2 Q SAT → S SAT → lift srg(9,4,1,2); m = 3 Q UNSAT; BvLS m = 11 table satisfies every Stage-Q constraint of the CNF
(streaming per-constraint check, exact because with all primaries fixed the CNF splits into independent constraints) and 6/6 random flips are rejected
(43–48 failing constraints each); Stage-S CNF accepts the planted S, rejects one flipped sign; BvLS D(U0) is of type sib. CP-SAT model: m = 2 feasible + lift, m = 3 infeasible.
Stage-Q CNFs (m = 7, Docker, LF): 1 197 042 vars / 2 530 942 clauses each; sha256 in `stageq_cnf_gen.log`.
Runs (started 21:10–21:21): kissat 4.0.4 ×3 (sib/one/dis, 1 CPU, 2 h, statistics on, no proof: kissat is deterministic, an UNSAT case is re-run with
a binary DRAT proof and checked by drat-trim 2e3b2dc, whose chain was smoke-tested); CP-SAT ×3 (3 workers each, 2 h).

### First-row structure of Stage Q (`code/z2/u0_rows.py`, log `u0_rows.log`)
Rows of U0 = (1,2,0) under the row constraints (one 2 at D(U0), ten 1s, block sums), and their orbits under Stab(U0, D(U0)) inside the
relabelling group 2^6 ⋊ S_7 (order 322 560; sigma acts trivially):
| case | |Stab| | rows | orbits (cubes) |
|---|---|---|---|
| sib | 7680 | 3 436 | 13 |
| one | 384 | 36 175 | 149 |
| dis | 384 | 321 878 | 1 164 |
Orbit sizes all divide |Stab| and sum to the row counts. Orbits were computed with 12 random stabiliser elements; re-audit 23:30
(`code/z2/check_symmetry.py`, `check_symmetry.log`): these 12 elements generate the whole Stab(U0, D(U0)) in all three cases, so the orbit counts
13 / 149 / 1 164 are exact. The sib count 3 436 was also re-derived by hand (4-regular multigraphs on blocks 3..7, multiplicity ≤ 2, one e-choice
per single edge): K5 1 024 + two doubled edges 15·2·2⁶ = 1 920 + doubled P3 and doubled K2 30·2⁴ = 480 + doubled C5 12 = 3 436.
Structural remark (sib): the Gram equation for (U0, sister) forces zero common neighbours, so the ten 1s of U0 and the ten 1s of its sister
partition the 20 orbits on blocks 3..7; the sister's row is determined by U0's. In general (Γ²)[U, D(U)] = 2 − Sh(U, D(U)), whence
#triangles(Γ₁) = 126 + 4 n_sib + 2 n_one (n_x = number of D-edges of type x); a consistency identity, not an obstruction.
(The phase-2 count 22 176 for sib concerns full-model rows, signs included; it is not comparable.)

### Cube pipeline (launched 23:11 on the 13 sib cubes)
`code/z2/stage_q_cubes.py` writes one cube per orbit representative (82 unit literals fixing U0's whole row; decode check passed for all
1 326). Exhaustive within each case: Stage Q and the case clause are invariant under Stab(U0, D(U0)). `code/z2/cube_run.sh` (image satbox-proof =
satbox + drat-trim 2e3b2dc): base CNF + units -> kissat (statistics on) -> with proof=1, an UNSAT cube's binary DRAT proof is checked by drat-trim
at once; only the check log and the proof's sha256 are kept. Tested: a real sib cube runs (2 010 conflicts in 5 s, UNKNOWN); a cube made UNSAT on
purpose (row sum violated) gives UNSAT and drat=VERIFIED. Bugs found and fixed while testing: drat-trim prints its verdict as "\rs VERIFIED".

### Stage-Q runs: outcome (2 h each, all UNKNOWN; a timeout is not evidence)
| case | kissat 4.0.4 (1 CPU) | CP-SAT (3 workers) |
|---|---|---|
| sib | s UNKNOWN; 5.46 M conflicts, 28.9 G propagations | UNKNOWN; 9.67 M conflicts, 27.1 M branches |
| one | s UNKNOWN; 6.96 M conflicts, 31.6 G propagations | UNKNOWN; 14.1 M conflicts, 29.1 M branches |
| dis | s UNKNOWN; 5.91 M conflicts, 28.9 G propagations | UNKNOWN; 34 696 conflicts, 4.0 M branches (see note) |
Note (re-audit): the CP-SAT `RESULT` counters are those of ONE worker, and not always the same one. The per-worker tables at the end of each log
show the CDCL worker `no_lp` did 9.67 M (sib) and 14.46 M (dis) conflicts; the dis figure 34 696 is its `default_lp` worker. There is no anomaly.
Reading (hypotheses, not established): ~4 500–5 300 propagations per conflict for kissat suggest the cardinality-over-products encoding is costly,
and ~16 % of variables still free after 2 h shows little global progress; symmetry is the other suspect. Both are to be tested (encoding benchmark,
cubes). Next: the symmetry cubes (13 sib cubes started 23:11, 20 min each, proofs on); see `HANDOFF_2026-09-22.md`.

## Re-audit (23:30), requested by the operator mid-session
**Re-checked, with how:**
- Archive: `sha256sum -c SHA256SUMS.txt` in the archive: all 11 591 entries verify; 11 591 files present; the two uploads are byte-identical (`cmp`) to their source.
- Repo: `git diff --stat`: only `notes/ONE10_PROVENANCE.md` modified, +11 / −0 (append only). All other new files untracked. The cube runner copy in use
  (`conway99-env\stageq\cube_run.sh`) is identical to `code/z2/cube_run.sh`.
- Case split exhaustive (computed, `check_symmetry.log`): |Stab(U0)| = 7 680, orbits on the other 41 orbits of sizes 1, 20, 20 containing (1,2,1),
  (1,3,0), (3,4,0). Cube counts exact (generators generate the full stabiliser). sib row count 3 436 re-derived by hand.
- Decomposition re-derived term by term: (I) for the two elements of block l have equal targets; their sum is the Q block sum (each orbit meeting l
  has one element of the block in rep and the other in σ·rep), their difference is Σ_V C[V,l] S[U,V] (C[U,l] = +1 iff u contains (l,0));
  |u∩v| + |u∩σv| = Sh and |u∩v| − |u∩σv| = G = CCᵀ; the pair (u, σu) is exactly (D); (u,u) is (R). Stage Q is a relaxation of the full model.
- F2 filter re-derived (it is used to skip Stage S, so it must be a proven necessary condition): r − s = 7 is odd, so E_r = (S − sI)/7 is a
  2-integral idempotent with E_r ≡ S (mod 2) (s = −4 even); an idempotent over Z_(2) has the same rank mod 2 as over Q, so rank_F2(S) = f = 27;
  S ≡ [[I, Cᵀ],[C, S_out]] mod 2 and the Schur complement gives rank_F2(S_out + CCᵀ) = 20, i.e. rank_F2((Q mod 2) + Sh) = 20. Sound.
- Identity #triangles(Γ₁) = 126 + 4 n_sib + 2 n_one re-derived (tr Q³ = 1260 both from the Gram equation and from the spectrum).
- Machine: Windows standby on AC and DC = 0 (never), checked with powercfg; the memory watchdog never fired.

**Corrections made (in this file and the handoff):** (1) CP-SAT dis "anomaly" was a reporting artefact (one worker's counters). (2) control_bvls
--cnf memory: ≥ 9.8 GB sampled, true peak unknown. (3) The encoding/symmetry "diagnosis" is a pair of hypotheses. (4) Cube counts exact (caveat removed).
(5) The handoff's "≤ 12 kissat at a time" ignored the 8 GB Docker VM cap: concurrency is bounded by memory, see the handoff. (6) The enumerator ran
~13 min (21:11–21:24), not ~10, without finding a Q.

**New findings:**
- A. Strategy. Stage Q is a relaxation, so its cubes are decisive only if Stage Q is UNSAT; orbit-matrix relaxations often have solutions that do not
  lift. Also, the Stage-Q CNF (1 197 042 vars / 2 530 942 clauses) is larger than the full-model CNF (666 183 / 1 510 448): the Q-Gram constraints
  have 162 product literals with targets up to 4, the full model's (P) constraints 81 literals with targets ≤ 2. The same 1 326 cubes can be run on
  the full model: fixing U0's Q-row in (a,b) is units for Q = 0 (¬a, ¬b) and Q = 2 (a, b) and two clauses for Q = 1 (a ∨ b, ¬a ∨ ¬b); exhaustive by the
  same argument (the full model is invariant under the relabelling group, which permutes Q). A full-model cube is decisive both ways (UNSAT closes it,
  SAT lifts to a graph). Proposed next measurement: the 13 sib cubes on the full model, same 20-min budget, compared with the Stage-Q cubes.
- B. Campaign resources. kissat's memory grows with time (0.4–0.5 GB per sib cube after 17 min; 2.5 GB after 2 h on a whole case) and drat-trim loads
  the whole proof in memory. drat-trim's default time limit is 40 000 s (`-t`); a check that hits it is recorded by the runner as drat=FAILED (the
  cube then counts as not closed and must be re-checked).

**Not re-verified in this session (honest list):** the flip-lemma credit (bibliographic); the order-7 audit (off-scope, not re-run); the omission of
Cᵀ S_out in `dfs_backup.py` (only `cpsat_model.py`'s log count 903 was seen); all phase-2 outputs; the enumerator's loop and CP-SAT's post-processing
at m = 7 (never exercised, since no Q was found).
- C. sib symmetry not used by the cube count (computed, `sib_complement_check.log`): the flip of block 1 swaps U0 and its sister and fixes the 20
  orbits on blocks 3..7, so a U0-row and its complement give equivalent cubes. With canonical forms under the full Stab(U0, D0), classes pair as
  4↔6, 7↔13, 8↔10, 9↔11 (1, 2, 3, 5, 12 are self-complementary): **sib needs 9 cubes, not 13** (lines 1, 2, 3, 4, 5, 7, 8, 9, 12 of `cubes_sib.txt`).
- First cube data (23:31): sib cubes 1, 6, 10 UNKNOWN at 20 min (1 050 600 / 928 501 / 997 919 conflicts). U0-row cubes are too coarse for a
  20-min budget; next steps in `HANDOFF_2026-09-22.md` §2.
- D. Two consequences of Stage Q (derived by hand, checked on the real BvLS m = 11 table, `mod2_mod4_remarks_check.log`; with Q = Γ + 2D and
  k − 2 ≡ 0 mod 4 for both m = 7 and m = 11): (a) Γ² + Γ ≡ Sh (mod 2), so the F2 filter reads rank_F2(Γ²) = 20; (b) (Γ² + Γ + Sh)/2 ≡ ΓD + DΓ + D (mod 2),
  a mod-2 relation between the matching D and Γ. Both follow from Stage Q; no use found yet (recorded so the reasoning is not lost).

## Stop at 23:38 (operator's request, to free the PC)
Cube containers killed (sib cubes 1, 6, 10 complete: UNKNOWN at 1 200 s; 2, 7, 11 interrupted at ~468 s; 3, 4, 5, 8, 9, 12, 13 never ran; logs in
`results/lab_2026-09-22/cubes_sib_stopped_2338/`); background helpers stopped; Docker Desktop stopped; `wsl --shutdown`; `.wslconfig` restored to the
original 4 GB (lab settings kept as `~/.wslconfig.lab-8GB-13cpu`). Free memory after the stop: 22.3 GB of 31.1 GB. Resume from `HANDOFF_2026-09-22.md`.
