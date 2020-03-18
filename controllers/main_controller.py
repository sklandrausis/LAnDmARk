from PyQt5.QtCore import QObject, pyqtSlot
from views.setup_view import SetupView
from views.run_view import RunView


class MainController(QObject):
    def __init__(self,):
        super().__init__()
        self.setup_view = SetupView()
        self.run_view = RunView()

    @pyqtSlot()
    def setup(self):
        self.setup_view.show()

    @pyqtSlot()
    def run(self):
        self.run_view.show()
