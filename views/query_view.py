from PyQt5.QtWidgets import QMainWindow
from views.query_view_ui import Ui_query_view


class QueryView(QMainWindow):
    def __init__(self):
        super().__init__()

        self._ui = Ui_query_view()
        self._ui.setupUi(self)
