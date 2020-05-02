# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/check_view.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_check_view(object):
    def setupUi(self, check_view):
        check_view.setObjectName("check_view")
        check_view.setWindowModality(QtCore.Qt.WindowModal)
        check_view.resize(932, 397)
        self.centralwidget = QtWidgets.QWidget(check_view)
        self.centralwidget.setObjectName("centralwidget")
        self.choose_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.choose_combobox.setGeometry(QtCore.QRect(10, 10, 231, 36))
        self.choose_combobox.setObjectName("choose_combobox")
        self.choose_combobox.addItem("")
        self.choose_combobox.addItem("")
        self.choose_combobox.addItem("")
        self.choose_combobox.addItem("")
        self.inspection_plots_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.inspection_plots_combobox.setGeometry(QtCore.QRect(250, 10, 301, 36))
        self.inspection_plots_combobox.setObjectName("inspection_plots_combobox")
        check_view.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(check_view)
        self.statusbar.setObjectName("statusbar")
        check_view.setStatusBar(self.statusbar)

        self.retranslateUi(check_view)
        QtCore.QMetaObject.connectSlotsByName(check_view)

    def retranslateUi(self, check_view):
        _translate = QtCore.QCoreApplication.translate
        check_view.setWindowTitle(_translate("check_view", "chech_view"))
        self.choose_combobox.setItemText(0, _translate("check_view", "LAnDmARk inspection plots"))
        self.choose_combobox.setItemText(1, _translate("check_view", "Prefacotor calibrator inspection plots"))
        self.choose_combobox.setItemText(2, _translate("check_view", "Prefactor target inspection plots"))
        self.choose_combobox.setItemText(3, _translate("check_view", "Prefactor imaging inspection plots"))
