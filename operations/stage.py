import os
from operations.operation import Operation
from parsers._configparser import getConfigs


class Stage(Operation):
    def __init__(self):
        Operation.__init__(self)
        self.__name = "stage"
        self.config_file = "config.cfg"
        sas_ids_target = [int(id) for id in getConfigs("Data", "targetSASids", self.config_file).replace(" ", "").split(",")]
        project = getConfigs("Data", "PROJECTid", self.config_file)

        if len(getConfigs("Data", "calibratorSASids", self.config_file)) == 0:
            if project == "MSSS_HBA_2013":
                self.sas_ids_calibrator = [id - 1 for id in sas_ids_target]

            else:
                raise Exception("SAS id for calibrator is not set in config.cfg file")
        else:
            self.sas_ids_calibrator = [int(id) for id in
                                  getConfigs("Data", "calibratorSASids",
                                             self.config_file).replace(" ", "").split(",")]

    def execute(self):
        os.system("python3 operations/staging.py")

    @property
    def name(self):
        return self.__name
