from .scene import Scene
from .base import HighLevelBase

all_hlbpy_objects_scene = Scene("all_hlbpy_objects", activate=False)


class HighLevelObject(HighLevelBase):
    def __init__(self):
        if self.bpy_object is not None:
            all_hlbpy_objects_scene.collection.objects.link(self.bpy_object)
            for child in self.bpy_object.children:
                all_hlbpy_objects_scene.collection.objects.link(child)
            self.update()
