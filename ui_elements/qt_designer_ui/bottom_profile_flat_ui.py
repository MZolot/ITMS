# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\bottom_profile_flat.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(231, 112)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QtCore.QSize(231, 112))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.line_edit_depth = QtWidgets.QLineEdit(Dialog)
        self.line_edit_depth.setMaximumSize(QtCore.QSize(100, 16777215))
        self.line_edit_depth.setObjectName("line_edit_depth")
        self.gridLayout.addWidget(self.line_edit_depth, 0, 1, 1, 1)
        self.label_depth = QtWidgets.QLabel(Dialog)
        self.label_depth.setObjectName("label_depth")
        self.gridLayout.addWidget(self.label_depth, 0, 0, 1, 1)
        self.label_length = QtWidgets.QLabel(Dialog)
        self.label_length.setObjectName("label_length")
        self.gridLayout.addWidget(self.label_length, 1, 0, 1, 1)
        self.line_edit_length = QtWidgets.QLineEdit(Dialog)
        self.line_edit_length.setMinimumSize(QtCore.QSize(0, 0))
        self.line_edit_length.setMaximumSize(QtCore.QSize(100, 16777215))
        self.line_edit_length.setObjectName("line_edit_length")
        self.gridLayout.addWidget(self.line_edit_length, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setObjectName("buttons_layout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttons_layout.addItem(spacerItem)
        self.push_button_ok = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_ok.sizePolicy().hasHeightForWidth())
        self.push_button_ok.setSizePolicy(sizePolicy)
        self.push_button_ok.setObjectName("push_button_ok")
        self.buttons_layout.addWidget(self.push_button_ok, 0, QtCore.Qt.AlignRight)
        self.push_button_cancel = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_cancel.sizePolicy().hasHeightForWidth())
        self.push_button_cancel.setSizePolicy(sizePolicy)
        self.push_button_cancel.setObjectName("push_button_cancel")
        self.buttons_layout.addWidget(self.push_button_cancel, 0, QtCore.Qt.AlignLeft)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttons_layout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.buttons_layout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Bottom profile"))
        self.label_depth.setText(_translate("Dialog", "Depth (m): "))
        self.label_length.setText(_translate("Dialog", "Length:"))
        self.line_edit_length.setPlaceholderText(_translate("Dialog", "900"))
        self.push_button_ok.setText(_translate("Dialog", "OK"))
        self.push_button_cancel.setText(_translate("Dialog", "Cancel"))
