# Branche C2 (involution) : programme strictement mathématique

Démarré le 2026-09-25 à la demande de l'opérateur : **aucun solveur (SAT, CP-SAT, recherche exhaustive)**. Les calculs machine ne servent
qu'à *tester* un lemme sur les deux graphes réels de la même famille qui possèdent une involution à un point fixe :
srg(9,4,1,2) (m = 2) et Berlekamp–van Lint–Seidel srg(243,22,1,2) (m = 11, `code/z2/control_bvls.py`).
Règle de cohérence : tout lemme général doit être vrai pour m = 2 et m = 11 ; une contradiction à m = 7 doit utiliser une
arithmétique propre à m = 7 (ici θ − τ = 7 = m).
Consigne opérateur : quand un raisonnement bute, inventer l'outil plutôt que chercher une solution existante.
Étiquettes : PROUVÉ / VÉRIFIÉ (sur m = 2, 11) / CONJECTURÉ / IMPASSE.

## 0. Notations (voir `NOTE_involution_case.md` §2)
Γ = srg(99,14,1,2), σ involution, Fix(σ) = {x}. Blocs B_i = {(i,0),(i,1)} (i = 1..7) de N(x) ; σ échange les deux sommets de
chaque bloc. Sommets extérieurs = étiquettes {a,b} (a, b dans des blocs différents), 84 ; orbites U = (ij,p), 42.
Représentant de U = (ij,p), i < j : u = {(i,0),(j,p)}. a_UW = A[u,w], b_UW = A[u,σw].
S (49×49, orbites intérieures puis extérieures) = [[−I7, Cᵀ],[C, S_out]], S² + S = 12I, spectre 3²⁷, (−4)²².
C (42×7) : C_Ui = +1 si u ∋ (i,0), −1 si u ∋ (i,1), 0 sinon. CᵀC = 12I, CᵀS_out = 0, S_out² + S_out = 12I − B, B = CCᵀ.

## 1. Structure locale (PROUVÉ)
**Lemme 1 (21 carrés).** Pour u extérieur, N(u) ∩ N(σu) = {v, σv} et (u, v, σu, σv) est un 4-cycle induit, σ-invariant, σ = rotation
d'un demi-tour. Les 84 sommets extérieurs sont partitionnés en 21 tels carrés (D est un couplage parfait des 42 orbites).
*Preuve.* μ = 2 et σ-invariance donnent {v,σv} ; v ≁ σv (NOTE §2(b)) ; D symétrique. ∎

**Lemme 2 (triangles extérieurs).** Les 3 étiquettes d'un triangle entièrement extérieur sont deux à deux disjointes.
*Preuve.* Si u ∩ w ∋ c, alors c est le sommet commun de u et w, donc le triangle unique de l'arête uw est {c,u,w}. ∎
Comptage : 7 triangles par x, 84 triangles {c,u,w} (un sommet intérieur), 140 triangles extérieurs (70 σ-orbites).

**Lemme 3 (deux couplages par bloc).** Soit O_i l'ensemble des 12 orbites passant par le bloc i, a = (i,0). Chaque u ∋ a a
exactement un voisin contenant a (couplage m_i) et exactement un voisin contenant a′ (appariement π_i : u ~ σw avec w ∋ a).
m_i et π_i sont deux couplages parfaits de O_i ; R_i = m_i ∪ π_i est 2-régulier (cycles pairs alternés + digones).
Les digones de R_i sont exactement les paires D contenues dans O_i. Pour tout U : Σ_{W∈O_i} Q_UW = 2.
En holonomie signée : une arête U–W de R_i a h = s_UW C_Ui C_Wi = +1 si elle est dans m_i, −1 si elle est dans π_i.

## 2. Un invariant 7-adique nouveau (PROUVÉ)
**Théorème A.** Pour toute srg(99,14,1,2), e′ := rank_F7(A − 3I) est pair.
**Théorème B.** Dans le cas involution, r := rank_F7(S − 3I) est pair ; de façon équivalente
e := rank_F7((S_out − 3I)|_{C⊥}) = r − 7 est impair (1 ≤ e ≤ 15).

