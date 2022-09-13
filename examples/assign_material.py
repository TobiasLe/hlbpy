import hlbpy

hlbpy.run_in_blender()

scene = hlbpy.Scene.from_context()
environment = scene.link(hlbpy.Collection("Environment"))
marbles = scene.link(hlbpy.Collection("Marbles"))

ground = environment.link(hlbpy.mesh.Cuboid((6, 3, 0.2)))
ground.location = (2, 0, -0.1)

for i in range(5):
    marble = marbles.link(hlbpy.mesh.UVSphere(radius=0.4))
    marble.shade_smooth()
    marble.location = (i, 0, 0.4)

    red_material = hlbpy.material.PrincipledBSDF(name="Red", srgb=(200, 0, 0))
    red_material.roughness = 1 - i / 4
    marble.material = red_material

