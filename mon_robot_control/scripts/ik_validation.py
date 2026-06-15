#!/usr/bin/env python3
"""
RGS2-22 : validation de la cinematique inverse (IK).

Le modele URDF actuel possede deux rotations coaxiales autour de Z. L'IK utile
porte donc sur l'orientation yaw; la position de tool_link reste fixe dans ce
modele.
"""

from pathlib import Path
import math


def wrap_pi(angle):
    return math.atan2(math.sin(angle), math.cos(angle))


def ik_yaw(yaw_target):
    yaw = wrap_pi(yaw_target)
    return [yaw / 2.0, yaw / 2.0]


def fk_yaw(q):
    return wrap_pi(q[0] + q[1])


def degrees(values):
    return [round(math.degrees(value), 2) for value in values]


def main():
    targets = [
        ("Yaw nul", 0.0),
        ("Yaw 90 deg", math.pi / 2.0),
        ("Yaw -120 deg", math.radians(-120.0)),
        ("Yaw 180 deg", math.pi),
    ]

    lines = ["RESULTATS IK - Robot ATAWI-3A3 URDF 2 DOF", "=" * 55, ""]

    print("=" * 55)
    print("   ROBOT ATAWI-3A3 - Cinematique Inverse (IK)")
    print("=" * 55)

    for label, target in targets:
        q = ik_yaw(target)
        yaw_check = fk_yaw(q)
        error = abs(wrap_pi(target - yaw_check))
        ok = error < 1e-9

        print(f"\n{label}: cible={math.degrees(target):.2f} deg")
        print(f"  q = {degrees(q)} deg")
        print(f"  erreur yaw = {math.degrees(error):.9f} deg")
        print(f"  statut = {'OK' if ok else 'ECHEC'}")

        lines.extend([
            f"{label}: cible={math.degrees(target):.2f} deg",
            f"  q={degrees(q)} deg",
            f"  erreur yaw={math.degrees(error):.9f} deg",
            f"  statut={'OK' if ok else 'ECHEC'}",
            "",
        ])

    output = Path.cwd() / "ik_results.txt"
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nResultats sauvegardes dans: {output}")
    print("RGS2-22 IK - TERMINE")


if __name__ == "__main__":
    main()
