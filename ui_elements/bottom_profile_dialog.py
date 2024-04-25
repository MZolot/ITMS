import ui_elements.qt_designer_ui.bottom_profile_flat_ui as flat_ui
import ui_elements.qt_designer_ui.bottom_profile_complex_ui as complex_ui
from .error_dialog import ErrorDialog
from PyQt5 import QtWidgets
import numpy as np


last_used_profile_file_name = "last_used_profile.txt"


def print_flat_profile(length, depth):
    f = open(last_used_profile_file_name, 'w')
    f.write(f'flat\n{length} {depth}')
    f.close()


def print_complex_profile(start_depth, length_list, depth_list):
    f = open(last_used_profile_file_name, 'w')
    f.write(f'complex\n{start_depth}\n')
    for i in range(len(length_list)):
        f.write(f'{length_list[i]} {depth_list[i]}\n')
    f.close()


class BottomProfileDialog(QtWidgets.QDialog):
    def __init__(self, parent, ok_callback):
        super().__init__(parent)
        self.ok_callback = ok_callback


class BottomProfileFlatDialog(BottomProfileDialog, flat_ui.Ui_Dialog):
    def __init__(self, parent, ok_callback):
        super().__init__(parent, ok_callback)
        self.setupUi(self)
        self.push_button_ok.clicked.connect(self.ok_pushed)
        self.push_button_cancel.clicked.connect(self.close)

    def ok_pushed(self):
        try:
            depth = float(self.line_edit_depth.text())
        except ValueError:
            error_dialog = ErrorDialog("Incorrect or empty depth value!\nPlease enter floating number.")
            error_dialog.exec()
            return
        try:
            length = int(self.line_edit_length.text())
        except ValueError:
            length = int(self.line_edit_length.placeholderText())

        arr = np.negative(np.full(length, depth))

        self.close()
        print_flat_profile(length, depth)
        self.ok_callback(arr)

    def set_values(self, length, depth):
        self.line_edit_depth.setText(depth)
        self.line_edit_length.setText(length)


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

        print_complex_profile(start_depth, lengths, depths)
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

    def add_level_with_values(self, length, depth):
        line_edit_depth = QtWidgets.QLineEdit()
        line_edit_depth.setText(depth)
        self.grid_layout.addWidget(line_edit_depth, (len(self.depth_line_edits) + 2), 0)
        self.depth_line_edits.append(line_edit_depth)

        line_edit_length = QtWidgets.QLineEdit()
        line_edit_length.setText(length)
        self.grid_layout.addWidget(line_edit_length, (len(self.length_line_edits) + 2), 1)
        self.length_line_edits.append(line_edit_length)

    def delete_level(self):
        if len(self.length_line_edits) == 1:
            return

        line_edit = self.depth_line_edits.pop()
        parent_layout = line_edit.parent().layout()
        parent_layout.removeWidget(line_edit)
        line_edit.deleteLater()

        line_edit = self.length_line_edits.pop()
        parent_layout = line_edit.parent().layout()
        parent_layout.removeWidget(line_edit)
        line_edit.deleteLater()

    def set_values(self, start_depth, lengths, depths):
        self.line_edit_start_depth.setText(start_depth)
        if len(lengths) < 1 or len(depths) < 1:
            return

        self.line_edit_depth.setText(depths[0])
        self.line_edit_length.setText(lengths[0])

        for i in range(1, len(lengths)):
            self.add_level_with_values(lengths[i], depths[i])
