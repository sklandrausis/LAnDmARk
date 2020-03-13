#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import (QWidget, QGridLayout, QApplication, QDesktopWidget, QPushButton, QLabel, QComboBox, QLineEdit, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import pyqtgraph as pg
import time
from stager_access import get_progress
from awlofar.toolbox.LtaStager import LtaStager
from awlofar.database.Context import context

from parsers._configparser import setConfigs, getConfigs
from querying import Querying


class Landmark_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main")
        self.center()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setSpacing(10)
        self.create_init_view()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_init_view(self):
        self.setup_button = QPushButton("Setup", self)
        self.run_button = QPushButton("Run", self)
        self.check_button = QPushButton("Check", self)
        self.setup_button.setStyleSheet("background-color: yellow")
        self.setup_button.clicked.connect(self.setup)
        self.run_button.setStyleSheet("background-color: green")
        self.run_button.clicked.connect(self.run_landmark)
        self.check_button.setStyleSheet("background-color: blue")
        self.grid.addWidget(self.setup_button, 0,0)
        self.grid.addWidget(self.run_button, 1,0)
        self.grid.addWidget(self.check_button, 2,0)

        self.init_label = QLabel("LAnDmARk GUI")
        init_label_font = QFont("Times New Roman", 30, QFont.Bold)
        self.init_label.setFont(init_label_font)
        self.grid.addWidget(self.init_label, 1,1)

    def validate_setup(self):
        valid_count = 0

        if self.querying_combobox.currentText() == "True" or self.stage_combobox.currentText() == "True" or self.retrive_combobox.currentText() == "True":
            if len(self.WorkingPath_input.text()) == 0:
                valid_count += 1
                QMessageBox.warning(self, "Warning", "Working path cannot be empty")
            else:
                if not os.path.isdir(self.WorkingPath_input.text()):
                    valid_count += 1
                    QMessageBox.warning(self, "Warning", "Working path is not existing")

            if len(self.PROJECTid_input.text()) == 0:
                valid_count += 1
                QMessageBox.warning(self, "Warning", "Project ID cannot be empty")
            else:
                project = self.PROJECTid_input.text()
                context.set_project(project)

                if project != context.get_current_project().name:
                    valid_count += 1
                    QMessageBox.warning(self, "Warning", "You are not member of project")

                else:
                    if self.which_combobox.currentText() == "calibrators":
                        if len(self.calibratorSASids_input.text()) == 0:
                            if project != "MSSS_HBA_2013":
                                valid_count += 1
                                QMessageBox.warning(self, "Warning", "If project is not MSSS_HBA_2013 SAS id for calibrator must be specified")
                            if len(self.targetSASids_input.text()) == 0:
                                valid_count += 1
                                QMessageBox.warning(self, "Warning", "Target SAS id must be specified")

                    elif self.which_combobox.currentText() == "target":
                        if len(self.targetSASids_input.text()) == 0:
                            valid_count += 1
                            QMessageBox.warning(self, "Warning", "Target SAS id must be specified")
                        if len(self.Target_name_input.text()) == 0:
                            valid_count += 1
                            QMessageBox.warning(self, "Warning", "Target name must be specified")
                    else:
                        if len(self.calibratorSASids_input.text()) == 0:
                            if project != "MSSS_HBA_2013":
                                valid_count += 1
                                QMessageBox.warning(self, "Warning", "If project is not MSSS_HBA_2013 SAS id for calibrator must be specified")

                            if len(self.targetSASids_input.text()) == 0:
                                valid_count += 1
                                QMessageBox.warning(self, "Warning", "Target SAS id must be specified")

                        if len(self.targetSASids_input.text()) == 0:
                            valid_count += 1
                            QMessageBox.warning(self, "Warning", "Target SAS id must be specified")
                        if len(self.Target_name_input.text()) == 0:
                            valid_count += 1
                            QMessageBox.warning(self, "Warning", "Target name must be specified")

        elif self.process_combobox.currentText() == "True":
            if len(self.WorkingPath_input.text()) == 0:
                valid_count += 1
                QMessageBox.warning(self, "Warning", "Working path cannot be empty")
            else:
                if not os.path.isdir(self.WorkingPath_input.text()):
                    valid_count += 1
                    QMessageBox.warning(self, "Warning", "Working path is not existing")

            if len(self.PrefactorPath_input.text()) == 0:
                valid_count += 1
                QMessageBox.warning(self, "Warning", "Working path cannot be empty")
            else:
                if not os.path.isdir(self.PrefactorPath_input.text()):
                    valid_count += 1
                    QMessageBox.warning(self, "Warning", "Working path is not existing")

            if len(self.lofarroot_input.text()) == 0:
                valid_count += 1
                QMessageBox.warning(self, "Warning", "LOFAR root cannot be empty")
            else:
                if not os.path.isdir(self.lofarroot_input.text()):
                    valid_count += 1
                    QMessageBox.warning(self, "Warning", "LOFAR root is not existing")

            if len(self.casaroot_input.text()) == 0:
                valid_count += 1
                QMessageBox.warning(self, "Warning", "CASA root cannot be empty")
            else:
                if not os.path.isdir(self.casaroot_input.text()):
                    valid_count += 1
                    QMessageBox.warning(self, "Warning", "CASA root is not existing")

            if len(self.pyraproot_input.text()) == 0:
                valid_count += 1
                QMessageBox.warning(self, "Warning", "Pyrap root cannot be empty")
            else:
                if not os.path.isdir(self.pyraproot_input.text()):
                    valid_count += 1
                    QMessageBox.warning(self, "Warning", "Pyrap root root is not existing")

            if len(self.losotoPath_input.text()) == 0:
                valid_count += 1
                QMessageBox.warning(self, "Warning", "losoto path cannot be empty")
            else:
                if not os.path.isdir(self.losotoPath_input.text()):
                    valid_count += 1
                    QMessageBox.warning(self, "Warning", "losoto path is not existing")

            if len(self.aoflagger_input.text()) == 0:
                valid_count += 1
                QMessageBox.warning(self, "Warning", "aoflagger cannot be empty")
            else:
                if not os.path.isfile(self.aoflagger_input.text()):
                    valid_count += 1
                    QMessageBox.warning(self, "Warning", "aoflagger is not existing")

            if len(self.aoflagger_input.text()) == 0:
                valid_count += 1
                QMessageBox.warning(self, "Warning", "aoflagger cannot be empty")
            else:
                if not os.path.isfile(self.aoflagger_input.text()):
                    valid_count += 1
                    QMessageBox.warning(self, "Warning", "aoflagger is not existing")

            if len(self.wsclean_executable_input.text()) == 0:
                valid_count += 1
                QMessageBox.warning(self, "Warning", "wsclean executable cannot be empty")
            else:
                if not os.path.isfile(self.wsclean_executable_input.text()):
                    valid_count += 1
                    QMessageBox.warning(self, "Warning", "wsclean executable is not existing")

            if len(self.task_file_input.text()) == 0:
                valid_count += 1
                QMessageBox.warning(self, "Warning", "task file cannot be empty")
            else:
                if not os.path.isfile(self.task_file_input.text()):
                    valid_count += 1
                    QMessageBox.warning(self, "Warning", "task file is not existing")

            if len(self.pythonpath_input.text()) == 0:
                valid_count += 1
                QMessageBox.warning(self, "Warning", "python path cannot be empty")
            else:
                if not os.path.isdir(self.pythonpath_input.text()):
                    valid_count += 1
                    QMessageBox.warning(self, "Warning", "python path is not existing")

        if valid_count == 0:
            valid = True
        else:
            valid = False
        return valid

    def run_landmark(self):
        self.setWindowTitle("Running ...")
        run_setup = True
        while run_setup:
            for w in self.setup_wigets:
                if type(w) is QLabel or type(w) is QLineEdit or type(w) is QComboBox:
                    w.clear()

                w.close()
                w.destroy()
                self.grid.removeWidget(w)
                del w

            self.show_query_progress_button = QPushButton("Show query progress")
            self.show_stage_progress_button = QPushButton("Show stage progress")
            self.show_retrieve_progress_button = QPushButton("Show retrieve progress")
            self.show_process_progress_button = QPushButton("Show process progress")

            self.show_query_progress_button.setDisabled(True)
            self.show_stage_progress_button.setDisabled(True)
            self.show_retrieve_progress_button.setDisabled(True)
            self.show_process_progress_button.setDisabled(True)

            self.grid.addWidget(self.show_query_progress_button, 1, 1)
            self.grid.addWidget(self.show_stage_progress_button, 1, 2)
            self.grid.addWidget(self.show_retrieve_progress_button, 1, 3)
            self.grid.addWidget(self.show_process_progress_button, 1, 4)

            run_setup = False

        else:

            config_file = "config.cfg"
            self.SASidsTarget = [int(id) for id in getConfigs("Data", "targetSASids", config_file).replace(" ", "").split(",")]
            project = getConfigs("Data", "PROJECTid", config_file)

            if len(getConfigs("Data", "calibratorSASids", config_file)) == 0:
                if project == "MSSS_HBA_2013":
                    self.SASidsCalibrator = [id - 1 for id in self.SASidsTarget]

                else:
                    raise Exception("SAS id for calibrator is not set in config.cfg file")
                    sys.exit(1)
            else:
                self.SASidsCalibrator = [int(id) for id in getConfigs("Data", "calibratorSASids", config_file).replace(" ", "").split(",")]
            self.config_file = "config.cfg"
            self.which_obj = getConfigs("Operations", "which_obj", config_file)

            self.show_query_progress_button.clicked.connect(self.show_querying_results)
            self.show_stage_progress_button.clicked.connect(self.show_stage_results)

            self.querying_done = False

            if getConfigs("Operations", "querying", config_file) == "True" and getConfigs("Operations", "stage", config_file) == "False":
                self.show_query_progress_button.setStyleSheet("background-color: green")
                self.show_query_progress_button.setDisabled(False)
                self.query()

            elif getConfigs("Operations", "querying", config_file) == "True" and getConfigs("Operations", "stage", config_file) == "True":
                self.show_query_progress_button.setStyleSheet("background-color: green")
                self.show_stage_progress_button.setStyleSheet("background-color: blue")
                self.show_query_progress_button.setDisabled(False)
                self.query()

    def query(self):
        if self.which_obj == "calibrators":
            self.q1 = Querying(self.SASidsCalibrator, True, self.config_file)
            self.q2 = None
        elif self.which_obj == "target":
            self.q1 = None
            self.q2 = Querying(self.SASidsTarget, False, self.config_file)
        else:
            self.q1 = Querying(self.SASidsCalibrator, True, self.config_file)
            self.q2 = Querying(self.SASidsTarget, False, self.config_file)

    def show_querying_results(self):
        querying_setup = True

        while querying_setup:
            self.querying_message = QLabel("Querying in progress")
            self.grid.addWidget(self.querying_message, 2, 1)
            querying_setup = False

        else:
            self.querying_setup_2 = True
            while self.querying_setup_2:
                self.query_station_count(self.q1, self.q2)
            else:
                self.query_data_products()

        self.show_query_progress_button.setStyleSheet("background-color: gray")
        self.show_query_progress_button.setDisabled(True)

        self.querying_done = True

        self.show_stage_progress_button.setStyleSheet("background-color: green")
        self.show_stage_progress_button.setDisabled(False)

    def show_stage_results(self):
        self.plt = pg.PlotWidget()
        self.plt.setBackground([255, 255, 255, 1])
        self.plt.plot(title='Staged files')
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', 'staged file count')
        self.plt.setLabel('bottom', 'time',)
        self.plt.resize(*(1000, 1000))
        self.time = [0]

        self.grid.addWidget(self.plt, 2, 2)
        #self.query_data_products2()

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

        else:
            stagesIDs = list(progress.keys())

        self.curves = []
        self.stages_files_counts = []
        for index in range(0, len(stagesIDs)):
            staged_file_count_for_stageID = [0]
            self.stages_files_counts.append(staged_file_count_for_stageID)
            curve = self.plt.plot(self.time, self.stages_files_counts[index], pen=(255 - index * 10, 0, 0))
            self.curves.append(curve)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)

        progress = get_progress()
        if progress is None:
            self.timer.stop()
            self.show_stage_progress_button.setStyleSheet("background-color: gray")
            self.show_stage_progress_button.setDisabled(True)

    def start_staging(self, SURIs, SASids):
        for id in SASids:
            stagger = LtaStager()
            stagger.stage_uris(SURIs[id])

    def query_station_count(self, q1, q2):
        if q1 is None:
            msg = q2.get_station_count()
            self.querying_message.setText(msg)
        elif q2 is None:
            msg = q1.get_station_count()
            self.querying_message.setText(msg)
        else:
            msg1 = q1.get_station_count()
            self.querying_message.setText(msg1)

            msg2 = q2.get_station_count()
            self.querying_message.setText(self.querying_message.text() + "\n" + msg2)

        self.querying_setup_2 = False

    def query_data_products(self):
        if self.q1 is None:
            msg2 = self.q2.get_data_products()
            self.querying_message.setText(self.querying_message.text() + "\n" + msg2)

        elif self.q2 is None:
            msg1 = self.q1.get_data_products()
            self.querying_message.setText(self.querying_message.text() + "\n" + msg1)

        else:
            msg1 = self.q1.get_data_products()
            self.querying_message.setText(self.querying_message.text() + "\n" + msg1)

            msg2 = self.q2.get_data_products()
            self.querying_message.setText(self.querying_message.text() + "\n" + msg2)

    def query_data_products2(self):
        if self.q1 is None:
            self.q2.get_data_products()

        elif self.q2 is None:
            self.q1.get_data_products()

        else:
            self.q1.get_data_products()
            self.q2.get_data_products()

    def get_staging_progress(self):
        progress = get_progress()
        progress_dict = {}
        if progress is not None:
            if "tuple" not in str(type(progress)):
                stagesIDs = list(progress.keys())
                for stageID in stagesIDs:
                    staged_file_count = progress[stageID]["File count"]
                    progress_dict[stageID] = float(staged_file_count)
            else:
                self.timer.stop()
                self.show_stage_progress_button.setStyleSheet("background-color: gray")
                self.show_stage_progress_button.setDisabled(True)
        else:
            self.timer.stop()
            self.show_stage_progress_button.setStyleSheet("background-color: gray")
            self.show_stage_progress_button.setDisabled(True)

        return progress_dict

    def update_plot(self):
        progress_dict = self.get_staging_progress()

        progress = get_progress()
        if progress is None:
            self.timer.stop()
            self.show_stage_progress_button.setStyleSheet("background-color: gray")
            self.show_stage_progress_button.setDisabled(True)

        elif len(progress_dict) == 0:
            self.timer.stop()
            self.show_stage_progress_button.setStyleSheet("background-color: gray")
            self.show_stage_progress_button.setDisabled(True)

        elif len(list(self.get_staging_progress().keys())) == 0:
            self.timer.stop()
            self.show_stage_progress_button.setStyleSheet("background-color: gray")
            self.show_stage_progress_button.setDisabled(True)

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

    def setup(self):
        self.setWindowTitle("Setup")
        self.grid.removeWidget(self.init_label)
        self.init_label.clear()

        self.opertion_label = QLabel("Operations:")

        self.querying_label = QLabel("Querying")
        self.querying_combobox = QComboBox()
        self.querying_combobox.addItems(["True", "False"])
        self.querying_combobox.setFixedWidth(100)

        self.stage_label = QLabel("Stage")
        self.stage_combobox = QComboBox()
        self.stage_combobox.setFixedWidth(100)
        self.stage_combobox.addItems(["True", "False"])

        self.retrive_label = QLabel("Retrieve")
        self.retrive_combobox = QComboBox()
        self.retrive_combobox.setFixedWidth(100)
        self.retrive_combobox.addItems(["True", "False",])

        self.process_label = QLabel("Process")
        self.process_combobox = QComboBox()
        self.process_combobox.setFixedWidth(100)
        self.process_combobox.addItems(["False", "True",])

        self.grid.addWidget(self.opertion_label, 0, 1)

        self.grid.addWidget(self.querying_label, 0, 2)
        self.grid.addWidget(self.querying_combobox, 0, 3)

        self.grid.addWidget(self.stage_label, 0, 4)
        self.grid.addWidget(self.stage_combobox, 0, 5)

        self.grid.addWidget(self.retrive_label, 0, 6)
        self.grid.addWidget(self.retrive_combobox, 0, 7)

        self.grid.addWidget(self.process_label, 0, 8)
        self.grid.addWidget(self.process_combobox, 0, 9)

        self.which_obj_label = QLabel("Which obj")
        self.which_combobox = QComboBox()
        self.which_combobox.addItems(["calibrators", "target", "all"])
        self.grid.addWidget(self.which_obj_label, 0, 10)
        self.grid.addWidget(self.which_combobox, 0, 11)

        self.data_label = QLabel("Data:")
        self.grid.addWidget(self.data_label, 1, 1)

        self.calibratorSASids_label = QLabel("Calibrator SAS ids")
        self.calibratorSASids_input = QLineEdit()
        self.calibratorSASids_input.setFixedWidth(100)
        self.grid.addWidget(self.calibratorSASids_label, 1, 2)
        self.grid.addWidget(self.calibratorSASids_input, 1, 3)

        self.targetSASids_label = QLabel("Target SAS ids")
        self.targetSASids_input = QLineEdit()
        self.targetSASids_input.setFixedWidth(100)
        self.grid.addWidget(self.targetSASids_label, 1, 4)
        self.grid.addWidget(self.targetSASids_input, 1, 5)

        self.Target_name_label = QLabel("Target Name")
        self.Target_name_input = QLineEdit()
        self.Target_name_input.setFixedWidth(100)
        self.grid.addWidget(self.Target_name_label, 1, 6)
        self.grid.addWidget(self.Target_name_input, 1, 7)

        self.PROJECTid_label = QLabel("Project id")
        self.PROJECTid_input = QLineEdit()
        self.PROJECTid_input.setFixedWidth(100)
        self.grid.addWidget(self.PROJECTid_label, 1, 8)
        self.grid.addWidget(self.PROJECTid_input, 1, 9)

        self.product_type_label = QLabel("Product Type")
        self.product_type_combobox = QComboBox()
        self.product_type_combobox.addItems(["observation", "pipeline"])
        self.grid.addWidget(self.product_type_label, 1, 10)
        self.grid.addWidget(self.product_type_combobox, 1, 11)

        self.cluster_label = QLabel("Cluster:")
        self.grid.addWidget(self.cluster_label, 2, 1)

        self.max_per_node = QLabel("Max per node")
        self.max_per_node_input = QLineEdit()
        self.max_per_node_input.setText(str(20))
        self.max_per_node_input.setFixedWidth(100)
        self.grid.addWidget(self.max_per_node, 2, 2)
        self.grid.addWidget(self.max_per_node_input, 2, 3)

        self.method_label = QLabel("Method")
        self.method_input = QLineEdit()
        self.method_input.setFixedWidth(100)
        self.method_input.setText('local')
        self.grid.addWidget(self.method_label, 2, 4)
        self.grid.addWidget(self.method_input, 2, 5)

        self.WorkingPath_label = QLabel("WorkingPath")
        self.WorkingPath_input = QLineEdit()
        self.WorkingPath_input.setFixedWidth(400)
        self.grid.addWidget(self.WorkingPath_label, 0, 12)
        self.grid.addWidget(self.WorkingPath_input, 1, 12)

        self.PrefactorPath_label = QLabel("PrefactorPath")
        self.PrefactorPath_input = QLineEdit()
        self.PrefactorPath_input.setFixedWidth(400)
        self.grid.addWidget(self.PrefactorPath_label, 2, 12)
        self.grid.addWidget(self.PrefactorPath_input, 3, 12)

        self.lofarroot_label = QLabel("lofarroot")
        self.lofarroot_input = QLineEdit()
        self.lofarroot_input.setFixedWidth(400)
        self.lofarroot_input.setText("/opt/cep/lofim/daily/Tue/lofar_build/install/gnucxx11_opt")
        self.grid.addWidget(self.lofarroot_label, 4, 12)
        self.grid.addWidget(self.lofarroot_input, 5, 12)

        self.casaroot_label = QLabel("casaroot")
        self.casaroot_input = QLineEdit()
        self.casaroot_input.setFixedWidth(400)
        self.casaroot_input.setText("/opt/cep/casacore/casacore_current")
        self.grid.addWidget(self.casaroot_label, 6, 12)
        self.grid.addWidget(self.casaroot_input, 7, 12)

        self.pyraproot_label = QLabel("pyraproot")
        self.pyraproot_input = QLineEdit()
        self.pyraproot_input.setText("/opt/cep/casacore/python-casacore_current/lib64/python2.7/site-packages")
        self.pyraproot_input.setFixedWidth(400)
        self.grid.addWidget(self.pyraproot_label, 8, 12)
        self.grid.addWidget(self.pyraproot_input, 9, 12)

        self.hdf5root_label = QLabel("hdf5root")
        self.hdf5root_input = QLineEdit()
        self.hdf5root_input.setFixedWidth(400)
        self.grid.addWidget(self.hdf5root_label, 10, 12)
        self.grid.addWidget(self.hdf5root_input, 11, 12)

        self.wcsroot_label = QLabel("wcsroot")
        self.wcsroot_input = QLineEdit()
        self.wcsroot_input.setFixedWidth(400)
        self.grid.addWidget(self.wcsroot_label, 12, 12)
        self.grid.addWidget(self.wcsroot_input, 13, 12)

        self.losotoPath_label = QLabel("losotoPath")
        self.losotoPath_input = QLineEdit()
        self.losotoPath_input.setFixedWidth(400)
        self.losotoPath_input.setText('/data/scratch/iacobelli/losoto_Nov21_latest_commit_a7790a6/')
        self.grid.addWidget(self.losotoPath_label, 14, 12)
        self.grid.addWidget(self.losotoPath_input, 15, 12)

        self.aoflagger_label = QLabel("aoflagger")
        self.aoflagger_input = QLineEdit()
        self.aoflagger_input.setText('/opt/cep/aoflagger/aoflagger-2.10.0/build/bin/aoflagger')
        self.grid.addWidget(self.aoflagger_label, 16, 12)
        self.grid.addWidget(self.aoflagger_input, 17, 12)

        self.wsclean_executable_label = QLabel("wsclean executable")
        self.wsclean_executable_input = QLineEdit()
        self.wsclean_executable_input.setText('/opt/cep/wsclean/wsclean-2.8/bin/wsclean')
        self.grid.addWidget(self.wsclean_executable_label, 18, 12)
        self.grid.addWidget(self.wsclean_executable_input, 19, 12)

        self.pythonpath_label = QLabel("pythonpath")
        self.pythonpath_input = QLineEdit()
        self.pythonpath_input.setText('/opt/cep/wsclean/wsclean-2.8/bin/wsclean')
        self.grid.addWidget(self.pythonpath_label, 20, 12)
        self.grid.addWidget(self.pythonpath_input, 21, 12)

        self.task_file_label = QLabel("task_file")
        self.task_file_input = QLineEdit()
        self.task_file_input.setText('%(lofarroot)s/share/pipeline/tasks.cfg')
        self.grid.addWidget(self.task_file_label, 22, 12)
        self.grid.addWidget(self.task_file_input, 23, 12)

        self.save_button = QPushButton("Save LAnDmARk configuration", self)
        self.save_button.setStyleSheet("background-color: green")
        self.save_button.clicked.connect(self.save_configuration)
        self.grid.addWidget(self.save_button, 4, 0)

        self.setup_wigets = set([self.opertion_label, self.querying_label, self.querying_combobox, self.stage_label, self.stage_combobox, self.retrive_label, self.retrive_combobox, self.process_label, self.process_combobox, self.which_obj_label, self.which_combobox, self.data_label, self.calibratorSASids_label, self.calibratorSASids_input, self.targetSASids_label, self.targetSASids_input, self.Target_name_label, self.Target_name_input, self.PROJECTid_label, self.PROJECTid_input, self.product_type_label, self.product_type_combobox, self.cluster_label, self.max_per_node, self.max_per_node_input, self.method_label, self.method_input, self.WorkingPath_label, self.WorkingPath_input, self.PrefactorPath_label, self.PrefactorPath_input, self.lofarroot_label, self.lofarroot_input, self.casaroot_label, self.casaroot_input, self.pyraproot_label, self.pyraproot_input, self.hdf5root_label, self.hdf5root_input, self.wcsroot_label, self.wcsroot_input, self.losotoPath_label, self.losotoPath_input, self.aoflagger_label, self.aoflagger_input, self.wsclean_executable_label, self.wsclean_executable_input, self.pythonpath_label, self.pythonpath_input, self.task_file_label, self.task_file_input, self.save_button])

    def save_configuration(self):
        if self.validate_setup():
            config_file = "config.cfg"

            setConfigs("Data", "targetSASids", self.targetSASids_input.text(), config_file)
            setConfigs("Data", "calibratorsasids", self.calibratorSASids_input.text(), config_file)
            setConfigs("Data", "targetname", self.Target_name_input.text(), config_file)
            setConfigs("Data", "projectid", self.PROJECTid_input.text(), config_file)
            setConfigs("Data", "producttype", self.product_type_combobox.currentText(), config_file)

            setConfigs("Operations", "querying", self.querying_combobox.currentText(), config_file)
            setConfigs("Operations", "stage", self.stage_combobox.currentText(), config_file)
            setConfigs("Operations", "retrieve", self.retrive_combobox.currentText(), config_file)
            setConfigs("Operations", "process", self.process_combobox.currentText(), config_file)

            setConfigs("Cluster", "max_per_node", self.max_per_node_input.text(), config_file)
            setConfigs("Cluster", "method", self.method_input.text(), config_file)

            setConfigs("Paths", "workingpath", self.WorkingPath_input.text(), config_file)
            setConfigs("Paths", "prefactorpath", self.PrefactorPath_input.text(), config_file)
            setConfigs("Paths", "lofarroot", self.lofarroot_input.text(), config_file)
            setConfigs("Paths", "casaroot", self.casaroot_input.text(), config_file)
            setConfigs("Paths", "pyraproot", self.pyraproot_input.text(), config_file)
            setConfigs("Paths", "hdf5root", self.hdf5root_input.text(), config_file)
            setConfigs("Paths", "wcsroot", self.wcsroot_input.text(), config_file)
            setConfigs("Paths", "losotopath", self.losotoPath_input.text(), config_file)
            setConfigs("Paths", "aoflagger", self.aoflagger_input.text(), config_file)
            setConfigs("Paths", "wsclean_executable", self.wsclean_executable_input.text(), config_file)
            setConfigs("Paths", "pythonpath", self.pythonpath_input.text(), config_file)
            setConfigs("Paths", "task_file", self.task_file_input.text(), config_file)

            QMessageBox.about(self, "", "LAnDmARk configuration has been saved")


def main():
    # Create App
    q_app = QApplication(sys.argv)
    aw = Landmark_GUI()
    aw.show()
    sys.exit(q_app.exec_())


if __name__ == "__main__":
    main()