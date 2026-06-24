#!/usr/bin/env python3
"""
Script pour valider la cinématique directe (Forward Kinematics).
"""

import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer
import math


class FKValidator(Node):
    def __init__(self):
        super().__init__('fk_validator')
        self._declare_parameter('reference_frame', 'base_link')
        self._declare_parameter('target_frame', 'tool_link')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.reference_frame = self.get_parameter('reference_frame').value
        self.target_frame = self.get_parameter('target_frame').value

        self.create_timer(1.0, self.check_fk)

    def _declare_parameter(self, name, default):
        """Declare un parametre seulement s'il ne l'est pas deja.

        Evite ParameterAlreadyDeclaredException quand le parametre a deja ete
        injecte (ex: use_sim_time fourni par le launch ou auto-declare rclpy).
        """
        if not self.has_parameter(name):
            self.declare_parameter(name, default)
        return self.get_parameter(name).value

    def check_fk(self):
        """Vérifie et affiche la position du end-effector."""
        try:
            transform = self.tf_buffer.lookup_transform(
                self.reference_frame,
                self.target_frame,
                rclpy.time.Time()
            )
            
            pos = transform.transform.translation
            
            self.get_logger().info(
                f'End-effector position: '
                f'x={pos.x:.4f}  y={pos.y:.4f}  z={pos.z:.4f}'
            )
        except Exception as e:
            self.get_logger().warn(f'Transform non disponible : {e}')


def main():
    rclpy.init()
    node = FKValidator()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
