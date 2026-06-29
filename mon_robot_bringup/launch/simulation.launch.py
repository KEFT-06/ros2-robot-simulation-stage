import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    description_share = get_package_share_directory('mon_robot_description')
    bringup_share = get_package_share_directory('mon_robot_bringup')
    gazebo_resource_path = os.path.dirname(description_share)

    boat_x = LaunchConfiguration('boat_x')
    boat_y = LaunchConfiguration('boat_y')
    boat_z = LaunchConfiguration('boat_z')
    boat_roll = LaunchConfiguration('boat_roll')
    boat_pitch = LaunchConfiguration('boat_pitch')
    boat_yaw = LaunchConfiguration('boat_yaw')
    load_controllers = LaunchConfiguration('load_controllers')

    urdf_model_path = PathJoinSubstitution([
        FindPackageShare('mon_robot_description'),
        'urdf',
        'mon_robot.urdf.xacro',
    ])

    controllers_yaml = os.path.join(bringup_share, 'config', 'controllers.yaml')

    world_path = PathJoinSubstitution([
        FindPackageShare('mon_robot_bringup'),
        'worlds',
        'robot_world.sdf',
    ])

    robot_description = ParameterValue(
        Command([
            'xacro ', urdf_model_path,
            ' use_gazebo:=true',
            ' controllers_yaml:=', controllers_yaml,
        ]),
        value_type=str,
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True,
        }],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py',
            ]),
        ]),
        launch_arguments={'gz_args': ['-r -v 4 ', world_path]}.items(),
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'atawi_3a3',
            '-x', boat_x,
            '-y', boat_y,
            '-z', boat_z,
            '-R', boat_roll,
            '-P', boat_pitch,
            '-Y', boat_yaw,
            '-topic', 'robot_description',   # ← remplace -string
        ],
        output='screen',
        
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/model/atawi_3a3/odometry@nav_msgs/msg/Odometry[gz.msgs.Odometry',
        ],
        output='screen',
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        output='screen',
        condition=IfCondition(load_controllers),
    )

    joint_trajectory_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller', '--controller-manager', '/controller_manager'],
        output='screen',
        condition=IfCondition(load_controllers),
    )

    # Demarre les controleurs des que le spawn du robot est termine (robuste,
    # vs un delai fixe qui echoue sur machine lente / 1er lancement Gazebo).
    controllers_after_spawn = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_robot,
            on_exit=[joint_state_broadcaster_spawner, joint_trajectory_controller_spawner],
        )
    )

    return LaunchDescription([
        AppendEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=gazebo_resource_path,
        ),
        DeclareLaunchArgument('boat_x', default_value='0.0'),
        DeclareLaunchArgument('boat_y', default_value='0.0'),
        # Spawn proche de l'equilibre de flottaison (~ -0.11 m, calcule depuis la
        # masse ~0.79 kg et la section de coque) pour minimiser le rebond initial.
        DeclareLaunchArgument('boat_z', default_value='-0.1'),
        DeclareLaunchArgument('boat_roll', default_value='0.0'),
        # Horizontal (pitch=0). L'ancienne valeur 1.5708 mettait le bateau a la verticale.
        DeclareLaunchArgument('boat_pitch', default_value='0.0'),
        DeclareLaunchArgument('boat_yaw', default_value='0.0'),
        DeclareLaunchArgument(
            'load_controllers',
            default_value='true',
            description='Spawn joint_state_broadcaster and joint_trajectory_controller',
        ),
        robot_state_publisher,
        gazebo,
        spawn_robot,
        bridge,
        controllers_after_spawn,
    ])
