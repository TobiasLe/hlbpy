import os
import inspect
import subprocess


def run_in_blender(blend_file_path=None, window_geometry=None):
    try:
        import bpy
    except ModuleNotFoundError:
        print("Starting blender...")
        command = ["blender"]
        if blend_file_path:
            command += [str(blend_file_path)]

        if window_geometry is None:
            command += ["--window-geometry", "1920", "0", "1920", "2160"]
        else:
            raise NotImplementedError

        main_file_path = inspect.stack()[1].filename
        command += ["--python", main_file_path]

        subprocess.run(command)
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

