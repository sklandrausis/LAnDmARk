from PyQt5.QtWidgets import QMainWindow
from operations.operation import Status
from views.run_view_ui import Ui_run_view
from controllers.run_controller import RunController
from parsers._configparser import getConfigs


class RunView(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(RunView, self).__init__(*args, **kwargs)
        self._ui = Ui_run_view()
        self._ui.setupUi(self)
        self.run_controller = RunController(self._ui)
        self._ui.show_query_progress_button.clicked.connect(self.run_controller.query_progress)
        self._ui.show_stage_progress_button.clicked.connect(self.run_controller.stage_progress)
        self._ui.show_retrieve_progress_button.clicked.connect(self.run_controller.retrieve_progress)
        self._ui.show_process_progress_button.clicked.connect(self.run_controller.process_progress)
        config_file = "config.cfg"
        self.not_selected_color = "background-color: gray"
        self.selected_color = "background-color: yellow"
        self.started_color = "background-color: blue"
        self.finished_color = "background-color: green"

        self.__setup(getConfigs("Operations", "querying", config_file),
                     getConfigs("Operations", "stage", config_file),
                     getConfigs("Operations", "retrieve", config_file),
                     getConfigs("Operations", "process", config_file))

    def __setup(self, query, stage, retrieve, process):
        if query == "True":
            self._ui.show_query_progress_button.setStyleSheet(self.selected_color)
            self._ui.show_query_progress_button.setDisabled(False)
            querying_results = open("querying_results.txt", "w")
            querying_results.close()

        if stage == "True":
            self._ui.show_stage_progress_button.setStyleSheet(self.selected_color)
            self._ui.show_stage_progress_button.setDisabled(False)

        if retrieve == "True":
            self._ui.show_retrieve_progress_button.setStyleSheet(self.selected_color)
            self._ui.show_retrieve_progress_button.setDisabled(False)

        if process == "True":
            self._ui.show_process_progress_button.setStyleSheet(self.selected_color)
            self._ui.show_process_progress_button.setDisabled(False)

    def update_view(self, operation):
        update_dict = {Status.not_selected: self.not_selected_color,
                       Status.not_started: self.selected_color,
                       Status.started: self.started_color,
                       Status.finished: self.finished_color}
        update_style = update_dict[operation.status]

        if operation.name == "query":
            self._ui.show_query_progress_button.setStyleSheet(update_style)
        elif operation.name == "stage":
            self._ui.show_stage_progress_button.setStyleSheet(update_style)
        elif operation.name == "retrieve":
            self._ui.show_retrieve_progress_button.setStyleSheet(update_style)
        elif operation.name == "process":
            self._ui.show_process_progress_button.setStyleSheet(update_style)



