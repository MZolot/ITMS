import ui_elements.qt_designer_ui.main_ui as main_ui
import ui_elements.qt_designer_ui.marigrams_info_message_ui as marigrams_info_ui
from ui_elements.input_dialog import *
from ui_elements.isoline_settings_dialog import IsolineSettingsDialog
from ui_elements.load_data_file_selection_dialog import FileSelectionMenuDialog
from ui_elements.static_settings_dialog import StaticSettingsDialog
from ui_elements.static_profile_dialog import StaticProfileDialog
from ui_elements.most_results_dialog import *

from subprograms.most_interface import MOSTInterface
from subprograms.static_interface import STATICInterface

from plots.stacked_plots_widget import PlotWidget
from plots.matplotlib_plot_builder import (HeatmapPlotBuilder,
                                           HeatmapContourPlotBuilder,
                                           BarPlotBuilder,
                                           CommonPlotBuilder)

from PyQt5 import QtWidgets

import numpy as np

import sys
from datetime import datetime

most_config_file_name = "resources/most_parameters_config.json"
most_ini_data_default_file_name = "subprograms/MOST/ini_data.txt"
most_exe_file_name = "subprograms/MOST/wave_1500x900_01.exe"

bottom_profile_file_name = "subprograms/MOST/koryto_profile.txt"

height_default_file_name = "subprograms/MOST/heigh.dat"
max_height_default_file_name = "subprograms/MOST/maxheigh.dat"

static_config_file_name = "resources/static_parameters_config.json"
static_ini_data_default_file_name = "subprograms/STATIC/static_param.txt"
static_exe_file_name = "subprograms/STATIC/Static.exe"
static_results_file_name = "subprograms/STATIC/static.bin"


