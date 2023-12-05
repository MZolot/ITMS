from PyQt5 import QtWidgets

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backend_bases import MouseButton
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import Axes3D


class PlotBuilder:
    def __init__(self, plot_type, plot_data):

        self.figure = plt.Figure()
        self.current_container = QtWidgets.QWidget
        # self.canvas = FigureCanvas(self.figure)

        if plot_type == "imshow":
            self.axes = self.figure.add_subplot(111)
            self.axes.imshow(plot_data)
        elif plot_type == "contour":
            self.axes = self.figure.add_subplot(111)
            self.axes.imshow(plot_data)
            self.axes.contourf(plot_data)
        elif plot_type == "bar":
            self.axes = self.figure.add_subplot(111)
            x = range(len(plot_data))
            self.axes.bar(x, plot_data)
        elif plot_type == "3d":
            self._plot_3d(plot_data)
        elif plot_type == "marigrams":
            self._plot_marigrams(plot_data)

    def _plot_3d(self, plot_data):
        self.axes = self.figure.add_subplot(1, 1, 1, projection='3d')
        y = np.arange(0, plot_data.shape[0])
        x = np.arange(0, plot_data.shape[1])
        x_arranged, y_arranged = np.meshgrid(x, y)
        self.axes.plot_surface(x_arranged, y_arranged, plot_data, cmap=cm.viridis)

    def _plot_marigrams(self, plot_data):
        n_marigrams = len(plot_data)
        self.axes = self.figure.subplots(n_marigrams)
        for i in range(len(plot_data)):
            point_data = plot_data[i]
            if n_marigrams == 1:
                curr_ax = self.axes
            else:
                curr_ax = self.axes[i]
            print(point_data)
            curr_ax.plot(point_data[2:])
            curr_ax.set_title("x = {}, y = {}".format(int(point_data[0]), int(point_data[1])), x=1.1, y=0)
            curr_ax.set_ylim([-1, 1])
            curr_ax.label_outer()
            curr_ax.spines['top'].set_visible(False)
            curr_ax.spines['right'].set_visible(False)
        self.figure.subplots_adjust(right=0.83)

    def get_widget(self):
        canvas = FigureCanvas(self.figure)

        toolbar = NavigationToolbar(canvas)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(canvas)

        self.current_container = QtWidgets.QWidget()
        self.current_container.setLayout(layout)

        return self.current_container

    def get_layout(self):
        canvas = FigureCanvas(self.figure)
        toolbar = NavigationToolbar(canvas)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(canvas)

        return layout

    def get_input_points(self):
        points = self.figure.ginput(n=-1, timeout=-1, show_clicks=True,
                                    mouse_stop=MouseButton.RIGHT,
                                    mouse_pop=MouseButton.MIDDLE)
        return points

    def draw_points(self, points):
        for p in points:
            self.axes.scatter(x=p[0], y=p[1], marker="+", c="blue")
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        # self.current_container.update()
