import os
from awlofar.database.Context import context
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSlot
from models.setup_model import SetupModel
from parsers._configparser import setConfigs


class SetupController(QObject):
    def __init__(self, _ui, run_ui, *args, **kwargs):
        super(SetupController, self).__init__(*args, **kwargs)
        self.setup_model = SetupModel()
        self._ui = _ui
        self.run_ui = run_ui

    @pyqtSlot(bool, name="valid")
    def __validate_setup(self):
        valid_count = 0
        self.setup_model.querying = self._ui.querying_comboBox.currentText()
        self.setup_model.stage = self._ui.stage_combobox.currentText()
        self.setup_model.retrieve = self._ui.retrieve_combobox.currentText()
        self.setup_model.process = self._ui.process_combobox.currentText()
        self.setup_model.which_obj = self._ui.which_combobox.currentText()
        self.setup_model.calibratorSASids = self._ui.calibratorSASids_input.text()
        self.setup_model.targetSASids = self._ui.targetSASids_input.text()
        self.setup_model.Target_name = self._ui.Target_name_input.text()
        self.setup_model.PROJECTid = self._ui.PROJECTid_input.text()
        self.setup_model.product_type = self._ui.product_type_combobox.currentText()
        self.setup_model.max_per_node = self._ui.max_per_node_input.text()
        self.setup_model.method = self._ui.method_input.text()
        self.setup_model.WorkingPath = self._ui.WorkingPath_input.text()
        self.setup_model.PrefactorPath = self._ui.PrefactorPath_input.text()
        self.setup_model.lofarroot = self._ui.lofarroot_input.text()
        self.setup_model.casaroot = self._ui.casaroot_input.text()
        self.setup_model.pyraproot = self._ui.pyraproot_input.text()
        self.setup_model.hdf5root = self._ui.hdf5root_input.text()
        self.setup_model.wcsroot = self._ui.wcsroot_input.text()
        self.setup_model.losotoPath = self._ui.losotoPath_input.text()
        self.setup_model.aoflagger = self._ui.aoflagger_input.text()
        self.setup_model.wsclean_executable = self._ui.wsclean_executable_input.text()
        self.setup_model.pythonpath = self._ui.pythonpath_input.text()
        self.setup_model.task_file = self._ui.task_file_input.text()
        self.setup_model.min_subband = self._ui.min_subband_input.text()
        self.setup_model.max_subband = self._ui.max_subband_input.text()
        self.setup_model.subband_select = self._ui.select_subband_range_combobox.currentText()
        self.setup_model.min_frequency = self._ui.min_frequency_input.text()
        self.setup_model.max_frequency = self._ui.max_frequency_input.text()
        self.setup_model.frequency_select = self._ui.select_frequency_range_combobox.currentText()

        def process_valid():
            valid_count = 0
            if len(self.setup_model.WorkingPath) == 0:
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "Working path cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.WorkingPath):
                    valid_count += 1
                    QMessageBox.warning(QMessageBox(), "Warning", "Working path is not existing")

            if len(self.setup_model.PrefactorPath) == 0:
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "Working path cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.PrefactorPath):
                    valid_count += 1
                    QMessageBox.warning(QMessageBox(), "Warning", "Working path is not existing")

            if len(self.setup_model.lofarroot) == 0:
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "LOFAR root cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.lofarroot):
                    valid_count += 1
                    QMessageBox.warning(QMessageBox(), "Warning", "LOFAR root is not existing")

            if len(self.setup_model.casaroot) == 0:
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "CASA root cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.casaroot):
                    valid_count += 1
                    QMessageBox.warning(QMessageBox(), "Warning", "CASA root is not existing")

            if len(self.setup_model.pyraproot) == 0:
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "Pyrap root cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.pyraproot):
                    valid_count += 1
                    QMessageBox.warning(QMessageBox(), "Warning", "Pyrap root root is not existing")

            if len(self.setup_model.losotoPath) == 0:
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "losoto path cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.losotoPath):
                    valid_count += 1
                    QMessageBox.warning(QMessageBox(), "Warning", "losoto path is not existing")

            if len(self.setup_model.aoflagger) == 0:
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "aoflagger cannot be empty")
            else:
                if not os.path.isfile(self.setup_model.aoflagger):
                    valid_count += 1
                    QMessageBox.warning(QMessageBox(), "Warning", "aoflagger is not existing")

            if len(self.setup_model.aoflagger) == 0:
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "aoflagger cannot be empty")
            else:
                if not os.path.isfile(self.setup_model.aoflagger):
                    valid_count += 1
                    QMessageBox.warning(QMessageBox(), "Warning", "aoflagger is not existing")

            if len(self.setup_model.wsclean_executable) == 0:
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "wsclean executable cannot be empty")
            else:
                if not os.path.isfile(self.setup_model.wsclean_executable):
                    valid_count += 1
                    QMessageBox.warning(QMessageBox(), "Warning", "wsclean executable is not existing")

            if len(self.setup_model.task_file) == 0:
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "task file cannot be empty")
            else:
                if not os.path.isfile(self.setup_model.task_file):
                    valid_count += 1
                    QMessageBox.warning(QMessageBox(), "Warning", "task file is not existing")

            if len(self.setup_model.pythonpath) == 0:
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "python path cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.pythonpath):
                    valid_count += 1
                    QMessageBox.warning(QMessageBox(), "Warning", "python path is not existing")
            return valid_count

        if self.setup_model.querying == "True" or \
                self.setup_model.stage == "True" or \
                self.setup_model.retrieve == "True" or \
                self.setup_model.process == "True":
            if len(self.setup_model.WorkingPath) == 0:
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "Working path cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.WorkingPath):
                    valid_count += 1
                    QMessageBox.warning(QMessageBox(), "Warning", "Working path is not existing")

            if len(self.setup_model.PROJECTid) == 0:
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "Project ID cannot be empty")
            else:
                project = self.setup_model.PROJECTid
                context.set_project(project)
                if project != context.get_current_project().name:
                    valid_count += 1
                    QMessageBox.warning(QMessageBox(), "Warning", "You are not member of project")

                else:
                    if self.setup_model.which_obj == "calibrators":
                        if len(self.setup_model.calibratorSASids) == 0:
                            if project != "MSSS_HBA_2013":
                                valid_count += 1
                                QMessageBox.warning(QMessageBox(), "Warning", "If project is not MSSS_HBA_2013 SAS id for calibrator must be specified")
                            if len(self.setup_model.targetSASids) == 0:
                                valid_count += 1
                                QMessageBox.warning(QMessageBox(), "Warning", "Target SAS id must be specified")

                    elif self.setup_model.which_obj == "target":
                        if len(self.setup_model.targetSASids) == 0:
                            valid_count += 1
                            QMessageBox.warning(QMessageBox(), "Warning", "Target SAS id must be specified")
                        if len(self.setup_model.Target_name) == 0:
                            valid_count += 1
                            QMessageBox.warning(QMessageBox(), "Warning", "Target name must be specified")
                    else:
                        if len(self.setup_model.calibratorSASids) == 0:
                            if project != "MSSS_HBA_2013":
                                valid_count += 1
                                QMessageBox.warning(QMessageBox(), "Warning", "If project is not MSSS_HBA_2013 SAS id for calibrator must be specified")

                            if len(self.setup_model.targetSASids) == 0:
                                valid_count += 1
                                QMessageBox.warning(QMessageBox(), "Warning", "Target SAS id must be specified")

                        if len(self.setup_model.targetSASids) == 0:
                            valid_count += 1
                            QMessageBox.warning(QMessageBox(), "Warning", "Target SAS id must be specified")
                        if len(self.setup_model.Target_name) == 0:
                            valid_count += 1
                            QMessageBox.warning(QMessageBox(), "Warning", "Target name must be specified")

        if self.setup_model.process == "True" and self.setup_model.which_obj == "calibrators":
            valid_count += process_valid()

        if self.setup_model.process == "True" and self.setup_model.which_obj == "target":
            valid_count += process_valid()
            if len(self.setup_model.targetSASids) != 0 and self.setup_model.PROJECTid == "MSSS_HBA_2013":
                targetSASids = [t.strip() for t in self.setup_model.targetSASids.split(",")]

                for id in targetSASids:
                    calibrator_id = int(id) -1
                    cal_solution_file = self.setup_model.WorkingPath + "/" + self.setup_model.Target_name + "/" + "calibrators/calibrators_results/results/cal_values_" + str(calibrator_id) + "/" + "cal_solutions.h5"
                    if not os.path.isfile(cal_solution_file):
                        valid_count += 1
                        QMessageBox.warning(QMessageBox(), "Warning", "calibrator solution file " + cal_solution_file + " do not exits")

        if self._ui.select_subband_range_combobox.currentText() == "True":
            if int(self._ui.min_subband_input.text()) >= int(self._ui.max_subband_input.text()):
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "min subband cannot be equal or smaller that max subband")
            else:
                if len(self.setup_model.min_subband) > 0:
                    if int(self.setup_model.min_subband) < 0:
                        valid_count += 1
                        QMessageBox.warning(QMessageBox(), "Warning", "Min subband cannot be negative")

                if len(self.setup_model.max_subband) > 0:
                    if int(self.setup_model.max_subband) < 0:
                        valid_count += 1
                        QMessageBox.warning(QMessageBox(), "Warning", "Min subband cannot be negative")

        if self._ui.select_frequency_range_combobox.currentText() == "True":
            if float(self._ui.min_frequency_input.text()) >= float(self._ui.max_frequency_input.text()):
                valid_count += 1
                QMessageBox.warning(QMessageBox(), "Warning", "min frequency cannot be equal or smaller that max frequency")
            else:
                if len(self.setup_model.min_frequency) > 0:
                    if float(self.setup_model.min_frequency) < 0:
                        valid_count += 1
                        QMessageBox.warning(QMessageBox(), "Warning", "Max frequency cannot be negative")

                if len(self.setup_model.max_frequency) > 0:
                    if float(self.setup_model.max_frequency) < 0:
                        valid_count += 1
                        QMessageBox.warning(QMessageBox(), "Warning", "Max frequency cannot be negative")

        if valid_count == 0:
            valid = True
        else:
            valid = False
        return valid

    def save_configuration(self):
        if self.__validate_setup():
            config_file = "config.cfg"
            setConfigs("Data", "targetSASids", self.setup_model.targetSASids, config_file)
            setConfigs("Data", "calibratorsasids", self.setup_model.calibratorSASids, config_file)
            setConfigs("Data", "targetname", self.setup_model.Target_name, config_file)
            setConfigs("Data", "projectid", self.setup_model.PROJECTid, config_file)
            setConfigs("Data", "producttype", self.setup_model.product_type, config_file)
            setConfigs("Data", "minSubband", self.setup_model.min_subband, config_file)
            setConfigs("Data", "maxSubband", self.setup_model.max_subband, config_file)
            setConfigs("Data", "subbandselect", self.setup_model.subband_select, config_file)
            setConfigs("Data", "minFrequency", self.setup_model.min_frequency, config_file)
            setConfigs("Data", "maxFrequency", self.setup_model.max_frequency, config_file)
            setConfigs("Data", "frequencyselect", self.setup_model.frequency_select, config_file)

            setConfigs("Operations", "querying", self.setup_model.querying, config_file)
            setConfigs("Operations", "stage", self.setup_model.stage, config_file)
            setConfigs("Operations", "retrieve", self.setup_model.retrieve, config_file)
            setConfigs("Operations", "process", self.setup_model.process, config_file)
            setConfigs("Operations", "which_obj", self.setup_model.which_obj, config_file)

            setConfigs("Cluster", "max_per_node", self.setup_model.max_per_node, config_file)
            setConfigs("Cluster", "method", self.setup_model.method, config_file)

            setConfigs("Paths", "workingpath", self.setup_model.WorkingPath, config_file)
            setConfigs("Paths", "prefactorpath", self.setup_model.PrefactorPath, config_file)
            setConfigs("Paths", "lofarroot", self.setup_model.lofarroot, config_file)
            setConfigs("Paths", "casaroot", self.setup_model.casaroot, config_file)
            setConfigs("Paths", "pyraproot", self.setup_model.pyraproot, config_file)
            setConfigs("Paths", "hdf5root", self.setup_model.hdf5root, config_file)
            setConfigs("Paths", "wcsroot", self.setup_model.wcsroot, config_file)
            setConfigs("Paths", "losotopath", self.setup_model.losotoPath, config_file)
            setConfigs("Paths", "aoflagger", self.setup_model.aoflagger, config_file)
            setConfigs("Paths", "wsclean_executable", self.setup_model.wsclean_executable, config_file)
            setConfigs("Paths", "pythonpath", self.setup_model.pythonpath, config_file)
            setConfigs("Paths", "task_file", self.setup_model.task_file, config_file)
            QMessageBox.about(QMessageBox(), "", "LAnDmARk configuration has been saved")

    def init_color_setup(self):
        self._ui.WorkingPath_input.setStyleSheet("Background-color: rgb(152,251,152)")
        self._ui.Target_name_input.setStyleSheet("Background-color: rgb(152,251,152)")
        self._ui.targetSASids_input.setStyleSheet("Background-color: rgb(152,251,152)")
        self._ui.PROJECTid_input.setStyleSheet("Background-color: rgb(152,251,152)")

    def on_querying_combobox_changed(self):
        if self._ui.querying_comboBox.currentText() == "True":
            self.init_color_setup()
            self.run_ui.show_query_progress_button.setStyleSheet("background-color: yellow")
            self.run_ui.show_query_progress_button.setDisabled(False)
        elif self._ui.querying_comboBox.currentText() == "False":
            self.run_ui.show_query_progress_button.setDisabled(True)
            self.run_ui.show_query_progress_button.setStyleSheet("background-color: white")

    def on_stage_combobox_changed(self):
        if self._ui.stage_combobox.currentText() == "True":
            self.init_color_setup()
            self.run_ui.show_stage_progress_button.setStyleSheet("background-color: yellow")
            self.run_ui.show_stage_progress_button.setDisabled(False)
        elif self._ui.stage_combobox.currentText() == "False":
            self.run_ui.show_stage_progress_button.setDisabled(True)
            self.run_ui.show_stage_progress_button.setStyleSheet("background-color: white")

    def on_retrieve_combobox_changed(self):
        if self._ui.retrieve_combobox.currentText() == "True":
            self.init_color_setup()
            self.run_ui.show_retrieve_progress_button.setStyleSheet("background-color: yellow")
            self.run_ui.show_retrieve_progress_button.setDisabled(False)
        elif self._ui.retrieve_combobox.currentText() == "False":
            self.run_ui.show_retrieve_progress_button.setDisabled(True)
            self.run_ui.show_retrieve_progress_button.setStyleSheet("background-color: white")

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

            self.run_ui.show_process_progress_button.setStyleSheet("background-color: yellow")
            self.run_ui.show_process_progress_button.setDisabled(False)

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

            self.run_ui.show_process_progress_button.setDisabled(True)
            self.run_ui.show_process_progress_button.setStyleSheet("background-color: white")

    def on_select_subband_range_combobox_changed(self):
        if self._ui.select_subband_range_combobox.currentText() == "True":
            self._ui.select_frequency_range_combobox.setCurrentText("False")
            self._ui.min_subband_label.setEnabled(True)
            self._ui.min_subband_input.setEnabled(True)
            self._ui.max_subband_label.setEnabled(True)
            self._ui.max_subband_input.setEnabled(True)

            if int(self._ui.min_subband_input.text()) >= int(self._ui.max_subband_input.text()):
                QMessageBox.warning(QMessageBox(), "Warning", "min subband cannot be equal or smaller that max subband")
            else:
                if len(self._ui.min_subband_input.text()) > 0:
                    if int(self._ui.min_subband_input.text()) < 0:
                        QMessageBox.warning(QMessageBox(), "Warning", "Subband cannot be negative")

                if len(self._ui.max_subband_input.text()) > 0:
                    if int(self._ui.max_subband_input.text()) < 0:
                        QMessageBox.warning(QMessageBox(), "Warning", "Subband cannot be negative")

        elif self._ui.select_subband_range_combobox.currentText() == "False":
            self._ui.select_frequency_range_combobox.setCurrentText("True")
            self._ui.min_subband_label.setEnabled(False)
            self._ui.min_subband_input.setEnabled(False)
            self._ui.max_subband_label.setEnabled(False)
            self._ui.max_subband_input.setEnabled(False)

    def on_select_frequency_range_combobox_changed(self):
        if self._ui.select_frequency_range_combobox.currentText() == "True":
            self._ui.select_subband_range_combobox.setCurrentText("False")
            self._ui.min_frequency_label.setEnabled(True)
            self._ui.min_frequency_input.setEnabled(True)
            self._ui.max_frequency_label.setEnabled(True)
            self._ui.max_frequency_input.setEnabled(True)

            if float(self._ui.min_frequency_input.text()) >= float(self._ui.max_frequency_input.text()):
                QMessageBox.warning(QMessageBox(), "Warning", "min frequency cannot be equal or smaller that max frequency")
            else:
                if len(self._ui.min_frequency_input.text()) > 0:
                    if float(self._ui.min_frequency_input.text()) < 0:
                        QMessageBox.warning(QMessageBox(), "Warning", "Frequency cannot be negative")

                if len(self._ui.max_frequency_input.text()) > 0:
                    if float(self._ui.max_frequency_input.text()) < 0:
                        QMessageBox.warning(QMessageBox(), "Warning", "Frequency cannot be negative")

        elif self._ui.select_frequency_range_combobox.currentText() == "False":
            self._ui.select_subband_range_combobox.setCurrentText("True")
            self._ui.min_frequency_label.setEnabled(False)
            self._ui.min_frequency_input.setEnabled(False)
            self._ui.max_frequency_label.setEnabled(False)
            self._ui.max_frequency_input.setEnabled(False)

