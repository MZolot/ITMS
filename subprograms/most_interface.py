from subprograms.subprogram_interface import SubprogramInterface

from ui_elements.load_data_file_selection_dialog import *
from ui_elements.waiting_screens import *
from file_loader import *
from plots.stacked_plots_widget import PlotWidget
from plots.matplotlib_plot_builder import (HeatmapPlotBuilder,
                                           HeatmapContourPlotBuilder,
                                           Heatmap3DPlotBuilder,
                                           BarPlotBuilder,
                                           MarigramsPlotBuilder)
from PyQt5.QtCore import QProcess, QThread

import numpy as np


class MOSTInterface(SubprogramInterface):
    def __init__(self,
                 config_file_name,
                 subprogram_file_names,
                 exe_file_name,
                 bottom_profile_file_name,
                 save_wave_profile_callback,
                 save_marigrams_callback,
                 show_calculation_screen_callback,
                 show_loading_screen_callback,
                 show_results_callback):
        super().__init__()
        self.program_file_names = subprogram_file_names
        self.exe_file_name = exe_file_name
        self.save_wave_profile = save_wave_profile_callback
        self.save_marigrams = save_marigrams_callback
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
        self.marigrams_plot_data = []
        self.marigrams_plot = None

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
        steps = self.ini_data_elements["number of time steps"].get_current_value()
        self.calculation_screen = MOSTComputationScreen(steps)

        return self.calculation_screen.get_screen()

    def parse_parameters(self):
        pass

    def load_results(self):
        # self.marigram_points = []
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

    def plot_marigrams(self):
        x = []
        time_step = self.ini_data_elements["time step"].get_current_value()
        steps_total = self.ini_data_elements["number of time steps"].get_current_value()
        steps_between = self.ini_data_elements[
            "number of steps between surface output"].get_current_value()
        for i in range(0, steps_total, steps_between):
            x.append(i * time_step)

        print("marigram points:")
        print(self.marigram_points)
        self.marigrams_plot_data = []
        n_marigrams = len(self.marigram_points)
        length = len(self.height)
        y_size = self.ini_data_elements["y-size"].get_current_value()

        for i in range(n_marigrams):
            point = self.marigram_points[i]
            start_y = int(point[1])
            if start_y == y_size:
                start_y = y_size - 1
            selected = self.height[[y for y in range(start_y, length, y_size)], int(point[0])]
            self.marigrams_plot_data.append(selected.tolist())

        self.marigrams_plot = MarigramsPlotBuilder(x, self.marigrams_plot_data, self.marigram_points,
                                                   self.save_marigrams)
        self.plot_widget.add_plot("marigrams", self.marigrams_plot)
        self.plot_widget.set_plot("marigrams")
