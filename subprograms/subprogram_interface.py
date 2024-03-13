from data_entry import DataEntry
from plots.stacked_plots_widget import PlotWidget
from PyQt5.QtCore import QProcess

import json


class SubprogramInterface:
    def __init__(self, subprogram_directory, subprogram_file_names):
        self.working_directory = subprogram_directory

        self.program_file_names = self.add_directory_to_file_names(subprogram_directory, subprogram_file_names)

        self.ini_data_elements: dict[str, DataEntry] = {}
        self.input_menu_to_elements: dict[str, str] = {}

        self.plot_widget = PlotWidget()
        self.process: QProcess = QProcess()

        self.wave_profile_end_points = []
        self.bar_chart_data = None
        self.isoline_levels = []
        self.isoline_plot_data = None
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

    def add_directory_to_file_names(self, directory, file_names):
        program_file_names = {}
        for f in file_names.keys():
            program_file_names[f] = directory + "\\" + file_names[f]
        return program_file_names

    # TODO: disable all actions while subprogram is working
