"""
RGS2-24 : Visualisation espace de travail atteignable
Robot atawi_3a3 — 3 DOF
Génère workspace_3d.png exploitable dans le rapport
"""
import numpy as np
import roboticstoolbox as rtb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

robot = rtb.DHRobot([
    rtb.RevoluteDH(d=0.10, a=0, alpha=0,       qlim=[-np.pi,   np.pi]),
    rtb.RevoluteDH(d=0.20, a=0, alpha=np.pi/2, qlim=[-np.pi/2, np.pi/2]),
    rtb.RevoluteDH(d=0.20, a=0, alpha=0,       qlim=[-np.pi,   np.pi]),
], name="atawi_3a3")

print("Calcul de l'espace de travail en cours...")
print("(~500 points, quelques secondes...)")

# Échantillonnage des configurations articulaires
points = []
N = 15  # résolution par joint

q1_range = np.linspace(-np.pi,    np.pi,    N)
q2_range = np.linspace(-np.pi/2,  np.pi/2,  N)
q3_range = np.linspace(-np.pi,    np.pi,    N)

for q1 in q1_range:
    for q2 in q2_range:
        for q3 in q3_range:
            T = robot.fkine([q1, q2, q3])
            points.append(T.t)

points = np.array(points)
print(f"✅ {len(points)} points calculés")

# ============================================================
# Figure 1 : Vue 3D
# ============================================================
fig = plt.figure(figsize=(14, 5))

ax1 = fig.add_subplot(131, projection='3d')
ax1.scatter(points[:,0], points[:,1], points[:,2],
            c=points[:,2], cmap='viridis', s=1, alpha=0.3)
ax1.set_xlabel('X (m)')
ax1.set_ylabel('Y (m)')
ax1.set_zlabel('Z (m)')
ax1.set_title('Espace de travail 3D')

# ============================================================
# Figure 2 : Vue de dessus (XY)
# ============================================================
ax2 = fig.add_subplot(132)
ax2.scatter(points[:,0], points[:,1],
            c=points[:,2], cmap='viridis', s=1, alpha=0.3)
ax2.set_xlabel('X (m)')
ax2.set_ylabel('Y (m)')
ax2.set_title('Vue de dessus (XY)')
ax2.set_aspect('equal')
ax2.grid(True)

# ============================================================
# Figure 3 : Vue de côté (XZ)
# ============================================================
ax3 = fig.add_subplot(133)
ax3.scatter(points[:,0], points[:,2],
            c=points[:,1], cmap='plasma', s=1, alpha=0.3)
ax3.set_xlabel('X (m)')
ax3.set_ylabel('Z (m)')
ax3.set_title('Vue de côté (XZ)')
ax3.set_aspect('equal')
ax3.grid(True)

plt.suptitle('Espace de travail — Robot atawi_3a3 (3 DOF)',
             fontsize=13, fontweight='bold')
plt.tight_layout()

output = '/home/karl/ros2_ws/workspace_3d.png'
plt.savefig(output, dpi=150, bbox_inches='tight')
print(f"✅ Graphe sauvegardé : {output}")

# Stats
print(f"\nSTATISTIQUES espace de travail :")
print(f"  X : [{points[:,0].min():.3f}, {points[:,0].max():.3f}] m")
print(f"  Y : [{points[:,1].min():.3f}, {points[:,1].max():.3f}] m")
print(f"  Z : [{points[:,2].min():.3f}, {points[:,2].max():.3f}] m")
print(f"  Portée max : {np.max(np.linalg.norm(points, axis=1)):.3f} m")
print(f"  Portée min : {np.min(np.linalg.norm(points, axis=1)):.3f} m")
print("✅ RGS2-24 Espace de travail — TERMINÉ")
EOF