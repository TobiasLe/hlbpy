import bpy
from .base_object import HighLevelObject
from .io_curve_svg.import_svg import SVGLoader
from .tex import tex_to_svg_file
import tempfile
import numpy as np


class ParentGroup(HighLevelObject):
    def __init__(self, children, name):
        bpy_object = bpy.data.objects.new(name, None)
        for child in children:
            child.parent = bpy_object
        super().__init__(bpy_object)


class SVG(ParentGroup):
    def __init__(self, file_path, name):
        self.file_path = file_path
        loader = SVGLoader(bpy.context, self.file_path, True)
        loader.parse()
        loader.createGeom(False)

        super().__init__(loader.objects, name)


class Tex(SVG):
    def __init__(self, content, name, scale=1000):
        with tempfile.TemporaryDirectory() as temp_dir_path:
            file_path = tex_to_svg_file(content, temp_dir_path)
            super().__init__(file_path, name)

        print(self.get_children_bound([-1, 0, 0]))
        print(np.array(self.bpy_object.children[0].bound_box))
        for child in self.bpy_object.children:
            child.scale = [scale] * 3
        self.update()
        print(np.array(self.bpy_object.children[0].bound_box))
        print(self.get_children_bound([-1, 0, 0]))