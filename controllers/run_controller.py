import sys
from threading import Thread
from PyQt5.QtCore import QObject
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import numpy as np
from views.query_view import QueryView
from services.querying_service import Querying
from views.stage_progress_view import StageProgressPlot
from views.retrieve_progress_view import RetrieveProgressPlot
from views.process_view import ProcessView
from parsers._configparser import getConfigs

sns.set()
rcParams["font.size"] = 18
rcParams["legend.fontsize"] = "xx-large"
rcParams["ytick.major.size"] = 14
rcParams["xtick.major.size"] = 14
rcParams["axes.labelsize"] = 18


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
        workingDir = getConfigs("Paths", "WorkingPath", self.config_file)
        targetName = getConfigs("Data", "TargetName", self.config_file)
        workingDir = workingDir + "/" + targetName + "/"
        auxDir = workingDir + "/LAnDmARk_aux"

        while querying_setup:
            Thread(target=self.query_view.show()).start()
            querying_setup = False
        else:
            if not self.query_done:
                while querying_setup2:
                    station_count_querying_thread = Thread(target=self.query_station_count())
                    station_count_querying_thread.start()
                    station_count_querying_thread.join()

                    width = 0.35
                    ind = np.arange(0, len(self.SASidsTarget))
                    fig = plt.figure("Number of stations", figsize=(50, 50))

                    def plot_station_count_calibrator():
                        axc = fig.add_subplot(1, 2, 2)
                        station_count_q1 = self.q1.get_station_count()
                        cStationsCalibrator = []
                        rStationsCalibrator = []
                        iStationsCalibrator = []
                        tStationsCalibrator = []


                        for id in self.SASidsCalibrator:
                            cStationsCalibrator.append(station_count_q1[id]["Core stations"])
                            rStationsCalibrator.append(station_count_q1[id]["Remote stations"])
                            iStationsCalibrator.append(station_count_q1[id]["International stations"])
                            tStationsCalibrator.append(station_count_q1[id]["Total stations"])


                        # pc4 = axc.bar(ind - width, tStationsCalibrator, width/2, color='y')
                        pc1 = axc.bar(ind, cStationsCalibrator, width, color='r', bottom=[0, 0])
                        pc2 = axc.bar(ind, rStationsCalibrator, width, color='g', bottom=cStationsCalibrator)
                        bottom_tmp = [cStationsCalibrator[b] + rStationsCalibrator[b] for b in
                                      range(0, len(cStationsCalibrator))]
                        pc3 = axc.bar(ind, iStationsCalibrator, width, color='b', bottom=bottom_tmp)
                        axc.set_xticks(ind)
                        axc.set_xticklabels((self.SASidsCalibrator))
                        axc.legend((pc1[0], pc2[0], pc3[0]), ('Core stations', 'Remote stations', 'International stations'))
                        axc.autoscale_view()
                        axc.set_title("Calibrator")
                        axc.set_xlabel("SAS id")
                        plt.grid()

                    def plot_station_count_target():
                        axt = fig.add_subplot(1, 2, 1)
                        station_count_q2 = self.q2.get_station_count()
                        cStationsTarget = []
                        rStationsTarget = []
                        iStationsTarget = []
                        tStationsTarget = []

                        for id in self.SASidsTarget:
                            cStationsTarget.append(station_count_q2[id]["Core stations"])
                            rStationsTarget.append(station_count_q2[id]["Remote station"])
                            iStationsTarget.append(station_count_q2[id]["International stations"])
                            tStationsTarget.append(station_count_q2[id]["Total stations"])

                        # pt4 = axt.bar(ind - width, tStationsTarget, width/2, color='y')
                        pt1 = axt.bar(ind, cStationsTarget, width, color='r', bottom=[0, 0])
                        pt2 = axt.bar(ind, rStationsTarget, width, color='g', bottom=cStationsTarget)
                        bottom_tmp = [cStationsTarget[b] + rStationsTarget[b] for b in range(0, len(cStationsTarget))]
                        pt3 = axt.bar(ind, iStationsTarget, width, color='b', bottom=bottom_tmp)
                        axt.set_xticks(ind)
                        axt.set_xticklabels((self.SASidsTarget))
                        axt.legend((pt1[0], pt2[0], pt3[0]), ('Core stations', 'Remote stations', 'International stations'))
                        axt.autoscale_view()
                        axt.set_title("Target")
                        axt.set_xlabel("SAS id")
                        plt.grid()

                    if getConfigs("Operations", "which_obj", self.config_file) == "calibrators":
                        plot_station_count_calibrator()

                    elif getConfigs("Operations", "which_obj", self.config_file) == "target":
                        plot_station_count_target()

                    elif getConfigs("Operations", "which_obj", self.config_file) == "all":
                        plot_station_count_calibrator()
                        plot_station_count_target()

                    plt.savefig(auxDir + "/selection/" + "station_count_per_sas_id.png")
                    querying_setup2 = False
                else:
                    self.query_data_products()

                    plt.figure("Percent of valid data", figsize=(25, 25))

                    def plot_valid_files_calibrator():
                        valid_files = self.q1.get_valid_file()
                        invalid_files = self.q1.get_invalid_file()
                        ratiosCalibrator = []
                        for id in self.SASidsCalibrator:
                            ratiosCalibrator.append(valid_files[id] / (valid_files[id] + invalid_files[id]))

                        plt.subplot(1, 2, 2)
                        plt.bar(self.SASidsCalibrator, np.array(ratiosCalibrator) * 100, color='g')
                        plt.xticks(self.SASidsCalibrator, self.SASidsCalibrator)
                        plt.xlabel("SAS id")
                        plt.ylabel("Percent")
                        plt.title("Calibrator")
                        plt.grid()

                    def plot_valid_files_target():
                        valid_files = self.q2.get_valid_file()
                        invalid_files = self.q2.get_invalid_file()
                        ratiosTarget = []
                        for id in self.SASidsTarget:
                            ratiosTarget.append(valid_files[id] / (valid_files[id] + invalid_files[id]))

                        plt.subplot(1, 2, 1)
                        plt.bar(self.SASidsTarget, np.array(ratiosTarget) * 100, color='g')
                        plt.xticks(self.SASidsTarget, self.SASidsTarget)
                        plt.xlabel("SAS id")
                        plt.ylabel("Percent")
                        plt.title("Target")
                        plt.grid()

                    if getConfigs("Operations", "which_obj", self.config_file) == "calibrators":
                        plot_valid_files_calibrator()

                    elif getConfigs("Operations", "which_obj", self.config_file) == "target":
                        plot_valid_files_target()

                    elif getConfigs("Operations", "which_obj", self.config_file) == "all":
                        plot_valid_files_calibrator()
                        plot_valid_files_target()

                    plt.savefig(auxDir + "/selection/" + "valid_data_per_sas_id.png")
                    querying_setup2 = False

            self.query_done = True
            self._ui.show_query_progress_button.setStyleSheet(self.done_color)

    def query_station_count(self,):
        if self.q1 is None:
            msg = self.q2.get_station_count_message()
            self.query_view._ui.querying_message.setText(msg)
        elif self.q2 is None:
            msg = self.q1.get_station_count_message()
            self.query_view._ui.querying_message.setText(msg)
        else:
            msg1 = self.q1.get_station_count_message()
            self.query_view._ui.querying_message.setText(msg1)

            msg2 = self.q2.get_station_count_message()
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
        self.retrieve_progress_plot = RetrieveProgressPlot(self)
        self.retrieve_progress_plot.show()

    def process_progress(self):
        self.process_progress_view = ProcessView()
        self.process_progress_view.show()
