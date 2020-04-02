import sys
from threading import Thread
from PyQt5.QtCore import QObject
from views.query_view import QueryView
from services.querying_service import Querying
from views.stage_progress_view import StageProgressPlot
from views.retrieve_progress_view import RetrieveProgressPlot
from views.process_view import ProcessView
from parsers._configparser import getConfigs


class RunController(QObject):
    def __init__(self, _ui):
        super().__init__()
        self.query_view = QueryView()
        self._ui = _ui
        self.config_file = "config.cfg"
        self.query_done = False
        self.done_color = "background-color: green"
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

        self.q1, self.q2 = self.__query()

    def query_progress(self):
        self.show_querying_results()

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

    def show_querying_results(self):
        querying_setup = True
        querying_setup2 = True

        while querying_setup:
            Thread(target=self.query_view.show()).start()
            querying_setup = False
        else:
            if not self.query_done:
                while querying_setup2:
                    station_count_querying_thread = Thread(target=self.query_station_count())
                    station_count_querying_thread.start()
                    station_count_querying_thread.join()
                    querying_setup2 = False
                else:
                    self.query_data_products()

            self.query_done = True
            self._ui.show_query_progress_button.setStyleSheet(self.done_color)

    def query_station_count(self,):
        if self.q1 is None:
            msg = self.q2.get_station_count()
            self.query_view._ui.querying_message.setText(msg)
        elif self.q2 is None:
            msg = self.q1.get_station_count()
            self.query_view._ui.querying_message.setText(msg)
        else:
            msg1 = self.q1.get_station_count()
            self.query_view._ui.querying_message.setText(msg1)

            msg2 = self.q2.get_station_count()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg2)

    def query_data_products(self):
        if self.q1 is None:
            msg2 = self.q2.get_valid_file_message()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg2)

        elif self.q2 is None:
            msg1 = self.q1.get_valid_file_message()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg1)

        else:
            msg1 = self.q1.get_valid_file_message()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg1)

            msg2 = self.q2.get_valid_file_message()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg2)

    def stage_progress(self):
        self.stage_progress_plot = StageProgressPlot(self._ui, self)
        self.stage_progress_plot.show()

    def retrieve_progress(self):
        self.retrieve_progress_plot = RetrieveProgressPlot()
        self.retrieve_progress_plot.show()

    def process_progress(self):
        self.process_progress_view = ProcessView()
        self.process_progress_view.show()
