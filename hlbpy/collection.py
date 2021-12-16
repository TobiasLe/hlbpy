import bpy
from .base import HighLevelBase


class Collection(HighLevelBase):
    def __init__(self, name):
        self.bpy_object = bpy.data.collections.new(name)

    def add(self, object):
        self.bpy_object.objects.link(object.bpy_object)
        for child in object.bpy_object.children:
            self.bpy_object.objects.link(child)

        return object


