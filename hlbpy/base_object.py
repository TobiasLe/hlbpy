import numpy as np

from .scene import Scene
from .base import HighLevelBase
from mathutils import Vector

all_hlbpy_objects_scene = Scene("all_hlbpy_objects", activate=False)


class HighLevelObject(HighLevelBase):
    def __init__(self, bpy_object):
        self.bpy_object = bpy_object
        all_hlbpy_objects_scene.bpy_object.collection.objects.link(self.bpy_object)
        for child in self.bpy_object.children:
            all_hlbpy_objects_scene.bpy_object.collection.objects.link(child)
        self.update()

    @property
    def center(self):
        return (np.array(self.bpy_object.bound_box[6]) + np.array(self.bpy_object.bound_box[0])) * \
               self.bpy_object.scale / 2

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
        return result * self.bpy_object.scale

    def get_children_bound(self, direction):
        max_point = np.max([np.array(child.bound_box[6]) * child.scale for child in self.bpy_object.children], axis=0)
        min_point = np.min([np.array(child.bound_box[0]) * child.scale for child in self.bpy_object.children], axis=0)
        center = (min_point + max_point) / 2
        result = np.zeros(3)
        for i, d in enumerate(direction):
            if d == 0:
                result[i] = center[i]
            elif d > 0:
                result[i] = max_point[i]
            else:
                result[i] = min_point[i]
        return result

    def get_children_center(self):
        return self.get_children_bound([0, 0, 0])

    def move_children(self, vector):
        for child in self.bpy_object.children:
            child.location += Vector(vector)
