# based on navigation2/nav2_bringup/launch/nav2_bringup_launch.py
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

from pathlib import Path

import launch.actions
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription


def generate_launch_description():
    config = Path(get_package_share_directory('openrover_demo'), 'config')
    nav2_yaml = config / 'nav2.yaml'
    assert nav2_yaml.is_file()
    map_yaml_filename = config / 'map.yaml'
    assert map_yaml_filename.is_file()

    return LaunchDescription([
        launch.actions.SetEnvironmentVariable('RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED', '1'),
        launch_ros.actions.Node(
            node_name='lifecycle_manager',
            package='nav2_lifecycle_manager',
            node_executable='lifecycle_manager',
            output='screen',
            parameters=[
                nav2_yaml,
                {
                    'autostart': True,
                    'node_names': ['map_server', 'amcl', ],
                }
            ]
        ),
        launch_ros.actions.LifecycleNode(
            node_name='map_server',
            package='nav2_map_server',
            node_executable='map_server',
            output='screen',
            parameters=[nav2_yaml, {'yaml_filename': str(map_yaml_filename)}]
        ),
        launch_ros.actions.Node(
            node_name='amcl',
            package='nav2_amcl',
            node_executable='amcl',
            output='screen',
            parameters=[nav2_yaml],
          #  arguments=['__log_level:=debug']
        ),
    ])
