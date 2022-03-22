import hlbpy

hlbpy.run_in_blender()

scene = hlbpy.Scene("TestScene")
collection = scene.link(hlbpy.Collection("TestCollection"))

tex1 = collection.link(hlbpy.special.MathTex("a", "f"))
tex2 = collection.link(hlbpy.special.MathTex("b", ""))

# tex1.transform(tex2, 0, target_indices=[(0, 1)])
tex1.transform(tex2, 0)

hlbpy.view.set_view([0, 0, 0], orthographic=True)
