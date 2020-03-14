from PyQt5.QtCore import QObject, pyqtSlot
from views.setup_view import SetupView
from models.setup_model import SetupModel
from controllers.setup_controller import SetupController


class MainController(QObject):
    def __init__(self,):
        super().__init__()

    @pyqtSlot()
    def setup(self):
        setup_model = SetupModel()
        setup_controller = SetupController(setup_model)
        self.setup_view = SetupView(setup_controller)
        self.setup_view.show()