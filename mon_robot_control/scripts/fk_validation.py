#!/usr/bin/env python3
"""
RGS2-21 : validation de la cinematique directe (FK).

Modele utilise: URDF actuel ATAWI-3A3, 2 DOF coaxiaux autour de Z.
"""

from pathlib import Path
import math


def transform_from_yaw_z(yaw, z):
    c = math.cos(yaw)
    s = math.sin(yaw)
    return [
        [c, -s, 0.0, 0.0],
        [s, c, 0.0, 0.0],
        [0.0, 0.0, 1.0, z],
        [0.0, 0.0, 0.0, 1.0],
    ]


def fk(q):
    q1, q2 = q
    return transform_from_yaw_z(q1 + q2, 0.010)


def degrees(values):
    return [round(math.degrees(value), 2) for value in values]


def print_matrix(matrix):
    for row in matrix:
        print("  [" + " ".join(f"{value:8.4f}" for value in row) + "]")


def main():
    tests = [
        ("Position neutre", [0.0, 0.0]),
        ("Tete 90 deg", [math.pi / 2.0, 0.0]),
        ("Rotor 90 deg", [0.0, math.pi / 2.0]),
        ("Configuration composee", [math.pi / 4.0, math.pi / 3.0]),
    ]

    lines = ["RESULTATS FK - Robot ATAWI-3A3 URDF 2 DOF", "=" * 55, ""]

    print("=" * 55)
    print("   ROBOT ATAWI-3A3 - Cinematique Directe (FK)")
    print("=" * 55)

    for label, q in tests:
        transform = fk(q)
        pos = [transform[0][3], transform[1][3], transform[2][3]]
        yaw = math.atan2(transform[1][0], transform[0][0])
        deg = degrees(q)

        print(f"\n{label}: q = {deg} deg")
        print_matrix(transform)
        print(f"Position tool_link: x={pos[0]:.4f} y={pos[1]:.4f} z={pos[2]:.4f} m")
        print(f"Yaw total: {math.degrees(yaw):.2f} deg")

        lines.extend([
            f"{label}: q = {deg} deg",
            f"  x={pos[0]:.4f}m y={pos[1]:.4f}m z={pos[2]:.4f}m yaw={math.degrees(yaw):.2f}deg",
            "",
        ])

    output = Path.cwd() / "fk_results.txt"
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nResultats sauvegardes dans: {output}")
    print("RGS2-21 FK - TERMINE")


if __name__ == "__main__":
    main()