*Outil (réseaux propres + formule d'oddité).* Soit X une matrice symétrique entière n×n, X² + X = 12I (valeurs propres 3, −4),
V₋ = ker(X + 4I), P₋ = (3I − X)/7 le projecteur orthogonal sur V₋, K₋ = Zⁿ ∩ V₋.
(i) 7P₋ est entière, donc 7K₋* = 7P₋(Zⁿ) ⊂ K₋ : le groupe discriminant est (Z/7)^d, et K₋*/K₋ ≅ Fⁿ₇ / ker(X̄ − 3) ≅ Im(X̄ − 3),
    donc d = rank_F7(X − 3I).
(ii) P₋ est 2-entière : K₋ ⊗ Z₂ est facteur direct orthogonal de Z₂ⁿ, donc unimodulaire.
(iii) w = P₋(1) est un vecteur caractéristique de K₋ ⊗ Z₂ (x·w = x·1 ≡ x·x mod 2), donc oddity(K₋) ≡ w·w = (3n − σ_X)/7 (mod 8),
    où σ_X = 1ᵀX1 = somme des coefficients.
(iv) Formule d'oddité (réseau défini positif de rang f = dim V₋) : oddity ≡ f + Σ_{p impair} p-excess (mod 8). Seul p = 7 intervient :
    K₋ ⊗ Z₇ = 1^{±(f−d)} ⊥ 7^{ε d}, 7-excess = 6d + 4k (k = 1 ssi ε = −1).
Donc (3n − σ_X)·7⁻¹ ≡ f + 6d + 4k (mod 8).

*Preuve de B.* X = S, n = 49, f = 22. Au-dessus de la diagonale, S a 7·12 + 210 = 294 coefficients ±1, donc
σ_S = tr S + 2Σ_{X<Y} S_XY ≡ −7 + 2·294 ≡ 1 (mod 4). Modulo 4 : w·w ≡ 3(3·49 − 1) ≡ 2, et 22 + 6d ≡ 2 + 2d. Donc d = r est pair.
Le bloc intérieur de S − 3I est −4I ≡ 3I (inversible mod 7), d'où r = 7 + rank(complément de Schur) ; ce complément est
Y = S_out − 3I + 2B (mod 7), nul sur span(C), égal à S_out − 3I sur C⊥, d'où e = r − 7. ∎
*Preuve de A.* X = A − (terme J) : on applique (i)–(iv) à K₋₄ = Z⁹⁹ ∩ E₋₄ (E₋₄ = (3I − A)/7 + J/63, 2-entière, 63E₋₄ ≡ 2(3I − A) mod 7).
1 ∈ E₁₄ donc w = E₋₄(1) = 0 : K₋₄ est pair, oddity 0. La partie 3-adique est 9^{±1} (recollement avec Z·1, norme 99), 3-excess ≡ 8 ≡ 0.
Donc 0 ≡ 44 + 6e′ + 4k (mod 8), e′ pair. ∎

*Contrôles.* m = 2 (Paley 9, p = 3, θ − τ = 3) : même argument, prédiction rank_F3(S − I) pair ; calcul à la main : rang 2. VÉRIFIÉ.
*Cohérence (IMPASSE partielle).* Les décompositions alternatives (K_C ⊥ K₃′ ⊥ K₋₄′ dans l'espace extérieur, partie invariante Q̃,
graphe extérieur H) redonnent les mêmes relations : toutes les formules d'oddité sont liées par l'invariance de l'oddité par
sous-réseau d'indice 2^a. Seule information nouvelle : r pair, et une relation (r/2 + k ≡ n₋ mod 2) entre le signe 7-adique k et
la parité du nombre n₋ d'arêtes négatives de Γ₁ dans la jauge standard.
Pour conclure par cette voie il faut une *seconde* détermination, indépendante, de r mod 2 ou de k.

## 3. Comptages de points fixes (IMPASSE, consigné pour ne pas refaire)
Pour une involution sur un ensemble fini X : |X| ≡ |X^σ| (mod 2). Essayé avec X = sommets, arêtes, triangles, non-arêtes,
4-cycles (2079 ; 21 fixes), 5-cycles (41 580 ; 0 fixe), 6-cycles (429 660 par Ihara–Bass ; 224 fixes : 42 réflexions par deux arêtes
de blocs + 42 hexagones antipodaux à une paire intérieure + 140 hexagones antipodaux extérieurs, ce dernier nombre étant forcé :
20 chemins u–q–r–σu extérieurs par u). Tout est pair et forcé : aucune information.

## 4. Raffinements 2-adiques et reformulation (PROUVÉ ; aucune contradiction)
- Module libre : K₋₄ ⊗ Z₂ ≅ Z₂[C₂]²² (Broué/Krull–Schmidt, χ₋₄(σ) = 0). Pour la moitié invariante β (forme x·(1+σ)y), un vecteur
  caractéristique w vérifie (1+σ)w = c := E₋₄(e_x), d'où β(w,w) = (E₋₄)_xx / 2 = 2/9 ≡ 2 (mod 8) ; det β est un carré.
  Avec oddity(K₋₄) = 0 on obtient **σ_S ≡ 1 (mod 8)**, puis **r/2 + k ≡ 0 (mod 2)**. Même résultat par E₃ (c·c/2 = 3/11).
- MAIS σ_S ≡ 1 (mod 8) se redémontre combinatoirement : pour chaque paire {U,W}, la chaîne P_UW des 2-chemins U–Z–W a une holonomie
  fixée par S_out² + S_out = 12I − B ; chaque arête apparaît 18 fois dans Σ P_UW, d'où Σ_{U<W}((G²)_UW + s_UW + B_UW)/2 ≡ 0,
  soit n₋ pair. Les réseaux ne donnent donc, au-delà de la combinatoire, que l'information 7-adique.
- **Reformulation (Théorème B′).** N := S − 3I mod 7 est symétrique, N² = 0, rang r pair, et la forme x ↦ xᵀNx sur F₇⁴⁹/ker N est
  *hyperbolique* (discriminant (−1)^{r/2}). Pour le graphe entier (Théorème A′) la forme induite par A − 3I mod 7 est de
  discriminant −(−1)^{e′/2} : *non déployée*. La partie σ-invariante est donc non déployée elle aussi.
  Une contradiction viendrait d'un sous-espace totalement isotrope explicite trop grand, ou d'un calcul indépendant du type de Witt.

## 5. Heuristique « 7 | k » (CONJECTURÉ comme piste)
Famille srg(1+2m², 2m, 1, 2), t = θ − τ = √(8m−7). Paramètres admissibles : m = 2, 7, 11, 56, 497 (t = 3, 7, 9, 21, 63).
Un premier p divise à la fois t et k = 2m ssi p = 7 (t² = 8m − 7) ssi 7 | m : c'est le cas exactement pour m = 7, 56, 497, les trois
paramètres dont l'existence est inconnue ; m = 2 et 11 (graphes existants, avec involution) ont t = 3, 9 premiers à 7.
Un argument 7-adique où « k ≡ 0 (mod 7) » intervient est donc le bon type d'argument (il ne peut pas s'appliquer à m = 2, 11).
Là où 7 | m intervient déjà : sur la partie invariante, Nbᵀ Nb = 10I + 2J₇ a les valeurs propres 24 et 10 congrues mod 7 (J₇ nilpotent mod 7).

