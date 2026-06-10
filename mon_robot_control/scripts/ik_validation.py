"""
RGS2-22 : Validation Cinématique Inverse (IK)
Robot atawi_3a3 — 3 DOF
"""
import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

# Même robot que FK
robot = rtb.DHRobot([
    rtb.RevoluteDH(d=0.10, a=0, alpha=0,       qlim=[-np.pi,   np.pi]),
    rtb.RevoluteDH(d=0.20, a=0, alpha=np.pi/2, qlim=[-np.pi/2, np.pi/2]),
    rtb.RevoluteDH(d=0.20, a=0, alpha=0,       qlim=[-np.pi,   np.pi]),
], name="atawi_3a3")

print("=" * 55)
print("   ROBOT atawi_3a3 — Cinématique Inverse (IK)")
print("=" * 55)

# ============================================================
# Fonction utilitaire
# ============================================================
def test_ik(target_pos, q_init=None):
    """Calcule IK pour une position cible et vérifie l'erreur."""
    T_target = SE3(target_pos[0], target_pos[1], target_pos[2])
    if q_init is None:
        q_init = [0, 0, 0]
    sol = robot.ikine_LM(T_target, q0=q_init)
    if sol.success:
        T_fk = robot.fkine(sol.q)
        erreur = np.linalg.norm(T_fk.t - np.array(target_pos))
        return sol.q, erreur, True
    return None, None, False

# ============================================================
# TEST IK 1 : Cible au-dessus de la base
# ============================================================
target1 = [0.0, 0.0, 0.50]
q_sol1, err1, ok1 = test_ik(target1)
print(f"\nTEST IK 1 — Cible : {target1} m")
if ok1:
    print(f"  Solution q = {np.round(np.degrees(q_sol1), 2)} degrés")
    print(f"  Erreur position = {err1*1000:.3f} mm ✅")
else:
    print("  ❌ Pas de solution trouvée")

# ============================================================
# TEST IK 2 : Cible décalée
# ============================================================
target2 = [0.15, 0.10, 0.40]
q_sol2, err2, ok2 = test_ik(target2)
print(f"\nTEST IK 2 — Cible : {target2} m")
if ok2:
    print(f"  Solution q = {np.round(np.degrees(q_sol2), 2)} degrés")
    print(f"  Erreur position = {err2*1000:.3f} mm ✅")
else:
    print("  ❌ Pas de solution trouvée")

# ============================================================
# TEST IK 3 : Vérification FK → IK → FK (aller-retour)
# ============================================================
print(f"\n{'='*55}")
print("TEST IK 3 — Vérification FK → IK → FK")
q_original = [np.pi/4, np.pi/6, np.pi/3]
T_from_fk = robot.fkine(q_original)
target3 = list(T_from_fk.t)
q_sol3, err3, ok3 = test_ik(target3, q_init=q_original)
if ok3:
    print(f"  q original  = {np.round(np.degrees(q_original), 2)}°")
    print(f"  q retrouvé  = {np.round(np.degrees(q_sol3), 2)}°")
    print(f"  Erreur pos  = {err3*1000:.3f} mm")
    if err3 < 0.001:
        print("  ✅ IK validée — erreur < 1mm")
    else:
        print("  ⚠️  Erreur > 1mm — vérifier les paramètres DH")

# ============================================================
# Sauvegarde résultats
# ============================================================
with open('/home/karl/ros2_ws/ik_results.txt', 'w') as f:
    f.write("RESULTATS IK — Robot atawi_3a3\n")
    f.write("="*55 + "\n\n")
    for i, (t, q, e, ok) in enumerate([
        (target1, q_sol1, err1, ok1),
        (target2, q_sol2, err2, ok2),
        (target3, q_sol3, err3, ok3)
    ]):
        f.write(f"Test IK {i+1} — Cible : {t}\n")
        if ok:
            f.write(f"  q = {np.round(np.degrees(q),2)} deg\n")
            f.write(f"  Erreur = {e*1000:.3f} mm\n\n")
        else:
            f.write("  Pas de solution\n\n")

print(f"\n✅ Résultats sauvegardés : ~/ros2_ws/ik_results.txt")
print("✅ RGS2-22 IK — TERMINÉ")
EOF