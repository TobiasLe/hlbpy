import bpy
import numpy as np


def activate():
    bpy.ops.rigidbody.world_add()
    bpy.context.scene.rigidbody_world.collection = bpy.data.collections.new("RigidBodyWorld")
    return bpy.context.scene.rigidbody_world


def add(object):
    bpy.context.scene.rigidbody_world.collection.objects.link(object)


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


def get_trajectory(objects, start_frame, end_frame, scene=None):
    """
    Args:
        objects:
        start_frame:
        end_frame:
        scene:

    Returns: trajectory as numpy array with shape (n_frames, n_objects, xyz)

    """
    if scene is None:
        scene = objects[0].users_scene[0]
    n_frames = end_frame - start_frame
    trajectory = np.zeros((n_frames, len(objects), 3))

    for i in range(n_frames):
        scene.frame_set(i)
        for j in range(len(objects)):
            trajectory[i, j] = objects[j].matrix_world.translation

    return trajectory
