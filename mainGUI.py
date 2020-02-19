#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QApplication, QDesktopWidget, QPushButton, QLabel, QComboBox, QLineEdit)
from PyQt5.QtGui import QFont


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
        setup_button = QPushButton("Setup", self)
        run_button = QPushButton("Run", self)
        check_button = QPushButton("Check", self)
        setup_button.setStyleSheet("background-color: yellow")
        setup_button.clicked.connect(self.setup)
        run_button.setStyleSheet("background-color: green")
        check_button.setStyleSheet("background-color: blue")
        self.grid.addWidget(setup_button, 0,0)
        self.grid.addWidget(run_button, 1,0)
        self.grid.addWidget(check_button, 2,0)

        self.init_label = QLabel("LAnDmARk GUI")
        init_label_font = QFont("Times New Roman", 30, QFont.Bold)
        self.init_label.setFont(init_label_font)
        self.grid.addWidget(self.init_label, 1,1)

    def setup(self):
        self.grid.removeWidget(self.init_label)
        self.init_label.clear()

        self.opertion_label = QLabel("Operations:")

        self.querying_label = QLabel("Querying")
        self.querying_combobox = QComboBox()
        self.querying_combobox.addItems(["True", "False"])

        self.stage_label = QLabel("Stage")
        self.stage_combobox = QComboBox()
        self.stage_combobox.addItems(["True", "False"])

        self.retrive_label = QLabel("Retrieve")
        self.retrive_combobox = QComboBox()
        self.retrive_combobox.addItems(["True", "False",])

        self.process_label = QLabel("Process")
        self.process_combobox = QComboBox()
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
        self.grid.addWidget(self.calibratorSASids_label, 1, 2)
        self.grid.addWidget(self.calibratorSASids_input, 1, 3)

        self.targetSASids_label = QLabel("Target SAS ids")
        self.targetSASids_input = QLineEdit()
        self.grid.addWidget(self.targetSASids_label, 1, 4)
        self.grid.addWidget(self.targetSASids_input, 1, 5)

        self.Target_name_label = QLabel("Target Name")
        self.Target_name_input = QLineEdit()
        self.grid.addWidget(self.Target_name_label, 1, 6)
        self.grid.addWidget(self.Target_name_input, 1, 7)

        self.PROJECTid_label = QLabel("Project id")
        self.PROJECTid_input = QLineEdit()
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
        self.grid.addWidget(self.max_per_node, 2, 2)
        self.grid.addWidget(self.max_per_node_input, 2, 3)

        self.method_label = QLabel("Method")
        self.method_input = QLineEdit()
        self.grid.addWidget(self.method_label, 2, 4)
        self.grid.addWidget(self.method_input, 2, 5)

        self.paths_label = QLabel("Paths:")
        self.grid.addWidget(self.paths_label, 3, 1)

        self.WorkingPath_label = QLabel("WorkingPath")
        self.WorkingPath_input = QLineEdit()
        self.grid.addWidget(self.WorkingPath_label, 3, 2)
        self.grid.addWidget(self.WorkingPath_input, 3, 3)

        self.PrefactorPath_label = QLabel("PrefactorPath")
        self.PrefactorPath_input = QLineEdit()
        self.grid.addWidget(self.PrefactorPath_label, 3, 4)
        self.grid.addWidget(self.PrefactorPath_input, 3, 5)

        self.lofarroot_label = QLabel("lofarroot")
        self.lofarroot_input = QLineEdit()
        self.grid.addWidget(self.lofarroot_label, 3, 6)
        self.grid.addWidget(self.lofarroot_input, 3, 7)

        self.casaroot_label = QLabel("casaroot")
        self.casaroot_input = QLineEdit()
        self.grid.addWidget(self.casaroot_label, 3, 8)
        self.grid.addWidget(self.casaroot_input, 3, 9)

        self.pyraproot_label = QLabel("pyraproot")
        self.pyraproot_input = QLineEdit()
        self.grid.addWidget(self.pyraproot_label, 3, 10)
        self.grid.addWidget(self.pyraproot_input, 3, 11)

        self.hdf5root_label = QLabel("hdf5root")
        self.hdf5root_input = QLineEdit()
        self.grid.addWidget(self.hdf5root_label, 3, 12)
        self.grid.addWidget(self.hdf5root_input, 3, 13)

        self.wcsroot_label = QLabel("wcsroot")
        self.wcsroot_input = QLineEdit()
        self.grid.addWidget(self.wcsroot_label, 3, 14)
        self.grid.addWidget(self.wcsroot_input, 3, 15)

        self.losotoPath_label = QLabel("losotoPath")
        self.losotoPath_input = QLineEdit()
        self.grid.addWidget(self.losotoPath_label, 3, 16)
        self.grid.addWidget(self.losotoPath_input, 3, 17)

        self.aoflagger_label = QLabel("aoflagger")
        self.aoflagger_input = QLineEdit()
        self.grid.addWidget(self.aoflagger_label, 3, 18)
        self.grid.addWidget(self.aoflagger_input, 3, 19)

        self.wsclean_executable_label = QLabel("wsclean executable")
        self.wsclean_executable_input = QLineEdit()
        self.grid.addWidget(self.wsclean_executable_label, 3, 20)
        self.grid.addWidget(self.wsclean_executable_input, 3, 21)

        self.pythonpath_label = QLabel("pythonpath")
        self.pythonpath_input = QLineEdit()
        self.grid.addWidget(self.pythonpath_label, 3, 22)
        self.grid.addWidget(self.pythonpath_input, 3, 23)


def main():
    # Create App
    q_app = QApplication(sys.argv)
    aw = Landmark_GUI()
    aw.show()
    sys.exit(q_app.exec_())


if __name__ == "__main__":
    main()

