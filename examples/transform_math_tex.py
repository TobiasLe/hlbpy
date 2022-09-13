import hlbpy

hlbpy.run_in_blender()

scene = hlbpy.Scene("TestScene")
collection = scene.link(hlbpy.Collection("ExampleCollection"))

tex1 = collection.link(hlbpy.special.MathTex(r"\frac{1}{T} = ", "{dS", r" \over", " dE}"))
tex2 = collection.link(hlbpy.special.MathTex(r"\frac{1}{T} = ", "{\Delta S", r" \over", " \Delta E}"))

tex1.transform(tex2, start=0, n_frames=30)

tex3 = collection.link(
        hlbpy.special.MathTex(r"\frac{1}{T} = ", r"{S_{E+\Delta E} - S_E", r" \over", " \Delta E}"))
tex2.transform(tex3, start=50, n_frames=30)

hlbpy.view.set_view([0, 0, 0], orthographic=True)
