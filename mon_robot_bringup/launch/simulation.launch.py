from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
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
    
    controllers_config = PathJoinSubstitution([
        FindPackageShare('mon_robot_bringup'),
        'config',
        'controllers.yaml'
    ])

    robot_description = Command(['xacro ', urdf_model_path])

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
        launch_arguments={'gz_args': world_path}.items()
    )

    # Spawn robot in Gazebo
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'mon_robot',
            '-x', '0',
            '-y', '0',
            '-z', '0.1',
            '-file', urdf_model_path
        ],
        output='screen'
    )

    # Bridge Gazebo/ROS 2
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model'
        ]
    )

    # Load Joint State Broadcaster
    spawn_jsb = TimerAction(
        period=5.0,
        actions=[
            ExecuteProcess(
                cmd=['ros2', 'control', 'load_controller',
                     '--set-state', 'active',
                     'joint_state_broadcaster'],
                output='screen'
            )
        ]
    )

    # Load Joint Trajectory Controller
    spawn_jtc = TimerAction(
        period=7.0,
        actions=[
            ExecuteProcess(
                cmd=['ros2', 'control', 'load_controller',
                     '--set-state', 'active',
                     'joint_trajectory_controller'],
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        robot_state_publisher,
        gazebo,
        spawn_robot,
        bridge,
        spawn_jsb,
        spawn_jtc,
    ])
