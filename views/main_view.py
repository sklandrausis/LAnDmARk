from PyQt5.QtWidgets import QMainWindow
from views.main_view_ui import Ui_main_window


class MainView(QMainWindow):
    def __init__(self, main_controller):
        super().__init__()

        self._main_controller = main_controller

        self._ui = Ui_main_window()
        self._ui.setupUi(self)

        self._ui.setup_button.clicked.connect(self._main_controller.setup)

