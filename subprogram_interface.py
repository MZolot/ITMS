from ui_elements.load_data_file_selection_dialog import *
from ui_elements.input_dialog import InputMenuDialog, SourceMenuDialog
from ui_elements.waiting_screens import *
from ui_elements.isoline_settings_dialog import IsolineSettingsDialog
from ui_elements.static_settings_dialog import StaticSettingsDialog
from data_entry import DataEntry
from file_loader import *
from plots.stacked_plots_widget import PlotWidget
from plots.matplotlib_plot_builder import (HeatmapPlotBuilder,
                                           HeatmapContourPlotBuilder,
                                           Heatmap3DPlotBuilder,
                                           BarPlotBuilder,
                                           MarigramsPlotBuilder)

from PyQt5 import QtWidgets
from PyQt5.QtCore import QProcess, QThread

import numpy as np

import json
import struct


class SubprogramInterface:
    def __init__(self):
        self.ini_data_elements: dict[str, DataEntry] = {}
        self.input_menu_to_elements: dict[str, str] = {}

        self.plot_widget = PlotWidget()
        self.process: QProcess = QProcess()

        self.wave_profile_end_points = []
        self.bar_chart_data = None
        self.thread = None
        self.loader = None
        self.calculation_screen = None

        self.heatmap_plot = None
        self.heatmap_with_contour_plot = None
        self.heatmap_3d_plot = None
        self.wave_profile_plot = None

        self.calculated = False

    def load_initial_data(self, config_file_name):
        self.ini_data_elements = {}
        with open(config_file_name, 'r') as j:
            from_json = json.loads(j.read())
            for element in from_json:
                self.ini_data_elements[element["name"]] = DataEntry(element["name"], element["label_text"],
                                                                    element["default_value"], element["unit"],
                                                                    element["is_float"])

    def save_parameters(self): pass

    def start_subprogram(self): pass

    def show_waiting_screen(self): pass

    def parse_parameters(self): pass

    def load_results(self): pass

    def visualise_results(self): pass


