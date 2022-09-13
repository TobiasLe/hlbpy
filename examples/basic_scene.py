import hlbpy
from math import pi
import numpy as np

hlbpy.run_in_blender()

scene = hlbpy.Scene.from_context()

cubes = scene.link(hlbpy.Collection("Cubes"))

big_cube = cubes.link(hlbpy.mesh.Cube(edge_length=2, name="BigCube"))
small_cube = cubes.link(hlbpy.mesh.Cube(edge_length=1, name="SmallCube"))

small_cube.location = (0, 0, 2.5)

small_cube.parent = big_cube

big_cube.set_keyframes("location", np.sin(np.linspace(0, 2*pi, 60)), index=2)
small_cube.set_keyframes("rotation_euler", [[0, 0, 0], [0, 0, 2*pi]], frame_numbers=[0, 60])

scene.frame_end = 60
