#!/usr/bin/env python3
"""Validation cinematique offline ATAWI-3A3."""

import math

from mon_robot_control.robot_kinematics import RobotKinematics


def print_configuration(robot, q):
    print(f"\n{'=' * 60}")
    print('CONFIGURATION ARTICULAIRE URDF 2 DOF')
    print(f"{'=' * 60}")

    for name, qi, q_min, q_max in zip(
        RobotKinematics.JOINT_NAMES, q, RobotKinematics.Q_MIN, RobotKinematics.Q_MAX
    ):
        print(
            f"{name:20s}: {math.degrees(qi):8.2f} deg "
            f"[{math.degrees(q_min):7.2f}, {math.degrees(q_max):7.2f}]"
        )

    pos, orient = robot.forward_kinematics(q)
    yaw = math.atan2(orient[1][0], orient[0][0])

    print(f"\n{'POSITION TOOL_LINK':^60}")
    print(f'  X: {pos[0]:.4f} m')
    print(f'  Y: {pos[1]:.4f} m')
    print(f'  Z: {pos[2]:.4f} m')
    print(f'  Yaw total: {math.degrees(yaw):.2f} deg')

    print(f"\n{'MATRICE DE ROTATION':^60}")
    for row in orient:
        print(f'  [{row[0]:7.4f} {row[1]:7.4f} {row[2]:7.4f}]')


def main():
    print('\n' + '=' * 60)
    print('   VALIDATION CINEMATIQUE - ATAWI-3A3 URDF 2 DOF')
    print('=' * 60)

    robot = RobotKinematics()

    tests = [
        ('Configuration zero', [0.0, 0.0]),
        ('Tete 90 deg', [math.pi / 2.0, 0.0]),
        ('Rotor 90 deg', [0.0, math.pi / 2.0]),
        ('Configuration composee', [math.pi / 4.0, math.pi / 3.0]),
    ]

    for label, q in tests:
        print(f'\n[TEST] {label}')
        print_configuration(robot, q)

    print('\n[TEST] IK orientation - yaw cible 120 deg')
    target_yaw = math.radians(120.0)
    q_solution, success = robot.inverse_kinematics_orientation(target_yaw)
    if success:
        print_configuration(robot, q_solution)
        yaw = robot.forward_kinematics_yaw(q_solution)
        error = abs(robot.wrap_pi(target_yaw - yaw))
        print(f'\nErreur yaw: {math.degrees(error):.6f} deg')
    else:
        print('Pas de solution dans les limites articulaires')


if __name__ == '__main__':
    main()
