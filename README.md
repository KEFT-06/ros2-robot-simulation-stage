# ros2-robot-simulation-stage

Simulation cinématique d'un robot 2-DOF (2 articulations) avec **ROS 2 Jazzy** et **Gazebo Harmonic**.

## 📋 Contenu du Projet

```
.
├── mon_robot_description/          # Description du robot
│   ├── urdf/
│   │   └── mon_robot.urdf.xacro    # Modèle URDF/Xacro du robot
│   ├── meshes/                      # Fichiers de géométrie (STL, DAE)
│   └── rviz/                        # Configs RViz
├── mon_robot_bringup/              # Lancement et config
│   ├── launch/
│   │   ├── display.launch.py        # Lancer RViz + visualisation
│   │   └── simulation.launch.py     # Lancer Gazebo + simulation
│   ├── config/
│   │   └── controllers.yaml         # Config contrôleurs PID
│   └── worlds/
│       └── robot_world.sdf          # Monde Gazebo
├── mon_robot_control/              # Scripts de contrôle
│   ├── scripts/
│   │   ├── send_trajectory.py       # Envoyer trajectoires
│   │   └── validate_fk.py           # Valider kinématique directe
│   └── mon_robot_control/           # Package Python
├── docs/                            # Documentation
└── README.md
```

## 🤖 Architecture du Robot

- **Base**: Bloc rigide (0.3 × 0.3 × 0.2 m)
- **Joint 1**: Rotation autour de Z (base)
  - Limite: [-90°, +90°]
  - Contrôleur: PID effort
- **Joint 2**: Articulation Y (bras)
  - Limite: [-90°, +90°]
  - Contrôleur: PID effort
- **Link 2**: Avant-bras + end-effector

## 🚀 Démarrage Rapide

### 1. Visualisation seule (RViz)
```bash
ros2 launch mon_robot_bringup display.launch.py
```

### 2. Simulation complète (Gazebo + ROS 2)
```bash
ros2 launch mon_robot_bringup simulation.launch.py
```

### 3. Envoyer une trajectoire
```bash
ros2 run mon_robot_control send_trajectory
```

### 4. Valider la cinématique directe
```bash
ros2 run mon_robot_control validate_fk
```

## 📦 Dépendances

```bash
# Système
sudo apt install ros-jazzy-ros2-control ros-jazzy-ros-gz-bridge
sudo apt install ros-jazzy-joint-trajectory-controller
sudo apt install ros-jazzy-robot-state-publisher

# Python
pip install xacro
```

## 🎯 Objectifs du Projet

- ✅ Modèle URDF complet avec ros2_control
- ✅ Contrôleurs PID (Joint Trajectory Controller)
- ✅ Simulation Gazebo avec gz_ros2_control
- ✅ Cinématique directe (FK) validée
- ✅ Scripts d'envoi de trajectoires
- ✅ Visualisation RViz

## 🔧 Notes de Configuration

- **use_sim_time**: Automatique en simulation
- **Controllers**: Joint State Broadcaster + Joint Trajectory Controller
- **PID Gains**: À ajuster selon la simulation (start: p=100, i=0, d=10)

## 📄 Fichiers Créés

| Fichier | Description |
|---------|-------------|
| `mon_robot.urdf.xacro` | Modèle robot 2-DOF |
| `controllers.yaml` | Config ros2_control + PID |
| `robot_world.sdf` | Monde Gazebo |
| `display.launch.py` | RViz launcher |
| `simulation.launch.py` | Gazebo launcher |
| `send_trajectory.py` | Script d'envoi de trajectoires |
| `validate_fk.py` | Script de validation FK |
