#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
from PyQt5.QtWidgets import (QWidget, QGridLayout, QApplication, QDesktopWidget, QPushButton, QLabel, QComboBox, QLineEdit, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import pyqtgraph as pg
from stager_access import *
from parsers._configparser import setConfigs, getConfigs
import selectionStaging
import query_socket
from threading import Thread


import re
import socket
import os
import struct


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

    def validate_setup(self, targetSASid, targetname, projectID, max_per_node, method, WorkingPath, PrefactorPath, lofarroot, casaroot, pyraproot, losotoPath, aoflagger, wsclean_executable, pythonpath, task_file):
        valid_count = 0
        if len(targetSASid) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "Target SAS id cannot be empty")

        if len(targetname) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "Target name cannot be empty")

        if len(projectID) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "Project ID cannot be empty")

        if len(max_per_node) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "max_per_node cannot be empty")

        if len(method) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "method cannot be empty")

        if len(WorkingPath) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "Working Pathcannot be empty")

        if len(PrefactorPath) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "PrefactorPath cannot be empty")

        if len(lofarroot) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "lofarroot cannot be empty")

        if len(casaroot) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "casaroot cannot be empty")

        if len(pyraproot) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "pyraproot cannot be empty")

        if len(losotoPath) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "losotoPath cannot be empty")

        if len(aoflagger) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "aoflagger cannot be empty")

        if len(wsclean_executable) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "wsclean_executable cannot be empty")

        if len(pythonpath) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "pythonpath cannot be empty")

        if len(task_file) == 0:
            valid_count += 1
            QMessageBox.warning(self, "Warning", "task_file cannot be empty")

        if valid_count == 0:
            valid = True
        else:
            valid = False
        return valid

    def run_landmark(self):
        self.setWindowTitle("Running ...")
        for w in self.setup_wigets:
            if type(w) is QLabel or type(w) is QLineEdit or type(w) is QComboBox:
                w.clear()

            w.close()
            w.destroy()
            self.grid.removeWidget(w)
            del w

        time.sleep(10)
        config_file = "config.cfg"

        SASidsTarget = [int(id) for id in getConfigs("Data", "targetSASids", config_file).replace(" ", "").split(",")]
        project = getConfigs("Data", "PROJECTid", config_file)

        if len(getConfigs("Data", "calibratorSASids", config_file)) == 0:
            if project == "MSSS_HBA_2013":
                SASidsCalibrator = [id - 1 for id in SASidsTarget]

            else:
                raise Exception("SAS id for calibrator is not set in config.cfg file")
                sys.exit(1)
        else:
            SASidsCalibrator = [int(id) for id in getConfigs("Data", "calibratorSASids", config_file).replace(" ", "").split(",")]

        which_obj = getConfigs("Operations", "which_obj", config_file)

        if getConfigs("Operations", "querying", config_file) == "True":
            self.querying_progress = QLabel("ABC")

            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update_querying_progress)
            self.timer.start(3000)
            self.grid.addWidget(self.querying_progress, 1, 1)
            self.query_data(which_obj, SASidsCalibrator, SASidsTarget)

        if getConfigs("Operations", "Stage", config_file) == "True":

            stagingTarget = selectionStaging.Staging(SASidsTarget, False, config_file)
            stagingTarget.query()
            stagingCalibrator = selectionStaging.Staging(SASidsCalibrator, True, config_file)
            stagingCalibrator.query()

            workingDir = getConfigs("Paths", "WorkingPath", config_file)
            targetName = getConfigs("Data", "TargetName", config_file)
            workingDir = workingDir + "/" + targetName + "/"
            auxDir = workingDir + "/LAnDmARk_aux"

            targetSURIs = []
            calibratorSURIs = []

            for id in SASidsTarget:
                for URI in stagingTarget.getSURIs()[str(id)]:
                    if "sara" in URI:
                        targetSURIs.append(
                            "https://lofar-download.grid.surfsara.nl/lofigrid/SRMFifoGet.py?surl=" + URI + "\n")
                    elif "juelich" in URI:
                        targetSURIs.append(
                            "https://lofar-download.fz-juelich.de/webserver-lofar/SRMFifoGet.py?surl=" + URI + "\n")
                    else:
                        targetSURIs.append(
                            "https://lta-download.lofar.psnc.pl/lofigrid/SRMFifoGet.py?surl=" + URI + "\n")

            for id in SASidsCalibrator:
                for URI in stagingCalibrator.getSURIs()[str(id)]:
                    if "sara" in URI:
                        calibratorSURIs.append(
                            "https://lofar-download.grid.surfsara.nl/lofigrid/SRMFifoGet.py?surl=" + URI + "\n")
                    elif "juelich" in URI:
                        calibratorSURIs.append(
                            "https://lofar-download.fz-juelich.de/webserver-lofar/SRMFifoGet.py?surl=" + URI + "\n")
                    else:
                        calibratorSURIs.append(
                            "https://lta-download.lofar.psnc.pl/lofigrid/SRMFifoGet.py?surl=" + URI + "\n")

            if stagingTarget.get_total_file_size() + stagingCalibrator.get_total_file_size() < 5000000000000 and stagingCalibrator.get_total_file_count() + stagingTarget.get_total_file_count() < 5000:
                if getConfigs("Operations", "which_obj", config_file) == "all" or len(getConfigs("Operations", "which_obj", config_file)) == 0:
                    stagingTarget.startStaging()
                    stagingCalibrator.startStaging()

                elif getConfigs("Operations", "which_obj", config_file) == "targets":
                    stagingTarget.startStaging()

                elif getConfigs("Operations", "which_obj", config_file) == "calibrators":
                    stagingCalibrator.startStaging()

            self.plt = pg.PlotWidget()
            self.plt.setBackground([255, 255, 255, 1])
            self.plt.plot(title='Staged files')
            self.plt.showGrid(x=True, y=True)
            self.plt.setLabel('left', 'staged file count')
            self.plt.setLabel('bottom', 'time')
            self.plt.resize(*(1000,1000))
            self.time = []
            progess = get_progress()
            stagesIDs = list(progess.keys())
            self.curves = []
            self.stages_files_counts = []
            for index in range(0, len(stagesIDs)):
                staged_file_count_for_stageID = []
                self.stages_files_counts.append(staged_file_count_for_stageID)
                curve = self.plt.plot(self.time, self.stages_files_counts[index], pen=(255 - index*10, 0, 0))
                self.curves.append(curve)
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update_plot)
            self.timer.start(3000)
            self.grid.addWidget(self.plt, 1,1)

    def get_staging_progress(self):
        progess = get_progress()
        progress_dict = {}
        if progess != None:
            if "tuple" not in str(type(progess)):
                stagesIDs = list(progess.keys())
                for stageID in stagesIDs:
                    staged_file_count = progess[stageID]["File count"]
                    progress_dict[stageID] = float(staged_file_count)

        return progress_dict

    def update_querying_progress(self):
        host = "127.0.0.1"
        port = 9001
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))

        data, addr = sock.recvfrom(2048)
        data = str(data)
        print(data)
        sock.close()
        self.querying_progress.setText(self.querying_progress.text() + data)

    def query_data(self, which_obj, SASidsCalibrator=[], SASidsTarget=[]):
        config_file = "config.cfg"
        if which_obj == "calibrators":
            if len(SASidsCalibrator) != 0:
                print("abcdefghijgg2")
                Thread(target=query_socket.Staging, args=([167226], True, "config.cfg")).start()
                print("abcdefghijgg")
                #stagingCalibrator = selectionStaging.Staging(SASidsCalibrator, True, config_file)
                #stagingCalibrator.query()
            else:
                QMessageBox.warning(self, "Warning", "Sas ID for calibrator cannot be empty")

        elif which_obj == "target":
            if len(SASidsTarget) != 0:
                stagingTarget = selectionStaging.Staging(SASidsTarget, False, config_file)
                stagingTarget.query()
            else:
                QMessageBox.warning(self, "Warning", "Sas ID for target cannot be empty")
        else:
            if len(SASidsCalibrator) != 0 or len(SASidsTarget) != 0:
                stagingTarget = selectionStaging.Staging(SASidsTarget, False, config_file)
                stagingTarget.query()
                stagingCalibrator = selectionStaging.Staging(SASidsCalibrator, True, config_file)
                stagingCalibrator.query()
            else:
                QMessageBox.warning(self, "Warning", "Sas ID for target and calibrator cannot be empty")

    def update_plot(self):
        progress_dict = self.get_staging_progress()

        if len(progress_dict) == 0:
            self.timer.stop()
        else:
            if len(self.time) == 0:
                self.time.append(30)
            else:
                self.time.append(self.time[-1] + 30)

            for index in range(0, len(self.get_staging_progress())):
                stageId = list(self.get_staging_progress().keys())[index]
                staged_file_count_for_id = self.get_staging_progress()[stageId]
                self.stages_files_counts[index].append(staged_file_count_for_id)
                curve = self.curves[index]
                curve.setData(self.time, self.stages_files_counts[index])

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
        if self.validate_setup(self.targetSASids_input.text(), self.Target_name_input.text(), self.PROJECTid_input.text(), self.max_per_node_input.text(), self.method_input.text(), self.WorkingPath_input.text(), self.PrefactorPath_input.text(), self.lofarroot_input.text(), self.casaroot_input.text(), self.pyraproot_input.text(), self.losotoPath_input.text(), self.aoflagger_input.text(), self.wsclean_executable_input.text(), self.pythonpath_input.text(), self.task_file_input.text()   ):
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

            print("Saving LAnDmARk configuration")
            QMessageBox.about(self, "", "LAnDmARk configuration has been saved")


def main():
    # Create App
    q_app = QApplication(sys.argv)
    aw = Landmark_GUI()
    aw.show()
    sys.exit(q_app.exec_())


if __name__ == "__main__":
    main()

