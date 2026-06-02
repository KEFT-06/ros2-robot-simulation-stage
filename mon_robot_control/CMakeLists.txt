cmake_minimum_required(VERSION 3.8)
project(mon_robot_control)

# Find python before ament_cmake
find_package(python3 REQUIRED)
find_package(ament_cmake_python REQUIRED)

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(trajectory_msgs REQUIRED)

ament_python_install_package(${PROJECT_NAME})

# Install Python executables
install(
  PROGRAMS
    scripts/send_trajectory.py
    scripts/validate_kinematics.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
