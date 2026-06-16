# Environnement aquatique Gazebo

Le monde Gazebo principal est:

```text
mon_robot_bringup/worlds/robot_world.sdf
```

Il contient:

- une surface d'eau visuelle `water_surface`;
- des lignes de vague visuelles `wave_lines`;
- un ciel et un eclairage adaptes a une scene maritime;
- aucun obstacle de test.

## Lancement standard

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch mon_robot_bringup simulation.launch.py
```

## Ajuster la pose du bateau

Le launch expose maintenant la pose initiale du bateau.

```bash
ros2 launch mon_robot_bringup simulation.launch.py \
  boat_x:=0.0 \
  boat_y:=0.0 \
  boat_z:=0.12 \
  boat_roll:=0.0 \
  boat_pitch:=1.5708 \
  boat_yaw:=0.0
```

Si le bateau n'est pas horizontal, ajuster d'abord `boat_pitch`.

Exemples:

```bash
ros2 launch mon_robot_bringup simulation.launch.py boat_pitch:=0.0
ros2 launch mon_robot_bringup simulation.launch.py boat_pitch:=1.5708
ros2 launch mon_robot_bringup simulation.launch.py boat_pitch:=-1.5708
```

Si le bateau est horizontal mais trop haut ou trop bas par rapport a l'eau:

```bash
ros2 launch mon_robot_bringup simulation.launch.py boat_z:=0.08
ros2 launch mon_robot_bringup simulation.launch.py boat_z:=0.16
```

## Flottabilite

La version stable actuelle n'active pas de plugin de flottabilite. Le bateau repose sur le plan de collision de la surface d'eau. Cette approche est moins physique, mais elle evite les erreurs de chargement Gazebo liees aux plugins systeme non disponibles selon l'installation.

## Limites actuelles

Cette scene n'est pas encore une simulation navale complete:

- pas de courant marin;
- pas de vagues physiques;
- pas de trainee hydrodynamique calibree;
- pas de modele de propulsion maritime;
- la stabilite depend fortement des collisions et inerties URDF.

Pour une demo visuelle de bateau en mer, l'environnement est suffisant. Pour une simulation physique avancee, il faudra ajouter un modele hydrodynamique dedie, verifier les plugins disponibles dans Gazebo Harmonic et ajuster les volumes de collision.
