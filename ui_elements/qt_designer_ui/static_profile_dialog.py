# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\static_profile_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(217, 69)
        self.vertical_layout = QtWidgets.QVBoxLayout(Dialog)
        self.vertical_layout.setObjectName("vertical_layout")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.vertical_layout.addWidget(self.widget)
        self.buttons_horizontal_layout = QtWidgets.QHBoxLayout()
        self.buttons_horizontal_layout.setObjectName("buttons_horizontal_layout")
        self.push_button_new_profile = QtWidgets.QPushButton(Dialog)
        self.push_button_new_profile.setObjectName("push_button_new_profile")
        self.buttons_horizontal_layout.addWidget(self.push_button_new_profile)
        self.push_button_close = QtWidgets.QPushButton(Dialog)
        self.push_button_close.setObjectName("push_button_close")
        self.buttons_horizontal_layout.addWidget(self.push_button_close)
        self.vertical_layout.addLayout(self.buttons_horizontal_layout)

        self.retranslateUi(Dialog)
        self.push_button_close.clicked.connect(Dialog.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "STATIC profile"))
        self.push_button_new_profile.setText(_translate("Dialog", "New profile"))
        self.push_button_close.setText(_translate("Dialog", "Close"))
