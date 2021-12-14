import bpy
from .base import HighLevelBase
from .io_curve_svg.import_svg import SVGLoader


class Text(HighLevelBase):
    def __init__(self, content, name):
        curve = bpy.data.curves.new(type="FONT", name="text_curve")
        self.bpy_object = bpy.data.objects.new(name, curve)
        self.bpy_object.data.body = content


class Tex(HighLevelBase):
    def __init__(self, content, name):
        file_path = r"C:\Users\Tobias\coding\hlbpy\data\test.svg"
        loader = SVGLoader(bpy.context, file_path, True)
        loader.parse()
        loader.createGeom(True)
        self.bpy_object = None

