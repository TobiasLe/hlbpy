import bpy
import numpy as np


def set_keyframes(obj, attribute, coordinates, frame_numbers=None, as_samples=False, interpolation_mode=1,
                  bezier_handles_left=None, bezier_handles_right=None):
    """
    Set a whole array of keyframes at once.
    Args:
        obj: bpy object
        attribute: specify which type of keyframe to set. e.g. "location" or "rotation_euler"...
        coordinates: array of coordinates e.g. [[x1, y1, z1], [x2, y2, z2], ...]
        frame_numbers: List of frame numbers. If None frame numbers 0,1,2,3.. will be used.
        as_samples: If True: Converts the keyframes into samples. (no interpolation between keyframes)
        interpolation_mode: 0 for CONSTANT, 1 for LINEAR, and 2 for BEZIER
                            (Warning: If bezier handles are not set, all handles are at (0,0))
        bezier_handles_left: coordinates of the left bezier handle relative to the keyframe coordinate.
                             shape: (n_keyframes, n_attribute_dimensions, handle_xy)
        bezier_handles_right: equivalent to bezier_handles_left

    Returns:

    """
    coordinates = np.array(coordinates)
    if coordinates.ndim == 1:
        coordinates = np.expand_dims(coordinates, axis=1)
    if obj.animation_data is None:
        obj.animation_data_create()
    if obj.animation_data.action is None:
        action = bpy.data.actions.new(obj.name + "_act")
        obj.animation_data.action = action

    n_frames = coordinates.shape[0]

    if frame_numbers is None:
        frame_numbers = np.arange(n_frames)

    for i in range(coordinates.shape[1]):
        fcurve = obj.animation_data.action.fcurves.new(attribute, index=i)
        fcurve.keyframe_points.add(n_frames)
        frame_data = np.column_stack((frame_numbers, coordinates[:, i]))
        fcurve.keyframe_points.foreach_set("co", frame_data.flatten())
        fcurve.keyframe_points.foreach_set("interpolation", [interpolation_mode] * n_frames)

        if as_samples:
            fcurve.convert_to_samples(0, n_frames)

        if interpolation_mode == 2:
            if bezier_handles_left is not None:
                bezier_handles_left_i = frame_data + np.array(bezier_handles_left)[:, i, :]
                fcurve.keyframe_points.foreach_set("handle_left", bezier_handles_left_i.flatten())
            if bezier_handles_right is not None:
                bezier_handles_right_i = frame_data + np.array(bezier_handles_right)[:, i, :]
                fcurve.keyframe_points.foreach_set("handle_right", bezier_handles_right_i.flatten())


def srgb_to_linearrgb(srgb, limit=255):
    linrgb = []
    for c in srgb:
        c /= limit
        if c < 0:
            lin_c = 0
        elif c < 0.04045:
            lin_c = c / 12.92
        else:
            lin_c = ((c + 0.055) / 1.055) ** 2.4
        linrgb.append(lin_c)
    return linrgb


def get_bpy_obj(obj):
    try:
        return obj.bpy_object
    except AttributeError:
        return obj


def apply_material_to_obj(obj, material, recursively=False):
    bpy_object = get_bpy_obj(obj)
    bpy_material = get_bpy_obj(material)

    bpy_object.active_material = bpy_material

    if recursively:
        for child in bpy_object.children:
            apply_material_to_obj(child, material, recursively=True)
