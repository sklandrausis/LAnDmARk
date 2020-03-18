import time
import pyqtgraph as pg
from awlofar.toolbox.LtaStager import LtaStager
from services.stager_access import get_progress, download, get_surls_online
from services.querying_service import Querying
from parsers._configparser import getConfigs


class StageProgressPlot(pg.GraphicsWindow):
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    #pg.showGrid(x=True, y=True)
    ptr1 = 0

    def __init__(self, _ui, **kargs):
        pg.GraphicsWindow.__init__(self, **kargs)
        self.config_file = "config.cfg"
        self.tmpStagesIDs = set([])
        self._ui = _ui
        self.download_dir = getConfigs("Paths", "WorkingPath", "config.cfg") + "/" + getConfigs("Data", "TargetName", "config.cfg") + "/"

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
        self.p1 = self.addPlot(labels={'left':'staged file count', 'bottom':'Time'})

        q1, q2 = self.__query()
        self.query_data_products(q1,q2)

        self.time = [0]

        if q1 is not None:
            calibrator_SURI = q1.get_SURI()
        else:
            calibrator_SURI = ""

        if q2 is not None:
            target_SURI = q2.get_SURI()
        else:
            target_SURI = ""

        if calibrator_SURI is not "":
            self.start_staging(calibrator_SURI, self.SASidsCalibrator)
        if target_SURI is not "":
            self.start_staging(target_SURI, self.SASidsTarget)

        progress = get_progress()
        if progress is None:
            time.sleep(10)

        else:
            stagesIDs = list(progress.keys())

        self.curves = []
        self.stages_files_counts = []
        for index in range(0, len(stagesIDs)):
            staged_file_count_for_stageID = [0]
            self.stages_files_counts.append(staged_file_count_for_stageID)
            curve = self.p1.plot(self.time, self.stages_files_counts[index], pen=(255 - index * 10, 0, 0))
            self.curves.append(curve)

        self.timer = pg.QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)

    def update_plot(self):
        progress_dict = self.get_staging_progress()

        progress = get_progress()
        if progress is None:
            self.timer.stop()
            self._ui.show_stage_progress_button.setStyleSheet("background-color: gray")
            self._ui.show_stage_progress_button.setDisabled(True)
            self._ui.show_retrieve_progress_button.setStyleSheet("background-color: green")
            self._ui.show_retrieve_progress_button.setDisabled(False)
            for id in self.tmpStagesIDs:
                surl = get_surls_online(int(id))
                download(surl, self.download_dir, self.SASidsCalibrator, self.SASidsTarget)

        elif len(progress_dict) == 0:
            self.timer.stop()
            self._ui.show_stage_progress_button.setStyleSheet("background-color: gray")
            self._ui.show_stage_progress_button.setDisabled(True)
            self._ui.show_retrieve_progress_button.setStyleSheet("background-color: green")
            self._ui.show_retrieve_progress_button.setDisabled(False)
            for id in self.tmpStagesIDs:
                surl = get_surls_online(int(id))
                download(surl, self.download_dir, self.SASidsCalibrator, self.SASidsTarget)

        elif len(list(self.get_staging_progress().keys())) == 0:
            self.timer.stop()
            self._ui.show_stage_progress_button.setStyleSheet("background-color: gray")
            self._ui.show_stage_progress_button.setDisabled(True)
            self._ui.show_retrieve_progress_button.setStyleSheet("background-color: green")
            self._ui.show_retrieve_progress_button.setDisabled(False)
            for id in self.tmpStagesIDs:
                surl = get_surls_online(int(id))
                download(surl, self.download_dir, self.SASidsCalibrator, self.SASidsTarget)

        else:
            if len(self.time) == 1:
                self.time.append(1)
            else:
                self.time.append(self.time[-1] + 1)
            try:
                for index in range(0, len(self.get_staging_progress())):
                    stageId = list(self.get_staging_progress().keys())[index]
                    staged_file_count_for_id = self.get_staging_progress()[stageId]
                    self.stages_files_counts[index].append(staged_file_count_for_id)
                    curve = self.curves[index]
                    curve.setData(self.time, self.stages_files_counts[index])
            except IndexError:
                pass

    def get_staging_progress(self):
        progress = get_progress()
        progress_dict = {}
        if progress is not None:
            if "tuple" not in str(type(progress)):
                stagesIDs = list(progress.keys())
                for stageID in stagesIDs:
                    self.tmpStagesIDs.add(stageID)
                    staged_file_count = progress[stageID]["File count"]
                    progress_dict[stageID] = float(staged_file_count)
            else:
                self.timer.stop()
                self._ui.show_stage_progress_button.setStyleSheet("background-color: gray")
                self._ui.show_stage_progress_button.setDisabled(True)
                self._ui.show_retrieve_progress_button.setStyleSheet("background-color: green")
                self._ui.show_retrieve_progress_button.setDisabled(False)
                for id in self.tmpStagesIDs:
                    surl = get_surls_online(int(id))
                    download(surl, self.download_dir, self.SASidsCalibrator, self.SASidsTarget)
        else:
            self.timer.stop()
            self._ui.show_stage_progress_button.setStyleSheet("background-color: gray")
            self._ui.show_stage_progress_button.setDisabled(True)
            self._ui.show_retrieve_progress_button.setStyleSheet("background-color: green")
            self._ui.show_retrieve_progress_button.setDisabled(False)
            for id in self.tmpStagesIDs:
                surl = get_surls_online(int(id))
                download(surl, self.download_dir, self.SASidsCalibrator, self.SASidsTarget)

        return progress_dict

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

    def query_data_products(self, q1, q2):
        if q1 is None:
            q2.get_data_products()

        elif q2 is None:
            q1.get_data_products()

        else:
            q1.get_data_products()
            q2.get_data_products()

    def start_staging(self, SURIs, SASids):
        for id in SASids:
            stagger = LtaStager()
            stagger.stage_uris(SURIs[id])
