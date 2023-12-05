import resources.main_ui as main_ui
from data_entry import DataEntry
from input_menu import InputMenuDialog
from plot_building.matplotlib_plot_builder import *

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
            "number of steps between surface output": DataEntry("Number of steps\nbetween surface output", 4, "")
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

        self.koryto_plot = PlotBuilder("imshow", self.koryto2d)

        self.marigram_points = []

        self.calculated = False

        self.setupUi(self)
        self._complete_ui()

    def _complete_ui(self):
        self.setCentralWidget(self.koryto_plot.get_widget())

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
            lambda: self.setCentralWidget(self.koryto_plot.get_widget()))

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
        self.process.finished.connect(self._load_and_show_result)
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

    def _load_and_show_result(self):
        # print("finished")
        self.max_height = np.loadtxt("MOST\\maxheigh.dat")
        self.height = np.loadtxt("MOST\\heigh.dat")

        self.calculated = True

        self.action_heatmap.setEnabled(True)
        self.action_3d_heatmap.setEnabled(True)
        self.action_heatmap_with_contour.setEnabled(True)
        self.action_shore_bar_chart.setEnabled(True)

        self.heatmap_plot = PlotBuilder("imshow", self.max_height)
        self.heatmap_3d_plot = PlotBuilder("3d", self.max_height)
        self.heatmap_with_contour_plot = PlotBuilder("contour", self.max_height)
        self.shore_bar_chart_plot = PlotBuilder("bar", self.max_height[750])

        if self.marigram_points:
            self.action_marigrams.setEnabled(True)

        self.action_heatmap.triggered.connect(
            lambda: self.setCentralWidget(self.heatmap_plot.get_widget())
        )
        self.action_3d_heatmap.triggered.connect(
            lambda: self.setCentralWidget(self.heatmap_3d_plot.get_widget())
        )
        self.action_heatmap_with_contour.triggered.connect(
            lambda: self.setCentralWidget(self.heatmap_with_contour_plot.get_widget())
        )
        self.action_shore_bar_chart.triggered.connect(
            lambda: self.setCentralWidget(self.shore_bar_chart_plot.get_widget())
        )

        self.setCentralWidget(self.heatmap_plot.get_widget())

    def _select_marigram_points(self):
        self.setCentralWidget(self.koryto_plot.get_widget())
        self.marigram_points = self.koryto_plot.get_input_points()
        self.koryto_plot.draw_points(self.marigram_points)

        if self.calculated:
            self.action_marigrams.setEnabled(True)

    def _plot_marigrams(self):
        plot_data = []
        n_marigrams = len(self.marigram_points)
        length = len(self.height)

        for i in range(n_marigrams):
            point = self.marigram_points[i]
            start_y = int(point[1])
            if start_y == 900:
                start_y = 899
            selected = self.height[[y for y in range(start_y, length, 900)], int(point[0])]
            plot_data.append([point[0], point[1]] + selected.tolist())

        self.marigrams_plot = PlotBuilder("marigrams", plot_data)
        self.setCentralWidget(self.marigrams_plot.get_widget())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MOSTApp()
    window.show()
    app.exec_()
