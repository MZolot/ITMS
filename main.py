import os
import sys
from datetime import datetime

import numpy as np
from PyQt5 import QtWidgets

import ui_elements.qt_designer_ui.main_ui as main_ui
import ui_elements.qt_designer_ui.marigrams_info_message_ui as marigrams_info_ui
from plots.matplotlib_plot_builder import (HeatmapPlotBuilder,
                                           HeatmapContourPlotBuilder,
                                           BarPlotBuilder,
                                           CommonPlotBuilder)
from plots.stacked_plots_widget import PlotWidget
from subprograms.most_interface import MOSTInterface
from subprograms.static_interface import STATICInterface
from ui_elements.bottom_profile_dialog import *
from ui_elements.heights_info_dialog import *
from ui_elements.input_dialog import *
from ui_elements.isoline_settings_dialog import IsolineSettingsDialog
from ui_elements.load_data_file_selection_dialog import FileSelectionMenuDialog
from ui_elements.most_results_dialog import *
from ui_elements.static_profile_dialog import StaticProfileDialog
from ui_elements.static_settings_dialog import StaticSettingsDialog
from ui_elements.waiting_screens import *

koryto_profile_file_name = os.path.join("subprograms/MOST/koryto_profile_default.txt")
most_config_file_name = "resources/most_parameters_config.json"
static_config_file_name = "resources/static_parameters_config.json"


