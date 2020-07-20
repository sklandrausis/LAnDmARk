from PyQt5.QtWidgets import QMainWindow
from views.main_view_ui import Ui_main_window


class MainView(QMainWindow):
    def __init__(self, main_controller, *args, **kwargs):
        super(MainView, self).__init__(*args, **kwargs)

        self._main_controller = main_controller

        self._ui = Ui_main_window()
        self._ui.setupUi(self)

        self._ui.setup_button.clicked.connect(self._main_controller.setup)
        self._ui.run_button.clicked.connect(self._main_controller.run)
        self._ui.check_button.clicked.connect(self._main_controller.check)

        self.setWindowTitle('Main')