#!/usr/bin/env python3
"""RGS2-22 : validation IK offline."""

from pathlib import Path
import math

from mon_robot_control.robot_kinematics import RobotKinematics


def degrees(values):
    return [round(math.degrees(value), 2) for value in values]


def main():
    targets = [
        ('Yaw nul', 0.0),
        ('Yaw 90 deg', math.pi / 2.0),
        ('Yaw -120 deg', math.radians(-120.0)),
        ('Yaw 180 deg', math.pi),
    ]

    lines = ['RESULTATS IK - Robot ATAWI-3A3 URDF 2 DOF', '=' * 55, '']

    print('=' * 55)
    print('   ROBOT ATAWI-3A3 - Cinematique Inverse (IK)')
    print('=' * 55)

    for label, target in targets:
        q, ok_limits = RobotKinematics.inverse_kinematics_orientation(target)
        yaw_check = RobotKinematics.forward_kinematics_yaw(q)
        error = abs(RobotKinematics.wrap_pi(target - yaw_check))
        ok = ok_limits and error < 1e-9

        print(f'\n{label}: cible={math.degrees(target):.2f} deg')
        print(f'  q = {degrees(q)} deg')
        print(f'  erreur yaw = {math.degrees(error):.9f} deg')
        print(f"  statut = {'OK' if ok else 'ECHEC'}")

        lines.extend([
            f'{label}: cible={math.degrees(target):.2f} deg',
            f'  q={degrees(q)} deg',
            f'  erreur yaw={math.degrees(error):.9f} deg',
            f"  statut={'OK' if ok else 'ECHEC'}",
            '',
        ])

    output = Path.cwd() / 'ik_results.txt'
    output.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nResultats sauvegardes dans: {output}')
    print('RGS2-22 IK - TERMINE')


if __name__ == '__main__':
    main()
