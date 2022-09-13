try:
    import bpy
    inside_blender = True
except ModuleNotFoundError:
    from .startup import run_in_blender
    print("hlbpy was imported outside of Blender")
    inside_blender = False

from .startup import *

if inside_blender:
    from . import misc
    from . import view
    from . import curve
    from .curve import Text
    from . import mesh
    from . import special
    from . import plotting
    from .special import ParentGroup
    from . import material
    from .empty import *
    from .collection import *
    from .scene import *
    from .external import tex
    from .directions import *

