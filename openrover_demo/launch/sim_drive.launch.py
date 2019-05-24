import os
from pathlib import Path

import launch
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    urdf = os.path.join(get_package_share_directory('openrover_demo'), 'urdf', 'rover.urdf')
    assert Path(urdf).is_file()

    presence_yaml = Path(get_package_share_directory('openrover_demo'), 'config', 'presence.yaml')
    assert presence_yaml.is_file()

    gzserver_exe = launch.actions.ExecuteProcess(
        cmd=['gzserver', '--verbose',
             '-s', 'libgazebo_ros_factory.so',
             '-s', 'libgazebo_ros_init.so',
             'worlds/willowgarage.world',
             '__params:=/home/cottsay/demo_ws/use_sim_time.yaml'],
        output='screen'
    )
    gzclient_exe = launch.actions.ExecuteProcess(
        cmd=['gzclient'],
        output='screen'
    )

    return launch.LaunchDescription([
        #gzclient_exe,
        gzserver_exe,
        Node(
            package='robot_localization',
            node_executable='se_node',
            output='screen',
            parameters=[presence_yaml],
            remappings=[
                ('odometry/filtered', 'odom')
            ]
        ),
        Node(
            package='openrover_demo', node_executable='urdf_spawner.py', output='screen',
            arguments=[urdf]),
        #Node(
        #    package='robot_state_publisher', node_executable='robot_state_publisher', output='screen',
        #    arguments=[urdf], node_name='openrover_robot_state_publisher',
        #    parameters=[{'publish_frequency': 50.0, 'use_sim_time': True}]),
    ])
