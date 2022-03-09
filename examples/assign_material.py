import hlbpy
hlbpy.run_in_blender()

scene = hlbpy.Scene.from_context()
collection = scene.link(hlbpy.Collection("TestCollection"))

cube = collection.link(hlbpy.mesh.Cube())

red = hlbpy.material.PrincipledBSDF(srgb=(200, 0, 0))

cube.material = red

