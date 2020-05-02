import sys
import os
import threading
from PyQt5.QtWidgets import QMainWindow, QProgressBar, QLabel
from PyQt5 import QtCore
from parsers._configparser import getConfigs


def get_pipeline_task(prefactor_path, parset_file):
    tasks = []
    file = prefactor_path + "/" + parset_file
    with open(file) as parset_file:
        lines = parset_file.readlines()
        for line in lines:
            if "pipeline.steps." in line:
                tasks_tmp = [t.strip() for t in line.split("=")[-1].replace("[", "").replace("]", "").replace("{", "").replace("}","").strip().split(",")]
                tasks.extend(tasks_tmp)
    return tasks


def get_tasks_from_log_file(log_file):
    tasks = []
    if os.path.isfile(log_file):
        with open(log_file, "rb") as parset_file:
            lines = parset_file.readlines()
            for line in lines:
                line = line.decode("utf-8")
                if "Beginning step" in line:
                    task = line.split(":")[-1].split(" ")[-1].replace("\n", "")
                    tasks.append(task.strip())

    return tasks


class ProcessView(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(ProcessView, self).__init__(*args, **kwargs)
        self.progress_bars = []
        self.task_labels = []
        self.progress_bars_index = 0
        self.progress = 0
        self.config_file = "config.cfg"
        workingDir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + getConfigs("Data", "TargetName", "config.cfg") + "/"
        self.calibratorDir = workingDir + "calibrators" + "/"
        self.targetDir = workingDir + "targets" + "/"
        self.imageDir = workingDir + "imaging_deep" + "/"
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.steps = []
        self.threads = []

        prefactor_path = getConfigs("Paths", "prefactorpath", self.config_file)
        calibrator_parset_file = "Pre-Facet-Calibrator.parset"
        target_parset_file = "Pre-Facet-Target.parset"
        imaging_parset_file = "Pre-Facet-Image.parset"

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

        self.timer.timeout.connect(self.update_progress_bar)
        threading.Thread(target=self.timer.start()).start()

        if getConfigs("Operations", "which_obj", "config.cfg") == "all" or len(getConfigs("Operations", "which_obj", "config.cfg")) == 0:
            self.calibrator_tasks = get_pipeline_task(prefactor_path, calibrator_parset_file)
            self.target_tasks = get_pipeline_task(prefactor_path, target_parset_file)
            self.imaging_tasks = get_pipeline_task(prefactor_path, imaging_parset_file)
            ids = self.SASidsCalibrator.extend(self.SASidsTarget)
            ids = ids.extend("imaging")
            self.create_init_view(ids)

            for id in ids:
                step = 0
                self.steps.append(step)

        elif getConfigs("Operations", "which_obj", "config.cfg") == "targets":
            self.target_tasks = get_pipeline_task(prefactor_path, target_parset_file)
            self.create_init_view(self.SASidsTarget)
            self.ids = self.SASidsTarget

            for id in self.SASidsTarget:
                step = 0
                self.steps.append(step)

        else:
            self.calibrator_tasks = get_pipeline_task(prefactor_path, calibrator_parset_file)
            self.create_init_view(self.SASidsCalibrator)
            self.ids = self.SASidsCalibrator

            for id in self.SASidsCalibrator:
                step = 0
                self.steps.append(step)

        threading.Thread(target=os.system, args=(" ./run_pipelines.py", )).start()

    def create_init_view(self, SAS_ids):
        y_l = 10
        y_p = 50

        for id in SAS_ids:
            if id in self.SASidsCalibrator:
                msg = "Progress for calibrator pipeline for SAS id " + str(id)
            elif id in self.SASidsTarget:
                msg = "Progress for target pipeline for SAS id " + str(id)

            else:
                msg = "Progress for imaging pipeline"

            self.progress_label = QLabel(self)
            self.progress_label.setText(msg)
            self.progress_label.setGeometry(10, y_l, 280, 25)

            self.progress_bar = QProgressBar(self)
            self.progress_bar.setGeometry(10, y_p, 280, 25)
            self.progress_bars.append(self.progress_bar)

            self.task_label = QLabel(self)
            self.task_label.setText("Pipeline is not started")
            self.task_label.setGeometry(300, y_p, 500, 25)
            self.task_labels.append(self.task_label)

            y_l += 70
            y_p += 70

        self.setGeometry(10, 20, len("Running progress for SAS id ") + 560, 90 * len(SAS_ids))

    def update_progress_bar(self):
        if sum(self.steps)/len(self.steps) >= 100.0:
            self.timer.stop()

        for id in self.ids:
            if id in self.SASidsCalibrator:
                log_file = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + \
                           getConfigs("Data", "TargetName", "config.cfg") + "/" + "calibrators/" + "pipeline_" + str(id) + ".log"
            elif id in self.SASidsTarget:
                log_file = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + \
                           getConfigs("Data", "TargetName", "config.cfg") + "/" + "target/" + "pipeline_" + str(id) + ".log"

            else:
                log_file = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + \
                           getConfigs("Data", "TargetName", "config.cfg") + "/" + "imaging_deep/" + "pipeline_" + str(id) + ".log"

            progress_bars_index = self.ids.index(id)

            executed_tasks = get_tasks_from_log_file(log_file)
            if len(executed_tasks) == 0:
                last_started_task = "not started"
            else:
                last_started_task = executed_tasks[-1]

            if last_started_task is not "not started":
                try:
                    self.progress = len(executed_tasks)
                    self.steps[progress_bars_index] = self.get_progress_value(id)
                    self.progress_bars[progress_bars_index].setValue(self.steps[progress_bars_index])
                    self.task_labels[progress_bars_index].setText("Prefactor started to execute task: " + last_started_task)
                except ValueError as e:
                    print("ValueError", e, sys.exc_info()[0])

    def get_progress_value(self, id):
        if id in self.SASidsCalibrator:
            return (self.progress / len(self.calibrator_tasks)) * 100
        elif id in self.SASidsTarget:
            return (self.progress / len(self.target_tasks)) * 100
        else:
            return(self.progress/len(self.imaging_tasks)) * 100
