import bpy
import bmesh


def arrow(length, width, head_length, head_width, thickness, collection, zero_pad=False):
    verts = [[0, 0.5 * width, 0],
             [length - head_length, 0.5 * width, 0],
             [length - head_length, 0.5 * head_width, 0],
             [length, 0, 0],
             [length - head_length, -0.5 * head_width, 0],
             [length - head_length, -0.5 * width, 0],
             [0, -0.5 * width, 0]]

    if zero_pad:
        verts[0][0] -= 0.5 * width
        verts[-1][0] -= 0.5 * width

    faces = [(0, 1, 5, 6),
             (1, 2, 3, 4, 5)]

    mesh = bpy.data.meshes.new("arrow")
    obj = bpy.data.objects.new(mesh.name, mesh)
    collection.objects.link(obj)
    mesh.from_pydata(verts, [], faces)

    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.solidify(bm, geom=bm.faces, thickness=thickness)
    bm.to_mesh(mesh)
    bm.free()
    for vertex in obj.data.vertices:
        vertex.co[2] -= 0.5 * thickness
    obj.data.update()

    return obj


def collection(name, activate=True, clear=False):
    if name not in [c.name for c in bpy.data.collections]:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    else:
        coll = bpy.data.collections[name]

    if activate:
        layer_collection = bpy.context.view_layer.layer_collection.children[coll.name]
        bpy.context.view_layer.active_layer_collection = layer_collection

    if clear:
        while coll.objects:
            bpy.data.objects.remove(coll.objects[0])
    return coll


def cuboid(name, collection, shape=(1, 1, 1)):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(mesh)
    bm.free()
    for vertex in obj.data.vertices:
        for i in range(3):
            vertex.co[i] *= shape[i]

    return obj


def text(content, collection, name="text"):
    curve = bpy.data.curves.new(type="FONT", name="text_curve")
    obj = bpy.data.objects.new(name, curve)
    obj.data.body = content
    collection.objects.link(obj)
    return obj


