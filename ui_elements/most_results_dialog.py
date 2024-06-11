import ui_elements.qt_designer_ui.plot_dialog_ui as dialog_ui
from plots.matplotlib_plot_builder import *
from PyQt5 import QtWidgets, QtCore


class PlotDialog(QtWidgets.QDialog, dialog_ui.Ui_Dialog):
    def __init__(self, parent, title: str, plot: PlotBuilder):
        super().__init__(parent)
        self.setupUi(self)
        self.vertical_layout.insertWidget(0, plot.get_widget())
        self.setWindowTitle(title)
        self.push_button_close.clicked.connect(self.close)


class HeatmapDialog(PlotDialog):
    def __init__(self, parent, title: str, plot: HeatmapPlotBuilder, wave_profile_callback):
        super().__init__(parent, title, plot)
        self.plot = plot
        self.wave_profile_callback = wave_profile_callback

        self.push_button_profile = QtWidgets.QPushButton(self.buttons_widget)
        self.push_button_profile.setMinimumSize(QtCore.QSize(125, 28))
        self.push_button_profile.setMaximumSize(QtCore.QSize(125, 28))
        self.push_button_profile.setText("Draw wave profile")
        self.push_button_profile.clicked.connect(self.get_wave_profile_points)
        self.buttons_layout.insertWidget(0, self.push_button_profile)

    def get_wave_profile_points(self):
        self.push_button_profile.setEnabled(False)
        # self.plot.clear_points()  # убирает мареограммы
        self.plot.clear_line()

        wave_profile_end_points = self.plot.get_input_points(n=2)
        if len(wave_profile_end_points) < 2:
            return

        self.plot.draw_line(wave_profile_end_points[0][0], wave_profile_end_points[0][1],
                            wave_profile_end_points[1][0], wave_profile_end_points[1][1])
        self.push_button_profile.setEnabled(True)

        self.wave_profile_callback(self, wave_profile_end_points)


class WaveProfileDialog(PlotDialog):
    def __init__(self, parent, title: str, plot: HeatmapPlotBuilder, height_info_callback):
        super().__init__(parent, title, plot)

        self.push_button_info = QtWidgets.QPushButton(self.buttons_widget)
        # self.push_button_info.setMinimumSize(QtCore.QSize(125, 28))
        # self.push_button_info.setMaximumSize(QtCore.QSize(125, 28))
        self.push_button_info.setText("View profile characteristics")
        self.push_button_info.clicked.connect(lambda: height_info_callback(self))
        self.buttons_layout.insertWidget(0, self.push_button_info)
