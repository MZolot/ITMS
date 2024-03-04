from data_entry import DataEntry
from plots.stacked_plots_widget import PlotWidget
from PyQt5.QtCore import QProcess, QThread

import json


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
