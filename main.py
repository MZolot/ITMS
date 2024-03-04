import ui_elements.qt_designer_ui.main_ui as main_ui
# from ui_elements.load_data_file_selection_dialog import *
from ui_elements.input_dialog import InputMenuDialog
# from ui_elements.waiting_screens import *
from ui_elements.isoline_settings_dialog import IsolineSettingsDialog
from ui_elements.static_settings_dialog import StaticSettingsDialog
# from data_entry import DataEntry
# from file_loader import *
from subprograms.most_interface import *
from subprograms.static_interface import *
from plots.stacked_plots_widget import PlotWidget
from plots.matplotlib_plot_builder import (HeatmapPlotBuilder,
                                           HeatmapContourPlotBuilder,
                                           Heatmap3DPlotBuilder,
                                           BarPlotBuilder,
                                           MarigramsPlotBuilder)
# from plots.pyqtgraph_plot_builder import QTGraphHeatmap3DPlotBuilder

from PyQt5 import QtWidgets
from PyQt5.QtCore import QProcess

import numpy as np

import sys
import json
import struct

most_config_file_name = "resources/most_parameters_config.json"
most_ini_data_default_file_name = "MOST/ini_data.txt"
most_exe_file_name = "MOST/wave_1500x900_01.exe"

bottom_profile_file_name = "MOST/koryto_profile.txt"

height_default_file_name = "MOST/heigh.dat"
max_height_default_file_name = "MOST/maxheigh.dat"

static_config_file_name = "resources/static_parameters_config.json"
static_ini_data_default_file_name = "STATIC/static_param.txt"
static_exe_file_name = "STATIC/Static.exe"
static_results_file_name = "STATIC/static.bin"


