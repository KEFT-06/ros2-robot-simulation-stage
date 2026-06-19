# ROS 2 Robot Simulation Stage - ATAWI-3A3

Projet ROS 2 pour la description, la visualisation, la simulation et la validation cinematique du robot ATAWI-3A3.

Le depot contient un modele URDF/Xacro avec meshes STL, une configuration `ros2_control`, des launch files RViz/Gazebo et des scripts Python pour envoyer des trajectoires et valider la cinematique.

## Environnement cible

- Ubuntu 24.04, natif ou WSL2
- ROS 2 Jazzy
- Gazebo Harmonic / Gazebo Sim
- Python 3
- Colcon

## Structure du projet

```text
ros2-robot-simulation-stage/
├── mon_robot_description/
│   ├── urdf/                 # Modele URDF/Xacro du robot
│   ├── meshes/               # Meshes STL du robot ATAWI-3A3
│   └── rviz/                 # Configuration RViz
├── mon_robot_bringup/
│   ├── launch/               # Launch files RViz et simulation
│   ├── config/               # Configuration ros2_control
│   └── worlds/               # Monde SDF Gazebo
├── mon_robot_control/
│   └── scripts/              # Trajectoires, FK, IK, workspace
├── Solidworks/               # Fichiers CAO source
├── convert_meshes.py         # Conversion STEP/STL
└── setup.sh.legacy           # Ancien installateur Humble (obsolete)
```

## Packages ROS 2

| Package | Role |
|---|---|
| `mon_robot_description` | Description du robot: URDF/Xacro, STL, RViz |
| `mon_robot_bringup` | Launch files, monde SDF, configuration controleurs |
| `mon_robot_control` | Trajectoires (action/topic), module `robot_kinematics`, tests pytest |

## Modele cinematique actuel

Le modele URDF actuel expose deux articulations commandees:

| Joint | Type | Axe | Description |
|---|---|---|---|
| `joint1_head` | revolute | Z | Rotation de la tete |
| `joint2_rotor` | revolute | Z | Rotation du rotor |

Tous les autres joints du modele sont fixes. Le modele commandable actuel est donc un modele **2 DOF**.

## Installation des dependances

```bash
sudo apt update
sudo apt install -y \
  doxygen \
  ros-jazzy-desktop \
  ros-jazzy-ros2-control \
  ros-jazzy-ros2-controllers \
  ros-jazzy-joint-state-publisher-gui \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-rviz2 \
  ros-jazzy-ros-gz-sim \
  ros-jazzy-ros-gz-bridge \
  ros-jazzy-gz-ros2-control \
  python3-colcon-common-extensions \
  python3-matplotlib \
  python3-pytest
```

## Installation dans un workspace ROS 2

Depuis Ubuntu ou WSL:

