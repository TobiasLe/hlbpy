import bpy
import bmesh


def arrow(collection, length, width, head_length, head_width, thickness, zero_pad=False):
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


def cuboid(collection, shape=(1, 1, 1), name="cuboid"):
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


def uv_sphere(collection, u_segments=32, v_segments=16, radius=1, name="uv_sphere", smooth=True):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=u_segments, v_segments=v_segments, diameter=radius)
    if smooth:
        for f in bm.faces:
            f.smooth = True
    bm.to_mesh(mesh)
    bm.free()
    return obj


def text(collection, content, name="text"):
    curve = bpy.data.curves.new(type="FONT", name="text_curve")
    obj = bpy.data.objects.new(name, curve)
    obj.data.body = content
    collection.objects.link(obj)
    return obj


