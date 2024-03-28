import numpy as np

from subprograms.subprogram_interface import SubprogramInterface
from subprograms.static_interface import STATICInterface

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
from datetime import datetime


class MOSTInterface(SubprogramInterface):
    def __init__(self,
                 config_file_name,
                 subprogram_directory,
                 subprogram_with_static_directory,
                 subprogram_file_names,
                 bottom_plot: HeatmapPlotBuilder,
                 save_wave_profile_callback,
                 save_marigrams_callback,
                 show_calculation_screen_callback,
                 show_loading_screen_callback,
                 show_results_callback,
                 static: STATICInterface):
        super().__init__(subprogram_directory, subprogram_file_names)
        self.save_wave_profile = save_wave_profile_callback
        self.save_marigrams = save_marigrams_callback
        self.show_calculation_screen_callback = show_calculation_screen_callback
        self.show_loading_screen_callback = show_loading_screen_callback
        self.show_results_callback = show_results_callback

        self.load_initial_data(config_file_name)

        self.bottom_plot = bottom_plot
        self.plot_widget.add_plot("bottom", self.bottom_plot)

        self.marigram_points = []
        self.marigrams_plot_data = []
        self.marigrams_plot = None

        self.isoline_levels = [0.005, 0.01, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1]

        self.steps_calculated: int = 0
        self.height = None
        self.max_height = None

        self.working_directory_with_static = subprogram_with_static_directory
        self.program_with_static_file_names = super().add_directory_to_file_names(subprogram_with_static_directory,
                                                                                  subprogram_file_names)
        self.static: STATICInterface = static

        self.elliptical_source: bool = True
        self.current_directory = self.working_directory
        self.current_program_file_names = self.program_file_names
        self.x_multiplier: int = 1
        self.y_multiplier: int = 1
        self.static_start_x = None
        self.static_start_y = None

    def load_initial_data(self, config_file_name):
        super().load_initial_data(config_file_name)

        self.input_menu_to_elements = {
            "area": ["x-size", "y-size", "x-step", "y-step", "lowest depth"],
            "size": ["x-size", "y-size", "x-step", "y-step"],
            "source": ["max elevation", "ellipse half x length", "ellipse half y length",
                       "center x", "center y", "lowest depth"],
            "calculation": ["time step", "number of time steps", "number of steps between surface output"]
        }

    def open_file_loading_menu(self):
        menu = FileSelectionMenuDialog(self.program_file_names, self.load_results)
        menu.exec()

    def check_parameters_correctness(self):
        m = self.static.ini_data_elements["M1"].get_current_value()
        n = self.static.ini_data_elements["N1"].get_current_value()
        m_corr = (m * self.x_multiplier) <= self.ini_data_elements["x-size"].get_current_value()
        n_corr = (n * self.y_multiplier) <= self.ini_data_elements["y-size"].get_current_value()
        return m_corr & n_corr

    def save_parameters(self):
        ini_data_file = open(self.current_program_file_names["initial"], "w")

        if not self.elliptical_source:
            self.ini_data_elements["center x"].set_current_value(self.static.ini_data_elements["x"].get_current_value())
            self.ini_data_elements["center y"].set_current_value(self.static.ini_data_elements["y"].get_current_value())
            self.ini_data_elements["max elevation"].set_current_value(0)

        print(">> Saving MOST parameters")
        for i in self.ini_data_elements.values():
            input_data = str(i.get_current_value()) + "  --  " + i.label_text + '\n'
            ini_data_file.write(input_data)

        if not self.elliptical_source:
            print(">> Saving MOST parameters: STATIC source")
            self.print_scaled_static()
            static_x = self.static.ini_data_elements["M1"].get_current_value() * self.x_multiplier
            static_y = self.static.ini_data_elements["N1"].get_current_value() * self.y_multiplier
            input_data = str(static_x) + "  --  statik X size\n" + str(static_y) + "  --  statik Y size\n"
            ini_data_file.write(input_data)

        ini_data_file.close()

    def set_source_to_ellipse(self):
        print(">> Set elliptical source")
        self.elliptical_source = True
        self.current_directory = self.working_directory
        self.current_program_file_names = self.program_file_names
        self.ini_data_elements["max elevation"].reset_value()

    def set_source_to_static(self):
        print(">> Set STATIC source")
        self.elliptical_source = False
        self.current_directory = self.working_directory_with_static
        self.current_program_file_names = self.program_with_static_file_names
        self.ini_data_elements["center x"].set_current_value(self.static.ini_data_elements["x"].get_current_value())
        self.ini_data_elements["center y"].set_current_value(self.static.ini_data_elements["y"].get_current_value())
        self.ini_data_elements["max elevation"].set_current_value(0)
        self.get_static_position()

        if self.static.calculated:
            self.print_scaled_static()

    def get_static_position(self):
        static_grid_x_step = self.static.ini_data_elements["Dx"].get_current_value()
        static_grid_y_step = self.static.ini_data_elements["Dy"].get_current_value()
        most_grid_x_step = self.ini_data_elements["x-step"].get_current_value() / 1000
        most_grid_y_step = self.ini_data_elements["y-step"].get_current_value() / 1000
        self.x_multiplier = static_grid_x_step / most_grid_x_step
        self.y_multiplier = static_grid_y_step / most_grid_y_step

        x = int(self.static.ini_data_elements["x"].get_current_value())
        m = int(self.static.ini_data_elements["M1"].get_current_value() * self.x_multiplier)
        self.static_start_x = x - int(m / 2)
        y = int(self.static.ini_data_elements["y"].get_current_value())
        n = int(self.static.ini_data_elements["N1"].get_current_value() * self.y_multiplier)
        self.static_start_y = y - int(n / 2)

        print(f"start vals: {self.static_start_x}, {self.static_start_y}")

    def print_scaled_static(self):
        # for p in self.static.ini_data_elements.keys():
        #     print(p + " - " + str(self.static.ini_data_elements[p]))
        unscaled_static = np.transpose(self.static.result)
        n = self.static.ini_data_elements["N1"].get_current_value()
        m = self.static.ini_data_elements["M1"].get_current_value()

        x_step = 0
        y_step = 0

        f_out = open("subprograms\\MOST_with_STATIC\\static.txt", "w")
        for j in range(0, n):
            while y_step < self.y_multiplier:
                for i in range(0, m):
                    while x_step < self.x_multiplier:
                        f_out.write(format(unscaled_static[i][j], '.3f') + " ")
                        x_step += 1
                    x_step = 0
                f_out.write("\n")
                y_step += 1
            y_step = 0
        f_out.close()

        # f_out = open("subprograms\\MOST_with_STATIC\\static.txt", "w")
        # for j in range(0, n):
        #     for i in range(0, m):
        #         f_out.write(format(unscaled_static[i][j], '.3f') + " ")
        #     f_out.write("\n")
        # f_out.close()

    def start_subprogram(self, error_callback):
        # TODO: это должно работать, только если программа запущена в первый раз, или если данные изменились
        if not self.check_parameters_correctness():
            error_callback()
            return
        self.show_calculation_screen_callback()
        self.save_parameters()

        if not self.elliptical_source:
            print(">> Starting MOST with STATIC source")
        else:
            print(">> Starting MOST with elliptical source")

        commands = self.current_program_file_names["exe"]

        self.process = QProcess()
        self.process.setWorkingDirectory(self.current_directory)
        self.process.readyReadStandardOutput.connect(self.update_progress)
        self.process.finished.connect(self.load_results)
        self.process.start(commands)

        time = datetime.now().strftime("%H:%M:%S:%f")
        print(f">> Started MOST ({commands})  {time}")

    def update_progress(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8").strip()
        if stdout != '':
            self.steps_calculated = int(stdout)
            self.calculation_screen.update_progress_bar(self.steps_calculated)

    def get_calculation_screen(self):
        steps = self.ini_data_elements["number of time steps"].get_current_value()
        self.calculation_screen = MOSTComputationScreen(steps)

        return self.calculation_screen.get_screen()

    def parse_parameters(self):
        f = open(self.program_file_names["initial"], "r")
        for parameter in self.ini_data_elements.values():
            new_value = f.readline().split()[0]
            parameter.set_current_value(new_value)

    def load_results(self):
        print(f">> MOST calculation finished ({self.steps_calculated} steps total)")
        if self.steps_calculated < self.ini_data_elements["number of time steps"].get_current_value():
            print(">> MOST SUBPROGRAM ERROR: only ", end='')
            print(str(self.steps_calculated) + " steps calculated instead of ", end='')
            print(str(self.ini_data_elements["number of time steps"].get_current_value()))
        # self.marigram_points = []
        self.show_loading_screen_callback()

        self.parse_parameters()

        self.thread = QThread()
        self.loader = FileLoader(
            [self.current_program_file_names["max_height"], self.current_program_file_names["height"]])
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

    def visualise_results(self):
        # self.bottom_plot = HeatmapPlotBuilder(self.bottom_map)
        # self.plot_widget = PlotWidget({"bottom": self.bottom_plot})
        # self.draw_source()
        self.plot_widget = PlotWidget()

        loaded_files = self.loader.get_results()
        # if self.program_file_names["initial"] != self.program_file_names["default_initial"]:
        #     self.parse_parameters()
        self.max_height = loaded_files[self.current_program_file_names["max_height"]]
        self.height = loaded_files[self.current_program_file_names["height"]]

        self.isoline_plot_data = self.max_height
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

    def draw_source(self, plot: HeatmapPlotBuilder):
        if self.elliptical_source:
            self.draw_elliptical_source(plot)
        else:
            # pass
            self.draw_static_source(plot)

    def draw_elliptical_source(self, plot: HeatmapPlotBuilder):
        plot.clear_contour()
        plot.clear_rectangle()
        x = self.ini_data_elements["center x"].get_current_value()
        y = self.ini_data_elements["center y"].get_current_value()
        x_step = self.ini_data_elements["x-step"].get_current_value()
        y_step = self.ini_data_elements["y-step"].get_current_value()
        plot.draw_elliptical_source(
            (x, y),
            (self.ini_data_elements["ellipse half x length"].get_current_value() * 2) / x_step,
            (self.ini_data_elements["ellipse half y length"].get_current_value() * 2) / y_step
        )

    def draw_static_source(self, plot: HeatmapPlotBuilder):
        plot.clear_contour()
        plot.clear_rectangle()
        z = np.loadtxt("subprograms\\MOST_with_STATIC\\static.txt")

        m = int(self.static.ini_data_elements["M1"].get_current_value() * self.x_multiplier)
        n = int(self.static.ini_data_elements["N1"].get_current_value() * self.y_multiplier)

        x_arr = list(range(self.static_start_x, self.static_start_x + m))
        y_arr = list(range(self.static_start_y, self.static_start_y + n))
        levels = self.static.isoline_levels
        plot.draw_contour(x_arr, y_arr, z, levels)
        plot.draw_rectangle(self.static_start_x - 1, self.static_start_y - 1, n, m)

    def plot_marigrams(self):
        x = []
        time_step = self.ini_data_elements["time step"].get_current_value()
        steps_total = self.ini_data_elements["number of time steps"].get_current_value()
        steps_between = self.ini_data_elements[
            "number of steps between surface output"].get_current_value()
        for i in range(0, steps_total, steps_between):
            x.append(i * time_step)

        print(">>> Marigram points:")
        for point in self.marigram_points:
            print("     " + str(point))
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

    def most_coordinates_to_static_coordinates(self, most_x, most_y):
        print(f" input from MOST: {most_x}, {most_y}")

        m = int(self.static.ini_data_elements["M1"].get_current_value())
        n = int(self.static.ini_data_elements["N1"].get_current_value() * self.y_multiplier)

        static_x = (most_x - self.static_start_x) / self.x_multiplier
        static_y = (most_y - self.static_start_y) / self.y_multiplier

        if most_x < self.static_start_x:
            static_x = 0
        if most_x > self.static_start_x + (m * self.x_multiplier):
            static_x = m - 1
        if most_y < self.static_start_y:
            static_y = 0
        if most_y > self.static_start_y + (n * self.y_multiplier):
            static_y = n - 1

        print(f" result on STATIC: {static_x}, {static_y}")
        return static_x, static_y
