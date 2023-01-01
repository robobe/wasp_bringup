# https://docs.ros.org/en/foxy/Tutorials/Intermediate/Launch/Using-Event-Handlers.html

from ament_index_python.packages import get_package_share_directory
import os
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, EmitEvent, ExecuteProcess,
                            LogInfo, RegisterEventHandler, TimerAction)
from launch.conditions import IfCondition
from launch.event_handlers import (OnExecutionComplete, OnProcessExit,
                                OnProcessIO, OnProcessStart, OnShutdown)
from launch.events import Shutdown
from launch.substitutions import (EnvironmentVariable, FindExecutable,
                                LaunchConfiguration, LocalSubstitution,
                                PythonExpression)


PACKAGE = "wasp_bringup"

def generate_launch_description():
    ld = LaunchDescription()

    pkg = get_package_share_directory(PACKAGE)
    sitl_executable = os.path.join(pkg, "bin", "arducopter")
    copter_param = os.path.join(pkg, "config", "copter.parm")
    gazebo_param = os.path.join(pkg, "config", "gazebo-iris.parm")
    chmod_sitl = ExecuteProcess(
        cmd=[[
            "chmod +x ",
            sitl_executable
        ]],
        shell=True
    )

    spawn_sitl = ExecuteProcess(
        cmd=[[
            sitl_executable,
            ' -S ',
            "--model gazebo-iris ",
            f'--defaults {copter_param},{gazebo_param} ',
            "-I0"
        ]],
        shell=True
    )

    spawn_mavproxy = ExecuteProcess(
        cmd=[[
            "mavproxy.py ",
            "--out 127.0.0.1:14550 ",
            "--out 127.0.0.1:14551 ", 
            "--master tcp:127.0.0.1:5760 "
        ]],
        shell=True
    )

    on_sitl_start = RegisterEventHandler(
            OnProcessStart(
                target_action=spawn_sitl,
                on_start=[
                    LogInfo(msg='SITL started, spawning mavproxy'),
                    spawn_mavproxy
                ]
            )
        )

    on_chmod = RegisterEventHandler(
            OnProcessStart(
                target_action=chmod_sitl,
                on_start=[
                    LogInfo(msg='chmod and run'),
                    spawn_sitl
                ]
            )
        )

    ld.add_action(chmod_sitl)
    ld.add_action(on_chmod)
    ld.add_action(spawn_mavproxy)
    # ld.add_action(on_sitl_start)
    
    return ld