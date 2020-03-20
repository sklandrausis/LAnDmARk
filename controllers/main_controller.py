import sys
import os
from sys import version_info
from PyQt5.QtCore import QObject, pyqtSlot
from views.setup_view import SetupView
from views.run_view import RunView

python_version = version_info.major


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
        if python_version == 3:
            os.system("python3 " + "setup.py")
        elif python_version == 2:
            os.system("python2 " + "setup.py")
        else:
            print("python version is not supported")
            sys.exit(1)

        self.run_view.show()
