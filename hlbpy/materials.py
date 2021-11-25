import bpy
from .misc import srgb_to_linearrgb


def principled_bsdf(name="principled_bsdf", srgb=(200, 200, 200)):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    principled_shader = material.node_tree.nodes.get("Principled BSDF")

    principled_shader.inputs[0].default_value = srgb_to_linearrgb(srgb) + [1]
    return material

