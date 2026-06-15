# RGS2-23 - Execution d'une trajectoire interpolee

Ce document decrit la validation de l'envoi de trajectoires au `joint_trajectory_controller`.

## Script utilise

```text
mon_robot_control/scripts/send_trajectory.py
```

Le script publie un message ROS 2:

```text
trajectory_msgs/msg/JointTrajectory
```

sur le topic:

```text
/joint_trajectory_controller/joint_trajectory
```

## Joints commandes

```text
joint1_head
joint2_rotor
```

Ces joints correspondent a ceux declares dans:

```text
mon_robot_description/urdf/mon_robot.urdf.xacro
mon_robot_bringup/config/controllers.yaml
```

## Trajectoires disponibles

| Nom | Commande | Description |
|---|---|---|
| `home` | `ros2 run mon_robot_control send_trajectory.py home` | Retour a `[0, 0]` |
| `sweep` | `ros2 run mon_robot_control send_trajectory.py sweep` | Balayage de la tete |
| `spin` | `ros2 run mon_robot_control send_trajectory.py spin` | Rotation du rotor |
| `complex` | `ros2 run mon_robot_control send_trajectory.py complex` | Mouvement multi-joints |
| `sine` | `ros2 run mon_robot_control send_trajectory.py sine` | Trajectoire sinusoidale |

## Procedure de validation

Terminal 1:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch mon_robot_bringup simulation.launch.py
```

Terminal 2:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run mon_robot_control send_trajectory.py home
ros2 run mon_robot_control send_trajectory.py sweep
ros2 run mon_robot_control send_trajectory.py spin
```

## Critere d'acceptation

La story est validee si:

- le script est installe par `colcon build`;
- `ros2 run mon_robot_control send_trajectory.py home` publie une trajectoire sans erreur;
- les noms de joints publies sont identiques aux joints du controleur;
- le controleur `joint_trajectory_controller` recoit la commande lorsque la simulation est lancee.

## Statut

RGS2-23 est considere comme **fait cote logiciel**: le publisher de trajectoire existe, il est installe comme executable ROS 2, et il publie les points de trajectoire pour les deux joints du modele actuel.
