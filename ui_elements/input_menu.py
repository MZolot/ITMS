import ui_elements.input_menu_ui as menu_ui
from PyQt5 import QtWidgets


class InputMenuDialog(QtWidgets.QDialog, menu_ui.Ui_Dialog):
    def __init__(self, data_elements, title):
        self.data_elements = data_elements

        super().__init__()
        self.setupUi(self)
        self.line_edits = []
        self.title = title
        self.__set_layout(self.data_elements)
        self.pushButton_ok.clicked.connect(self._ok_button_pushed)

    def __set_layout(self, data_elements):
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

    def _ok_button_pushed(self):
        for i in range(len(self.data_elements)):
            new_value = self.line_edits[i].text()
            if new_value != "":
                self.data_elements[i].set_current_value(new_value)
        self.close()


class SourceMenuDialog(InputMenuDialog):
    def __init__(self, data_elements, title, app):
        super().__init__(data_elements, title)
        self.app = app

    def _ok_button_pushed(self):
        super()._ok_button_pushed()
        self.app.draw_source()
