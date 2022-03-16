class Transitions:
    def __init__(self, high_level_object):
        self.hl_object = high_level_object
        self.bpy_object = high_level_object.bpy_object

    def scale_up_elastic(self, start, stop=None, n_frames=30, amplitude=None, period=None):
        if stop is None:
            stop = start + n_frames

        for i in range(3):
            attribute = "scale"
            key_frame = self.hl_object.set_keyframe(attribute, 0, start, i, interpolation='ELASTIC')
            if amplitude:
                key_frame.amplitude = amplitude
            if period:
                key_frame.period = period
            self.hl_object.set_keyframe(attribute, 1, stop, i)

