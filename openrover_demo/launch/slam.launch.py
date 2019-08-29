"""
Converts LIDAR data to a map and determines where the rover is with respect to walls.
"""
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node


def generate_launch_description():
    slam_config = Path(get_package_share_directory('openrover_demo'), 'config', 'slam_karto.yaml')
    assert slam_config.is_file()

    return LaunchDescription([
        SetEnvironmentVariable('RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED', '1'),
        Node(
            package='slam_karto', node_executable='slam_karto', output='screen',
            parameters=[slam_config]),
        # Node(
        #     package='cartographer_ros', node_executable='cartographer_node', output='screen',
        #     arguments=[
        #         '-configuration_directory', get_package_share_directory('openrover_demo') + '/config',
        #         '-configuration_basename', 'cartographer.lua'
        #     ],
        #     remappings=[
        #         ('imu', 'imu/data')
        #     ],
        # ),
        # Node(
        #     package='cartographer_ros',
        #     node_executable='occupancy_grid_node',
        #     output='screen',
        #     arguments=['-resolution', '0.02', '-publish_period_sec', '1.0']
        # ),
    ])
