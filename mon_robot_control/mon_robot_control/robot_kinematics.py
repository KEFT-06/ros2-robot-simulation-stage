"""Cinematique 2 DOF coaxiale ATAWI-3A3 (joint1_head + joint2_rotor)."""

import math


class RobotKinematics:
    """FK/IK coherente avec mon_robot.urdf.xacro."""

    JOINT_NAMES = ['joint1_head', 'joint2_rotor']
    Q_MIN = (-math.pi, -math.pi)
    Q_MAX = (math.pi, math.pi)
    TOOL_OFFSET = (0.0, 0.0, 0.010)

    @staticmethod
    def wrap_pi(angle):
        return math.atan2(math.sin(angle), math.cos(angle))

    @staticmethod
    def rotz(theta):
        c = math.cos(theta)
        s = math.sin(theta)
        return [
            [c, -s, 0.0],
            [s, c, 0.0],
            [0.0, 0.0, 1.0],
        ]

    @classmethod
    def forward_kinematics(cls, q):
        if len(q) != 2:
            raise ValueError('Expected [joint1_head, joint2_rotor]')
        yaw = cls.wrap_pi(q[0] + q[1])
        return list(cls.TOOL_OFFSET), cls.rotz(yaw)

    @classmethod
    def forward_kinematics_yaw(cls, q):
        return cls.wrap_pi(q[0] + q[1])

    @classmethod
    def inverse_kinematics_orientation(cls, yaw_target):
        yaw = cls.wrap_pi(yaw_target)
        q = [yaw / 2.0, yaw / 2.0]
        ok = all(
            cls.Q_MIN[i] <= q[i] <= cls.Q_MAX[i]
            for i in range(2)
        )
        return q, ok

    @classmethod
    def workspace_yaw_samples(cls, n=32):
        yaws = set()
        step = (cls.Q_MAX[0] - cls.Q_MIN[0]) / (n - 1)
        for i in range(n):
            q = cls.Q_MIN[0] + i * step
            yaws.add(round(cls.forward_kinematics_yaw([q, 0.0]), 6))
            yaws.add(round(cls.forward_kinematics_yaw([0.0, q]), 6))
            yaws.add(round(cls.forward_kinematics_yaw([q, q]), 6))
        return sorted(yaws)
