import bpy


class HighLevelBase:
    def __init__(self, name):
        self.bpy_object = None

    def __getattr__(self, item):
        try:
            bpy_object = super().__getattribute__("bpy_object")
        except AttributeError:
            bpy_object = None

        if hasattr(bpy_object, item):
            return getattr(bpy_object, item)
        else:
            raise AttributeError

    def __setattr__(self, key, value):
        try:
            bpy_object = self.bpy_object
        except AttributeError:
            bpy_object = None

        if hasattr(bpy_object, key):
            setattr(bpy_object, key, value)
        else:
            super().__setattr__(key, value)

    @staticmethod
    def update():
        """
        update blender stuff. For example dimensions or bound_box are recalculated
        """
        for scene in bpy.data.scenes:
            for view_layer in scene.view_layers:
                view_layer.update()
