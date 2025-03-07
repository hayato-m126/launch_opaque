import os
from launch import LaunchDescription
from launch.actions import RegisterEventHandler, LogInfo, ExecuteProcess
from launch.events.process import ProcessIO
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from launch.event_handlers import OnProcessIO

# 特定の出力を検出して次のアクションを実行するイベントハンドラ
def on_matching_output(matcher: str, result):
    def on_output(event: ProcessIO):
        for line in event.text.decode().splitlines():
            if matcher in line:
                return result
    return on_output

def generate_launch_description():
    # launchファイルのパス
    pkg_share = FindPackageShare('launch_opaque').find('launch_opaque')
    pre_process_path = os.path.join(pkg_share, 'launch', 'pre-process.launch.py')
    simulation_path = os.path.join(pkg_share, 'launch', 'simulation.launch.py')
    post_process_path = os.path.join(pkg_share, 'launch', 'post-process.launch.py')

    # pre-processを実行
    pre_process = ExecuteProcess(
        cmd=['ros2', 'launch', pre_process_path],
        output='screen',
        name='pre_process'
    )

    # simulationを実行
    simulation = ExecuteProcess(
        cmd=['ros2', 'launch', simulation_path],
        output='screen',
        name='simulation'
    )

    # post-processを実行
    post_process = ExecuteProcess(
        cmd=['ros2', 'launch', post_process_path],
        output='screen',
        name='post_process'
    )

    # pre-processの完了を検知してsimulationを開始
    start_simulation = RegisterEventHandler(
        OnProcessIO(
            target_action=pre_process,
            on_stdout=on_matching_output(
                "Pre-process completed", # 完了を示すマーカー文字列
                [
                    LogInfo(msg="Pre-process完了。Simulationを開始します..."),
                    simulation
                ]
            )
        )
    )

    # simulationの完了を検知してpost-processを開始
    start_post_process = RegisterEventHandler(
        OnProcessIO(
            target_action=simulation,
            on_stdout=on_matching_output(
                "Simulation completed", # 完了を示すマーカー文字列
                [
                    LogInfo(msg="Simulation完了。Post-processを開始します..."),
                    post_process
                ]
            )
        )
    )

    return LaunchDescription([
        pre_process,
        start_simulation,
        start_post_process
    ])
