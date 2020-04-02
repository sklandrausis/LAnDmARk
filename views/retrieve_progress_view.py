import os
import pyqtgraph as pg
from PyQt5.QtWidgets import QMessageBox
from parsers._configparser import getConfigs


class RetrieveProgressPlot(pg.GraphicsWindow):
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    #pg.showGrid(x=True, y=True)
    ptr1 = 0

    def __init__(self, parent=None, **kargs):
        pg.GraphicsWindow.__init__(self, **kargs)
        self.config_file = "config.cfg"
        self.download_dir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + getConfigs("Data", "TargetName", "config.cfg") + "/"
        self.setParent(parent)
        self.setWindowTitle('Retrieved files')
        self.p1 = self.addPlot(labels={'left': 'Retrieved file count', 'bottom': 'Time'})

        self.SASidsTarget = [int(id) for id in getConfigs("Data", "targetSASids", self.config_file).replace(" ", "").split(",")]
        project = getConfigs("Data", "projectid", self.config_file)

        if len(getConfigs("Data", "calibratorSASids", self.config_file)) == 0:
            if project == "MSSS_HBA_2013":
                self.SASidsCalibrator = [id - 1 for id in self.SASidsTarget]

            else:
                raise Exception("SAS id for calibrator is not set in config.cfg file")
                sys.exit(1)
        else:
            self.SASidsCalibrator = [int(id) for id in getConfigs("Data", "calibratorSASids", self.config_file).replace(" ", "").split(",")]

        self.retrieve_files_counts = dict()
        if getConfigs("Operations", "which_obj",  self.config_file) == "calibrators":
            for id in self.SASidsCalibrator:
                self.retrieve_files_counts[id] = []

        elif getConfigs("Operations", "which_obj",  self.config_file) == "target":
            for id in self.self.SASidsTarget:
                self.retrieve_files_counts[id] = []
        else:
            for id in self.SASidsCalibrator:
                self.retrieve_files_counts[id] = []
            for id in self.self.SASidsTarget:
                self.retrieve_files_counts[id] = []

        self.time = [0]
        self.curves = []

        for id in self.retrieve_files_counts:
            self.retrieve_files_counts[id].append(0)
            curve = self.p1.plot(self.time, self.retrieve_files_counts[id], pen=(255 - 10 * 10, 0, 0))
            self.curves.append(curve)

        self.timer = pg.QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)

    def update_plot(self):
        if len(self.time) == 1:
            self.time.append(1)
        else:
            self.time.append(self.time[-1] + 1)

        for sas_id in list(self.retrieve_files_counts.keys()):
            if sas_id in self.SASidsCalibrator:
                directory = self.download_dir + "calibrators/" + str(sas_id) + "_RAW/"
            elif sas_id in self.SASidsTarget:
                directory = self.download_dir + "targets/" + str(sas_id) + "_RAW/"

            else:
                QMessageBox.warning(QMessageBox(), "Warning", "Wrong sas id", "", None)
                directory = ""

            if directory != "":
                file_count = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and ".tar" in f])
                self.retrieve_files_counts[sas_id].append(file_count)
                curve = self.curves[list(self.retrieve_files_counts.keys()).index(sas_id)]
                curve.setData(self.time, self.retrieve_files_counts[sas_id])