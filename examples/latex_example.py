import bpy
import hlbpy
import pydevd_pycharm
import numpy as np

try:
    pydevd_pycharm.settrace('localhost', port=1090, stdoutToServer=True, stderrToServer=True,
                            suspend=False)
except ConnectionRefusedError:
    print("no connection to Debug server")

scene = hlbpy.Scene("TestScene")
collection = scene.add(hlbpy.Collection("TestCollection"))

tex = collection.add(hlbpy.special.Tex(r"Hello Tex World: $\mathrm{3x^2 \Omega \in R \subset Q}$", "TestTex"))
tex.move_children(-tex.get_children_bound([0, -1, 0]))



# cube = collection.add(hlbpy.mesh.Cube())
#
# a = cube.get_bound([-1, 0, 0])
# cube.bpy_object.scale = [5] * 3
# b = cube.get_bound([-1, 0, 0])
pass
