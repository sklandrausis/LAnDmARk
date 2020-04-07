import sys
import time
from PyQt5 import QtCore
from PyQt5.QtWidgets import QGridLayout, QWidget
from awlofar.toolbox.LtaStager import LtaStager
from services.stager_access import get_progress, download, get_surls_online
from services.querying_service import Querying
from parsers._configparser import getConfigs
from plotting import Plot


class StageProgressPlot(QWidget):

    def __init__(self, _ui, run_controller, *args, **kwargs):
        super(StageProgressPlot, self).__init__(*args, **kwargs)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setSpacing(10)
        self.config_file = "config.cfg"
        self.tmpStagesIDs = set([])
        self._ui = _ui
        self.run_controller = run_controller
        self.download_dir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + \
                            getConfigs("Data", "TargetName", "config.cfg") + "/"

        self.SASidsTarget = [int(id) for id in getConfigs("Data", "targetSASids", self.config_file).replace(" ", "").split(",")]
        project = getConfigs("Data", "PROJECTid", self.config_file)

        if len(getConfigs("Data", "calibratorSASids", self.config_file)) == 0:
            if project == "MSSS_HBA_2013":
                self.SASidsCalibrator = [id - 1 for id in self.SASidsTarget]

            else:
                raise Exception("SAS id for calibrator is not set in config.cfg file")
        else:
            self.SASidsCalibrator = [int(id) for id in getConfigs("Data", "calibratorSASids", self.config_file).replace(" ", "").split(",")]

        self.time = [0]
        self.curves = []

        self.p1 = Plot(self)
        self.p1.set_grid(self.grid, 1, 0)
        self.p1.graph.set_xlabel("Time (seconds)")
        self.p1.graph.set_ylabel("Stage file count")
        self.grid.addWidget(self.p1, 0, 0)

        self.p2 = Plot(self)
        self.p2.set_grid(self.grid, 1, 1)
        self.p2.graph.set_xlabel("Time (seconds)")
        self.p2.graph.set_ylabel("Stage file percent")
        self.grid.addWidget(self.p2, 0, 1)

        self.q1 = self.run_controller.q1
        self.q2 = self.run_controller.q2

        if self.q1 is not None:
            calibrator_SURI = self.q1.get_SURI()
        else:
            calibrator_SURI = ""

        if self.q2 is not None:
            target_SURI = self.q2.get_SURI()
        else:
            target_SURI = ""

        if calibrator_SURI is not "":
            self.start_staging(calibrator_SURI, self.SASidsCalibrator)
        if target_SURI is not "":
            self.start_staging(target_SURI, self.SASidsTarget)

        progress = get_progress()
        if progress is None:
            time.sleep(10)
            stagesIDs = list(progress.keys())

        else:
            stagesIDs = list(progress.keys())

        self.curves = []
        self.stages_files_counts = []
        self.stages_files_percent = []
        symbols = ["*", "o", "v", "^", "<", ">", "1", "2", "3", "4"]
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        i = 0
        for index in range(0, len(stagesIDs)):
            staged_file_count_for_stage_id = [0]
            self.stages_files_counts.append(staged_file_count_for_stage_id)
            self.stages_files_percent.append(staged_file_count_for_stage_id)
            self.p1.graph.plot(self.time, self.stages_files_counts[index], colors[i] + symbols[i], label=str(stagesIDs[index]))
            self.p2.graph.plot(self.time, self.stages_files_percent[index], colors[i] + symbols[i],  label=str(stagesIDs[index]))
            i += 1

        self.p1.legend()
        self.p2.legend()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        progress_dict = self.get_staging_progress()

        progress = get_progress()
        if progress is None:
            self.__retrieve()

        elif len(progress_dict) == 0:
            self.__retrieve()

        elif len(list(self.get_staging_progress().keys())) == 0:
            self.__retrieve()

        else:
            if len(self.time) == 1:
                self.time.append(1)
            else:
                self.time.append(self.time[-1] + 1)
            try:
                symbols = ["*", "o", "v", "^", "<", ">", "1", "2", "3", "4"]
                colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
                i = 0
                for index in range(0, len(self.get_staging_progress())):
                    stage_id = list(self.get_staging_progress().keys())[index]
                    staged_file_count_for_id = self.get_staging_progress()[stage_id]
                    self.stages_files_counts[index].append(staged_file_count_for_id)
                    if self.q1 is not None:
                        valid_q1 = self.q1.valid_files
                    else:
                        valid_q1 = dict()

                    if self.q2 is not None:
                        valid_q2 = self.q2.valid_files
                    else:
                        valid_q2 = dict()

                    if index in valid_q1:
                        valid = valid_q1
                    elif index in valid_q2:
                        valid = valid_q2

                    self.stages_files_percent[index].append(staged_file_count_for_id/valid[index])
                    symbols = ["*", "o", "v", "^", "<", ">", "1", "2", "3", "4"]
                    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
                    self.p1.graph.plot(self.time, self.stages_files_counts[index], colors[i] + symbols[i], label=str(stage_id))
                    self.p1.draw()
                    self.p2.graph.plot(self.time, self.stages_files_percent[index], colors[i] + symbols[i], label=str(stage_id))
                    self.p2.draw()
                    i += 1

            except KeyError as e:
                print("Key Error", e)
            except IndexError as e:
                print("Index Error", e)
            except:
                print("Unexpected error:", sys.exc_info()[0])

    def get_staging_progress(self):
        progress = get_progress()
        progress_dict = {}
        if progress is not None:
            if "tuple" not in str(type(progress)):
                stages_ids = list(progress.keys())
                for stage_id in stages_ids:
                    self.tmpStagesIDs.add(stage_id)
                    staged_file_count = progress[stage_id]["File count"]
                    progress_dict[stage_id] = float(staged_file_count)
            else:
                self.__retrieve()
        else:
            self.__retrieve()

        return progress_dict

    def start_staging(self, SURIs, SASids):
        for id in SASids:
            stagger = LtaStager()
            stagger.stage_uris(SURIs[id])

    def __retrieve(self):
        retrieve_setup = True
        while retrieve_setup:
            self.timer.stop()
            workingDir = getConfigs("Paths", "WorkingPath", self.config_file)
            targetName = getConfigs("Data", "TargetName", self.config_file)
            workingDir = workingDir + "/" + targetName + "/"
            auxDir = workingDir + "/LAnDmARk_aux"
            self.p1.fig.savefig(auxDir + "/stage/" + 'staging_progress_count.png')
            self.p2.fig.savefig(auxDir + "/stage/" + 'staging_progress_percent.png')
            self._ui.show_stage_progress_button.setStyleSheet("background-color: gray")
            self._ui.show_stage_progress_button.setDisabled(True)
            retrieve_setup = False
        else:
            if getConfigs("Operations", "retrieve", self.config_file) == "True":
                for id in self.tmpStagesIDs:
                    surl = get_surls_online(int(id))
                    download(surl, self.download_dir, self.SASidsCalibrator, self.SASidsTarget)
