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
        self.principled_BSDF_node.inputs[0].default_value = srgb_to_linearrgb(value) + [255]

    @property
    def alpha(self):
        self.principled_BSDF_node.inputs[21].default_value

    @alpha.setter
    def alpha(self, value):
        self.principled_BSDF_node.inputs[21].default_value = value
        if value != 1:
            self.bpy_object.blend_method = "BLEND"
