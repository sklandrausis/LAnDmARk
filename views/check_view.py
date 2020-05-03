import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from views.check_view_ui import Ui_check_view
from controllers.check_controller import CheckController

from parsers._configparser import getConfigs


class CheckView(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(CheckView, self).__init__(*args, **kwargs)

        self._ui = Ui_check_view()
        self._ui.setupUi(self)
        self.check_controller = CheckController(self)
        self.setWindowTitle('Check')
        self._ui.choose_combobox.currentTextChanged.connect(self.check_controller.on_choose_combobox_changed)
        self._ui.inspection_plots_combobox.currentTextChanged.connect(self.check_controller.on_inspection_plots_combobox_changed)

        self.config_file = "config.cfg"
        self.working_directory = getConfigs("Paths", "workingpath", "config.cfg") + "/" + getConfigs("Data", "targetname", "config.cfg")
        project = getConfigs("Data", "PROJECTid", self.config_file)

        targetSASids = getConfigs("Data", "targetSASids", self.config_file).replace(" ", "").split(",")
        if len(getConfigs("Data", "calibratorSASids", self.config_file)) == 0:
            if project == "MSSS_HBA_2013":
                SASidsCalibrator = [int(id) - 1 for id in targetSASids]

            else:
                raise Exception("SAS id for calibrator is not set in config.cfg file")
        else:
            SASidsCalibrator = [int(id) for id in getConfigs("Data", "calibratorSASids", self.config_file).replace(" ", "").split(",")]

        dirs = ["selection/", "retrieve/",  "stage/"]
        dirs = [self.working_directory + "/LAnDmARk_aux/" + d for d in dirs]

        for id in SASidsCalibrator:
            dirs.append(self.working_directory + "/calibrators/calibrators_results/results/inspection_" + str(id))

        for id in targetSASids:
            dirs.append(self.working_directory + "/targets/target_results/results/inspection_" + str(id))

        existing_dirs = [d for d in dirs if os.path.isdir(d)]
        non_empty_dirs = [d for d in existing_dirs if len(os.listdir(d)) != 0]
        dir_length = [len(os.listdir(d)) for d in existing_dirs]

        self._ui.choose_combobox.clear()
        for d in non_empty_dirs:
            if "LAnDmARk" in d:
                self._ui.choose_combobox.addItem("LAnDmARk inspection plots")

            for id in SASidsCalibrator:
                if str(id) in d:
                    self._ui.choose_combobox.addItem("Prefacotor calibrator inspection plots for SAS id " + str(id))

            for id in targetSASids:
                if str(id) in d:
                    self._ui.choose_combobox.addItem("Prefactor target inspection plots for SAS id " + str(id))

        if sum(dir_length) == 0:
            self._ui.inspection_plot.setText("No inspection plot available")
        else:
            items = []
            image = self._ui.inspection_plots_combobox.currentText()
            if "LAnDmARk" in self._ui.choose_combobox.currentText():
                for d in non_empty_dirs:
                    if "LAnDmARk" in d:
                        items.extend(os.listdir(d))

                path = self.working_directory + "/LAnDmARk_aux/" + [d for d in os.listdir(self.working_directory + "/LAnDmARk_aux/") if image in os.listdir(self.working_directory + "/LAnDmARk_aux/" + d)][0] + "/"
                self.set_image(path + image)

            for id in SASidsCalibrator:
                if str(id) in self._ui.choose_combobox.currentText():
                    for d in non_empty_dirs:
                        if str(id) in d:
                            items = os.listdir(d)
                            path = d + "/"
                            self.set_image(path + image)

            for id in targetSASids:
                if str(id) in self._ui.choose_combobox.currentText():
                    for d in non_empty_dirs:
                        if str(id) in d:
                            items = os.listdir(d)
                            path = d
                            self.set_image(path + image)

            self._ui.inspection_plots_combobox.clear()
            self._ui.inspection_plots_combobox.addItems(items)

    def set_image(self, image):
        self.pixmap = QPixmap(image)
        img = self.pixmap.scaled(self._ui.inspection_plot.size(), Qt.KeepAspectRatio, Qt.FastTransformation)
        self._ui.inspection_plot.setPixmap(img)


