import bpy
import hlbpy
import pydevd_pycharm

try:
    pydevd_pycharm.settrace('localhost', port=1090, stdoutToServer=True, stderrToServer=True,
                            suspend=False)
except ConnectionRefusedError:
    print("no connection to Debug server")

scene = hlbpy.Scene.from_context()
collection = scene.link(hlbpy.Collection("TestCollection"))

tex1 = collection.link(hlbpy.special.MathTex(r"\frac{1}{T} = {dS \over  ", r"dE}"))
# tex2 = collection.link(hlbpy.special.Tex(r"o"))
# tex3 = collection.link(hlbpy.special.Tex(r"b"))


# curve_1 = tex1[0]
# curve_2 = tex2[0]
# curve_1.transform(curve_2, 0, 30)

hlbpy.view.set_view([0, 0, 0], orthographic=True)
