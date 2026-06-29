cmake_minimum_required(VERSION 3.8)
project(mon_robot_control)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

ament_python_install_package(${PROJECT_NAME})

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

if(BUILD_TESTING)
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(test_kinematics test/test_kinematics.py
    APPEND_ENV PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR})
  ament_add_pytest_test(test_trajectory_node test/test_trajectory_node.py
    APPEND_ENV PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR})
endif()

ament_package()
