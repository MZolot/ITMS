import ui_elements.qt_designer_ui.error_dialog_ui as error_ui
from PyQt5 import QtWidgets


class ErrorDialog(QtWidgets.QDialog, error_ui.Ui_Dialog):
    def __init__(self, text: str):
        super().__init__()
        self.setupUi(self)
        self.label.setText(text)
        self.push_button.clicked.connect(self.ok_button_pushed)
        self.adjustSize()

    def ok_button_pushed(self):
        self.close()
