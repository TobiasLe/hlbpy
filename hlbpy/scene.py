import bpy
from .base import HighLevelBase


class Scene(HighLevelBase):
    def __init__(self, name=None, activate=True, bpy_object=None, reuse=True):
        if bpy_object is None:
            already_present = name in [s.name for s in bpy.data.scenes]
            if already_present and reuse:
                self.bpy_object = bpy.data.scenes[name]
            else:
                self.bpy_object = bpy.data.scenes.new(name)
        else:
            self.bpy_object = bpy_object
        if activate:
            bpy.context.window.scene = self.bpy_object

    def link(self, collection):
        try:
            self.bpy_object.collection.children[collection.bpy_object.name]
        except KeyError:
            self.bpy_object.collection.children.link(collection.bpy_object)
        return collection

    @classmethod
    def from_context(cls):
        return cls(bpy_object=bpy.context.scene)

    @property
    def frame_end(self):
        return self.bpy_object.frame_end

    @frame_end.setter
    def frame_end(self, value):
        self.bpy_object.frame_end = value

    @property
    def frame_start(self):
        return self.bpy_object.frame_start

    @frame_start.setter
    def frame_start(self, value):
        self.bpy_object.frame_start = value



