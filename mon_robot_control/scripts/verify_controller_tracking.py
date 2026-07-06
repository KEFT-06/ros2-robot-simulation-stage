#!/usr/bin/env python3
"""Verifie que joint_trajectory_controller suit une consigne simple."""

import argparse
import sys
import time

import rclpy
from builtin_interfaces.msg import Duration
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.utilities import remove_ros_args
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectoryPoint

from mon_robot_control.robot_kinematics import RobotKinematics


class ControllerTrackingVerifier(Node):
    def __init__(self, tolerance, settle_timeout):
        super().__init__('controller_tracking_verifier')
        self.tolerance = float(tolerance)
        self.settle_timeout = float(settle_timeout)
        self.joint_names = list(RobotKinematics.JOINT_NAMES)
        self.target = [0.35, -0.25]
        self.latest_positions = None
        self._action_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/joint_trajectory_controller/follow_joint_trajectory',
        )
        self.create_subscription(
            JointState,
            '/joint_states',
            self._on_joint_state,
            10,
        )

    def _on_joint_state(self, msg):
        positions_by_name = dict(zip(msg.name, msg.position))
        if all(name in positions_by_name for name in self.joint_names):
            self.latest_positions = [positions_by_name[name] for name in self.joint_names]

    def run(self):
        if not self._action_client.wait_for_server(timeout_sec=15.0):
            self.get_logger().error('Action FollowJointTrajectory indisponible')
            return 2

        goal = FollowJointTrajectory.Goal()
        goal.trajectory.joint_names = self.joint_names
        goal.trajectory.header.stamp = self.get_clock().now().to_msg()

        for sec, positions in ((2, [0.0, 0.0]), (5, self.target)):
            point = JointTrajectoryPoint()
            point.positions = positions
            point.velocities = [0.0, 0.0]
            point.time_from_start = Duration(sec=sec)
            goal.trajectory.points.append(point)

        self.get_logger().info(f'Envoi consigne de test: {self.target}')
        future = self._action_client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future, timeout_sec=10.0)
        goal_handle = future.result()
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().error('Goal refuse par joint_trajectory_controller')
            return 3

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future, timeout_sec=15.0)
        result = result_future.result()
        if result is None:
            self.get_logger().warn(
                'Aucun resultat action recu avant timeout; validation par /joint_states.'
            )
        elif result.result.error_code != 0:
            self.get_logger().error(
                f'Action terminee en erreur: code={result.result.error_code} '
                f'message="{result.result.error_string}"'
            )
            return 5

        deadline = time.monotonic() + self.settle_timeout
        while time.monotonic() < deadline:
            rclpy.spin_once(self, timeout_sec=0.2)
            if self.latest_positions is None:
                continue
            errors = [
                abs(actual - expected)
                for actual, expected in zip(self.latest_positions, self.target)
            ]
            if max(errors) <= self.tolerance:
                self.get_logger().info(
                    'PASS suivi trajectoire: '
                    f'positions={self.latest_positions} target={self.target} '
                    f'erreurs={errors}'
                )
                return 0

        self.get_logger().error(
            'FAIL suivi trajectoire: '
            f'positions={self.latest_positions} target={self.target} '
            f'tolerance={self.tolerance}'
        )
        return 6


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--tolerance', type=float, default=0.08)
    parser.add_argument('--settle-timeout', type=float, default=5.0)
    return parser.parse_args(remove_ros_args(args=argv)[1:])


def main(argv=None):
    argv = sys.argv if argv is None else argv
    args = parse_args(argv)
    rclpy.init(args=argv)
    node = ControllerTrackingVerifier(args.tolerance, args.settle_timeout)
    try:
        return node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    sys.exit(main())
