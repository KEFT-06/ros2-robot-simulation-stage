# Demo ATAWI-3A3 — ROS 2 Jazzy + Gazebo Harmonic

## 1. Preparation (une fois)

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_ws/src
# copier les 3 paquets depuis ce depot
cd ~/ros2_ws
python3 src/ros2-robot-simulation-stage/generate_placeholder_meshes.py
colcon build --symlink-install
source install/setup.bash
colcon test --packages-select mon_robot_control
colcon test-result --verbose
```

## 2. Demo RViz (2 DOF manuel)

```bash
ros2 launch mon_robot_bringup display.launch.py
```

Verifier : glissieres `joint1_head` / `joint2_rotor`, TF `base_link` -> `tool_link`.

## 3. Demo Gazebo + controleurs + trajectoire

**Terminal 1** — demo automatisee :

```bash
ros2 launch mon_robot_bringup demo.launch.py
```

Lance : monde aquatique, spawn URDF, `joint_state_broadcaster`, `joint_trajectory_controller`, trajectoire `sweep` apres 10 s.

Options :

```bash
ros2 launch mon_robot_bringup demo.launch.py trajectory_type:=spin
ros2 launch mon_robot_bringup demo.launch.py record_bag:=true
```

**Terminal 2** — trajectoire manuelle :

```bash
ros2 run mon_robot_control send_trajectory.py home
ros2 run mon_robot_control send_trajectory.py complex
```

Mode topic (sans action) :

```bash
ros2 run mon_robot_control send_trajectory.py home --ros-args -p use_action:=false
```

## 4. Verification rapide

```bash
ros2 control list_controllers
ros2 topic echo /joint_states --once
ros2 action list | grep follow_joint_trajectory
ros2 run mon_robot_control validate_fk.py
```

Attendu :

| Element | Attendu |
|---|---|
| `joint_state_broadcaster` | active |
| `joint_trajectory_controller` | active |
| `/joint_states` | 2 joints |
| Action | `/joint_trajectory_controller/follow_joint_trajectory` |

## 5. Rosbag (option demo)

```bash
ros2 launch mon_robot_bringup demo.launch.py record_bag:=true run_trajectory:=true
# Ctrl+C puis :
ros2 bag info atawi_demo_bag
```

## 6. Docker

```bash
docker build -t atawi-3a3:jazzy .
docker run --rm -it atawi-3a3:jazzy \
  python3 /ros2_ws/src/ros2-robot-simulation-stage/generate_placeholder_meshes.py
docker run --rm -it --net=host -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw atawi-3a3:jazzy \
  ros2 launch mon_robot_bringup demo.launch.py
```

## 7. Cinematique offline

```bash
python3 ~/ros2_ws/src/mon_robot_control/scripts/fk_validation.py
python3 ~/ros2_ws/src/mon_robot_control/scripts/ik_validation.py
python3 ~/ros2_ws/src/mon_robot_control/scripts/workspace_visualization.py
```
