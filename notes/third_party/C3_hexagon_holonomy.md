# [Third-party note] Conway-99, branche C3 : obstruction locale de relèvement sur les six orbites triangulaires

**Provenance.** Note produite par ChatGPT (session de D. Djematene, 21 septembre 2026), transmise telle quelle.
**Statut de vérification (Claude, 21 septembre 2026, 20:30) :** chaque étape a été relue et le calcul central a été refait
indépendamment (`check_c3_hexagon.py` dans ce dossier) : pour u = (−1,−1,0,1,1,0), v = (1,0,−1,−1,0,1), on trouve exactement
10 supports admissibles, et uᵀDv ≡ −h (mod 3) avec D₀₄ = h, D₀₅ = −h, D₁₅ = h, ce qui force h = 0. **Le lemme est correct.**
**Portée :** un sous-cas de la branche d'ordre 3 sans point fixe (six orbites triangulaires formant un C₆ sans corde) ; il élimine deux des
trois classes d'holonomie, pas la troisième ; il n'exclut ni C₃ ni le motif C₆. Il ne dépend pas de la branche involution.
**Nouveauté :** non établie. Les projets `Lundle22/conway-99-cyclic-lifts` (critère de complétion modulaire pour les relèvements d'ordre 3, modulus (1−ω)³)
et `ibenarb/conway99-research` (recensement des types O3) travaillent au même niveau ; une formulation équivalente pourrait y exister.

---

## Résultat et limites

Soit G un graphe fortement régulier de paramètres (99,14,1,2), muni d'un automorphisme g d'ordre 3 sans point fixe. Supposons que les orbites de g qui induisent un triangle soient exactement T_0,...,T_5, et que le graphe des adjacences entre ces six orbites soit **exactement un cycle C6** (sans corde).

Entre deux orbites triangulaires adjacentes, les arêtes forment un appariement équivariant. En coordonnées (i,a), a dans F3, cet appariement s'écrit (i,a) ~ (i+1, a+ε_i). Alors nécessairement ε_0 + ... + ε_5 = 0 dans F3 : la composée des six appariements autour du cycle est l'identité.

Ce résultat n'exclut pas C3, ni le cas où les six orbites triangulaires forment C6 (l'holonomie nulle n'est pas éliminée). Il ne construit aucun graphe. Il ne suppose pas que la branche involution est exclue.

## Contexte
- Ishida, arXiv:2606.29183v2, prop. 8.7 : a_1(g) = 18 dans le cas d'ordre 3 sans point fixe ⇒ six orbites triangulaires, 27 indépendantes.
- Quotient Q (33×33) : Q·1 = 14·1, Q² + Q = 12I + 6J.

## Blocs binaires
Un sommet extérieur à un triangle ne peut être adjacent à deux de ses sommets (λ = 1). Par équivariance, entre une orbite triangulaire et toute autre orbite, les arêtes sont absentes ou forment un appariement parfait. Avec F l'adjacence du C6 sur les six orbites triangulaires et B la matrice binaire 6×27 vers les orbites indépendantes, le bloc triangulaire du quotient vaut 2I + F et
  B Bᵀ = 6I + 6J − 5F − F² =: G0.   (1)

## Deux contraintes sur chaque colonne de B
u = (−1,−1,0,1,1,0)ᵀ et v = (1,0,−1,−1,0,1)ᵀ vérifient Fu = u, Fv = v, Ju = Jv = 0, donc G0 u = G0 v = 0 ; par (1), ‖Bᵀu‖² = uᵀG0u = 0 ⇒ Bᵀu = 0, de même Bᵀv = 0. Toute colonne s de B satisfait uᵀs = vᵀs = 0 en entiers. (2)
Les dix supports possibles : vide ; une paire de sommets opposés (3) ; un triple alterné (2) ; le complément d'une paire opposée (3) ; les six sommets.

## Compatibilité des phases
Sur les 18 sommets des six triangles, P = adjacence induite, Y = adjacences vers les 81 autres sommets : Y Yᵀ = 12I + 2J − P² − P =: R. (3)
Posons D_ij = Σ_a a·R_{(i,0),(j,a)} (mod 3) ; R symétrique à blocs circulants ⇒ D_ji = −D_ij.
Une orbite extérieure de support s et de phases p_i contribue à R par s_i s_j 1[a = p_j − p_i], donc à D par s tᵀ − t sᵀ (t_i = s_i p_i). Par (2), uᵀ(s tᵀ − t sᵀ)v = 0 ; en sommant sur les 27 orbites : uᵀ D v = 0 dans F3. (4)

## Calcul autour de l'hexagone
En changeant l'origine dans chaque orbite, cinq appariements ont phase 0 et le dernier (T_5 → T_0) a phase h = Σ ε_i. Le calcul de R donne, pour i < j, les seuls moments non nuls D_05 = −h, D_04 = h, D_15 = h (consécutifs : un seul 1 au décalage ; distance 2 : 2 moins l'indicatrice du décalage du chemin ; opposés : constante 2, moment nul). Avec u_0v_5 − u_5v_0 = u_0v_4 − u_4v_0 = u_1v_5 − u_5v_1 = −1 :
  uᵀ D v = (−1)(−h) + (−1)h + (−1)h = −h.
(4) force h = 0. ∎

## Vérification
`check_c3_hexagon.py` (Claude) : reconstruit P et R pour h = 0, 1, 2, vérifie l'antisymétrie de D, les vecteurs propres u, v, G0u = G0v = 0, compte les supports admissibles (10) et évalue uᵀDv : 0, 2, 1 pour h = 0, 1, 2, i.e. −h mod 3.
(La note originale mentionne un vérificateur `verify_c3_hexagon.py` et un fichier `hexagon_verification.json` non transmis ici.)
