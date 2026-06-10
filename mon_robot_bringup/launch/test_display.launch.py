from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_share = FindPackageShare('mon_robot_description').find('mon_robot_description')
    urdf_file = PathJoinSubstitution([pkg_share, 'urdf', 'mon_robot.urdf.xacro'])

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_file])
        }]
    )

    return LaunchDescription([
        robot_state_publisher_node
    ])