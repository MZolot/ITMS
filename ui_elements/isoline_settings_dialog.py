import ui_elements.qt_designer_ui.isoline_settings_dialog_ui as menu_ui
import ui_elements.qt_designer_ui.error_dialog as error_ui
from PyQt5 import QtWidgets


class IsolineSettingsDialog(QtWidgets.QDialog, menu_ui.Ui_Dialog):
    def __init__(self, levels, ok_callback_function):
        super().__init__()
        self.setupUi(self)
        self.ok_callback_function = ok_callback_function
        self.levels = levels

        self.line_edits = []
        for level in levels:
            line_edit = QtWidgets.QLineEdit()
            line_edit.setPlaceholderText(str(level))
            self.scroll_area_layout.addWidget(line_edit)
            self.line_edits.append(line_edit)

        self.button_box.accepted.connect(self.ok_button_pushed)
        self.push_button_add.clicked.connect(self.add_level)
        self.push_button_delete.clicked.connect(self.delete_level)

    def ok_button_pushed(self):
        for i in range(len(self.line_edits)):
            value = self.line_edits[i].text()
            if value == "":
                continue
            try:
                float(value)
            except ValueError:
                error_dialog = ErrorDialog()
                error_dialog.exec()
                return

        for i in range(len(self.line_edits)):
            value = self.line_edits[i].text()
            if value != "":
                if i < len(self.levels):
                    self.levels[i] = float(value)
                else:
                    self.levels.append(float(value))

        self.levels.sort()
        self.button_box.accepted.connect(self.accept)
        self.ok_callback_function()
        self.close()

    def add_level(self):
        line_edit = QtWidgets.QLineEdit()
        line_edit.setPlaceholderText("0.00")
        self.scroll_area_layout.addWidget(line_edit)
        self.line_edits.append(line_edit)

    def delete_level(self):
        self.levels.pop()
        line_edit = self.line_edits.pop()
        parent_layout = line_edit.parent().layout()
        parent_layout.removeWidget(line_edit)
        line_edit.deleteLater()


class ErrorDialog(QtWidgets.QDialog, error_ui.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        line = f"Incorrect value for one of the levels!\nPlease enter floating number or nothing."
        self.label.setText(line)

        self.push_button.clicked.connect(self.ok_button_pushed)

    def ok_button_pushed(self):
        self.close()
