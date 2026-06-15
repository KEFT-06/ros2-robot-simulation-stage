# RGS2-28 - Documentation du code

Ce document complete le README et sert de point d'entree pour la documentation technique du code.

## Fichiers principaux

| Fichier | Role |
|---|---|
| `README.md` | Documentation principale du projet |
| `mon_robot_description/urdf/mon_robot.urdf.xacro` | Modele robot URDF/Xacro |
| `mon_robot_bringup/config/controllers.yaml` | Configuration des controleurs |
| `mon_robot_bringup/launch/display.launch.py` | Lancement RViz |
| `mon_robot_bringup/launch/simulation.launch.py` | Lancement Gazebo |
| `mon_robot_control/scripts/send_trajectory.py` | Publication de trajectoires |
| `mon_robot_control/scripts/fk_validation.py` | Validation FK |
| `mon_robot_control/scripts/ik_validation.py` | Validation IK |
| `mon_robot_control/scripts/workspace_visualization.py` | Visualisation de l'espace atteignable |

## Generation Doxygen

Un fichier `Doxyfile` est fourni a la racine du projet.

Commande:

```bash
doxygen Doxyfile
```

Sortie attendue:

```text
docs/doxygen/html/index.html
```

## Notes de maintenance

- Le modele commandable actuel est 2 DOF: `joint1_head` et `joint2_rotor`.
- Les scripts Python doivent rester en fins de ligne Unix dans WSL.
- Les fichiers STL representent l'assemblage mecanique, mais la cinematique vient uniquement de l'URDF.

## Statut

RGS2-28 est considere comme **fait pour README + base Doxygen**. La documentation peut etre enrichie ensuite avec des commentaires plus detailles si le modele evolue.
