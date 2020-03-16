# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/setup_view.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_setup_view(object):
    def setupUi(self, setup_view):
        setup_view.setObjectName("setup_view")
        setup_view.resize(931, 952)
        self.operation_label = QtWidgets.QLabel(setup_view)
        self.operation_label.setGeometry(QtCore.QRect(20, 20, 71, 20))
        self.operation_label.setObjectName("operation_label")
        self.data_label = QtWidgets.QLabel(setup_view)
        self.data_label.setGeometry(QtCore.QRect(160, 20, 31, 20))
        self.data_label.setObjectName("data_label")
        self.cluster_label = QtWidgets.QLabel(setup_view)
        self.cluster_label.setGeometry(QtCore.QRect(300, 20, 51, 20))
        self.cluster_label.setObjectName("cluster_label")
        self.prefactor_label = QtWidgets.QLabel(setup_view)
        self.prefactor_label.setGeometry(QtCore.QRect(410, 160, 101, 20))
        self.prefactor_label.setObjectName("prefactor_label")
        self.hdf5root_input = QtWidgets.QLineEdit(setup_view)
        self.hdf5root_input.setGeometry(QtCore.QRect(500, 580, 431, 36))
        self.hdf5root_input.setText("")
        self.hdf5root_input.setObjectName("hdf5root_input")
        self.querying_label = QtWidgets.QLabel(setup_view)
        self.querying_label.setGeometry(QtCore.QRect(20, 60, 41, 20))
        self.querying_label.setObjectName("querying_label")
        self.retrive_label = QtWidgets.QLabel(setup_view)
        self.retrive_label.setGeometry(QtCore.QRect(20, 260, 61, 20))
        self.retrive_label.setObjectName("retrive_label")
        self.stage_label = QtWidgets.QLabel(setup_view)
        self.stage_label.setGeometry(QtCore.QRect(20, 160, 41, 20))
        self.stage_label.setObjectName("stage_label")
        self.process_label = QtWidgets.QLabel(setup_view)
        self.process_label.setGeometry(QtCore.QRect(20, 360, 51, 20))
        self.process_label.setObjectName("process_label")
        self.which_obj_label = QtWidgets.QLabel(setup_view)
        self.which_obj_label.setGeometry(QtCore.QRect(20, 460, 71, 20))
        self.which_obj_label.setObjectName("which_obj_label")
        self.querying_comboBox = QtWidgets.QComboBox(setup_view)
        self.querying_comboBox.setGeometry(QtCore.QRect(20, 100, 102, 36))
        self.querying_comboBox.setEditable(False)
        self.querying_comboBox.setMinimumContentsLength(0)
        self.querying_comboBox.setObjectName("querying_comboBox")
        self.querying_comboBox.addItem("")
        self.querying_comboBox.addItem("")
        self.retrieve_combobox = QtWidgets.QComboBox(setup_view)
        self.retrieve_combobox.setGeometry(QtCore.QRect(20, 300, 103, 36))
        self.retrieve_combobox.setInputMethodHints(QtCore.Qt.ImhNone)
        self.retrieve_combobox.setObjectName("retrieve_combobox")
        self.retrieve_combobox.addItem("")
        self.retrieve_combobox.addItem("")
        self.which_combobox = QtWidgets.QComboBox(setup_view)
        self.which_combobox.setGeometry(QtCore.QRect(20, 500, 131, 36))
        self.which_combobox.setObjectName("which_combobox")
        self.which_combobox.addItem("")
        self.which_combobox.addItem("")
        self.which_combobox.addItem("")
        self.process_combobox = QtWidgets.QComboBox(setup_view)
        self.process_combobox.setGeometry(QtCore.QRect(20, 400, 103, 36))
        self.process_combobox.setObjectName("process_combobox")
        self.process_combobox.addItem("")
        self.process_combobox.addItem("")
        self.stage_combobox = QtWidgets.QComboBox(setup_view)
        self.stage_combobox.setGeometry(QtCore.QRect(20, 200, 103, 36))
        self.stage_combobox.setObjectName("stage_combobox")
        self.stage_combobox.addItem("")
        self.stage_combobox.addItem("")
        self.WorkingPath_input = QtWidgets.QLineEdit(setup_view)
        self.WorkingPath_input.setGeometry(QtCore.QRect(410, 100, 431, 36))
        self.WorkingPath_input.setInputMask("")
        self.WorkingPath_input.setText("")
        self.WorkingPath_input.setFrame(True)
        self.WorkingPath_input.setObjectName("WorkingPath_input")
        self.calibratorSASids_input = QtWidgets.QLineEdit(setup_view)
        self.calibratorSASids_input.setGeometry(QtCore.QRect(160, 100, 91, 36))
        self.calibratorSASids_input.setText("")
        self.calibratorSASids_input.setObjectName("calibratorSASids_input")
        self.calibratorSASids_label = QtWidgets.QLabel(setup_view)
        self.calibratorSASids_label.setGeometry(QtCore.QRect(160, 60, 111, 20))
        self.calibratorSASids_label.setObjectName("calibratorSASids_label")
        self.product_type_label = QtWidgets.QLabel(setup_view)
        self.product_type_label.setGeometry(QtCore.QRect(160, 460, 91, 20))
        self.product_type_label.setObjectName("product_type_label")
        self.PROJECTid_label = QtWidgets.QLabel(setup_view)
        self.PROJECTid_label.setGeometry(QtCore.QRect(160, 360, 61, 20))
        self.PROJECTid_label.setObjectName("PROJECTid_label")
        self.Target_name_label = QtWidgets.QLabel(setup_view)
        self.Target_name_label.setGeometry(QtCore.QRect(160, 260, 91, 20))
        self.Target_name_label.setObjectName("Target_name_label")
        self.targetSASids_label = QtWidgets.QLabel(setup_view)
        self.targetSASids_label.setGeometry(QtCore.QRect(160, 160, 91, 20))
        self.targetSASids_label.setObjectName("targetSASids_label")
        self.Target_name_input = QtWidgets.QLineEdit(setup_view)
        self.Target_name_input.setGeometry(QtCore.QRect(160, 300, 91, 36))
        self.Target_name_input.setText("")
        self.Target_name_input.setObjectName("Target_name_input")
        self.targetSASids_input = QtWidgets.QLineEdit(setup_view)
        self.targetSASids_input.setGeometry(QtCore.QRect(160, 200, 91, 36))
        self.targetSASids_input.setText("")
        self.targetSASids_input.setObjectName("targetSASids_input")
        self.PROJECTid_input = QtWidgets.QLineEdit(setup_view)
        self.PROJECTid_input.setGeometry(QtCore.QRect(160, 400, 91, 36))
        self.PROJECTid_input.setText("")
        self.PROJECTid_input.setObjectName("PROJECTid_input")
        self.product_type_combobox = QtWidgets.QComboBox(setup_view)
        self.product_type_combobox.setGeometry(QtCore.QRect(160, 500, 141, 36))
        self.product_type_combobox.setObjectName("product_type_combobox")
        self.product_type_combobox.addItem("")
        self.product_type_combobox.addItem("")
        self.max_per_node_label = QtWidgets.QLabel(setup_view)
        self.max_per_node_label.setGeometry(QtCore.QRect(300, 60, 91, 20))
        self.max_per_node_label.setObjectName("max_per_node_label")
        self.method_label = QtWidgets.QLabel(setup_view)
        self.method_label.setGeometry(QtCore.QRect(300, 160, 51, 20))
        self.method_label.setObjectName("method_label")
        self.max_per_node_input = QtWidgets.QLineEdit(setup_view)
        self.max_per_node_input.setGeometry(QtCore.QRect(300, 100, 91, 36))
        self.max_per_node_input.setText("")
        self.max_per_node_input.setObjectName("max_per_node_input")
        self.method_input = QtWidgets.QLineEdit(setup_view)
        self.method_input.setGeometry(QtCore.QRect(300, 200, 91, 36))
        self.method_input.setText("")
        self.method_input.setObjectName("method_input")
        self.wsclean_executable_input = QtWidgets.QLineEdit(setup_view)
        self.wsclean_executable_input.setGeometry(QtCore.QRect(20, 690, 431, 36))
        self.wsclean_executable_input.setObjectName("wsclean_executable_input")
        self.losotoPath_input = QtWidgets.QLineEdit(setup_view)
        self.losotoPath_input.setGeometry(QtCore.QRect(500, 780, 431, 36))
        self.losotoPath_input.setObjectName("losotoPath_input")
        self.pythonpath_input = QtWidgets.QLineEdit(setup_view)
        self.pythonpath_input.setGeometry(QtCore.QRect(20, 790, 431, 36))
        self.pythonpath_input.setText("")
        self.pythonpath_input.setObjectName("pythonpath_input")
        self.task_file_input = QtWidgets.QLineEdit(setup_view)
        self.task_file_input.setGeometry(QtCore.QRect(20, 890, 431, 36))
        self.task_file_input.setObjectName("task_file_input")
        self.lofarroot_input = QtWidgets.QLineEdit(setup_view)
        self.lofarroot_input.setGeometry(QtCore.QRect(410, 300, 431, 36))
        self.lofarroot_input.setInputMask("")
        self.lofarroot_input.setPlaceholderText("")
        self.lofarroot_input.setObjectName("lofarroot_input")
        self.PrefactorPath_input = QtWidgets.QLineEdit(setup_view)
        self.PrefactorPath_input.setGeometry(QtCore.QRect(410, 200, 431, 36))
        self.PrefactorPath_input.setText("")
        self.PrefactorPath_input.setObjectName("PrefactorPath_input")
        self.casaroot_input = QtWidgets.QLineEdit(setup_view)
        self.casaroot_input.setGeometry(QtCore.QRect(410, 400, 431, 36))
        self.casaroot_input.setObjectName("casaroot_input")
        self.aoflagger_input = QtWidgets.QLineEdit(setup_view)
        self.aoflagger_input.setGeometry(QtCore.QRect(20, 590, 431, 36))
        self.aoflagger_input.setObjectName("aoflagger_input")
        self.wcsroot_input = QtWidgets.QLineEdit(setup_view)
        self.wcsroot_input.setGeometry(QtCore.QRect(500, 680, 431, 36))
        self.wcsroot_input.setText("")
        self.wcsroot_input.setObjectName("wcsroot_input")
        self.pyraproot_input = QtWidgets.QLineEdit(setup_view)
        self.pyraproot_input.setGeometry(QtCore.QRect(500, 490, 431, 36))
        self.pyraproot_input.setObjectName("pyraproot_input")
        self.path_label = QtWidgets.QLabel(setup_view)
        self.path_label.setGeometry(QtCore.QRect(410, 20, 41, 20))
        self.path_label.setObjectName("path_label")
        self.task_file_label = QtWidgets.QLabel(setup_view)
        self.task_file_label.setGeometry(QtCore.QRect(20, 850, 61, 20))
        self.task_file_label.setObjectName("task_file_label")
        self.losotoPath_label = QtWidgets.QLabel(setup_view)
        self.losotoPath_label.setGeometry(QtCore.QRect(510, 740, 71, 20))
        self.losotoPath_label.setObjectName("losotoPath_label")
        self.wcsroot_label = QtWidgets.QLabel(setup_view)
        self.wcsroot_label.setGeometry(QtCore.QRect(500, 640, 61, 20))
        self.wcsroot_label.setObjectName("wcsroot_label")
        self.hdf5root_label = QtWidgets.QLabel(setup_view)
        self.hdf5root_label.setGeometry(QtCore.QRect(500, 540, 61, 20))
        self.hdf5root_label.setObjectName("hdf5root_label")
        self.pyraproot_label = QtWidgets.QLabel(setup_view)
        self.pyraproot_label.setGeometry(QtCore.QRect(500, 450, 71, 20))
        self.pyraproot_label.setObjectName("pyraproot_label")
        self.casaroot_label = QtWidgets.QLabel(setup_view)
        self.casaroot_label.setGeometry(QtCore.QRect(410, 360, 61, 20))
        self.casaroot_label.setObjectName("casaroot_label")
        self.lofaroot_label = QtWidgets.QLabel(setup_view)
        self.lofaroot_label.setGeometry(QtCore.QRect(410, 260, 61, 20))
        self.lofaroot_label.setObjectName("lofaroot_label")
        self.working_path_label = QtWidgets.QLabel(setup_view)
        self.working_path_label.setGeometry(QtCore.QRect(410, 60, 91, 20))
        self.working_path_label.setObjectName("working_path_label")
        self.pythonpath_label = QtWidgets.QLabel(setup_view)
        self.pythonpath_label.setGeometry(QtCore.QRect(20, 750, 81, 20))
        self.pythonpath_label.setObjectName("pythonpath_label")
        self.wsclean_executable_label = QtWidgets.QLabel(setup_view)
        self.wsclean_executable_label.setGeometry(QtCore.QRect(20, 650, 131, 20))
        self.wsclean_executable_label.setObjectName("wsclean_executable_label")
        self.aoflagger_label = QtWidgets.QLabel(setup_view)
        self.aoflagger_label.setGeometry(QtCore.QRect(20, 550, 61, 20))
        self.aoflagger_label.setObjectName("aoflagger_label")
        self.save_button = QtWidgets.QPushButton(setup_view)
        self.save_button.setGeometry(QtCore.QRect(500, 890, 221, 36))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(138, 226, 52))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(198, 255, 143))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(168, 240, 97))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(69, 113, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(92, 151, 34))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(138, 226, 52))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(196, 240, 153))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(138, 226, 52))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(198, 255, 143))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(168, 240, 97))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(69, 113, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(92, 151, 34))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(138, 226, 52))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(196, 240, 153))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(69, 113, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(138, 226, 52))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(198, 255, 143))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(168, 240, 97))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(69, 113, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(92, 151, 34))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(69, 113, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(69, 113, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(138, 226, 52))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(138, 226, 52))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(138, 226, 52))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.save_button.setPalette(palette)
        self.save_button.setObjectName("save_button")

        self.retranslateUi(setup_view)
        self.querying_comboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(setup_view)
        setup_view.setTabOrder(self.which_combobox, self.hdf5root_input)
        setup_view.setTabOrder(self.hdf5root_input, self.process_combobox)
        setup_view.setTabOrder(self.process_combobox, self.retrieve_combobox)
        setup_view.setTabOrder(self.retrieve_combobox, self.calibratorSASids_input)
        setup_view.setTabOrder(self.calibratorSASids_input, self.Target_name_input)
        setup_view.setTabOrder(self.Target_name_input, self.stage_combobox)
        setup_view.setTabOrder(self.stage_combobox, self.targetSASids_input)
        setup_view.setTabOrder(self.targetSASids_input, self.PROJECTid_input)
        setup_view.setTabOrder(self.PROJECTid_input, self.product_type_combobox)
        setup_view.setTabOrder(self.product_type_combobox, self.max_per_node_input)
        setup_view.setTabOrder(self.max_per_node_input, self.method_input)
        setup_view.setTabOrder(self.method_input, self.wsclean_executable_input)
        setup_view.setTabOrder(self.wsclean_executable_input, self.losotoPath_input)
        setup_view.setTabOrder(self.losotoPath_input, self.pythonpath_input)
        setup_view.setTabOrder(self.pythonpath_input, self.querying_comboBox)
        setup_view.setTabOrder(self.querying_comboBox, self.task_file_input)
        setup_view.setTabOrder(self.task_file_input, self.lofarroot_input)
        setup_view.setTabOrder(self.lofarroot_input, self.PrefactorPath_input)
        setup_view.setTabOrder(self.PrefactorPath_input, self.casaroot_input)
        setup_view.setTabOrder(self.casaroot_input, self.aoflagger_input)
        setup_view.setTabOrder(self.aoflagger_input, self.wcsroot_input)
        setup_view.setTabOrder(self.wcsroot_input, self.pyraproot_input)
        setup_view.setTabOrder(self.pyraproot_input, self.save_button)
        setup_view.setTabOrder(self.save_button, self.WorkingPath_input)

    def retranslateUi(self, setup_view):
        _translate = QtCore.QCoreApplication.translate
        setup_view.setWindowTitle(_translate("setup_view", "Setup"))
        self.operation_label.setText(_translate("setup_view", "Operations"))
        self.data_label.setText(_translate("setup_view", "Data"))
        self.cluster_label.setText(_translate("setup_view", "Cluster"))
        self.prefactor_label.setText(_translate("setup_view", "Prefactor path"))
        self.querying_label.setText(_translate("setup_view", "Query"))
        self.retrive_label.setText(_translate("setup_view", "Retrieve"))
        self.stage_label.setText(_translate("setup_view", "Stage"))
        self.process_label.setText(_translate("setup_view", "Process"))
        self.which_obj_label.setText(_translate("setup_view", "Which obj"))
        self.querying_comboBox.setCurrentText(_translate("setup_view", "True"))
        self.querying_comboBox.setItemText(0, _translate("setup_view", "True"))
        self.querying_comboBox.setItemText(1, _translate("setup_view", "False"))
        self.retrieve_combobox.setItemText(0, _translate("setup_view", "False"))
        self.retrieve_combobox.setItemText(1, _translate("setup_view", "True"))
        self.which_combobox.setItemText(0, _translate("setup_view", "calibrators"))
        self.which_combobox.setItemText(1, _translate("setup_view", "target"))
        self.which_combobox.setItemText(2, _translate("setup_view", "all"))
        self.process_combobox.setItemText(0, _translate("setup_view", "False"))
        self.process_combobox.setItemText(1, _translate("setup_view", "True"))
        self.stage_combobox.setItemText(0, _translate("setup_view", "False"))
        self.stage_combobox.setItemText(1, _translate("setup_view", "True"))
        self.calibratorSASids_label.setText(_translate("setup_view", "Calibrator SAS id"))
        self.product_type_label.setText(_translate("setup_view", "Product Type"))
        self.PROJECTid_label.setText(_translate("setup_view", "Project id"))
        self.Target_name_label.setText(_translate("setup_view", "Target Name"))
        self.targetSASids_label.setText(_translate("setup_view", "Target SAS id"))
        self.product_type_combobox.setItemText(0, _translate("setup_view", "observation"))
        self.product_type_combobox.setItemText(1, _translate("setup_view", "pipeline"))
        self.max_per_node_label.setText(_translate("setup_view", "Max per node"))
        self.method_label.setText(_translate("setup_view", "Method"))
        self.wsclean_executable_input.setText(_translate("setup_view", "/opt/cep/wsclean/wsclean-2.8/bin/wsclean"))
        self.losotoPath_input.setText(_translate("setup_view", "/data/scratch/iacobelli/losoto_Nov21_latest_commit_a7790a6/"))
        self.task_file_input.setText(_translate("setup_view", "%(lofarroot)s/share/pipeline/tasks.cfg"))
        self.lofarroot_input.setText(_translate("setup_view", "/opt/cep/lofim/daily/Tue/lofar_build/install/gnucxx11_opt"))
        self.casaroot_input.setText(_translate("setup_view", "/opt/cep/casacore/casacore_current"))
        self.aoflagger_input.setText(_translate("setup_view", "/opt/cep/aoflagger/aoflagger-2.10.0/build/bin/aoflagger"))
        self.pyraproot_input.setText(_translate("setup_view", "/opt/cep/casacore/python-casacore_current/lib64/python2.7/site-packages"))
        self.path_label.setText(_translate("setup_view", "Paths"))
        self.task_file_label.setText(_translate("setup_view", "task_file"))
        self.losotoPath_label.setText(_translate("setup_view", "losotoPath"))
        self.wcsroot_label.setText(_translate("setup_view", "wcsroot"))
        self.hdf5root_label.setText(_translate("setup_view", "hdf5root"))
        self.pyraproot_label.setText(_translate("setup_view", "pyraproot"))
        self.casaroot_label.setText(_translate("setup_view", "casaroot"))
        self.lofaroot_label.setText(_translate("setup_view", "lofarroot"))
        self.working_path_label.setText(_translate("setup_view", "Working path"))
        self.pythonpath_label.setText(_translate("setup_view", "pythonpath"))
        self.wsclean_executable_label.setText(_translate("setup_view", "wsclean executable"))
        self.aoflagger_label.setText(_translate("setup_view", "aoflagger"))
        self.save_button.setWhatsThis(_translate("setup_view", "<html><head/><body><p><span style=\" font-size:12pt;\">Store values in config.cfg file</span></p></body></html>"))
        self.save_button.setText(_translate("setup_view", "Save LAnDmARk configuration"))