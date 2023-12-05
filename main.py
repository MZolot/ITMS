import resources.main_ui as main_ui
from data_entry import DataEntry
from input_menu import InputMenuDialog
from plot_building.plot_building import *

import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QProcess, Qt

from matplotlib.backend_bases import MouseButton
import numpy as np


class MOSTApp(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # можно будет добавить кнопку reset для возвращения к начальному значению
        self.ini_data_elements = {
            "x-size": DataEntry("X-size", 1500, ""),
            "y-size": DataEntry("Y-size", 900, ""),
            "x-step": DataEntry("X-step", 400, "m", True),
            "y-step": DataEntry("Y-step", 400, "m", True),
            "max elevation at source": DataEntry("Max elevation at source", 1.0, "m", True),
            "ellipse half x length": DataEntry("Ellipse half x length", 50000, "m"),
            "ellipse half y length": DataEntry("Ellipse half y length", 25000, "m"),
            "ellipse center x location": DataEntry("Ellipse center x location", 750, ""),
            "ellipse center y location": DataEntry("Ellipse center y location", 750, ""),
            "lowest depth": DataEntry("Lowest depth", 8.0, "m", True),
            "time step": DataEntry("Time step", 0.5, "s", True),
            "number of time steps": DataEntry("Number of time steps", 20, ""),
            "number of steps between surface output": DataEntry("Number of steps\nbetween surface output", 10, "")
        }

        self.input_menus_elements = {
            "area": [
                "x-size",
                "y-size",
                "x-step",
                "y-step"
            ],
            "size": [
                "x-size",
                "y-size"
            ],
            "steps": [
                "x-step",
                "y-step"
            ],
            "source": [
                "max elevation at source",
                "ellipse half x length",
                "ellipse half y length",
                "ellipse center x location",
                "ellipse center y location",
                "lowest depth"
            ],
            "calculation": [
                "time step",
                "number of time steps",
                "number of steps between surface output"
            ]
        }

        self.koryto = np.loadtxt("MOST\\koryto_profile.txt")
        self.koryto2d = np.transpose(np.tile(self.koryto, (1500, 1)))

        self.marigram_points = []

        self.calculated = False

        self.setupUi(self)
        self._complete_ui()

    def _complete_ui(self):
        self.setCentralWidget(get_plot_widget("imshow", self.koryto2d))

        self.action_size.triggered.connect(
            lambda: self._open_input_menu(self.input_menus_elements["size"]))
        self.action_steps.triggered.connect(
            lambda: self._open_input_menu(self.input_menus_elements["steps"]))
        self.action_source_parameters.triggered.connect(
            lambda: self._open_input_menu(self.input_menus_elements["source"]))
        self.action_calculation_parameters.triggered.connect(
            lambda: self._open_input_menu(self.input_menus_elements["calculation"]))
        self.action_calculate.triggered.connect(self._calculate)

        self.action_show_area.triggered.connect(
            lambda: self.setCentralWidget(get_plot_widget("imshow", self.koryto2d))
        )

        self.menu_visualisation.triggered.connect(
            lambda: print("visualisation!")
        )

        self.action_select_points.triggered.connect(self._select_marigram_points)
        self.action_marigrams.triggered.connect(self._plot_marigrams)

    def _open_input_menu(self, element_names):
        elements = []
        for n in element_names:
            elements.append(self.ini_data_elements[n])
        menu = InputMenuDialog(elements)
        menu.exec()

    def _save_all_parameters(self):
        ini_data_file = open("MOST\\ini_data.txt", "w")

        for i in self.ini_data_elements.values():
            input_data = str(i.get_current_value()) + '\n'
            ini_data_file.write(input_data)
        ini_data_file.close()

    def _calculate(self):
        # это должно работать, только если программа запущена в первый раз, или если данные изменились!!!
        self._save_all_parameters()
        self._show_calculation_screen()

        commands = "MOST\\wave_1500x900_01.exe"

        self.process = QProcess()
        self.process.setWorkingDirectory('MOST\\')
        self.process.readyReadStandardOutput.connect(self._update_progress)
        self.process.finished.connect(self._show_result)
        self.process.start(commands)

    def _update_progress(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8").strip()
        if stdout != '':
            self.pbar.setValue(int(stdout))

    def _show_calculation_screen(self):
        steps = self.ini_data_elements["number of time steps"].get_current_value()
        label1 = QtWidgets.QLabel("Computation in progress... Please wait.\n" + str(steps) + " steps total.")
        label1.setAlignment(Qt.AlignCenter)
        label1.setFont(QFont("MS Shell Dlg 2", 9))
        label1.setMaximumHeight(50)

        self.pbar = QtWidgets.QProgressBar(self)
        self.pbar.setMaximum(steps)
        self.pbar.setMaximumWidth(500)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(self.pbar)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(70)

        container = QtWidgets.QWidget()
        container.setLayout(layout)
        # container.setAutoFillBackground(True)
        # container.setStyleSheet("background-color: blue;")

        self.setCentralWidget(container)

    def _show_result(self):
        # print("finished")
        self.max_height = np.loadtxt("MOST\\maxheigh.dat")
        self.height = np.loadtxt("MOST\\heigh.dat")

        self.calculated = True

        self.action_heatmap.setEnabled(True)
        self.action_3d_heatmap.setEnabled(True)
        self.action_heatmap_with_contour.setEnabled(True)
        self.action_shore_bar_chart.setEnabled(True)

        if self.marigram_points:
            self.action_marigrams.setEnabled(True)

        self.action_heatmap.triggered.connect(
            lambda: self.setCentralWidget(get_plot_widget("imshow", self.max_height))
        )
        self.action_3d_heatmap.triggered.connect(
            lambda: self.setCentralWidget(get_plot_widget("3d", self.max_height))
        )
        self.action_heatmap_with_contour.triggered.connect(
            lambda: self.setCentralWidget(get_plot_widget("contour", self.max_height))
        )
        self.action_shore_bar_chart.triggered.connect(
            lambda: self.setCentralWidget(get_plot_widget("bar", self.max_height[750]))
        )

        self.setCentralWidget(get_plot_widget("imshow", self.max_height))

    def _select_marigram_points(self):
        figure = plt.Figure()
        canvas = FigureCanvas(figure)
        axes = figure.add_subplot(111)
        axes.imshow(self.koryto2d)

        toolbar = NavigationToolbar(canvas)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(canvas)

        container = QtWidgets.QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        print("MARIGRAMS!")

        self.marigram_points = figure.ginput(n=-1, timeout=-1, show_clicks=True,
                                             mouse_stop=MouseButton.RIGHT,
                                             mouse_pop=MouseButton.MIDDLE)
        print(self.marigram_points)
        self._draw_marigram_points(self.marigram_points)

        if self.calculated:
            self.action_marigrams.setEnabled(True)

    def _draw_marigram_points(self, points):
        figure = plt.Figure()
        axes = figure.add_subplot(111)
        axes.imshow(self.koryto2d)

        for p in points:
            axes.scatter(x=p[0], y=p[1], marker="+", c="blue")

        widget = make_widget_with_toolbar(figure)
        self.setCentralWidget(widget)

    def _plot_marigrams(self):
        n_marigrams = len(self.marigram_points)

        figure = plt.Figure()

        length = len(self.height)
        print(length)
        axes = figure.subplots(n_marigrams)

        for i in range(n_marigrams):
            point = self.marigram_points[i]
            if n_marigrams == 1:
                curr_ax = axes
            else:
                curr_ax = axes[i]
            start_y = int(point[1])
            if start_y == 900:
                start_y = 899
            selected = self.height[[y for y in range(start_y, length, 900)], int(point[0])]
            print(selected)
            print(selected[2:])
            curr_ax.plot(selected)
            curr_ax.set_title("x = {}, y = {}".format(int(point[0]), int(point[1])), x=1.1, y=0)
            curr_ax.set_ylim([-1, 1])
            curr_ax.label_outer()
            curr_ax.spines['top'].set_visible(False)
            curr_ax.spines['bottom'].set_visible(False)
            curr_ax.spines['right'].set_visible(False)

        figure.subplots_adjust(right=0.83)

        self.setCentralWidget(make_widget_with_toolbar(figure))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MOSTApp()
    window.show()
    app.exec_()
