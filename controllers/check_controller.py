import os
from PyQt5.QtCore import QObject

from parsers._configparser import getConfigs


class CheckController(QObject):
    def __init__(self, ui, *args, **kwargs):
        super(CheckController, self).__init__(*args, **kwargs)
        self.ui = ui
        self.working_directory = getConfigs("Paths", "workingpath", "config.cfg") + "/" + getConfigs("Data", "targetname", "config.cfg")

    def choose_combobox_changed(self):
        if self.ui.choose_combobox.currentText() == "LAnDmARk inspection plots":
            self.ui.inspection_plots_combobox.clear()
            items = os.listdir(self.working_directory + "/LAnDmARk_aux/selection/")
            items.extend(os.listdir(self.working_directory + "/LAnDmARk_aux/retrieve/"))
            items.extend(os.listdir(self.working_directory + "/LAnDmARk_aux/stage/"))
            self.ui.inspection_plots_combobox.addItems(items)
        elif self.ui.inspection_plots_combobox.currentText == "Prefacotor calibrator inspection plots":
            self.ui.clear()
        elif self.ui.inspection_plots_combobox.currentText == "Prefactor target inspection plots":
            self.ui.clear()
        elif self.ui.inspection_plots_combobox.currentText == "Prefactor imaging inspection plots":
            self.ui.clear()
