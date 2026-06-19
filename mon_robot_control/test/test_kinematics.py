import math

import pytest

from mon_robot_control.robot_kinematics import RobotKinematics


def test_fk_zero():
    pos, rot = RobotKinematics.forward_kinematics([0.0, 0.0])
    assert pos == [0.0, 0.0, 0.010]
    assert rot[0][0] == pytest.approx(1.0)
    assert rot[1][1] == pytest.approx(1.0)


def test_fk_head_90():
    yaw = RobotKinematics.forward_kinematics_yaw([math.pi / 2, 0.0])
    assert yaw == pytest.approx(math.pi / 2, abs=1e-9)


def test_fk_rotor_90():
    yaw = RobotKinematics.forward_kinematics_yaw([0.0, math.pi / 2])
    assert yaw == pytest.approx(math.pi / 2, abs=1e-9)


def test_ik_roundtrip():
    target = math.radians(120.0)
    q, ok = RobotKinematics.inverse_kinematics_orientation(target)
    assert ok
    yaw = RobotKinematics.forward_kinematics_yaw(q)
    assert RobotKinematics.wrap_pi(target - yaw) == pytest.approx(0.0, abs=1e-9)


def test_workspace_covers_full_circle():
    yaws = RobotKinematics.workspace_yaw_samples(n=16)
    assert len(yaws) > 1
    assert min(yaws) <= -math.pi + 0.01
    assert max(yaws) >= math.pi - 0.01
