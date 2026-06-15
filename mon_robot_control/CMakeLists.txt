cmake_minimum_required(VERSION 3.8)
project(mon_robot_control)

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(trajectory_msgs REQUIRED)

# Install Python executables
install(
  PROGRAMS
    scripts/send_trajectory.py
    scripts/validate_kinematics.py
    scripts/fk_validation.py
    scripts/ik_validation.py
    scripts/validate_fk.py
    scripts/workspace_visualization.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
