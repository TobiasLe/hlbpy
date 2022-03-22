import bpy
import numpy as np
from ..empty import Empty
from .axis import Axis
from ..curve import Curve, Rectangle


class Figure(Empty):
    def __init__(self, shape=(1, 1), axis_style="BAR", name="Figure"):
        super().__init__(name=name)
        self.shape = shape
        self.shape_3d = shape if len(shape)==3 else (*shape, 0)

        self.bpy_object.empty_display_type = 'ARROWS'
        self.default_line_width = min(shape) * 0.01

        self.lines = []
        self.bars = []

        self.axes = []
        if isinstance(axis_style, str):
            axis_style = [axis_style] * len(shape)
        for i in range(len(self.shape)):
            axis = Axis(length=self.shape[i], width=self.default_line_width, dim=i, axis_style=axis_style[i])
            axis.parent = self
            self.axes.append(axis)

    def line_plot(self, data, colors=None, bevel=None, spline_type="POLY", bezier_handle_type="AUTO"):
        data = np.array(data)

        if data.shape[1] == 2:
            data = np.concatenate((data, np.zeros((data.shape[0], 1))), axis=1)

        self.extent = self.default_extent(data)
        line = Curve(self.transform_to_extent(data), spline_type=spline_type, bezier_handle_type=bezier_handle_type)

        line.bevel_object = bevel or Rectangle(self.default_line_width, self.default_line_width)
        line.parent = self
        self.lines.append(line)

    def transform_to_extent(self, data):
        data = data - self.extent[:, 0]
        data = data / (self.extent[:, 1] - self.extent[:, 0]) * self.shape_3d
        return data



    # @property
    # def extent(self):
    #     return np.array([axis.extent for axis in self.axes])
    #
    # @extent.setter
    # def extent(self, extent):
    #     extent = np.array(extent)
    #     for i, axis in enumerate(self.axes):
    #         axis.extent = extent[i]
    #
    #     for i in range(len(self.axes)):
    #         scale = self.shape[i] / (extent[i, 1] - extent[i, 0])
    #         self.data_origin.location[i] = -extent[i, 0] * scale
    #         self.data_origin.scale[i] = scale


    @staticmethod
    def default_extent(data):
        extent = np.array([[np.min(data[..., i]), np.max(data[..., i])] for i in range(data.shape[-1])], dtype=np.float)
        extent[:, 0] -= 0.1 * (extent[:, 1] - extent[:, 0])
        extent[:, 1] += 0.1 * (extent[:, 1] - extent[:, 0])
        for i in range(len(extent)):
            if extent[i, 0] == extent[i, 1]:
                extent[i, 0] -= 0.5
                extent[i, 1] += 0.5

        return extent