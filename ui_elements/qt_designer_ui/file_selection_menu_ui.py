# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\files_selection_menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(228, 258)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.vertical_layout_initial = QtWidgets.QVBoxLayout()
        self.vertical_layout_initial.setObjectName("vertical_layout_initial")
        self.label_initial = QtWidgets.QLabel(Dialog)
        self.label_initial.setObjectName("label_initial")
        self.vertical_layout_initial.addWidget(self.label_initial)
        self.horizontal_layout_initial = QtWidgets.QHBoxLayout()
        self.horizontal_layout_initial.setObjectName("horizontal_layout_initial")
        self.label_ini_data_file_name = QtWidgets.QLabel(Dialog)
        self.label_ini_data_file_name.setObjectName("label_ini_data_file_name")
        self.horizontal_layout_initial.addWidget(self.label_ini_data_file_name)
        self.push_button_initial = QtWidgets.QPushButton(Dialog)
        self.push_button_initial.setMinimumSize(QtCore.QSize(93, 0))
        self.push_button_initial.setObjectName("push_button_initial")
        self.horizontal_layout_initial.addWidget(self.push_button_initial)
        self.vertical_layout_initial.addLayout(self.horizontal_layout_initial)
        self.verticalLayout.addLayout(self.vertical_layout_initial)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.vertical_layout_height = QtWidgets.QVBoxLayout()
        self.vertical_layout_height.setObjectName("vertical_layout_height")
        self.label_height = QtWidgets.QLabel(Dialog)
        self.label_height.setObjectName("label_height")
        self.vertical_layout_height.addWidget(self.label_height)
        self.horizontal_layout_height = QtWidgets.QHBoxLayout()
        self.horizontal_layout_height.setObjectName("horizontal_layout_height")
        self.label_height_file_name = QtWidgets.QLabel(Dialog)
        self.label_height_file_name.setObjectName("label_height_file_name")
        self.horizontal_layout_height.addWidget(self.label_height_file_name)
        self.push_button_height = QtWidgets.QPushButton(Dialog)
        self.push_button_height.setMinimumSize(QtCore.QSize(93, 0))
        self.push_button_height.setObjectName("push_button_height")
        self.horizontal_layout_height.addWidget(self.push_button_height)
        self.vertical_layout_height.addLayout(self.horizontal_layout_height)
        self.verticalLayout.addLayout(self.vertical_layout_height)
        self.vertical_layout_max_height = QtWidgets.QVBoxLayout()
        self.vertical_layout_max_height.setObjectName("vertical_layout_max_height")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.vertical_layout_max_height.addWidget(self.line_2)
        self.label_max_height = QtWidgets.QLabel(Dialog)
        self.label_max_height.setObjectName("label_max_height")
        self.vertical_layout_max_height.addWidget(self.label_max_height)
        self.horizontal_layout_max_height = QtWidgets.QHBoxLayout()
        self.horizontal_layout_max_height.setObjectName("horizontal_layout_max_height")
        self.label_max_height_file_name = QtWidgets.QLabel(Dialog)
        self.label_max_height_file_name.setObjectName("label_max_height_file_name")
        self.horizontal_layout_max_height.addWidget(self.label_max_height_file_name)
        self.push_button_max_height = QtWidgets.QPushButton(Dialog)
        self.push_button_max_height.setMinimumSize(QtCore.QSize(93, 0))
        self.push_button_max_height.setObjectName("push_button_max_height")
        self.horizontal_layout_max_height.addWidget(self.push_button_max_height)
        self.vertical_layout_max_height.addLayout(self.horizontal_layout_max_height)
        self.verticalLayout.addLayout(self.vertical_layout_max_height)
        self.horizontal_layout_buttons = QtWidgets.QHBoxLayout()
        self.horizontal_layout_buttons.setObjectName("horizontal_layout_buttons")
        self.push_button_ok = QtWidgets.QPushButton(Dialog)
        self.push_button_ok.setObjectName("push_button_ok")
        self.horizontal_layout_buttons.addWidget(self.push_button_ok)
        self.push_button_cancel = QtWidgets.QPushButton(Dialog)
        self.push_button_cancel.setObjectName("push_button_cancel")
        self.horizontal_layout_buttons.addWidget(self.push_button_cancel)
        self.verticalLayout.addLayout(self.horizontal_layout_buttons)

        self.retranslateUi(Dialog)
        self.push_button_cancel.clicked.connect(Dialog.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select MOST files"))
        self.label_initial.setText(_translate("Dialog", "Initial parameters:"))
        self.label_ini_data_file_name.setText(_translate("Dialog", "default_file_name"))
        self.push_button_initial.setText(_translate("Dialog", "Select file..."))
        self.label_height.setText(_translate("Dialog", "Height results:"))
        self.label_height_file_name.setText(_translate("Dialog", "default_file_name"))
        self.push_button_height.setText(_translate("Dialog", "Select file..."))
        self.label_max_height.setText(_translate("Dialog", "Max height results:"))
        self.label_max_height_file_name.setText(_translate("Dialog", "default_file_name"))
        self.push_button_max_height.setText(_translate("Dialog", "Select file..."))
        self.push_button_ok.setText(_translate("Dialog", "OK"))
        self.push_button_cancel.setText(_translate("Dialog", "Cancel"))
