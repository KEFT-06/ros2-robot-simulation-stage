# Rapport de validation - RGS2-21, RGS2-22, RGS2-24

Ce document resume les validations cinematiques realisees sans dependance a RViz ou Gazebo.

## RGS2-21 - Cinematique directe FK

Script:

```text
mon_robot_control/scripts/fk_validation.py
```

Commande:

```bash
python3 mon_robot_control/scripts/fk_validation.py
```

Artefact genere:

```text
fk_results.txt
```

Modele valide:

```text
T_world_tool = Rz(q1) * Rz(q2) * Tz(0.010)
```

Configurations testees:

| Test | q1 | q2 | Resultat attendu |
|---|---:|---:|---|
| Position neutre | 0 deg | 0 deg | yaw = 0 deg |
| Tete 90 deg | 90 deg | 0 deg | yaw = 90 deg |
| Rotor 90 deg | 0 deg | 90 deg | yaw = 90 deg |
| Configuration composee | 45 deg | 60 deg | yaw = 105 deg |

Statut: **fait**.

## RGS2-22 - Cinematique inverse IK

Script:

```text
mon_robot_control/scripts/ik_validation.py
```

Commande:

```bash
python3 mon_robot_control/scripts/ik_validation.py
```

Artefact genere:

```text
ik_results.txt
```

Principe:

Le modele URDF actuel possede deux rotations coaxiales. L'IK pertinente porte donc sur l'orientation yaw. Pour une cible `yaw_target`, une solution simple est:

```text
q1 = yaw_target / 2
q2 = yaw_target / 2
```

Tests valides:

| Cible yaw | Solution |
|---:|---|
| 0 deg | q = [0 deg, 0 deg] |
| 90 deg | q = [45 deg, 45 deg] |
| -120 deg | q = [-60 deg, -60 deg] |
| 180 deg | q = [90 deg, 90 deg] |

Statut: **fait**.

## RGS2-24 - Visualisation de l'espace atteignable

Script:

```text
mon_robot_control/scripts/workspace_visualization.py
```

Commande:

```bash
python3 mon_robot_control/scripts/workspace_visualization.py
```

Artefact attendu:

```text
workspace_3d.png
```

Interpretation:

Dans le modele URDF actuel, les deux joints mobiles sont coaxiaux et l'effecteur `tool_link` est fixe a `z = 0.010 m`. L'espace atteignable en position est donc un point, tandis que l'espace atteignable en orientation couvre le yaw sur `[-180 deg, 180 deg]`.

Statut: **fait** si `workspace_3d.png` est genere et conserve avec le projet.

## Conclusion

Les validations FK, IK et espace atteignable sont terminees pour le modele URDF actuel 2 DOF.