## 6. Observations sur BvLS (m = 11) — à ne pas prendre pour des lemmes
- Les 55 carrés y sont tous du type « frère » (D(U) = U′). Les types « un bloc commun » et « disjoints » ne sont exclus par aucun
  argument local que j'ai trouvé (les identités Q², S² et le comptage des apex sont automatiquement satisfaits).
- G ∘ (DGD) = 0 (si U ~ W dans Γ₁ alors D(U) ≁ D(W)) ; [S_out, J] ≠ 0 et {S_out, J} ≠ 0 pour la structure complexe J des carrés.

## 7. Théorème D : le cas « tous les carrés frères » est impossible (PROUVÉ, 2026-09-25)
Notation : P = ij une paire de blocs ; ses 4 étiquettes {a,b},{a,b′},{a′,b′},{a′,b} forment deux orbites sœurs P₀, P₁.
Type de P : n_s(P) = Q_{P₀P₁} ∈ {0,1,2} ; n_s = 2 ⟺ D(P₀) = P₁ (carré « frère »).
**Théorème D.** Il n'existe pas de srg(99,14,1,2) avec involution σ telle que D(U) = U′ (orbite sœur) pour toute orbite U.
*Preuve.*
(1) Si D(U) = U′ et u = {a,b} : les deux étiquettes sœurs {a,b′} ∋ a et {a′,b} ∋ a′ sont voisines de u, donc m_a(u), P_a(u),
    m_b(u), P_b(u) sont ces deux étiquettes (condition (I) : un seul voisin contenant a, a′, b, b′). Les 10 autres voisins
    extérieurs de u ne rencontrent ni le bloc i ni le bloc j : ils sont dans des paires de blocs disjointes de P.
(2) Deux voisins y₁ ≠ y₂ de u dans une même paire P′ sont soit σ-conjugués (alors y₁ ∈ N(u) ∩ N(σu) = D(u) ⊂ P, absurde), soit
    partagent un sommet c ; dans un carré frère ils sont adjacents, et c, u seraient deux voisins communs d'une arête (λ = 1). Absurde.
