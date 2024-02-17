import ui_elements.qt_designer_ui.file_selection_menu_ui as menu_ui
from PyQt5 import QtWidgets


class FileSelectionMenuDialog(QtWidgets.QDialog, menu_ui.Ui_Dialog):
    def __init__(self, file_name_dictionary, ok_callback_function):
        self.dictionary = file_name_dictionary
        self.ini_data_file_name = file_name_dictionary["initial"]
        self.height_file_name = file_name_dictionary["height"]
        self.max_height_file_name = file_name_dictionary["max_height"]

        self.ok_callback_function = ok_callback_function

        super().__init__()
        self.setupUi(self)

        self.title = "Select files to load"

        self.label_ini_data_file_name.setText(self.ini_data_file_name)
        self.label_height_file_name.setText(self.height_file_name)
        self.label_max_height_file_name.setText(self.max_height_file_name)

        self.label_ini_data_file_name.setMaximumWidth(100)
        self.label_height_file_name.setMaximumWidth(100)
        self.label_max_height_file_name.setMaximumWidth(100)

        self.push_button_initial.clicked.connect(lambda: self.open_file_name_dialog("initial"))
        self.push_button_height.clicked.connect(lambda: self.open_file_name_dialog("height"))
        self.push_button_max_height.clicked.connect(lambda: self.open_file_name_dialog("max_height"))

        self.push_button_ok.clicked.connect(self._ok_button_pushed)

    def open_file_name_dialog(self, file):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                             "All Files (*);;Python Files (*.py)", options=options)

        if file_name:
            if file == "initial":
                label = self.label_ini_data_file_name
                self.ini_data_file_name = file_name
            elif file == "height":
                label = self.label_height_file_name
                self.height_file_name = file_name
            elif file == "max_height":
                label = self.label_max_height_file_name
                self.max_height_file_name = file_name
            else:
                return
            label.setText(file_name)

    def _ok_button_pushed(self):
        self.dictionary["initial"] = self.ini_data_file_name
        self.dictionary["height"] = self.height_file_name
        self.dictionary["max_height"] = self.max_height_file_name

        self.close()
        self.ok_callback_function()
