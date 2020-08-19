from enum import Enum
from PyQt5.QtCore import QObject

from parsers._configparser import getConfigs


class Status(Enum):
    not_selected = "not_selected"
    not_started = "not_started"
    started = "started"
    finished = "finished"


class Operation(QObject):
    def __init__(self):
        super().__init__()
        self.__status = Status.not_selected
        self.__name = ""
        self.config_file = "config.cfg"
        self.sas_ids_target = [int(id) for id in getConfigs("Data", "targetSASids", self.config_file).replace(" ", "").split(",")]
        self.project = getConfigs("Data", "PROJECTid", self.config_file)

        if len(getConfigs("Data", "calibratorSASids", self.config_file)) == 0:
            if self.project == "MSSS_HBA_2013":
                self.sas_ids_calibrator = [id - 1 for id in self.sas_ids_target]

            else:
                raise Exception("SAS id for calibrator is not set in config.cfg file")
        else:
            self.sas_ids_calibrator = [int(id) for id in
                                getConfigs("Data", "calibratorSASids", self.config_file).replace(" ", "").split(",")]

        self.working_dir = getConfigs("Paths", "WorkingPath", self.config_file)
        self.target_name = getConfigs("Data", "TargetName", self.config_file)
        self.working_dir = self.working_dir + "/" + self.target_name + "/"
        self.aux_dir = self.working_dir + "/LAnDmARk_aux"

    def execute(self):
        pass

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def name(self):
        return self.__name
