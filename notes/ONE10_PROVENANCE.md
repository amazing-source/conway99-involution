# Provenance du log `results/batch_kissat_one10.log` (s UNSATISFIABLE) — note du 2026-09-22

Faits : commité dans le premier commit (19:00:45), 10 min apres le lancement de la batterie (18:50) ; absent du bilan
de nuit ; aucun script du depot ne genere les CNF one00/one10/dis00/dis10 ; les CNF vivent sur l'AUTRE machine.

Reconstruction (non certaine) : one10 = cas one (D(U0) = (1,3,0)) + clause unitaire "u0 adjacent a la soeur (1,2,1)".
Dans le cas one, la contrainte (I) sature les deux places du bloc 1 par D(U0) : cette adjacence est impossible.
=> UNSAT reel, sous-branche VIDE PAR CONSTRUCTION, elimine 0 % de la branche involution. Le cas "one" reste ouvert.

Test decisif (sur l'autre machine, sans rien ecraser) :
  sha256sum k14_one.cnf k14_one10.cnf
  diff <(sort k14_one.cnf) <(sort k14_one10.cnf)
Prediction : une ou deux clauses unitaires sur a/b du couple (U0, (1,2,1)). Sinon, ne rien conclure avant examen.
Ne pas citer ce log comme un resultat. Details : report/dossier_chercheurs_fr.pdf, section « Anomalies ».

Complement 2026-09-22 (audit) : l'argument « vide par (I) » est confirme independamment. Les empreintes SHA-256 des CNF regenerees
(k14_sib/one/dis/none) et la procedure complete du test sont dans LAB_INSTRUCTIONS.md §3 (generer et hacher en LF, sous Docker/WSL).
