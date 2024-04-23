import ui_elements.qt_designer_ui.bottom_profile_flat_ui as flat_ui
import ui_elements.qt_designer_ui.bottom_profile_complex_ui as complex_ui
from .error_dialog import ErrorDialog
from PyQt5 import QtWidgets
import numpy as np


class BottomProfileDialog(QtWidgets.QDialog):
    def __init__(self, parent, ok_callback):
        super().__init__(parent)
        self.ok_callback = ok_callback


class BottomProfileFlatDialog(BottomProfileDialog, flat_ui.Ui_Dialog):
    def __init__(self, parent, ok_callback):
        super().__init__(parent, ok_callback)
        self.setupUi(self)
        self.line_edit_length.setPlaceholderText("900")
        self.line_edit_depth.setPlaceholderText("500")
        self.push_button_ok.clicked.connect(self.ok_pushed)
        self.push_button_cancel.clicked.connect(self.close)

    def ok_pushed(self):
        try:
            depth = float(self.line_edit_depth.text())
        except ValueError:
            # error_dialog = ErrorDialog("Incorrect or empty depth value!\nPlease enter floating number.")
            # error_dialog.exec()
            # return
            depth = 500
        try:
            length = int(self.line_edit_length.text())
        except ValueError:
            # error_dialog = ErrorDialog("Incorrect or empty length value!\nPlease enter integer number.")
            # error_dialog.exec()
            # return
            length = 900

        # arr = np.full(length, depth)
        arr = np.negative(np.full(length, depth))
        self.close()
        self.ok_callback(arr)


class BottomProfileComplexDialog(BottomProfileDialog, complex_ui.Ui_Dialog):
    def __init__(self, parent, ok_callback):
        super().__init__(parent, ok_callback)
        self.setupUi(self)
        self.push_button_ok.clicked.connect(self.ok_pushed)
        self.push_button_cancel.clicked.connect(self.close)

    def ok_pushed(self):
        self.ok_callback()
