import ui_elements.qt_designer_ui.static_settings_ui as settings_ui
import ui_elements.qt_designer_ui.static_results_widget_ui as results_widget_ui
import ui_elements.qt_designer_ui.error_dialog as error_ui
from ui_elements.collapsible_box import CollapsibleBox
from data_entry import DataEntry
from PyQt5 import QtWidgets


class StaticSettingsDialog(QtWidgets.QDialog, settings_ui.Ui_Dialog):
    def __init__(self, parameters: dict[str, DataEntry], parameters_to_menu_section, calculate_callbacks: list):
        self.parameters = parameters
        self.parameters_to_menu = parameters_to_menu_section
        self.calculate_callbacks = calculate_callbacks

        super().__init__()
        self.setupUi(self)

        self.line_edits: dict[str, QtWidgets.QLineEdit] = {}
        self.__set_layout()
        self.push_button_calculate.clicked.connect(self.calculate_button_pushed)
        self.push_button_close.clicked.connect(self.close)
        self.push_button_default.clicked.connect(self.default_button_pushed)

        self.results_widget = None

    def __set_layout(self):
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)

        fault_parameters = [self.parameters[p] for p in
                            self.parameters_to_menu["fault"]]
        calculation_parameters = [self.parameters[p] for p in
                                  self.parameters_to_menu["calculation"]]
        coordinates_parameters = [self.parameters[p] for p in
                                  self.parameters_to_menu["coordinates"]]

        coordinates_label = QtWidgets.QLabel("Coordinates parameters")
        coordinates_container = QtWidgets.QWidget()
        coordinates_container.setContentsMargins(0, 0, 0, 0)
        coordinates_container.setLayout(self.__layout_parameters(coordinates_parameters))

        fault_label = QtWidgets.QLabel("Fault parameters")
        fault_container = QtWidgets.QWidget()
        fault_container.setContentsMargins(0, 0, 0, 0)
        fault_container.setLayout(self.__layout_parameters(fault_parameters))

        calculation_container = CollapsibleBox("Calculation parameters")
        calculation_container.setContentsMargins(0, 0, 0, 0)
        calculation_container.set_content_layout(self.__layout_parameters(calculation_parameters))

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        parameters_layout = QtWidgets.QVBoxLayout()
        parameters_layout.addWidget(coordinates_label)
        parameters_layout.addWidget(coordinates_container)
        parameters_layout.addWidget(fault_label)
        parameters_layout.addWidget(fault_container)
        parameters_layout.addWidget(line)
        parameters_layout.addWidget(calculation_container)
        self.parameters_widget.setLayout(parameters_layout)

        self.scroll_area.setMinimumHeight(int((fault_container.height())))

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

        for callback in self.calculate_callbacks:
            callback()
        # self.close()

    def default_button_pushed(self):
        for parameter in self.parameters.values():
            parameter.set_current_value(parameter.default_value)

            line_edit = self.line_edits[parameter.name]
            line_edit.setPlaceholderText(str(parameter.get_current_value()))

    def add_result_values(self, v0, ve, ets, u_min, u_max):
        if self.results_widget is not None:
            self.verticalLayout.removeWidget(self.results_widget)

        self.results_widget = ResultsWidget(v0, ve, ets, u_min, u_max)
        self.verticalLayout.insertWidget(1, self.results_widget)


class ResultsWidget(QtWidgets.QWidget, results_widget_ui.Ui_Form):
    def __init__(self, v0, ve, ets, u_min, u_max):
        super().__init__()
        self.setupUi(self)

        self.label_v0_val.setText(format(v0, '.3e') + " km3")
        self.label_ve_val.setText(format(ve, '.3e') + " km3")
        self.label_ets_val.setText(format(ets, '.3e'))
        self.label_umin_val.setText(format(u_min, '.3e') + " m")
        self.label_umax_val.setText(format(u_max, '.3e') + " m")


class ErrorDialog(QtWidgets.QDialog, error_ui.Ui_Dialog):
    def __init__(self, error_field_name: str):
        super().__init__()
        self.setupUi(self)

        line = f"Incorrect value for {error_field_name}!\nPlease enter floating number or nothing."
        self.label.setText(line)

        self.push_button.clicked.connect(self.ok_button_pushed)

    def ok_button_pushed(self):
        self.close()
