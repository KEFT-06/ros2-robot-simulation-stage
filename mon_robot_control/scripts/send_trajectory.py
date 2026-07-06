#!/usr/bin/env python3
"""Publie des trajectoires via action FollowJointTrajectory ou topic JointTrajectory."""

import math
import sys

import rclpy
from builtin_interfaces.msg import Duration
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from mon_robot_control.robot_kinematics import RobotKinematics


class TrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('trajectory_publisher')

        self._declare_parameter('use_action', True)
        self._declare_parameter(
            'trajectory_topic',
            '/joint_trajectory_controller/joint_trajectory',
        )
        self._declare_parameter(
            'action_name',
            '/joint_trajectory_controller/follow_joint_trajectory',
        )

        self.use_action = self.get_parameter('use_action').value
        self.joint_names = list(RobotKinematics.JOINT_NAMES)

        if self.use_action:
            action_name = self.get_parameter('action_name').value
            self._action_client = ActionClient(
                self, FollowJointTrajectory, action_name)
        else:
            topic = self.get_parameter('trajectory_topic').value
            qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
            self._publisher = self.create_publisher(JointTrajectory, topic, qos)

        self.get_logger().info(
            f"Mode={'action' if self.use_action else 'topic'} "
            f'joints={self.joint_names}'
        )

    def _declare_parameter(self, name, default):
        """Declare un parametre seulement s'il ne l'est pas deja.

        Evite ParameterAlreadyDeclaredException quand le parametre a deja ete
        injecte (ex: use_sim_time fourni par le launch ou auto-declare rclpy).
        """
        if not self.has_parameter(name):
            self.declare_parameter(name, default)
        return self.get_parameter(name).value

    def _build_waypoints(self, waypoints, time_from_start):
        if time_from_start is None:
            time_from_start = [float(i * 2.0) for i in range(len(waypoints))]
        return list(zip(waypoints, time_from_start))

    def publish_trajectory(self, waypoints, time_from_start=None):
        pairs = self._build_waypoints(waypoints, time_from_start)

        if self.use_action:
            return self._send_action(pairs)
        return self._publish_topic(pairs)

    def _publish_topic(self, pairs):
        msg = JointTrajectory()
        msg.joint_names = self.joint_names
        msg.header.frame_id = 'base_link'
        msg.header.stamp = self.get_clock().now().to_msg()

        for positions, time_sec in pairs:
            point = JointTrajectoryPoint()
            point.positions = list(positions)
            point.velocities = [0.0] * len(self.joint_names)
            point.accelerations = [0.0] * len(self.joint_names)
            point.time_from_start = Duration(
                sec=int(time_sec),
                nanosec=int((time_sec % 1) * 1e9),
            )
            msg.points.append(point)

        self._publisher.publish(msg)
        self.get_logger().info(f'Trajectoire publiee (topic): {len(msg.points)} points')
        return True

    def _send_action(self, pairs):
        if not self._action_client.wait_for_server(timeout_sec=10.0):
            self.get_logger().error('Action server FollowJointTrajectory indisponible')
            return False

        goal = FollowJointTrajectory.Goal()
        goal.trajectory.joint_names = self.joint_names
        goal.trajectory.header.frame_id = 'base_link'
        goal.trajectory.header.stamp = self.get_clock().now().to_msg()

        for positions, time_sec in pairs:
            point = JointTrajectoryPoint()
            point.positions = list(positions)
            point.velocities = [0.0] * len(self.joint_names)
            point.time_from_start = Duration(
                sec=int(time_sec),
                nanosec=int((time_sec % 1) * 1e9),
            )
            goal.trajectory.points.append(point)

        future = self._action_client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future, timeout_sec=15.0)
        goal_handle = future.result()
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().error('Goal rejete par joint_trajectory_controller')
            return False

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future, timeout_sec=30.0)
        result = result_future.result()
        if result is None:
            self.get_logger().warn(
                'Goal accepte, mais aucun resultat action recu avant timeout; '
                'utilisez verify_controller_tracking.py pour valider /joint_states.'
            )
            return True
        if result.result.error_code != 0:
            self.get_logger().error(
                f'Trajectoire terminee en erreur: code={result.result.error_code} '
                f'message="{result.result.error_string}"'
            )
            return False

        self.get_logger().info('Trajectoire executee (action)')
        return True

    def trajectory_home(self):
        return self.publish_trajectory([[0.0, 0.0]], [3.0])

    def trajectory_sweep_z(self):
        waypoints = [
            [0.0, 0.0],
            [math.pi / 4, 0.0],
            [math.pi / 2, 0.0],
            [-math.pi / 2, 0.0],
            [-math.pi / 4, 0.0],
            [0.0, 0.0],
        ]
        return self.publish_trajectory(waypoints, [float(i) for i in range(len(waypoints))])

    def trajectory_spin_rotor(self):
        waypoints = [
            [0.0, 0.0],
            [0.0, math.pi / 2],
            [0.0, math.pi],
            [0.0, -math.pi],
            [0.0, 0.0],
        ]
        return self.publish_trajectory(waypoints, [float(i) for i in range(len(waypoints))])

    def trajectory_complex(self):
        waypoints = [
            [0.0, 0.0],
            [math.pi / 6, math.pi / 4],
            [math.pi / 3, math.pi / 2],
            [math.pi / 2, 0.0],
            [math.pi / 4, -math.pi / 2],
            [0.0, 0.0],
        ]
        return self.publish_trajectory(waypoints, [float(i * 1.5) for i in range(len(waypoints))])

    def trajectory_sine_wave(self):
        waypoints = []
        times = []
        for i in range(20):
            t = i * 0.1
            waypoints.append([math.sin(t), math.cos(t) * math.pi / 4])
            times.append(t * 2.0)
        return self.publish_trajectory(waypoints, times)


def main():
    rclpy.init()
    node = TrajectoryPublisher()

    traj_type = sys.argv[1].lower() if len(sys.argv) > 1 else 'home'
    trajectories = {
        'home': node.trajectory_home,
        'sweep': node.trajectory_sweep_z,
        'spin': node.trajectory_spin_rotor,
        'complex': node.trajectory_complex,
        'sine': node.trajectory_sine_wave,
    }

    exit_code = 0
    if traj_type in trajectories:
        if not trajectories[traj_type]():
            exit_code = 1
    else:
        node.get_logger().error(f'Trajectoire inconnue: {traj_type}')
        node.get_logger().info(f'Options: {", ".join(trajectories)}')
        exit_code = 2

    node.destroy_node()
    rclpy.shutdown()
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
