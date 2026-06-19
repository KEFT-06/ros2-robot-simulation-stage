#!/usr/bin/env python3
"""Genere des meshes STL placeholder (boites) pour demo sans CAO."""

from pathlib import Path

MESH_DIR = Path(__file__).resolve().parent.parent / 'meshes'

FILES = [
    'Body.stl', 'Handle_1.stl', 'Handle_2.stl',
    'Hexnut_1.stl', 'Hexnut_2.stl', 'Vis_1.stl', 'Vis_2.stl',
    'L2_1.stl', 'L2_2.stl', 'L2_3.stl', 'L2_4.stl',
    'part2.stl', 'Blade_1.stl', 'Blade_2.stl', 'Blade_3.stl', 'Blade_4.stl',
]

SIZES = {
    'Body.stl': (0.112, 0.063, 0.194),
    'Handle_1.stl': (0.010, 0.008, 0.025),
    'Handle_2.stl': (0.010, 0.008, 0.025),
    'Hexnut_1.stl': (0.008, 0.008, 0.004),
    'Hexnut_2.stl': (0.008, 0.008, 0.004),
    'Vis_1.stl': (0.004, 0.004, 0.012),
    'Vis_2.stl': (0.004, 0.004, 0.012),
    'part2.stl': (0.101, 0.043, 0.039),
    'Blade_1.stl': (0.030, 0.006, 0.006),
    'Blade_2.stl': (0.030, 0.006, 0.006),
    'Blade_3.stl': (0.030, 0.006, 0.006),
    'Blade_4.stl': (0.030, 0.006, 0.006),
}
DEFAULT_SIZE = (0.010, 0.010, 0.010)


def box_triangles(sx, sy, sz):
    hx, hy, hz = sx / 2, sy / 2, sz / 2
    v = [
        (-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
        (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz),
    ]
    faces = [
        (0, 1, 2), (0, 2, 3), (4, 6, 5), (4, 7, 6),
        (0, 4, 5), (0, 5, 1), (2, 6, 7), (2, 7, 3),
        (0, 3, 7), (0, 7, 4), (1, 5, 6), (1, 6, 2),
    ]
    return [(v[a], v[b], v[c]) for a, b, c in faces]


def write_stl(path: Path, sx: float, sy: float, sz: float) -> None:
    lines = [f'solid {path.stem}']
    for tri in box_triangles(sx, sy, sz):
        lines.append('  facet normal 0 0 0')
        lines.append('    outer loop')
        for x, y, z in tri:
            lines.append(f'      vertex {x:.6f} {y:.6f} {z:.6f}')
        lines.append('    endloop')
        lines.append('  endfacet')
    lines.append(f'endsolid {path.stem}')
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> None:
    MESH_DIR.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        sx, sy, sz = SIZES.get(name, DEFAULT_SIZE)
        write_stl(MESH_DIR / name, sx, sy, sz)
        print(f'  {name}')
    print(f'OK: {len(FILES)} meshes -> {MESH_DIR}')


if __name__ == '__main__':
    main()
