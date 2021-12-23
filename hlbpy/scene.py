import bpy
from .base import HighLevelBase


class Scene(HighLevelBase):
    def __init__(self, name=None, activate=True, bpy_object=None):
        if bpy_object is None:
            self.bpy_object = bpy.data.scenes.new(name)
        else:
            self.bpy_object = bpy_object
        if activate:
            bpy.context.window.scene = self.bpy_object

    def link(self, collection):
        self.bpy_object.collection.children.link(collection.bpy_object)
        return collection

    @classmethod
    def from_context(cls):
        return cls(bpy_object=bpy.context.scene)



