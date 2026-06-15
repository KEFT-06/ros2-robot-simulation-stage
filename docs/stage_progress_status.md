# Etat d'avancement des stories RGS2

## A passer en Fait

| ID | Story | Justification |
|---|---|---|
| RGS2-21 | Calculer et valider la cinematique directe FK | Script `fk_validation.py` + resultats `fk_results.txt` |
| RGS2-22 | Calculer et valider la cinematique inverse IK | Script `ik_validation.py` + resultats `ik_results.txt` |
| RGS2-23 | Executer une trajectoire interpolee | Script ROS 2 `send_trajectory.py` installe et publie sur le controleur |
| RGS2-24 | Visualiser l'espace de travail atteignable | Script `workspace_visualization.py` + image `workspace_3d.png` |
| RGS2-28 | Documenter le code README + Doxygen | `README.md`, `docs/code_documentation.md`, `Doxyfile` |
| RGS2-29 | Lister les parametres DH / liens / joints / reperes | `docs/kinematic_parameters.md` |

## Remarque importante

Les validations sont faites pour le modele URDF actuel, qui expose deux joints commandables:

```text
joint1_head
joint2_rotor
```

Si le modele mecanique evolue vers un robot 3 DOF, les scripts FK/IK et les documents de validation devront etre mis a jour.
