import os
from launch import LaunchDescription
from launch.actions import RegisterEventHandler, LogInfo, ExecuteProcess
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # パッケージのパス
    pkg_share = FindPackageShare('launch_opaque').find('launch_opaque')
    pre_process_path = os.path.join(pkg_share, 'launch', 'pre-process.launch.py')
    simulation_path = os.path.join(pkg_share, 'launch', 'simulation.launch.py')
    post_process_path = os.path.join(pkg_share, 'launch', 'post-process.launch.py')

    # 各launch fileをExecuteProcessで起動
    pre_process_cmd = ['ros2', 'launch', pre_process_path]
    simulation_cmd = ['ros2', 'launch', simulation_path]
    post_process_cmd = ['ros2', 'launch', post_process_path]

    pre_process = ExecuteProcess(
        cmd=pre_process_cmd,
        output='screen',
        name='pre_process'
    )

    simulation = ExecuteProcess(
        cmd=simulation_cmd,
        output='screen',
        name='simulation'
    )

    post_process = ExecuteProcess(
        cmd=post_process_cmd,
        output='screen',
        name='post_process'
    )

    # pre-processの終了を検知してsimulationを開始
    start_simulation = RegisterEventHandler(
        OnProcessExit(
            target_action=pre_process,
            on_exit=[
                LogInfo(msg="Pre-process完了。Simulationを開始します..."),
                simulation
            ]
        )
    )

    # simulationの終了を検知してpost-processを開始
    start_post_process = RegisterEventHandler(
        OnProcessExit(
            target_action=simulation,
            on_exit=[
                LogInfo(msg="Simulation完了。Post-processを開始します..."),
                post_process
            ]
        )
    )

    return LaunchDescription([
        pre_process,
        start_simulation,
        start_post_process,
    ])
