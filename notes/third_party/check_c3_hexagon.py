"""Independent check of the C3 hexagon holonomy lemma (third-party note, 2026-09-21).
Six triangular orbits T_0..T_5 of an order-3 fixed-point-free automorphism, adjacent in a chordless C6 with matching shifts
eps_i (normalised: 0,0,0,0,0,h). P = induced adjacency on the 18 triangle vertices; R = 12I + 2J - P^2 - P; D_ij = sum_a a*R[(i,0),(j,a)] mod 3.
Claim: u^T D v = -h (mod 3) for u=(-1,-1,0,1,1,0), v=(1,0,-1,-1,0,1); the note shows u^T D v must be 0, hence h=0."""
import numpy as np, itertools
def check(h):
    idx = lambda i, a: 3 * i + a % 3
    P = np.zeros((18, 18), dtype=int)
    for i in range(6):
        for a in range(3):
            for b in range(3):
                if a != b: P[idx(i, a), idx(i, b)] = 1
    eps = [0, 0, 0, 0, 0, h]
    for i in range(6):
        j = (i + 1) % 6
        for a in range(3):
            P[idx(i, a), idx(j, a + eps[i])] = P[idx(j, a + eps[i]), idx(i, a)] = 1
    R = 12 * np.eye(18, dtype=int) + 2 * np.ones((18, 18), dtype=int) - P @ P - P
    D = np.zeros((6, 6), dtype=int)
    for i in range(6):
        for j in range(6):
            D[i, j] = sum(a * R[idx(i, 0), idx(j, a)] for a in range(3)) % 3
    assert np.array_equal(D, (-D.T) % 3), "D not antisymmetric"
    u = np.array([-1, -1, 0, 1, 1, 0]); v = np.array([1, 0, -1, -1, 0, 1])
    F = np.zeros((6, 6), dtype=int)
    for i in range(6): F[i, (i + 1) % 6] = F[(i + 1) % 6, i] = 1
    assert np.array_equal(F @ u, u) and np.array_equal(F @ v, v) and u.sum() == 0 and v.sum() == 0
    G0 = 6 * np.eye(6, dtype=int) + 6 * np.ones((6, 6), dtype=int) - 5 * F - F @ F
    assert not (G0 @ u).any() and not (G0 @ v).any()
    return int(u @ D @ v) % 3, {(i, j): int(D[i, j]) for i in range(6) for j in range(i + 1, 6) if D[i, j]}
sup = [s for s in itertools.product((0, 1), repeat=6) if -s[0]-s[1]+s[3]+s[4] == 0 and s[0]-s[2]-s[3]+s[5] == 0]
print("admissible supports (kernel of u,v):", len(sup))
for h in range(3):
    val, nz = check(h); print("h=%d: u^T D v = %d (mod 3)  nonzero D_ij: %s" % (h, val, nz))