class MOSTApp(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.file_names = {
            "most_initial": most_ini_data_default_file_name,
            "height": height_default_file_name,
            "max_height": max_height_default_file_name,
            "static_initial": static_ini_data_default_file_name
        }

        most_files = {
            "initial": most_ini_data_default_file_name,
            "height": height_default_file_name,
            "max_height": max_height_default_file_name
        }

        self.MOST_subprogram = MOSTInterface(config_file_name=most_config_file_name,
                                             subprogram_file_names=most_files,
                                             exe_file_name=most_exe_file_name,
                                             bottom_profile_file_name=bottom_profile_file_name,
                                             save_wave_profile_callback=self.save_wave_profile_data,
                                             save_marigrams_callback=self.save_marigrams_data,
                                             show_calculation_screen_callback=self.show_most_calculation_screen,
                                             show_loading_screen_callback=self.show_loading_screen,
                                             show_results_callback=self.show_most_result)

        static_files = {
            "initial": static_ini_data_default_file_name,
            "result": static_results_file_name
        }

        self.STATIC_subprogram = STATICInterface(static_config_file_name,
                                                 static_files,
                                                 static_exe_file_name,
                                                 self.save_wave_profile_data,
                                                 self.show_static_calculation_screen,
                                                 self.show_loading_screen,
                                                 self.show_static_result)

        # self.most_ini_data_elements: dict[str, DataEntry] = {}
        # with open(most_config_file_name, 'r') as j:
        #     from_json = json.loads(j.read())
        #     for element in from_json:
        #         self.most_ini_data_elements[element["name"]] = DataEntry(element["name"], element["label_text"],
        #                                                                  element["default_value"], element["unit"],
        #                                                                  element["is_float"])

        self.most_input_menu_to_elements = {
            "area": ["x-size", "y-size", "x-step", "y-step", "lowest depth"],
            "size": ["x-size", "y-size"],
            "steps": ["x-step", "y-step"],
            "source": ["max elevation at source", "ellipse half x length", "ellipse half y length",
                       "ellipse center x location", "ellipse center y location", "lowest depth"],
            "calculation": ["time step", "number of time steps", "number of steps between surface output"]
        }

        self.static_ini_data_elements: dict[str, DataEntry] = {}
        with open(static_config_file_name, 'r') as j:
            from_json = json.loads(j.read())
            for element in from_json:
                self.static_ini_data_elements[element["name"]] = DataEntry(element["name"], element["label_text"],
                                                                           element["default_value"], element["unit"],
                                                                           element["is_float"])

        self.static_input_menu_to_elements = {
            "fault": ["L", "W", "DE", "LA", "TE", "D0", "h0"],
            "calculation": ["N1", "M1", "Dx", "Dy", "jj", "kk"]
        }

        self.bottom_profile = np.loadtxt(bottom_profile_file_name)
        self.bottom_map = np.transpose(np.tile(self.bottom_profile, (1500, 1)))
        # self.bottom_map = np.tile(self.bottom_profile, (1500, 1))

        # self.bottom_plot = HeatmapPlotBuilder(self.bottom_map)
        # self.draw_source()
        # self.plot_widget = PlotWidget({"bottom": self.bottom_plot})
        self.plot_widget = PlotWidget({"bottom": self.MOST_subprogram.bottom_plot})

        self.wave_profile_end_points = []
        self.wave_profile_data = None
        self.marigram_points = []
        self.isoline_levels = [0.005, 0.01, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1]

        self.calculated = False

        self.height = None
        self.max_height = None
        self.thread = None
        self.loader = None
        self.static_results = None
        self.isoline_plot_data = None

        self.heatmap_plot = None
        self.heatmap_with_contour_plot = None
        self.heatmap_3d_plot = None
        self.wave_profile_plot = None

        self.process: QProcess = QProcess()
        self.calculation_screen = None

        self.setupUi(self)
        self.set_actions()

        self.setCentralWidget(self.plot_widget.get_widget())
        # self.draw_source()

    def set_actions(self):
        self.action_size.triggered.connect(
            lambda: self.open_most_input_menu(self.most_input_menu_to_elements["size"], "Size parameters"))
        self.action_steps.triggered.connect(
            lambda: self.open_most_input_menu(self.most_input_menu_to_elements["steps"], "Steps parameters"))
        self.action_source_parameters.triggered.connect(
            lambda: self.open_most_input_menu(self.most_input_menu_to_elements["source"], "Source parameters", True))
        self.action_calculation_parameters.triggered.connect(
            lambda: self.open_most_input_menu(self.most_input_menu_to_elements["calculation"],
                                              "Calculation parameters"))
        self.action_calculate.triggered.connect(self.MOST_subprogram.start_subprogram)

        self.action_show_area.triggered.connect(
            lambda: self.plot_widget.set_plot("bottom"))

        self.action_select_points_on_area.triggered.connect(
            lambda: self.get_marigram_points("bottom"))
        self.action_marigrams.triggered.connect(self.plot_marigrams)

        self.action_load_existing_results.triggered.connect(self.open_most_file_selection_menu)
        self.action_set_contour_lines_levels.triggered.connect(self.open_isoline_settings_menu)

        self.action_static.triggered.connect(self.open_static_settings_dialog)

    def open_most_input_menu(self, element_names, title, source=False):
        elements = []
        for n in element_names:
            elements.append(self.MOST_subprogram.ini_data_elements[n])
            # elements.append(self.most_ini_data_elements[n])
        if source:
            menu = InputMenuDialog(elements, title, self.MOST_subprogram.draw_source)
        else:
            menu = InputMenuDialog(elements, title)
        menu.exec()

    def open_isoline_settings_menu(self):
        menu = IsolineSettingsDialog(self.isoline_levels, self.update_isoline_levels)
        menu.exec()

    def open_most_file_selection_menu(self):
        menu = FileSelectionMenuDialog(self.MOST_subprogram.program_file_names, self.MOST_subprogram.load_results)
        menu.exec()

    # def save_most_parameters(self):
    #     self.MOST_subprogram.save_parameters()

    # def calculate_most(self):
    #     self.MOST_subprogram.start_subprogram()

    def show_most_calculation_screen(self):
        calculation_screen = self.MOST_subprogram.get_calculation_screen()
        self.setCentralWidget(calculation_screen)

    def show_loading_screen(self):
        loading_screen = self.MOST_subprogram.get_loading_screen()
        self.setCentralWidget(loading_screen)

    # def load_most_result(self):
    #     self.MOST_subprogram.load_results()

    def parse_initial_data_file(self):  # TODO: change to work for static
        f = open(self.file_names["most_initial"], "r")
        for parameter in self.MOST_subprogram.ini_data_elements.values():
            new_value = f.readline().split()[0]
            parameter.set_current_value(new_value)

    def show_most_result(self):
        self.plot_widget = self.MOST_subprogram.plot_widget

        self.action_heatmap.setEnabled(True)
        self.action_heatmap_with_contour.setEnabled(True)
        self.action_3d_heatmap.setEnabled(True)
        self.action_wave_profile.setEnabled(True)
        self.action_draw_wave_profile.setEnabled(True)

        if (self.MOST_subprogram.marigram_points is not None) & (self.MOST_subprogram.marigram_points != []):
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
        self.action_wave_profile.triggered.connect(
            lambda: self.plot_widget.set_plot("profile")
        )

        self.action_select_points_on_heatmap.setEnabled(True)
        self.action_select_points_on_heatmap.triggered.connect(
            lambda: self.get_marigram_points("heatmap"))
        self.action_draw_wave_profile.triggered.connect(self.draw_wave_profile)

        self.plot_widget.set_plot("heatmap")
        self.setCentralWidget(self.plot_widget.get_widget())

    def get_marigram_points(self, plot_name: str):
        self.plot_widget.set_plot(plot_name)
        plot: HeatmapPlotBuilder = self.plot_widget.get_plot_by_name(plot_name)
        plot.clear_points()
        self.marigram_points = plot.get_input_points()
        plot.draw_points(self.marigram_points)

        self.MOST_subprogram.marigram_points = self.marigram_points

        if self.MOST_subprogram.calculated & (self.MOST_subprogram.marigram_points != []):
            self.action_marigrams.setEnabled(True)

    def plot_marigrams(self):
        self.MOST_subprogram.plot_marigrams()
        self.plot_widget.set_plot("marigrams")

    def draw_source(self):  # TODO
        x = self.MOST_subprogram.ini_data_elements["ellipse center x location"].get_current_value()
        y = self.MOST_subprogram.ini_data_elements["ellipse center y location"].get_current_value()
        x_step = self.MOST_subprogram.ini_data_elements["x-step"].get_current_value()
        y_step = self.MOST_subprogram.ini_data_elements["y-step"].get_current_value()
        self.bottom_plot.draw_source(
            (x, y),
            (self.MOST_subprogram.ini_data_elements["ellipse half x length"].get_current_value() * 2) / x_step,
            (self.MOST_subprogram.ini_data_elements["ellipse half y length"].get_current_value() * 2) / y_step
        )

    def draw_wave_profile(self):
        self.plot_widget.set_plot("heatmap")
        plot: HeatmapPlotBuilder = self.plot_widget.get_plot_by_name("heatmap")
        plot.clear_points()
        self.wave_profile_end_points = plot.get_input_points(n=2)
        # plot.draw_points(self.wave_profile_end_points)
        plot.draw_line(self.wave_profile_end_points[0][0], self.wave_profile_end_points[0][1],
                       self.wave_profile_end_points[1][0], self.wave_profile_end_points[1][1])

        self.wave_profile_data = self.get_wave_profile_on_line()
        self.wave_profile_plot = BarPlotBuilder(self.wave_profile_data, self.save_wave_profile_data)
        self.plot_widget.add_plot("profile", self.wave_profile_plot)

    def update_isoline_levels(self):
        if not self.calculated:
            return

        self.heatmap_with_contour_plot = HeatmapContourPlotBuilder(self.isoline_plot_data,
                                                                   levels=self.isoline_levels,
                                                                   use_default_cmap=False)
        self.plot_widget.add_plot("heatmap contour", self.heatmap_with_contour_plot)
        self.plot_widget.set_plot("heatmap contour")

    def open_save_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                             "All Files (*);;Text Files (*.txt)", options=options)
        return file_name

    def save_wave_profile_data(self):
        file_name = self.open_save_file_dialog()
        if not file_name:
            print("no file name")
            return
        file = open(file_name, "w")
        file.write(np.array2string(self.wave_profile_data, threshold=sys.maxsize))
        file.close()

    def save_marigrams_data(self):
        file_name = self.open_save_file_dialog()
        if not file_name:
            print("no file name")
            return

        file = open(file_name, "w")
        for i in range(len(self.marigram_points)):
            s = str(self.marigram_points[i]) + " " + str(self.marigrams_plot_data[i]) + '\n'
            file.write(s)

        file.close()

    def get_wave_profile_on_line(self):
        x1 = round(self.wave_profile_end_points[0][0])
        y1 = round(self.wave_profile_end_points[0][1])
        x2 = round(self.wave_profile_end_points[1][0])
        y2 = round(self.wave_profile_end_points[1][1])

        x_len = x2 - x1
        y_len = y2 - y1

        data = []

        if abs(x_len) >= abs(y_len):
            x_step = 1
            y_step = y_len / x_len

            if x1 < x2:
                curr_x = x1
                curr_y = y1
                fin = x2
            else:
                curr_x = x2
                curr_y = y2
                fin = x1

            curr = curr_x
        else:
            y_step = 1
            x_step = x_len / y_len

            if y1 < y2:
                curr_x = x1
                curr_y = y1
                fin = y2
            else:
                curr_x = x2
                curr_y = y2
                fin = y1

            curr = curr_y

        while abs(curr - fin) > 0:
            curr_x += x_step
            curr_y += y_step
            curr += 1
            try:
                data.append(self.max_height[round(curr_y), round(curr_x)])
            except IndexError:
                print("ERROR")
                print(self.wave_profile_end_points)
                print("steps: " + str((x_step, y_step)))
                print("lens: " + str((x_len, y_len)))
                print(curr)
                print(curr_x)
                print(curr_y)
                print('\n')
                return self.wave_profile_data

        return data

    def open_static_settings_dialog(self):
        dialog = StaticSettingsDialog(self.static_ini_data_elements, self.static_input_menu_to_elements,
                                      self.run_static)
        dialog.exec()

    def save_static_parameters(self):
        ini_data_file = open(self.file_names["static_initial"], "w")

        for parameter in self.static_ini_data_elements.values():
            input_data = parameter.name + "= " + str(parameter.get_current_value()) + '\n'
            ini_data_file.write(input_data)
        ini_data_file.close()

    def show_static_calculation_screen(self):
        self.calculation_screen = STATICComputationScreen()
        self.setCentralWidget(self.calculation_screen.get_screen())

    def run_static(self):
        self.save_static_parameters()
        self.show_static_calculation_screen()

        commands = static_exe_file_name

        self.process = QProcess()
        self.process.setWorkingDirectory('STATIC\\')
        self.process.finished.connect(self.load_static_result)
        self.process.start(commands)

    def load_static_result(self):
        n1 = self.static_ini_data_elements["N1"].get_current_value()
        m1 = self.static_ini_data_elements["M1"].get_current_value()
        self.static_results = np.zeros((n1, m1), float)
        f = open(static_results_file_name, "rb")
        for j in range(0, m1):
            for i in range(0, n1):
                self.static_results[i][j] = struct.unpack('d', f.read(8))[0]
        self.show_static_result()

    def show_static_result(self):
        self.plot_widget = PlotWidget()

        self.isoline_plot_data = self.static_results

        self.calculated = True

        self.heatmap_plot = HeatmapPlotBuilder(self.static_results)
        self.heatmap_with_contour_plot = HeatmapContourPlotBuilder(self.static_results, levels=self.isoline_levels)
        self.heatmap_3d_plot = Heatmap3DPlotBuilder(self.static_results)

        self.plot_widget.add_plot("heatmap", self.heatmap_plot)
        self.plot_widget.add_plot("heatmap contour", self.heatmap_with_contour_plot)
        self.plot_widget.add_plot("heatmap 3d", self.heatmap_3d_plot)

        self.action_heatmap.setEnabled(True)
        self.action_heatmap_with_contour.setEnabled(True)
        self.action_3d_heatmap.setEnabled(True)
        # self.action_wave_profile_bar_chart.setEnabled(True)
        # self.action_draw_wave_profile.setEnabled(True)

        self.action_heatmap.triggered.connect(
            lambda: self.plot_widget.set_plot("heatmap")
        )
        self.action_3d_heatmap.triggered.connect(
            lambda: self.plot_widget.set_plot("heatmap 3d")
        )
        self.action_heatmap_with_contour.triggered.connect(
            lambda: self.plot_widget.set_plot("heatmap contour")
        )

        # self.action_draw_wave_profile.triggered.connect(self.draw_wave_profile)

        self.plot_widget.set_plot("heatmap")
        self.setCentralWidget(self.plot_widget.get_widget())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MOSTApp()
    window.show()
    app.exec_()
