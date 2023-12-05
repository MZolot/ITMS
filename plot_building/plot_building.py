from PyQt5 import QtWidgets

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import Axes3D


def get_plot_widget(type_of_plot, args):
    canvas = get_canvas(type_of_plot, args)

    toolbar = NavigationToolbar(canvas)

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(toolbar)
    layout.addWidget(canvas)

    container = QtWidgets.QWidget()
    container.setLayout(layout)

    return container


def get_canvas(type_of_plot, args):
    figure = plt.Figure()
    canvas = FigureCanvas(figure)
    axes = figure.add_subplot(111)

    if type_of_plot == "imshow":
        axes.imshow(args)
    elif type_of_plot == "contour":
        axes.imshow(args)
        axes.contourf(args)
    elif type_of_plot == "bar":
        x = range(len(args))
        axes.bar(x, args)
    elif type_of_plot == "3d":
        axes = figure.add_subplot(1, 1, 1, projection='3d')
        y = np.arange(0, args.shape[0])
        x = np.arange(0, args.shape[1])
        X, Y = np.meshgrid(x, y)
        # x_scale = 5
        # y_scale = 3
        # z_scale = 1
        # scale = np.diag([x_scale, y_scale, z_scale, 1.0])
        # scale = scale * (1.0 / scale.max())
        # scale[3, 3] = 1.0
        # axes.get_proj = short_proj
        axes.plot_surface(X, Y, args, cmap=cm.viridis)

    return canvas


def make_widget_with_toolbar(figure):
    canvas = FigureCanvas(figure)

    toolbar = NavigationToolbar(canvas)

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(toolbar)
    layout.addWidget(canvas)

    container = QtWidgets.QWidget()
    container.setLayout(layout)

    return container


def short_proj(axes, scale):
    return np.dot(Axes3D.get_proj(axes), scale)

