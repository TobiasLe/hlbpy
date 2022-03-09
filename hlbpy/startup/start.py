import os
import inspect
import subprocess


def run_in_blender():
    try:
        import bpy
    except ModuleNotFoundError:
        print("Starting blender...")
        main_file_path = inspect.stack()[1].filename
        subprocess.run(["blender", "--window-geometry", "1920", "0", "1920", "2160", "--python", main_file_path])
        exit()

    try:
        import pydevd_pycharm
        try:
            pydevd_pycharm.settrace('localhost', port=1090, stdoutToServer=True, stderrToServer=True,
                                    suspend=False)
        except ConnectionRefusedError:
            pass
    except ModuleNotFoundError:
        pass

