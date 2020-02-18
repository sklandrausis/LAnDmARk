#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QApplication, QDesktopWidget, QPushButton, QLabel, QComboBox, QInputDialog)
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

        self.which_obj_label = QLabel("Which obj:")
        self.which_combobox = QComboBox()
        self.which_combobox.addItems(["calibrators", "target", "all"])
        self.grid.addWidget(self.which_obj_label, 0, 10)
        self.grid.addWidget(self.which_combobox, 0, 11)

        self.config_label = QLabel("Config")
        self.parset_label = QLabel("Parset")

        self.grid.addWidget(self.config_label, 1,1)
        self.grid.addWidget(self.parset_label, 1,2)


def main():
    # Create App
    q_app = QApplication(sys.argv)
    aw = Landmark_GUI()
    aw.show()
    sys.exit(q_app.exec_())


if __name__ == "__main__":
    main()

