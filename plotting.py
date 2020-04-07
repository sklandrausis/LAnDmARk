from __future__ import unicode_literals
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.backends.backend_qt5agg as qt5agg
from matplotlib.figure import Figure
from PyQt5 import QtWidgets

matplotlib.use('Qt5Agg')


class Plot(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=300):
        self.parent = parent
        self.grid = None
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(self.parent)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.graph = self.fig.add_subplot(111)

    def set_grid(self, grid):
        self.grid = grid
        self.toolbar = qt5agg.NavigationToolbar2QT(self, self.parent)
        self.toolbar.update()
        self.grid.addWidget(self.toolbar, 1, 0)