class MOSTApp(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.bottom_profile = np.loadtxt(bottom_profile_file_name)
        self.bottom_map = np.transpose(np.tile(self.bottom_profile, (1500, 1)))
        # self.bottom_map = np.tile(self.bottom_profile, (1500, 1))
        self.bottom_plot = HeatmapContourPlotBuilder(self.bottom_map, 10)

        self.static_files = {
            "exe": "Static.exe",
            "initial": "static_param.txt",
            "result": "static.bin"
        }

        self.STATIC_subprogram = STATICInterface(config_file_name=static_config_file_name,
                                                 subprogram_directory="subprograms\\STATIC",
                                                 subprogram_file_names=self.static_files,
                                                 bottom_plot=self.bottom_plot,
                                                 save_wave_profile_callback=self.save_wave_profile_data,
                                                 show_calculation_screen_callback=self.show_static_calculation_screen,
                                                 show_loading_screen_callback=self.show_loading_screen,
                                                 show_results_callback=self.show_static_results)

        self.most_files = {
            "exe": "wave_1500x900_08.exe",
            "initial": "ini_data.txt",
            "height": "heigh.dat",
            "max_height": "maxheigh.dat"
        }

        self.MOST_subprogram = MOSTInterface(config_file_name=most_config_file_name,
                                             subprogram_directory="subprograms\\MOST",
                                             subprogram_file_names=self.most_files,
                                             bottom_plot=self.bottom_plot,
                                             save_wave_profile_callback=self.save_wave_profile_data,
                                             save_marigrams_callback=self.save_marigrams_data,
                                             show_calculation_screen_callback=self.show_most_calculation_screen,
                                             show_loading_screen_callback=self.show_loading_screen,
                                             show_results_callback=self.show_most_result,
                                             static=self.STATIC_subprogram)

        self.plot_widget = PlotWidget({"bottom": self.MOST_subprogram.bottom_plot})

        # self.MOST_subprogram.draw_elliptical_source()

        self.static_settings_dialog = None
        self.static_profile_dialog = None

        self.wave_profile_end_points = []
        self.wave_profile_data = None

        self.setupUi(self)
        self.set_actions()

        self.setCentralWidget(self.plot_widget.get_widget())

    def set_actions(self):
        self.action_size.triggered.connect(
            lambda: self.open_most_input_menu(self.MOST_subprogram.input_menu_to_elements["size"],
                                              "Size parameters", "size"))
        self.action_elliptical_source.triggered.connect(
            lambda: self.open_most_input_menu(self.MOST_subprogram.input_menu_to_elements["source"],
                                              "Elliptical source parameters", "source"))
        self.action_calculation_parameters.triggered.connect(
            lambda: self.open_most_input_menu(self.MOST_subprogram.input_menu_to_elements["calculation"],
                                              "Calculation parameters", "calculation"))
        self.action_calculate_most.triggered.connect(
            lambda: self.MOST_subprogram.start_subprogram(self.show_error_message))

        self.action_show_area.triggered.connect(
            lambda: self.plot_widget.set_plot("bottom"))

        self.action_select_points_on_area.triggered.connect(
            lambda: self.get_marigram_points("bottom"))
        self.action_marigrams.triggered.connect(self.plot_marigrams)

        self.action_load_existing_results.triggered.connect(self.open_most_file_selection_menu)

        self.action_set_contour_lines_levels_for_MOST.triggered.connect(self.open_isoline_settings_menu_for_most)
        self.action_set_contour_lines_levels_for_STATIC.triggered.connect(self.open_isoline_settings_menu_for_static)

        self.action_static_source.triggered.connect(self.open_static_settings_dialog)
        self.action_show_static.triggered.connect(self.open_static_result_dialog)
        self.action_draw_static_profile.triggered.connect(self.open_static_profile_dialog)

        # ============== Results interaction =================

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
        #     lambda: self.plot_widget.set_plot("profile")
        # )

        self.action_heatmap.triggered.connect(
            lambda: self.open_most_results_dialog("heatmap", "Heatmap")
        )
        self.action_3d_heatmap.triggered.connect(
            lambda: self.open_most_results_dialog("heatmap 3d", "3D Heatmap")
        )
        self.action_heatmap_with_contour.triggered.connect(
            lambda: self.open_most_results_dialog("heatmap contour", "Heatmap with contour lines")
        )
        self.action_wave_profile_bar_chart.triggered.connect(
            lambda: self.open_most_results_dialog("profile", "Wave profile")
        )

        self.action_select_points_on_heatmap.triggered.connect(
            lambda: self.get_marigram_points("heatmap"))

        # self.action_draw_wave_profile.triggered.connect(self.draw_wave_profile_on_most)

    def open_most_input_menu(self, element_names, title, menu_type=""):
        elements = []
        for n in element_names:
            elements.append(self.MOST_subprogram.ini_data_elements[n])
        if menu_type == "source":
            menu = InputMenuDialogWithCallbacks(elements, title,
                                                [self.MOST_subprogram.set_source_to_ellipse,
                                                 lambda: self.MOST_subprogram.draw_source(self.bottom_plot)])
        elif menu_type == "size":
            menu = InputMenuDialogWithCallbacks(elements, title,
                                                [lambda: self.MOST_subprogram.draw_source(self.bottom_plot)])
        elif menu_type == "calculation":
            menu = CalculationMenuDialog(elements, title,
                                         [lambda: self.MOST_subprogram.start_subprogram(self.show_error_message)])
        else:
            menu = InputMenuDialog(elements, title)
        menu.exec()

    def open_isoline_settings_menu_for_most(self):
        menu = IsolineSettingsDialog(self.MOST_subprogram.isoline_levels, self.update_isoline_levels_for_most)
        menu.exec()

    def open_isoline_settings_menu_for_static(self):
        menu = IsolineSettingsDialog(self.STATIC_subprogram.isoline_levels, self.update_isoline_levels_for_static)
        menu.exec()

    def open_most_file_selection_menu(self):
        menu = FileSelectionMenuDialog(self.MOST_subprogram.program_file_names, self.MOST_subprogram.load_results)
        menu.exec()

    def show_most_calculation_screen(self):
        calculation_screen = self.MOST_subprogram.get_calculation_screen()
        self.setCentralWidget(calculation_screen)

    def show_loading_screen(self):
        loading_screen = self.MOST_subprogram.get_loading_screen()
        self.setCentralWidget(loading_screen)

    # def parse_initial_data_file(self):  # TODO: change to work for static
    def show_most_result(self):
        self.plot_widget = self.MOST_subprogram.plot_widget
        self.bottom_plot = HeatmapContourPlotBuilder(self.bottom_map, 10)
        self.plot_widget.add_plot("bottom", self.bottom_plot)
        self.MOST_subprogram.draw_source(self.bottom_plot)

        if self.STATIC_subprogram.calculated:
            self.plot_widget.add_plot("static", self.STATIC_subprogram.heatmap_plot)

        self.action_heatmap.setEnabled(True)
        self.action_heatmap_with_contour.setEnabled(True)
        self.action_3d_heatmap.setEnabled(True)
        self.action_wave_profile_bar_chart.setEnabled(True)
        self.action_draw_wave_profile.setEnabled(True)

        if (self.MOST_subprogram.marigram_points is not None) & (self.MOST_subprogram.marigram_points != []):
            self.action_marigrams.setEnabled(True)

        # self.action_select_points_on_heatmap.setEnabled(True)

        # self.plot_widget.set_plot("heatmap")
        # self.setCentralWidget(self.plot_widget.get_widget())

        self.plot_widget.set_plot("bottom")
        self.setCentralWidget(self.plot_widget.get_widget())
        self.open_most_results_dialog("heatmap", "Heatmap")

    def open_most_results_dialog(self, plot_name: str, dialog_title):
        plot = self.MOST_subprogram.results_name_to_plot[plot_name]
        plot.update_canvas()
        if plot_name == "heatmap":
            dialog = HeatmapDialog(self, dialog_title, plot, self.show_most_wave_profile)
        else:
            dialog = PlotDialog(self, dialog_title, plot)
        # dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        dialog.show()

    def open_static_result_dialog(self):
        plot = self.STATIC_subprogram.heatmap_with_contour_plot
        plot.update_canvas()
        dialog = PlotDialog(self, "STATIC heatmap", plot)
        # dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        dialog.show()

    def get_marigram_points(self, plot_name: str):
        self.plot_widget.set_plot(plot_name)
        plot: HeatmapPlotBuilder = self.plot_widget.get_plot_by_name(plot_name)
        plot.clear_points()
        plot.clear_line()

        dialog = MarigramsInfoDialog(self)
        dialog.move(self.pos() + self.centralWidget().pos() * 5)
        dialog.show()

        marigram_points = plot.get_input_points()
        plot.draw_points(marigram_points)

        self.MOST_subprogram.marigram_points = marigram_points

        if self.MOST_subprogram.calculated & (self.MOST_subprogram.marigram_points != []):
            self.action_marigrams.setEnabled(True)

        dialog.close()

    def plot_marigrams(self):
        self.MOST_subprogram.plot_marigrams()
        self.plot_widget.set_plot("marigrams")

    # def draw_wave_profile_on_most(self):
    #     self.plot_widget.set_plot("heatmap")
    #     plot = self.plot_widget.get_plot_by_name("heatmap")
    #
    #     plot.clear_points()  # убирает мареограммы
    #     plot.clear_line()
    #     self.wave_profile_end_points = plot.get_input_points(n=2)
    #     if len(self.wave_profile_end_points) < 2:
    #         return
    #
    #     plot.draw_line(self.wave_profile_end_points[0][0], self.wave_profile_end_points[0][1],
    #                    self.wave_profile_end_points[1][0], self.wave_profile_end_points[1][1])
    #
    #     self.wave_profile_data = self.get_wave_profile_on_line(self.wave_profile_end_points,
    #                                                            self.MOST_subprogram.max_height)
    #     wave_profile_plot = BarPlotBuilder(self.wave_profile_data, self.save_wave_profile_data)
    #
    #     # wave_profile_plot = self.get_wave_profile(plot, self.MOST_subprogram.max_height)
    #     self.plot_widget.add_plot("profile", wave_profile_plot)

    def show_most_wave_profile(self, heatmap_dialog, wave_profile_end_points):
        self.wave_profile_end_points = wave_profile_end_points
        self.wave_profile_data = self.get_wave_profile_on_line(self.wave_profile_end_points,
                                                               self.MOST_subprogram.max_height)
        wave_profile_plot = BarPlotBuilder(self.wave_profile_data, self.save_wave_profile_data)

        dialog = PlotDialog(heatmap_dialog, "Wave profile", wave_profile_plot)
        dialog.show()

    def draw_wave_profile_on_static(self, draw_profile_callback):
        self.plot_widget.set_plot("bottom")
        plot = self.plot_widget.get_plot_by_name("bottom")

        plot.clear_points()
        plot.clear_line()
        wave_profile_end_points = plot.get_input_points(n=2)
        print(wave_profile_end_points)
        if len(wave_profile_end_points) < 2:
            return
        # plot.draw_points(self.wave_profile_end_points)
        plot.draw_line(wave_profile_end_points[0][0], wave_profile_end_points[0][1],
                       wave_profile_end_points[1][0], wave_profile_end_points[1][1])

        point1 = self.MOST_subprogram.most_coordinates_to_static_coordinates(wave_profile_end_points[0][0],
                                                                             wave_profile_end_points[0][1])
        point2 = self.MOST_subprogram.most_coordinates_to_static_coordinates(wave_profile_end_points[1][0],
                                                                             wave_profile_end_points[1][1])
        wave_profile_end_points = [point1, point2]

        wave_profile_data = self.get_wave_profile_on_line(wave_profile_end_points, self.STATIC_subprogram.result)
        wave_profile_plot = CommonPlotBuilder(wave_profile_data)

        # wave_profile_plot = self.get_wave_profile(plot, self.STATIC_subprogram.result, True)
        draw_profile_callback(wave_profile_plot)

    def get_wave_profile_on_line(self, wave_profile_end_points, data_source):
        x1 = round(wave_profile_end_points[0][0])
        y1 = round(wave_profile_end_points[0][1])
        x2 = round(wave_profile_end_points[1][0])
        y2 = round(wave_profile_end_points[1][1])

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
                data.append(data_source[round(curr_y), round(curr_x)])
            except IndexError:
                print("ERROR")
                print(wave_profile_end_points)
                print("steps: " + str((x_step, y_step)))
                print("lens: " + str((x_len, y_len)))
                print(curr)
                print(curr_x)
                print(curr_y)
                print('\n')
                return self.wave_profile_data

        return data

    def update_isoline_levels_for_most(self):
        if not self.MOST_subprogram.calculated:
            return

        heatmap_with_contour_plot = HeatmapContourPlotBuilder(self.MOST_subprogram.isoline_plot_data,
                                                              levels=self.MOST_subprogram.isoline_levels,
                                                              use_default_cmap=False)

        self.MOST_subprogram.results_name_to_plot["heatmap contour"] = heatmap_with_contour_plot
        # subprogram.plot_widget.add_plot("heatmap contour", subprogram.heatmap_with_contour_plot)
        # subprogram.plot_widget.set_plot("heatmap contour")

    def update_isoline_levels_for_static(self):
        if not self.STATIC_subprogram.calculated:
            return

        self.STATIC_subprogram.heatmap_with_contour_plot = HeatmapContourPlotBuilder(
            self.STATIC_subprogram.isoline_plot_data,
            levels=self.STATIC_subprogram.isoline_levels,
            use_default_cmap=False)

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

        marigram_points = self.MOST_subprogram.marigram_points
        file = open(file_name, "w")
        for i in range(len(marigram_points)):
            s = str(marigram_points[i]) + " " + str(self.MOST_subprogram.marigrams_plot_data[i]) + '\n'
            file.write(s)

        file.close()

    def open_static_settings_dialog(self):
        self.static_settings_dialog = StaticSettingsDialog(self,
                                                           self.STATIC_subprogram.ini_data_elements,
                                                           self.STATIC_subprogram.input_menu_to_elements,
                                                           [
                                                               # self.MOST_subprogram.set_source_to_static,
                                                               self.STATIC_subprogram.start_subprogram
                                                           ])

        self.static_settings_dialog.move(self.pos() + self.centralWidget().pos() * 5)
        # self.static_settings_dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.static_settings_dialog.show()

    def show_static_calculation_screen(self):
        calculation_screen = self.STATIC_subprogram.get_calculation_screen()
        self.setCentralWidget(calculation_screen)

    def show_static_results(self):
        self.plot_widget = self.STATIC_subprogram.plot_widget
        self.bottom_plot = HeatmapContourPlotBuilder(self.bottom_map, 10)
        self.MOST_subprogram.set_source_to_static()
        self.MOST_subprogram.draw_static_source(self.bottom_plot)
        self.plot_widget.add_plot("bottom", self.bottom_plot)
        # self.plot_widget.add_plot("static", self.STATIC_subprogram.heatmap_plot)
        # self.plot_widget = PlotWidget({"bottom": self.MOST_subprogram.bottom_plot})

        self.static_settings_dialog.add_result_values(self.STATIC_subprogram.v0 / 1000000000,
                                                      self.STATIC_subprogram.ve / 1000000000,
                                                      self.STATIC_subprogram.ets,
                                                      self.STATIC_subprogram.u_min,
                                                      self.STATIC_subprogram.u_max)

        self.action_calculate_most_static.setEnabled(True)
        self.action_show_static.setEnabled(True)
        self.action_draw_static_profile.setEnabled(True)

        self.plot_widget.set_plot("bottom")
        self.setCentralWidget(self.plot_widget.get_widget())

    def show_error_message(self):
        print(">> STATIC size error")
        error_dialog = ErrorDialog()
        error_dialog.exec()

    def open_static_profile_dialog(self):
        self.static_profile_dialog = StaticProfileDialog(self, self.draw_wave_profile_on_static)
        # self.static_profile_dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.static_profile_dialog.show()


class ErrorDialog(QtWidgets.QDialog, error_ui.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        line = "Incorrect values for STATIC source size or area size.\nSTATIC source is bigger then the area."
        self.label.setWordWrap(True)
        self.label.setText(line)

        self.push_button.clicked.connect(self.ok_button_pushed)

    def ok_button_pushed(self):
        self.close()


class MarigramsInfoDialog(QtWidgets.QDialog, marigrams_info_ui.Ui_Dialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    time = datetime.now().strftime("%H:%M:%S:%f")
    print(f"\n>> Started ITMS  {time}")
    window = MOSTApp()
    window.showMaximized()
    # window.show()

    app.exec_()
