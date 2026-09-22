# Ce qui manque / ce qui aiderait (à transmettre à un chercheur)

État : la branche « involution » de Conway-99 est formulée exactement (voir `NOTE_involution_case.md`, rapport LaTeX) et attaquée
par SAT/CP-SAT sans résultat. Rien ci-dessous n'est bloquant pour ce qui est déjà établi ; tout ce qui suit accélérerait ou permettrait de
**décider** la branche (dans un sens ou l'autre, de façon certifiable).

## A. Documents non obtenus (accès institutionnel)
1. **D. Crnković, M. Maksimović**, *Construction of strongly regular graphs having an automorphism group of composite order*,
   Contrib. Discrete Math. 15(1) (2020) 22–41 — exclusion des groupes d'ordre 6 et 9 pour (99,14,1,2) (le résumé, lu le 22/09, cite Z6, S3, Z9, E9). Question précise : leur analyse de Z6
   a-t-elle construit/énuméré des matrices d'orbites pour l'involution (50 orbites) ? Si oui, quel a été le coût et la méthode ?
2. **M. Behbahani, C. Lam**, *Strongly regular graphs with non-trivial automorphisms*, Discrete Math. 311 (2011) 132–144 — version publiée
   de la thèse (que nous avons) ; vérifier si p = 2 y est discuté pour (99,14,1,2) et quelle borne de points fixes est utilisée.
3. (Optionnel) **H. Wilbrink** (1984), note sur l'ordre 11 ; **A. Makhnev, I. Minakova** traduction anglaise DMA 14:2 (2004) 201–210 (nous avons l'original russe).

## B. Outils / logiciels
- **nauty/Traces** (canonical labelling) — indispensable pour un générateur ordonné sur les 42 orbites (rejet d'isomorphes sous 2⁷⋊S₇, ordre 645 120). Sous Windows l'installation de `pynauty` échoue ; un environnement Linux avec nauty compilé suffirait.
- **BreakID** (ou `shatter`) — cassage de symétrie automatique pour les CNF (nos instances ont un groupe de symétrie résiduel énorme).
- **drat-trim / cake_lpr** — pour vérifier une éventuelle preuve UNSAT (certificat indépendant du solveur).
- Solveurs : CaDiCaL et Kissat compilés (déjà faits via Docker), éventuellement **Gimsatul** (Kissat parallèle) ou un portfolio de la SAT Competition.

## C. Calcul
- Une machine Linux **multi-cœurs (32–64) pendant plusieurs jours** : (i) batterie SAT longue sur les 3 cas ; (ii) surtout, le générateur ordonné
  (entrelacement spectral + couplage D + invariant F₂) — c'est là que se décide réellement la branche. Les CNF (29 Mo chacun) sont regénérables
  en 2 s (`code/z2/orbit_sat.py`).

## D. Vérification humaine (le plus précieux)
1. Le **Théorème de rang F₂** (rapport §3) : la preuve est désormais élémentaire (spectre de S + complément de Schur) ; Broué n'est plus nécessaire.
   C'est une conséquence du modèle, pas une obstruction indépendante (révision du 22/09).
2. Les lemmes de rigidité (§2) sont élémentaires mais méritent une relecture (en particulier l'équivalence exacte du modèle (R),(D),(I),(P) avec A²+A−12I=2J).
3. L'**audit Reimbayev** (4 coquilles) : un mail à l'auteur (R. Reimbayev) serait utile — nos corrections sont vérifiées symboliquement et contre le dépôt public.

## E. Questions à poser à des spécialistes (Crnković, Maksimović, Behbahani/Lam, Cesarz/Woldar, Ishida)
- Quelqu'un a-t-il déjà tenté le cas involution de (99,14,1,2) ? (Nous n'en trouvons aucune trace.)
- La méthode « matrices d'orbites + relèvement » est-elle praticable pour 50 orbites avec la structure rigide décrite (7 lignes intérieures forcées,
  une entrée 2 par ligne formant un couplage parfait, blocs contraints) ? Estimation du nombre de matrices d'orbites ?
- L'identité trace–rang d'Ishida a-t-elle une version « réseau libre » utilisable au-delà du rang 20 (par ex. via la forme quadratique mod 2) ?

## F. Ce qui n'est PAS nécessaire
- Les 205+ vagues du dépôt public : seules les vagues 21–23, 43–44 (ordre 6/7) et 206 (trois centres) ont été utilisées, et leurs vérificateurs sont publics.
- Les figures de Reimbayev : l'audit est fait sans elles (appariement de valeurs).
