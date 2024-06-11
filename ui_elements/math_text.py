from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QPalette
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MathTextLabel(QtWidgets.QWidget):

    def __init__(self, math_text, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        if parent is not None:
            r, g, b, a = self.palette().color(QPalette.Background).getRgbF()
            figure = Figure(edgecolor=(r, g, b), facecolor=(r, g, b))
        else:
            r, g, b, a = self.palette().base().color().getRgbF()
            figure = Figure(edgecolor=(r, g, b), facecolor=(r, g, b))

        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)
        figure.clear()
        text = figure.suptitle(
            math_text,
            x=0.0,
            y=1.0,
            horizontalalignment='left',
            verticalalignment='top',
            # size=QtGui.QFont().pointSize() * 2
        )
        canvas.draw()

        (x0, y0), (x1, y1) = text.get_window_extent().get_points()
        w = x1 - x0
        h = y1 - y0

        figure.set_size_inches(w / 80, h / 80)
        self.setFixedSize(int(w), int(h))
