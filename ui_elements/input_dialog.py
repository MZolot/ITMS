import ui_elements.qt_designer_ui.input_menu_ui as menu_ui
import ui_elements.qt_designer_ui.error_dialog as error_ui
from data_entry import DataEntry
from PyQt5 import QtWidgets


class InputMenuDialog(QtWidgets.QDialog, menu_ui.Ui_Dialog):
    def __init__(self, data_elements: list[DataEntry], title, ok_pushed_callback=None):
        self.data_elements = data_elements
        self.ok_pushed = ok_pushed_callback

        super().__init__()
        self.setupUi(self)

        self.line_edits = []
        self.title = title
        self.set_layout(self.data_elements)
        self.pushButton_ok.clicked.connect(self.ok_button_pushed)

    def set_layout(self, data_elements):
        for i in range(len(data_elements)):
            p = data_elements[i]

            name_label = QtWidgets.QLabel(p.label_text)
            name_label.setWordWrap(True)
            name_label.setMinimumWidth(150)

            line_edit = QtWidgets.QLineEdit()
            line_edit.setPlaceholderText(str(p.get_current_value()))
            line_edit.setMaximumWidth(60)
            self.line_edits.append(line_edit)
            # line_edit.setStyleSheet("background-color: blue;")

            unit_label = QtWidgets.QLabel(p.unit)
            unit_label.setMaximumWidth(30)

            self.gridLayout.addWidget(name_label, i, 0)
            self.gridLayout.addWidget(line_edit, i, 1)
            self.gridLayout.addWidget(unit_label, i, 2)

            self.gridLayout.setHorizontalSpacing(15)

            self.setWindowTitle(self.title)

    def ok_button_pushed(self):
        for i in range(len(self.data_elements)):
            new_value = self.line_edits[i].text()
            if new_value == "":
                continue
            try:
                float(new_value)
            except ValueError:
                error_dialog = ErrorDialog(self.data_elements[i].name)
                error_dialog.exec()
                return

        for i in range(len(self.data_elements)):
            new_value = self.line_edits[i].text()
            if new_value != "":
                new_value_float = float(self.line_edits[i].text())
                self.data_elements[i].set_current_value(new_value_float)

        self.ok_pushed()
        self.close()


class ErrorDialog(QtWidgets.QDialog, error_ui.Ui_Dialog):
    def __init__(self, error_field_name: str):
        super().__init__()
        self.setupUi(self)

        line = f"Incorrect value for {error_field_name}!\nPlease enter floating number or nothing."
        self.label.setText(line)

        self.push_button.clicked.connect(self.ok_button_pushed)

    def ok_button_pushed(self):
        self.close()
