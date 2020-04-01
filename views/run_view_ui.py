# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/run_view.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_run_view(object):
    def setupUi(self, run_view):
        run_view.setObjectName("run_view")
        run_view.resize(666, 93)
        self.centralwidget = QtWidgets.QWidget(run_view)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 671, 76))
        self.centralwidget.setObjectName("centralwidget")
        self.show_query_progress_button = QtWidgets.QPushButton(self.centralwidget)
        self.show_query_progress_button.setEnabled(False)
        self.show_query_progress_button.setGeometry(QtCore.QRect(10, 20, 151, 36))
        self.show_query_progress_button.setObjectName("show_query_progress_button")
        self.show_stage_progress_button = QtWidgets.QPushButton(self.centralwidget)
        self.show_stage_progress_button.setEnabled(False)
        self.show_stage_progress_button.setGeometry(QtCore.QRect(170, 20, 151, 36))
        self.show_stage_progress_button.setObjectName("show_stage_progress_button")
        self.show_retrieve_progress_button = QtWidgets.QPushButton(self.centralwidget)
        self.show_retrieve_progress_button.setEnabled(False)
        self.show_retrieve_progress_button.setGeometry(QtCore.QRect(330, 20, 161, 36))
        self.show_retrieve_progress_button.setObjectName("show_retrieve_progress_button")
        self.show_process_progress_button = QtWidgets.QPushButton(self.centralwidget)
        self.show_process_progress_button.setEnabled(False)
        self.show_process_progress_button.setGeometry(QtCore.QRect(500, 20, 161, 36))
        self.show_process_progress_button.setObjectName("show_process_progress_button")
        run_view.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(run_view)
        self.statusbar.setGeometry(QtCore.QRect(0, 0, 3, 25))
        self.statusbar.setObjectName("statusbar")
        run_view.setStatusBar(self.statusbar)

        self.retranslateUi(run_view)
        QtCore.QMetaObject.connectSlotsByName(run_view)

    def retranslateUi(self, run_view):
        _translate = QtCore.QCoreApplication.translate
        run_view.setWindowTitle(_translate("run_view", "Run"))
        self.show_query_progress_button.setText(_translate("run_view", "Show query progress"))
        self.show_stage_progress_button.setText(_translate("run_view", "Show stage progress"))
        self.show_retrieve_progress_button.setText(_translate("run_view", "Show retrieve progress"))
        self.show_process_progress_button.setText(_translate("run_view", "Show process progress"))
