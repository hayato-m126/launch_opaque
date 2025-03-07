# Copyright (c) 2025 TIER IV.inc
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

import time
from launch import LaunchContext
from launch import LaunchDescription
from launch.actions import LogInfo
from launch.actions import OpaqueFunction


def echo_process(context: LaunchContext) -> list:  # noqa
    # 5 seconds sleep
    time.sleep(1)
    return [LogInfo(msg="Pre-process completed")]


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription(
        [
            OpaqueFunction(function=echo_process),
        ],
    )
