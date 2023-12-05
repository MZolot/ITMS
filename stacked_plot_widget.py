from PyQt5.QtWidgets import QWidget


class StackedPlotWidget:
    def __init__(self):
        self.widgets_by_name = {}

    def add_plot(self, widget, plot_name):
        self.widgets_by_name[plot_name] = widget

    def get_plot_widget(self, plot_name):
        if plot_name in self.widgets_by_name.keys():
            return self.widgets_by_name[plot_name]
