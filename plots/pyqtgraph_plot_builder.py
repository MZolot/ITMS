import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore

import numpy as np


class QTGraphHeatmap3DPlotBuilder:
    def __init__(self, plot_data):
        self.widget = gl.GLViewWidget()
        self.widget.setCameraPosition(distance=500)
        self.widget.show()

        res = np.loadtxt("MOST/extras/maxheigh_long_3.dat")

        # g = gl.GLGridItem()
        # g.scale(2, 2, 1)
        # g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
        # self.widget.addItem(g)

        p1 = gl.GLSurfacePlotItem(z=res[::3, ::3], shader='heightColor')
        p1.scale(0.1, 0.1, 10.)
        p1.translate(-18, 2, 0)
        self.widget.addItem(p1)

    def get_widget(self):
        return self.widget
