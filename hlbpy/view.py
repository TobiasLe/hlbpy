import bpy
import mathutils
from math import pi


def set_view(view_rotation_euler_degree, view_location=(0, 0, 0), view_distance=10, orthographic=False):
    """
    Set the perspective in all 3D viewports
    Args:
        view_rotation_euler_degree: direction you are looking in as euler angles
        view_location: position you are looking at (not position of you)
        view_distance: distance you are away from the position you are looking at
        orthographic:

    Returns:

    """
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces[0].region_3d.view_distance = view_distance
            area.spaces[0].region_3d.view_location = view_location
            euler_rad = [x/(2*pi)*360 for x in view_rotation_euler_degree]
            area.spaces[0].region_3d.view_rotation = mathutils.Euler(euler_rad).to_quaternion()
            if orthographic:
                area.spaces[0].region_3d.view_perspective = "ORTHO"
