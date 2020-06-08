import os
from PyQt5.QtCore import QObject

from parsers._configparser import getConfigs


class CheckController(QObject):
    def __init__(self, check_view, *args, **kwargs):
        super(CheckController, self).__init__(*args, **kwargs)
        os.sync()
        self.check_view = check_view
        self.ui = self.check_view._ui
        self.config_file = "config.cfg"
        self.working_directory = getConfigs("Paths", "workingpath", "config.cfg") + "/" + getConfigs("Data", "targetname", "config.cfg")

        self.project = getConfigs("Data", "PROJECTid", self.config_file)
        self.targetSASids = getConfigs("Data", "targetSASids", self.config_file).replace(" ", "").split(",")
        if len(getConfigs("Data", "calibratorSASids", self.config_file)) == 0:
            if self.project == "MSSS_HBA_2013":
                self.SASidsCalibrator = [int(id) - 1 for id in self.targetSASids]

            else:
                raise Exception("SAS id for calibrator is not set in config.cfg file")
        else:
            self.SASidsCalibrator = [int(id) for id in
                                getConfigs("Data", "calibratorSASids", self.config_file).replace(" ", "").split(",")]

        dirs = ["selection/", "retrieve/", "stage/"]
        dirs = [self.working_directory + "/LAnDmARk_aux/" + d for d in dirs]

        for id in self.SASidsCalibrator:
            dirs.append(self.working_directory + "/calibrators/calibrators_results/results/inspection_" + str(id))

        for id in self.targetSASids:
            dirs.append(self.working_directory + "/targets/target_results/results/inspection_" + str(id))

        dirs = ["selection/", "retrieve/", "stage/"]
        dirs = [self.working_directory + "/LAnDmARk_aux/" + d for d in dirs]

        for id in self.SASidsCalibrator:
            dirs.append(self.working_directory + "/calibrators/calibrators_results/results/inspection_" + str(id))

        for id in self.targetSASids:
            dirs.append(self.working_directory + "/targets/target_results/results/inspection_" + str(id))

        existing_dirs = [d for d in dirs if os.path.isdir(d)]
        self.non_empty_dirs = [d for d in existing_dirs if len(os.listdir(d)) != 0]

    def on_choose_combobox_changed(self):
        items = []
        if "LAnDmARk" in self.ui.choose_combobox.currentText():
            for d in self.non_empty_dirs:
                if "LAnDmARk" in d:
                    items.extend(os.listdir(d))

        for id in self.SASidsCalibrator:
            if str(id) in self.ui.choose_combobox.currentText():
                for d in self.non_empty_dirs:
                    if str(id) in d:
                        items = os.listdir(d)

        for id in self.targetSASids:
            if str(id) in self.ui.choose_combobox.currentText():
                for d in self.non_empty_dirs:
                    if str(id) in d:
                        items = os.listdir(d)

        self.ui.inspection_plots_combobox.clear()
        self.ui.inspection_plots_combobox.addItems(items)

    def on_inspection_plots_combobox_changed(self):
        image = self.ui.inspection_plots_combobox.currentText()
        path = self.working_directory

        if "LAnDmARk" in self.ui.choose_combobox.currentText():
            path += "/LAnDmARk_aux/"
            sub_path = [d for d in os.listdir(path) if image in os.listdir(path + "/" + d)]
            if len(sub_path) != 0:
                path += sub_path[0] + "/"
                self.check_view.set_image(path + image)

        else:
            for id in self.SASidsCalibrator:
                if str(id) in self.ui.choose_combobox.currentText():
                    for d in self.non_empty_dirs:
                        if str(id) in d:
                            path = d + "/"
                            self.check_view.set_image(path + image)
                            break

            for id in self.targetSASids:
                if str(id) in self.ui.choose_combobox.currentText():
                    for d in self.non_empty_dirs:
                        if str(id) in d:
                            path = d + "/"
                            self.check_view.set_image(path + image)
                            break
