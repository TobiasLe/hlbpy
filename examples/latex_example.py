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

tex = collection.add(hlbpy.curve.Tex(r"Hello Tex World: $3x^2 \Omega \in R \subset Q$", "TestTex"))

for child in tex.children[:3]:
    print(child.dimensions)

tex.update()

for child in tex.children[:3]:
    print(child.dimensions)
pass