(3) Il y a exactement C(5,2) = 10 paires disjointes de P et 10 voisins lointains : **u a exactement un voisin dans chaque paire
    disjointe** (c'est ici que m = 7 sert : 2m − 4 = C(m−2,2) ⟺ m = 7 ; pour m = 11, BvLS a 18 voisins pour 36 paires).
    Par (3) appliqué aux deux côtés, H[P,P′] est un couplage parfait σ-invariant, qui induit une bijection des orbites P → P′.
(4) Donc, en indexant les orbites par (P, ε) : Q_out = 2·(échange frère) + Σ_{P∩P′=∅} E_{PP′} ⊗ Π_{PP′}, Π ∈ {I₂, X}, et 0 entre
    paires partageant un bloc. Les espaces Sym (constants sur P) et Alt (h(P,ε) = (−1)^ε g(P)) sont invariants :
    Q_out|Sym = A(KG) + 2I et Q_out|Alt = A_χ − 2I, où KG = graphe de Kneser K(7,2) = srg(21,10,3,6), de spectre 10, 1¹⁴, (−4)⁶,
    et A_χ est une signature de KG (χ_PP′ = +1 si Π = I₂, −1 si Π = X).
(5) Spec(Q_out) = {12, (−2)⁶, 3²⁰, (−4)¹⁵} (NOTE §2(e) / DEEP_THOUGHT §1). Sym en prend {12, (−2)⁶, 3¹⁴}, donc Alt porte {3⁶, (−4)¹⁵} :
    A_χ a le spectre {5⁶, (−2)¹⁵}, soit A_χ² = 3A_χ + 10I.
(6) P, P′ disjointes ont 3 voisins communs dans KG : (A_χ²)_{PP′} = 3χ_PP′ force χ_PR χ_RP′ = χ_PP′ pour chacun : **tous les
    triangles de KG sont équilibrés**. P = 12, P′ = 13 (non adjacentes) ont 6 voisins communs, les paires de {4,5,6,7}, groupées en
    3 couples complémentaires {R, R̄} ; R ~ R̄ et les triangles (P,R,R̄), (P′,R,R̄) équilibrés donnent χ_PR χ_RP′ = χ_PR̄ χ_R̄P′.
    Donc (A_χ²)_{PP′} = 2(t₁ + t₂ + t₃) avec tᵢ = ±1 : c'est ±2 ou ±6, jamais 0. Or A_χ² = 3A_χ + 10I exige 0. Contradiction. ∎
*Cohérence.* Pour m = 11 l'étape (3) échoue (18 < 36) : aucun conflit avec BvLS, dont les 55 carrés sont frères.
**Conséquence.** Toute involution devrait avoir au moins un carré de type « un bloc commun » ou « disjoint ».
Types : sib ⟺ n_s = 2 ; « un bloc » ⟹ n_s = 0 ; « disjoint » ⟹ n_s ∈ {0,1} ; n_s = 1 ⟹ D de type disjoint.

## 8. Cas mixte : outils (PROUVÉ) et premières contraintes
Compression sur les paires de blocs. Sym = vecteurs constants sur chaque paire P (21), Alt = h(P,ε) = (−1)^ε g(P) (21) ;
Sym = span(Nb) ⊕ Sym′. T = compression de Q_out sur Sym (T_PP = n_s(P), T_PP′ = e(P,P′)/4, e = nb d'arêtes de H entre les 4+4
étiquettes), Q_A = compression sur Alt ((Q_A)_PP = −n_s(P), (Q_A)_PP′ = (q₀₀ + q₁₁ − q₀₁ − q₁₀)/2 avec q_ab = Q_{P_a P′_b}),
K = bloc Sym′→Alt, K_PP′ = (q_P(P′₀) − q_P(P′₁))/2, q_P(Z) = nb de voisins de z dans P. Comme Nb⊥ est Q-invariant avec Q² + Q = 12 :
  T² + T + KKᵀ = (12I + 4J − Sh)|_Sym  et  Q_A² + Q_A + KᵀK = 12I   (identités exactes).
Sommes de lignes : Σ_{P′∩P=∅} T_PP′ = 8 + n_s(P), Σ_{|P′∩P|=1} T_PP′ = 4 − 2n_s(P).
**Lemme 8.1 (paires frères, PROUVÉ).** Si P est frère : toute étiquette disjointe de P a exactement un voisin dans P, et aucune
étiquette partageant un bloc avec P n'y a de voisin (c'est la perfection de la grille G_P, Lemme 9.1). Donc e(P,R) = 4 pour R
disjointe, T_PR = 1, et la ligne P de K est nulle. Si P et P′ sont frères et disjointes, H[P,P′] est un couplage parfait.
**CORRECTION (2026-09-25, même séance).** Une première version affirmait aussi que la *colonne* P de K est nulle, donc que chaque
étiquette de P a exactement un voisin dans *toute* paire disjointe R. C'est FAUX en général : pour R disjointe non frère, les deux
orbites de P peuvent avoir (2,0) voisins dans R (l'orbite à 2 voisins est alors le μ-partenaire d'une paire partageante non
adjacente de R). L'identité diagonale donne μ_U + μ_U′ = ‖K_{·P}‖², qui est *automatiquement* vraie dans ce cas. Les anciens
lemmes 8.2–8.4 (équilibre des triangles, contrainte sur les couplages de K₄) ne valent donc que si les paires R concernées sont
elles aussi frères ; l'argument de parité exige localement « tout frère ». RETIRÉS en l'état.
**Lemme 8.2 (diagonale, PROUVÉ).** Pour toute paire P : μ_U + μ_U′ + n_s(P) + ‖K_{P·}‖² − ‖K_{·P}‖² = 2, avec
μ_U = Σ_R Q_{UR₀}Q_{UR₁} ; sommé sur P : Σ_U μ_U = 42 − N_s (c'est l'entrée (Q²)_{UU′} = 2 − n_s, rien de neuf).
**Lemme 8.5 (graphe non frère, PROUVÉ).** Soit N ⊂ E(K₇) l'ensemble des paires non frères. Chaque bloc d'une paire X ∈ N porte
une autre paire de N (les voisins proches d'une étiquette de X ne peuvent pas être dans une paire frère partageant un bloc,
par 8.1) : N n'a pas de sommet de degré 1.
Reste à traiter : tout cas où N ≠ ∅.

