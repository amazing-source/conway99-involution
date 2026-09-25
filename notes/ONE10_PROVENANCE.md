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

Complement 2026-09-22 (soir, session labo, machine de calcul) : test decisif fait, prediction confirmee.
- Transcription de la session d'origine (eeaf2d22, 2026-09-21 16:51 UTC) : les sous-cas ont ete ecrits par un script en ligne,
  a, b = A[0,1], B[0,1] (couple U0 / soeur (1,2,1)) ; one10 = one + clauses unitaires [1], [-2] ; one00 = one + [-1], [-2] ; idem dis00/dis10.
- Empreintes (generees sous Docker, LF) : k14_sib/one/dis/none regeneres = table de LAB_INSTRUCTIONS.md §3, et = anciens fichiers
  apres tr -d '\r' (les anciens etaient CRLF). diff trie : one -> one10 = exactement « 1 0 », « -2 0 » et l'en-tete (1510448 -> 1510450) ;
  one00, dis00, dis10 : idem avec leurs unites. Journal : results/lab_2026-09-22/s3_cnf_hashes_and_diffs.log.
- Propagation unitaire (cadical195) sur k14_one : (a,b) = (1,0), (0,1), (1,1) -> conflit ; (0,0) -> pas de conflit. Donc one10 est vide
  par propagation et one00 est equivalent au cas one tout entier. Sur k14_dis : (1,0) et (0,1) sans conflit (echange des blocs 1 et 2),
  (1,1) conflit : le sous-decoupage dis00/dis10 est sain.
- Conclusion inchangee : le log one10 (UNSAT) n'elimine rien et ne doit pas etre cite.
