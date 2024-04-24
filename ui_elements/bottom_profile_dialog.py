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
            length = int(self.line_edit_length.placeholderText())

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
        self.push_button_add.clicked.connect(self.add_level)
        self.push_button_delete.clicked.connect(self.delete_level)

        self.depth_line_edits = [self.line_edit_depth]
        self.length_line_edits = [self.line_edit_length]

    def ok_pushed(self):
        try:
            start_depth = float(self.line_edit_start_depth.text())
            start_depth = abs(start_depth) * -1
        except ValueError:
            # error_dialog = ErrorDialog("Incorrect or empty depth value!\nPlease enter floating number.")
            # error_dialog.exec()
            # return
            start_depth = 0

        depths = []
        lengths = []
        for i in range(len(self.depth_line_edits)):
            try:
                depth = float(self.depth_line_edits[i].text())
                depths.append(abs(depth) * -1)
            except ValueError:
                if i == 0:
                    depth = float(self.depth_line_edits[i].placeholderText())
                    depths.append(abs(depth) * -1)
                else:
                    error_dialog = ErrorDialog("Incorrect or empty depth value!\nPlease enter floating number.")
                    error_dialog.exec()
                    return
            try:
                length = int(self.length_line_edits[i].text())
                lengths.append(length)
            except ValueError:
                if i == 0:
                    length = float(self.length_line_edits[i].placeholderText())
                    lengths.append(length)
                else:
                    error_dialog = ErrorDialog("Incorrect or empty length value!\nPlease enter integer number.")
                    error_dialog.exec()
                    return

        arr = np.empty(0)
        for i in range(len(depths)):
            if i == 0:
                x0 = start_depth
            else:
                x0 = depths[i - 1]
            xn = depths[i]
            n = lengths[i]
            if x0 == xn:
                curr_arr = np.full(n, x0)
            else:
                step = (xn - x0) / n
                curr_arr = np.arange(x0, xn, step)
            arr = np.concatenate([arr, curr_arr])

        arr = np.append(arr, depths[-1])

        self.close()
        self.ok_callback(arr)

    def add_level(self):
        line_edit_depth = QtWidgets.QLineEdit()
        line_edit_depth.setPlaceholderText(str(len(self.depth_line_edits) + 1))
        self.grid_layout.addWidget(line_edit_depth, (len(self.depth_line_edits) + 2), 0)
        self.depth_line_edits.append(line_edit_depth)

        line_edit_length = QtWidgets.QLineEdit()
        line_edit_length.setPlaceholderText(str(len(self.length_line_edits) + 1))
        self.grid_layout.addWidget(line_edit_length, (len(self.length_line_edits) + 2), 1)
        self.length_line_edits.append(line_edit_length)

    def delete_level(self):
        line_edit = self.depth_line_edits.pop()
        parent_layout = line_edit.parent().layout()
        parent_layout.removeWidget(line_edit)
        line_edit.deleteLater()

        line_edit = self.length_line_edits.pop()
        parent_layout = line_edit.parent().layout()
        parent_layout.removeWidget(line_edit)
        line_edit.deleteLater()
