import hlbpy
hlbpy.run_in_blender()

scene = hlbpy.Scene.from_context()
collection = scene.link(hlbpy.Collection("TestCollection"))

# tex1 = collection.link(hlbpy.special.MathTex(r"\frac{1}{T} = ", "{dS", r" \over dE}"))
# tex2 = collection.link(hlbpy.special.MathTex(r"\frac{1}{T} = ", "{d ln \Omega", r" \over dE}"))



pass
# cube.hide_until(20)
# cube.hide_from(30)

# tex1 = collection.link(hlbpy.special.MathTex(r"a", r"b"))
# tex2 = collection.link(hlbpy.special.MathTex(r"a", r"bb"))

# tex1.transform(tex2, 0, 30)

hlbpy.view.set_view([0, 0, 0], orthographic=True)
