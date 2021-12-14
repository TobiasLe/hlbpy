import bpy
from .base import HighLevelBase


class Scene(HighLevelBase):
    def __init__(self, name, activate=True):
        self.bpy_object = bpy.data.scenes.new(name)
        if activate:
            bpy.context.window.scene = self.bpy_object

    def add(self, collection):
        self.bpy_object.collection.children.link(collection.bpy_object)
        return collection



