from __future__ import unicode_literals
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.backends.backend_qt5agg as qt5agg
from matplotlib.figure import Figure
from PyQt5 import QtWidgets



class Plot(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.parent = parent
        self.grid = None
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(self.parent)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.graph = self.fig.add_subplot(111)
        self.graph.grid(True, which='major', color='k', linestyle='-', linewidth=0.5)
        self.graph.grid(False, which='minor')

    def set_grid(self, grid, x, y):
        self.grid = grid
        self.toolbar = qt5agg.NavigationToolbar2QT(self, self.parent)
        self.toolbar.update()
        self.grid.addWidget(self.toolbar, x, y)

    def legend(self):
        font_size = 20
        self.legend = self.graph.legend(prop={'size': font_size})
        self.legend.set_draggable(True, update='loc')

