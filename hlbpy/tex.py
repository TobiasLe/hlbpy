from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def tex_to_svg(tex_string, save_path):
    fig = Figure(figsize=(5, 4))
    fig.text(.5, .5, tex_string, fontsize=40, color="white")
    fig.savefig(save_path, bbox_inches="tight", facecolor=(1, 1, 1, 0))
    return save_path
