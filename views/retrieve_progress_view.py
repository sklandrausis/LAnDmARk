import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QGridLayout, QWidget
from plotting import Plot
from parsers._configparser import getConfigs


class RetrieveProgressPlot(QWidget):
    def __init__(self, run_controller, *args, **kwargs):
        super(RetrieveProgressPlot, self).__init__(*args, **kwargs)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setSpacing(10)
        self.run_controller = run_controller
        self.setWindowTitle('Retrieved files')
        self.config_file = "config.cfg"
        self.download_dir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + \
                            getConfigs("Data", "TargetName", "config.cfg") + "/"

        self.SASidsTarget = [int(sas_id) for sas_id in getConfigs("Data", "targetSASids",
                                                                  self.config_file).replace(" ", "").split(",")]
        project = getConfigs("Data", "projectid", self.config_file)

        if len(getConfigs("Data", "calibratorSASids", self.config_file)) == 0:
            if project == "MSSS_HBA_2013":
                self.SASidsCalibrator = [sas_id - 1 for sas_id in self.SASidsTarget]

            else:
                raise Exception("SAS id for calibrator is not set in config.cfg file")
        else:
            self.SASidsCalibrator = [int(sas_id) for sas_id in getConfigs("Data", "calibratorSASids",
                                                                          self.config_file).replace(" ", "").split(",")]

        for q in (self.run_controller.q1, self.run_controller.q2):
            if q is not None:
                if len(q.valid_files) == 0:
                    q.get_SURI()

        self.retrieve_files_counts = dict()
        self.retrieve_files_percent = dict()
        if getConfigs("Operations", "which_obj", self.config_file) == "calibrators":
            for sas_id in self.SASidsCalibrator:
                self.retrieve_files_counts[sas_id] = []
                self.retrieve_files_percent[sas_id] = []

        elif getConfigs("Operations", "which_obj", self.config_file) == "target":
            for sas_id in self.SASidsTarget:
                self.retrieve_files_counts[sas_id] = []
                self.retrieve_files_percent[sas_id] = []
        else:
            for sas_id in self.SASidsCalibrator:
                self.retrieve_files_counts[sas_id] = []
                self.retrieve_files_percent[sas_id] = []
            for sas_id in self.SASidsTarget:
                self.retrieve_files_counts[sas_id] = []
                self.retrieve_files_percent[sas_id] = []

        self.time = [0]

        self.p1 = Plot(self)
        self.p1.set_grid(self.grid, 1, 0)
        self.p1.graph.set_xlabel("Time (seconds)")
        self.p1.graph.set_ylabel("Retrieved file count")
        self.grid.addWidget(self.p1, 0, 0)

        self.p2 = Plot(self)
        self.p2.set_grid(self.grid, 1, 1)
        self.p2.graph.set_xlabel("Time (seconds)")
        self.p2.graph.set_ylabel("Retrieved file percent")
        self.grid.addWidget(self.p2, 0, 1)

        symbols = ["*", "o", "v", "^", "<", ">", "1", "2", "3", "4"]
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        i = 0

        for sas_id in self.retrieve_files_counts:
            self.retrieve_files_counts[sas_id].append(0)
            self.retrieve_files_percent[sas_id].append(0)
            self.p1.graph.plot(self.time, self.retrieve_files_counts[sas_id], colors[i] + symbols[i], label=str(sas_id))
            self.p2.graph.plot(self.time, self.retrieve_files_percent[sas_id], colors[i] + symbols[i], label=str(sas_id))
            i += 1

        self.p1.legend()
        self.p2.legend()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        if len(self.time) == 1:
            self.time.append(1)
        else:
            self.time.append(self.time[-1] + 1)

        i = 0
        for sas_id in list(self.retrieve_files_counts.keys()):
            if sas_id in self.SASidsCalibrator:
                directory = self.download_dir + "calibrators/" + str(sas_id) + "_RAW/"
            elif sas_id in self.SASidsTarget:
                directory = self.download_dir + "targets/" + str(sas_id) + "_RAW/"

            else:
                QMessageBox.warning(QMessageBox(), "Warning", "Wrong sas id", "", None)
                directory = ""

            if directory != "":
                if sas_id in self.run_controller.q1.valid_files.keys():
                    valid_files = self.run_controller.q1.valid_files
                elif sas_id in self.run_controller.q2.get_SURI().keys():
                    valid_files = self.run_controller.q2.valid_files

                symbols = ["*", "o", "v", "^", "<", ">", "1", "2", "3", "4"]
                colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
                file_count = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
                                  and ".tar" in f or ".MS" in f])
                self.retrieve_files_counts[sas_id].append(file_count)
                self.p1.graph.plot(self.time, self.retrieve_files_counts[sas_id], colors[i] + symbols[i], label=str(sas_id))
                self.p1.draw()
                self.retrieve_files_percent[sas_id].append(file_count/valid_files[sas_id])
                self.p2.graph.plot(self.time, self.retrieve_files_percent[sas_id], colors[i] + symbols[i], label=str(sas_id))
                self.p2.draw()
                i += 1
