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
        
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        self.target_frame = 'link2'
        self.reference_frame = 'base_link'
        
        self.create_timer(1.0, self.check_fk)

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
