import bpy
from .base_object import HighLevelObject
from .io_curve_svg.import_svg import SVGLoader
from .tex import tex_to_svg_file
import tempfile


class Text(HighLevelObject):
    def __init__(self, content, name):
        curve = bpy.data.curves.new(type="FONT", name=name)
        self.bpy_object = bpy.data.objects.new(name, curve)
        self.bpy_object.data.body = content
        super().__init__()


class SVG(HighLevelObject):
    def __init__(self, file_path, name):
        self.file_path = file_path
        loader = SVGLoader(bpy.context, self.file_path, True)
        loader.parse()
        loader.createGeom(False)

        self.bpy_object = bpy.data.objects.new(name, None)

        for object in loader.objects:
            object.parent = self.bpy_object
        super().__init__()
        pass


class Tex(SVG):
    def __init__(self, content, name):
        with tempfile.TemporaryDirectory() as temp_dir_path:
            file_path = tex_to_svg_file(content, temp_dir_path)
            super().__init__(file_path, name)
