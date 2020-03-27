from PyQt5.QtWidgets import QMainWindow
from views.setup_view_ui import Ui_setup_view
from controllers.setup_controller import SetupController
from parsers._configparser import getConfigs


class SetupView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config_file = "config.cfg"

        self._ui = Ui_setup_view()
        self._ui.setupUi(self)

        self._setup_controller = SetupController(self._ui)
        self._ui.save_button.clicked.connect(self._setup_controller.save_configuration)

        if len(getConfigs("Data", "targetsasids", self.config_file)) != 0:
            self._ui.targetSASids_input.setText(getConfigs("Data", "targetsasids", self.config_file))

        if len(getConfigs("Data", "calibratorsasids", self.config_file)) != 0:
            self._ui.calibratorSASids_input.setText(getConfigs("Data", "calibratorsasids", self.config_file))

        if len(getConfigs("Data", "targetname", self.config_file)) != 0:
            self._ui.Target_name_input.setText(getConfigs("Data", "targetname", self.config_file))

        if len(getConfigs("Data", "projectid", self.config_file)) != 0:
            self._ui.PROJECTid_input.setText(getConfigs("Data", "projectid", self.config_file))

        if len(getConfigs("Data", "producttype", self.config_file)) != 0:
            self._ui.product_type_combobox.setCurrentText(getConfigs("Data", "producttype", self.config_file))

        if len(getConfigs("Operations", "querying", self.config_file)) != 0:
            self._ui.querying_comboBox.setCurrentText(getConfigs("Operations", "querying", self.config_file))

        if len(getConfigs("Operations", "stage", self.config_file)) != 0:
            self._ui.stage_combobox.setCurrentText(getConfigs("Operations", "stage", self.config_file))

        if len(getConfigs("Operations", "retrieve", self.config_file)) != 0:
            self._ui.retrieve_combobox.setCurrentText(getConfigs("Operations", "retrieve", self.config_file))

        if len(getConfigs("Operations", "process", self.config_file)) != 0:
            self._ui.process_combobox.setCurrentText(getConfigs("Operations", "process", self.config_file))

        if len(getConfigs("Operations", "which_obj", self.config_file)) != 0:
            self._ui.which_combobox.setCurrentText(getConfigs("Operations", "which_obj", self.config_file))

        if len(getConfigs("Paths", "workingpath", self.config_file)) != 0:
            self._ui.WorkingPath_input.setText(getConfigs("Paths", "workingpath", self.config_file))

        if len(getConfigs("Paths", "prefactorpath", self.config_file)) != 0:
            self._ui.PrefactorPath_input.setText(getConfigs("Paths", "prefactorpath", self.config_file))

        if len(getConfigs("Paths",  "lofarroot", self.config_file) )!= 0:
            self._ui.lofarroot_input.setText(getConfigs("Paths", "lofarroot", self.config_file))

        if len(getConfigs("Paths", "casaroot", self.config_file)) != 0:
            self._ui.casaroot_input.setText(getConfigs("Paths", "casaroot", self.config_file))

        if len(getConfigs("Paths", "pyraproot", self.config_file)) != 0:
            self._ui.pyraproot_input.setText(getConfigs("Paths", "pyraproot", self.config_file))

        if len(getConfigs("Paths", "hdf5root", self.config_file)) != 0:
            self._ui.hdf5root_input.setText(getConfigs("Paths", "hdf5root", self.config_file))

        if len(getConfigs("Paths", "wcsroot", self.config_file)) != 0:
            self._ui.wcsroot_input.setText(getConfigs("Paths", "wcsroot", self.config_file))

        if len(getConfigs("Paths", "losotopath", self.config_file)) != 0:
            self._ui.losotoPath_input.setText(getConfigs("Paths", "losotopath", self.config_file))

        if len(getConfigs("Paths", "aoflagger", self.config_file)) != 0:
            self._ui.aoflagger_input.setText(getConfigs("Paths", "aoflagger", self.config_file))

        if len(getConfigs("Paths", "wsclean_executable", self.config_file)) != 0:
            self._ui.wsclean_executable_input.setText(getConfigs("Paths", "wsclean_executable", self.config_file))

        if len(getConfigs("Paths", "pythonpath", self.config_file)) != 0:
            self._ui.pythonpath_input.setText(getConfigs("Paths", "pythonpath", self.config_file))

        if len(getConfigs("Paths", "task_file", self.config_file)) != 0:
            self._ui.task_file_input.setText(getConfigs("Paths", "task_file", self.config_file))

        if len(getConfigs("Cluster", "max_per_node", self.config_file)) != 0:
            self._ui.max_per_node_input.setText(getConfigs("Cluster", "max_per_node", self.config_file))

        if len(getConfigs("Cluster", "method", self.config_file)) != 0:
            self._ui.method_input.setText(getConfigs("Cluster", "method", self.config_file))
