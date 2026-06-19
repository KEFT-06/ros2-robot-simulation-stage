# ROS 2 Robot Simulation Stage — ATAWI-3A3

Projet ROS 2 pour la description, la visualisation, la simulation et la validation cinématique du robot ATAWI-3A3.

## Démarrage rapide

```bash
source /opt/ros/jazzy/setup.bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
# copier mon_robot_description, mon_robot_bringup, mon_robot_control
python3 mon_robot_description/scripts/generate_placeholder_meshes.py
cd ~/ros2_ws && colcon build --symlink-install && source install/setup.bash
ros2 launch mon_robot_bringup demo.launch.py
```

## Documentation

Toute la documentation du projet se trouve dans un seul fichier :

**[docs/projet.md](docs/projet.md)**

Installation, cinématique, Gazebo, trajectoires, validation FK/IK, Docker, CI, dépannage.

## Packages

| Package | Rôle |
|---|---|
| `mon_robot_description` | URDF/Xacro, meshes STL, RViz |
| `mon_robot_bringup` | Launch files, monde SDF, contrôleurs |
| `mon_robot_control` | Trajectoires, `robot_kinematics`, tests pytest |

## Licence

MIT
