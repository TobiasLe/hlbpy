import numpy as np

from .scene import Scene
from .base import HighLevelBase

all_hlbpy_objects_scene = Scene("all_hlbpy_objects", activate=False)


class HighLevelObject(HighLevelBase):
    def __init__(self):
        if self.bpy_object is not None:
            all_hlbpy_objects_scene.bpy_object.collection.objects.link(self.bpy_object)
            for child in self.bpy_object.children:
                all_hlbpy_objects_scene.collection.objects.link(child)
            self.update()

    @property
    def center(self):
        return np.mean(self.bpy_object.bound_box, axis=0)

    def get_bound(self, direction):
        center = self.center
        result = np.zeros(3)
        for i, d in enumerate(direction):
            if d == 0:
                result[i] = center[i]
            elif d > 0:
                result[i] = self.bpy_object.bound_box[6][i]
            else:
                result[i] = self.bpy_object.bound_box[0][i]
        return result
