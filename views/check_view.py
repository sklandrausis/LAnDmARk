import os
from PyQt5.QtWidgets import QMainWindow
from views.check_view_ui import Ui_check_view
from controllers.check_controller import CheckController

from parsers._configparser import getConfigs


class CheckView(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(CheckView, self).__init__(*args, **kwargs)

        self._ui = Ui_check_view()
        self._ui.setupUi(self)
        self.check_controller = CheckController(self._ui)
        self.setWindowTitle('Check')
        self.working_directory = getConfigs("Paths", "workingpath", "config.cfg") + "/" + getConfigs("Data", "targetname", "config.cfg")

        self._ui.choose_combobox.currentTextChanged.connect(self.check_controller.choose_combobox_changed)
        items = os.listdir(self.working_directory + "/LAnDmARk_aux/selection/")
        items.extend(os.listdir(self.working_directory + "/LAnDmARk_aux/retrieve/"))
        items.extend(os.listdir(self.working_directory + "/LAnDmARk_aux/stage/"))
        self._ui.inspection_plots_combobox.addItems(items)

