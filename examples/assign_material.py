import hlbpy

hlbpy.run_in_blender()

scene = hlbpy.Scene.from_context()
collection = scene.link(hlbpy.Collection("TestCollection"))

cube = collection.link(hlbpy.mesh.Cube())

red = hlbpy.material.PrincipledBSDF(name="Red", srgb=(200, 0, 0))
red.alpha_blend(20, 50, 1, 0)

cube.material = red
