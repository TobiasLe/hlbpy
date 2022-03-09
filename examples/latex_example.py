import hlbpy
hlbpy.run_in_blender()
from math import pi

try:
    pydevd_pycharm.settrace('localhost', port=1090, stdoutToServer=True, stderrToServer=True,
                            suspend=False)
except ConnectionRefusedError:
    print("no connection to Debug server")

scene = hlbpy.Scene("TestScene")
collection = scene.link(hlbpy.Collection("TestCollection"))

# tex = collection.add(hlbpy.special.Tex(r"Hello Tex World: $\mathrm{3x^2 \Omega \in R \subset Q}$", "TestTex"))
# tex.move_children(-tex.get_children_bound([0, -1, 0]))

# polygon = collection.add(hlbpy.curve.Polygon(6))
#
# polygon.bevel_object = hlbpy.curve.Rectangle(width=0.1, height=0.01)

cube = collection.link(hlbpy.mesh.Cube())

a = cube.get_bound([-1, 0, 0])
cube.scale = 3
b = cube.get_bound([-1, 0, 0])
cube.rotation_euler = [0, 0, pi/4]
c = cube.get_bound([-1, 0, 0])
empty = collection.add(hlbpy.Empty("test"))
empty.location = cube.get_bound([-1, 0, 0])

# arrow = collection.add(hlbpy.special.Arrow([[0, 0, 0],
#                                             [0, 1, 0],
#                                             [2, 2, 0]], 0.05, 0.2, 0.2, 0.02))

pass

hlbpy.view.set_view([0, 0, 0], orthographic=True)
