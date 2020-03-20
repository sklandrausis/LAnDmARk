from PyQt5.QtWidgets import QMainWindow
from views.process_view_ui import Ui_process_progress_view


class ProcessView(QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_process_progress_view()
        self._ui.setupUi(self)