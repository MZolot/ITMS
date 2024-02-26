import ui_elements.qt_designer_ui.static_settings_ui as settings_ui
import ui_elements.qt_designer_ui.error_dialog as error_ui
from ui_elements.collapsible_box import CollapsibleBox
from data_entry import DataEntry
from PyQt5 import QtWidgets


class StaticSettingsDialog(QtWidgets.QDialog, settings_ui.Ui_Dialog):
    def __init__(self, parameters: dict[str, DataEntry], parameters_to_menu_section, calculate_callback):
        self.parameters = parameters
        self.parameters_to_menu = parameters_to_menu_section
        self.calculate_callback = calculate_callback

        super().__init__()
        self.setupUi(self)

        self.line_edits: dict[str, QtWidgets.QLineEdit] = {}
        self.__set_layout()
        self.push_button_calculate.clicked.connect(self.calculate_button_pushed)
        self.push_button_close.clicked.connect(self.close)
        self.push_button_default.clicked.connect(self.default_button_pushed)

    def __set_layout(self):
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        fault_parameters = [self.parameters[p] for p in
                            self.parameters_to_menu["fault"]]
        calculation_parameters = [self.parameters[p] for p in
                                  self.parameters_to_menu["calculation"]]

        fault_box = CollapsibleBox("Fault parameters")
        fault_box.set_content_layout(self.__layout_parameters(fault_parameters))

        calculation_box = CollapsibleBox("Calculation parameters")
        calculation_box.set_content_layout(self.__layout_parameters(calculation_parameters))

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        parameters_layout = QtWidgets.QVBoxLayout()
        parameters_layout.addWidget(fault_box)
        parameters_layout.addWidget(line)
        parameters_layout.addWidget(calculation_box)
        self.parameters_widget.setLayout(parameters_layout)
        # self.parameters_widget.adjustSize()
        # self.adjustSize()

        # self.scroll_area.setMinimumHeight(fault_box.height() + calculation_box.height() + 30)
        self.scroll_area.setMinimumHeight(200)

    def __layout_parameters(self, parameters):
        layout = QtWidgets.QVBoxLayout()
        for parameter in parameters:
            label = QtWidgets.QLabel(parameter.label_text)
            label.setMinimumWidth(100)

            line_edit = QtWidgets.QLineEdit()
            line_edit.setPlaceholderText(str(parameter.get_current_value()))
            line_edit.setFixedWidth(80)
            self.line_edits[parameter.name] = line_edit

            parameter_layout = QtWidgets.QHBoxLayout()
            parameter_layout.addWidget(label)
            parameter_layout.addWidget(line_edit)
            parameter_layout.setContentsMargins(0, 0, 0, 0)

            parameter_container = QtWidgets.QWidget()
            parameter_container.setLayout(parameter_layout)
            # parameter_container.setFixedHeight(30)

            parameter_container.setAutoFillBackground(True)
            # parameter_container.setStyleSheet()

            layout.addWidget(parameter_container)
        return layout

    def calculate_button_pushed(self):
        print("calculate!")
        for i in self.parameters.keys():
            new_value = self.line_edits[i].text()
            if new_value == "":
                continue
            try:
                float(new_value)
            except ValueError:
                error_dialog = ErrorDialog(self.parameters[i].name)
                error_dialog.exec()
                return

        for i in self.parameters.keys():
            new_value = self.line_edits[i].text()
            if new_value != "":
                new_value_float = float(self.line_edits[i].text())
                self.parameters[i].set_current_value(new_value_float)
        self.calculate_callback()
        self.close()

    def default_button_pushed(self):
        self.adjustSize()


class ErrorDialog(QtWidgets.QDialog, error_ui.Ui_Dialog):
    def __init__(self, error_field_name: str):
        super().__init__()
        self.setupUi(self)

        line = f"Incorrect value for {error_field_name}!\nPlease enter floating number or nothing."
        self.label.setText(line)

        self.push_button.clicked.connect(self.ok_button_pushed)

    def ok_button_pushed(self):
        self.close()
