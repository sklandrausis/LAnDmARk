# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/check_view.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_check_view(object):
    def setupUi(self, check_view):
        check_view.setObjectName("check_view")
        check_view.setWindowModality(QtCore.Qt.WindowModal)
        check_view.resize(457, 112)
        self.centralwidget = QtWidgets.QWidget(check_view)
        self.centralwidget.setObjectName("centralwidget")
        self.landmark_button = QtWidgets.QPushButton(self.centralwidget)
        self.landmark_button.setGeometry(QtCore.QRect(20, 20, 231, 36))
        self.landmark_button.setObjectName("landmark_button")
        check_view.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(check_view)
        self.statusbar.setObjectName("statusbar")
        check_view.setStatusBar(self.statusbar)

        self.retranslateUi(check_view)
        QtCore.QMetaObject.connectSlotsByName(check_view)

    def retranslateUi(self, check_view):
        _translate = QtCore.QCoreApplication.translate
        check_view.setWindowTitle(_translate("check_view", "chech_view"))
        self.landmark_button.setText(_translate("check_view", "View LAnDmARk inspection plos"))
