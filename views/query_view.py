from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from views.query_view_ui import Ui_query_view


class QueryView(QMainWindow):
    def __init__(self, run_ui, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)

        self._ui = Ui_query_view()
        self._ui.setupUi(self)
        self.run_ui = run_ui
        self.timer = QtCore.QTimer()
        f_tmp = open("querying_results.txt", "w")
        f_tmp.close()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_query_message)
        self.timer.start()

    def update_query_message(self):
        querying_results = open("querying_results.txt", "r")
        querying_msg = querying_results.readlines()
        if "done" in querying_msg:
            querying_msg.remove("done")
            self.timer.stop()
            self.run_ui.show_query_progress_button.setStyleSheet("background-color: green")
        if len(querying_msg) > 0:
            self.setGeometry(QtCore.QRect(10, 10, len(max(querying_msg)) + 470, len(querying_msg) + 470))
            self._ui.querying_message.setGeometry(QtCore.QRect(10, 10, len(max(querying_msg)) +
                                                               470, len(querying_msg) + 470))
            self._ui.querying_message.setText("".join(querying_msg))
        querying_results.close()
