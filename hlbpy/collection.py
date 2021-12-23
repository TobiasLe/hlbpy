import bpy
from .base import HighLevelBase


class Collection(HighLevelBase):
    def __init__(self, name="Collection", bpy_object=None, reuse=True, clear=False):
        if bpy_object is None:
            already_present = name in [c.name for c in bpy.data.collections]
            if reuse and already_present:
                self.bpy_object = bpy.data.collections[name]
            else:
                self.bpy_object = bpy.data.collections.new(name)

            if already_present and clear:
                while self.bpy_object.objects:
                    bpy.data.objects.remove(self.bpy_object.objects[0])

        else:
            self.bpy_object = bpy_object

    def link(self, object):
        # Todo: link collections
        try:
            bpy_object = object.bpy_object
        except AttributeError:
            bpy_object = object
        self.bpy_object.objects.link(bpy_object)
        for child in bpy_object.children:
            self.link(child)
        return object
