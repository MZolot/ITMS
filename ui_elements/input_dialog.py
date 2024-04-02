import ui_elements.qt_designer_ui.input_menu_ui as menu_ui
import ui_elements.qt_designer_ui.error_dialog_ui as error_ui
from data_entry import DataEntry
from PyQt5 import QtWidgets


class InputMenuDialog(QtWidgets.QDialog, menu_ui.Ui_Dialog):
    def __init__(self, data_elements: list[DataEntry], title):
        self.data_elements = data_elements

        super().__init__()
        self.setupUi(self)

        self.line_edits = []
        self.title = title
        self.set_layout(self.data_elements)
        self.push_button_ok.clicked.connect(self.ok_button_pushed)

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

            self.parameters_grid_layout.addWidget(name_label, i, 0)
            self.parameters_grid_layout.addWidget(line_edit, i, 1)
            self.parameters_grid_layout.addWidget(unit_label, i, 2)

            self.parameters_grid_layout.setHorizontalSpacing(15)

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

        self.close()


class InputMenuDialogWithCallbacks(InputMenuDialog):
    def __init__(self, data_elements, title, ok_pushed_callbacks: list):
        super().__init__(data_elements, title)
        self.ok_pushed = ok_pushed_callbacks

    def ok_button_pushed(self):
        super().ok_button_pushed()
        for callback in self.ok_pushed:
            callback()


class CalculationMenuDialog(InputMenuDialog):
    def __init__(self, data_elements, title, calculate_pushed_callbacks: list):
        super().__init__(data_elements, title)
        self.calculate_pushed = calculate_pushed_callbacks

        push_button_calculate = QtWidgets.QPushButton()
        push_button_calculate.setText("Calculate")
        self.buttons_horizontal_layout.insertWidget(1, push_button_calculate)
        push_button_calculate.clicked.connect(self.calculate_button_pushed)

    def calculate_button_pushed(self):
        self.ok_button_pushed()
        for c in self.calculate_pushed:
            c()


class ErrorDialog(QtWidgets.QDialog, error_ui.Ui_Dialog):
    def __init__(self, error_field_name: str):
        super().__init__()
        self.setupUi(self)

        line = f"Incorrect value for {error_field_name}!\nPlease enter floating number or nothing."
        self.label.setText(line)

        self.push_button.clicked.connect(self.ok_button_pushed)

    def ok_button_pushed(self):
        self.close()
