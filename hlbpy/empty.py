import bpy
from .base_object import HighLevelObject


class Empty(HighLevelObject):
    def __init__(self, name):
        self.bpy_object = bpy.data.objects.new(name, None)
        super().__init__()