class MOSTApp(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.koryto_profile = np.loadtxt(koryto_profile_file_name)
        self.bottom_profile = np.copy(self.koryto_profile)
        self.bottom_map = np.transpose(np.tile(self.bottom_profile, (1500, 1)))
        self.bottom_plot = HeatmapPlotBuilder(self.bottom_map)

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
            "exe": "wave_mareo_min.exe",
            "initial": "ini_data.txt",
            "height": "heigh.dat",
            "max_height": "maxheigh.dat",
            "min_height": "h_min.dat",
            "profile": "koryto_profile.txt"
        }

        self.MOST_subprogram = MOSTInterface(config_file_name=most_config_file_name,
                                             subprogram_directory="subprograms\\MOST",
                                             subprogram_file_names=self.most_files,
                                             bottom_profile=self.bottom_profile,
                                             save_wave_profile_callback=self.save_wave_profile_data,
                                             save_marigrams_callback=self.save_marigrams_data,
                                             show_calculation_screen_callback=self.show_most_calculation_screen,
                                             show_loading_screen_callback=self.show_loading_screen,
                                             show_results_callback=self.show_most_result,
                                             static=self.STATIC_subprogram)

        self.plot_widget = PlotWidget({"bottom": self.bottom_plot})

        # self.set_bottom_profile(self.bottom_profile)
        self.MOST_subprogram.draw_source(self.bottom_plot)

        self.bottom_profile_flat_dialog = None
        self.bottom_profile_complex_dialog = None
        self.static_settings_dialog = None
        self.static_profile_dialog = None

        self.wave_profile_end_points = []
        self.wave_profile_data = None

        self.setupUi(self)
        self.set_actions()

        self.setCentralWidget(self.plot_widget.get_widget())

    def set_actions(self):
        self.action_load_existing_results.setEnabled(False)  # TODO: fix loading (marigrams issue)

        # ============== Parameter menus =================

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

        # ============== Bottom profile =================

        # self.action_profile_default.triggered.connect(
        #     lambda: self.set_bottom_profile(self.koryto_profile)
        # )
        self.action_profile_last.triggered.connect(self.load_last_used_profile)
        self.action_profile_koryto.triggered.connect(self.set_koryto_profile)

        self.action_profile_flat.triggered.connect(
            lambda: self.open_bottom_profile_dialog("flat")
        )
        self.action_profile_tilted.triggered.connect(
            lambda: self.open_bottom_profile_dialog("complex")
        )

        # ============== STATIC ========================

        self.action_static_source.triggered.connect(self.open_static_settings_dialog)
        self.action_show_static.triggered.connect(self.open_static_result_dialog)
        self.action_draw_static_profile.triggered.connect(self.open_static_profile_dialog)

        # ============== Visualisation =================

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
        self.action_marigrams.triggered.connect(
            lambda: self.open_most_results_dialog("marigrams", "Marigrams")
        )

        # ============== Parameters =================

        self.action_set_contour_lines_levels_for_MOST.triggered.connect(self.open_isoline_settings_menu_for_most)
        self.action_set_contour_lines_levels_for_STATIC.triggered.connect(self.open_isoline_settings_menu_for_static)

        # ============== Other ======================

        self.action_select_marigram_points.triggered.connect(self.get_marigram_points)
        self.action_load_existing_results.triggered.connect(self.open_most_file_selection_menu)

    def open_bottom_profile_dialog(self, profile_type: str):
        if profile_type == "flat":
            if self.bottom_profile_flat_dialog is None:
                self.bottom_profile_flat_dialog = BottomProfileFlatDialog(self, self.set_bottom_profile)
            dialog = self.bottom_profile_flat_dialog
        elif profile_type == "complex":
            if self.bottom_profile_complex_dialog is None:
                self.bottom_profile_complex_dialog = BottomProfileComplexDialog(self, self.set_bottom_profile)
            dialog = self.bottom_profile_complex_dialog
        else:
            print("incorrect bottom profile type: " + profile_type)
            return

        dialog.show()

    def set_bottom_profile(self, profile):
        self.bottom_profile = profile
        self.set_bottom_plot()

        self.MOST_subprogram.set_bottom_profile(self.bottom_profile)
        self.open_bottom_profile_plot_dialog(self.bottom_profile)

    def set_koryto_profile(self):
        f = open("last_used_profile.txt", 'w')
        f.write(f'koryto\n')
        f.close()
        self.set_bottom_profile(self.koryto_profile)

    def load_last_used_profile(self):
        f = open("last_used_profile.txt", 'r')
        profile_type = f.readline().strip()
        print(f">> Loading last used profile: {profile_type}")

        if profile_type == "koryto":
            self.set_bottom_profile(self.koryto_profile)

        elif profile_type == "flat":
            values = f.readline().strip().split()
            self.bottom_profile_flat_dialog = BottomProfileFlatDialog(self, self.set_bottom_profile)
            self.bottom_profile_flat_dialog.set_values(values[0], values[1])
            self.bottom_profile_flat_dialog.ok_pushed()

        elif profile_type == "complex":
            start_depth = f.readline().strip()
            depths = []
            lengths = []
            for line in f:
                values = line.strip().split()
                lengths.append(values[0])
                depths.append(values[1])

            self.bottom_profile_complex_dialog = BottomProfileComplexDialog(self, self.set_bottom_profile)
            self.bottom_profile_complex_dialog.set_values(start_depth, lengths, depths)
            self.bottom_profile_complex_dialog.ok_pushed()

        f.close()

    def set_bottom_plot(self):
        x_size = self.MOST_subprogram.ini_data_elements["x-size"].get_current_value()
        self.bottom_map = np.transpose(np.tile(self.bottom_profile, (x_size, 1)))
        self.bottom_plot = HeatmapPlotBuilder(self.bottom_map)
        self.MOST_subprogram.draw_source(self.bottom_plot)
        self.plot_widget.add_plot("bottom", self.bottom_plot)
        self.plot_widget.set_plot("bottom")

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
                                                [self.set_bottom_plot
                                                 # lambda: self.MOST_subprogram.draw_source(self.bottom_plot)
                                                 ])
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
        loading_screen = LoadingScreen()
        self.setCentralWidget(loading_screen.get_screen())

    # def parse_initial_data_file(self):  # TODO: change to work for static
    def show_most_result(self):
        self.plot_widget = PlotWidget()
        self.bottom_plot = HeatmapPlotBuilder(self.bottom_map)
        self.plot_widget.add_plot("bottom", self.bottom_plot)
        self.MOST_subprogram.draw_source(self.bottom_plot)

        self.action_heatmap.setEnabled(True)
        self.action_heatmap_with_contour.setEnabled(True)
        self.action_3d_heatmap.setEnabled(True)
        self.action_wave_profile_bar_chart.setEnabled(True)
        self.action_draw_wave_profile.setEnabled(True)

        if (self.MOST_subprogram.marigram_points is not None) & (self.MOST_subprogram.marigram_points != []):
            self.action_marigrams.setEnabled(True)
            self.bottom_plot.draw_points(self.MOST_subprogram.marigram_points)

        self.plot_widget.set_plot("bottom")
        self.setCentralWidget(self.plot_widget.get_widget())
        # self.setCentralWidget(self.bottom_plot.get_widget())
        self.open_most_results_dialog("heatmap", "Heatmap")

    def open_most_results_dialog(self, plot_name: str, dialog_title):
        plot = self.MOST_subprogram.get_plot(plot_name)
        plot.update_canvas()
        if plot_name == "heatmap":
            dialog = HeatmapDialog(self, dialog_title, plot, self.show_most_wave_profile)
        elif plot_name == "profile":
            dialog = WaveProfileDialog(self, dialog_title, plot, self.show_wave_profile_info)
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

    def open_bottom_profile_plot_dialog(self, profile):
        plot = CommonPlotBuilder(profile)
        dialog = PlotDialog(self, "Bottom profile", plot)
        dialog.move(self.pos() + self.centralWidget().pos() * 5)
        dialog.resize(370, 370)
        dialog.show()

    def get_marigram_points(self):
        # self.plot_widget.set_plot(plot_name)
        # plot: HeatmapPlotBuilder = self.plot_widget.get_plot_by_name("bottom")
        plot: HeatmapPlotBuilder = self.bottom_plot
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

    def show_most_wave_profile(self, heatmap_dialog, wave_profile_end_points):
        self.wave_profile_end_points = wave_profile_end_points
        self.wave_profile_data = self.get_wave_profile_on_line(self.wave_profile_end_points,
                                                               self.MOST_subprogram.max_height)
        wave_profile_data_min = self.get_wave_profile_on_line(self.wave_profile_end_points,
                                                              self.MOST_subprogram.min_height)
        wave_profile_plot = BarPlotBuilder(self.wave_profile_data, wave_profile_data_min, self.save_wave_profile_data)

        dialog = PlotDialog(heatmap_dialog, "Wave profile", wave_profile_plot)
        dialog.show()

    def show_wave_profile_info(self, profile_dialog):
        dialog = HeightsInfoDialog(profile_dialog, self.wave_profile_data)
        dialog.show()

    def draw_wave_profile_on_static(self, draw_profile_callback):
        # self.plot_widget.set_plot("bottom")
        # plot = self.plot_widget.get_plot_by_name("bottom")
        plot = self.bottom_plot

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

        self.MOST_subprogram.plot_name_to_builder["heatmap contour"] = heatmap_with_contour_plot
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
        self.static_settings_dialog.show()

    def show_static_calculation_screen(self):
        calculation_screen = self.STATIC_subprogram.get_calculation_screen()
        self.setCentralWidget(calculation_screen)

    def show_static_results(self):
        self.bottom_plot = HeatmapPlotBuilder(self.bottom_map)
        self.MOST_subprogram.set_source_to_static()
        self.MOST_subprogram.draw_static_source(self.bottom_plot)
        self.plot_widget = PlotWidget({"bottom": self.bottom_plot})

        self.static_settings_dialog.add_result_values(self.STATIC_subprogram.v0 / 1000000000,
                                                      self.STATIC_subprogram.ve / 1000000000,
                                                      self.STATIC_subprogram.ets,
                                                      self.STATIC_subprogram.u_min,
                                                      self.STATIC_subprogram.u_max)

        # self.action_calculate_most_static.setEnabled(True)
        self.action_show_static.setEnabled(True)
        self.action_draw_static_profile.setEnabled(True)

        self.plot_widget.set_plot("bottom")
        self.setCentralWidget(self.plot_widget.get_widget())
        # self.setCentralWidget(self.bottom_plot.get_widget())

    def show_error_message(self):
        print(">> STATIC size error")
        error_dialog = ErrorDialog()
        error_dialog.exec()

    def open_static_profile_dialog(self):
        self.static_profile_dialog = StaticProfileDialog(self, self.draw_wave_profile_on_static)
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
