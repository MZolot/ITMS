# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\plot_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(705, 515)
        self.vertical_layout = QtWidgets.QVBoxLayout(Dialog)
        self.vertical_layout.setObjectName("vertical_layout")
        self.buttons_widget = QtWidgets.QWidget(Dialog)
        self.buttons_widget.setObjectName("buttons_widget")
        self.buttons_layout = QtWidgets.QHBoxLayout(self.buttons_widget)
        self.buttons_layout.setContentsMargins(3, 3, 3, 3)
        self.buttons_layout.setSpacing(5)
        self.buttons_layout.setObjectName("buttons_layout")
        self.push_button_close = QtWidgets.QPushButton(self.buttons_widget)
        self.push_button_close.setMinimumSize(QtCore.QSize(95, 28))
        self.push_button_close.setMaximumSize(QtCore.QSize(95, 28))
        self.push_button_close.setObjectName("push_button_close")
        self.buttons_layout.addWidget(self.push_button_close)
        self.vertical_layout.addWidget(self.buttons_widget, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignBottom)

        self.retranslateUi(Dialog)
        self.push_button_close.clicked.connect(Dialog.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MOST calculation results"))
        self.push_button_close.setText(_translate("Dialog", "Close"))
