import bpy
from .base import HighLevelBase


class Empty(HighLevelBase):
    def __init__(self, name):
        self.bpy_object = bpy.data.objects.new(name, None)


