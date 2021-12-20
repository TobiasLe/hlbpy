import bpy
from .base import HighLevelBase


class Collection(HighLevelBase):
    def __init__(self, name):
        self.bpy_object = bpy.data.collections.new(name)

    def add(self, object):
        try:
            bpy_object = object.bpy_object
        except AttributeError:
            bpy_object = object
        self.bpy_object.objects.link(bpy_object)
        for child in bpy_object.children:
            self.add(child)
        return object


