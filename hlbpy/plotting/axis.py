import bpy
import numpy as np
from ..empty import Empty
from ..mesh import Cuboid
from ..special import Tex
from math import pi

class Axis(Empty):
    def __init__(self, length, dim, extent=None, width=None, axis_style="BAR", name="Axis"):
        super().__init__(name=name)
        self.length = length
        if extent is None:
            extent = [0, 1]
        self.extent = extent
        if width is None:
            width = 0.02 * length
        self.width = width
        self.dim = dim

        axis_shape = [width] * 3
        axis_shape[dim] = length
        if axis_style == "ARROW":
            raise NotImplementedError("Todo: rotation of arrows for axis directions")
            self.axis_object = arrow(length, width, width * 2, width * 2, width, self.collection,
                                     zero_pad=True)

        elif axis_style == "BAR":
            self.axis_object = Cuboid(axis_shape, name="axis_bar")
            self.axis_object.parent = self
            for vertex in self.axis_object.bpy_object.data.vertices:
                vertex.co[dim] += 0.5 * length - 0.5 * width
        elif not axis_style:
            self.axis_object = None
        else:
            raise NotImplementedError(f"Axis style '{axis_style}' is not implemented.")

        use_axes = [False, False, False]
        use_axes[dim] = True

        self.ticks = []
        self.tick_labels = []
        self.label = None

        self.label_rotation = (0, 0, 0)

    def set_ticks(self, tick_locations, tick_label_texts=None, auto_toggle_visibility=True):
        raise NotImplementedError
        tick_coordinates = np.zeros((len(tick_locations), 3))
        tick_coordinates[:, self.dim] = tick_locations
        self.axis_scaffold.data.from_pydata(tick_coordinates, [], [])
        self.axis_scaffold.data.update()
        if tick_label_texts is None:
            tick_label_texts = [f"{location:,}".replace(",", " ") for location in tick_locations]

        for i, location in enumerate(tick_locations):
            # tick origin
            tick_origin = bpy.data.objects.new("tick_origin", None)
            self.collection.objects.link(tick_origin)
            tick_origin.parent = self.axis_scaffold
            tick_origin.parent_type = "VERTEX"
            tick_origin.parent_vertices[0] = i
            tick_origin["tick_priority"] = tick_priority(location)
            add_constraint(tick_origin, "COPY_ROTATION", self.figure_origin)
            if auto_toggle_visibility:
                add_label_visibility_driver(tick_origin, self.figure_origin, self.data_origin, self.length, self.dim)

            # tick
            tick_shapes = np.array([[1, 2, 1],
                                    [2, 1, 1],
                                    [2, 1, 1]]) * self.width
            tick = make_cuboid("tick", self.collection, tick_shapes[self.dim])
            tick.parent = tick_origin
            offset_directions = [1, 0, 0]
            for vertex in tick.data.vertices:
                vertex.co[offset_directions[self.dim]] -= self.width
            self.ticks.append(tick)

            # tick label
            if tick_label_texts[i]:
                label = make_text(tick_label_texts[i], self.collection, name="tick_label")
                if self.dim == 0:
                    label.data.align_x = "CENTER"
                    label.data.align_y = "TOP"
                else:
                    label.data.align_x = "RIGHT"
                    label.data.align_y = "CENTER"
                label.data.space_word = 0.7
                label.parent = tick_origin
                label.location[offset_directions[self.dim]] -= 4 * self.width
                label.scale *= self.width * 15
                self.tick_labels.append(label)

    def set_latex_label(self, text, offset=None):
        if offset is None:
            offset = self.width * 25
        self.label = Tex(text, name="self.label_dim{}".format(self.dim))
        self.label.parent = self
        self.label.scale *= self.width * 15
        if self.dim == 0:
            self.label.location = [self.length / 2, -offset, 0]
        elif self.dim == 1:
            self.label.location = [-offset, self.length / 2, 0]
            self.label.rotation_euler[2] = pi / 2
        elif self.dim == 2:
            self.label.location = [-offset, 0, self.length / 2]
        return self.label