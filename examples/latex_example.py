import hlbpy

hlbpy.run_in_blender()

scene = hlbpy.Scene("TestScene")
collection = scene.link(hlbpy.Collection("TestCollection"))

tex = collection.link(hlbpy.special.Tex(r"Hello Tex World: $\mathrm{3x^2 \Omega \in R \subset Q}$", "TestTex"))

hlbpy.view.set_view([0, 0, 0], orthographic=True)
