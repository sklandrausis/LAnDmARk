import sys
import os
from sys import version_info
import threading
from PyQt5.QtCore import QObject, pyqtSlot
from views.check_view import CheckView
from views.setup_view import SetupView
from views.run_view import RunView

python_version = version_info.major


def run_selected_operation():
    if python_version == 3:
        os.system("python3 " + "run_operations.py")
    elif python_version == 2:
        os.system("python2 " + "run_operations.py")
    else:
        print("python version is not supported")
        sys.exit(1)


class MainController(QObject):
    def __init__(self, *args, **kwargs):
        super(MainController, self).__init__(*args, **kwargs)
        self.run_view = RunView()
        self.setup_view = SetupView(self.run_view._ui)
        self.check_view = CheckView()

    @pyqtSlot()
    def setup(self):
        self.setup_view.show()

    @pyqtSlot()
    def run(self):
        if python_version == 3:
            os.system("python3 " + "setup.py")
        elif python_version == 2:
            os.system("python2 " + "setup.py")
        else:
            print("python version is not supported")
            sys.exit(1)

        threading.Thread(target=run_selected_operation).start()
        self.run_view.show()

    @pyqtSlot()
    def check(self):
        os.sync()
        self.check_view.show()
