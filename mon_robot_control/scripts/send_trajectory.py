#!/usr/bin/env python3
"""
Script pour envoyer des trajectoires au robot ATAWI-3A3 via ROS 2
Compatible avec le JointTrajectoryController
"""

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import math
import sys


class TrajectoryPublisher(Node):
    """Nœud ROS 2 pour publier des trajectoires"""
    
    def __init__(self):
        super().__init__('trajectory_publisher')
        
        # Éditeur de trajectoires
        self.publisher_ = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )
        
        # Noms des articulations commandees dans l'URDF actuel
        self.joint_names = [
            'joint1_head',
            'joint2_rotor'
        ]
        
        # Limites articulaires
        self.joint_limits = {
            'joint1_head': (-math.pi, math.pi),
            'joint2_rotor': (-math.pi, math.pi)
        }
        
        self.get_logger().info("Trajectory Publisher initialisé")
        self.get_logger().info(f"Topics de publication: /joint_trajectory_controller/joint_trajectory")
    
    def publish_trajectory(self, waypoints, time_from_start=None):
        """
        Publie une trajectoire
        
        Args:
            waypoints: Liste de listes de positions articulaires
            time_from_start: Liste des temps (s) ou None pour espacement uniforme
        """
        trajectory = JointTrajectory()
        trajectory.joint_names = self.joint_names
        trajectory.header.frame_id = "base_link"
        
        # Espacement uniforme si temps non spécifié
        if time_from_start is None:
            time_from_start = [i * 2.0 for i in range(len(waypoints))]
        
        for positions, time_sec in zip(waypoints, time_from_start):
            # Vérifier les limites
            for joint_name, pos in zip(self.joint_names, positions):
                q_min, q_max = self.joint_limits[joint_name]
                if not (q_min <= pos <= q_max):
                    self.get_logger().warn(
                        f"Position {joint_name}={math.degrees(pos):.1f}° hors limites "
                        f"[{math.degrees(q_min):.1f}°, {math.degrees(q_max):.1f}°]"
                    )
            
            point = JointTrajectoryPoint()
            point.positions = list(positions)
            point.velocities = [0.0] * len(self.joint_names)
            point.accelerations = [0.0] * len(self.joint_names)
            point.time_from_start = Duration(sec=int(time_sec), nanosec=int((time_sec % 1) * 1e9))
            
            trajectory.points.append(point)
        
        self.publisher_.publish(trajectory)
        self.get_logger().info(f"Trajectoire publiée: {len(trajectory.points)} points")
        
        for i, point in enumerate(trajectory.points):
            angles_deg = [math.degrees(p) for p in point.positions]
            self.get_logger().info(
                f"  Point {i}: [{angles_deg[0]:.1f}°, {angles_deg[1]:.1f}°] "
                f"t={point.time_from_start.sec}s"
            )
    
    def trajectory_home(self):
        """Trajectoire vers position de repos"""
        self.get_logger().info("\n📍 Trajectoire HOME (repos)")
        waypoints = [
            [0.0, 0.0]  # Position de repos
        ]
        self.publish_trajectory(waypoints, [3.0])
    
    def trajectory_sweep_z(self):
        """Trajectoire circulaire en rotation Z"""
        self.get_logger().info("\n🔄 Trajectoire SWEEP Z (rotation base)")
        waypoints = [
            [0.0, 0.0],
            [math.pi/4, 0.0],
            [math.pi/2, 0.0],
            [-math.pi/2, 0.0],
            [-math.pi/4, 0.0],
            [0.0, 0.0]
        ]
        times = [i * 1.0 for i in range(len(waypoints))]
        self.publish_trajectory(waypoints, times)
    
    def trajectory_spin_rotor(self):
        """Trajectoire de rotation du rotor"""
        self.get_logger().info("\n💪 Trajectoire SPIN ROTOR")
        waypoints = [
            [0.0, 0.0],
            [0.0, math.pi/2],
            [0.0, math.pi],
            [0.0, -math.pi],
            [0.0, 0.0]
        ]
        times = [i * 1.0 for i in range(len(waypoints))]
        self.publish_trajectory(waypoints, times)
    
    def trajectory_complex(self):
        """Trajectoire complexe multi-articulaire"""
        self.get_logger().info("\n🎯 Trajectoire COMPLEXE (multi-articulations)")
        waypoints = [
            [0.0, 0.0],
            [math.pi/6, math.pi/4],
            [math.pi/3, math.pi/2],
            [math.pi/2, 0.0],
            [math.pi/4, -math.pi/2],
            [0.0, 0.0]
        ]
        times = [i * 1.5 for i in range(len(waypoints))]
        self.publish_trajectory(waypoints, times)
    
    def trajectory_sine_wave(self):
        """Trajectoire ondulante avec sinus"""
        self.get_logger().info("\n〰️ Trajectoire SINE WAVE")
        waypoints = []
        times = []
        
        for i in range(20):
            t = i * 0.1
            q1 = math.sin(t)
            q2 = math.cos(t) * math.pi / 4
            
            waypoints.append([q1, q2])
            times.append(t * 2.0)
        
        self.publish_trajectory(waypoints, times)


def main():
    rclpy.init()
    node = TrajectoryPublisher()
    
    if len(sys.argv) > 1:
        traj_type = sys.argv[1].lower()
    else:
        traj_type = "home"
    
    # Sélectionner la trajectoire
    trajectories = {
        'home': node.trajectory_home,
        'sweep': node.trajectory_sweep_z,
        'spin': node.trajectory_spin_rotor,
        'complex': node.trajectory_complex,
        'sine': node.trajectory_sine_wave
    }
    
    if traj_type in trajectories:
        trajectories[traj_type]()
    else:
        node.get_logger().error(f"Trajectoire inconnue: {traj_type}")
        node.get_logger().info(f"Options disponibles: {', '.join(trajectories.keys())}")
    
    # Garder le nœud actif quelques secondes
    rclpy.spin_once(node, timeout_sec=2.0)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
