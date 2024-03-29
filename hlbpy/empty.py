import bpy
from .base_object import HighLevelObject


class Empty(HighLevelObject):
    def __init__(self, name="Empty"):
        bpy_object = bpy.data.objects.new(name, None)
        super().__init__(bpy_object, no_update=True)


