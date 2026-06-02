#!/bin/bash
# Script d'installation automatique du projet ros2-robot-simulation-stage
# Usage: chmod +x setup.sh && ./setup.sh

set -e

echo "================================"
echo "🚀 Installation du projet ATAWI-3A3"
echo "================================"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier Ubuntu 22.04
if ! grep -q "22.04" /etc/lsb-release; then
    echo -e "${RED}❌ Ubuntu 22.04 LTS requis${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Ubuntu 22.04 LTS détecté${NC}"

# Vérifier ROS 2 Humble
if ! command -v ros2 &> /dev/null; then
    echo -e "${YELLOW}⚠️ ROS 2 non trouvé. Installation...${NC}"
    sudo apt update
    sudo apt install -y software-properties-common
    sudo add-apt-repository universe
    sudo apt update
    sudo apt install -y curl gnupg lsb-release
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
    sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main"
    sudo apt update
    sudo apt install -y ros-humble-desktop
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
    source ~/.bashrc
else
    echo -e "${GREEN}✓ ROS 2 Humble détecté${NC}"
fi

# Installer les dépendances ROS
echo -e "${YELLOW}📦 Installation des dépendances ROS 2...${NC}"
sudo apt update
sudo apt install -y \
    ros-humble-gazebo-ros \
    ros-humble-gazebo-ros2-control \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-joint-state-publisher-gui \
    ros-humble-robot-state-publisher \
    ros-humble-rviz2 \
    ros-humble-tf2-tools \
    freecad \
    python3-freecad \
    python3-pip

echo -e "${GREEN}✓ Dépendances installées${NC}"

# Créer le workspace s'il n'existe pas
WORKSPACE="${HOME}/ros2_ws"
if [ ! -d "$WORKSPACE" ]; then
    echo -e "${YELLOW}📂 Création du workspace ROS 2...${NC}"
    mkdir -p "$WORKSPACE/src"
    cd "$WORKSPACE"
    colcon build --symlink-install || echo -e "${YELLOW}⚠️ colcon build a échoué (normal pour workspace vide)${NC}"
fi

echo -e "${GREEN}✓ Workspace créé: $WORKSPACE${NC}"

# Compiler le projet
echo -e "${YELLOW}🔨 Compilation du projet...${NC}"
cd "$WORKSPACE"
source /opt/ros/humble/setup.bash
colcon build --symlink-install

echo -e "${GREEN}✓ Compilation réussie${NC}"

# Convertir les meshes STEP
echo -e "${YELLOW}🔄 Conversion des fichiers STEP en STL...${NC}"
cd "$WORKSPACE/src/ros2-robot-simulation-stage"

if [ -f "convert_meshes.py" ]; then
    python3 convert_meshes.py || echo -e "${YELLOW}⚠️ Conversion échouée (FreeCAD peut être nécessaire)${NC}"
fi

echo -e "${GREEN}✓ Installation complète!${NC}"
echo ""
echo "================================"
echo "🎯 Prochaines étapes:"
echo "================================"
echo ""
echo "1️⃣  Sourcer le workspace:"
echo "   source $WORKSPACE/install/setup.bash"
echo ""
echo "2️⃣  Affichage RViz simple:"
echo "   ros2 launch mon_robot_bringup display.launch.py"
echo ""
echo "3️⃣  Simulation complète Gazebo:"
echo "   ros2 launch mon_robot_bringup simulation.launch.py"
echo ""
echo "4️⃣  Tester cinématique:"
echo "   python3 $WORKSPACE/src/ros2-robot-simulation-stage/mon_robot_control/scripts/validate_kinematics.py"
echo ""
echo -e "${GREEN}Bonne chance! 🚀${NC}"