class MOSTInterface(SubprogramInterface):
    def __init__(self,
                 config_file_name,
                 subprogram_file_names,
                 exe_file_name,
                 bottom_profile_file_name,
                 save_wave_profile_callback,
                 show_calculation_screen_callback,
                 show_loading_screen_callback,
                 show_results_callback):
        super().__init__()
        self.program_file_names = subprogram_file_names
        self.exe_file_name = exe_file_name
        self.save_wave_profile = save_wave_profile_callback
        self.show_calculation_screen_callback = show_calculation_screen_callback
        self.show_loading_screen_callback = show_loading_screen_callback
        self.show_results_callback = show_results_callback

        print(subprogram_file_names)

        self.load_initial_data(config_file_name)

        self.bottom_profile = np.loadtxt(bottom_profile_file_name)
        self.bottom_map = np.transpose(np.tile(self.bottom_profile, (1500, 1)))

        # Пока не будет понятно, что должно быть на главном экране при запуске
        self.bottom_plot = HeatmapPlotBuilder(self.bottom_map)
        self.draw_source()
        self.plot_widget.add_plot("bottom", self.bottom_plot)

        self.marigram_points = []
        self.isoline_levels = [0.005, 0.01, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1]

        self.height = None
        self.max_height = None

    def load_initial_data(self, config_file_name):
        super().load_initial_data(config_file_name)

        self.input_menu_to_elements = {
            "area": ["x-size", "y-size", "x-step", "y-step", "lowest depth"],
            "size": ["x-size", "y-size"],
            "steps": ["x-step", "y-step"],
            "source": ["max elevation at source", "ellipse half x length", "ellipse half y length",
                       "ellipse center x location", "ellipse center y location", "lowest depth"],
            "calculation": ["time step", "number of time steps", "number of steps between surface output"]
        }

    def open_file_loading_menu(self):
        menu = FileSelectionMenuDialog(self.program_file_names, self.load_results)
        menu.exec()

    def save_parameters(self):
        ini_data_file = open(self.program_file_names["initial"], "w")

        for i in self.ini_data_elements.values():
            input_data = str(i.get_current_value()) + "  --  " + i.label_text + '\n'
            ini_data_file.write(input_data)
        ini_data_file.close()

    def start_subprogram(self):
        # TODO: это должно работать, только если программа запущена в первый раз, или если данные изменились
        self.save_parameters()
        self.show_calculation_screen_callback()
        # self.show_waiting_screen()

        commands = self.exe_file_name

        self.process = QProcess()
        self.process.setWorkingDirectory('MOST\\')
        self.process.readyReadStandardOutput.connect(self.update_progress)
        self.process.finished.connect(self.load_results)
        self.process.start(commands)

    def update_progress(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8").strip()
        if stdout != '':
            self.calculation_screen.update_progress_bar(int(stdout))

    def show_waiting_screen(self):
        steps = self.ini_data_elements["number of time steps"].get_current_value()
        self.calculation_screen = MOSTComputationScreen(steps)
        # self.setCentralWidget(self.calculation_screen.get_screen())

    def get_calculation_screen(self):
        if not self.calculation_screen:
            steps = self.ini_data_elements["number of time steps"].get_current_value()
            self.calculation_screen = MOSTComputationScreen(steps)

        return self.calculation_screen.get_screen()

    def parse_parameters(self):
        pass

    def load_results(self):
        self.marigram_points = []
        # self.show_loading_screen()
        self.show_loading_screen_callback()

        self.thread = QThread()
        self.loader = FileLoader([self.program_file_names["max_height"], self.program_file_names["height"]])
        self.loader.moveToThread(self.thread)
        self.thread.started.connect(self.loader.run)
        self.loader.finished.connect(self.thread.quit)
        self.loader.finished.connect(self.loader.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.visualise_results)
        self.thread.start()

    def get_loading_screen(self):
        loading_screen = LoadingScreen()
        return loading_screen.get_screen()
        # self.setCentralWidget(loading_screen.get_screen())

    def visualise_results(self):
        self.bottom_plot = HeatmapPlotBuilder(self.bottom_map)
        self.draw_source()
        self.plot_widget = PlotWidget({"bottom": self.bottom_plot})

        loaded_files = self.loader.get_results()
        # if self.program_file_names["initial"] != self.program_file_names["default_initial"]:
        #     self.parse_parameters()
        self.max_height = loaded_files[self.program_file_names["max_height"]]
        self.height = loaded_files[self.program_file_names["height"]]

        self.bar_chart_data = self.max_height[3]

        self.calculated = True

        self.heatmap_plot = HeatmapPlotBuilder(self.max_height, default_cmap=False)
        self.heatmap_with_contour_plot = HeatmapContourPlotBuilder(self.max_height,
                                                                   levels=self.isoline_levels,
                                                                   use_default_cmap=False)
        self.heatmap_3d_plot = Heatmap3DPlotBuilder(self.max_height)
        self.wave_profile_plot = BarPlotBuilder(self.bar_chart_data, self.save_wave_profile)

        self.plot_widget.add_plot("heatmap", self.heatmap_plot)
        self.plot_widget.add_plot("heatmap contour", self.heatmap_with_contour_plot)
        self.plot_widget.add_plot("heatmap 3d", self.heatmap_3d_plot)
        self.plot_widget.add_plot("profile", self.wave_profile_plot)

        self.show_results_callback()
        # self.action_heatmap.setEnabled(True)
        # self.action_heatmap_with_contour.setEnabled(True)
        # self.action_3d_heatmap.setEnabled(True)
        # self.action_wave_profile_bar_chart.setEnabled(True)
        # self.action_draw_wave_profile.setEnabled(True)

        # if self.marigram_points:
        #     self.action_marigrams.setEnabled(True)

        # self.action_heatmap.triggered.connect(
        #     lambda: self.plot_widget.set_plot("heatmap")
        # )
        # self.action_3d_heatmap.triggered.connect(
        #     lambda: self.plot_widget.set_plot("heatmap 3d")
        # )
        # self.action_heatmap_with_contour.triggered.connect(
        #     lambda: self.plot_widget.set_plot("heatmap contour")
        # )
        # self.action_wave_profile_bar_chart.triggered.connect(
        #     lambda: self.plot_widget.set_plot("bar")
        # )

        # self.action_select_points_on_heatmap.setEnabled(True)
        # self.action_select_points_on_heatmap.triggered.connect(
        #     lambda: self.get_marigram_points("heatmap"))
        # self.action_draw_wave_profile.triggered.connect(self.draw_wave_profile)

        # self.plot_widget.set_plot("heatmap")
        # self.setCentralWidget(self.plot_widget.get_widget())

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


class STATICInterface(SubprogramInterface):
    def __init__(self,
                 config_file_name,
                 subprogram_file_names,
                 exe_file_name,
                 save_wave_profile_callback,
                 show_calculation_screen_callback,
                 show_loading_screen_callback,
                 show_results_callback):
        super().__init__()
        self.program_file_names = subprogram_file_names
        self.exe_file_name = exe_file_name
        self.save_wave_profile = save_wave_profile_callback
        self.show_calculation_screen_callback = show_calculation_screen_callback
        self.show_loading_screen_callback = show_loading_screen_callback
        self.show_results_callback = show_results_callback

        self.load_initial_data(config_file_name)

        self.isoline_levels = [-0.5, -0.4, -0.3, -0.2, -0.1, -0.05, 0.0, 0.01, 0.05, 0.1, 0.4]

        self.result = None

    def load_initial_data(self, config_file_name):
        super().load_initial_data(config_file_name)

        self.input_menu_to_elements = {
            "fault": ["L", "W", "DE", "LA", "TE", "D0", "h0"],
            "calculation": ["N1", "M1", "Dx", "Dy", "jj", "kk"]
        }

    def save_parameters(self):
        ini_data_file = open(self.program_file_names["initial"], "w")

        for parameter in self.ini_data_elements.values():
            input_data = parameter.name + "= " + str(parameter.get_current_value()) + '\n'
            ini_data_file.write(input_data)
        ini_data_file.close()

    def start_subprogram(self):
        self.save_parameters()
        self.show_calculation_screen_callback()
        # self.show_waiting_screen()

        commands = self.exe_file_name

        self.process = QProcess()
        self.process.setWorkingDirectory('STATIC\\')
        self.process.finished.connect(self.load_results)
        self.process.start(commands)

    def show_waiting_screen(self):
        self.calculation_screen = STATICComputationScreen()
        # self.setCentralWidget(self.calculation_screen.get_screen())

    def parse_parameters(self):
        pass

    def load_results(self):
        self.show_loading_screen_callback()

        n1 = self.ini_data_elements["N1"].get_current_value()
        m1 = self.ini_data_elements["M1"].get_current_value()
        self.result = np.zeros((n1, m1), float)
        f = open(self.program_file_names["result"], "rb")
        for j in range(0, m1):
            for i in range(0, n1):
                self.result[i][j] = struct.unpack('d', f.read(8))[0]
        self.visualise_results()

    def visualise_results(self):
        self.plot_widget = PlotWidget()

        self.calculated = True

        self.heatmap_plot = HeatmapPlotBuilder(self.result)
        self.heatmap_with_contour_plot = HeatmapContourPlotBuilder(self.result, levels=self.isoline_levels)
        self.heatmap_3d_plot = Heatmap3DPlotBuilder(self.result)

        self.plot_widget.add_plot("heatmap", self.heatmap_plot)
        self.plot_widget.add_plot("heatmap contour", self.heatmap_with_contour_plot)
        self.plot_widget.add_plot("heatmap 3d", self.heatmap_3d_plot)

        self.show_results_callback()
