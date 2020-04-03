import sys
import time
import pyqtgraph as pg
from awlofar.toolbox.LtaStager import LtaStager, LtaStagerError
from services.stager_access import get_progress, download, get_surls_online
from services.querying_service import Querying
from parsers._configparser import getConfigs


class StageProgressPlot(pg.GraphicsWindow):
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    ptr1 = 0

    def __init__(self, _ui, run_controller, **kargs):
        pg.GraphicsWindow.__init__(self, **kargs)
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
                sys.exit(1)
        else:
            self.SASidsCalibrator = [int(id) for id in getConfigs("Data", "calibratorSASids", self.config_file).replace(" ", "").split(",")]

        parent = None
        self.setParent(parent)
        self.setWindowTitle('Staged files')
        self.p1 = self.addPlot(labels={'left': 'staged file count', 'bottom': 'Time (Seconds)'})
        self.p1.showGrid(x=True, y=True)
        self.p1.setLimits(xMin=0, yMin=0)

        self.q1, self.q2 = self.__query()
        self.time = [0]

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
        i = 0
        symbols = ['o', 't', 't1', 't2', 't3', 's', 'p', 'h', 'star', '+', 'w']
        colors = [(0, 0, 200), (0, 128, 0), (19, 234, 201), (195, 46, 212), (250, 194, 5), (55, 55, 55), (0, 114, 189), (217, 83, 25), (237, 177, 32), (126, 47, 142), (119, 172, 48)]
        for index in range(0, len(stagesIDs)):
            staged_file_count_for_stage_id = [0]
            self.stages_files_counts.append(staged_file_count_for_stage_id)
            curve = self.p1.plot(self.time, self.stages_files_counts[index], symbol=symbols[i], symbolSize=30, symbolBrush=colors[i])
            self.curves.append(curve)
            i += 1

        self.timer = pg.QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)

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
                for index in range(0, len(self.get_staging_progress())):
                    stage_id = list(self.get_staging_progress().keys())[index]
                    staged_file_count_for_id = self.get_staging_progress()[stage_id]
                    self.stages_files_counts[index].append(staged_file_count_for_id)
                    curve = self.curves[index]
                    curve.setData(self.time, self.stages_files_counts[index])
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

    def __query(self):
        if getConfigs("Operations", "which_obj", self.config_file) == "calibrators":
            q1 = Querying(self.SASidsCalibrator, True, self.config_file)
            q2 = None
        elif getConfigs("Operations", "which_obj", self.config_file) == "target":
            q1 = None
            q2 = Querying(self.SASidsTarget, False, self.config_file)
        else:
            q1 = Querying(self.SASidsCalibrator, True, self.config_file)
            q2 = Querying(self.SASidsTarget, False, self.config_file)
        return q1, q2

    def start_staging(self, SURIs, SASids):
        for id in SASids:
            stagger = LtaStager()
            stagger.stage_uris(SURIs[id])

    def __retrieve(self):
        retrieve_setup = True
        while retrieve_setup:
            self.timer.stop()
            self._ui.show_stage_progress_button.setStyleSheet("background-color: gray")
            self._ui.show_stage_progress_button.setDisabled(True)
            retrieve_setup = False
        else:
            if getConfigs("Operations", "retrieve", self.config_file) == "True":
                for id in self.tmpStagesIDs:
                    surl = get_surls_online(int(id))
                    download(surl, self.download_dir, self.SASidsCalibrator, self.SASidsTarget)
