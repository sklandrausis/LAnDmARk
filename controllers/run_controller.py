import sys
from PyQt5.QtCore import QObject
from views.query_view import QueryView
from services.querying_service import Querying
from parsers._configparser import getConfigs


class RunController(QObject):
    def __init__(self, _ui):
        super().__init__()
        self.query_view = QueryView()
        self._ui = _ui
        self.config_file = "config.cfg"
        self.SASidsTarget = [int(id) for id in getConfigs("Data", "targetSASids", self.config_file).replace(" ", "").split(",")]
        project = getConfigs("Data", "PROJECTid", self.config_file)

        if len(getConfigs("Data", "calibratorSASids", self.config_file)) == 0:
            if project == "MSSS_HBA_2013":
                self.SASidsCalibrator = [id - 1 for id in self.SASidsTarget]

            else:
                raise Exception("SAS id for calibrator is not set in config.cfg file")
                sys.exit(1)
        else:
            self.SASidsCalibrator = [int(id) for id in getConfigs("Data", "calibratorSASids", self.config_file).replace(" ", "").split(",")]

    def query_progress(self):
        q1, q2 = self.__query()
        self.show_querying_results(q1, q2)

    def __query(self):
        if getConfigs("Operations", "which_obj",  self.config_file) == "calibrators":
            q1 = Querying(self.SASidsCalibrator, True, self.config_file)
            q2 = None
        elif getConfigs("Operations", "which_obj",  self.config_file) == "target":
            q1 = None
            q2 = Querying(self.SASidsTarget, False, self.config_file)
        else:
            q1 = Querying(self.SASidsCalibrator, True, self.config_file)
            q2 = Querying(self.SASidsTarget, False, self.config_file)
        return q1, q2

    def show_querying_results(self, q1, q2):
        querying_setup = True
        self.query_view.show()

        while querying_setup:
            self.query_station_count(q1, q2)
            querying_setup = False
        else:
            self.query_data_products(q1, q2)

        self._ui.show_query_progress_button.setStyleSheet("background-color: gray")
        self._ui.show_query_progress_button.setDisabled(True)

        '''
        #self.show_stage_progress_button.setStyleSheet("background-color: green")
        #self.show_stage_progress_button.setDisabled(False)
        '''

    def query_station_count(self, q1, q2):
        if q1 is None:
            msg = q2.get_station_count()
            self.query_view._ui.querying_message.setText(msg)
        elif q2 is None:
            msg = q1.get_station_count()
            self.query_view._ui.querying_message.setText(msg)
        else:
            msg1 = q1.get_station_count()
            self.query_view._ui.querying_message.setText(msg1)

            msg2 = q2.get_station_count()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg2)

    def query_data_products(self, q1, q2):
        if q1 is None:
            msg2 = q2.get_data_products()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg2)

        elif q2 is None:
            msg1 = q1.get_data_products()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg1)

        else:
            msg1 = q1.get_data_products()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg1)

            msg2 = q2.get_data_products()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg2)