```bash
source /opt/ros/jazzy/setup.bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

Si le depot est dans Windows, par exemple:

```bash
cp -r /mnt/c/Users/FOKO/Documents/GitHub/ros2-robot-simulation-stage/mon_robot_description .
cp -r /mnt/c/Users/FOKO/Documents/GitHub/ros2-robot-simulation-stage/mon_robot_bringup .
cp -r /mnt/c/Users/FOKO/Documents/GitHub/ros2-robot-simulation-stage/mon_robot_control .
chmod +x mon_robot_control/scripts/*.py
sed -i 's/\r$//' mon_robot_control/scripts/*.py
```

Compiler:

```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

Verifier que les packages sont visibles:

```bash
ros2 pkg list | grep mon_robot
```

## Utilisation avec Docker

Construire l'image reproductible ROS 2 Jazzy:

```bash
docker build -t atawi-3a3:jazzy .
```

Ouvrir un shell dans le conteneur:

```bash
docker run --rm -it atawi-3a3:jazzy
```

Lancer RViz depuis le conteneur sur Linux avec X11:

```bash
xhost +local:docker
docker run --rm -it --net=host \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  atawi-3a3:jazzy \
  ros2 launch mon_robot_bringup display.launch.py
```

Lancer Gazebo:

```bash
docker run --rm -it --net=host \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  atawi-3a3:jazzy \
  ros2 launch mon_robot_bringup simulation.launch.py
```

## Lancer RViz

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch mon_robot_bringup display.launch.py
```

Ce lancement demarre:

- `robot_state_publisher`
- `joint_state_publisher_gui`
- `rviz2`

## Lancer la simulation Gazebo

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch mon_robot_bringup simulation.launch.py
```

Ce lancement charge le monde SDF aquatique, spawn le robot via `-string` (URDF xacro) et demarre `gz_ros2_control` avec les spawners `joint_state_broadcaster` + `joint_trajectory_controller` (`load_controllers:=true` par defaut).

Desactiver les controleurs:

```bash
ros2 launch mon_robot_bringup simulation.launch.py load_controllers:=false
```

Le monde Gazebo contient:

- une surface d'eau visuelle;
- un ciel et une lumiere adaptes a une scene maritime;
- aucun obstacle de test.

Cette version est volontairement stable: l'eau est visuelle et le bateau repose sur un plan de collision. Elle ne simule pas encore la flottabilite, la trainee, les courants ou les vagues physiques.

La pose initiale du bateau est configurable:

```bash
ros2 launch mon_robot_bringup simulation.launch.py boat_z:=0.12 boat_pitch:=1.5708
```

Voir aussi:

```text
docs/marine_environment.md
```

## Envoyer une trajectoire

Dans un terminal separe:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run mon_robot_control send_trajectory.py home
```

Par defaut le script utilise l'action `/joint_trajectory_controller/follow_joint_trajectory`. Mode topic:

```bash
ros2 run mon_robot_control send_trajectory.py home --ros-args -p use_action:=false
```

Trajectoires disponibles:

```bash
ros2 run mon_robot_control send_trajectory.py home
ros2 run mon_robot_control send_trajectory.py sweep
ros2 run mon_robot_control send_trajectory.py spin
ros2 run mon_robot_control send_trajectory.py complex
ros2 run mon_robot_control send_trajectory.py sine
```

## Tests unitaires

```bash
cd ~/ros2_ws
colcon test --packages-select mon_robot_control
colcon test-result --verbose
```

Ou apres build:

```bash
pytest src/ros2-robot-simulation-stage/mon_robot_control/test/
```

## Validation cinematique

### Validation complete FK/IK

```bash
python3 ~/ros2_ws/src/mon_robot_control/scripts/validate_kinematics.py
```

### Cinematique directe

```bash
python3 ~/ros2_ws/src/mon_robot_control/scripts/fk_validation.py
```

Le script genere:

```text
fk_results.txt
```

### Cinematique inverse

```bash
python3 ~/ros2_ws/src/mon_robot_control/scripts/ik_validation.py
```

Le script genere:

```text
ik_results.txt
```

### Espace atteignable

```bash
python3 ~/ros2_ws/src/mon_robot_control/scripts/workspace_visualization.py
```

Le script genere:

```text
workspace_3d.png
```

## Controleurs

La configuration des controleurs se trouve dans:

```text
mon_robot_bringup/config/controllers.yaml
```

Controleurs principaux:

- `joint_state_broadcaster`
- `joint_trajectory_controller`

Joints commandes:

- `joint1_head`
- `joint2_rotor`

## Conversion des meshes

Le script `convert_meshes.py` permet de convertir des fichiers STEP vers STL avec FreeCAD si necessaire.

```bash
python3 convert_meshes.py
```

Les meshes utilises par l'URDF sont dans:

```text
mon_robot_description/meshes/
```

## Depannage

### `Package 'mon_robot_control' not found`

Le workspace n'est probablement pas source:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

Verifier:

```bash
ros2 pkg list | grep mon_robot
```

### `No executable found`

Verifier que les scripts sont executables puis rebuild:

```bash
chmod +x ~/ros2_ws/src/mon_robot_control/scripts/*.py
cd ~/ros2_ws
colcon build --symlink-install --packages-select mon_robot_control
source install/setup.bash
```

### `/usr/bin/env: 'python3\r': No such file or directory`

Les scripts ont des fins de ligne Windows. Corriger dans WSL:

```bash
sed -i 's/\r$//' ~/ros2_ws/src/mon_robot_control/scripts/*.py
chmod +x ~/ros2_ws/src/mon_robot_control/scripts/*.py
```

### `simulation.launch.py was not found`

Le package `mon_robot_bringup` installe une ancienne version ou n'a pas ete recopie dans le workspace.

```bash
cd ~/ros2_ws/src
rm -rf mon_robot_bringup
cp -r /mnt/c/Users/FOKO/Documents/GitHub/ros2-robot-simulation-stage/mon_robot_bringup .
cd ~/ros2_ws
colcon build --symlink-install --packages-select mon_robot_bringup
source install/setup.bash
```

### Warnings `AMENT_PREFIX_PATH doesn't exist`

Ces warnings apparaissent souvent apres `rm -rf install` dans un terminal deja source. Ils ne sont pas bloquants. Ouvrir un terminal neuf ou relancer:

```bash
source /opt/ros/jazzy/setup.bash
```

## Etat du projet

Stories realisees:

- Installation ROS 2 Jazzy / Gazebo Harmonic
- Depot Git structure
- Description URDF/Xacro
- Ajout des meshes STL
- Balises visual/collision
- Tenseurs d'inertie
- Limites articulaires
- Monde SDF Gazebo
- Bloc `ros2_control`
- Configuration `controllers.yaml`
- Launch files
- Integration Gazebo Harmonic + ros2_control + trajectoires
- Tests pytest cinématique (`mon_robot_control/test/`)

Travaux restants possibles:

- Ajouter des capteurs simules
- Enregistrer une session `rosbag2`
- Rediger le rapport technique
- Preparer slides et demo video

## Licence

MIT

