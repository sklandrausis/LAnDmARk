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
        run_color = "background-color: green"
        run_nex_color = "background-color: blue"

        if getConfigs("Operations", "querying", config_file) == "True" and getConfigs("Operations", "stage", config_file) == "False" and  getConfigs("Operations", "retrieve", config_file) == "False" and getConfigs("Operations", "process", config_file) == "False":
            self._ui.show_query_progress_button.setStyleSheet(run_color)
            self._ui.show_query_progress_button.setDisabled(False)

        elif getConfigs("Operations", "querying", config_file) == "True" and getConfigs("Operations", "stage", config_file) == "True" and getConfigs("Operations", "retrieve", config_file) == "False" and getConfigs("Operations", "process", config_file) == "False":
            self._ui.show_query_progress_button.setStyleSheet(run_color)
            self._ui.show_stage_progress_button.setStyleSheet(run_nex_color)
            self._ui.show_query_progress_button.setDisabled(False)

        elif getConfigs("Operations", "querying", config_file) == "True" and getConfigs("Operations", "stage", config_file) == "True" and getConfigs("Operations", "retrieve", config_file) == "True" and getConfigs("Operations", "process", config_file) == "False":
            self._ui.show_query_progress_button.setStyleSheet(run_color)
            self._ui.show_stage_progress_button.setStyleSheet(run_nex_color)
            self._ui.show_retrieve_progress_button.setStyleSheet(run_nex_color)
            self._ui.show_query_progress_button.setDisabled(False)

        elif getConfigs("Operations", "querying", config_file) == "True" and getConfigs("Operations", "stage", config_file) == "True" and getConfigs("Operations", "retrieve", config_file) == "True" and getConfigs("Operations", "process", config_file) == "True":
            self._ui.show_query_progress_button.setStyleSheet(run_color)
            self._ui.show_stage_progress_button.setStyleSheet(run_nex_color)
            self._ui.show_retrieve_progress_button.setStyleSheet(run_nex_color)
            self._ui.show_process_progress_button.setStyleSheet(run_nex_color)
            self._ui.show_query_progress_button.setDisabled(False)

        elif getConfigs("Operations", "querying", config_file) == "False" and getConfigs("Operations", "stage", config_file) == "True" and getConfigs("Operations", "retrieve", config_file) == "False" and getConfigs("Operations", "process", config_file) == "False":
            self._ui.show_stage_progress_button.setStyleSheet(run_color)
            self._ui.show_stage_progress_button.setDisabled(False)

        elif getConfigs("Operations", "querying", config_file) == "True" and getConfigs("Operations", "stage", config_file) == "True" and getConfigs("Operations", "retrieve", config_file) == "False" and getConfigs("Operations", "process", config_file) == "False":
            self._ui.show_query_progress_button.setStyleSheet(run_color)
            self._ui.show_query_progress_button.setDisabled(False)
            self._ui.show_stage_progress_button.setStyleSheet(run_nex_color)

        elif getConfigs("Operations", "querying", config_file) == "False" and getConfigs("Operations", "stage", config_file) == "False" and getConfigs("Operations", "retrieve", config_file) == "True" and getConfigs("Operations", "process", config_file) == "False":
            self._ui.show_retrieve_progress_button.setStyleSheet(run_color)
            self._ui.show_retrieve_progress_button.setDisabled(False)




