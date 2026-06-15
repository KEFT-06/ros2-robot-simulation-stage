# RGS2-29 - Parametres cinematiques du robot ATAWI-3A3

Ce document liste les liens, joints, reperes et parametres cinematiques utilises par le modele URDF actuel.

## Modele retenu

Le fichier de reference est:

```text
mon_robot_description/urdf/mon_robot.urdf.xacro
```

Le modele commandable actuel est un robot **2 DOF**. Les fichiers STL representent l'assemblage mecanique complet, mais la cinematique est definie uniquement par les joints URDF.

## Joints commandables

| Joint | Type | Parent | Enfant | Origine xyz | Axe | Limites |
|---|---|---|---|---|---|---|
| `joint1_head` | revolute | `base_link` | `head_link` | `0 0 0` | `0 0 1` | `[-pi, pi]` |
| `joint2_rotor` | revolute | `head_link` | `rotor_link` | `0 0 0` | `0 0 1` | `[-pi, pi]` |

Les deux axes de rotation sont coaxiaux autour de Z.

## Liens principaux

| Link | Role |
|---|---|
| `world` | Repere fixe global |
| `base_link` | Corps principal du robot |
| `head_link` | Tete orientable |
| `rotor_link` | Rotor / support des pales |
| `tool_link` | Repere effecteur final |

## Joints fixes

Les pieces suivantes sont montees par joints fixes:

- `world_to_base`
- `handle1_joint`
- `handle2_joint`
- `hexnut1_joint`
- `hexnut2_joint`
- `vis1_joint`
- `vis2_joint`
- `l2_1_joint`
- `l2_2_joint`
- `l2_3_joint`
- `l2_4_joint`
- `blade2_joint`
- `blade3_joint`
- `blade4_joint`
- `tool_joint`

## Parametres DH simplifiés

Comme les deux articulations mobiles sont coaxiales, le modele cinematique peut etre represente par deux rotations successives autour de Z.

| i | Joint | theta | d | a | alpha |
|---|---|---|---|---|---|
| 1 | `joint1_head` | `q1` | `0` | `0` | `0` |
| 2 | `joint2_rotor` | `q2` | `0` | `0` | `0` |
| Tool | `tool_joint` | `0` | `0.010 m` | `0` | `0` |

La pose de `tool_link` est donc:

```text
T_world_tool = Rz(q1) * Rz(q2) * Tz(0.010)
```

La position de `tool_link` reste fixe dans ce modele:

```text
x = 0
y = 0
z = 0.010 m
```

L'orientation yaw vaut:

```text
yaw = q1 + q2
```

## Conclusion

RGS2-29 est considere comme fait: les joints, liens, reperes, limites et parametres cinematiques du modele URDF actuel sont identifies et documentes.
