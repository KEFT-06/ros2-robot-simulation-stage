from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    bag_name = LaunchConfiguration('bag_name')
    record_bag = LaunchConfiguration('record_bag')
    run_trajectory = LaunchConfiguration('run_trajectory')
    trajectory_type = LaunchConfiguration('trajectory_type')
    verify_controller = LaunchConfiguration('verify_controller')

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('mon_robot_bringup'),
                'launch',
                'simulation.launch.py',
            ]),
        ]),
        launch_arguments={'load_controllers': 'true'}.items(),
    )

    trajectory = TimerAction(
        period=10.0,
        actions=[
            ExecuteProcess(
                cmd=['ros2', 'run', 'mon_robot_control', 'send_trajectory.py', trajectory_type],
                output='screen',
                condition=IfCondition(run_trajectory),
            ),
        ],
    )

    bag_record = TimerAction(
        period=5.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'bag', 'record', '-o', bag_name,
                    '/joint_states', '/tf', '/tf_static', '/clock',
                    '/model/atawi_3a3/odometry',
                ],
                output='screen',
                condition=IfCondition(record_bag),
            ),
        ],
    )

    controller_check = TimerAction(
        period=22.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'run', 'mon_robot_control',
                    'verify_controller_tracking.py',
                ],
                output='screen',
                condition=IfCondition(verify_controller),
            ),
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument('run_trajectory', default_value='true'),
        DeclareLaunchArgument('trajectory_type', default_value='sweep'),
        DeclareLaunchArgument('record_bag', default_value='false'),
        DeclareLaunchArgument('bag_name', default_value='atawi_demo_bag'),
        DeclareLaunchArgument('verify_controller', default_value='false'),
        simulation,
        bag_record,
        trajectory,
        controller_check,
    ])
