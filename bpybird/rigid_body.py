import bpy


def activate():
    bpy.ops.rigidbody.world_add()
    bpy.context.scene.rigidbody_world.collection = bpy.data.collections.new("RigidBodyWorld")


def pop_up(obj, location, frame):
    """
    Move object to location and activate rigid body sim at the same time.
    Args:
        obj:
        location:
        frame:

    Returns:

    """
    obj.keyframe_insert(data_path="location", frame=frame - 2)
    obj.location = location
    obj.keyframe_insert(data_path="location", frame=frame - 1)
    obj.location = location
    obj.keyframe_insert(data_path="location", frame=frame)

    obj.rigid_body.kinematic = True
    obj.keyframe_insert(data_path="rigid_body.kinematic", frame=frame)
    obj.rigid_body.kinematic = False
    obj.keyframe_insert(data_path="rigid_body.kinematic", frame=frame + 1)
