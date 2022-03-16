import hlbpy

hlbpy.run_in_blender()

scene = hlbpy.Scene.from_context()
collection = scene.link(hlbpy.Collection("TestCollection"))


cube = collection.link(hlbpy.mesh.Cube())
cube.transitions.scale_up_elastic(5)

