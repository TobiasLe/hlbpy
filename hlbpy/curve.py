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
    def __init__(self, vertices, spline_type="POLY", name="Curve", bevel_object=None):
        """

        Args:
            vertices: array of shape: (n_vertices, 3)
            spline_type: chose any from: "POLY", "BEZIER", or "NURBS"
            name:
            bevel_object:
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
            spline.use_smooth = False

        super().__init__(bpy_object)
        self._bevel_object = bevel_object

    @property
    def bevel_object(self):
        return self._bevel_object

    @bevel_object.setter
    def bevel_object(self, value):
        self.bpy_object.data.bevel_mode = "OBJECT"
        self.bpy_object.data.bevel_object = value.bpy_object
        self._bevel_object = value

    @property
    def shade_smooth(self):
        return self.bpy_object.data.splines[0].use_smooth

    @shade_smooth.setter
    def shade_smooth(self, value):
        self.bpy_object.data.splines[0].use_smooth = value

    @property
    def fill_mode(self):
        return self.bpy_object.data.fill_mode

    @fill_mode.setter
    def fill_mode(self, value):
        """allowed values: "NONE", "BOTH", "BACK", "FRONT" """
        self.bpy_object.data.fill_mode = value

    @property
    def cyclic(self):
        return self.bpy_object.data.splines[0].use_cyclic_u

    @cyclic.setter
    def cyclic(self, value):
        self.bpy_object.data.splines[0].use_cyclic_u = value


class Polygon(Curve):
    def __init__(self, n_corners, radius=1, spline_type="POLY", name="Polygon"):
        """
        Create a polygon shaped curve.
        Args:
            n_corners: Number of Corners
            radius:
        """
        angles = np.linspace(0, 2 * pi, n_corners + 1)[:-1]
        x_values = np.sin(angles) * radius
        y_values = np.cos(angles) * radius
        z_values = np.zeros(n_corners)
        vertices = np.column_stack((x_values, y_values, z_values))
        super().__init__(vertices, spline_type, name)
        self.cyclic = True


class Rectangle(Curve):
    def __init__(self, width, height, spline_type="POLY", name="Rectangle"):
        vertices = np.array([[-width / 2, -height / 2, 0],
                             [-width / 2, +height / 2, 0],
                             [+width / 2, +height / 2, 0],
                             [+width / 2, -height / 2, 0]])
        super().__init__(vertices, spline_type, name)
        self.cyclic = True


class TipTriangle(Curve):
    def __init__(self, width, length, thickness=0):
        vertices = np.array([[-width / 2, 0, 0],
                             [0, length, 0],
                             [width / 2, 0, 0]])
        super().__init__(vertices, name="TipTriangle")
        self.fill_mode = "BOTH"
        self.bpy_object.data.extrude = thickness/2
        self.cyclic = True

