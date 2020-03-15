from PyQt5.QtWidgets import QMainWindow
from views.setup_view_ui import Ui_setup_view
from controllers.setup_controller import SetupController


class SetupView(QMainWindow):
    def __init__(self):
        super().__init__()

        self._ui = Ui_setup_view()
        self._ui.setupUi(self)

        self._setup_controller = SetupController(self._ui)
        self._ui.save_button.clicked.connect(self._setup_controller.save_configuration)
