import ui_elements.qt_designer_ui.main_ui as main_ui
from data_entry import DataEntry
from ui_elements.file_selection_menu import *
from ui_elements.input_menu import *
from ui_elements.computation_in_process_screen import *
from ui_elements.isoline_settings_dialog import *
from file_loader import *
from plots.stacked_plots_widget import PlotWidget
from plots.matplotlib_plot_builder import (HeatmapPlotBuilder,
                                           HeatmapContourPlotBuilder,
                                           Heatmap3DPlotBuilder,
                                           BarPlotBuilder,
                                           MarigramsPlotBuilder)

from PyQt5 import QtWidgets
from PyQt5.QtCore import QProcess, Qt, QThread

import numpy as np

import sys
import json

ini_data_elements_file_name = "resources/ini_data_elements.json"

executable_file_name = "MOST/wave_1500x900_01.exe"

bottom_profile_file_name = "MOST/koryto_profile.txt"

ini_data_default_file_name = "MOST/ini_data.txt"
height_default_file_name = "MOST/heigh.dat"
max_height_default_file_name = "MOST/maxheigh.dat"


class MOSTApp(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.file_names = {
            "initial": ini_data_default_file_name,
            "height": height_default_file_name,
            "max_height": max_height_default_file_name
        }

        # можно будет добавить кнопку reset для возвращения к начальному значению
        self.ini_data_elements = {}
        with open(ini_data_elements_file_name, 'r') as j:
            from_json = json.loads(j.read())
            for element in from_json:
                self.ini_data_elements[element["name"]] = DataEntry(element["name"], element["label_text"],
                                                                    element["default_value"], element["unit"],
                                                                    element["is_float"])

        self.input_menus_elements = {
            "area": ["x-size", "y-size", "x-step", "y-step"],
            "size": ["x-size", "y-size"],
            "steps": ["x-step", "y-step"],
            "source": ["max elevation at source", "ellipse half x length", "ellipse half y length",
                       "ellipse center x location", "ellipse center y location", "lowest depth"],
            "calculation": ["time step", "number of time steps", "number of steps between surface output"]
        }

        self.bottom_profile = np.loadtxt(bottom_profile_file_name)
        self.bottom_map = np.transpose(np.tile(self.bottom_profile, (1500, 1)))
        # self.bottom_map = np.tile(self.bottom_profile, (1500, 1))

        self.bottom_plot = HeatmapPlotBuilder(self.bottom_map)
        self.draw_source()
        self.plot_widget = PlotWidget({"bottom": self.bottom_plot})

        self.marigram_points = []
        self.isoline_levels = [0.005, 0.01, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1]

        self.calculated = False

        self.height = None
        self.max_height = None
        self.thread = None
        self.loader = None

        self.heatmap_plot = None
        self.heatmap_with_contour_plot = None
        self.heatmap_3d_plot = None
        self.shore_bar_chart_plot = None

        self.setupUi(self)
        self._complete_ui()

    def _complete_ui(self):
        self.setCentralWidget(self.plot_widget.get_widget())
        self.draw_source()

        self.action_size.triggered.connect(
            lambda: self._open_input_menu(self.input_menus_elements["size"], "Size parameters"))
        self.action_steps.triggered.connect(
            lambda: self._open_input_menu(self.input_menus_elements["steps"], "Steps parameters"))
        self.action_source_parameters.triggered.connect(
            lambda: self._open_input_menu(self.input_menus_elements["source"], "Source parameters", True))
        self.action_calculation_parameters.triggered.connect(
            lambda: self._open_input_menu(self.input_menus_elements["calculation"], "Calculation parameters"))
        self.action_calculate.triggered.connect(self._calculate)

        self.action_show_area.triggered.connect(
            lambda: self.plot_widget.set_plot("bottom"))

        self.action_select_points_on_area.triggered.connect(
            lambda: self._select_marigram_points("bottom"))
        self.action_marigrams.triggered.connect(self._plot_marigrams)

        self.action_load_existing_results.triggered.connect(self._open_file_selection_menu)
        self.action_set_contour_lines_levels.triggered.connect(self._open_isoline_settings_menu)

    def _open_input_menu(self, element_names, title, source=False):
        elements = []
        for n in element_names:
            elements.append(self.ini_data_elements[n])
        if source:
            menu = SourceMenuDialog(elements, title, self)
        else:
            menu = InputMenuDialog(elements, title)
        menu.exec()

    def _open_isoline_settings_menu(self):
        menu = IsolineSettingsDialog(self.isoline_levels, self.update_isoline_levels)
        menu.exec()

    def _open_file_selection_menu(self):
        menu = FileSelectionMenuDialog(self.file_names, self.load_result)
        menu.exec()

    def _save_all_parameters(self):
        ini_data_file = open(self.file_names["initial"], "w")

        for i in self.ini_data_elements.values():
            input_data = str(i.get_current_value()) + "  --  " + i.label_text + '\n'
            ini_data_file.write(input_data)
        ini_data_file.close()

    def _calculate(self):
        # это должно работать, только если программа запущена в первый раз, или если данные изменились
        self._save_all_parameters()
        self._show_calculation_screen()

        commands = executable_file_name

        self.process = QProcess()
        self.process.setWorkingDirectory('MOST\\')
        self.process.readyReadStandardOutput.connect(self._update_progress)
        self.process.finished.connect(self.load_result)
        self.process.start(commands)

    def _update_progress(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8").strip()
        if stdout != '':
            self.calculation_screen.update_progress_bar(int(stdout))

    def _show_calculation_screen(self):
        steps = self.ini_data_elements["number of time steps"].get_current_value()
        self.calculation_screen = ComputationScreen(steps)
        self.setCentralWidget(self.calculation_screen.get_screen())

    def _show_loading_screen(self):
        label_computation_info = QtWidgets.QLabel("Loading results... Please wait.")
        label_computation_info.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label_computation_info)

    def load_result(self):
        self._show_loading_screen()

        self.thread = QThread()
        self.loader = FileLoader([self.file_names["max_height"], self.file_names["height"]])
        self.loader.moveToThread(self.thread)
        self.thread.started.connect(self.loader.run)
        self.loader.finished.connect(self.thread.quit)
        self.loader.finished.connect(self.loader.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.show_result)
        self.thread.start()

    def parse_initial_data_file(self):
        f = open(self.file_names["initial"], "r")
        for parameter in self.ini_data_elements.values():
            new_value = f.readline().split()[0]
            parameter.set_current_value(new_value)

    def show_result(self):
        print("show result")
        self.bottom_plot = HeatmapPlotBuilder(self.bottom_map)
        self.draw_source()
        self.plot_widget = PlotWidget({"bottom": self.bottom_plot})

        loaded_files = self.loader.get_results()
        if self.file_names["initial"] != ini_data_default_file_name:
            self.parse_initial_data_file()
        self.max_height = loaded_files[self.file_names["max_height"]]
        self.height = loaded_files[self.file_names["height"]]

        self.calculated = True

        self.action_heatmap.setEnabled(True)
        self.action_heatmap_with_contour.setEnabled(True)
        self.action_3d_heatmap.setEnabled(True)
        self.action_shore_bar_chart.setEnabled(True)

        self.heatmap_plot = HeatmapPlotBuilder(self.max_height, default_cmap=False)
        self.heatmap_with_contour_plot = HeatmapContourPlotBuilder(self.max_height,
                                                                   levels=self.isoline_levels,
                                                                   use_default_cmap=False)
        self.heatmap_3d_plot = Heatmap3DPlotBuilder(self.max_height)
        self.shore_bar_chart_plot = BarPlotBuilder(self.max_height[3])

        self.plot_widget.add_plot("heatmap", self.heatmap_plot)
        self.plot_widget.add_plot("heatmap contour", self.heatmap_with_contour_plot)
        self.plot_widget.add_plot("heatmap 3d", self.heatmap_3d_plot)
        self.plot_widget.add_plot("bar", self.shore_bar_chart_plot)

        if self.marigram_points:
            self.action_marigrams.setEnabled(True)

        self.action_heatmap.triggered.connect(
            lambda: self.plot_widget.set_plot("heatmap")
        )
        self.action_3d_heatmap.triggered.connect(
            lambda: self.plot_widget.set_plot("heatmap 3d")
        )
        self.action_heatmap_with_contour.triggered.connect(
            lambda: self.plot_widget.set_plot("heatmap contour")
        )
        self.action_shore_bar_chart.triggered.connect(
            lambda: self.plot_widget.set_plot("bar")
        )

        self.action_select_points_on_heatmap.setEnabled(True)
        self.action_select_points_on_heatmap.triggered.connect(
            lambda: self._select_marigram_points("heatmap"))

        self.plot_widget.set_plot("heatmap")
        self.setCentralWidget(self.plot_widget.get_widget())

    def _select_marigram_points(self, plot_name: str):
        self.plot_widget.set_plot(plot_name)
        plot = self.plot_widget.get_plot_by_name(plot_name)
        self.marigram_points = plot.get_input_points()
        plot.draw_points(self.marigram_points)

        if self.calculated:
            self.action_marigrams.setEnabled(True)

    def _plot_marigrams(self):
        x = []
        time_step = self.ini_data_elements["time step"].get_current_value()
        steps_total = self.ini_data_elements["number of time steps"].get_current_value()
        steps_between = self.ini_data_elements["number of steps between surface output"].get_current_value()
        for i in range(0, steps_total, steps_between):
            x.append(i * time_step)

        plot_data = []
        coordinates = []
        n_marigrams = len(self.marigram_points)
        length = len(self.height)
        y_size = self.ini_data_elements["y-size"].get_current_value()

        for i in range(n_marigrams):
            point = self.marigram_points[i]
            start_y = int(point[1])
            if start_y == y_size:
                start_y = y_size - 1
            selected = self.height[[y for y in range(start_y, length, y_size)], int(point[0])]
            plot_data.append(selected.tolist())
            coordinates.append((point[0], point[1]))

        self.marigrams_plot = MarigramsPlotBuilder(x, plot_data, coordinates)
        self.plot_widget.add_plot("marigrams", self.marigrams_plot)
        self.plot_widget.set_plot("marigrams")
        # self.setCentralWidget(self.marigrams_plot.get_widget())

    def draw_source(self):
        x = self.ini_data_elements["ellipse center x location"].get_current_value()
        y = self.ini_data_elements["ellipse center y location"].get_current_value()
        x_step = self.ini_data_elements["x-step"].get_current_value()
        y_step = self.ini_data_elements["y-step"].get_current_value()
        self.bottom_plot.draw_source(
            (x, y),
            (self.ini_data_elements["ellipse half x length"].get_current_value() * 2) / x_step,
            (self.ini_data_elements["ellipse half y length"].get_current_value() * 2) / y_step
        )

    def update_isoline_levels(self):
        if not self.calculated:
            return

        self.heatmap_with_contour_plot = HeatmapContourPlotBuilder(self.max_height,
                                                                   levels=self.isoline_levels,
                                                                   use_default_cmap=False)
        self.plot_widget.add_plot("heatmap contour", self.heatmap_with_contour_plot)
        self.plot_widget.set_plot("heatmap contour")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MOSTApp()
    window.show()
    app.exec_()
