"""
RGS2-21 : Validation Cinématique Directe (FK)
Robot atawi_3a3 — 3 DOF
Paramètres DH extraits de l'URDF
"""
import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3
import matplotlib
matplotlib.use('Agg')  # pas besoin d'écran
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# Paramètres Denavit-Hartenberg du robot atawi_3a3
# Extraits de l'URDF :
#   joint1_rotation : origine z=0.10, axe Z
#   joint2_flexion  : origine z=0.20, axe Y
#   joint3_wrist    : origine z=0.20, axe Z
#
# Format DH standard : [d, a, alpha]
# d     = translation sur Z
# a     = translation sur X
# alpha = rotation sur X
# theta = variable articulaire (q)
# ============================================================

robot = rtb.DHRobot([
    rtb.RevoluteDH(d=0.10, a=0,    alpha=0,       qlim=[-np.pi,    np.pi]),
    rtb.RevoluteDH(d=0.20, a=0,    alpha=np.pi/2, qlim=[-np.pi/2,  np.pi/2]),
    rtb.RevoluteDH(d=0.20, a=0,    alpha=0,       qlim=[-np.pi,    np.pi]),
], name="atawi_3a3")

print("=" * 55)
print("   ROBOT atawi_3a3 — Cinématique Directe (FK)")
print("=" * 55)
print(robot)

# ============================================================
# TEST 1 : Position neutre [0, 0, 0]
# ============================================================
q0 = [0.0, 0.0, 0.0]
T0 = robot.fkine(q0)
print(f"\n{'='*55}")
print(f"TEST 1 — Position neutre : q = {q0}")
print(f"Matrice de transformation T :")
print(T0)
print(f"Position effecteur (x, y, z) en mètres :")
print(f"  x = {T0.t[0]:.4f} m")
print(f"  y = {T0.t[1]:.4f} m")
print(f"  z = {T0.t[2]:.4f} m")

# ============================================================
# TEST 2 : joint1=90°, joint2=0°, joint3=0°
# ============================================================
q1 = [np.pi/2, 0.0, 0.0]
T1 = robot.fkine(q1)
print(f"\n{'='*55}")
print(f"TEST 2 — Rotation base : q = [90°, 0°, 0°]")
print(f"Position effecteur :")
print(f"  x = {T1.t[0]:.4f} m")
print(f"  y = {T1.t[1]:.4f} m")
print(f"  z = {T1.t[2]:.4f} m")

# ============================================================
# TEST 3 : joint1=90°, joint2=45°, joint3=0°
# ============================================================
q2 = [np.pi/2, np.pi/4, 0.0]
T2 = robot.fkine(q2)
print(f"\n{'='*55}")
print(f"TEST 3 — Flexion bras : q = [90°, 45°, 0°]")
print(f"Position effecteur :")
print(f"  x = {T2.t[0]:.4f} m")
print(f"  y = {T2.t[1]:.4f} m")
print(f"  z = {T2.t[2]:.4f} m")

# ============================================================
# TEST 4 : joint1=45°, joint2=30°, joint3=90°
# ============================================================
q3 = [np.pi/4, np.pi/6, np.pi/2]
T3 = robot.fkine(q3)
print(f"\n{'='*55}")
print(f"TEST 4 — Configuration complexe : q = [45°, 30°, 90°]")
print(f"Position effecteur :")
print(f"  x = {T3.t[0]:.4f} m")
print(f"  y = {T3.t[1]:.4f} m")
print(f"  z = {T3.t[2]:.4f} m")

# ============================================================
# Calcul du Jacobien
# ============================================================
print(f"\n{'='*55}")
print("JACOBIEN en position neutre :")
J = robot.jacob0(q0)
print(J)

# ============================================================
# Export des résultats dans un fichier texte
# ============================================================
with open('/home/karl/ros2_ws/fk_results.txt', 'w') as f:
    f.write("RESULTATS FK — Robot atawi_3a3\n")
    f.write("="*55 + "\n\n")
    for i, (q, T) in enumerate([(q0,T0),(q1,T1),(q2,T2),(q3,T3)]):
        f.write(f"Test {i+1} : q = {np.round(np.degrees(q),1)} deg\n")
        f.write(f"  x={T.t[0]:.4f}m  y={T.t[1]:.4f}m  z={T.t[2]:.4f}m\n\n")

print(f"\n✅ Résultats sauvegardés dans : ~/ros2_ws/fk_results.txt")
print("✅ RGS2-21 FK — TERMINÉ")
EOF
