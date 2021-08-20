import bpy
import numpy as np


def set_keyframes(obj, attribute, coordinates, frame_numbers=None, as_samples=False):
    """
    Set a whole array of keyframes at once.
    Args:
        obj: bpy object
        attribute: specify which type of keyframe to set. e.g. "location" or "rotation_euler"...
        coordinates: array of coordinates e.g. [[x1, y1, z1], [x2, y2, z2], ...]
        frame_numbers: List of frame numbers. If None frame numbers 0,1,2,3.. will be used.
        as_samples: If True: Converts the keyframes into samples. (no interpolation between keyframes)

    Returns:

    """
    coordinates = np.array(coordinates)
    if coordinates.ndim == 1:
        coordinates = np.expand_dims(coordinates, axis=1)
    obj.animation_data_create()
    action = bpy.data.actions.new(obj.name + "_act")
    obj.animation_data.action = action

    n_frames = coordinates.shape[0]

    if frame_numbers is None:
        frame_numbers = np.arange(n_frames)

    for i in range(coordinates.shape[1]):
        fcurve = action.fcurves.new(attribute, index=i)
        fcurve.keyframe_points.add(n_frames)
        frame_data = np.column_stack((frame_numbers, coordinates[:, i]))
        fcurve.keyframe_points.foreach_set("co", frame_data.flatten())
        if as_samples:
            fcurve.convert_to_samples(0, n_frames)


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
