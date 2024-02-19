from PyQt5 import QtWidgets

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Ellipse
from matplotlib import colors

from mpl_toolkits.mplot3d.axes3d import Axes3D

import os

colors_list = ['#0092df', '#2efe00', "#feea00", '#ffa000', '#fe0000', '#fe0000']
cmap_imshow = colors.LinearSegmentedColormap.from_list("tsunami", colors_list)


class PlotBuilder:
    def __init__(self):
        self.figure = plt.Figure()

        self.canvas = FigureCanvas(self.figure)
        self.toolbar: NavigationToolbar = NavigationToolbar(self.canvas)
        self.container: QtWidgets.QWidget | None = None

    def get_widget(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.container = QtWidgets.QWidget()
        self.container.setLayout(layout)

        return self.container


class HeatmapPlotBuilder(PlotBuilder):
    def __init__(self, plot_data, default_cmap=True):
        super().__init__()
        self.line = None
        self.scatter_points: list = []
        self.ellipse = None
        self.source_center = None
        self.patches = []

        self.axes = self.figure.add_subplot(111)
        if default_cmap:
            data = self.axes.imshow(plot_data)
        else:
            data = self.axes.imshow(plot_data, cmap=cmap_imshow)

        self.figure.colorbar(data, fraction=0.046, pad=0.04)

    def get_input_points(self, n=-1):
        points = self.figure.ginput(n=n, timeout=-1, show_clicks=True,
                                    mouse_stop=MouseButton.RIGHT,
                                    mouse_pop=MouseButton.MIDDLE)
        return points

    def draw_points(self, points, color='white', marker="+"):
        xs = []
        ys = []
        for p in points:
            xs.append(p[0])
            ys.append(p[1])
            self.scatter_points.append(self.axes.scatter(x=p[0], y=p[1], marker=marker, c=color))
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def draw_source(self, center, width, height, color='white'):
        self.clear_source()
        self.source_center = self.axes.plot(center[0], center[1], marker='+', markeredgecolor=color)
        self.ellipse = Ellipse(center, width, height, facecolor='none', edgecolor=color)
        self.axes.add_patch(self.ellipse)
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def draw_line(self, x1, y1, x2, y2, color='white'):
        self.axes.plot([x1, x2], [y1, y2], marker='o', color=color)
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def clear_source(self):
        if self.source_center:
            self.source_center[0].remove()
        if self.ellipse:
            self.ellipse.remove()

    def clear_points(self):
        if len(self.scatter_points) > 0:
            for point in self.scatter_points:
                point.remove()
            self.figure.canvas.draw()
            self.figure.canvas.flush_events()
            self.scatter_points = []

    def clear_line(self):
        self.line.remove()


class HeatmapContourPlotBuilder(HeatmapPlotBuilder):
    def __init__(self, plot_data, levels, use_default_cmap=True):
        super().__init__(plot_data, use_default_cmap)
        self.levels = levels

        if use_default_cmap:
            self.axes.contourf(plot_data, levels=levels)
        else:
            self.axes.contourf(plot_data, levels=levels, cmap=cmap_imshow)


class Heatmap3DPlotBuilder(PlotBuilder):
    def __init__(self, plot_data):
        super().__init__()

        self.axes = self.figure.add_subplot(1, 1, 1, projection='3d')
        self.axes.view_init(elev=30, azim=40, roll=0)

        y = np.arange(0, plot_data.shape[0])
        x = np.arange(0, plot_data.shape[1])
        x_arranged, y_arranged = np.meshgrid(x, y)

        x_scale = 5
        y_scale = 3
        z_scale = 0.5

        scale = np.diag([x_scale, y_scale, z_scale, 1.0])
        scale = scale * (1.0 / scale.max())
        scale[3, 3] = 1

        def short_proj():
            return np.dot(Axes3D.get_proj(self.axes), scale)

        self.axes.get_proj = short_proj

        data = self.axes.plot_surface(x_arranged, y_arranged, plot_data, cmap=cmap_imshow)

        self.axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.axes.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.axes.set_zticks([])
        self.axes.grid(False)
        self.figure.colorbar(data, fraction=0.046, pad=0.04)
        # self.axes.plot_surface(x_arranged, y_arranged, plot_data, cmap=colormaps.viridis)


class BarPlotBuilder(PlotBuilder):
    def __init__(self, plot_data, save_data_callback):
        super().__init__()
        self.toolbar: NavigationToolbar = ToolbarWithSaveData(self.canvas, save_data_callback)

        self.axes = self.figure.add_subplot(111)
        x = range(len(plot_data))
        self.axes.bar(x, plot_data)


class MarigramsPlotBuilder(PlotBuilder):
    def __init__(self, xs, plot_data, coordinates, save_data_callback):
        super().__init__()
        self.toolbar: NavigationToolbar = ToolbarWithSaveData(self.canvas, save_data_callback)

        n_marigrams = len(plot_data)
        self.axes = self.figure.subplots(n_marigrams)
        for i in range(len(plot_data)):
            point_data = plot_data[i]
            point_coords = coordinates[i]
            if n_marigrams == 1:
                curr_ax = self.axes
            else:
                curr_ax = self.axes[i]
            curr_ax.plot(xs, point_data)
            curr_ax.set_title("x = {}, y = {}".format(int(point_coords[0]), int(point_coords[1])), x=1.11, y=0.2)
            curr_ax.set_ylim([-1, 1])
            curr_ax.label_outer()
            curr_ax.spines['top'].set_visible(False)
            curr_ax.spines['right'].set_visible(False)
            curr_ax.spines['bottom'].set_visible(False)
            curr_ax.grid(True)

        if n_marigrams == 1:
            self.axes.set_xlabel("s", loc='right')
        else:
            self.axes[-1].set_xlabel("s", loc='right')
            self.axes[-1].spines['bottom'].set_visible(True)

        self.figure.subplots_adjust(right=0.83)


class ToolbarWithSaveData(NavigationToolbar):
    toolitems = [*NavigationToolbar.toolitems,
                 ('SaveData', 'Save data', str(os.getcwd()) + '\\resources\\save_file_icon', 'save_data')]

    def __init__(self, canvas, save_data_callback):
        super().__init__(canvas)
        self.save_data_callback = save_data_callback

    def save_data(self):
        self.save_data_callback()
