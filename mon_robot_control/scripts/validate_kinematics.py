#!/usr/bin/env python3
"""
Validation cinematique du modele URDF actuel ATAWI-3A3.

Le fichier URDF expose deux articulations commandees:
  - joint1_head  : rotation Z de la tete
  - joint2_rotor : rotation Z du rotor

Les deux axes sont coaxiaux dans l'URDF actuel. La position de tool_link est donc
fixee a 10 mm sur Z par rapport au rotor; les joints modifient l'orientation.
"""

import math


class RobotKinematics:
    """Cinematique directe et inverse coherente avec l'URDF 2 DOF."""

    def __init__(self):
        self.joint_names = ["joint1_head", "joint2_rotor"]
        self.q_min = [-math.pi, -math.pi]
        self.q_max = [math.pi, math.pi]
        self.tool_offset = [0.0, 0.0, 0.010]

    @staticmethod
    def rotz(theta):
        c = math.cos(theta)
        s = math.sin(theta)
        return [
            [c, -s, 0.0],
            [s, c, 0.0],
            [0.0, 0.0, 1.0],
        ]

    def forward_kinematics(self, q):
        if len(q) != 2:
            raise ValueError("Le modele URDF actuel attend 2 angles: [joint1_head, joint2_rotor]")

        for i, (qi, q_min, q_max) in enumerate(zip(q, self.q_min, self.q_max)):
            if not q_min <= qi <= q_max:
                print(
                    f"Avertissement: {self.joint_names[i]} = {math.degrees(qi):.2f} deg "
                    f"hors limites [{math.degrees(q_min):.2f}, {math.degrees(q_max):.2f}] deg"
                )

        yaw = q[0] + q[1]
        return self.tool_offset[:], self.rotz(yaw)

    def inverse_kinematics_orientation(self, yaw_target):
        yaw = math.atan2(math.sin(yaw_target), math.cos(yaw_target))
        q = [yaw / 2.0, yaw / 2.0]
        ok = all(q_min <= qi <= q_max for qi, q_min, q_max in zip(q, self.q_min, self.q_max))
        return q, ok

    def print_configuration(self, q):
        print(f"\n{'=' * 60}")
        print("CONFIGURATION ARTICULAIRE URDF 2 DOF")
        print(f"{'=' * 60}")

        for name, qi, q_min, q_max in zip(self.joint_names, q, self.q_min, self.q_max):
            print(
                f"{name:20s}: {math.degrees(qi):8.2f} deg "
                f"[{math.degrees(q_min):7.2f}, {math.degrees(q_max):7.2f}]"
            )

        pos, orient = self.forward_kinematics(q)
        yaw = math.atan2(orient[1][0], orient[0][0])

        print(f"\n{'POSITION TOOL_LINK':^60}")
        print(f"  X: {pos[0]:.4f} m")
        print(f"  Y: {pos[1]:.4f} m")
        print(f"  Z: {pos[2]:.4f} m")
        print(f"  Yaw total: {math.degrees(yaw):.2f} deg")

        print(f"\n{'MATRICE DE ROTATION':^60}")
        for row in orient:
            print(f"  [{row[0]:7.4f} {row[1]:7.4f} {row[2]:7.4f}]")


def main():
    print("\n" + "=" * 60)
    print("   VALIDATION CINEMATIQUE - ATAWI-3A3 URDF 2 DOF")
    print("=" * 60)

    robot = RobotKinematics()

    tests = [
        ("Configuration zero", [0.0, 0.0]),
        ("Tete 90 deg", [math.pi / 2.0, 0.0]),
        ("Rotor 90 deg", [0.0, math.pi / 2.0]),
        ("Configuration composee", [math.pi / 4.0, math.pi / 3.0]),
    ]

    for label, q in tests:
        print(f"\n[TEST] {label}")
        robot.print_configuration(q)

    print("\n[TEST] IK orientation - yaw cible 120 deg")
    target_yaw = math.radians(120.0)
    q_solution, success = robot.inverse_kinematics_orientation(target_yaw)
    if success:
        robot.print_configuration(q_solution)
        _, orientation = robot.forward_kinematics(q_solution)
        yaw = math.atan2(orientation[1][0], orientation[0][0])
        error = abs(math.atan2(math.sin(target_yaw - yaw), math.cos(target_yaw - yaw)))
        print(f"\nErreur yaw: {math.degrees(error):.6f} deg")
    else:
        print("Pas de solution dans les limites articulaires")


if __name__ == "__main__":
    main()
