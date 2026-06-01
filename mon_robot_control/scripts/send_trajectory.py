#!/usr/bin/env python3
"""
Script pour envoyer une trajectoire au contrôleur du robot.
"""

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


class TrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('trajectory_publisher')
        self.publisher = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )
        self.get_logger().info('TrajectoryPublisher initialized')

    def send_goal(self, joint_angles, time_sec=3):
        """
        Envoie une trajectoire au contrôleur.
        
        Args:
            joint_angles: list of target angles [joint1, joint2]
            time_sec: time to reach goal in seconds
        """
        trajectory = JointTrajectory()
        trajectory.joint_names = ['joint1', 'joint2']
        
        point = JointTrajectoryPoint()
        point.positions = joint_angles
        point.velocities = [0.0, 0.0]
        point.time_from_start = Duration(sec=int(time_sec), nanosec=0)
        
        trajectory.points.append(point)
        
        self.publisher.publish(trajectory)
        self.get_logger().info(f'Trajectory sent: {joint_angles} in {time_sec}s')


def main():
    rclpy.init()
    node = TrajectoryPublisher()
    
    # Example: joint1 -> 90 deg, joint2 -> -45 deg
    node.send_goal([1.57, -0.78], time_sec=3)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
