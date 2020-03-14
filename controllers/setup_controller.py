import os
from awlofar.database.Context import context
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QObject, pyqtSlot
from parsers._configparser import setConfigs


class SetupController(QObject):
    def __init__(self, setup_model):
        super().__init__()
        self.setup_model = setup_model

    @pyqtSlot(bool)
    def __validate_setup(self):
        valid_count = 0

        if self.setup_model.querying == "True" or self.setup_model.stage == "True" or self.setup_model.retrive == "True":
            if len(self.setup_model.WorkingPath) == 0:
                valid_count += 1
                QMessageBox.warning(QWidget(), "Warning", "Working path cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.WorkingPath):
                    valid_count += 1
                    QMessageBox.warning(QWidget(), "Warning", "Working path is not existing")

            if len(self.setup_model.PROJECTid) == 0:
                valid_count += 1
                QMessageBox.warning(QWidget(), "Warning", "Project ID cannot be empty")
            else:
                project = self.setup_model.PROJECTid
                context.set_project(project)

                if project != context.get_current_project().name:
                    valid_count += 1
                    QMessageBox.warning(QWidget(), "Warning", "You are not member of project")

                else:
                    if self.setup_model.which_obj == "calibrators":
                        if len(self.setup_model.calibratorSASids) == 0:
                            if project != "MSSS_HBA_2013":
                                valid_count += 1
                                QMessageBox.warning(QWidget(), "Warning", "If project is not MSSS_HBA_2013 SAS id for calibrator must be specified")
                            if len(self.setup_model.targetSASids) == 0:
                                valid_count += 1
                                QMessageBox.warning(QWidget(), "Warning", "Target SAS id must be specified")

                    elif self.setup_model.which_obj == "target":
                        if len(self.setup_model.targetSASids) == 0:
                            valid_count += 1
                            QMessageBox.warning(QWidget(), "Warning", "Target SAS id must be specified")
                        if len(self.setup_model.Target_name) == 0:
                            valid_count += 1
                            QMessageBox.warning(QWidget(), "Warning", "Target name must be specified")
                    else:
                        if len(self.setup_model.calibratorSASids) == 0:
                            if project != "MSSS_HBA_2013":
                                valid_count += 1
                                QMessageBox.warning(QWidget(), "Warning", "If project is not MSSS_HBA_2013 SAS id for calibrator must be specified")

                            if len(self.setup_model.targetSASids) == 0:
                                valid_count += 1
                                QMessageBox.warning(QWidget(), "Warning", "Target SAS id must be specified")

                        if len(self.setup_model.targetSASids) == 0:
                            valid_count += 1
                            QMessageBox.warning(QWidget(), "Warning", "Target SAS id must be specified")
                        if len(self.setup_model.Target_name) == 0:
                            valid_count += 1
                            QMessageBox.warning(QWidget(), "Warning", "Target name must be specified")

        elif self.setup_model.process == "True":
            if len(self.setup_model.WorkingPath) == 0:
                valid_count += 1
                QMessageBox.warning(QWidget(), "Warning", "Working path cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.WorkingPath):
                    valid_count += 1
                    QMessageBox.warning(QWidget(), "Warning", "Working path is not existing")

            if len(self.setup_model.PrefactorPath) == 0:
                valid_count += 1
                QMessageBox.warning(QWidget, "Warning", "Working path cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.PrefactorPath):
                    valid_count += 1
                    QMessageBox.warning(QWidget(), "Warning", "Working path is not existing")

            if len(self.setup_model.lofarroot) == 0:
                valid_count += 1
                QMessageBox.warning(QWidget(), "Warning", "LOFAR root cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.lofarroot):
                    valid_count += 1
                    QMessageBox.warning(QWidget(), "Warning", "LOFAR root is not existing")

            if len(self.setup_model.casaroot) == 0:
                valid_count += 1
                QMessageBox.warning(QWidget(), "Warning", "CASA root cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.casaroot):
                    valid_count += 1
                    QMessageBox.warning(QWidget(), "Warning", "CASA root is not existing")

            if len(self.setup_model.pyraproot) == 0:
                valid_count += 1
                QMessageBox.warning(QWidget(), "Warning", "Pyrap root cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.pyraproot):
                    valid_count += 1
                    QMessageBox.warning(QWidget, "Warning", "Pyrap root root is not existing")

            if len(self.setup_model.losotoPath) == 0:
                valid_count += 1
                QMessageBox.warning(QWidget(), "Warning", "losoto path cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.losotoPath):
                    valid_count += 1
                    QMessageBox.warning(QWidget(), "Warning", "losoto path is not existing")

            if len(self.setup_model.aoflagger) == 0:
                valid_count += 1
                QMessageBox.warning(QWidget(), "Warning", "aoflagger cannot be empty")
            else:
                if not os.path.isfile(self.setup_model.aoflagger):
                    valid_count += 1
                    QMessageBox.warning(QWidget(), "Warning", "aoflagger is not existing")

            if len(self.setup_model.aoflagger) == 0:
                valid_count += 1
                QMessageBox.warning(QWidget(), "Warning", "aoflagger cannot be empty")
            else:
                if not os.path.isfile(self.setup_model.aoflagger):
                    valid_count += 1
                    QMessageBox.warning(QWidget(), "Warning", "aoflagger is not existing")

            if len(self.setup_model.wsclean_executable) == 0:
                valid_count += 1
                QMessageBox.warning(QWidget(), "Warning", "wsclean executable cannot be empty")
            else:
                if not os.path.isfile(self.setup_model.wsclean_executable):
                    valid_count += 1
                    QMessageBox.warning(QWidget(), "Warning", "wsclean executable is not existing")

            if len(self.setup_model.task_file) == 0:
                valid_count += 1
                QMessageBox.warning(QWidget(), "Warning", "task file cannot be empty")
            else:
                if not os.path.isfile(self.setup_model.task_file):
                    valid_count += 1
                    QMessageBox.warning(QWidget(), "Warning", "task file is not existing")

            if len(self.setup_model.pythonpath) == 0:
                valid_count += 1
                QMessageBox.warning(QWidget(), "Warning", "python path cannot be empty")
            else:
                if not os.path.isdir(self.setup_model.pythonpath):
                    valid_count += 1
                    QMessageBox.warning(QWidget, "Warning", "python path is not existing")

        if valid_count == 0:
            valid = True
        else:
            valid = False
        return valid

    @pyqtSlot()
    def save_configuration(self):
        if self.__validate_setup():
            config_file = "config.cfg"
            setConfigs("Data", "targetSASids", self.setup_model.targetSASids, config_file)
            setConfigs("Data", "calibratorsasids", self.setup_model.calibratorSASids, config_file)
            setConfigs("Data", "targetname", self.setup_model.Target_name, config_file)
            setConfigs("Data", "projectid", self.setup_model.PROJECTid, config_file)
            setConfigs("Data", "producttype", self.setup_model.product_type, config_file)

            setConfigs("Operations", "querying", self.setup_model.querying, config_file)
            setConfigs("Operations", "stage", self.setup_model.stage, config_file)
            setConfigs("Operations", "retrieve", self.setup_model.retrive, config_file)
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
            QMessageBox.about(QWidget(), "", "LAnDmARk configuration has been saved")