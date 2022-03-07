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

tex1 = collection.link(hlbpy.special.MathTex(r"\frac{1}{T} = ", "{dS", r" \over dE}"))
tex2 = collection.link(hlbpy.special.MathTex(r"\frac{1}{T} = ", "{d ln \Omega", r" \over dE}"))



# tex1 = collection.link(hlbpy.special.MathTex(r"a", r"b"))
# tex2 = collection.link(hlbpy.special.MathTex(r"a", r"bb"))

tex1.transform(tex2, 0, 30)

hlbpy.view.set_view([0, 0, 0], orthographic=True)
