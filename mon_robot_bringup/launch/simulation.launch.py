import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    description_share = get_package_share_directory('mon_robot_description')
    gazebo_resource_path = os.path.dirname(description_share)

    boat_x = LaunchConfiguration('boat_x')
    boat_y = LaunchConfiguration('boat_y')
    boat_z = LaunchConfiguration('boat_z')
    boat_roll = LaunchConfiguration('boat_roll')
    boat_pitch = LaunchConfiguration('boat_pitch')
    boat_yaw = LaunchConfiguration('boat_yaw')
    load_controllers = LaunchConfiguration('load_controllers')

    # Paths
    urdf_model_path = PathJoinSubstitution([
        FindPackageShare('mon_robot_description'),
        'urdf',
        'mon_robot.urdf.xacro'
    ])
    
    world_path = PathJoinSubstitution([
        FindPackageShare('mon_robot_bringup'),
        'worlds',
        'robot_world.sdf'
    ])

    robot_description = Command(['xacro ', urdf_model_path, ' use_gazebo:=true'])

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )

    # Gazebo Simulator
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            ])
        ]),
        launch_arguments={
            'gz_args': [world_path, ' -v 4']
        }.items()
    )

    # Spawn robot in Gazebo
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
            '-topic', '/robot_description'
        ],
        output='screen'
    )

    # Bridge Gazebo/ROS 2 - Topics
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/atawi_3a3/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model'
        ],
        remappings=[
            ('/atawi_3a3/joint_states', '/joint_states')
        ],
        output='screen'
    )

    # Load Joint State Broadcaster
    load_jsb = TimerAction(
        period=3.0,
        actions=[
            ExecuteProcess(
                cmd=['ros2', 'control', 'load_controller',
                     '--set-state', 'active',
                     'joint_state_broadcaster'],
                output='screen',
                condition=IfCondition(load_controllers)
            )
        ]
    )

    # Load Joint Trajectory Controller
    load_jtc = TimerAction(
        period=6.0,
        actions=[
            ExecuteProcess(
                cmd=['ros2', 'control', 'load_controller',
                     '--set-state', 'active',
                     'joint_trajectory_controller'],
                output='screen',
                condition=IfCondition(load_controllers)
            )
        ]
    )

    return LaunchDescription([
        AppendEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=gazebo_resource_path
        ),
        DeclareLaunchArgument(
            'boat_x',
            default_value='0.0',
            description='Initial boat X position in Gazebo'
        ),
        DeclareLaunchArgument(
            'boat_y',
            default_value='0.0',
            description='Initial boat Y position in Gazebo'
        ),
        DeclareLaunchArgument(
            'boat_z',
            default_value='0.12',
            description='Initial boat Z position relative to the water surface'
        ),
        DeclareLaunchArgument(
            'boat_roll',
            default_value='0.0',
            description='Initial boat roll in radians'
        ),
        DeclareLaunchArgument(
            'boat_pitch',
            default_value='1.5708',
            description='Initial boat pitch in radians; adjust if the mesh is not horizontal'
        ),
        DeclareLaunchArgument(
            'boat_yaw',
            default_value='0.0',
            description='Initial boat yaw in radians'
        ),
        DeclareLaunchArgument(
            'load_controllers',
            default_value='false',
            description='Load ros2_control controllers. Keep false unless gz_ros2_control is confirmed active.'
        ),
        robot_state_publisher,
        gazebo,
        spawn_robot,
        bridge,
        load_jsb,
        load_jtc,
    ])
