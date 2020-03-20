# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/process_view.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_process_progress_view(object):
    def setupUi(self, process_progress_view):
        process_progress_view.setObjectName("process_progress_view")
        process_progress_view.resize(507, 164)
        self.centralwidget = QtWidgets.QWidget(process_progress_view)
        self.centralwidget.setObjectName("centralwidget")
        self.calibrator_progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.calibrator_progress_bar.setGeometry(QtCore.QRect(0, 10, 501, 23))
        self.calibrator_progress_bar.setProperty("value", 0)
        self.calibrator_progress_bar.setObjectName("calibrator_progress_bar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 30, 241, 20))
        self.label.setObjectName("label")
        self.target_progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.target_progress_bar.setGeometry(QtCore.QRect(0, 50, 501, 23))
        self.target_progress_bar.setMaximum(100)
        self.target_progress_bar.setProperty("value", 0)
        self.target_progress_bar.setObjectName("target_progress_bar")
        self.imaging_progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.imaging_progress_bar.setGeometry(QtCore.QRect(0, 90, 501, 23))
        self.imaging_progress_bar.setProperty("value", 0)
        self.imaging_progress_bar.setObjectName("imaging_progress_bar")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(130, 70, 241, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(130, 110, 241, 20))
        self.label_3.setObjectName("label_3")
        process_progress_view.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(process_progress_view)
        self.statusbar.setObjectName("statusbar")
        process_progress_view.setStatusBar(self.statusbar)

        self.retranslateUi(process_progress_view)
        QtCore.QMetaObject.connectSlotsByName(process_progress_view)

    def retranslateUi(self, process_progress_view):
        _translate = QtCore.QCoreApplication.translate
        process_progress_view.setWindowTitle(_translate("process_progress_view", "process_view"))
        self.label.setText(_translate("process_progress_view", "Percent of calibrator run tasks"))
        self.label_2.setText(_translate("process_progress_view", "Percent of target run tasks"))
        self.label_3.setText(_translate("process_progress_view", "Percent of imaging run tasks"))
