import os
from PyQt5.QtWidgets import QMainWindow, QProgressBar, QLabel
from PyQt5.QtCore import QBasicTimer
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


class ProcessView(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(ProcessView, self).__init__(*args, **kwargs)
        self.progress_bars = []
        self.progress_bars_index = 0
        self.progress = 0
        self.config_file = "config.cfg"
        workingDir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + getConfigs("Data", "TargetName", "config.cfg") + "/"
        self.calibratorDir = workingDir + "calibrators" + "/"
        self.targetDir = workingDir + "targets" + "/"
        self.imageDir = workingDir + "imaging_deep" + "/"


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

        if getConfigs("Operations", "which_obj", "config.cfg") == "all" or len(getConfigs("Operations", "which_obj", "config.cfg")) == 0:
            calibrator_tasks = get_pipeline_task(prefactor_path, calibrator_parset_file)
            target_tasks = get_pipeline_task(prefactor_path, target_parset_file)
            imaging_tasks = get_pipeline_task(prefactor_path, imaging_parset_file)

            '''
            for id in self.SASidsCalibrator:
                parsetCalib = self.calibratorDir + str(id) + "_RAW/" + "Pre-Facet-Calibrator.parset"
                configCalib = self.calibratorDir + str(id) + "_RAW/" + "pipeline.cfg"
                self.run_pipeline(parsetCalib, configCalib)  # run calibrator

            for id in self.SASidsTarget:
                parsetTarget = targetDir + str(id) + "_RAW/" + "Pre-Facet-Target.parset"
                configTarget = targetDir + str(id) + "_RAW/" + "pipeline.cfg"
                self.run_pipeline(parsetTarget, configTarget)  # run target

            parsetImage = imageDir + "Initial-Subtract.parset"
            configImage = imageDir + "pipeline.cfg"
            self.run_pipeline(parsetImage, configImage)  # run imaging
            '''

        elif getConfigs("Operations", "which_obj", "config.cfg") == "targets":
            self.tasks = get_pipeline_task(prefactor_path, target_parset_file)
            self.create_init_view(self.SASidsTarget)

            for id in self.SASidsTarget:
                parsetTarget = self.targetDir + str(id) + "_RAW/" + "Pre-Facet-Target.parset"
                configTarget = self.targetDir + str(id) + "_RAW/" + "pipeline.cfg"
                self.run_pipeline(parsetTarget, configTarget)  # run target
                self.timer.start(80, self)
                self.progress_bars_index += 1
                self.log_file = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + getConfigs("Data", "TargetName", "config.cfg") + "/" + "targets" + "pipeline_" + str(id) + ".log"

        else:
            self.tasks = get_pipeline_task(prefactor_path, calibrator_parset_file)
            self.create_init_view(self.SASidsCalibrator)

            for id in self.SASidsCalibrator:
                parsetCalib = self.calibratorDir + str(id) + "_RAW/" + "Pre-Facet-Calibrator.parset"
                configCalib = self.calibratorDir + str(id) + "_RAW/" + "pipeline.cfg"
                self.run_pipeline(parsetCalib, configCalib)  # run calibrator
                self.timer.start(80, self)
                self.progress_bars_index += 1
                self.log_file = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + getConfigs("Data", "TargetName", "config.cfg") + "/" + "calibrators" + "pipeline_" + str(id) + ".log"

        self.timer = QBasicTimer()
        self.step = 0
        self.startProgress()

    def create_init_view(self, SAS_ids):
        y_l = 10
        y_p = 50
        for id in SAS_ids:
            self.progress_label = QLabel(self)
            self.progress_label.setText("Running progress for SAS id " + str(id))
            self.progress_label.setGeometry(10, y_l, 250, 25)

            self.progress_bar = QProgressBar(self)
            self.progress_bar.setGeometry(10, y_p, 250, 25)
            self.progress_bars.append(self.progress_bar)

            y_l += 70
            y_p += 70

        self.setGeometry(10, 20, len("Running progress for SAS id ") + 250, 90 * len(SAS_ids))

    def startProgress(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(80, self)

    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            return

        self.progress = self.tasks.index(self.get_task_from_log_file())
        self.step = self.get_progress_value()
        self.progress_bars[self.progress_bars_index].setValue(self.step)

    def get_progress_value(self):
        return self.progress / len(self.tasks)

    def run_pipeline(self, parset_file, config_file):
        try:
            os.system('genericpipeline.py ' + parset_file + ' -c ' + config_file + ' -d')
        except:
            print("Something went wrong")

    def get_task_from_log_file(self):
        task = ""
        log_file = self.log_file
        with open(log_file) as parset_file:
            lines = parset_file.readlines()
            for line in lines:
                if "completed successfully" in line:
                    task = line.split(" ")[5]

        return task
