import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QGridLayout, QWidget
from plotting import Plot
from parsers._configparser import getConfigs


class RetrieveProgressPlot(QWidget):
    def __init__(self, *args, **kwargs):
        super(RetrieveProgressPlot, self).__init__(*args, **kwargs)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setSpacing(10)

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

        self.retrieve_files_counts = dict()
        if getConfigs("Operations", "which_obj", self.config_file) == "calibrators":
            for sas_id in self.SASidsCalibrator:
                self.retrieve_files_counts[sas_id] = []

        elif getConfigs("Operations", "which_obj", self.config_file) == "target":
            for sas_id in self.SASidsTarget:
                self.retrieve_files_counts[sas_id] = []
        else:
            for sas_id in self.SASidsCalibrator:
                self.retrieve_files_counts[sas_id] = []
            for sas_id in self.SASidsTarget:
                self.retrieve_files_counts[sas_id] = []

        self.p1 = Plot(self)
        self.p1.set_grid(self.grid)
        self.time = [0]
        self.curves = []
        self.grid.addWidget(self.p1, 0, 0)

        symbols = ["*", "o", "v", "^", "<", ">", "1", "2", "3", "4"]
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        i = 0
        for sas_id in self.retrieve_files_counts:
            self.retrieve_files_counts[sas_id].append(0)
            curve = self.p1.graph.plot(self.time, self.retrieve_files_counts[sas_id], colors[i] + symbols[i])
            self.curves.append(curve)
            i += 1

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
                symbols = ["*", "o", "v", "^", "<", ">", "1", "2", "3", "4"]
                colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
                file_count = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
                                  and ".tar" in f])
                self.retrieve_files_counts[sas_id].append(file_count)
                self.p1.graph.plot(self.time, self.retrieve_files_counts[sas_id], colors[i] + symbols[i])
                self.p1.draw()
                i += 1
