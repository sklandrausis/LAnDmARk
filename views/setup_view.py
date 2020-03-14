from PyQt5.QtWidgets import QMainWindow
from views.setup_view_ui import Ui_setup_view
from models.setup_model import SetupModel


class SetupView(QMainWindow):
    def __init__(self, setup_controller):
        super().__init__()

        self._setup_controller = setup_controller
        self._setup_model = SetupModel()
        self._ui = Ui_setup_view()
        self._ui.setupUi(self)

        self._setup_model.querying = self._ui.querying_comboBox.currentText()
        self._setup_model.stage = self._ui.stage_combobox.currentText()
        self._setup_model.retrieve = self._ui.retrieve_combobox.currentText()
        self._setup_model.process = self._ui.process_combobox.currentText()
        self._setup_model.which_obj = self._ui.which_combobox.currentText()
        self._setup_model.calibratorSASids = self._ui.calibratorSASids_input.text()
        self._setup_model.targetSASids = self._ui.targetSASids_input.text()
        self._setup_model.Target_name = self._ui.Target_name_input.text()
        self._setup_model.PROJECTid = self._ui.PROJECTid_input.text()
        self._setup_model.product_type = self._ui.product_type_combobox.currentText()
        self._setup_model.max_per_node = self._ui.max_per_node_input.text()
        self._setup_model.method = self._ui.method_input.text()
        self._setup_model.WorkingPath = self._ui.WorkingPath_input.text()
        self._setup_model.PrefactorPath = self._ui.PrefactorPath_input.text()
        self._setup_model.lofarroot = self._ui.lofarroot_input.text()
        self._setup_model.casaroot = self._ui.casaroot_input.text()
        self._setup_model.pyraproot = self._ui.pyraproot_input.text()
        self._setup_model.hdf5root = self._ui.hdf5root_input.text()
        self._setup_model.wcsroot = self._ui.wcsroot_input.text()
        self._setup_model.losotoPath = self._ui.losotoPath_input.text()
        self._setup_model.aoflagger = self._ui.aoflagger_input.text()
        self._setup_model.wsclean_executable = self._ui.wsclean_executable_input.text()
        self._setup_model.pythonpath = self._ui.pythonpath_input.text()
        self._setup_model.task_file = self._ui.task_file_input.text()

        self._ui.save_button.clicked.connect(self._setup_controller.save_configuration)
