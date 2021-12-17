import bpy
from .base_object import HighLevelObject


class Text(HighLevelObject):
    def __init__(self, content, name):
        curve = bpy.data.curves.new(type="FONT", name=name)
        self.bpy_object = bpy.data.objects.new(name, curve)
        self.bpy_object.data.body = content
        super().__init__()