## 9. Grilles et quasi-perfection (PROUVÉ)
**Lemme 9.1 (grilles parfaites, sans involution).** Si S est un ensemble de 9 sommets induisant 18 arêtes (p. ex. une grille
K₃□K₃ = srg(9,4,1,2)), alors ‖E₋₄1_S‖² = (3·9 − 36)/7 + 81/63 = 0, donc 1_S ∈ E₁₄ ⊕ E₃ et A1_S = 3·1_S + 1 : **tout sommet hors
de S a exactement un voisin dans S**. (Critère général : E₋₄f = 0 ⟺ Af = 3f + (1ᵀf/9)·1.)
Au point fixe x, P = ij est frère ⟺ G_P = {x, a, a′, b, b′} ∪ (4 étiquettes de P) est une grille ; le lemme redonne 8.1 et 8.4.
Pour P quelconque : ‖E₋₄1_{G_P}‖² = (8 − 4n_s(P))/7 et ⟨E₋₄1_{G_P}, E₋₄1_{G_P′}⟩ = (4/7)(T₀ − T)_{PP′} (T₀ = A(KG) + 2I) :
c'est exactement T ≼ T₀ (rien de neuf côté invariant).
**Lemme 9.2 (carré « un bloc commun » presque parfait).** Soit Q = (u,v,σu,σv), u = {a,b} ∈ 12, v = {a,d} ∈ 13, β(Q) = {1,2,3},
F_β = les 24 étiquettes des 6 paires de {4,5,6,7}, w l'apex extérieur de l'arête v–σu.
(i) une étiquette y ∉ Q a au plus un voisin dans Q, sauf les apex (a, a′, w, σw) qui en ont deux (voisins adjacents) ;
(ii) Σ_{y∈F_β} |N(y) ∩ Q| = 24 + 2(ω(u) + ω(v)), où ω(u) = nb de {m_b(u), P_b(u)} dont l'autre élément est dans le bloc 3
     (idem ω(v) avec d et le bloc 2). D'où ω(u) + ω(v) ≤ [w ∈ F_β] ≤ 1 : presque toute étiquette lointaine a exactement un voisin dans Q.
(iii) si ω(u) = 0 : u a 6 voisins lointains dans les 6 paires de {4,5,6,7} ; si ce multigraphe est simple c'est K₄ et les quatre
     « demi-arêtes » (autres éléments de m_b, P_b, y_d, y_d′) tombent dans les quatre blocs lointains, une chacune.
Les 6 paires lointaines d'un carré « un bloc » forment 3 couples complémentaires : c'est la configuration exacte de l'argument
de parité du Théorème D (P = 12, P′ = 13, R ⊂ {4,5,6,7}). Piste : un argument de parité local sur chaque carré non frère.
