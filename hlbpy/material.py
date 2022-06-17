import bpy
from .base import HighLevelBase
from .misc import srgb_to_linearrgb


class PrincipledBSDF(HighLevelBase):
    def __init__(self, name="PrincipledBSDF", srgb=(200, 200, 200)):
        self.bpy_object = bpy.data.materials.new(name)
        self.bpy_object.use_nodes = True
        self.principled_BSDF_node = self.bpy_object.node_tree.nodes.get("Principled BSDF")

        self.srgb = srgb

    @property
    def srgb(self):
        raise NotImplementedError

    @srgb.setter
    def srgb(self, value):
        self.principled_BSDF_node.inputs["Base Color"].default_value = srgb_to_linearrgb(value) + [255]

    @property
    def alpha(self):
        self.principled_BSDF_node.inputs["Alpha"].default_value

    @alpha.setter
    def alpha(self, value):
        self.principled_BSDF_node.inputs["Alpha"].default_value = value
        if value != 1:
            self.bpy_object.blend_method = "BLEND"

    def alpha_blend(self, start, stop, start_value, stop_value):
        self.bpy_object.blend_method = "BLEND"
        self.set_keyframes('node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value',
                           [start_value, stop_value], [start, stop])

    @property
    def roughness(self):
        self.principled_BSDF_node.inputs["Roughness"].default_value

    @roughness.setter
    def roughness(self, value):
        self.principled_BSDF_node.inputs["Roughness"].default_value = value


