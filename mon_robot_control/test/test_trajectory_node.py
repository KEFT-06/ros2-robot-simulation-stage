import math

import pytest
from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from mon_robot_control.robot_kinematics import RobotKinematics


def test_joint_trajectory_message_structure():
    traj = JointTrajectory()
    traj.joint_names = list(RobotKinematics.JOINT_NAMES)
    traj.header.frame_id = 'base_link'

    point = JointTrajectoryPoint()
    point.positions = [0.0, math.pi / 4]
    point.time_from_start = Duration(sec=2, nanosec=0)
    traj.points.append(point)

    assert traj.joint_names == ['joint1_head', 'joint2_rotor']
    assert len(traj.points) == 1
    assert traj.points[0].positions[1] == pytest.approx(math.pi / 4)
