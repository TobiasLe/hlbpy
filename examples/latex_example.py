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
obj = collection.add(hlbpy.Empty("TestObject"))

# text = collection.add(hlbpy.curve.Text("Hello World", "TestText"))
tex = collection.add(hlbpy.curve.Tex("Hello Tex World", "TestTex"))

# hlbpy.tex.tex_to_svg(r"$\Omega_{\mathrm{E}+1}=$", r"C:\Users\Tobias\coding\hlbpy\data\test.svg")

print(obj.location)
