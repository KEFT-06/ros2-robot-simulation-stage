from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    urdf_file = PathJoinSubstitution([
        FindPackageShare('mon_robot_description'),
        'urdf',
        'mon_robot.urdf.xacro',
    ])

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': ParameterValue(
                Command(['xacro ', urdf_file]),
                value_type=str,
            )
        }]
    )

    return LaunchDescription([
        robot_state_publisher_node
    ])
