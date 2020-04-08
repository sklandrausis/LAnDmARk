from PyQt5.QtWidgets import QMainWindow
from views.check_view_ui import Ui_check_view
from controllers.check_controller import CheckController


class CheckView(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(CheckView, self).__init__(*args, **kwargs)

        self._ui = Ui_check_view()
        self._ui.setupUi(self)
        self.check_controller = CheckController()
        self._ui.landmark_button.clicked.connect(self.check_controller.check)
        self.setWindowTitle('Check')
