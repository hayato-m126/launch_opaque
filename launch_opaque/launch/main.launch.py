import os
from launch import LaunchDescription
from launch.actions import RegisterEventHandler, LogInfo
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # launchファイルのパス
    pkg_share = get_package_share_directory('launch_opaque')
    pre_process_path = os.path.join(pkg_share, 'launch', 'pre-process.launch.py')
    simulation_path = os.path.join(pkg_share, 'launch', 'simulation.launch.py')
    post_process_path = os.path.join(pkg_share, 'launch', 'post-process.launch.py')

    # 各プロセスのlaunchファイルをインクルード
    pre_process = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([pre_process_path])
    )

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([simulation_path])
    )

    post_process = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([post_process_path])
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

    # # simulationの終了を検知してpost-processを開始
    # start_post_process = RegisterEventHandler(
    #     OnProcessExit(
    #         target_action=simulation,
    #         on_exit=[
    #             LogInfo(msg="Simulation完了。Post-processを開始します..."),
    #             post_process
    #         ]
    #     )
    #)

    return LaunchDescription([
        pre_process,
        simulation,
        post_process,
        #start_simulation,
        #start_post_process
    ])
