import hlbpy

hlbpy.run_in_blender()

scene = hlbpy.Scene("TestScene")
collection = scene.link(hlbpy.Collection("TestCollection"))

line = collection.link(hlbpy.curve.Line([1, 0, 0], [2, 1, 0]))
print(line.center)
line.location = (1, 1, 0)
print(line.get_own_bound([0, 0, 0], in_global_space=True))
print(line.get_own_bound([0, 0, 0], in_global_space=False))

print(line.center)
line.origin_to(line.center)
print(line.center)
