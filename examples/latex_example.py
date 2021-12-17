import bpy
import hlbpy
import pydevd_pycharm

try:
    pydevd_pycharm.settrace('localhost', port=1090, stdoutToServer=True, stderrToServer=True,
                            suspend=False)
except ConnectionRefusedError:
    print("no connection to Debug server")

scene = hlbpy.Scene("TestScene")
collection = scene.add(hlbpy.Collection("TestCollection"))

# tex = collection.add(hlbpy.curve.Tex(r"Hello Tex World: $3x^2 \Omega \in R \subset Q$", "TestTex"))

cube = collection.add(hlbpy.mesh.Cube(1))

cube.get_bound([1, 0, 0])

pass
