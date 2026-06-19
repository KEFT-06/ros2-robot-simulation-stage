# Reproducible ROS 2 Jazzy environment for the ATAWI-3A3 robot project.
#
# Build:
#   docker build -t atawi-3a3:jazzy .
#
# Run shell:
#   docker run --rm -it atawi-3a3:jazzy
#
# Run RViz/Gazebo with X11 on Linux:
#   xhost +local:docker
#   docker run --rm -it --net=host \
#     -e DISPLAY=$DISPLAY \
#     -e QT_X11_NO_MITSHM=1 \
#     -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
#     atawi-3a3:jazzy

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
    ros-jazzy-control-msgs \
    ros-jazzy-controller-manager \
    python3-pytest \
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
    ros-jazzy-xacro \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${ROS_WS}

COPY . ${ROS_WS}/src/ros2-robot-simulation-stage

# Normalize scripts copied from Windows and make them executable in Linux.
RUN find ${ROS_WS}/src/ros2-robot-simulation-stage/mon_robot_control/scripts \
      -type f -name "*.py" -exec sed -i 's/\r$//' {} \; \
    && chmod +x ${ROS_WS}/src/ros2-robot-simulation-stage/mon_robot_control/scripts/*.py

RUN source /opt/ros/${ROS_DISTRO}/setup.bash \
    && colcon build --symlink-install

COPY docker/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh \
    && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
