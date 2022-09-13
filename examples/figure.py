import hlbpy
import numpy as np

hlbpy.run_in_blender()

scene = hlbpy.Scene.from_context()
collection = scene.link(hlbpy.Collection("ExampleCollection"))

x_values = np.linspace(0, np.pi * 2, 100)
y_values = np.sin(x_values)

data = np.stack((x_values, y_values), axis=1)

fig = hlbpy.plotting.Figure(shape=(6, 3))
fig.line_plot(data)
fig.axes[0].set_latex_label(r"$\alpha$")
fig.axes[1].set_latex_label(r"$sin(\alpha)$")

collection.link(fig)

hlbpy.view.set_view([0, 0, 0], orthographic=True)
