# Commandes de lancement — ATAWI-3A3

Toutes les commandes à exécuter dans un **terminal Ubuntu** (WSL), depuis `~/ros2_ws`.

---

## 0. À faire dans CHAQUE nouveau terminal (sourcing)
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
cd ~/ros2_ws
```

## 1. Compiler le workspace (après chaque modif de code)
```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

## 2. RViz seul — modèle + curseurs articulaires
```bash
ros2 launch mon_robot_bringup display.launch.py
```
Ouvre RViz + la fenêtre `joint_state_publisher_gui` pour bouger `joint1_head` / `joint2_rotor` à la main.

## 3. Gazebo — bateau horizontal sur l'eau
```bash
ros2 launch mon_robot_bringup simulation.launch.py
```
Options utiles :
```bash
ros2 launch mon_robot_bringup simulation.launch.py boat_yaw:=0.0
# sans les contrôleurs :
ros2 launch mon_robot_bringup simulation.launch.py load_controllers:=false
```
La hauteur fine du STL sur l'eau est reglee dans l'URDF par le joint `world_to_hull` (`z=0.13`). Le repere `hull_link` reste technique et invisible : il ne doit plus afficher de carre noir.

> ⚠️ Ne lance pas RViz (§2) et Gazebo (§3) en même temps dans le même réseau ROS : ils publient tous deux `/robot_description` et se gênent. Un seul à la fois (ou des `ROS_DOMAIN_ID` différents).

## 4. Trajectoires — la « course temporelle »
**Dans un 2ᵉ terminal** (Gazebo tournant, bien sourcer) :
```bash
ros2 run mon_robot_control send_trajectory.py home      # retour à zéro
ros2 run mon_robot_control send_trajectory.py sweep     # balayage tête ±90°
ros2 run mon_robot_control send_trajectory.py spin      # rotation de l'hélice
ros2 run mon_robot_control send_trajectory.py complex   # mouvement multi-joints
ros2 run mon_robot_control send_trajectory.py sine      # ondulation sinusoïdale
```
Mode topic (au lieu de l'action) :
```bash
ros2 run mon_robot_control send_trajectory.py sweep --ros-args -p use_action:=false
```

## 5. Démo complète — Gazebo + trajectoire + rosbag
```bash
ros2 launch mon_robot_bringup demo.launch.py record_bag:=true
# options :
ros2 launch mon_robot_bringup demo.launch.py run_trajectory:=true trajectory_type:=complex record_bag:=true bag_name:=atawi_demo_complex
ros2 launch mon_robot_bringup demo.launch.py verify_controller:=true trajectory_type:=sweep
```
Après `Ctrl+C`, inspecter / rejouer l'enregistrement :
```bash
ros2 bag info atawi_demo_bag
ros2 bag play atawi_demo_bag
```
Si un dossier rosbag du même nom existe déjà, choisis un autre `bag_name` ou supprime l'ancien dossier avant l'enregistrement.

Vérifier explicitement que `joint_trajectory_controller` suit une consigne :
```bash
ros2 run mon_robot_control verify_controller_tracking.py
```

## 6. Validation cinématique hors-ligne (sans Gazebo)
```bash
ros2 run mon_robot_control validate_kinematics.py      # affiche FK/IK
ros2 run mon_robot_control fk_validation.py            # -> results/fk_results.txt
ros2 run mon_robot_control ik_validation.py            # -> results/ik_results.txt
ros2 run mon_robot_control workspace_visualization.py  # -> results/workspace_3d.png
```
Validation FK **en direct** (pendant que Gazebo/RViz tourne, lit les TF) :
```bash
ros2 run mon_robot_control validate_fk.py
```

## 7. Tests
```bash
cd ~/ros2_ws
colcon test --packages-select mon_robot_control
colcon test-result --verbose
```

## 8. Inspection / débogage (Gazebo tournant)
```bash
ros2 control list_controllers                                          # état des contrôleurs
ros2 action list | grep follow_joint_trajectory                        # action du contrôleur
ros2 topic list                                                        # liste des topics
ros2 topic echo /joint_states --field position                         # positions articulaires
ros2 topic echo /model/atawi_3a3/odometry --field pose.pose.position   # position de la coque
ros2 node list
```

## 9. Tout arrêter
```bash
# Ctrl+C dans chaque terminal, ou :
pkill -f "gz sim"; pkill -f rviz2; pkill -f robot_state_publisher
```

---

## Scénario typique « je montre tout » (3 terminaux)
| Terminal | Commande |
|---|---|
| **1** | sourcing → `ros2 launch mon_robot_bringup simulation.launch.py` (Gazebo, bateau horizontal sur l'eau) |
| **2** | sourcing → `ros2 run mon_robot_control send_trajectory.py complex` (la tête/hélice bouge) |
| **3** | sourcing → `ros2 run mon_robot_control verify_controller_tracking.py` (vérifie le suivi du contrôleur) |
