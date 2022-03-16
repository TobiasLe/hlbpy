import hlbpy

hlbpy.run_in_blender()

scene = hlbpy.Scene.from_context()
collection = scene.link(hlbpy.Collection("TestCollection"))

tex1 = collection.link(hlbpy.special.Tex(r"a"))
tex2 = collection.link(hlbpy.special.Tex(r"bb"))

tex1.transform(tex2, 0, 30)

hlbpy.view.set_view([0, 0, 0], orthographic=True)
