import ui_elements.qt_designer_ui.most_results_dialog_ui as dialog_ui
from plots.matplotlib_plot_builder import PlotBuilder
from PyQt5 import QtWidgets


class MostResultsDialog(QtWidgets.QDialog, dialog_ui.Ui_Dialog):
    def __init__(self, parent, title: str, plot: PlotBuilder):
        super().__init__(parent)
        self.setupUi(self)
        self.vertical_layout.insertWidget(0, plot.get_widget())
        self.setWindowTitle(title)
        self.push_button_close.clicked.connect(self.close)
