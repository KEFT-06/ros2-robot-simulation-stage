#!/usr/bin/env python3
"""RGS2-21 : validation FK offline."""

from pathlib import Path
import math

from mon_robot_control.robot_kinematics import RobotKinematics


def degrees(values):
    return [round(math.degrees(value), 2) for value in values]


def print_matrix(yaw, z):
    c = math.cos(yaw)
    s = math.sin(yaw)
    matrix = [
        [c, -s, 0.0, 0.0],
        [s, c, 0.0, 0.0],
        [0.0, 0.0, 1.0, z],
        [0.0, 0.0, 0.0, 1.0],
    ]
    for row in matrix:
        print('  [' + ' '.join(f'{value:8.4f}' for value in row) + ']')


def main():
    tests = [
        ('Position neutre', [0.0, 0.0]),
        ('Tete 90 deg', [math.pi / 2.0, 0.0]),
        ('Rotor 90 deg', [0.0, math.pi / 2.0]),
        ('Configuration composee', [math.pi / 4.0, math.pi / 3.0]),
    ]

    lines = ['RESULTATS FK - Robot ATAWI-3A3 URDF 2 DOF', '=' * 55, '']

    print('=' * 55)
    print('   ROBOT ATAWI-3A3 - Cinematique Directe (FK)')
    print('=' * 55)

    for label, q in tests:
        pos, _ = RobotKinematics.forward_kinematics(q)
        yaw = RobotKinematics.forward_kinematics_yaw(q)
        deg = degrees(q)

        print(f'\n{label}: q = {deg} deg')
        print_matrix(yaw, pos[2])
        print(f'Position tool_link: x={pos[0]:.4f} y={pos[1]:.4f} z={pos[2]:.4f} m')
        print(f'Yaw total: {math.degrees(yaw):.2f} deg')

        lines.extend([
            f'{label}: q = {deg} deg',
            f'  x={pos[0]:.4f}m y={pos[1]:.4f}m z={pos[2]:.4f}m yaw={math.degrees(yaw):.2f}deg',
            '',
        ])

    results_dir = Path(__file__).resolve().parent.parent / 'results'
    results_dir.mkdir(parents=True, exist_ok=True)
    output = results_dir / 'fk_results.txt'
    output.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nResultats sauvegardes dans: {output}')
    print('RGS2-21 FK - TERMINE')


if __name__ == '__main__':
    main()
