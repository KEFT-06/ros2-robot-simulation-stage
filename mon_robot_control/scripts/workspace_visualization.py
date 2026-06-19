#!/usr/bin/env python3
"""RGS2-24 : visualisation workspace offline."""

from pathlib import Path
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from mon_robot_control.robot_kinematics import RobotKinematics


def main():
    n = 120
    q1_range = np.linspace(-math.pi, math.pi, n)
    q2_range = np.linspace(-math.pi, math.pi, n)

    yaw_values = []
    for q1 in q1_range:
        for q2 in q2_range:
            yaw_values.append(RobotKinematics.forward_kinematics_yaw([q1, q2]))

    yaw_values = np.array(yaw_values)

    fig = plt.figure(figsize=(12, 4))

    ax1 = fig.add_subplot(131, projection='3d')
    ax1.scatter([0.0], [0.0], [0.010], s=80)
    ax1.set_title('Position tool_link')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Z (m)')
    ax1.set_xlim(-0.02, 0.02)
    ax1.set_ylim(-0.02, 0.02)
    ax1.set_zlim(0.0, 0.02)

    ax2 = fig.add_subplot(132)
    ax2.hist(np.degrees(yaw_values), bins=72)
    ax2.set_title('Orientations yaw atteignables')
    ax2.set_xlabel('Yaw (deg)')
    ax2.set_ylabel('Nombre de configurations')
    ax2.grid(True)

    ax3 = fig.add_subplot(133)
    theta = np.linspace(-math.pi, math.pi, 360)
    ax3.plot(np.cos(theta), np.sin(theta))
    ax3.set_aspect('equal')
    ax3.set_title("Cercle d'orientation SO(2)")
    ax3.set_xlabel('cos(yaw)')
    ax3.set_ylabel('sin(yaw)')
    ax3.grid(True)

    fig.suptitle('Espace atteignable - ATAWI-3A3 URDF 2 DOF')
    plt.tight_layout()

    output = Path.cwd() / 'workspace_3d.png'
    plt.savefig(output, dpi=150, bbox_inches='tight')

    print('STATISTIQUES espace atteignable:')
    print('  Position tool_link: x=0.000 m, y=0.000 m, z=0.010 m')
    print('  Yaw: [-180, 180] deg')
    print(f'  Graphe sauvegarde: {output}')
    print('RGS2-24 Espace de travail - TERMINE')


if __name__ == '__main__':
    main()
