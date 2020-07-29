from PyQt5.QtWidgets import QMainWindow
from views.setup_view_ui import Ui_setup_view
from controllers.setup_controller import SetupController
from parsers._configparser import getConfigs


class SetupView(QMainWindow):
    def __init__(self, run_ui, *args, **kwargs):
        super(SetupView, self).__init__(*args, **kwargs)

        self.config_file = "config.cfg"
        self.run_ui = run_ui

        self._ui = Ui_setup_view()
        self._ui.setupUi(self)
        self.init_color_setup()

        self._setup_controller = SetupController(self._ui,  self.run_ui)
        self._ui.save_button.clicked.connect(self._setup_controller.save_configuration)
        self._ui.querying_comboBox.currentTextChanged.connect(self._setup_controller.on_querying_combobox_changed)
        self._ui.stage_combobox.currentTextChanged.connect(self._setup_controller.on_stage_combobox_changed)
        self._ui.retrieve_combobox.currentTextChanged.connect(self._setup_controller.on_retrieve_combobox_changed)
        self._ui.process_combobox.currentTextChanged.connect(self._setup_controller.on_process_combobox_changed)
        self._ui.select_subband_range_combobox.currentTextChanged.connect(
            self._setup_controller.on_select_subband_range_combobox_changed)

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

        if len(getConfigs("Data", "minsubband", self.config_file)) != 0:
            self._ui.min_subband_input.setText(getConfigs("Data", "minsubband", self.config_file))

        if len(getConfigs("Data", "maxsubband", self.config_file)) != 0:
            self._ui.max_subband_input.setText(getConfigs("Data", "maxsubband", self.config_file))

        if len(getConfigs("Data", "subbandselect", self.config_file)) != 0:
            self._ui.select_subband_range_combobox.setCurrentText(getConfigs("Data", "subbandselect", self.config_file))

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

        if self._ui.select_subband_range_combobox.currentText() == "True":
            self._ui.min_subband_label.setEnabled(True)
            self._ui.min_subband_input.setEnabled(True)
            self._ui.max_subband_label.setEnabled(True)
            self._ui.max_subband_input.setEnabled(True)

        elif self._ui.select_subband_range_combobox.currentText() == "False":
            self._ui.min_subband_label.setEnabled(False)
            self._ui.min_subband_input.setEnabled(False)
            self._ui.max_subband_label.setEnabled(False)
            self._ui.max_subband_input.setEnabled(False)

    def init_color_setup(self):
        self._ui.WorkingPath_input.setStyleSheet("Background-color: rgb(152,251,152)")
        self._ui.Target_name_input.setStyleSheet("Background-color: rgb(152,251,152)")
        self._ui.targetSASids_input.setStyleSheet("Background-color: rgb(152,251,152)")
        self._ui.PROJECTid_input.setStyleSheet("Background-color: rgb(152,251,152)")

    def on_querying_combobox_changed(self):
        if self._ui.querying_comboBox.currentText() == "True":
            self.init_color_setup()

    def on_stage_combobox_changed(self):
        if self._ui.stage_combobox.currentText() == "True":
            self.init_color_setup()

    def on_retrieve_combobox_changed(self):
        if self._ui.retrieve_combobox.currentText() == "True":
            self.init_color_setup()

    def on_process_combobox_changed(self):
        if self._ui.process_combobox.currentText() == "True":
            self.init_color_setup()
            self._ui.max_per_node_input.setStyleSheet("Background-color: rgb(152,251,152)")
            self._ui.method_input.setStyleSheet("Background-color: rgb(152,251,152)")

            self._ui.PrefactorPath_input.setStyleSheet("Background-color: rgb(152,251,152)")
            self._ui.lofarroot_input.setStyleSheet("Background-color: rgb(152,251,152)")
            self._ui.casaroot_input.setStyleSheet("Background-color: rgb(152,251,152)")
            self._ui.pyraproot_input.setStyleSheet("Background-color: rgb(152,251,152)")
            self._ui.losotoPath_input.setStyleSheet("Background-color: rgb(152,251,152)")
            self._ui.aoflagger_input.setStyleSheet("Background-color: rgb(152,251,152)")
            self._ui.wsclean_executable_input.setStyleSheet("Background-color: rgb(152,251,152)")
            self._ui.pythonpath_input.setStyleSheet("Background-color: rgb(152,251,152)")
            self._ui.task_file_input.setStyleSheet("Background-color: rgb(152,251,152)")

        elif self._ui.process_combobox.currentText() == "False":
            self._ui.max_per_node_input.setStyleSheet("Background-color: rgb(255,255,255)")
            self._ui.method_input.setStyleSheet("Background-color: rgb(255,255,255)")

            self._ui.PrefactorPath_input.setStyleSheet("Background-color: rgb(255,255,255)")
            self._ui.lofarroot_input.setStyleSheet("Background-color: rgb(255,255,255)")
            self._ui.casaroot_input.setStyleSheet("Background-color: rgb(255,255,255)")
            self._ui.pyraproot_input.setStyleSheet("Background-color: rgb(255,255,255)")
            self._ui.losotoPath_input.setStyleSheet("Background-color: rgb(255,255,255)")
            self._ui.aoflagger_input.setStyleSheet("Background-color: rgb(255,255,255)")
            self._ui.wsclean_executable_input.setStyleSheet("Background-color: rgb(255,255,255)")
            self._ui.pythonpath_input.setStyleSheet("Background-color: rgb(255,255,255)")
            self._ui.task_file_input.setStyleSheet("Background-color: rgb(255,255,255)")

