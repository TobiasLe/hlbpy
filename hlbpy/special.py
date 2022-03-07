import bpy
from .base_object import HighLevelObject
from .curve import Curve, TipTriangle, Rectangle
from .io_curve_svg.import_svg import SVGLoader
from .external.tex import tex_to_svg_file
from .external.tex import get_modified_expression
from .directions import *
import tempfile
import numpy as np
from mathutils import Vector


class ParentGroup(HighLevelObject):
    def __init__(self, children, name="ParentGroup", bpy_object=None):
        if bpy_object is None:
            bpy_object = bpy.data.objects.new(name, None)
        super().__init__(bpy_object)
        for child in children:
            child.parent = self

    def get_bound(self, direction):
        return self.get_children_bound(direction)


class SVG(ParentGroup):
    def __init__(self, file_path, name="SVG"):
        self.file_path = file_path
        loader = SVGLoader(bpy.context, self.file_path, True)
        loader.parse()
        loader.createGeom(False)
        high_level_objects = [Curve(bpy_object=obj) for obj in loader.objects]
        super().__init__(high_level_objects, name)


class Tex(SVG):
    def __init__(self, tex_string, name=None, environment="center", scale=1000):
        self.tex_string = tex_string
        if name is None:
            name = tex_string[:10] if len(tex_string) > 10 else tex_string

        with tempfile.TemporaryDirectory() as temp_dir_path:
            print("Compiling ", tex_string)
            file_path = tex_to_svg_file(get_modified_expression(tex_string), temp_dir_path, environment=environment)
            super().__init__(file_path, name)

        for child in self.bpy_object.children:
            child.scale = [scale] * 3
        self.update()
        self.align_children(CENTER)


class MathTex(Tex):
    def __init__(self, *tex_strings, name=None, scale=1000):
        super().__init__("".join(tex_strings), name=name, environment="align*", scale=scale)

        begin = 0
        subobjects = []
        for tex_string in tex_strings:
            subobject = Tex(tex_string, environment="align*", scale=scale)
            end = begin + len(subobject)
            for obj in list(subobject.children):
                obj.delete()
            for i in range(begin, end):
                self.children[0].parent = subobject
            subobjects.append(subobject)
            begin = end
        for subobject in subobjects:
            subobject.parent = self


class Arrow(Curve):
    def __init__(self, coordinates, line_width, tip_width, tip_length, thickness, name="Arrow"):
        coordinates = np.array(coordinates, dtype=float)
        tip_direction = coordinates[-1] - coordinates[-2]
        tip_direction = tip_direction / np.linalg.norm(tip_direction)
        coordinates[-1] -= tip_direction * tip_length  # making space for the tip

        super().__init__(coordinates, spline_type="NURBS", name=name)

        self.bevel_object = Rectangle(line_width, thickness)

        self.tip = TipTriangle(tip_width, tip_length, thickness)
        self.tip.parent = self
        self.tip.location = coordinates[-1]
        self.tip.rotation_euler = Vector([0, 1, 0]).rotation_difference(Vector(tip_direction)).to_euler()
