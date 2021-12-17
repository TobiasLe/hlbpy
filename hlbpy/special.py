import bpy
from .base_object import HighLevelObject
from .io_curve_svg.import_svg import SVGLoader
from .tex import tex_to_svg_file
import tempfile


class ParentGroup(HighLevelObject):
    def __init__(self, children, name):
        self.bpy_object = bpy.data.objects.new(name, None)
        for child in children:
            child.parent = self.bpy_object
        super().__init__()


class SVG(ParentGroup):
    def __init__(self, file_path, name):
        self.file_path = file_path
        loader = SVGLoader(bpy.context, self.file_path, True)
        loader.parse()
        loader.createGeom(False)

        super().__init__(loader.objects, name)


class Tex(SVG):
    def __init__(self, content, name):
        with tempfile.TemporaryDirectory() as temp_dir_path:
            file_path = tex_to_svg_file(content, temp_dir_path)
            super().__init__(file_path, name)
