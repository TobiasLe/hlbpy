import numpy as np
import bpy
from .scene import Scene
from .base import HighLevelBase
from .directions import *
from mathutils import Vector
from .misc import apply_material_to_obj, get_bpy_obj

all_hlbpy_objects_scene = Scene("all_hlbpy_objects", activate=False)


class HighLevelObject(HighLevelBase):
    def __init__(self, bpy_object):
        self.bpy_object = bpy_object
        self.children = []
        all_hlbpy_objects_scene.bpy_object.collection.objects.link(self.bpy_object)
        self.update()

    def __getitem__(self, key):
        return self.children[key]

    def __setitem__(self, key, value):
        self.children[key] = value

    @property
    def center(self):
        return (np.array(self.bpy_object.bound_box[6]) + np.array(self.bpy_object.bound_box[0])) * \
               self.bpy_object.scale / 2

    @property
    def left(self):
        return self.get_bound(LEFT)

    @property
    def right(self):
        return self.get_bound(RIGHT)

    @property
    def top(self):
        return self.get_bound(UP)

    @property
    def bottom(self):
        return self.get_bound(DOWN)

    @property
    def front(self):
        return self.get_bound(OUT)

    @property
    def back(self):
        return self.get_bound(IN)

    @property
    def location(self):
        return self.bpy_object.location

    @location.setter
    def location(self, value):
        self.bpy_object.location = value
        self.update()

    @property
    def rotation_euler(self):
        return self.bpy_object.rotation_euler

    @rotation_euler.setter
    def rotation_euler(self, value):
        self.bpy_object.rotation_euler = value
        self.update()

    @property
    def scale(self):
        return self.bpy_object.scale

    @scale.setter
    def scale(self, value):
        try:
            iter(value)
        except TypeError:
            self.bpy_object.scale = [value] * 3
        else:
            self.bpy_object.scale = value
        self.update()

    @property
    def parent(self):
        return self.bpy_object.parent

    @parent.setter
    def parent(self, parent):
        self.bpy_object.parent = parent.bpy_object
        parent.children.append(self)

    def apply_material(self, material, recursively=False):
        apply_material_to_obj(self, material, recursively)

    def get_bound(self, direction):
        return self.get_own_bound(direction)

    def get_own_bound(self, direction, in_global_space=False):
        center = self.center
        result = Vector((0, 0, 0))
        for i, d in enumerate(direction):
            if d == 0:
                result[i] = center[i]
            elif d > 0:
                result[i] = self.bpy_object.bound_box[6][i]
            else:
                result[i] = self.bpy_object.bound_box[0][i]
        if in_global_space:
            return np.array(self.bpy_object.matrix_global @ result)
        else:
            return np.array(self.bpy_object.matrix_local @ result)

    def get_children_bound(self, direction, in_global_space=False):
        child_box_corners = np.array([child.matrix_local @ Vector(corner) for child in self.bpy_object.children
                                      for corner in child.bound_box])
        max_point = np.max(child_box_corners, axis=0)
        min_point = np.min(child_box_corners, axis=0)
        center = (min_point + max_point) / 2
        result = Vector((0, 0, 0))
        for i, d in enumerate(direction):
            if d == 0:
                result[i] = center[i]
            elif d > 0:
                result[i] = max_point[i]
            else:
                result[i] = min_point[i]
        if in_global_space:
            return np.array(self.bpy_object.matrix_global @ result)
        else:
            return np.array(self.bpy_object.matrix_local @ result)

    def get_children_center(self):
        return self.get_children_bound([0, 0, 0])

    def move_children(self, vector):
        for child in self.bpy_object.children:
            child.location += Vector(vector)
        return self

    def align_children(self, direction):
        self.move_children(-self.get_children_bound(direction))
        return self

    def to_local(self, vector):
        """
        Returns corresponding vector in local space i.e. the internal space of the parent
        If no parent is present, local space is equal to global space.
        Args:
            vector:

        Returns:

        """
        return np.array(self.bpy_object.matrix_local @ Vector(vector))

    def to_global(self, vector):
        """
        Returns corresponding vector in global space.
        Args:
            vector:

        Returns:

        """
        np.array(self.bpy_object.matrix_global @ Vector(vector))
