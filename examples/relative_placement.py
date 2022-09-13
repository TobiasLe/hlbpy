import hlbpy
from hlbpy.directions import *
from math import pi

hlbpy.run_in_blender()

scene = hlbpy.Scene.from_context()

spheres = scene.link(hlbpy.Collection("Spheres"))
labels = scene.link(hlbpy.Collection("Labels"))

main_sphere = spheres.link(hlbpy.mesh.UVSphere(radius=5))

sphere_right = spheres.link(hlbpy.mesh.UVSphere(radius=1))
sphere_right.location = main_sphere.right

label_right = labels.link(hlbpy.special.Tex("Right"))
label_right.align_children(LEFT)
label_right.rotation_euler = (pi/2, 0, 0)
label_right.location = sphere_right.right + 0.1 * RIGHT

sphere_top = spheres.link(hlbpy.mesh.UVSphere(radius=1.5))
sphere_top.location = main_sphere.top

label_top = labels.link(hlbpy.special.Tex("Top"))
label_top.align_children(OUT)
label_top.rotation_euler = (pi/2, 0, 0)

label_top.location = sphere_top.top + 0.1 * UP
