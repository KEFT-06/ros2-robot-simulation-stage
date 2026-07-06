# Documentation du projet ATAWI-3A3

Projet ROS 2 pour la description, la visualisation, la simulation et la validation cinématique du robot ATAWI-3A3.

---

## Table des matières

1. [Vue d'ensemble](#1-vue-densemble)
2. [Structure du dépôt](#2-structure-du-dépôt)
3. [Environnement et dépendances](#3-environnement-et-dépendances)
4. [Installation](#4-installation)
5. [Packages ROS 2](#5-packages-ros-2)
6. [Modèle cinématique](#6-modèle-cinématique)
7. [Meshes et CAO](#7-meshes-et-cao)
8. [Lancement RViz](#8-lancement-rviz)
9. [Simulation Gazebo](#9-simulation-gazebo)
10. [Environnement aquatique](#10-environnement-aquatique)
11. [Contrôleurs et trajectoires](#11-contrôleurs-et-trajectoires)
12. [Démo complète](#12-démo-complète)
13. [Validation cinématique](#13-validation-cinématique)
14. [Tests unitaires](#14-tests-unitaires)
15. [Docker](#15-docker)
16. [CI GitHub Actions](#16-ci-github-actions)
17. [Documentation Doxygen](#17-documentation-doxygen)
18. [État d'avancement (stories RGS2)](#18-état-davancement-stories-rgs2)
19. [Dépannage](#19-dépannage)
20. [Licence](#20-licence)

---

## 1. Vue d'ensemble

Le dépôt contient :

- un modèle URDF/Xacro avec meshes STL ;
- une configuration `ros2_control` ;
- des launch files RViz et Gazebo Harmonic ;
- des scripts Python pour envoyer des trajectoires et valider la cinématique (FK, IK, espace atteignable).

**Environnement cible :**

| Composant | Version |
|---|---|
| OS | Ubuntu 24.04 (natif ou WSL2) |
| ROS 2 | Jazzy |
| Simulateur | Gazebo Harmonic / Gazebo Sim |
| Build | Colcon |
| Python | 3 |

---

## 2. Structure du dépôt

```text
ros2-robot-simulation-stage/
├── README.md
├── docs/
│   ├── projet.md              # Cette documentation
│   └── Doxyfile               # Configuration Doxygen
├── docker/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── setup.sh.legacy        # Ancien installateur Humble (obsolète)
├── mon_robot_description/
│   ├── urdf/                  # Modèle URDF/Xacro
│   ├── meshes/                # Meshes STL
│   ├── rviz/                  # Configuration RViz
│   └── scripts/               # Génération / conversion meshes
├── mon_robot_bringup/
│   ├── launch/                # Launch files RViz, Gazebo, démo
│   ├── config/                # Configuration ros2_control
│   └── worlds/                # Monde SDF Gazebo
├── mon_robot_control/
│   ├── mon_robot_control/     # Module robot_kinematics
│   ├── scripts/               # Trajectoires, FK, IK, workspace
│   ├── test/                  # Tests pytest
│   └── results/               # Résultats FK/IK
└── .github/workflows/ci.yml
```

Le dossier `src/` n'est **pas requis dans ce dépôt** : les 3 paquets sont à la racine et se copient dans `~/ros2_ws/src/` (layout colcon standard côté workspace, pas côté Git).

---

## 3. Environnement et dépendances

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
  ros-jazzy-control-msgs \
  ros-jazzy-controller-manager \
  ros-jazzy-rosbag2 \
  python3-colcon-common-extensions \
  python3-numpy \
  python3-matplotlib \
  python3-pytest
```

---

## 4. Installation

Depuis Ubuntu ou WSL :

```bash
source /opt/ros/jazzy/setup.bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

Copier les 3 paquets (exemple depuis Windows) :

```bash
cp -r /mnt/c/Users/FOKO/Documents/GitHub/ros2-robot-simulation-stage/mon_robot_description .
cp -r /mnt/c/Users/FOKO/Documents/GitHub/ros2-robot-simulation-stage/mon_robot_bringup .
cp -r /mnt/c/Users/FOKO/Documents/GitHub/ros2-robot-simulation-stage/mon_robot_control .
chmod +x mon_robot_control/scripts/*.py
sed -i 's/\r$//' mon_robot_control/scripts/*.py
```

Générer les meshes placeholder puis compiler :

```bash
python3 mon_robot_description/scripts/generate_placeholder_meshes.py
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

Vérifier :

```bash
ros2 pkg list | grep mon_robot
```

---

## 5. Packages ROS 2

| Package | Rôle |
|---|---|
| `mon_robot_description` | Description du robot : URDF/Xacro, STL, RViz |
| `mon_robot_bringup` | Launch files, monde SDF, configuration contrôleurs |
| `mon_robot_control` | Trajectoires (action/topic), module `robot_kinematics`, tests pytest |

### Fichiers principaux

| Fichier | Rôle |
|---|---|
| `mon_robot_description/urdf/mon_robot.urdf.xacro` | Modèle robot URDF/Xacro |
| `mon_robot_bringup/config/controllers.yaml` | Configuration des contrôleurs |
| `mon_robot_bringup/launch/display.launch.py` | Lancement RViz |
| `mon_robot_bringup/launch/simulation.launch.py` | Lancement Gazebo |
| `mon_robot_bringup/launch/demo.launch.py` | Démo Gazebo + trajectoire + rosbag optionnel |
| `mon_robot_bringup/worlds/robot_world.sdf` | Monde aquatique Gazebo |
| `mon_robot_control/scripts/send_trajectory.py` | Trajectoires (action/topic) |
| `mon_robot_control/mon_robot_control/robot_kinematics.py` | Module FK/IK partagé |
| `mon_robot_control/scripts/fk_validation.py` | Validation FK |
| `mon_robot_control/scripts/ik_validation.py` | Validation IK |
| `mon_robot_control/scripts/workspace_visualization.py` | Visualisation de l'espace atteignable |
| `mon_robot_control/test/` | Tests pytest |

---

## 6. Modèle cinématique

Fichier de référence : `mon_robot_description/urdf/mon_robot.urdf.xacro`

Le modèle commandable actuel est un robot **2 DOF**. Les fichiers STL représentent l'assemblage mécanique complet, mais la cinématique est définie uniquement par les joints URDF.

### Joints commandables

| Joint | Type | Parent | Enfant | Origine xyz | Axe | Limites |
|---|---|---|---|---|---|---|
| `joint1_head` | revolute | `base_link` | `head_link` | `0 0 0` | `0 0 1` | `[-π, π]` |
| `joint2_rotor` | revolute | `head_link` | `rotor_link` | `0 0 0` | `0 0 1` | `[-π, π]` |

Les deux axes de rotation sont coaxiaux autour de Z.

### Liens principaux

| Link | Rôle |
|---|---|
| `world` | Repère fixe global |
| `hull_link` | Repère technique invisible, fixé au monde pour stabiliser le bateau |
| `base_link` | Corps principal du robot, STL recentré et posé horizontalement sur l'eau |
| `head_link` | Tête orientable |
| `rotor_link` | Rotor / support des pales |
| `tool_link` | Repère effecteur final |

### Joints fixes

Les pièces suivantes sont montées par joints fixes :

- `world_to_base` (**RViz uniquement**, via `xacro:unless use_gazebo`), `handle1_joint`, `handle2_joint`
- `hexnut1_joint`, `hexnut2_joint`, `vis1_joint`, `vis2_joint`
- `l2_1_joint`, `l2_2_joint`, `l2_3_joint`, `l2_4_joint`
- `blade2_joint`, `blade3_joint`, `blade4_joint`, `tool_joint`

### Paramètres DH simplifiés

| i | Joint | θ | d | a | α |
|---|---|---|---|---|---|
| 1 | `joint1_head` | q1 | 0 | 0 | 0 |
| 2 | `joint2_rotor` | q2 | 0 | 0 | 0 |
| Tool | `tool_joint` | 0 | 0.010 m | 0 | 0 |

Pose de `tool_link` :

```text
T_world_tool = Rz(q1) × Rz(q2) × Tz(0.010)
```

Position de `tool_link` (fixe dans ce modèle) :

```text
x = 0,  y = 0,  z = 0.010 m
```

Orientation yaw :

```text
yaw = q1 + q2
```

Le module Python `RobotKinematics` (`mon_robot_control/mon_robot_control/robot_kinematics.py`) implémente FK/IK cohérente avec ce modèle.

---

## 7. Meshes et CAO

Les meshes utilisés par l'URDF sont dans `mon_robot_description/meshes/`.

### Meshes placeholder (démo sans CAO)

```bash
python3 mon_robot_description/scripts/generate_placeholder_meshes.py
```

Génère des boîtes STL pour : `Body.stl`, `Handle_1.stl`, `Handle_2.stl`, `Hexnut_1.stl`, `Hexnut_2.stl`, `Vis_1.stl`, `Vis_2.stl`, `L2_1.stl`–`L2_4.stl`, `part2.stl`, `Blade_1.stl`–`Blade_4.stl`.

### Conversion STEP → STL (FreeCAD)

```bash
python3 mon_robot_description/scripts/convert_meshes.py
```

Place les fichiers STEP dans `Solidworks/` à la racine du dépôt. Nécessite FreeCAD :

```bash
sudo apt-get install freecad python3-freecad
```

---

## 8. Lancement RViz

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch mon_robot_bringup display.launch.py
```

Démarre :

- `robot_state_publisher`
- `joint_state_publisher_gui`
- `rviz2`

Vérifier : glissières `joint1_head` / `joint2_rotor`, TF `base_link` → `tool_link`.

---

## 9. Simulation Gazebo

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch mon_robot_bringup simulation.launch.py
```

Ce lancement :

- charge le monde SDF aquatique ;
- spawn le robot via le topic `robot_description` ;
- démarre `gz_ros2_control` avec les spawners `joint_state_broadcaster` + `joint_trajectory_controller` (`load_controllers:=true` par défaut).

Désactiver les contrôleurs :

```bash
ros2 launch mon_robot_bringup simulation.launch.py load_controllers:=false
```

---

## 10. Environnement aquatique

Monde principal : `mon_robot_bringup/worlds/robot_world.sdf`

Contenu :

- plugins système Gazebo Harmonic : `Physics`, `SceneBroadcaster`, `UserCommands` ;
- surface d'eau **purement visuelle** `water_surface` (aucune collision), teinte mer turquoise ;
- petites crêtes de vague visuelles `wave_lines` autour du bateau ;
- ciel et éclairage adaptés à une scène maritime.

**Bateau fixe, à plat sur l'eau.** Le repère racine de simulation est `hull_link`, mais il est maintenant **invisible** : il conserve les frames ROS/Gazebo sans afficher de bloc noir. Il est fixé au monde par `world_to_hull`, donc le bateau reste stable et horizontal. Le robot ATAWI-3A3 est couché à l'horizontale via `hull_to_base` (`rpy="1.5708 0 1.5708"`).

La taille du robot est pilotée par une **propriété xacro unique** `s` (facteur d'échelle, `1.0` par défaut) dans `mon_robot.urdf.xacro`. Le plugin `Buoyancy` a été retiré : la scène actuelle privilégie un rendu stable pour la démo plutôt qu'une dynamique navale.

### Ajuster la pose du bateau

- **Hauteur sur l'eau** : `origin z` du joint `world_to_hull` (par défaut `0.13`).
- **Position/orientation du robot** : `origin xyz/rpy` du joint `hull_to_base`.
- **Taille** : propriété `s` (`1.0`).

### Course temporelle

`demo.launch.py` enchaîne : simulation → chargement des contrôleurs (sur fin du spawn) → trajectoire chronométrée → enregistrement rosbag optionnel de `/joint_states`, `/tf`, `/tf_static`, `/clock` et `/model/atawi_3a3/odometry`.

```bash
ros2 launch mon_robot_bringup demo.launch.py record_bag:=true run_trajectory:=true bag_name:=atawi_demo_bag
# Ctrl+C, puis :
ros2 bag info atawi_demo_bag
```

### Limites actuelles

- vagues seulement visuelles, pas physiques ;
- pas de modèle hydrodynamique de Fossen ni de poussée d'Archimède calibrée ;
- bateau volontairement fixe pour obtenir une démo reproductible.

Pour une simulation navale avancée, ajouter le plugin `Hydrodynamics` de Gazebo Harmonic avec des coefficients calibrés.

---

## 11. Contrôleurs et trajectoires

Configuration : `mon_robot_bringup/config/controllers.yaml`

Contrôleurs principaux :

- `joint_state_broadcaster`
- `joint_trajectory_controller`

Joints commandés : `joint1_head`, `joint2_rotor`

### Script de trajectoire

`mon_robot_control/scripts/send_trajectory.py` publie des trajectoires via :

- **action** : `/joint_trajectory_controller/follow_joint_trajectory` (par défaut)
- **topic** : `/joint_trajectory_controller/joint_trajectory`

### Trajectoires disponibles

| Nom | Commande | Description |
|---|---|---|
| `home` | `ros2 run mon_robot_control send_trajectory.py home` | Retour à `[0, 0]` |
| `sweep` | `ros2 run mon_robot_control send_trajectory.py sweep` | Balayage de la tête |
| `spin` | `ros2 run mon_robot_control send_trajectory.py spin` | Rotation du rotor |
| `complex` | `ros2 run mon_robot_control send_trajectory.py complex` | Mouvement multi-joints |
| `sine` | `ros2 run mon_robot_control send_trajectory.py sine` | Trajectoire sinusoïdale |

Mode topic (sans action) :

```bash
ros2 run mon_robot_control send_trajectory.py home --ros-args -p use_action:=false
```

### Vérification du suivi contrôleur

`verify_controller_tracking.py` envoie une consigne courte au contrôleur, attend le résultat de l'action, puis compare `/joint_states` avec la cible finale.

```bash
ros2 run mon_robot_control verify_controller_tracking.py
```

Critère par défaut : erreur maximale `<= 0.08 rad` sur `joint1_head` et `joint2_rotor`.

### Envoi manuel (terminal séparé)

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run mon_robot_control send_trajectory.py home
```

---

## 12. Démo complète

### Préparation (une fois)

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_ws/src
# copier les 3 paquets depuis ce dépôt
cd ~/ros2_ws
python3 src/ros2-robot-simulation-stage/mon_robot_description/scripts/generate_placeholder_meshes.py
colcon build --symlink-install
source install/setup.bash
colcon test --packages-select mon_robot_control
colcon test-result --verbose
```

### Démo RViz (2 DOF manuel)

```bash
ros2 launch mon_robot_bringup display.launch.py
```

### Démo Gazebo automatisée

**Terminal 1 :**

```bash
ros2 launch mon_robot_bringup demo.launch.py
```

Lance : monde aquatique, spawn URDF, contrôleurs, trajectoire `sweep` après 10 s.

Options :

```bash
ros2 launch mon_robot_bringup demo.launch.py trajectory_type:=spin
ros2 launch mon_robot_bringup demo.launch.py record_bag:=true
ros2 launch mon_robot_bringup demo.launch.py trajectory_type:=complex record_bag:=true bag_name:=atawi_demo_complex verify_controller:=true
```

**Terminal 2 — trajectoire manuelle :**

```bash
ros2 run mon_robot_control send_trajectory.py home
ros2 run mon_robot_control send_trajectory.py complex
```

### Vérification rapide

```bash
ros2 control list_controllers
ros2 topic echo /joint_states --once
ros2 action list | grep follow_joint_trajectory
ros2 run mon_robot_control verify_controller_tracking.py
ros2 run mon_robot_control validate_fk.py
```

| Élément | Attendu |
|---|---|
| `joint_state_broadcaster` | active |
| `joint_trajectory_controller` | active |
| `/joint_states` | 2 joints |
| Action | `/joint_trajectory_controller/follow_joint_trajectory` |

### Rosbag (option démo)

```bash
ros2 launch mon_robot_bringup demo.launch.py record_bag:=true run_trajectory:=true
# Ctrl+C puis :
ros2 bag info atawi_demo_bag
```

---

## 13. Validation cinématique

Validations offline sans dépendance à RViz ou Gazebo.

### Validation complète FK/IK

```bash
python3 ~/ros2_ws/src/mon_robot_control/scripts/validate_kinematics.py
```

### Cinématique directe (RGS2-21)

```bash
python3 ~/ros2_ws/src/mon_robot_control/scripts/fk_validation.py
```

Modèle validé : `T_world_tool = Rz(q1) × Rz(q2) × Tz(0.010)`

| Test | q1 | q2 | Résultat attendu |
|---|---:|---:|---|
| Position neutre | 0° | 0° | yaw = 0° |
| Tête 90° | 90° | 0° | yaw = 90° |
| Rotor 90° | 0° | 90° | yaw = 90° |
| Configuration composée | 45° | 60° | yaw = 105° |

Artefact : `mon_robot_control/results/fk_results.txt`

### Cinématique inverse (RGS2-22)

```bash
python3 ~/ros2_ws/src/mon_robot_control/scripts/ik_validation.py
```

Pour une cible `yaw_target`, solution simple (rotations coaxiales) :

```text
q1 = yaw_target / 2
q2 = yaw_target / 2
```

| Cible yaw | Solution |
|---:|---|
| 0° | q = [0°, 0°] |
| 90° | q = [45°, 45°] |
| -120° | q = [-60°, -60°] |
| 180° | q = [90°, 90°] |

Artefact : `mon_robot_control/results/ik_results.txt`

### Espace atteignable (RGS2-24)

```bash
python3 ~/ros2_ws/src/mon_robot_control/scripts/workspace_visualization.py
```

Artefact : `mon_robot_control/results/workspace_3d.png`

Interprétation : l'effecteur `tool_link` est fixe en position (`z = 0.010 m`). L'espace atteignable en orientation couvre le yaw sur `[-180°, 180°]`.

---

## 14. Tests unitaires

```bash
cd ~/ros2_ws
colcon test --packages-select mon_robot_control
colcon test-result --verbose
```

Ou directement :

```bash
pytest src/ros2-robot-simulation-stage/mon_robot_control/test/
```

---

## 15. Docker

Construire l'image reproductible ROS 2 Jazzy :

```bash
docker build -f docker/Dockerfile -t atawi-3a3:jazzy .
```

Shell dans le conteneur :

```bash
docker run --rm -it atawi-3a3:jazzy
```

RViz (Linux + X11) :

```bash
xhost +local:docker
docker run --rm -it --net=host \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  atawi-3a3:jazzy \
  ros2 launch mon_robot_bringup display.launch.py
```

Gazebo :

```bash
docker run --rm -it --net=host \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  atawi-3a3:jazzy \
  ros2 launch mon_robot_bringup simulation.launch.py
```

Démo :

```bash
docker run --rm -it --net=host -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw atawi-3a3:jazzy \
  ros2 launch mon_robot_bringup demo.launch.py
```

---

## 16. CI GitHub Actions

Workflow : `.github/workflows/ci.yml`

Sur chaque push/PR vers `main` ou `master` :

1. génération des meshes placeholder ;
2. build colcon des 3 paquets ;
3. tests `mon_robot_control` ;
4. lint xacro (URDF Gazebo).

---

## 17. Documentation Doxygen

Configuration : `docs/Doxyfile`

```bash
doxygen docs/Doxyfile
```

Sortie : `docs/doxygen/html/index.html`

---

## 18. État d'avancement (stories RGS2)

### Stories réalisées

| ID | Story | Statut |
|---|---|---|
| RGS2-21 | Cinématique directe FK | Fait — `fk_validation.py` + `results/fk_results.txt` |
| RGS2-22 | Cinématique inverse IK | Fait — `ik_validation.py` + `results/ik_results.txt` |
| RGS2-23 | Trajectoire interpolée | Fait — `send_trajectory.py` installé et fonctionnel |
| RGS2-24 | Espace de travail atteignable | Fait — `workspace_visualization.py` |
| RGS2-28 | Documentation code | Fait — README + `docs/projet.md` + Doxygen |
| RGS2-29 | Paramètres DH / liens / joints | Fait — section 6 de ce document |

### Checklist intégration

| Point | Statut |
|---|---|
| Spawn Gazebo (`-topic robot_description`) | OK |
| `controllers_yaml` xacro | OK |
| `gz_ros2_control` + spawners JTC/JSB (sur événement) | OK |
| Action + topic trajectoire | OK |
| Module `robot_kinematics` + tests pytest | OK |
| Deps `package.xml` / Docker | OK |
| Legacy Humble / `gazebo_ros*` | Retiré |
| Meshes STL | Placeholder (non destructif) ou CAO |
| Bateau horizontal stable sur l'eau | OK |
| Odométrie 3D du bateau | OK (`/model/atawi_3a3/odometry`) |
| Hydrodynamique (courants, traînée) | Hors scope volontaire |
| CI GitHub Actions | OK |
| Démo | OK (`demo.launch.py`) |
| Rosbag session Gazebo | OK via `demo.launch.py record_bag:=true` |
| Vérification JTC | OK via `verify_controller_tracking.py` |
| Capteurs simulés | Backlog |

### Travaux restants possibles

- Ajouter des capteurs simulés
- Enregistrer une session `rosbag2`
- Rédiger le rapport technique
- Préparer slides et démo vidéo

> **Remarque :** si le modèle mécanique évolue vers un robot 3 DOF, les scripts FK/IK et cette documentation devront être mis à jour.

---

## 19. Dépannage

### `Package 'mon_robot_control' not found`

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 pkg list | grep mon_robot
```

### `No executable found`

```bash
chmod +x ~/ros2_ws/src/mon_robot_control/scripts/*.py
cd ~/ros2_ws
colcon build --symlink-install --packages-select mon_robot_control
source install/setup.bash
```

### `/usr/bin/env: 'python3\r': No such file or directory`

Fins de ligne Windows — corriger dans WSL :

```bash
sed -i 's/\r$//' ~/ros2_ws/src/mon_robot_control/scripts/*.py
chmod +x ~/ros2_ws/src/mon_robot_control/scripts/*.py
```

### `simulation.launch.py was not found`

Recopier et rebuilder `mon_robot_bringup` :

```bash
cd ~/ros2_ws/src
rm -rf mon_robot_bringup
cp -r /mnt/c/Users/FOKO/Documents/GitHub/ros2-robot-simulation-stage/mon_robot_bringup .
cd ~/ros2_ws
colcon build --symlink-install --packages-select mon_robot_bringup
source install/setup.bash
```

### Warnings `AMENT_PREFIX_PATH doesn't exist`

Non bloquants après `rm -rf install` dans un terminal déjà sourcé. Ouvrir un terminal neuf ou :

```bash
source /opt/ros/jazzy/setup.bash
```

---

## 20. Licence

MIT
