# Vérification (Claude, 21 septembre 2026, ~21:00)

Paquet reçu de ChatGPT via D. Djematene (`conway_c3_suivi_generalisation.zip`). Hachages SHA256SUMS_SUIVI.txt : tous OK.

1. **Pont (4) → (3)** : vérifié par dérivation indépendante. Pour des blocs 3×3 circulants, le premier moment m(X)_{ij} = Σ_a a·x_a (mod 3)
   satisfait la règle de Leibniz m(XY) = m(X)Q(Y) + Q(X)m(Y) où Q est le quotient (somme des blocs). Appliquée à A²+A−12I = 2J (moments de 12I et 2J nuls),
   elle donne MQ + QM + M ≡ 0 (mod 3), soit l'équation linéaire (4). Son bloc triangulaire est 5E + FE + EF − BVᵀ + VBᵀ ; la contraction par une base K
   du noyau entier de G0 = BBᵀ annule les termes mixtes (BᵀK = 0 car uᵀG0u = ‖Bᵀu‖²), ce qui redonne exactement (3). Correct.
2. **Saturation des noyaux entiers** : re-calculée indépendamment avec sympy (noyau rationnel, dénominateurs chassés, forme normale de Smith :
   tous les facteurs invariants valent 1 ⇔ base saturée) — `crosscheck.py`. Correct pour les 44 cas PSD.
3. **Recensement** : reproduit indépendamment (numpy/sympy, moments par construction directe des matrices 18×18, rang sur GF(3)) :
   87 (entrée négative) / 25 (non PSD) / 44 (PSD) ; nullités {0: 29, 1: 13, 2: 2} ; unique motif à équation non triviale = C6 (masque 21041), rang 1.
   Les deux vérificateurs livrés rejouent PASS.

**Conclusion** : les deux affirmations tiennent. Limite à retenir : le filtre « noyau entier du Gram des six orbites triangulaires → moment antisymétrique »
est saturé par C6 ; inutile de relancer cette généralisation. Non testés ici : l'équation quadratique de Lundle22, les sous-Grams incluant des orbites
indépendantes, et la faisabilité de la factorisation binaire B des 44 Grams PSD (les 44 « survivants » ne sont pas 44 quotients réalisables).
