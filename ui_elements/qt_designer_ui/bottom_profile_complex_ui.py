# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\bottom_profile_complex.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(357, 240)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_start_depth = QtWidgets.QWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_start_depth.sizePolicy().hasHeightForWidth())
        self.widget_start_depth.setSizePolicy(sizePolicy)
        self.widget_start_depth.setObjectName("widget_start_depth")
        self.horizontal_layout_start_depth = QtWidgets.QHBoxLayout(self.widget_start_depth)
        self.horizontal_layout_start_depth.setContentsMargins(-1, 5, -1, 5)
        self.horizontal_layout_start_depth.setObjectName("horizontal_layout_start_depth")
        self.label_start_depth = QtWidgets.QLabel(self.widget_start_depth)
        self.label_start_depth.setObjectName("label_start_depth")
        self.horizontal_layout_start_depth.addWidget(self.label_start_depth)
        self.line_edit_start_depth = QtWidgets.QLineEdit(self.widget_start_depth)
        self.line_edit_start_depth.setObjectName("line_edit_start_depth")
        self.horizontal_layout_start_depth.addWidget(self.line_edit_start_depth)
        self.verticalLayout_2.addWidget(self.widget_start_depth)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.scroll_area = QtWidgets.QScrollArea(Dialog)
        self.scroll_area.setMinimumSize(QtCore.QSize(335, 0))
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setLineWidth(0)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area_contents = QtWidgets.QWidget()
        self.scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 335, 85))
        self.scroll_area_contents.setMinimumSize(QtCore.QSize(290, 0))
        self.scroll_area_contents.setAutoFillBackground(True)
        self.scroll_area_contents.setObjectName("scroll_area_contents")
        self.scroll_area_layout = QtWidgets.QVBoxLayout(self.scroll_area_contents)
        self.scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area_layout.setSpacing(7)
        self.scroll_area_layout.setObjectName("scroll_area_layout")
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setContentsMargins(-1, -1, 0, -1)
        self.grid_layout.setObjectName("grid_layout")
        self.label_length = QtWidgets.QLabel(self.scroll_area_contents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_length.sizePolicy().hasHeightForWidth())
        self.label_length.setSizePolicy(sizePolicy)
        self.label_length.setMinimumSize(QtCore.QSize(160, 0))
        self.label_length.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_length.setFont(font)
        self.label_length.setAlignment(QtCore.Qt.AlignCenter)
        self.label_length.setObjectName("label_length")
        self.grid_layout.addWidget(self.label_length, 1, 1, 1, 1)
        self.label_depth = QtWidgets.QLabel(self.scroll_area_contents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_depth.sizePolicy().hasHeightForWidth())
        self.label_depth.setSizePolicy(sizePolicy)
        self.label_depth.setMinimumSize(QtCore.QSize(160, 0))
        self.label_depth.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_depth.setFont(font)
        self.label_depth.setAlignment(QtCore.Qt.AlignCenter)
        self.label_depth.setObjectName("label_depth")
        self.grid_layout.addWidget(self.label_depth, 1, 0, 1, 1)
        self.line_edit_depth = QtWidgets.QLineEdit(self.scroll_area_contents)
        self.line_edit_depth.setObjectName("line_edit_depth")
        self.grid_layout.addWidget(self.line_edit_depth, 2, 0, 1, 1)
        self.line_edit_length = QtWidgets.QLineEdit(self.scroll_area_contents)
        self.line_edit_length.setText("")
        self.line_edit_length.setObjectName("line_edit_length")
        self.grid_layout.addWidget(self.line_edit_length, 2, 1, 1, 1)
        self.scroll_area_layout.addLayout(self.grid_layout)
        self.scroll_area.setWidget(self.scroll_area_contents)
        self.verticalLayout_2.addWidget(self.scroll_area)
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.push_button_add = QtWidgets.QPushButton(Dialog)
        self.push_button_add.setObjectName("push_button_add")
        self.horizontal_layout.addWidget(self.push_button_add)
        self.push_button_delete = QtWidgets.QPushButton(Dialog)
        self.push_button_delete.setObjectName("push_button_delete")
        self.horizontal_layout.addWidget(self.push_button_delete)
        self.verticalLayout_2.addLayout(self.horizontal_layout)
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setContentsMargins(0, 0, -1, -1)
        self.buttons_layout.setObjectName("buttons_layout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttons_layout.addItem(spacerItem)
        self.push_button_ok = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_ok.sizePolicy().hasHeightForWidth())
        self.push_button_ok.setSizePolicy(sizePolicy)
        self.push_button_ok.setMaximumSize(QtCore.QSize(93, 16777215))
        self.push_button_ok.setObjectName("push_button_ok")
        self.buttons_layout.addWidget(self.push_button_ok, 0, QtCore.Qt.AlignHCenter)
        self.push_button_cancel = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_cancel.sizePolicy().hasHeightForWidth())
        self.push_button_cancel.setSizePolicy(sizePolicy)
        self.push_button_cancel.setMaximumSize(QtCore.QSize(93, 16777215))
        self.push_button_cancel.setObjectName("push_button_cancel")
        self.buttons_layout.addWidget(self.push_button_cancel, 0, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttons_layout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.buttons_layout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Bottom profile"))
        self.label_start_depth.setText(_translate("Dialog", "Start depth:"))
        self.line_edit_start_depth.setPlaceholderText(_translate("Dialog", "0"))
        self.label_length.setText(_translate("Dialog", "Segment length (steps)"))
        self.label_depth.setText(_translate("Dialog", "Segment end depth (m)"))
        self.line_edit_depth.setPlaceholderText(_translate("Dialog", "5000"))
        self.line_edit_length.setPlaceholderText(_translate("Dialog", "900"))
        self.push_button_add.setText(_translate("Dialog", "Add level"))
        self.push_button_delete.setText(_translate("Dialog", "Delete level"))
        self.push_button_ok.setText(_translate("Dialog", "OK"))
        self.push_button_cancel.setText(_translate("Dialog", "Cancel"))
