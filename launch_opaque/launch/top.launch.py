from launch import LaunchContext
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import LogInfo
from launch.actions import OpaqueFunction

def launch_setup(context: LaunchContext) -> list:
    conf = context.launch_configurations
    if conf["condition"] == "true":
        return echo_hello(context)
    return echo_world(context)


def echo_hello(context: LaunchContext) -> list:
    return [LogInfo(msg="hello")]

def echo_world(context: LaunchContext) -> list:
    return [LogInfo(msg="world")]



def generate_launch_description() -> LaunchDescription:
    return LaunchDescription(
        [
            DeclareLaunchArgument("condition", default_value="true"),
            OpaqueFunction(function=launch_setup),
        ],
    )
