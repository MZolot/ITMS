import ui_elements.qt_designer_ui.static_profile_dialog_ui as dialog_ui
from plots.matplotlib_plot_builder import PlotBuilder
from PyQt5 import QtWidgets


class StaticProfileDialog(QtWidgets.QDialog, dialog_ui.Ui_Dialog):
    def __init__(self, parent, new_profile_callback_function: callable):
        super().__init__(parent)
        self.setupUi(self)
        self.new_profile_callback_function = new_profile_callback_function

        self.push_button_close.clicked.connect(self.close)
        self.push_button_new_profile.clicked.connect(self.new_profile_pushed)

        self.current_widget = None

    def set_plot(self, plot: PlotBuilder):
        self.set_widget(plot.get_widget())
        self.resize(600, 500)
        # self.adjustSize()

    def set_widget(self, widget):
        if self.current_widget is not None:
            self.vertical_layout.removeWidget(self.current_widget)
        self.current_widget = widget
        self.vertical_layout.insertWidget(0, self.current_widget)

    def new_profile_pushed(self):
        self.push_button_new_profile.setEnabled(False)
        self.set_widget(QtWidgets.QLabel("Please draw profile"))
        self.new_profile_callback_function(self.set_plot)
        self.push_button_new_profile.setEnabled(True)
