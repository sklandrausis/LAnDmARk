import sys
import os
from sys import version_info
import threading
from PyQt5.QtCore import QObject, pyqtSlot
from operations.operation import Status
from operations.process import Process
from operations.query import Query
from operations.retrieve import Retrieve
from operations.stage import Stage
from parsers._configparser import getConfigs
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
        self.config_file = "config.cfg"

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

        threading.Thread(target=self.run_view.show).start()

        operations = []
        if getConfigs("Operations", "querying", self.config_file) == "True":
            query_operation = Query()
            query_operation.status = Status.not_started
            operations.append(query_operation)
            self.run_view.update_view(query_operation)

        if getConfigs("Operations", "stage", self.config_file) == "True":
            stage_operation = Stage()
            stage_operation.status = Status.not_started
            operations.append(stage_operation)
            self.run_view.update_view(stage_operation)

        if getConfigs("Operations", "retrieve", self.config_file) == "True":
            retrieve_operation = Retrieve()
            retrieve_operation.status = Status.not_started
            operations.append(retrieve_operation)
            self.run_view.update_view(retrieve_operation)

        if getConfigs("Operations", "process", self.config_file) == "True":
            process_operation = Process()
            process_operation.status = Status.not_started
            operations.append(process_operation)
            self.run_view.update_view(process_operation)

        threading.Thread(target=self.run_operations, args=(operations,)).start()

    @pyqtSlot()
    def check(self):
        os.sync()
        self.check_view.show()

    def run_operations(self, operations):
        for operation in operations:
            operation.status = Status.started
            self.run_view.update_view(operation)
            operation.execute()
            operation.status = Status.finished
            self.run_view.update_view(operation)
