import bpy
import numpy as np
from math import pi

from .base_object import HighLevelObject


class Text(HighLevelObject):
    def __init__(self, content, name):
        curve = bpy.data.curves.new(type="FONT", name=name)
        bpy_object = bpy.data.objects.new(name, curve)
        bpy_object.data.body = content
        super().__init__(bpy_object)


class Curve(HighLevelObject):
    def __init__(self, vertices, spline_type="POLY", name="Curve"):
        """
        :param vertices: array of shape: (n_vertices, 3)
        :param spline_type: chose any from: "POLY", "BEZIER", or "NURBS"
        """

        curve = bpy.data.curves.new(name, type='CURVE')
        bpy_object = bpy.data.objects.new(name, curve)
        spline = curve.splines.new(type=spline_type)
        if spline_type == "BEZIER":
            raise NotImplementedError
        else:
            type_numbers = np.zeros((len(vertices), 1))
            if spline_type == "NURBS":
                type_numbers += 1
            vertices_with_type = np.concatenate((vertices, type_numbers), axis=1)
            spline.points.add(len(vertices) - 1)  # spline has one point by default
            spline.points.foreach_set('co', vertices_with_type.flatten())
            spline.use_endpoint_u = True

        super().__init__(bpy_object)

    def add_flat_bevel(self):
        pass


class Polygon(Curve):
    def __init__(self, n_corners, radius=1, spline_type="POLY", name="Curve"):
        """
        Create a polygon shaped curve.
        Args:
            n_corners: Number of Corners
            radius:
        """
        angles = np.linspace(0, 2*pi, n_corners+1)[:-1]
        x_values = np.sin(angles) * radius
        y_values = np.cos(angles) * radius
        z_values = np.zeros(n_corners)
        vertices = np.column_stack((x_values, y_values, z_values))
        super().__init__(vertices, spline_type, name)
        self.bpy_object.data.splines[0].use_cyclic_u = True
