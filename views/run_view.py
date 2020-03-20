from PyQt5.QtWidgets import QMainWindow
from views.run_view_ui import Ui_run_view
from controllers.run_controller import RunController
from parsers._configparser import getConfigs


class RunView(QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_run_view()
        self._ui.setupUi(self)
        self.run_controller = RunController(self._ui)
        self._ui.show_query_progress_button.clicked.connect(self.run_controller.query_progress)
        self._ui.show_stage_progress_button.clicked.connect(self.run_controller.stage_progress)
        self._ui.show_retrieve_progress_button.clicked.connect(self.run_controller.retrieve_progress)
        config_file = "config.cfg"
        self.run_color = "background-color: green"

        self.__setup(getConfigs("Operations", "querying", config_file),
                     getConfigs("Operations", "stage", config_file),
                     getConfigs("Operations", "retrieve", config_file),
                     getConfigs("Operations", "process", config_file))

    def __setup(self, query, stage, retrieve, process):
        if query == "True":
            self._ui.show_query_progress_button.setStyleSheet(self.run_color)
            self._ui.show_query_progress_button.setDisabled(False)

        if stage == "True":
            self._ui.show_stage_progress_button.setStyleSheet(self.run_color)
            self._ui.show_stage_progress_button.setDisabled(False)

        if retrieve == "True":
            self._ui.show_retrieve_progress_button.setStyleSheet(self.run_color)
            self._ui.show_retrieve_progress_button.setDisabled(False)

        if process == "True":
            self._ui.show_process_progress_button.setStyleSheet(self.run_color)
            self._ui.show_process_progress_button.setDisabled(False)


