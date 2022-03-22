import hlbpy

hlbpy.run_in_blender()

scene = hlbpy.Scene("TestScene")
collection = scene.link(hlbpy.Collection("TestCollection"))

line = collection.link(hlbpy.curve.Line([1, 0, 0], [2, 1, 0]))
line.location = (1, 1, 0)

line.origin_to(line.center)
