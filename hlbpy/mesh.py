import bpy
import bmesh
from .base_object import HighLevelObject


class Cuboid(HighLevelObject):
    def __init__(self, shape=(1, 1, 1), limits=None, name="cuboid"):
        mesh = bpy.data.meshes.new(name)
        bpy_object = bpy.data.objects.new(name, mesh)
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bm.to_mesh(mesh)
        bm.free()
        if limits is not None:
            shape = tuple(lim[1] - lim[0] for lim in limits)
        for vertex in bpy_object.data.vertices:
            for i in range(3):
                vertex.co[i] *= shape[i]
        if limits is not None:
            # shift origin to corner
            for vertex in bpy_object.data.vertices:
                for i in range(3):
                    vertex.co[i] += shape[i] * 0.5
            bpy_object.location = tuple(lim[0] for lim in limits)

        super().__init__(bpy_object)


class Cube(Cuboid):
    def __init__(self, edge_length=1, name="cube"):
        super().__init__(shape=[edge_length] * 3, name=name)
