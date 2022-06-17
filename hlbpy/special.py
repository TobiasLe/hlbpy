import bpy
from .base_object import HighLevelObject
from .curve import Curve, TipTriangle, Rectangle
from .io_curve_svg.import_svg import SVGLoader
from .external.tex import tex_to_svg_file
from .external.tex import get_modified_expression
from .directions import *
from .empty import Empty
from .material import PrincipledBSDF
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
        if file_path is not None:
            self.file_path = file_path
            loader = SVGLoader(bpy.context, self.file_path, True)
            loader.parse()
            loader.createGeom(False)
            high_level_objects = [Curve(bpy_object=obj) for obj in loader.objects]
        else:
            high_level_objects = []
        super().__init__(high_level_objects, name)


class Tex(SVG):
    def __init__(self, tex_string, name=None, environment="center", scale=1000):
        self.tex_string = tex_string
        if name is None:
            if tex_string:
                name = tex_string[:10] if len(tex_string) > 10 else tex_string
            else:
                name = "EmptyTex"

        if tex_string:
            with tempfile.TemporaryDirectory() as temp_dir_path:
                print("Compiling ", tex_string)
                file_path = tex_to_svg_file(get_modified_expression(tex_string), temp_dir_path, environment=environment)
                super().__init__(file_path, name)
        else:
            super().__init__(None, name)

        for child in self.bpy_object.children:
            child.scale = [scale] * 3
        self.set_recursively("material", PrincipledBSDF(name=name + "Mat"))
        self.update()
        self.align_children(CENTER)

    def transform(self, target, start, stop=None, n_frames=30, target_indices=None, adjust_spline_number=True,
                  blend_offset=0):
        if stop is None:
            stop = start + n_frames

        if len(self) == 0:
            target.material.alpha_blend(start + blend_offset, stop, 0, 1)
            target.hide_until(start)

        elif len(target) == 0:
            self.material.alpha_blend(start, stop - blend_offset, 1, 0)
            self.hide_from(stop)
        else:
            self.equalize_child_numbers(target)
            for own_child, target_child in zip(self, target):
                own_child.transform(target_child,
                                    start=start,
                                    stop=stop,
                                    n_frames=n_frames,
                                    hide=True,
                                    adjust_spline_number=adjust_spline_number)

    def equalize_child_numbers(self, target):
        if len(self) == 0 or len(target) == 0:
            return

        if len(self) > len(target):
            to_extend = target
            other = self
        elif len(target) > len(self):
            to_extend = self
            other = target
        else:
            return

        repeat_indices = (np.arange(len(other)) * len(to_extend) // len(other))
        copy_factors = [sum(repeat_indices == i) for i in range(len(to_extend))]
        new_children = []
        for child, factor in zip(to_extend.children, copy_factors):
            new_children.append(child)
            for _ in range(1, factor):
                new_children.append(child.copy())

        for child in new_children:
            child.parent = to_extend


class MathTex(ParentGroup):
    def __init__(self, *tex_strings, name=None, scale=1000):
        full_tex = Tex("".join(tex_strings), name=name, environment="align*", scale=scale)
        if len(tex_strings) == 1:
            subobjects = [full_tex]
        else:
            begin = 0
            subobjects = []
            for tex_string in tex_strings:
                subobject = Tex(tex_string, environment="align*", scale=scale)

                end = begin + len(subobject)
                for obj in list(subobject.children):
                    obj.delete()
                for i in range(begin, end):
                    full_tex.children[0].parent = subobject
                subobjects.append(subobject)
                begin = end
            full_tex.delete()

        if name is None:
            if tex_strings[0]:
                name = tex_strings[0][:10] if len(tex_strings[0]) > 10 else tex_strings[0]
            else:
                name = "EmptyTex"

        super().__init__(subobjects, name=name)

        for subobject in subobjects:
            subobject.set_recursively("material", PrincipledBSDF(name=subobject.name + "Mat"))

    def transform(self, target, start, stop=None, n_frames=30, target_indices=None, adjust_spline_number=True,
                  blend_offset=None):
        if stop is None:
            stop = start + n_frames
        if blend_offset is None:
            blend_offset = int((stop - start) * 2 / 3)

        if target_indices is None:
            if len(self) != len(target):
                raise ValueError("self and transformation target must have the same number of tex_strings or "
                                 "target_indices must be given.")
            for own_child, target_child in zip(self, target):
                own_child.transform(target_child, start, stop=stop, n_frames=n_frames,
                                    adjust_spline_number=adjust_spline_number, blend_offset=blend_offset)

        else:
            if len(self) != len(target_indices):
                raise ValueError("The number of target indices must be equal to the number of tex segments")
            for own_child, target_index in zip(self, target_indices):
                own_child.transform(target[target_index], start, stop=stop, n_frames=n_frames,
                                    adjust_spline_number=adjust_spline_number, blend_offset=blend_offset)


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
