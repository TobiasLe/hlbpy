import bpy
import numpy as np


class HighLevelBase:
    if "all_hlbpy_objects" in [s.name for s in bpy.data.scenes]:
        all_hlbpy_objects_scene = bpy.data.scenes["all_hlbpy_objects"]
        objects = all_hlbpy_objects_scene.collection.objects
        while objects:
            objects.unlink(objects[0])
    else:
        all_hlbpy_objects_scene = bpy.data.scenes.new("all_hlbpy_objects")

    def __init__(self, name):
        self.bpy_object = None

    # def __getattr__(self, item):
    #     try:
    #         bpy_object = super().__getattribute__("bpy_object")
    #     except AttributeError:
    #         bpy_object = None
    #
    #     if hasattr(bpy_object, item):
    #         return getattr(bpy_object, item)
    #     else:
    #         raise AttributeError
    #
    # def __setattr__(self, key, value):
    #     try:
    #         bpy_object = self.bpy_object
    #     except AttributeError:
    #         bpy_object = None
    #
    #     if hasattr(bpy_object, key):
    #         setattr(bpy_object, key, value)
    #     else:
    #         super().__setattr__(key, value)

    @staticmethod
    def update():
        """
        update blender stuff. For example dimensions or bound_box are recalculated
        """
        for view_layer in HighLevelBase.all_hlbpy_objects_scene.view_layers:
            view_layer.update()

    def set_up_animation_data(self):
        if self.bpy_object.animation_data is None:
            self.bpy_object.animation_data_create()
        if self.bpy_object.animation_data.action is None:
            action = bpy.data.actions.new(self.bpy_object.name + "_act")
            self.bpy_object.animation_data.action = action

    def set_keyframes(self, attribute, values, frame_numbers=None, index=None, as_samples=False,
                      interpolation_mode="LINEAR",
                      bezier_handles_left=None, bezier_handles_right=None):
        """
        Set a whole array of keyframes at once.
        Args:
            bpy_object: bpy object
            attribute: specify which type of keyframe to set. e.g. "location" or "rotation_euler"...
            values: array of coordinates e.g. [[x1, y1, z1], [x2, y2, z2], ...]
            frame_numbers: List of frame numbers. If None frame numbers 0,1,2,3.. will be used.
            index: indoex of attribute e.g. for location: 0 for x 1 for y ...
            as_samples: If True: Converts the keyframes into samples. (no interpolation between keyframes)
            interpolation_mode: "CONSTANT", "LINEAR", or "BEZIER"
                                (Warning: If bezier handles are not set, all handles are at (0,0))
            bezier_handles_left: coordinates of the left bezier handle relative to the keyframe coordinate.
                                 shape: (n_keyframes, n_attribute_dimensions, handle_xy)
            bezier_handles_right: equivalent to bezier_handles_left

        Returns:

        """
        assert isinstance(interpolation_mode, str)
        interpolation_mode_number = {"CONSTANT": 0, "LINEAR": 1, "BEZIER": 2}[interpolation_mode]

        values = np.array(values)
        if values.ndim == 1:
            values = np.expand_dims(values, axis=1)
        self.set_up_animation_data()

        n_frames = values.shape[0]

        if frame_numbers is None:
            frame_numbers = np.arange(n_frames)

        for i in range(values.shape[1]):
            if values.shape[1] > 1:
                index_to_use = i
            else:
                if index is not None:
                    index_to_use = index

                else:
                    index_to_use = 0

            fcurve = self.bpy_object.animation_data.action.fcurves.find(attribute, index=index_to_use)

            if not fcurve:
                fcurve = self.bpy_object.animation_data.action.fcurves.new(attribute, index=index_to_use)

                fcurve.keyframe_points.add(n_frames)
                frame_data = np.column_stack((frame_numbers, values[:, i]))
                fcurve.keyframe_points.foreach_set("co", frame_data.flatten())
                fcurve.keyframe_points.foreach_set("interpolation", [interpolation_mode_number] * n_frames)
                if interpolation_mode == "BEZIER":
                    if bezier_handles_left is not None:
                        bezier_handles_left_i = frame_data + np.array(bezier_handles_left)[:, i, :]
                        fcurve.keyframe_points.foreach_set("handle_left", bezier_handles_left_i.flatten())
                    if bezier_handles_right is not None:
                        bezier_handles_right_i = frame_data + np.array(bezier_handles_right)[:, i, :]
                        fcurve.keyframe_points.foreach_set("handle_right", bezier_handles_right_i.flatten())

            else:
                for frame_number, value in zip(frame_numbers, values[:, i]):
                    key_frame = fcurve.keyframe_points.insert(frame_number, value, options={"FAST"})
                    key_frame.interpolation = interpolation_mode
                    if interpolation_mode == "BEZIER":
                        raise NotImplementedError("inserting bezier keyframes to existing kurve not implemented yet")

            if as_samples:
                fcurve.convert_to_samples(0, n_frames)

    def set_keyframe(self, attribute, value, frame_number, index=0, interpolation=None):
        self.set_up_animation_data()
        fcurve = self.bpy_object.animation_data.action.fcurves.find(attribute, index=index)
        if not fcurve:
            fcurve = self.bpy_object.animation_data.action.fcurves.new(attribute, index=index)
        key_frame = fcurve.keyframe_points.insert(frame_number, value, options={"FAST"})
        if interpolation:
            key_frame.interpolation = interpolation
        return key_frame
        # Warning! key_frame is only valid until another keyframe has been created
        # see https://developer.blender.org/T83044
