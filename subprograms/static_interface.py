from subprograms.subprogram_interface import SubprogramInterface

from ui_elements.waiting_screens import *
from plots.stacked_plots_widget import PlotWidget
from plots.matplotlib_plot_builder import (HeatmapPlotBuilder,
                                           HeatmapContourPlotBuilder,
                                           Heatmap3DPlotBuilder)

from PyQt5.QtCore import QProcess

import numpy as np

import struct


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

    def get_calculation_screen(self):
        self.calculation_screen = STATICComputationScreen()
        return self.calculation_screen.get_screen()

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

        self.isoline_plot_data = self.result

        self.heatmap_plot = HeatmapPlotBuilder(self.result, default_cmap=True)
        self.heatmap_with_contour_plot = HeatmapContourPlotBuilder(self.result,
                                                                   levels=self.isoline_levels,
                                                                   use_default_cmap=False)
        self.heatmap_3d_plot = Heatmap3DPlotBuilder(self.result)

        self.plot_widget.add_plot("heatmap", self.heatmap_plot)
        self.plot_widget.add_plot("heatmap contour", self.heatmap_with_contour_plot)
        self.plot_widget.add_plot("heatmap 3d", self.heatmap_3d_plot)

        self.plot_widget.set_plot("heatmap")

        self.show_results_callback()
