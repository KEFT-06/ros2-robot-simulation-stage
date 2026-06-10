from setuptools import setup
from glob import glob
import os

package_name = 'mon_robot_control'

setup(
    name=package_name,
    version='0.0.1',
    packages=[],
    py_modules=[],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Copy scripts directory
        (os.path.join('share', package_name, 'scripts'), glob('scripts/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='ATAWI Stage',
    author_email='stage@atawi.fr',
    maintainer='ATAWI Stage',
    maintainer_email='stage@atawi.fr',
    url='https://github.com/atawi/ros2-robot-simulation-stage',
    description='Control and kinematics validation for ATAWI-3A3 robot',
    long_description='Scripts for trajectory sending and kinematic validation of the ATAWI-3A3 robot in ROS 2',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'send_trajectory=mon_robot_control.scripts.send_trajectory:main',
            'validate_kinematics=mon_robot_control.scripts.validate_kinematics:main',
        ],
    },
)
