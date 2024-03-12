from plots.matplotlib_plot_builder import *

from PyQt5.QtWidgets import QStackedWidget, QWidget


class PlotWidget:
    def __init__(self, plots: dict[str, PlotBuilder] | None = None):
        self.stacked_widget = QStackedWidget()

        self.plot_name_to_widget: dict[str, QWidget] = {}
        self.plot_name_to_plot: dict[str, PlotBuilder] = {}
        if plots:
            for p in plots.keys():
                self.add_plot(p, plots[p])

    def get_widget(self):
        return self.stacked_widget

    def get_plot_by_name(self, name):
        if not self.plot_name_to_plot.keys().__contains__(name):
            print("No such plots in stacked widget: " + name)
            return None
        return self.plot_name_to_plot[name]

    def set_plot(self, plot_name):
        if not self.plot_name_to_widget.keys().__contains__(plot_name):
            print("No such plots in stacked widget: " + plot_name)
            return
        self.stacked_widget.setCurrentWidget(self.plot_name_to_widget[plot_name])

    def add_plot(self, plot_name: str, plot: PlotBuilder):
        plot.update_canvas()
        if self.plot_name_to_widget.keys().__contains__(plot_name):
            plot_index = self.stacked_widget.indexOf(self.plot_name_to_widget[plot_name])
            self.plot_name_to_widget[plot_name] = plot.get_widget()
            self.plot_name_to_plot[plot_name] = plot
            self.stacked_widget.insertWidget(plot_index, self.plot_name_to_widget[plot_name])
            return

        self.plot_name_to_widget[plot_name] = plot.get_widget()
        self.plot_name_to_plot[plot_name] = plot
        self.stacked_widget.addWidget(self.plot_name_to_widget[plot_name])
