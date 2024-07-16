#!/usr/bin/env python3
#
# Copyright 2019 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Joep Tool

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Directories
    launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # Launch configurations
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='-2.0')
    y_pose = LaunchConfiguration('y_pose', default='-0.5')

    # AprilTag configurations
    apriltag_x_pose = LaunchConfiguration('apriltag_x_pose', default='1.0')
    apriltag_y_pose = LaunchConfiguration('apriltag_y_pose', default='0.50')
    apriltag_z_pose = LaunchConfiguration('apriltag_z_pose', default='0.30')
    apriltag_roll = LaunchConfiguration('apriltag_roll', default='1.5707')
    apriltag_pitch = LaunchConfiguration('apriltag_pitch', default='0.0')
    apriltag_yaw = LaunchConfiguration('apriltag_yaw', default='0.0')

    # Paths
    world = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'worlds', 'turtlebot3_world.world')
    apriltag_model_path = os.path.join(os.getenv('HOME'), '.gazebo', 'models', 'Apriltag36_11_00000', 'model.sdf')

    print("AprilTag model path:", apriltag_model_path)  # Debugging

    # Gazebo server and client
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')),
        launch_arguments={'world': world}.items()
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py'))
    )

    # Robot state publisher
    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_file_dir, 'robot_state_publisher.launch.py')),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    # Spawn TurtleBot3
    spawn_turtlebot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_file_dir, 'spawn_turtlebot3.launch.py')),
        launch_arguments={'x_pose': x_pose, 'y_pose': y_pose}.items()
    )

    # Spawn AprilTag
    spawn_apriltag_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_apriltag',
        output='screen',
        arguments=[
            '-file', apriltag_model_path,
            '-entity', 'Apriltag36_11_00000',
            '-x', apriltag_x_pose,
            '-y', apriltag_y_pose,
            '-z', apriltag_z_pose,
            '-R', apriltag_roll,
            '-P', apriltag_pitch,
            '-Y', apriltag_yaw
        ]
    )

    # Launch description
    ld = LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true', description='Use simulation time'),
        DeclareLaunchArgument('x_pose', default_value='-2.0', description='Initial X position of TurtleBot3'),
        DeclareLaunchArgument('y_pose', default_value='-0.5', description='Initial Y position of TurtleBot3'),
        DeclareLaunchArgument('apriltag_x_pose', default_value='0.0', description='Initial X position of AprilTag'),
        DeclareLaunchArgument('apriltag_y_pose', default_value='-0.50', description='Initial Y position of AprilTag'),
        DeclareLaunchArgument('apriltag_z_pose', default_value='0.20', description='Initial Z position of AprilTag'),
        DeclareLaunchArgument('apriltag_roll', default_value='0.00', description='Roll of AprilTag'),
        DeclareLaunchArgument('apriltag_pitch', default_value='1.5707', description='Pitch of AprilTag'),
        DeclareLaunchArgument('apriltag_yaw', default_value='0.0', description='Yaw of AprilTag')
    ])

    # Add the commands to the launch description
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_turtlebot_cmd)
    ld.add_action(spawn_apriltag_cmd)

    return ld
