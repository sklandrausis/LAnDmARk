# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/query_view.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_query_view(object):
    def setupUi(self, query_view):
        query_view.setObjectName("query_view")
        query_view.resize(185, 38)
        self.centralwidget = QtWidgets.QWidget(query_view)
        self.centralwidget.setObjectName("centralwidget")
        self.querying_message = QtWidgets.QLabel(self.centralwidget)
        self.querying_message.setGeometry(QtCore.QRect(20, 10, 141, 20))
        self.querying_message.setObjectName("querying_message")
        query_view.setCentralWidget(self.centralwidget)

        self.retranslateUi(query_view)
        QtCore.QMetaObject.connectSlotsByName(query_view)

    def retranslateUi(self, query_view):
        _translate = QtCore.QCoreApplication.translate
        query_view.setWindowTitle(_translate("query_view", "Querying results"))
        self.querying_message.setText(_translate("query_view", "Querying in progress"))
