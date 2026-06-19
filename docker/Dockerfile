# Reproducible ROS 2 Jazzy environment for the ATAWI-3A3 robot project.

FROM ros:jazzy-ros-base

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=jazzy
ENV ROS_WS=/ros2_ws
ENV QT_X11_NO_MITSHM=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash-completion \
    build-essential \
    doxygen \
    git \
    python3-colcon-common-extensions \
    python3-matplotlib \
    python3-numpy \
    python3-pip \
    python3-pytest \
    ros-jazzy-control-msgs \
    ros-jazzy-controller-manager \
    ros-jazzy-gz-ros2-control \
    ros-jazzy-joint-state-broadcaster \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-joint-trajectory-controller \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros2-control \
    ros-jazzy-ros2-controllers \
    ros-jazzy-rviz2 \
    ros-jazzy-ament-cmake-python \
    ros-jazzy-rosbag2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${ROS_WS}

COPY . ${ROS_WS}/src/ros2-robot-simulation-stage

RUN find ${ROS_WS}/src/ros2-robot-simulation-stage/mon_robot_control/scripts \
      -type f -name "*.py" -exec sed -i 's/\r$//' {} \; \
    && chmod +x ${ROS_WS}/src/ros2-robot-simulation-stage/mon_robot_control/scripts/*.py \
    && cp -r ${ROS_WS}/src/ros2-robot-simulation-stage/mon_robot_* ${ROS_WS}/src/ \
    && python3 ${ROS_WS}/src/ros2-robot-simulation-stage/mon_robot_description/scripts/generate_placeholder_meshes.py

RUN source /opt/ros/${ROS_DISTRO}/setup.bash \
    && cd ${ROS_WS} \
    && colcon build --symlink-install \
    && colcon test --packages-select mon_robot_control \
    && colcon test-result --verbose

COPY docker/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
